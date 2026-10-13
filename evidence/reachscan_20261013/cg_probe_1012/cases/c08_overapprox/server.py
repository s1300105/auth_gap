import os
import subprocess
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class Cache:
    def get(self, key):
        os.remove(key)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def lookup(key: str) -> str:
    d = {}
    return str(d.get(key))
