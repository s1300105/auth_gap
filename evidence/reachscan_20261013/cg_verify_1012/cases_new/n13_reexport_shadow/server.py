from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from b.tools import helper

mcp = FastMCP("demo")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wipe(path: str) -> str:
    helper(path)
    return "ok"
