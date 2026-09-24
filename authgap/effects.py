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
from .catalog.statements import HTTP_METHOD_ARG_SUFFIXES, HTTP_METHOD_SUFFIXES
from .ir import (
    REMOTE,
    RESOLVED,
    Argv,
    Atom,
    Obj,
    Path,
    Prin,
    Prov,
    Seq,
    Str,
    Value,
    opaque,
    prov_merge,
    value_join,
)
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
    #: FS_WRITE の性質（D32）: True = 削除・上書き、False = 追記、None = 不明。
    #: `destructiveHint==false` に対する CONTRADICTION は False 以外に立つ。
    destructive: Optional[bool] = None
    #: 非 DB の `.execute()` の機械判定結果（`db` / `db_unresolved`）。
    db_rule: Optional[str] = None
    #: `open` 系の mode（確度が resolved の定数だけ。読めなければ `None`）。§7.4 の追記の判定（D56）。
    fs_mode: Optional[str] = None
    #: HTTP メソッド（大文字）。sink 名の末尾、または `*.request` の第 1 引数の定数（D56）。
    http_method: Optional[str] = None
    #: HTTP メソッドの値がモデル由来か（原理 3-a。D56）。
    http_method_model: bool = False
    #: この行が依存する sink 表の行（triage 表と突き合わせるため）。
    required_by: tuple[str, ...] = ()

    @property
    def sql_head(self) -> Optional[str]:
        """DB 効果の SQL の先頭語（大文字）。**定数に解決できたときだけ**。読めなければ `None`。

        `sub_kind` の `DB_WRITE` は「読み取り語で始まらない」という意味で `PRAGMA` / `BEGIN` も
        含むので、矛盾の判定はこちらを使う（`dparse.contradiction`、D55）。`_sub_kind` と同じく
        `Value.const`（確度が resolved の定数）だけを読む。
        """
        if self.kind != "DB":
            return None
        return _sql_head_of(self.slots.get("sql"))

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
        if self.kind == "FS_WRITE":
            d["destructive"] = self.destructive
        if self.db_rule:
            d["db_rule"] = self.db_rule
        if self.sql_head:
            d["sql_head"] = self.sql_head
        if self.fs_mode is not None:
            d["fs_mode"] = self.fs_mode
        if self.http_method:
            d["http_method"] = self.http_method
        if self.http_method_model:
            d["http_method_model"] = True
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
    if ref.kws:
        # **渡されたキーワードだけを合流する**（D59、O37。`body ← data|json`）。
        got = [ev.kwargs[k] for k in ref.kws if k in ev.kwargs]
        if not got:
            return None
        out = got[0]
        for v in got[1:]:
            out = value_join(out, v)
        return out
    base: Optional[Value]
    if ref.pos is not None:
        base = ev.args[ref.pos] if ref.pos < len(ev.args) else None
        if base is None and ref.kw is not None:
            base = ev.kwargs.get(ref.kw)  # 位置に無ければ仮引数名のキーワードで引く（F8）
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


def _mode_const(ev: CallEvent, row: SinkRow) -> Optional[str]:
    """`open` 系の mode の定数（引数が無ければ既定の `"r"`）。読めなければ `None`（D56）。"""
    node: Optional[Value] = None
    if row.mode_kw and row.mode_kw in ev.kwargs:
        node = ev.kwargs[row.mode_kw]
    elif row.mode_pos is not None and row.mode_pos < len(ev.args):
        node = ev.args[row.mode_pos]
    if node is None:
        return "r"
    const = node.const
    return const if isinstance(const, str) else None


def _http_method(suffix: str, ev: CallEvent) -> tuple[Optional[str], bool]:
    """HTTP メソッド（大文字）と、それがモデル由来か（§7.6、D56）。

    sink 名の末尾がメソッド名ならそれ。末尾が `request` なら第 1 引数（キーワード `method` も見る）を
    読み、定数なら大文字、モデル由来なら `(None, True)`、それ以外は `(None, False)`（読めない）。
    """
    suffix = suffix.lower()
    if suffix in HTTP_METHOD_SUFFIXES:
        return suffix.upper(), False
    if suffix in HTTP_METHOD_ARG_SUFFIXES:
        v = ev.kwargs.get("method") if "method" in ev.kwargs else (ev.args[0] if ev.args else None)
        if v is None:
            return None, False
        c = v.const
        if isinstance(c, str):
            return c.upper(), False
        # 「モデルが選べる」は主体 MODEL かつ確度 resolved（D57、§9.3）。opaque は読めない扱い。
        return None, v.prin is Prin.MODEL and v.prov.kind == "resolved"
    return None, False


