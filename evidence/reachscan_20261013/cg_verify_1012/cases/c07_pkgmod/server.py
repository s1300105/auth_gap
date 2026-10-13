import os
import subprocess
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")

from pkg import ops


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wipe(path: str) -> str:
    ops.purge(path)
    return "ok"
