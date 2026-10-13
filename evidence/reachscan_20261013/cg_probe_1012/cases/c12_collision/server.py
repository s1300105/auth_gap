import os
import subprocess
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


def helper(p):
    return p


def other(p):
    def helper(q):
        os.remove(q)
    helper(p)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def safe(path: str) -> str:
    return helper(path)
