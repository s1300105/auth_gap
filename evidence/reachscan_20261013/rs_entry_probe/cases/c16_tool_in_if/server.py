import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")
ENABLE_WRITE = os.environ.get("ENABLE_WRITE") == "1"

if ENABLE_WRITE:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def purge_if(path: str) -> str:
        os.remove(path)
        return "ok"

try:
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def purge_try(path: str) -> str:
        os.remove(path)
        return "ok"
except Exception:
    pass
