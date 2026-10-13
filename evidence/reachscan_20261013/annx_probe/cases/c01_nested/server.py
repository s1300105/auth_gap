import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


def register_tools(server: FastMCP) -> None:
    @server.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def wipe(path: str) -> str:
        os.remove(path)
        return "ok"


register_tools(mcp)
