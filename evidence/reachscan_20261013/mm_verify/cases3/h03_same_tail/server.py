from mcp.server import Server
from mcp import types
import mod_a
import mod_b

app = Server("ll")

@app.list_tools()
async def list_tools():
    return [
        types.Tool(name="tool_a", description="a", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="tool_b", description="b", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]

@app.call_tool()
async def call_tool(name, arguments):
    if name == "tool_a":
        mod_a.cleanup(arguments["p"])
    elif name == "tool_b":
        return mod_b.cleanup(arguments["p"])
    return "ok"
