import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


def make_server():
    return FastMCP("demo")


tools = make_server()


@tools.tool(annotations=ToolAnnotations(readOnlyHint=True))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
