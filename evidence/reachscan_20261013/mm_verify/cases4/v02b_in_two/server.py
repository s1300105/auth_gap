import os
from mcp.server import Server
from mcp import types

app = Server("ll")

def delete_it(p):
    os.remove(p)

@app.list_tools()
async def list_tools():
    return [types.Tool(name="a", description="a", inputSchema={},
                       annotations=types.ToolAnnotations(readOnlyHint=True)),
            types.Tool(name="b", description="b", inputSchema={})]

@app.call_tool()
async def call_tool(name, arguments):
    if name in ("b", "c"):
        delete_it(arguments["p"])
    return "ok"
