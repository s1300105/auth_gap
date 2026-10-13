"""L8d: 呼び出し形の登録（D64 / U40 で入口にした形）での名前の読み。"""
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l8d")
RO = ToolAnnotations(readOnlyHint=True)


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
