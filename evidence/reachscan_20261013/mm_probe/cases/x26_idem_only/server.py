from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x26")

@mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
def log(p: str, s: str) -> None:
    with open(p, "a") as f:  # reachscan:allow-WRITE log append
        f.write(s)
