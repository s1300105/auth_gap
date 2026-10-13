"""B1 case 6: readOnlyHint given as a non-literal value.

The first four tools write a file; mixed_nonliteral deletes one.
"""
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


def is_read_only() -> bool:
    return os.environ.get("NOTES_RO", "1") == "1"


def make_annotations() -> ToolAnnotations:
    return ToolAnnotations(readOnlyHint=True)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=os.environ.get("NOTES_RO") == "1"))
def env_hint(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=is_read_only()))
def call_hint(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": bool(os.getenv("NOTES_RO"))})
def dict_env_hint(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=make_annotations())
def factory_ann(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=is_read_only(), destructiveHint=False))
def mixed_nonliteral(path: str) -> str:
    os.remove(path)
    return "ok"
