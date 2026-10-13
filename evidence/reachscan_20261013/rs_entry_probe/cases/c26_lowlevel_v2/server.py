import os
from mcp.server.lowlevel import Server


async def handle_call_tool(ctx, params):
    if params.name == "wipe":
        os.remove(params.arguments["path"])
    return "ok"


server = Server("demo", on_call_tool=handle_call_tool)
