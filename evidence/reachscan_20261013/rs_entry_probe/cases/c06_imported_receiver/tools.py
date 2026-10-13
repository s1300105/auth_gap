import os
from mcp.types import ToolAnnotations
from core import my_server, mcp


@my_server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge_my(path: str) -> str:
    os.remove(path)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge_mcp(path: str) -> str:
    os.remove(path)
    return "ok"
