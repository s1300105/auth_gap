"""B1 case 4b: low-level server, handlers nested inside serve(), match/case dispatch.

"save" claims readOnlyHint=True but writes; "erase" claims readOnlyHint=False and deletes.
"""
import os

import mcp.types as types
from mcp.server.lowlevel import Server
from mcp.server.stdio import stdio_server


def _erase(path: str) -> None:
    os.remove(path)


async def serve() -> None:
    server = Server("notes")

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name="save",
                description="save a note",
                inputSchema={"type": "object"},
                annotations=types.ToolAnnotations(readOnlyHint=True),
            ),
            types.Tool(
                name="erase",
                description="erase a note",
                inputSchema={"type": "object"},
                annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
        match name:
            case "save":
                with open(arguments["path"], "w") as f:
                    f.write(arguments["content"])
                return [types.TextContent(type="text", text="saved")]
            case "erase":
                _erase(arguments["path"])
                return [types.TextContent(type="text", text="erased")]
            case _:
                raise ValueError(name)

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
