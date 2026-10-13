import os
import mcp.types as types
from mcp.server import Server

server = Server("demo")


def _tool_defs() -> list[types.Tool]:
    return [
        types.Tool(name="wipe", description="w", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return _tool_defs()


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "wipe":
        os.remove(arguments["path"])
        return "ok"
    raise ValueError(name)
