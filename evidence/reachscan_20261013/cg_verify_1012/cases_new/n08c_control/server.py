import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class Base:
    def __init__(self):
        self.x = 1


class Danger:
    def __init__(self):
        os.remove("/tmp/x")


class Child(Base):
    def setup(self):
        return 1


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def make() -> str:
    c = Child()
    c.setup()
    return "ok"
