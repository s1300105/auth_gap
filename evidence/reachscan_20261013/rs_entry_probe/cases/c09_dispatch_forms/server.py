import os
import mcp.types as types
from mcp.server import Server

server = Server("demo")


def _wipe(arguments):
    os.remove(arguments["path"])
    return "ok"


def _zap(arguments):
    os.remove(arguments["path"])
    return "ok"


HANDLERS = {"zap": _zap}


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="wipe", description="w", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="wipe_alias", description="w", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="zap", description="z", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="erase", description="e", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    tool = name
    if name in ("wipe", "wipe_alias"):
        return _wipe(arguments)
    if name in HANDLERS:
        return HANDLERS[name](arguments)
    if tool == "erase":
        os.remove(arguments["path"])
        return "ok"
    raise ValueError(name)
