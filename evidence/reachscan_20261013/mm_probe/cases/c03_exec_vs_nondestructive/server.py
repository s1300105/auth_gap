from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def run_cmd(cmd: str) -> str:
    subprocess.run(cmd, shell=True)
    return "ok"
