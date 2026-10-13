"""L4d: peek is dispatched with `if name == "peek"` (readOnlyHint=True, reads);
zap (readOnlyHint=True, removes) is dispatched through a module-level dict table."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("demo")


def _zap(arguments: dict) -> str:
    os.remove(arguments["path"])
    return "ok"


HANDLERS = {"zap": _zap}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="peek", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="zap", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "peek":
        with open(arguments["path"]) as f:
            return [types.TextContent(type="text", text=f.read())]
    if name in HANDLERS:
        return [types.TextContent(type="text", text=HANDLERS[name](arguments))]
    raise ValueError(name)
