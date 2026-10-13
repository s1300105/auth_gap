from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v04")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def members(x: int) -> list:
    oset = {1, 2, 3}
    oset.remove(x)
    return sorted(oset)
