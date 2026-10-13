"""L13: which calls put 'unresolved' into a unit's opaque_reasons."""
import logging
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l13")
log = logging.getLogger(__name__)


def _helper(x):
    return x + "!"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def no_calls(path: str) -> str:
    return path


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def in_tree_only(path: str) -> str:
    return _helper(path)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def builtin_len(path: str) -> str:
    return str(len(path))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def logger_only(path: str) -> str:
    log.info("hi %s", path)
    return path


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def read_file(path: str) -> str:
    with open(path) as f:
        return f.read()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def remove_file(path: str) -> str:
    os.remove(path)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def raise_only(path: str) -> str:
    raise ValueError(path)
