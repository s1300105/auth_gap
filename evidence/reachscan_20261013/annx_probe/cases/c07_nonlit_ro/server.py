import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from .settings import settings

mcp = FastMCP("demo")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=settings.read_only, destructiveHint=False))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
