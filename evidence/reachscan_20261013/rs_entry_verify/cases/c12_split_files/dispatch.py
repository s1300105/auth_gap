import os
from app import server


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "wipe":
        os.remove(arguments["path"])
        return "ok"
    raise ValueError(name)
