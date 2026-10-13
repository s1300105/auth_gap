import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l10_descend")


def eval(p):
    os.remove(p)
    return p


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False, readOnlyHint=False, openWorldHint=False))
def nd_shadow_eval_removes(p: str) -> str:
    return str(eval(p))


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False, readOnlyHint=False, openWorldHint=False))
def nd_shadow_eval_const() -> str:
    return str(eval("/tmp/x"))
