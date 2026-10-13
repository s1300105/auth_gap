"""L9b: jlowin fastmcp（サードパーティ）の @mcp.tool。カタログには framework=fastmcp の規則がある。"""
import os

from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l9b")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge(path: str) -> str:
    os.remove(path)
    return "ok"
