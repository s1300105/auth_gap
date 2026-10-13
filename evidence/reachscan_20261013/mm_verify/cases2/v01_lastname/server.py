import os
from mcp.server import Server
from mcp import types

app = Server("ll")

class Cache:
    def purge(self, k):
        return None

cache = Cache()

def purge(p):
    os.remove(p)

@app.list_tools()
async def list_tools():
    return [
        types.Tool(name="reader", description="r", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="deleter", description="d", inputSchema={}),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "reader":
        cache.purge(arguments["k"])
        return "ok"
    elif name == "deleter":
        purge(arguments["p"])
        return "ok"
