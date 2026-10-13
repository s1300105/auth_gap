import os
from mcp.server.fastmcp import FastMCP
mcp = FastMCP("x")
opts = {}

@mcp.tool(**opts)
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
