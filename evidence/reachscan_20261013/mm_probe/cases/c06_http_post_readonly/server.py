from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def post_it(data: str) -> None:
    requests.post("https://api.example.com/items", json={"d": data})

@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def delete_remote(item: str) -> None:
    requests.delete("https://api.example.com/items/" + item)
