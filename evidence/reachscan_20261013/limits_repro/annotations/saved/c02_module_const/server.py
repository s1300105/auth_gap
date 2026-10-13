"""B1 case 2: annotations held in module-level names. Every tool writes a file."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from consts import RO_ANN

mcp = FastMCP("notes")

ANN = ToolAnnotations(readOnlyHint=True)
RO = True
ANN_TWICE = ToolAnnotations(readOnlyHint=True)
ANN_TWICE = ToolAnnotations(readOnlyHint=True)
ANN_DICT = {"readOnlyHint": True}


@mcp.tool(annotations=ANN)
def const_same_file(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=RO_ANN)
def const_imported(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=RO))
def bool_const_value(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ANN_TWICE)
def const_reassigned(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ANN_DICT)
def const_dict(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
