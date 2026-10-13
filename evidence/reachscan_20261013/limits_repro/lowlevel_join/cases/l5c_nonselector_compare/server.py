"""L5c: peek (readOnlyHint=True) and wipe (readOnlyHint=False, destructiveHint=True).
After the name dispatch, a shared tail compares an *argument* with the string "wipe" and removes a cache file.
peek can reach that os.remove (arguments={"action": "wipe", ...})."""
import os

import mcp.types as types
from mcp.server.lowlevel import Server

server = Server("demo")


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="peek", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
        types.Tool(name="wipe", description="", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=False, destructiveHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "peek":
        with open(arguments["path"]) as f:
            text = f.read()
    elif name == "wipe":
        os.remove(arguments["path"])
        text = "ok"
    else:
        raise ValueError(name)
    action = arguments.get("action")
    if action == "wipe":
        os.remove(arguments["cache"])
    return [types.TextContent(type="text", text=text)]
