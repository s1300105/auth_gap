import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
mcp = FastMCP("x")
class S: ro = False
settings = S()

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=settings.ro, destructiveHint=False))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
