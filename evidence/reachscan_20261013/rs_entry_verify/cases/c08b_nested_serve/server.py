import os
import mcp.types as types
from mcp.server import Server


async def serve() -> None:
    server = Server("demo")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(name="read_note", description="r", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=True)),
            types.Tool(name="purge", description="p", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
            types.Tool(name="wipe", description="w", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=True)),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        if name == "read_note":
            with open(arguments["path"]) as fh:
                return fh.read()
        elif name == "purge":
            os.remove(arguments["path"])
            return "ok"
        elif name == "wipe":
            os.remove(arguments["path"])
            return "ok"
        raise ValueError(name)
