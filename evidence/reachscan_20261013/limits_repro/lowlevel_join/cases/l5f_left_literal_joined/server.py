"""L5f: both tools are joined through an `in` guard; the wipe branch is written "wipe" == name.
peek (readOnlyHint=True) reads; wipe (readOnlyHint=False, destructiveHint=True) removes."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

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
    known = name in ("peek", "wipe")
    if not known:
        raise ValueError(name)
    if "wipe" == name:
        os.remove(arguments["path"])
        return [types.TextContent(type="text", text="ok")]
    with open(arguments["path"]) as f:
        return [types.TextContent(type="text", text=f.read())]
