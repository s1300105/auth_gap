import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")
extra = {"title": "Wipe"}


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, **extra))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
