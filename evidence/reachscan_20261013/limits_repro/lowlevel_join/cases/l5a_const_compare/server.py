"""L5a: peek (readOnlyHint=True) reads; wipe (readOnlyHint=False, destructiveHint=True) removes.
The wipe branch compares with a module constant."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

WIPE = "wipe"
server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="peek", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="wipe", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "peek":
        with open(arguments["path"]) as f:
            text = f.read()
    elif name == WIPE:
        os.remove(arguments["path"])
        text = "ok"
    else:
        raise ValueError(name)
    return [types.TextContent(type="text", text=text)]
