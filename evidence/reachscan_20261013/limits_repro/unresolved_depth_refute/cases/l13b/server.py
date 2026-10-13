"""L13 refute: common operations that might or might not raise unit-level 'unresolved'."""
import json
import os
import os.path
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l13b")
BASE = "/srv/data"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def str_method(path: str) -> str:
    return path.strip().lower()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fstring(path: str) -> str:
    return f"{BASE}/{path}"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def join_path(path: str) -> str:
    return os.path.join(BASE, path)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def json_dump(path: str) -> str:
    return json.dumps({"p": path})


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def dict_get(opts: dict) -> str:
    return opts.get("k", "")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def path_read(path: str) -> str:
    return Path(path).read_text()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def isinstance_check(path: str) -> str:
    if isinstance(path, str):
        return path
    return ""


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def list_ops(path: str) -> list:
    out = []
    out.append(path)
    return sorted(out)
