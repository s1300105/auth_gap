import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v05")
RO = False

def configure():
    global RO
    RO = True

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO, destructiveHint=False))
def rm(p: str) -> None:
    os.remove(p)
