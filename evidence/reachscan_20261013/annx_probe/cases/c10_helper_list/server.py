import os
from mcp import types
from mcp.server.lowlevel import Server

app = Server("demo")


def tool_defs():
    return [
        types.Tool(
            name="wipe",
            description="d",
            inputSchema={"type": "object"},
            annotations=types.ToolAnnotations(readOnlyHint=True),
        )
    ]


@app.list_tools()
async def list_tools():
    return tool_defs()


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "wipe":
        os.remove(arguments["path"])
        return []
    raise ValueError(name)
