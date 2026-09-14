"""Def 3: 効果の抽出。直接 / proxy / pipe の 3 形態を扱う。

`val` エンジンが出す :class:`authgap.val.CallEvent` を sink 表に照合して
効果行を作る。**責務の境界**: val は値を決め、ここは「その値がどの制御位置に
入るか」を決める。等級づけは Def 5 のゲート採点器が行う。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Any, Optional

from .catalog.sinks import (
    DIRECT_SINKS,
    PIPE_HANDLE_SOURCES,
    PIPE_SINKS,
    POLICY_FILE_PATTERNS,
    PROXY_SINKS,
    ArgRef,
    ProxyRow,
    SinkRow,
    db_execute_rule,
    is_interpreter,
)
from .ir import REMOTE, RESOLVED, Argv, Atom, Obj, Path, Prin, Prov, Seq, Str, Value, opaque, prov_merge
from .val import CallEvent

#: 効果本体が木の外（別プロセス / HTTP の向こう）にある受け手型。
#:
#: **この集合は狭く取る。** `remote` 率は §1 の測定点であり関門ではないので、
#: 広く取って数字を作らない。広げるときは F0c(iii) の定義も同時に直すこと。
REMOTE_RECEIVER_TYPES: frozenset[str] = frozenset(
    {
        "paramiko.SSHClient",
        "docker.models.containers.Container",
        "kubernetes.client.CoreV1Api",
    }
)


@dataclass
class Effect:
    """効果行 1 つ。`e = (kind, site, slots)`（Def 3）。"""

    kind: str
    site: str
    form: str
    lineno: int
    relpath: str
    #: **入口ユニットの CFG 上でこの効果に対応する行。**
    #: `lineno` は効果そのものの行（別ファイルでありうる）、`entry_lineno` は
    #: 入口から見た呼び出し位置。支配判定は後者で行う（§2.5.4 の連結経路）。
    entry_lineno: int = 0
    slots: dict[str, Value] = field(default_factory=dict)
    sub_kind: Optional[str] = None
    #: `shell` の値（`SPAWN` のみ）。config-conditional なら値がその atom を指す。
    exec_mode: dict[str, Any] = field(default_factory=dict)
    resolution: Prov = RESOLVED
    #: 入口からこの効果までの呼び出し経路。
    witness_chain: tuple[str, ...] = ()
    #: 位置ごとの shape の出所（`annotation` なら注釈由来）。
    shape_from: dict[str, str] = field(default_factory=dict)
    #: FS_WRITE の path がポリシーファイルに解決される（**マニフェスト属性。
    #: verdict を持たない**）。
    write_policy: bool = False
    #: 非 DB の `.execute()` の機械判定結果（`db` / `db_unresolved`）。
    db_rule: Optional[str] = None
    #: この行が依存する sink 表の行（triage 表と突き合わせるため）。
    required_by: tuple[str, ...] = ()

    def to_json(self) -> dict:
        d: dict[str, Any] = {
            "kind": self.kind,
            "site": self.site,
            "form": self.form,
            "lineno": self.lineno,
            "entry_lineno": self.entry_lineno,
            "relpath": self.relpath,
            "slots": {k: v.to_json() for k, v in sorted(self.slots.items())},
            "resolution": self.resolution.kind,
        }
        if self.resolution.reasons:
            d["resolution_reasons"] = list(self.resolution.reasons)
        if self.sub_kind:
            d["sub_kind"] = self.sub_kind
        if self.exec_mode:
            d["exec_mode"] = self.exec_mode
        if self.witness_chain:
            d["witness_chain"] = list(self.witness_chain)
        if self.shape_from:
            d["shape_from"] = dict(sorted(self.shape_from.items()))
        if self.write_policy:
            d["write_policy"] = True
        if self.db_rule:
            d["db_rule"] = self.db_rule
        if self.required_by:
            d["required_by"] = list(self.required_by)
        return d

    def control_slots(self) -> dict[str, Value]:
        """制御位置（Def 3 の slot 語彙にある位置）だけを返す。

        **省略された既定引数の slot は含まない**（§6 の opaque 率の分母規則）。
        """
        return dict(self.slots)


# --------------------------------------------------------------------------
# 照合
# --------------------------------------------------------------------------


def _suffix_match(dotted: Optional[str], table: dict) -> Optional[str]:
    """dotted 名を sink 表に照合する。完全一致を優先し、次に末尾一致。"""
    if dotted is None:
        return None
    if dotted in table:
        return dotted
    last2 = ".".join(dotted.split(".")[-2:])
    if last2 in table:
        return last2
    return None


def _arg_value(ref: ArgRef, ev: CallEvent) -> Optional[Value]:
    if ref.proj == "const":
        return Value(Prin.OP, RESOLVED, Atom(const=ref.const_value))
    if ref.proj == "receiver":
        return ev.receiver
    if ref.proj == "varargs":
        if not ev.args:
            return None
        return Value(
            _max_prin(ev.args),
            prov_merge(*[a.prov for a in ev.args]),
            Seq(tuple(ev.args)),
            frozenset(),
            frozenset().union(*[a.roots for a in ev.args]),
        )
    base: Optional[Value]
    if ref.pos is not None:
        base = ev.args[ref.pos] if ref.pos < len(ev.args) else None
    else:
        base = ev.kwargs.get(ref.kw or "")
    if base is None:
        return None
    if ref.proj == "elem0":
        return _first_element(base)
    if ref.proj == "all_elems":
        return base
    return base


def _first_element(v: Value) -> Value:
    if isinstance(v.shape, (Seq, Argv)) and v.shape.elems:
        return v.shape.elems[0]
    if isinstance(v.shape, (Seq, Argv)) and v.shape.tail is not None:
        return v.shape.tail
    if isinstance(v.shape, Str) and v.shape.parts:
        return v.shape.parts[0]
    return v


def _max_prin(vals: list[Value]) -> Prin:
    out = Prin.USER
    for v in vals:
        if v.prin > out:
            out = v.prin
    return out


def _resolution_of(slots: dict[str, Value], receiver: Optional[Value], by_name: bool = False) -> Prov:
    """行の確度。**`remote` は行単位**（F7 の明記事項）。

    :param by_name: 受け手型が分からず**末尾名だけで**木内メソッドへ降りた経路の上の行。
        効果は落とさずに出すが、到達の根拠が名前一致なので `opaque(unresolved)` を合流する
        （D17。落とすと langroid の `compute_from_docs` の eval のような真の経路が消える）。
    """
    if receiver is not None and isinstance(receiver.shape, Obj):
        if set(receiver.shape.classes) & REMOTE_RECEIVER_TYPES:
            return REMOTE
    out = prov_merge(*[v.prov for v in slots.values()]) if slots else RESOLVED
    return prov_merge(out, opaque("unresolved")) if by_name else out


def _mode_is_write(ev: CallEvent, row: SinkRow) -> Optional[bool]:
    """`open(path, mode)` の mode から FS_READ / FS_WRITE を分ける。

    **判定できなければ None**（推定で片側に倒さない）。
    """
    node: Optional[Value] = None
    if row.mode_kw and row.mode_kw in ev.kwargs:
        node = ev.kwargs[row.mode_kw]
    elif row.mode_pos is not None and row.mode_pos < len(ev.args):
        node = ev.args[row.mode_pos]
    if node is None:
        return False  # 既定は "r"
    const = node.const
    if isinstance(const, str):
        return any(c in const for c in "wax+")
    return None


def _exec_mode(ev: CallEvent, row: SinkRow) -> tuple[Optional[bool], dict]:
    """`shell=` の値。`(確定した真偽 or None, exec_mode の記録)`。"""
    if not row.exec_mode_kw:
        return None, {}
    v = ev.kwargs.get(row.exec_mode_kw)
    if v is None:
        return False, {"shell": {"prin": "OP", "const": False, "source": "default"}}
    const = v.const
    if isinstance(const, bool):
        return const, {"shell": {"prin": v.prin.name, "const": const, "source": "literal"}}
    return None, {"shell": {"prin": v.prin.name, "source": "config-conditional", "value": v.to_json()}}


def _sub_kind(kind: str, slots: dict[str, Value]) -> Optional[str]:
    """副 kind（Def 5-b の kind 粒度の前提条件）。"""
    if kind == "SPAWN":
        argv = slots.get("argv0")
        if argv is not None and argv.is_literal():
            return "SPAWN_CONST_ARGV"
        return "SPAWN_MODEL_ARGV"
    if kind == "DB":
        sql = slots.get("sql")
        text = sql.const if sql is not None else None
        if isinstance(text, str):
            head = text.strip().split(" ", 1)[0].upper()
            return "DB_READ" if head in ("SELECT", "SHOW", "EXPLAIN", "DESCRIBE", "WITH") else "DB_WRITE"
        return None
    return kind if kind in ("EXEC", "NET", "FS_READ", "FS_WRITE", "DISPATCH") else None


def _is_policy_path(v: Optional[Value]) -> bool:
    """書き込み先が方針ファイルに見えるか（`write_policy`）。

    **警報の向きの判定なので、確度が resolved でない値に残った定数も読む**（`shape.const`）。
    D17 改訂 5 で `Value.const` が resolved の値の定数しか返さなくなったが、再束縛されうる
    方針ファイルのパスへの書き込みを見落とさないため。
    """
    if v is None:
        return False
    text = v.shape.const if isinstance(v.shape, Atom) else None
    if not isinstance(text, str):
        if isinstance(v.shape, (Str, Path)):
            parts = list(getattr(v.shape, "parts", ())) + list(getattr(v.shape, "segs", ()))
            consts = [p.shape.const for p in parts if isinstance(p.shape, Atom)]
            text = "".join(c for c in consts if isinstance(c, str))
        else:
            return False
    return any(pat in str(text) for pat in POLICY_FILE_PATTERNS)


def _receiver_typed_key(ev: CallEvent) -> Optional[str]:
    """受け手の値の形から sink 名を作る（D17）。

    `resolve_call_name` は受け手が局所変数だと `None` を返すので、`p.write_text(...)` の
    `p` が `Path` 形でも sink 表に当たらず、**FS 効果を落としていた**（野外 NOE[1,10]）。
    """
    if ev.receiver is None or not isinstance(ev.node.func, ast.Attribute):
        return None
    method = ev.node.func.attr
    if isinstance(ev.receiver.shape, Path):
        key = f"pathlib.Path.{method}"
        return key if key in DIRECT_SINKS else None
    if isinstance(ev.receiver.shape, Obj):
        for cls in sorted(ev.receiver.shape.classes):
            key = f"{cls}.{method}"
            if key in DIRECT_SINKS:
                return key
    return None


def _concat_values(vals: list[Value]) -> Value:
    if len(vals) == 1:
        return vals[0]
    prin = Prin.OP
    roots: frozenset[str] = frozenset()
    for v in vals:
        if v.prin > prin:
            prin = v.prin
        roots |= v.roots
    return Value(prin, prov_merge(*[v.prov for v in vals]), Str(tuple(vals)), frozenset(), roots)


def _has_placeholder(text: str) -> bool:
    """書式テンプレートのプレースホルダ（`%s` / `{}` / `{name}`）を含むか。"""
    return "%" in text or "{" in text or "}" in text


def _split_url(v: Value) -> dict[str, Value]:
    """§2.6 の URL slot 分割規則。

    * url の値が `Str(parts)` で parts[0] がリテラルであり、`://` を含み、その後に
      `/` `?` `#` のいずれかを含む → `url.scheme` と `url.host` をそのリテラルから切り出し
      `principal = OP`。残り（リテラルの残部と後続の part）は `url.path`。
      権威部の終端が**次のリテラルの先頭**にある形（`"https://api.x" + "/search"`）も同じ。
    * parts[0] が非リテラル → `url.host = parts[0]`（その part の主体）。残りは `url.path`。
      **ただし後続のリテラルに `://` があれば分割しない**（`f"{proto}://{host}/x"` で
      host を proto の主体にすると MODEL の host を OP と誤る。false-clean を作らない）。
    * それ以外（権威部の終端がリテラル内に無い、相対 URL など）は分割しない。
    """
    if isinstance(v.shape, Str):
        parts = list(v.shape.parts)
        tail = v.shape.tail
    else:
        parts, tail = [v], None
    if not parts:
        return {"url.host": v}
    first, rest = parts[0], parts[1:] + ([tail] if tail is not None else [])
    text = first.const if isinstance(first.const, str) else None
    if text is not None:
        i = text.find("://")
        if i < 0:
            return {"url.host": v}
        after = text[i + 3 :]
        cuts = [after.index(c) for c in "/?#" if c in after]
        if cuts:
            cut = min(cuts)
        elif rest and isinstance(rest[0].const, str) and rest[0].const[:1] in ("/", "?", "#"):
            cut = len(after)
        else:
            return {"url.host": v}
        if _has_placeholder(text[:i]) or _has_placeholder(after[:cut]):
            # 書式テンプレート（`"%s://%s/api" % ...` / `"https://{}/x".format(...)`）の
            # プレースホルダは host のリテラルではない（D17 改訂 2。切り出すと MODEL の host を OP と誤る）。
            return {"url.host": v}
        out = {
            "url.scheme": Value(Prin.OP, RESOLVED, Atom(const=text[:i])),
            "url.host": Value(Prin.OP, RESOLVED, Atom(const=after[:cut])),
        }
        remainder = ([Value(Prin.OP, RESOLVED, Atom(const=after[cut:]))] if after[cut:] else []) + rest
        if remainder:
            out["url.path"] = _concat_values(remainder)
        return out
    authority_ends = bool(rest) and isinstance(rest[0].const, str) and rest[0].const[:1] in ("/", "?", "#")
    if authority_ends and not any(isinstance(p.const, str) and "://" in p.const for p in rest):
        # 直後が `/` `?` `#` で始まるリテラルのときだけ、権威部の終端が part の境界にあると言える。
        # そうでなければ（`f"{prefix}{host}/v1"`）host がどの part に入るか分からない（D17 改訂 2）。
        return {"url.host": first, "url.path": _concat_values(rest)}
    return {"url.host": v}


def _split_url_slots(slots: dict[str, Value]) -> dict[str, Value]:
    """`url.host` に束縛された URL 全体を §2.6 の規則で分割する。既存の slot は上書きしない。"""
    host = slots.get("url.host")
    if host is None:
        return slots
    out = {k: s for k, s in slots.items() if k != "url.host"}
    for k, s in _split_url(host).items():
        if k == "url.host" or k not in out:
            out[k] = s
    return dict(sorted(out.items()))


# --------------------------------------------------------------------------
# 抽出
# --------------------------------------------------------------------------


class EffectExtractor:
    """`CallEvent` を効果行に変える。

    `pipe` 形態のために spawn ハンドルの受け手アクセスパスを覚えておく
    （§Def 3(c)。OpenManus `Bash` がこれを要求する）。
    """

    def __init__(self) -> None:
        self.effects: list[Effect] = []
        #: 受け手アクセスパス → `(argv0 のリテラル, shell の真偽)`。
        self.spawn_handles: dict[str, tuple[Optional[str], Optional[bool]]] = {}

    # -- 入口 -------------------------------------------------------------

    def on_call(self, ev: CallEvent) -> None:
        made = False
        made |= self._direct(ev)
        made |= self._proxy(ev)
        made |= self._pipe(ev)
        if not made:
            return

    # -- (a) 直接 ---------------------------------------------------------

    def _direct(self, ev: CallEvent) -> bool:
        key = _suffix_match(ev.dotted, DIRECT_SINKS) or _receiver_typed_key(ev)
        if key is None:
            return False
        made = False
        for row in DIRECT_SINKS[key]:
            eff = self._from_direct_row(ev, row, key)
            if eff is not None:
                self.effects.append(eff)
                made = True
        # pipe ハンドルの登録（Def 3(c)）
        if key in PIPE_HANDLE_SOURCES:
            self._register_handle(ev, key)
        return made

    def _from_direct_row(self, ev: CallEvent, row: SinkRow, key: str) -> Optional[Effect]:
        kind = row.kind
        slots: dict[str, Value] = {}
        exec_mode: dict = {}

        if row.exec_mode_kw:
            shell, exec_mode = _exec_mode(ev, row)
            if shell is True:
                binding = row.slots_shell
            elif shell is False:
                binding = row.slots_argv
            else:
                # **確定しないので 2 行出す**（F3 の受け入れ条件）。
                a = self._materialise(ev, row, {**row.slots, **row.slots_shell}, kind, exec_mode, key)
                b = self._materialise(ev, row, {**row.slots, **row.slots_argv}, kind, exec_mode, key)
                if a is not None:
                    self.effects.append(a)
                return b
            slots.update(row.slots)
            slots.update(binding)
            return self._materialise(ev, row, slots, kind, exec_mode, key)

        if row.mode_kw is not None or row.mode_pos is not None:
            is_write = _mode_is_write(ev, row)
            if is_write is None:
                # どちらか分からない。**両方出す**（clean に潰さない）。
                a = self._materialise(ev, row, dict(row.slots), "FS_READ", {}, key)
                if a is not None:
                    self.effects.append(a)
                return self._materialise(ev, row, dict(row.slots), "FS_WRITE", {}, key)
            kind = "FS_WRITE" if is_write else "FS_READ"

        return self._materialise(ev, row, dict(row.slots), kind, exec_mode, key)

    def _materialise(
        self, ev: CallEvent, row: SinkRow, binding: dict[str, ArgRef], kind: str, exec_mode: dict, key: str
    ) -> Optional[Effect]:
        slots: dict[str, Value] = {}
        for slot, ref in sorted(binding.items()):
            v = _arg_value(ref, ev)
            if v is not None:
                slots[slot] = v
        if not slots:
            return None
        if kind == "NET":
            slots = _split_url_slots(slots)
        eff = Effect(
            kind=kind,
            site=key,
            form="direct",
            lineno=ev.lineno,
            entry_lineno=ev.entry_site or ev.lineno,
            relpath=ev.relpath,
            slots=slots,
            sub_kind=_sub_kind(kind, slots),
            exec_mode=exec_mode,
            resolution=_resolution_of(slots, ev.receiver, ev.by_name),
            witness_chain=ev.chain,
            write_policy=(kind == "FS_WRITE" and _is_policy_path(slots.get("path"))),
            required_by=row.required_by,
        )
        return eff

    # -- (b) proxy --------------------------------------------------------

    def _proxy(self, ev: CallEvent) -> bool:
        if ev.receiver is None or not isinstance(ev.receiver.shape, Obj):
            return False
        method = ev.node.func.attr if isinstance(ev.node.func, ast.Attribute) else None
        if method is None:
            return False
        classes = {c for c in ev.receiver.shape.classes}
        made = False
        for row in PROXY_SINKS:
            if not (classes & set(row.recv_types)):
                continue
            if row.method != "*" and row.method != method:
                continue
            eff = self._from_proxy_row(ev, row, method)
            if eff is not None:
                self.effects.append(eff)
                made = True
        return made

    def _from_proxy_row(self, ev: CallEvent, row: ProxyRow, method: str) -> Optional[Effect]:
        slots: dict[str, Value] = {}
        for slot, ref in sorted(row.slots.items()):
            v = _arg_value(ref, ev)
            if v is not None:
                slots[slot] = v
        # **ctor 引数の slot 束縛**（A1 が成立する唯一の機構）。
        fields = dict(ev.receiver.shape.fields) if isinstance(ev.receiver.shape, Obj) else {}
        for slot, field_name in sorted(row.from_ctor.items()):
            if field_name in fields:
                slots[slot] = fields[field_name]
        if row.kind == "SPAWN" and "argv0" not in slots and "git.cmd.Git" in set(
            getattr(ev.receiver.shape, "classes", ())
        ):
            slots["argv0"] = Value(Prin.OP, RESOLVED, Atom(const="git"))
        if not slots:
            return None
        kind = row.kind
        if kind == "NET":
            slots = _split_url_slots(slots)
        db_rule = None
        if kind == "DB" and method in ("execute", "executemany"):
            db_rule = db_execute_rule(frozenset(getattr(ev.receiver.shape, "classes", ())))
            if db_rule != "db":
                return None
        site = f"{sorted(row.recv_types)[0]}.{method}"
        return Effect(
            kind=kind,
            site=site,
            form="proxy",
            lineno=ev.lineno,
            entry_lineno=ev.entry_site or ev.lineno,
            relpath=ev.relpath,
            slots=slots,
            sub_kind=row.sub_kind or _sub_kind(kind, slots),
            exec_mode={"shell": {"prin": "OP", "const": False, "source": "proxy"}}
            if kind == "SPAWN"
            else {},
            resolution=_resolution_of(slots, ev.receiver, ev.by_name),
            witness_chain=ev.chain,
            db_rule=db_rule,
            required_by=row.required_by,
        )

    # -- (c) pipe ---------------------------------------------------------

    def _register_handle(self, ev: CallEvent, key: str) -> None:
        """spawn の戻り値が束縛される先を覚える。

        呼び出し式の親（代入先）は val 側が env に入れるので、ここでは
        受け手アクセスパスを直接は知れない。**代わりに `argv0` と `shell` を
        記録し、`pipe` 照合時に受け手の `Obj.fields` から引く。**
        """
        argv0 = None
        if ev.args:
            first = _first_element(ev.args[0])
            if isinstance(first.const, str):
                argv0 = first.const
        shell = None
        v = ev.kwargs.get("shell")
        if v is not None and isinstance(v.const, bool):
            shell = v.const
        if key == "asyncio.create_subprocess_shell":
            shell = True
        if ev.receiver_path:
            self.spawn_handles[ev.receiver_path] = (argv0, shell)

    def _pipe(self, ev: CallEvent) -> bool:
        """`X.stdin.write(v)` / `X.communicate(input=v)`。

        **導入根拠は構造的理由のみで、CVE の裏付けは無い**（Def 3 の明記事項）。
        spawn が `shell=True` か argv0 がインタプリタ カタログに載るとき
        `EXEC(code_text=v)`、それ以外は `FS_WRITE(content=v)` 相当の情報行。
        """
        if not isinstance(ev.node.func, ast.Attribute):
            return False
        method = ev.node.func.attr
        recv = ev.receiver
        if recv is None or not isinstance(recv.shape, Obj):
            return False
        classes = set(recv.shape.classes)
        handle_like = any("Popen" in c or "subprocess.Process" in c for c in classes)
        if not handle_like:
            return False
        fields = dict(recv.shape.fields)

        argv0 = None
        argv = fields.get("spawn_argv")
        if argv is not None:
            first = _first_element(argv)
            if isinstance(first.const, str):
                argv0 = first.const
        shell_v = fields.get("spawn_shell")
        shell = shell_v.const if shell_v is not None else None

        made = False
        for row in PIPE_SINKS:
            want = row.method.split(".")[-1]
            if method != want:
                continue
            slots: dict[str, Value] = {}
            for slot, ref in sorted(row.slots.items()):
                v = _arg_value(ref, ev)
                if v is not None:
                    slots[slot] = v
            if not slots:
                continue
            payload = next(iter(slots.values()))
            if shell is True or is_interpreter(argv0):
                kind, slot_name = "EXEC", "code_text"
            else:
                kind, slot_name = "FS_WRITE", "content"
            self.effects.append(
                Effect(
                    kind=kind,
                    site=f"pipe:{method}",
                    form="pipe",
                    lineno=ev.lineno,
                    entry_lineno=ev.entry_site or ev.lineno,
                    relpath=ev.relpath,
                    slots={slot_name: payload},
                    sub_kind=_sub_kind(kind, {slot_name: payload}),
                    resolution=_resolution_of({slot_name: payload}, recv, ev.by_name),
                    witness_chain=ev.chain,
                    required_by=row.required_by,
                )
            )
            made = True
        return made
