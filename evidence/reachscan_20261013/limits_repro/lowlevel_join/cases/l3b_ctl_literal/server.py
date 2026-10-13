"""L3b control: same as L3a but Tool(name="wipe") literal."""
import os
from enum import Enum

import mcp.types as types
from mcp.server.lowlevel import Server


class Tools(str, Enum):
    WIPE = "wipe"


server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="wipe", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "wipe":
        os.remove(arguments["path"])
    return []
