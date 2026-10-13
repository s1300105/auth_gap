from mcp.server.fastmcp import FastMCP
mcp = FastMCP("x")

@mcp.tool(annotations={"title": "Nice"})
def t() -> str:
    return "ok"
