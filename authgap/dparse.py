"""Def 6: 宣言権限 D の 3 層パーサ（D_kind / D_op / D_prev）。

**D_dom のパーサは書かない。** 前測で D_dom として観測された母集団は
MCP サーバ 0/141、ツールパッケージ 0/191 である。着手条件は
「F0a が手続き間深さ 3 で低レベル経路の危険効果を解決したうえで、D_dom の母集団が
非空（≥ 5 ユニット、かつ ≥ 2 リポジトリ）であることを示す」こと。満たすまで
定義・執行表・被覆規則だけを置き `r_dom = 0` として報告する（反証条件 F1）。

**層ごとに独立に評価し、弱い層が強い層の GAP を消してはならない。**
"""

from __future__ import annotations

import ast
import json
import os
from dataclasses import dataclass, field, replace
from typing import Any, Optional

from .catalog.statements import (
    FS_OPEN_SITES,
    FS_WRITEOUT_SITES,
    HTTP_IDEMPOTENT,
    HTTP_MODIFY,
    HTTP_SAFE,
    SQL_CLASS_CONNECTION,
    SQL_CLASS_MODIFY,
    SQL_CLASS_PERSISTENT,
    SQL_CLASS_READ,
    SQL_DESTRUCTIVE_HEADS,
    SQL_MODIFY_HEADS,
    SQL_NONIDEMPOTENT_HEADS,
    sql_class,
)
from .entries import Unit
from .srcindex import SourceIndex, dotted_of

# --------------------------------------------------------------------------
# D_kind（旧 D_author）: MCP annotations
# --------------------------------------------------------------------------

#: `readOnlyHint==true` が宣言する効果 kind の上界。
READ_ONLY_UPPER = frozenset({"FS_READ", "NET"})

#: 破壊的な kind（`destructiveHint==false` が宣言外にするもの）。
DESTRUCTIVE_KINDS = frozenset({"EXEC", "SPAWN", "FS_WRITE"})

#: SQL の先頭語の類は `authgap/catalog/statements.py`（D55 / D56）。


@dataclass
class DKind:
    """効果 kind の上界。**既定値による補完を禁止する。**

    annotation の不在は「非破壊の宣言」ではない。一次的根拠は MCP 公式ブログ
    （2026-03-16、untrusted hint）。
    """

    #: 宣言された上界。`None` は `⊥`（宣言が無い）。
    upper: Optional[frozenset[str]] = None
    #: 明示されたフィールド。
    explicit: tuple[str, ...] = ()
    #: 上界を動かさないが明示はされているフィールド（`r_kind` の分子に数えない）。
    present_no_bound: tuple[str, ...] = ()
    #: snake_case 別名など、protocol に届かない形。
    malformed: tuple[str, ...] = ()
    #: 読めない形（`D_unknown`）。
    unknown: bool = False
    #: `openWorldHint==true` により P0 の private-range 制限だけを解除する。
    open_world: bool = False
    #: `openWorldHint==false` の明示（D3、D56）。上界は動かさない。
    closed_world: bool = False
    #: `idempotentHint==true` の明示で、`readOnlyHint==true` が無いもの（D4、D56）。上界は動かさない。
    idempotent: bool = False

    @property
    def is_bottom(self) -> bool:
        return self.upper is None

    def covers(self, kind: str) -> bool:
        """`D_kind ⊨ kind` か。`⊥` は何も被覆しない。"""
        return self.upper is not None and kind in self.upper

    def to_json(self) -> dict:
        d: dict[str, Any] = {
            "bottom": self.is_bottom,
            "explicit": list(self.explicit),
            "present_no_bound": list(self.present_no_bound),
        }
        if self.upper is not None:
            d["upper"] = sorted(self.upper)
        if self.malformed:
            d["malformed"] = list(self.malformed)
        if self.unknown:
            d["unknown"] = True
        if self.open_world:
            d["open_world"] = True
        if self.closed_world:
            d["closed_world"] = True
        if self.idempotent:
            d["idempotent"] = True
        return d


