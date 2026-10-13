import os
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

mcp = MCPServer("demo")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def wipe(path: str) -> str:
    os.remove(path)
    return "ok"
