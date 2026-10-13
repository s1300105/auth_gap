import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge(path: str) -> str:
    os.remove(path)
    return "ok"
