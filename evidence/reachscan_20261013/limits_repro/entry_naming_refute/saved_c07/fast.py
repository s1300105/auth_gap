"""B1 case 7 (FastMCP): the registered tool name differs from the function name. Both write a file."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes-fast")


@mcp.tool(name="write-memo", annotations=ToolAnnotations(readOnlyHint=True))
def memo_impl(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool("write-memo-positional", annotations=ToolAnnotations(readOnlyHint=True))
def memo_impl_positional(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
