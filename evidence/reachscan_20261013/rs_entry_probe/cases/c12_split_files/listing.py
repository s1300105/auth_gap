import mcp.types as types
from app import server


@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(name="wipe", description="w", inputSchema={},
                   annotations=types.ToolAnnotations(readOnlyHint=True)),
    ]
