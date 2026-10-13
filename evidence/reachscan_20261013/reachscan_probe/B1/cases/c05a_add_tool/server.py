"""B1 case 5a: tools registered by call instead of decorator. Both registered tools write a file.

ping is an ordinary decorated tool so that the tree has at least one detected entry point.
"""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


def save_added(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


def save_call_form(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


mcp.add_tool(save_added, annotations=ToolAnnotations(readOnlyHint=True))
mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(save_call_form)


@mcp.tool()
def ping() -> str:
    return "pong"
