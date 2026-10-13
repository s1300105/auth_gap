import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")

from mod import Klass


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def safe(path: str) -> str:
    return Klass.run(path)
