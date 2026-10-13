import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
mcp = FastMCP("x")
extra = {}

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=None, openWorldHint=False, **extra))
def a(path: str) -> str:
    return "ok"

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=None, read_only_hint=True, openWorldHint=False))
def b(path: str) -> str:
    return "ok"

@mcp.tool(annotations={"readonlyHint": True, "openWorldHint": False})
def c(path: str) -> str:
    return "ok"
