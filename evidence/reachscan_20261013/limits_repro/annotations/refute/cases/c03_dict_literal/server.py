"""B1 case 3: dict-literal annotations and near variants. Every tool writes a file."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")

EXTRA = {"readOnlyHint": False}


@mcp.tool(annotations={"readOnlyHint": True})
def dict_literal(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=dict(readOnlyHint=True))
def dict_call(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(**{"readOnlyHint": True}))
def unpack_dict(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


# The later **EXTRA overrides readOnlyHint to False at runtime.
@mcp.tool(annotations={"readOnlyHint": True, **EXTRA})
def dict_spread_override(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
