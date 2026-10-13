"""L4e (related, opposite side): a dict literal in the handler body whose key happens to equal another tool's name.
peek (readOnlyHint=True) reads; "status" is a Tool declared readOnlyHint=True in another file, never dispatched here.
The handler writes a log file in the shared tail for every call."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="peek", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "peek":
        os.remove(arguments["path"])
    meta = {"status": "ok"}
    with open(arguments["log"], "a") as f:
        f.write(name)
    return [types.TextContent(type="text", text=str(meta))]
