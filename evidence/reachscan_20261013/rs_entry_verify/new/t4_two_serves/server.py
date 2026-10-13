import os
import mcp.types as types
from mcp.server import Server


async def serve_a() -> None:
    server = Server("a")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(name="tool_a", description="a", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=True)),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "tool_a":
            return "a"
        return "x"


async def serve_b() -> None:
    server = Server("b")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(name="wipe_b", description="b", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=True)),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "wipe_b":
            os.remove(arguments["path"])
        return "x"
