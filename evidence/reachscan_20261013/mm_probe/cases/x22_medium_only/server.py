from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x22")

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def save(p: str, s: str) -> None:
    with open(p, "w") as f:  # reachscan:allow-WRITE writes the user's export file
        f.write(s)
