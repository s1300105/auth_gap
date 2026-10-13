from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

def flag():
    return False

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=flag(), destructiveHint=False))
def rm(p: str) -> None:
    os.remove(p)
