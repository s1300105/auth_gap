import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("idem")
RO = True


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, idempotentHint=True))
def nl_idem_remove(path: str) -> str:
    os.remove(path)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, idempotentHint=True))
def lit_idem_remove(path: str) -> str:
    os.remove(path)
    return "ok"
