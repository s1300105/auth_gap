"""FastMCP: reader has readOnlyHint=True and only reads."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def reader(path: str) -> str:
    with open(path) as f:
        return f.read()
