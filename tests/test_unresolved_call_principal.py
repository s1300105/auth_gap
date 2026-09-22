"""解決できない呼び出しの戻り値の主体と root（O25 / D44）。

**期待値はこの表で、`authgap/val/engine.py` を直す前に書いた**（CLAUDE.md 規則 5）。

直す前は `_ev_Call` の最後の fallback が **root だけを引き継ぎ、主体を `Prin.OP` に
固定**していた。**root が「この値はツール引数 p 由来だ」と言っているのに主体が
「運用者の値だ」と言うのは矛盾で、向きは誤 clear。** さらにキーワード引数と受け手は
root にも入っていなかったので、`f(value=p)` と `p.unknown_method()` は root ごと消えていた。

**両方向を固定する。** 入力に MODEL があれば MODEL、無ければ OP のまま。
OP のままであるべき側（X1 / X3 / X7 / X8）を落とすと誤警報になる。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run

SRC = '''
import os, uuid, time
import subprocess
from mcp.server.fastmcp import FastMCP
from unknown_lib import mystery
mcp = FastMCP("t")

@mcp.tool()
async def positional(p: str) -> str:
    os.system("echo " + mystery(p)); return "x"

@mcp.tool()
async def keyword(p: str) -> str:
    os.system("echo " + mystery(value=p)); return "x"

@mcp.tool()
async def receiver(p: str) -> str:
    os.system("echo " + p.mystery_method()); return "x"

@mcp.tool()
async def model_receiver_const_arg(p: str) -> str:
    os.system("echo " + p.mystery_method("lit")); return "x"

@mcp.tool()
async def nested(p: str) -> str:
    os.system("echo " + mystery(mystery(p))); return "x"

@mcp.tool()
async def builtin_str(p: str) -> str:
    os.system("echo " + str(p)); return "x"

@mcp.tool()
async def no_args_call(unused: str) -> str:
    os.system("echo " + str(uuid.uuid4()) + str(time.time())); return "x"

@mcp.tool()
async def module_receiver(unused: str) -> str:
    os.system("echo " + os.path.mystery_fn("lit")); return "x"

@mcp.tool()
async def literal_kwarg(unused: str) -> str:
    os.system("echo " + mystery(kw="lit")); return "x"

@mcp.tool()
async def literal_call_in_argv(p: str) -> str:
    subprocess.run([mystery("git"), "status"], shell=False); return "x"
'''


@pytest.fixture(scope="module")
def slots(tmp_path_factory):
    d = tmp_path_factory.mktemp("unresolved_call")
    (d / "server.py").write_text(SRC, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    out = {}
    for u in manifest_json(res, "t")["units"]:
        for e in u.get("effects", []):
            out.setdefault(u["unit"]["qualname"], {}).update(e.get("slots") or {})
    return out


#: 入力に MODEL があるので戻り値も MODEL。**直す前はすべて OP だった（誤 clear）。**
@pytest.mark.parametrize(
    "tool",
    ["positional", "keyword", "receiver", "model_receiver_const_arg", "nested", "builtin_str"],
)
def test_model_input_makes_the_result_model(slots, tool):
    v = slots[tool]["shell_string"]
    assert v["prin"] == "MODEL", f"{tool}: 主体が {v['prin']}（誤 clear）"
    assert v.get("roots") == ["p"], f"{tool}: roots が {v.get('roots')}"


#: **ここを MODEL にすると誤警報。** 引数を取らない呼び出し、モジュール受け手、
#: リテラルだけの引数は運用者の値である。
@pytest.mark.parametrize("tool", ["no_args_call", "module_receiver", "literal_kwarg"])
def test_no_model_input_stays_op(slots, tool):
    v = slots[tool]["shell_string"]
    assert v["prin"] == "OP", f"{tool}: 主体が {v['prin']}（誤警報）"
    assert not v.get("roots"), f"{tool}: roots が {v.get('roots')}"


def test_literal_call_does_not_taint_the_whole_argv(slots):
    """`[mystery("git"), "status"]` は列全体を MODEL にしない。

    CLAUDE.md の落とし穴「列の分岐合流で要素を捨てない。argv0 のリテラルが列全体の
    主体になる」の逆向き。要素ごとに主体を持つことを確かめる。
    """
    s = slots["literal_call_in_argv"]
    assert s["argv0"]["prin"] == "OP"
    assert s["argv[*]"]["prin"] == "OP"
