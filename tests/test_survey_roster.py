"""`scripts/survey_roster.py`（実態調査の名簿、D85）のテスト。解析器を使わずに D1 の宣言をツールに結びつける。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

import survey_roster as sr  # noqa: E402

SRC = b'''
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations, Tool

mcp = FastMCP("x")
RO = ToolAnnotations(readOnlyHint=True)
UNUSED = ToolAnnotations(readOnlyHint=True)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def search(q: str) -> str:
    return q

@mcp.tool(annotations=RO)
async def lookup(q: str) -> str:
    return q

@mcp.tool(annotations={"readOnlyHint": True})
def dict_form() -> str:
    return ""

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False))
def writer() -> str:
    return ""

@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake() -> str:
    return ""

def helper():
    return 1

mcp.add_tool(helper, annotations=RO)

TOOLS = [Tool(name="low_level", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True))]

def reg_fn():
    return 1

mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(reg_fn)

REGISTRY = {"handler": reg_fn, "readOnlyHint": True}
TABLE = {"table_tool": {"title": "T", "annotations": {"readOnlyHint": True}}}
'''


def test_forms():
    es = sr.declarations(SRC, "server.py")
    got = {(e["form"], e["tool"]) for e in es}
    assert ("decorator", "search") in got
    assert ("name", "lookup") in got
    assert ("decorator", "dict_form") in got
    assert ("decorator", "snake") in got
    assert ("name", "helper") in got  # add_tool(…, annotations=RO)
    assert ("tool_ctor", "low_level") in got
    assert ("call_register", "reg_fn") in got
    assert ("dict_registry", "reg_fn") in got
    assert ("dict_registry", "table_tool") in got
    assert all(e["tool"] != "writer" for e in es)  # readOnlyHint=False は入れない
    # 使い先の無い UNUSED は unmapped として残す（黙って落とさない）
    assert any(e["form"] == "unmapped" for e in es)
    # 名前に代入した宣言（RO）は使われているので unmapped にしない。unmapped は UNUSED の 1 件だけ
    assert sum(1 for e in es if e["form"] == "unmapped") == 1


def test_build_skips_non_src_and_records_parse_failures(tmp_path):
    t = tmp_path / "v9-a__b"
    (t / "src").mkdir(parents=True)
    (t / "tests").mkdir()
    (t / "src" / "server.py").write_bytes(SRC)
    (t / "tests" / "test_x.py").write_bytes(SRC)  # テストのディレクトリは名簿に入れない
    (t / "src" / "broken.py").write_bytes(b"def (:\n")
    p = sr.build_tree(str(t), "v9-a__b")
    assert {e["relpath"] for e in p["entries"]} == {"src/server.py"}
    assert [f["relpath"] for f in p["parse_failures"]] == ["src/broken.py"]


def test_bom_file_is_read(tmp_path):
    t = tmp_path / "v9-c__d"
    t.mkdir()
    (t / "server.py").write_bytes(b"\xef\xbb\xbf" + SRC)
    p = sr.build_tree(str(t), "v9-c__d")
    assert p["entries"] and not p["parse_failures"]


def test_sample_is_deterministic_and_one_per_tree(tmp_path):
    roster = {"trees": [{"tree": f"t{i:02d}", "entries": [{"relpath": "a.py", "tool": f"f{j}", "form": "decorator",
                                                             "def_lineno": j, "decl_lineno": j} for j in range(3)]}
                        for i in range(30)] + [{"tree": "empty", "entries": []}]}
    a = sr.sample(roster, seed=7, n=20)
    b = sr.sample(roster, seed=7, n=20)
    assert a["targets"] == b["targets"]
    assert a["n_targets"] == 20 and a["n_trees_in_roster"] == 30
    assert len({x["tree"] for x in a["targets"]}) == 20
    assert [x["seq"] for x in a["targets"]] == list(range(1, 21))
    assert sr.sample(roster, seed=8, n=20)["targets"] != a["targets"]
    json.dumps(a, ensure_ascii=False)
