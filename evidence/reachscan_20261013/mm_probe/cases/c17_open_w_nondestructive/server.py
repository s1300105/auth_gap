from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def save(p: str, s: str) -> None:
    with open(p, "w") as f:
        f.write(s)

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def append(p: str, s: str) -> None:
    with open(p, "a") as f:
        f.write(s)

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def copy_over(src: str, dst: str) -> None:
    shutil.copy(src, dst)
