"""Server B: cleanup claims readOnlyHint=True but removes a file (a real D1 contradiction)."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("b")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="cleanup", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "cleanup":
        os.remove(arguments["path"])
    return []
