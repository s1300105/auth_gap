import mcp.types as types
from mcp.server import Server
import a
import b

server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="wipe", description="w", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="zap", description="z", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "wipe":
        a.purge(arguments["path"])
    elif name == "zap":
        b.zap(arguments["path"])
    return "ok"
