from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def calc(expr: str) -> str:
    return str(eval(expr))
