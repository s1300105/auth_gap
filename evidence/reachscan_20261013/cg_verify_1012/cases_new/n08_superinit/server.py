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
    def __init__(self):
        super().__init__()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def make() -> str:
    c = Child()
    c.__init__()
    return "ok"
