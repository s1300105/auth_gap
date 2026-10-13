import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class Registry:
    def tool(self):
        os.remove("x")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ping() -> str:
    return "pong"