def parse_d_kind(unit: Unit) -> DKind:
    """ユニットの annotations から D_kind を作る（Def 6）。

    低レベルハンドラ（`dispatch_annotations` を持つ）は、join した全ツールの
    宣言の**積**（:func:`meet_d_kind`）をユニット水準の D_kind にする
    （§2.9 (c)。効果ごとの帰属は `analyze.py`）。
    """
    if unit.dispatch_annotations and not unit.annotations:
        dk = meet_d_kind([d_kind_from(a, f) for a, f in unit.dispatch_annotations.values()])
    else:
        dk = d_kind_from(unit.annotations, unit.annotation_form)
    # **snake_case は記録だけ。上界にも `explicit` にも入れない**（仕様書 322 行目、O27）。
    # `covers` / `contradiction` / `is_bottom` は `malformed` を見ないので verdict は動かない。
    if unit.malformed_fields:
        return replace(dk, malformed=tuple(sorted(set(dk.malformed) | set(unit.malformed_fields))))
    return dk


def parse_d_kind_by_tool(unit: Unit) -> dict[str, DKind]:
    """低レベルハンドラの、join したツールごとの D_kind（§2.9 (a)）。"""
    return {name: d_kind_from(a, f) for name, (a, f) in sorted(unit.dispatch_annotations.items())}


def meet_d_kind(dks: list[DKind]) -> DKind:
    """複数ツールに帰属する効果の判定に使う「最も厳しい宣言」（§2.9 (c)）。

    * `upper`: どれか 1 つでも ⊥ なら ⊥（被覆しない = GAP_SELECT が出る側）、
      全部に上界があればその**積**。
    * `explicit` / `present_no_bound` / `malformed`: 和（CONTRADICTION は
      どれか 1 つの明示宣言に反すれば立つ）。
    * `unknown`: どれか 1 つでも読めなければ真。
    * `open_world`: **全部**が宣言したときだけ真（P0 の緩和は保守的に）。

    どの座標でも false-clean 側には倒れない（帰属先の各ツールで判定した結果の
    和集合と同じ verdict になる）。
    """
    if not dks:
        return DKind()
    upper: Optional[frozenset[str]]
    if any(d.upper is None for d in dks):
        upper = None
    else:
        acc = set(dks[0].upper or ())
        for d in dks[1:]:
            acc &= set(d.upper or ())
        upper = frozenset(acc)
    return DKind(
        upper=upper,
        explicit=tuple(sorted({x for d in dks for x in d.explicit})),
        present_no_bound=tuple(sorted({x for d in dks for x in d.present_no_bound})),
        malformed=tuple(sorted({x for d in dks for x in d.malformed})),
        unknown=any(d.unknown for d in dks),
        open_world=all(d.open_world for d in dks),
        # どれか 1 つの明示宣言に反すれば矛盾（explicit と同じく和）。
        closed_world=any(d.closed_world for d in dks),
        idempotent=any(d.idempotent for d in dks),
    )


def d_kind_from(ann: Optional[dict], form: Optional[str]) -> DKind:
    """annotations 1 つから D_kind を作る（Def 6。`parse_d_kind` の本体）。

    **上界を動かさないフィールドは D_kind を構成しない。**
    `title` / `idempotentHint` / `readOnlyHint==false` 単独 /
    `destructiveHint==true` 単独 / `openWorldHint==false` 単独は、明示されていても
    `D_kind = ⊥` のままとする。

    したがって `r_kind` の分子は「`readOnlyHint==true` / `destructiveHint==false` の
    いずれかを明示した（= 上界を動かす）ユニット」であって「`annotations=` を持つ
    ユニット」ではない。`openWorldHint==true` 単独の明示は `explicit` に残るが
    上界を動かさないので分子に入れない（学生の決定 O15、D32。`scripts/f0a.py` は
    `D_kind ≠ ⊥` で数える）。
    """
    if form == "unreadable":
        return DKind(unknown=True)
    if not ann:
        return DKind()
    explicit: list[str] = []
    no_bound: list[str] = []
    upper: Optional[set[str]] = None
    open_world = False

    read_only = ann.get("readOnlyHint")
    destructive = ann.get("destructiveHint")
    open_world_hint = ann.get("openWorldHint")

    if read_only is True:
        explicit.append("readOnlyHint")
        upper = set(READ_ONLY_UPPER)
    elif "readOnlyHint" in ann:
        no_bound.append("readOnlyHint")

    if destructive is False and read_only is not True:
        explicit.append("destructiveHint")
        # 破壊的 kind は宣言外。追記型の FS_WRITE と DB(insert) は宣言内。
        upper = (upper or set()) | {"FS_READ", "NET", "FS_WRITE", "DB"}
        upper -= DESTRUCTIVE_KINDS - {"FS_WRITE"}
    elif "destructiveHint" in ann:
        no_bound.append("destructiveHint")

    if open_world_hint is True:
        explicit.append("openWorldHint")
        open_world = True
    elif "openWorldHint" in ann:
        no_bound.append("openWorldHint")

    for f in ("title", "idempotentHint"):
        if f in ann:
            no_bound.append(f)

    return DKind(
        upper=frozenset(upper) if upper is not None else None,
        explicit=tuple(sorted(set(explicit))),
        present_no_bound=tuple(sorted(set(no_bound))),
        open_world=open_world,
        closed_world=open_world_hint is False,
        idempotent=ann.get("idempotentHint") is True and read_only is not True,
    )


