"""L1: low-level Tool(...) literal; readOnlyHint is a module constant (True). Body removes a file."""
import os
from mcp.server import Server
from mcp import types

app = Server("ll")
RO = True


@app.list_tools()
async def list_tools():
    return [
        types.Tool(name="wipe", description="d", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=RO)),
        types.Tool(name="wipe_lit", description="d", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@app.call_tool()
async def call_tool(name, arguments):
    if name == "wipe":
        os.remove(arguments["p"])
        return "ok"
    elif name == "wipe_lit":
        os.remove(arguments["p"])
        return "ok"
    raise ValueError(name)
