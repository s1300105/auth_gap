import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")

try:
    from util import purge
except ImportError:
    purge = None


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wipe(path: str) -> str:
    purge(path)
    return "ok"
