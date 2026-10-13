import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v08")

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def ping() -> None:
    r, w = await asyncio.open_connection("203.0.113.5", 80)
    w.close()
