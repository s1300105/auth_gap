import os, sys
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v06")
RO = True
if sys.platform != "nonexistent":
    RO = False

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO))
def rm(p: str) -> None:
    os.remove(p)
