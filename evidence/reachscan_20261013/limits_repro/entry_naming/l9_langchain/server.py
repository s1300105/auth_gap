"""L9a: MCP サーバの木に、LangChain のエージェント用の @tool が同居する（t14 の拡張）。"""
import os
import subprocess

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l9a")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge(path: str) -> str:
    os.remove(path)
    return "ok"