def _mode_destructive(ev: CallEvent, row: SinkRow) -> Optional[bool]:
    """`open(path, mode)` の mode から削除・上書き型か追記型かを決める（D32）。

    `w` / `+` を含めば上書き（True）、`a` / `x` だけなら追記（False）、
    **読めなければ None**（呼び出し側で True 扱い = 推定で clean にしない）。
    """
    node: Optional[Value] = None
    if row.mode_kw and row.mode_kw in ev.kwargs:
        node = ev.kwargs[row.mode_kw]
    elif row.mode_pos is not None and row.mode_pos < len(ev.args):
        node = ev.args[row.mode_pos]
    if node is None:
        return False  # 既定 "r"（書き込みではない）
    const = node.const
    if isinstance(const, str):
        if "w" in const or "+" in const:
            return True
        if "a" in const or "x" in const:
            return False
        return False
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


def _sql_head_of(sql: Optional[Value]) -> Optional[str]:
    """定数 SQL の先頭語（大文字、末尾の `;` を除く）。空白だけ・非定数なら `None`。"""
    text = sql.const if sql is not None else None
    if not isinstance(text, str):
        return None
    parts = text.split(None, 1)
    return parts[0].upper().rstrip(";") if parts else None


def sql_text(sql: Optional[Value]) -> tuple[Optional[str], bool]:
    """SQL の定数の文字列と、それが全体か（D57、§9.4）。

    全体が確度 resolved の定数なら `(文字列, True)`。連結（`Str`）で先頭の部分が resolved の定数なら
    `(その接頭辞, False)`。どちらでもなければ `(None, False)`。
    """
    if sql is None:
        return None, False
    if isinstance(sql.const, str):
        return sql.const, True
    if isinstance(sql.shape, Str) and sql.shape.parts:
        first = sql.shape.parts[0].const
        if isinstance(first, str):
            return first, False
    return None, False


def sql_head_of_text(text: Optional[str], complete: bool) -> Optional[str]:
    """先頭語（大文字）。接頭辞のときは**最初の語の後に空白がある**ときだけ決める（`"UPD" + x` は決めない）。"""
    if not isinstance(text, str):
        return None
    stripped = text.lstrip()
    parts = stripped.split(None, 1)
    if not parts:
        return None
    if not complete and len(parts) < 2 and not stripped[len(parts[0]):][:1].isspace():
        return None
    return parts[0].upper().rstrip(";")


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
            # **空白全般で切る。**`split(" ", 1)` だと `"\n  SELECT\n    id, ..."` のような
            # 改行で始まる複数行 SQL が `head == "SELECT\n"` になり、読み取り語の一覧に
            # 当たらず `DB_WRITE` に落ちていた（誤警報の向き。D41 の B1）。
            parts = text.split(None, 1)
            if not parts:
                # 空白だけの SQL は読み / 書きが決まらない。**`DB_WRITE` に倒さない**
                # （規則 4。母集団 v2 に該当 0 件なので観測は変わらない）。
                return None
            head = parts[0].upper()
            # **`DB_WRITE` は「読み取り語で始まらない」という意味であって「データを変更する」
            # ではない。** `PRAGMA` / `BEGIN` / `COMMIT` / `ROLLBACK` もここに入る
            # （母集団 v2 で 105 件）。`readOnlyHint` の矛盾判定に**そのまま使ってはならない**
            # （D41 の B2、`docs/contradiction_matrix.md` §5）。
            # **`WITH` は読み取りとして扱うが、`WITH x AS (...) INSERT INTO ...` は書き込みで
            # ある（潜在的な誤 clear。母集団 v2 に 0 件なので憶測で直さない。O24）。**
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
    if text is not None and len(text) >= 2 and text[0] == "/" and text[1] != "/" and "://" not in text:
        # **相対 URL**（D57、O32）: 宛先はクライアントの base_url が決め、モデルが入れられるのは
        # パスとクエリだけ。`"/"` だけ・`"//"` で始まるものは分割しない（`"/" + "/evil.example/x"` は
        # `urljoin` 系で宛先が変わる。誤 clear を作らない）。
        return {"url.path": v}
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
    split = _split_url(host)
    for k, s in split.items():
        if k == "url.host" or k not in out:
            out[k] = s
    if "url.host" not in split and "url.scheme" in out:
        # 相対 URL: 宛先は受け手の base_url（`from_ctor` で `url.scheme` に入っている）から取る（D57）。
        base = _split_url(out["url.scheme"]).get("url.host")
        if base is not None:
            out["url.host"] = base
    return dict(sorted(out.items()))


