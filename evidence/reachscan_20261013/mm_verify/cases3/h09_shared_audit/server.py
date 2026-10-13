from mcp.server import Server
from mcp import types

app = Server("ll")

@app.list_tools()
async def list_tools():
    return [
        types.Tool(name="reader", description="r", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="other", description="o", inputSchema={}),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    open("/tmp/audit", "w").write(name)
    if name == "reader":
        return "r"
    elif name == "other":
        return "o"
