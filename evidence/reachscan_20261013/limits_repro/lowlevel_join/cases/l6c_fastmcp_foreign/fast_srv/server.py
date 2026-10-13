"""FastMCP server: status has NO annotations and appends to a file."""
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("fast")


@mcp.tool()
def status(path: str) -> str:
    with open(path, "a") as f:
        f.write("ping\n")
    return "ok"
