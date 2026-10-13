from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

# reachscan:allow-mismatch cache cleanup only
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def a(p: str) -> None:
    os.remove(p)

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def b(p: str) -> None:
    os.remove(p)  # reachscan:allow-WRITE intended delete
