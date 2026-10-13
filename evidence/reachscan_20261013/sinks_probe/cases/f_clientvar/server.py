import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("f_clientvar")


def setup() -> None:
    client = httpx.Client()
    client.close()


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def ow_dict_get(key: str) -> str:
    client = {"a": "1"}
    return str(client.get(key))