# --------------------------------------------------------------------------
# 抽出
# --------------------------------------------------------------------------


#: 仕様書 1118 行目の「非 DB の `.execute()`」の対象メソッド。
#: **広げない。** `run` / `aql` のような一般的な名前を足すと FP 監査の分子が膨らむ。
DB_EXECUTE_METHODS: frozenset[str] = frozenset({"execute", "executemany"})


class EffectExtractor:
    """`CallEvent` を効果行に変える。

    `pipe` 形態のために spawn ハンドルの受け手アクセスパスを覚えておく
    （§Def 3(c)。OpenManus `Bash` がこれを要求する）。
    """

    def __init__(self) -> None:
        self.effects: list[Effect] = []
        #: 受け手アクセスパス → `(argv0 のリテラル, shell の真偽)`。
        self.spawn_handles: dict[str, tuple[Optional[str], Optional[bool]]] = {}
        #: **受け手型を DB に解決できなかった `.execute()`**（仕様書 1118 行目、O28 / D49）。
        #: `effect_fp_audit.db_only_non_db_execute` の分子。
        #: **効果には数えないが、記録はする**（規則 4。落としたものを黙って消さない）。
        self.db_unresolved: list[dict] = []

    # -- 入口 -------------------------------------------------------------

    def on_call(self, ev: CallEvent) -> None:
        n_before = len(self.effects)
        made = False
        made |= self._direct(ev)
        made |= self._proxy(ev)
        made |= self._pipe(ev)
        self._note_db_unresolved(ev, self.effects[n_before:])
        if not made:
            return

    def _note_db_unresolved(self, ev: CallEvent, new_effects: list[Effect]) -> None:
        """DB 効果にならなかった `.execute()` を記録する（仕様書 1118 行目）。

        **`effects.py` の `if db_rule != "db": return None` は到達不能である。**
        DB の proxy 行の `recv_types` はすべて `DB_RECEIVER_TYPES` の部分集合なので、
        `_from_proxy_row` に入る時点で受け手は DB 型に解決できている。
        受け手型が分からない `.execute()` は proxy 行に一致せず、**痕跡なく消えていた。**
        ここで拾う。

        **効果は作らない**（仕様の「危険効果に数えない」）。manifest の属性として残すだけで、
        verdict には影響しない。
        """
        if not isinstance(ev.node.func, ast.Attribute):
            return
        method = ev.node.func.attr
        if method not in DB_EXECUTE_METHODS:
            return
        if any(e.kind == "DB" for e in new_effects):
            return
        classes = tuple(sorted(getattr(ev.receiver.shape, "classes", ())) if ev.receiver else ())
        self.db_unresolved.append({
            "method": method,
            "relpath": ev.relpath,
            "lineno": ev.lineno,
            "receiver_classes": list(classes),
        })

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

        if kind == "SPAWN" and "shell_string" in row.slots and not row.exec_mode_kw:
            # 常にシェル経由の sink（`asyncio.create_subprocess_shell` / `os.system` …）は
            # `shell=` の引数を持たないので exec_mode を明示しておく（F6 の `shell = OP/lit=True`）。
            exec_mode = {"shell": {"prin": "OP", "const": True, "source": "implicit"}}
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
        if kind == "FS_WRITE":
            if row.mode_kw is not None or row.mode_pos is not None:
                eff.destructive = _mode_destructive(ev, row)
                eff.fs_mode = _mode_const(ev, row)
            else:
                eff.destructive = row.destructive
        if kind == "NET":
            eff.http_method, eff.http_method_model = _http_method(key.rsplit(".", 1)[-1], ev)
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
            # proxy の SPAWN は既定で argv 実行（git）だが、`shell_string` slot を持つ行
            # （paramiko `exec_command`）はシェル実行。const False を一律に付けると
            # `_is_argv_exec` が真になり、シェル文字列の検証子が strong-token に上がる（レビュー g1）。
            exec_mode={"shell": {"prin": "OP", "const": "shell_string" in slots, "source": "proxy"}}
            if kind == "SPAWN"
            else {},
            resolution=_resolution_of(slots, ev.receiver, ev.by_name),
            witness_chain=ev.chain,
            db_rule=db_rule,
            required_by=row.required_by,
            **dict(zip(("http_method", "http_method_model"), _http_method(method, ev), strict=True))
            if kind == "NET"
            else {},
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