#: 判定の結果（`contradiction_findings` の各要素の第 2 要素）。
CONTRA = "contradiction"
CONTRA_UNKNOWN = "unknown"


def _slot_model(e, *names: str) -> bool:
    from .ir import Prin

    for n in names:
        v = (getattr(e, "slots", None) or {}).get(n)
        if v is not None and v.prin is Prin.MODEL:
            return True
    return False


def _host_class(e) -> str:
    """`url.host` の類: `local`（localhost / private / loopback）/ `external` / `model` / `unknown`。"""
    import ipaddress
    from urllib.parse import urlparse

    v = (getattr(e, "slots", None) or {}).get("url.host")
    if v is None:
        return "unknown"
    c = v.const
    if isinstance(c, str) and c:
        host = urlparse(c).hostname if "://" in c else c.split("/")[0].rsplit(":", 1)[0] if c.count(":") <= 1 else c
        host = (host or "").strip("[]").lower()
        if not host:
            return "unknown"
        if host == "localhost" or host.endswith(".localhost") or host.endswith(".local"):
            return "local"
        try:
            ip = ipaddress.ip_address(host)
        except ValueError:
            return "external"
        return "local" if (ip.is_private or ip.is_loopback or ip.is_link_local) else "external"
    return "model" if _slot_model(e, "url.host") else "unknown"


def _fs_class(e) -> str:
    """FS_WRITE の類（§7.2）: `append` / `remove` / `writeout` / `unknown`。"""
    site = e.site
    destructive = getattr(e, "destructive", None)
    if site in FS_WRITEOUT_SITES:
        if site in FS_OPEN_SITES and destructive is False:
            return "append"
        if site in FS_OPEN_SITES and destructive is None:
            return "unknown"
        return "writeout"
    if destructive is False:
        return "append"
    if destructive is True:
        return "remove"
    return "unknown"


def _d1(e) -> Optional[tuple[str, str]]:
    """D1 `readOnlyHint: true`（§7.1）。`None` は宣言内。"""
    k = e.kind
    if k == "EXEC":
        return CONTRA, "exec"
    if k == "SPAWN":
        return (CONTRA, "spawn_model") if _slot_model(e, "argv0", "shell_string") else (CONTRA_UNKNOWN, "spawn_command")
    if k == "FS_WRITE":
        return CONTRA, "fs_write"
    if k == "DB":
        return _db(e, modify_heads=SQL_MODIFY_HEADS, persistent=(CONTRA, "db_persistent"))
    if k == "NET":
        m = getattr(e, "http_method", None)
        if m in HTTP_SAFE:
            return None
        if m in HTTP_MODIFY:
            return CONTRA, "net_modify"
        if m == "POST":
            return CONTRA_UNKNOWN, "net_post"
        if getattr(e, "http_method_model", False):
            return CONTRA, "net_method_model"
        return CONTRA_UNKNOWN, "net_method_unknown"
    return None


