"""B1 case 10: a server file at test_server.py (test/benchmark-looking path). The tool claims readOnlyHint=True and writes."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def save_test_server(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
