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

from .entries import Unit
from .srcindex import SourceIndex, dotted_of

# --------------------------------------------------------------------------
# D_kind（旧 D_author）: MCP annotations
# --------------------------------------------------------------------------

#: `readOnlyHint==true` が宣言する効果 kind の上界。
READ_ONLY_UPPER = frozenset({"FS_READ", "NET"})

#: 破壊的な kind（`destructiveHint==false` が宣言外にするもの）。
DESTRUCTIVE_KINDS = frozenset({"EXEC", "SPAWN", "FS_WRITE"})


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
    )


def contradiction(dk: DKind, effects) -> bool:
    """`CONTRADICTION(e)`: 明示した宣言に反する効果が M にある（Def 7、D32）。

    * `readOnlyHint==true` の明示 → EXEC / SPAWN / FS_WRITE のすべて。
    * `destructiveHint==false` の明示（readOnly は明示していない）→ EXEC / SPAWN、
      および `destructive` が False **でない** FS_WRITE（削除・上書き型、または
      mode が読めず不明のもの。追記型 `mkdir` / `open('a')` は宣言内）。

    `effects` は `Effect` の列。後方互換で kind の文字列集合も受け付ける
    （その場合は FS_WRITE を削除・上書き型として扱う = 従来の規則）。
    """
    explicit = set(dk.explicit)
    if not ({"readOnlyHint", "destructiveHint"} & explicit):
        return False
    read_only = "readOnlyHint" in explicit
    for e in effects:
        kind = e if isinstance(e, str) else e.kind
        if kind in ("EXEC", "SPAWN"):
            return True
        if kind == "FS_WRITE":
            if read_only:
                return True
            destructive = True if isinstance(e, str) else getattr(e, "destructive", None)
            if destructive is not False:
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
