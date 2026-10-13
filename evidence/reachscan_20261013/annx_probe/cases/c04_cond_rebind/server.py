import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")
READ_ONLY = True
if os.getenv("ALLOW_WRITES"):
    READ_ONLY = False


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=READ_ONLY))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
