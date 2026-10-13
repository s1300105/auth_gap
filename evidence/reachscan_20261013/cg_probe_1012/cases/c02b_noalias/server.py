import os
import subprocess
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")

from util import purge


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wipe(path: str) -> str:
    purge(path)
    return "ok"
