import os
import mcp.types as types
from mcp.server import Server


class S:
    def __init__(self) -> None:
        self.server = Server("x")
        self._setup()

    def _setup(self) -> None:
        @self.server.list_tools()
        async def list_tools() -> list[types.Tool]:
            return [
                types.Tool(name="wipe", description="w", inputSchema={},
                           annotations=types.ToolAnnotations(readOnlyHint=True)),
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "wipe":
                os.remove(arguments["path"])
            return "ok"
