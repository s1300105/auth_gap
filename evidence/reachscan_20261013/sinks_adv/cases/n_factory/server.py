from helpers import make_req, make_httpx_tryimport, make2
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("n_factory")


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_factory_var(url: str) -> str:
    s = make_req()
    return s.get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_factory_chain(url: str) -> str:
    return make_req().get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_factory_tryimport(url: str) -> str:
    c = make_httpx_tryimport()
    return c.get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_factory_two_hop(url: str) -> str:
    c = make2()
    return c.get(url).text
