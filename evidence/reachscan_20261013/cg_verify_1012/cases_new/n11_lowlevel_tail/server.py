from mcp.server.lowlevel import Server
from mcp.types import Tool, ToolAnnotations
from util import delete

server = Server("demo")


@server.list_tools()
async def list_tools():
    return [
        Tool(name="forget", description="f", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
        Tool(name="wipe", description="w", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=False)),
    ]


@server.call_tool()
async def call_tool(name, arguments):
    if name == "forget":
        cache = {}
        cache.pop("k", None)
        arguments.delete("k") if hasattr(arguments, "delete") else None
        return "ok"
    elif name == "wipe":
        delete(arguments["p"])
        return "ok"
