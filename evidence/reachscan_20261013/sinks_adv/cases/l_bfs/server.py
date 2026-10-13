from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


def helper():
    import shutil as os
    return os.rmtree


import os

mcp = FastMCP("l_bfs")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_os_remove_after_nested_alias(p: str) -> str:
    os.remove(p)
    return "ok"
