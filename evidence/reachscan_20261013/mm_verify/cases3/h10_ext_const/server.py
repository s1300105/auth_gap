import os
from external_pkg_not_in_tree import RO
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("h10")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO))
def rm(p: str) -> None:
    os.remove(p)