def _d2(e) -> Optional[tuple[str, str]]:
    """D2 `destructiveHint: false`（§7.2）。"""
    k = e.kind
    if k == "EXEC":
        return CONTRA, "exec"
    if k == "SPAWN":
        return (CONTRA, "spawn_model") if _slot_model(e, "argv0", "shell_string") else (CONTRA_UNKNOWN, "spawn_command")
    if k == "FS_WRITE":
        c = _fs_class(e)
        if c == "append":
            return None
        if c == "remove":
            return CONTRA, "fs_remove"
        if _slot_model(e, "path"):
            return CONTRA, f"fs_{c}_model_path"
        return CONTRA_UNKNOWN, f"fs_{c}"
    if k == "DB":
        return _db(e, modify_heads=SQL_DESTRUCTIVE_HEADS, persistent=(CONTRA_UNKNOWN, "db_persistent"),
                   additive=frozenset({"INSERT", "CREATE"}))
    if k == "NET":
        m = getattr(e, "http_method", None)
        if m in HTTP_SAFE:
            return None
        if m in ("DELETE", "PATCH"):
            return CONTRA, "net_modify"
        if m == "PUT":
            return (CONTRA, "net_put_model_url") if _slot_model(e, "url.host", "url.path") else (CONTRA_UNKNOWN, "net_put")
        if m == "POST":
            return CONTRA_UNKNOWN, "net_post"
        if getattr(e, "http_method_model", False):
            return CONTRA, "net_method_model"
        return CONTRA_UNKNOWN, "net_method_unknown"
    return None


def _db(e, *, modify_heads, persistent, additive=frozenset()) -> Optional[tuple[str, str]]:
    head = getattr(e, "sql_head", None)
    if head is None:
        return (CONTRA, "db_model_sql") if _slot_model(e, "sql") else (CONTRA_UNKNOWN, "db_sql_unreadable")
    if head in modify_heads:
        return CONTRA, "db_modify"
    if head in additive:
        return None
    sql = (getattr(e, "slots", None) or {}).get("sql")
    cls = sql_class(sql.const if sql is not None else None)
    if cls == SQL_CLASS_PERSISTENT:
        return persistent
    if cls in (SQL_CLASS_CONNECTION, SQL_CLASS_READ):
        return None
    if cls == SQL_CLASS_MODIFY:  # additive（INSERT / CREATE）は上で除いた
        return None
    return CONTRA_UNKNOWN, "db_unknown_statement"


def _d3(e) -> Optional[tuple[str, str]]:
    """D3 `openWorldHint: false`（§7.3、探索的）。"""
    k = e.kind
    if k == "NET":
        c = _host_class(e)
        if c == "local":
            return None
        if c == "external":
            return CONTRA, "net_external_host"
        if c == "model":
            return CONTRA, "net_model_host"
        return CONTRA_UNKNOWN, "net_host_unknown"
    if k == "EXEC":
        return (CONTRA, "exec_model") if _slot_model(e, "code_text") else (CONTRA_UNKNOWN, "exec")
    if k == "SPAWN":
        return (CONTRA, "spawn_model") if _slot_model(e, "argv0", "shell_string") else (CONTRA_UNKNOWN, "spawn_command")
    return None


def _d4(e) -> Optional[tuple[str, str]]:
    """D4 `idempotentHint: true`（§7.4、探索的）。原理 3 は当てない（§7.0 の 1）。"""
    k = e.kind
    if k == "FS_WRITE":
        if e.site in FS_OPEN_SITES:
            mode = getattr(e, "fs_mode", None)
            if mode is None:
                return CONTRA_UNKNOWN, "fs_mode_unknown"
            if "a" in mode:
                return CONTRA, "fs_append"
        return None
    if k == "DB":
        head = getattr(e, "sql_head", None)
        if head is None:
            return CONTRA_UNKNOWN, "db_sql_unreadable"
        if head in SQL_NONIDEMPOTENT_HEADS:
            return CONTRA_UNKNOWN, "db_nonidempotent_statement"
        return None
    if k == "NET":
        m = getattr(e, "http_method", None)
        if m in HTTP_IDEMPOTENT:
            return None
        if m in ("POST", "PATCH"):
            return CONTRA_UNKNOWN, "net_nonidempotent_method"
        return CONTRA_UNKNOWN, "net_method_unknown"
    if k in ("EXEC", "SPAWN"):
        return CONTRA_UNKNOWN, "exec_or_spawn"
    return None


