from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
import os, shutil, subprocess, socket, sqlite3, requests
from pathlib import Path

mcp = FastMCP("probe")

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def local_http() -> str:
    return requests.get("http://localhost:8080/status").text

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def local_sock() -> None:
    socket.create_connection(("localhost", 8080))

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def private_sock() -> None:
    socket.create_connection(("10.0.0.5", 8080))
