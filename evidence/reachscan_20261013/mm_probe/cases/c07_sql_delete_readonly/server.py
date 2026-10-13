from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge() -> None:
    conn = sqlite3.connect("db.sqlite")
    conn.execute("DELETE FROM items")
    conn.commit()
