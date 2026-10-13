"""Server A: cleanup is declared destructive (readOnlyHint=False, destructiveHint=True) and removes a file."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("a")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="cleanup", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "cleanup":
        os.remove(arguments["path"])
    return []