def contradiction_findings(dk: DKind, e) -> list[tuple[str, str, str]]:
    """効果 1 つを、明示された宣言ごとに判定する（Def 7、D32 / D55 / D56）。

    返り値は `(宣言, 結果, 理由)` の列。宣言は `D1`（readOnlyHint: true）/ `D2`（destructiveHint:
    false、readOnly が無いとき）/ `D3`（openWorldHint: false）/ `D4`（idempotentHint: true、
    readOnly が無いとき）。結果は `CONTRA`（矛盾）か `CONTRA_UNKNOWN`（不明、原理 2-a）。
    宣言内のものは返さない。規則は `docs/contradiction_principles.md` §7（原理を選んでコミットした
    後に機械的に導いた表）。D3 / D4 は探索的な分析（§6）。
    """
    explicit = set(dk.explicit)
    out: list[tuple[str, str, str]] = []
    read_only = "readOnlyHint" in explicit
    if read_only:
        r = _d1(e)
        if r:
            out.append(("D1", *r))
    elif "destructiveHint" in explicit:
        r = _d2(e)
        if r:
            out.append(("D2", *r))
    if dk.closed_world:
        r = _d3(e)
        if r:
            out.append(("D3", *r))
    if dk.idempotent and not read_only:
        r = _d4(e)
        if r:
            out.append(("D4", *r))
    return out


def contradiction(dk: DKind, effects) -> bool:
    """`CONTRADICTION(e)`: 明示した宣言に反する効果が M にある（`contradiction_findings` のどれかが矛盾）。

    `effects` は `Effect` の列。後方互換で kind の文字列も受け付ける（その場合は D1 / D2 の
    EXEC / SPAWN / FS_WRITE を矛盾とする従来の規則。実データの判定には使わない）。
    """
    explicit = set(dk.explicit)
    for e in effects:
        if isinstance(e, str):
            if ({"readOnlyHint", "destructiveHint"} & explicit) and e in ("EXEC", "SPAWN", "FS_WRITE"):
                return True
            continue
        if any(status == CONTRA for _d, status, _r in contradiction_findings(dk, e)):
            return True
    return False


# --------------------------------------------------------------------------
# D_op（旧 D_operator）: ホスト承認リスト / exposure ファイル
# --------------------------------------------------------------------------


@dataclass
class DOp:
    """要求主体を引き上げる層。**host が執行する。**"""

    #: 許可されたツール名。`None` は `⊥`。
    allow: Optional[frozenset[str]] = None
    ask: frozenset[str] = frozenset()
    deny: frozenset[str] = frozenset()
    source: Optional[str] = None
    #: 帰属規則で除外したファイル（開発用の別エージェントの設定）。
    excluded_files: tuple[str, ...] = ()

    @property
    def is_bottom(self) -> bool:
        return self.allow is None and not self.ask and not self.deny

    def covers(self, tool_name: Optional[str]) -> bool:
        if tool_name is None:
            return False
        if tool_name in self.deny:
            return True
        if tool_name in self.ask:
            return True
        return self.allow is not None and tool_name in self.allow

    def to_json(self) -> dict:
        return {
            "bottom": self.is_bottom,
            "allow": sorted(self.allow) if self.allow is not None else None,
            "ask": sorted(self.ask),
            "deny": sorted(self.deny),
            "source": self.source,
            "excluded_files": list(self.excluded_files),
        }


def parse_d_op(
    index: SourceIndex, population: str, exposure_file: Optional[str] = None
) -> DOp:
    """D_op を読む。

    **帰属規則**（Def 6）: 解析対象木の `.claude/settings.json` は、
    **その木がエージェントアプリ（T3-app 母集団）である場合にのみ** D_op である。
    MCP サーバ / ツールパッケージの木にあるそれは開発用の別エージェントの設定で
    あり出荷物の宣言ではない。**帰属は木の母集団で決め、内容では決めない。**
    運用者が `--exposure <file>` で明示的に供給したものだけが例外なく D_op。

    :param population: ``app`` / ``mcp_server`` / ``tool_package``
    """
    if exposure_file:
        with open(exposure_file, encoding="utf-8") as fh:
            data = json.load(fh)
        return _from_permissions(data, f"exposure:{os.path.basename(exposure_file)}")

    found: list[str] = []
    for dirpath, dirs, files in os.walk(index.src_root):
        dirs[:] = sorted(dirs)
        for fn in sorted(files):
            if fn in ("settings.json", "settings.local.json") and os.path.basename(dirpath) == ".claude":
                found.append(os.path.relpath(os.path.join(dirpath, fn), index.src_root))
    if not found:
        return DOp()
    if population != "app":
        # 帰属規則により D_op ではない。**内容では判断しない。**
        return DOp(excluded_files=tuple(found))
    merged = DOp(source=f"in_tree:{found[0]}")
    for rel in found:
        with open(os.path.join(index.src_root, rel), encoding="utf-8") as fh:
            try:
                data = json.load(fh)
            except json.JSONDecodeError:
                continue
        part = _from_permissions(data, rel)
        merged = DOp(
            allow=(merged.allow or frozenset()) | (part.allow or frozenset())
            if (merged.allow is not None or part.allow is not None)
            else None,
            ask=merged.ask | part.ask,
            deny=merged.deny | part.deny,
            source=merged.source,
        )
    return merged


