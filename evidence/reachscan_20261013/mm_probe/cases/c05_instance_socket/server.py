from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def raw_connect(host: str) -> None:
    s = socket.socket()
    s.connect((host, 80))
