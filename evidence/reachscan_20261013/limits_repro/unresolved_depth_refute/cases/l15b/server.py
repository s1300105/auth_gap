"""L15 refute: tail-name descent from a builtin-typed receiver, with matching arity and a constant path."""
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l15b")
CACHE = "/tmp/app.cache"


class Trash:
    def clear(self):
        os.remove(CACHE)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def dict_clear(key: str) -> str:
    cache = {key: 1}
    cache.clear()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def param_dict_clear(opts: dict) -> str:
    opts.clear()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_clear(key: str) -> str:
    xs = [key]
    xs.clear()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def typed_trash(key: str) -> str:
    Trash().clear()
    return "ok"
