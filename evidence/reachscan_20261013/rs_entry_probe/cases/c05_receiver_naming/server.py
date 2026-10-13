import os
import fastmcp
from mcp.types import ToolAnnotations

srv = fastmcp.FastMCP("a")
mcp = fastmcp.FastMCP("b")


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge_srv(path: str) -> str:
    os.remove(path)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge_mcp(path: str) -> str:
    os.remove(path)
    return "ok"
