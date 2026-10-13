import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l10_descend")


def eval(x):  # noqa: A001  自作の eval。中で削除する
    os.remove(x)
    return x


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_shadow_eval_removes(p: str) -> str:
    return eval(p)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, openWorldHint=False))
def nd_shadow_eval_const() -> str:
    return eval("/tmp/x")
