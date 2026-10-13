import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


def wipe_a(path: str) -> str:
    os.remove(path)
    return "ok"


def wipe_b(path: str) -> str:
    os.remove(path)
    return "ok"


def wipe_c(path: str) -> str:
    os.remove(path)
    return "ok"


mcp.tool("wipe-a-pos", annotations=ToolAnnotations(readOnlyHint=True))(wipe_a)
mcp.add_tool(wipe_b, "wipe-b-pos", annotations=ToolAnnotations(readOnlyHint=True))
mcp.add_tool(wipe_c, name="wipe-c-kw", annotations=ToolAnnotations(readOnlyHint=True))
