"""snake_case の注釈を `D_malformed` として記録する（O27 / D48）。

**期待値はこのテストで、`authgap/` を直す前に書いた**（CLAUDE.md 規則 5 の趣旨）。

仕様書 322 行目:

> snake_case 表記（`read_only_hint` 等、前測で 21 エントリ）は `ToolAnnotations` に
> deserialize されず protocol に届かないので **`D_malformed` として別行で報告する**。

**`malformed` は記録だけで、上界にも verdict にも影響してはならない。**
影響させると「snake_case を書いたら宣言したことになる」ことになり、
**protocol に届いていないものを届いたものとして扱う誤 clear**になる。
"""

from __future__ import annotations

import pytest

from authgap.dparse import parse_d_kind
from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import os
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("t")

# (1) デコレータ経路の snake_case
@mcp.tool(annotations={"read_only_hint": True})
async def snake_decorator(p: str) -> str:
    os.makedirs(p); return "x"

# (2) camelCase は従来どおり上界を動かす
@mcp.tool(annotations={"readOnlyHint": True})
async def camel_decorator(p: str) -> str:
    os.makedirs(p); return "x"

# (3) 混在: camelCase は効き、snake_case は malformed に載る
@mcp.tool(annotations={"readOnlyHint": True, "destructive_hint": False})
async def mixed(p: str) -> str:
    os.makedirs(p); return "x"

# (4) 4 種すべての snake_case
@mcp.tool(annotations={"read_only_hint": True, "destructive_hint": False,
                       "idempotent_hint": True, "open_world_hint": False})
async def all_snake(p: str) -> str:
    os.makedirs(p); return "x"

# (5) 注釈なし
@mcp.tool()
async def no_annotations(p: str) -> str:
    os.makedirs(p); return "x"

# (6) 仕様外のフィールドは malformed ではない（D でもない）
@mcp.tool(annotations={"category": "fs"})
async def out_of_spec(p: str) -> str:
    os.makedirs(p); return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("d_malformed")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


@pytest.mark.parametrize(
    "tool,want",
    [
        ("snake_decorator", ["read_only_hint"]),
        ("camel_decorator", []),
        ("mixed", ["destructive_hint"]),
        ("all_snake", ["destructive_hint", "idempotent_hint", "open_world_hint", "read_only_hint"]),
        ("no_annotations", []),
        ("out_of_spec", []),
    ],
)
def test_malformed_is_recorded(units, tool, want):
    """**直す前はどのツールも `malformed` が空だった**（構造的に常に空）。"""
    assert sorted((units[tool]["D_kind"] or {}).get("malformed", [])) == want


def test_snake_case_does_not_move_the_upper_bound(units):
    """**最重要。** snake_case は protocol に届かないので宣言ではない。

    上界を動かすと「書いただけで宣言したことになる」= 誤 clear になる。
    """
    for tool in ("snake_decorator", "all_snake"):
        dk = units[tool]["D_kind"]
        assert dk["bottom"] is True, f"{tool}: snake_case が上界を動かした"
        assert dk["explicit"] == [], f"{tool}: snake_case が explicit に入った"


def test_snake_case_does_not_create_a_contradiction(units):
    """snake_case の `read_only_hint: True` で CONTRADICTION を出してはならない。"""
    for tool in ("snake_decorator", "all_snake"):
        vs = {v for r in units[tool].get("rows", []) for v in r.get("verdicts", [])}
        assert "CONTRADICTION" not in vs, f"{tool}: snake_case で CONTRADICTION が出た"


def test_camel_case_still_works(units):
    """camelCase の判定は変えない（回帰の防止）。"""
    for tool in ("camel_decorator", "mixed"):
        dk = units[tool]["D_kind"]
        assert dk["explicit"] == ["readOnlyHint"]
        assert sorted(dk["upper"]) == ["FS_READ", "NET"]
        vs = {v for r in units[tool].get("rows", []) for v in r.get("verdicts", [])}
        assert "CONTRADICTION" in vs


def test_dkind_object_carries_malformed():
    """`DKind` そのものにも載ること（manifest 経由でなく直接）。"""
    from authgap.entries import Unit

    u = Unit(framework="mcp", entry_kind="decorator", module="m", qualname="q",
             relpath="m.py", node=None, annotations={}, annotation_form="dict",
             malformed_fields=("read_only_hint",))
    assert parse_d_kind(u).malformed == ("read_only_hint",)
