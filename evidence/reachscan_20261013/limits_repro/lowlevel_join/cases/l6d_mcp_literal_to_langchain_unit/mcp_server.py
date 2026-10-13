"""An MCP low-level server whose own cleanup tool is readOnlyHint=True and only reads."""
import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("low")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="cleanup", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "cleanup":
        with open(arguments["path"]) as f:
            return [types.TextContent(type="text", text=f.read())]
    raise ValueError(name)
