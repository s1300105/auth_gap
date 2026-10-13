import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class A:
    class Meta:
        def build(self):
            return 1


class B:
    class Meta:
        def build(self):
            os.remove("/tmp/x")


def helper():
    return A.Meta().build()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def safe() -> str:
    helper()
    return "ok"
