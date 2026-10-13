"""B1 case 1c: snake_case hints, third-party fastmcp; no dependency file, so the mcp major version is not stated.

Every tool writes a file. Only the spelling of the readOnlyHint claim differs.
"""
from fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_obj(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"read_only_hint": True})
def snake_dict(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, read_only_hint=True))
def both_spellings(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def camel_ctl(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
