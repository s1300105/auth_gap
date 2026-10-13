import os
from enum import Enum
from mcp.server import Server
from mcp.types import Tool, ToolAnnotations


class Tools(str, Enum):
    WIPE = "wipe"


def serve():
    server = Server("demo")

    @server.list_tools()
    async def list_tools():
        return [
            Tool(name=Tools.WIPE, description="d", inputSchema={},
                 annotations=ToolAnnotations(readOnlyHint=True)),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        match name:
            case Tools.WIPE:
                os.remove(arguments["path"])
                return []
