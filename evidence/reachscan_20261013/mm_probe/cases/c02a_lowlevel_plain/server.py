import os
from mcp.server import Server
from mcp import types

app = Server("ll")

def read_it(p):
    with open(p) as f:
        return f.read()

def delete_it(p):
    os.remove(p)

@app.list_tools()
async def list_tools():
    return [
        types.Tool(name="reader", description="r", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="deleter", description="d", inputSchema={},
                   annotations=types.ToolAnnotations(destructiveHint=True)),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "reader":
        return read_it(arguments["p"])
    elif name == "deleter":
        delete_it(arguments["p"])
        return "ok"
    raise ValueError(name)
