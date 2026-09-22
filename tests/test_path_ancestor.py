"""`Path.parent` / `Path.parents[n]` の受け手型（O22 / D43）。

**期待値はこの表で、`authgap/val/engine.py` を直す前に書いた**（CLAUDE.md 規則 5）。

直す前は `Path(...).parent` が受け手の `Path` 形を落とし、`_receiver_typed_key` の
`isinstance(shape, Path)` が外れて **FS の効果行が 1 本も出なかった**
（誤 clear。`v2-rwheeler007__cohort` の `internal_web_fetch`）。

**R2 が最重要の反証テストである。** 祖先が `Path.resolve()` の `canonicalised` 属性を
引き継ぐと、検査済みの値についての包含述語が**別の値**（root の外に出うる祖先）に
ついて成立し、strong-path が誤って立つ。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import os
from pathlib import Path
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("t")

@mcp.tool(annotations={"readOnlyHint": True})
async def parent_of_model(user_path: str) -> str:
    Path(user_path).parent.mkdir(parents=True)
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def parents_index(user_path: str) -> str:
    Path(user_path).parents[2].mkdir()
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def parents_var_index(user_path: str, n: int) -> str:
    Path(user_path).parents[n].mkdir()
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def parent_chain(user_path: str) -> str:
    Path(user_path).parent.parent.mkdir()
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def canonical_not_inherited(user_path: str) -> str:
    root = Path("/srv/data")
    cand = (root / user_path).resolve()
    if str(cand).startswith(str(root) + os.sep):
        cand.parent.write_text("x")
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def no_parent_stays_resolved(unused: str) -> str:
    (Path("/tmp") / "x").mkdir()
    return "x"

@mcp.tool(annotations={"readOnlyHint": True})
async def str_attr_still_works(user_path: str) -> str:
    os.system("echo " + Path(user_path).parent.name)
    return "x"
'''


@pytest.fixture(scope="module")
def units(tmp_path_factory):
    d = tmp_path_factory.mktemp("path_ancestor")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u):
    return [(e["site"], e["kind"], e["resolution"]) for e in u.get("effects", [])]


def _path_prin(u, site):
    for e in u.get("effects", []):
        if e["site"] == site:
            return ((e.get("slots") or {}).get("path") or {}).get("prin")
    return None


@pytest.mark.parametrize(
    "tool", ["parent_of_model", "parents_index", "parents_var_index", "parent_chain"]
)
def test_ancestor_keeps_the_fs_effect(units, tool):
    """**直す前はここが空だった**（効果行が 1 本も出ない = 誤 clear）。"""
    assert ("pathlib.Path.mkdir", "FS_WRITE", "opaque") in _effects(units[tool])


@pytest.mark.parametrize(
    "tool", ["parent_of_model", "parents_index", "parents_var_index", "parent_chain"]
)
def test_ancestor_keeps_the_principal(units, tool):
    """**主体を落とすと誤 clear。** MODEL のパスの親は MODEL である。"""
    assert _path_prin(units[tool], "pathlib.Path.mkdir") == "MODEL"


@pytest.mark.parametrize(
    "tool", ["parent_of_model", "parents_index", "parents_var_index", "parent_chain"]
)
def test_ancestor_is_opaque_not_resolved(units, tool):
    """どこまで遡ったかは値として決まらないので**確度は opaque**。UNKNOWN が立つ。"""
    u = units[tool]
    vs = {v for r in u.get("rows", []) for v in r.get("verdicts", [])}
    assert "UNKNOWN" in vs
    assert "CONTRADICTION" in vs  # readOnlyHint:true に対する FS_WRITE


def test_r2_canonicalised_is_not_inherited(units):
    """**最重要の反証テスト。**

    `(root / user_path).resolve()` は検査済みだが、**その親は root の外に出うる。**
    祖先が `canonicalised` 属性を引き継ぐと strong-path が誤って立ち、
    `write_text` が clear される。等級が立たないことを確かめる。
    """
    u = units["canonical_not_inherited"]
    assert ("pathlib.Path.write_text", "FS_WRITE", "opaque") in _effects(u)
    assert _path_prin(u, "pathlib.Path.write_text") == "MODEL"
    grades = u.get("grades") or {}
    for key, g in grades.items():
        if key.endswith(":path"):
            assert g.get("grade") is None, f"{key} に等級が立った: {g}"
    vs = {v for r in u.get("rows", []) for v in r.get("verdicts", [])}
    assert "CONTRADICTION" in vs


def test_paths_without_an_ancestor_stay_resolved(units):
    """**この変更で確度を落としてはいけない範囲。** `/` と `resolve()` は resolved のまま。"""
    assert ("pathlib.Path.mkdir", "FS_WRITE", "resolved") in _effects(units["no_parent_stays_resolved"])


def test_str_valued_attributes_are_unaffected(units):
    """`.name` は str を返す。`Path` 形にしてはいけない。"""
    assert any(s == "os.system" for s, _k, _r in _effects(units["str_attr_still_works"]))
