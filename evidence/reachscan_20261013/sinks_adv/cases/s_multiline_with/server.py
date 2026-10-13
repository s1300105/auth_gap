import os
import shutil
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("s_multiline_with")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_two_opens_two_lines(a: str, b: str) -> str:
    with (open(a, "a") as f,
          open(b, "w") as g):
        g.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_remove_then_copy(a: str, b: str) -> str:
    os.remove(a); shutil.copy(b, a)
    return "ok"