def _from_permissions(data: dict, source: str) -> DOp:
    perms = data.get("permissions", data)
    allow = perms.get("allow")
    return DOp(
        allow=frozenset(allow) if isinstance(allow, list) else None,
        ask=frozenset(perms.get("ask", []) or []),
        deny=frozenset(perms.get("deny", []) or []),
        source=source,
    )


# --------------------------------------------------------------------------
# in-tree の露出宣言（§8-7。含めるかは未凍結）
# --------------------------------------------------------------------------

#: §8 項目 7 の凍結（2026-09-09）: **含める。**
#:
#: ただし Def 6 の D_op 節の条件をそのまま課す — `enabled=` の式が
#: **真偽 config atom に解決でき、かつ atom の既定が閉**のときのみ D として読む。
#: 既定が開なら `D ⊭ e` 側に倒す。解決できない式は `opaque` として記録し、
#: **D にも `D ⊭ e` にも数えない**。
#:
#: 前測の実使用は 0 件なので数値影響は無い見込みだが、「含めるか否かを先に
#: 決める」という §8-7 の要求を満たすために既定を明示する。
#: 判断の根拠は `docs/decisions.md` D3。
INCLUDE_IN_TREE_EXPOSURE = True


def in_tree_exposure(index: SourceIndex) -> list[dict]:
    """FastMCP `enabled=` / `disable(names=|tags=)` / 低レベル `list_tools` フィルタ。

    各行に `resolved`（真偽 config atom に解決できたか）と `default_closed` を
    付ける。**解決できない式は `opaque` として記録し、D にも `D ⊭ e` にも
    数えない**（Def 6）。
    """
    from .atoms import build_atom_index

    ai = build_atom_index(index)
    out: list[dict] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fname = (dotted_of(node.func) or "").split(".")[-1]
            if fname in ("disable", "enable"):
                names = _string_list_kwarg(node, "names")
                out.append(
                    {
                        "relpath": rel,
                        "lineno": node.lineno,
                        "form": fname,
                        "names": names,
                        "resolved": bool(names),
                        "default_closed": fname == "disable" if names else None,
                    }
                )
            for kw in node.keywords:
                if kw.arg != "enabled":
                    continue
                atom, closed = _resolve_enabled(kw.value, ai)
                out.append(
                    {
                        "relpath": rel,
                        "lineno": node.lineno,
                        "form": "enabled=",
                        "tool": _tool_name_of(node),
                        "atom": atom,
                        "resolved": closed is not None,
                        "default_closed": closed,
                    }
                )
    return out


def _string_list_kwarg(call: ast.Call, key: str) -> list[str]:
    for kw in call.keywords:
        if kw.arg == key and isinstance(kw.value, (ast.List, ast.Tuple, ast.Set)):
            return [e.value for e in kw.value.elts if isinstance(e, ast.Constant) and isinstance(e.value, str)]
    return []


def _tool_name_of(call: ast.Call) -> Optional[str]:
    for kw in call.keywords:
        if kw.arg == "name" and isinstance(kw.value, ast.Constant):
            if isinstance(kw.value.value, str):
                return kw.value.value
    if call.args and isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
        return call.args[0].value
    return None


