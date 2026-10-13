import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class Svc:
    def __init__(self):
        os.remove("/tmp/x")


svc = Svc()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ping() -> str:
    return "pong"
