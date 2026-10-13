import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("h07")

@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def status() -> str:
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as c:
        r = await c.get("/x")
        return r.text