def _resolve_enabled(expr: ast.AST, ai) -> tuple[Optional[str], Optional[bool]]:
    """`enabled=<式>` を真偽 config atom に解決する。

    :returns: `(atom 名, 既定が閉か)`。**解決できなければ `(None, None)`**
        （`opaque`。推定で開閉を決めない）。
    """
    if isinstance(expr, ast.Constant) and isinstance(expr.value, bool):
        return "<literal>", expr.value is False
    name = dotted_of(expr)
    if name is None and isinstance(expr, ast.Lambda):
        # `enabled=lambda config: config.execute_local_commands` の形。
        name = dotted_of(expr.body)
    if name is None:
        return None, None
    atom = ai.lookup(name)
    if atom is None or atom.default_closed is None:
        return name.split(".")[-1], None
    return atom.name, atom.default_closed


def exposure_as_d_op(declarations: list[dict]) -> DOp:
    """in-tree の露出宣言を D_op に畳む（§8-7 の凍結: **含める**）。

    既定が閉（露出されない）ものだけを D として読む。既定が開のものと
    解決できないものは D に数えない。
    """
    if not INCLUDE_IN_TREE_EXPOSURE:
        return DOp()
    deny: set[str] = set()
    for d in declarations:
        if not d.get("resolved") or not d.get("default_closed"):
            continue
        if d.get("form") == "disable":
            deny.update(d.get("names") or [])
        elif d.get("tool"):
            deny.add(d["tool"])
    if not deny:
        return DOp()
    return DOp(allow=None, deny=frozenset(deny), source="in_tree_exposure")


# --------------------------------------------------------------------------
# D_prev: 直前リリースの M
# --------------------------------------------------------------------------


@dataclass
class DPrev:
    """直前リリースの manifest（unit id で join する）。"""

    units: dict[str, dict] = field(default_factory=dict)
    source: Optional[str] = None
    #: unit id を取れずに読み飛ばした行数。**0 でないなら報告する。**
    skipped: int = 0

    @classmethod
    def load(cls, path: str) -> DPrev:
        """`manifest.json` を読む。**unit id は `units[i]["unit"]["unit_id"]` にある。**

        `report.py: _unit_manifest` は `UnitReport.to_json()` をそのまま出すので、
        unit id はユニット直下ではなく `unit` ブロックの中である。直下を引いて
        いたため、**自分の `scan` 出力を `--prev-manifest` に渡すと `KeyError` で
        落ちていた**（D22）。自分の出力を自分で読めない層は一度も通っていない。

        id を取れない行は**黙って捨てず** `skipped` に数える。join できない行を
        0 件として扱うと `r_prev` の分母が静かに縮む。
        """
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        units: dict[str, dict] = {}
        skipped = 0
        for u in data.get("units", []):
            uid = (u.get("unit") or {}).get("unit_id")
            if not uid:
                skipped += 1
                continue
            units[uid] = u
        return cls(units, path, skipped)

    def join(self, unit_id: str) -> Optional[dict]:
        return self.units.get(unit_id)


def drift(prev: Optional[dict], now: dict) -> list[str]:
    """Def 6 の差分規則。

    `GAP_DRIFT(u, e) ⇔ e の kind が M_{r-1}(u) に無い、または制御位置 p の val が
    OP から MODEL になった、または req_occ / req_val の等級が下がった`。

    **行が増えないこと自体は verdict ではない。**
    """
    if prev is None:
        return []
    out: list[str] = []
    prev_kinds = {e["kind"] for e in prev.get("effects", [])}
    now_kinds = {e["kind"] for e in now.get("effects", [])}
    for k in sorted(now_kinds - prev_kinds):
        out.append(f"new_kind:{k}")

    def slot_prin(u: dict) -> dict[str, str]:
        acc: dict[str, str] = {}
        for e in u.get("effects", []):
            for slot, v in e.get("slots", {}).items():
                key = f"{e['kind']}@{slot}"
                cur = acc.get(key)
                if cur is None or v.get("prin") == "MODEL":
                    acc[key] = v.get("prin", "OP")
        return acc

    p, n = slot_prin(prev), slot_prin(now)
    for key, val in sorted(n.items()):
        if val == "MODEL" and p.get(key) in ("OP", "USER"):
            out.append(f"principal_raised:{key}")

    order = {"MODEL": 0, "OP": 1, "USER": 2}
    for key in ("req_occ", "req_val_min"):
        a, b = prev.get(key), now.get(key)
        if a in order and b in order and order[b] < order[a]:
            out.append(f"{key}_lowered:{a}->{b}")
    return out
