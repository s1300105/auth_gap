import os
import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v11")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def rm(p: str) -> None:
    await asyncio.to_thread(os.remove, p)
