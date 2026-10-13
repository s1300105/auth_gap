"""低レベル MCP ハンドラと `Tool(...)` 宣言の join（docs/preregistration.md §2.9）の fixture。

**期待値は §2.9 の規則から書き、実装より先にコミットする**（CLAUDE.md 規則 5）。
"""

import os

from mcp.server import Server
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent, Tool, ToolAnnotations

server = Server("t")
mcp = FastMCP("t2")
ROOT = "/srv/data"
DYN_NAME = os.environ.get("DYN_TOOL", "dyn_note")


@server.list_tools()
async def list_tools():
    return [
        # (i) 明示宣言（readOnlyHint=True → upper = {FS_READ, NET}）
        Tool(name="read_note", description="read", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
        # (i) 宣言はあるが上界を動かさない（⊥。readOnlyHint=False / destructiveHint=True 単独）
        Tool(name="write_note", description="write", inputSchema={},
             annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
        # (iii) 名前が非リテラル → join しない（件数に出す）
        Tool(name=DYN_NAME, description="dyn", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    # (ii) 共通処理の効果: どの name 判定にも支配されない → join した全ツールに帰属 →
    #      最も厳しい宣言（read_note の readOnly）で判定 → CONTRADICTION（false-dirty 側）
    os.makedirs(ROOT, exist_ok=True)
    if name == "read_note":
        # (i) read_note に帰属 → D_kind が FS_READ を被覆 → INVENTORY（covered_by = kind）
        with open(arguments["path"]) as f:
            return [TextContent(type="text", text=f.read())]
    elif name == "write_note":
        # (i) write_note に帰属 → 宣言 ⊥ → GAP_SELECT のまま、CONTRADICTION は付かない
        with open(arguments["path"], "w") as f:
            f.write(arguments["content"])
        return []
    raise ValueError(name)


# (iv) FastMCP デコレータ形（既存経路。壊れてはいけない）
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def deco_read(path: str) -> str:
    with open(path) as f:
        return f.read()
