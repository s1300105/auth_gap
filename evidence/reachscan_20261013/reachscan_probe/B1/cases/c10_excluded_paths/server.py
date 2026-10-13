"""B1 case 10 (control): an ordinary server file at the tree root. Claims readOnlyHint=True and writes."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def save_root(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
