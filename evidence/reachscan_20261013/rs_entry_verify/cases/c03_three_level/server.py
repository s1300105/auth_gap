import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


class Holder:
    mcp = FastMCP("demo")


@Holder.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge(path: str) -> str:
    os.remove(path)
    return "ok"


class Service:
    def __init__(self) -> None:
        self.mcp = FastMCP("svc")
        self._register()

    def _register(self) -> None:
        @self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
        def purge2(path: str) -> str:
            os.remove(path)
            return "ok"
