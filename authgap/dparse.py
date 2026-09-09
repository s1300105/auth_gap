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
from dataclasses import dataclass, field
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

    **上界を動かさないフィールドは D_kind を構成しない。**
    `title` / `idempotentHint` / `readOnlyHint==false` 単独 /
    `destructiveHint==true` 単独 / `openWorldHint==false` 単独は、明示されていても
    `D_kind = ⊥` のままとする。

    したがって `r_kind` の分子は「`readOnlyHint==true` / `destructiveHint==false` /
    `openWorldHint==true` のいずれかを明示したユニット」であって
    「`annotations=` を持つユニット」ではない。
    """
    if unit.annotation_form == "unreadable":
        return DKind(unknown=True)
    ann = unit.annotations
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


def contradiction(dk: DKind, effect_kinds: set[str]) -> bool:
    """`CONTRADICTION(e)`: `readOnlyHint==true` または `destructiveHint==false` を
    **明示**しているのに M に WRITE / EXEC がある（Def 7）。"""
    if not ({"readOnlyHint", "destructiveHint"} & set(dk.explicit)):
        return False
    return bool(effect_kinds & {"EXEC", "SPAWN", "FS_WRITE"})


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

#: §8 項目 7 の凍結が済むまで **含めない**。前測の実使用は 0 件なので
#: 数値影響は無い見込みだが、既定を明示しておく（`docs/open_questions.md` Q6）。
INCLUDE_IN_TREE_EXPOSURE = False


def in_tree_exposure(index: SourceIndex) -> list[dict]:
    """FastMCP `enabled=` / `disable(names=|tags=)` / 低レベル `list_tools` フィルタ。

    **測って報告するが、`INCLUDE_IN_TREE_EXPOSURE` が偽の間は D_op に入れない。**
    """
    out: list[dict] = []
    for path in index.py_files():
        tree = index.parse(path)
        if tree is None:
            continue
        rel = index.relpath(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = (dotted_of(node.func) or "").split(".")[-1]
                if name in ("disable", "enable"):
                    out.append({"relpath": rel, "lineno": node.lineno, "form": name})
                for kw in node.keywords:
                    if kw.arg == "enabled":
                        out.append({"relpath": rel, "lineno": node.lineno, "form": "enabled="})
    return out


# --------------------------------------------------------------------------
# D_prev: 直前リリースの M
# --------------------------------------------------------------------------


@dataclass
class DPrev:
    """直前リリースの manifest（unit id で join する）。"""

    units: dict[str, dict] = field(default_factory=dict)
    source: Optional[str] = None

    @classmethod
    def load(cls, path: str) -> DPrev:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
        units = {u["unit_id"]: u for u in data.get("units", [])}
        return cls(units, path)

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
