from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v_prefix")


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_dict_named_requests(key: str) -> str:
    requests_seen = {"a": "1"}
    return str(requests_seen.get(key))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_shutil_prefixed_obj(a: str) -> str:
    shutil_log = []
    shutil_log.copy()
    return a
