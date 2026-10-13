"""L1 (snake_case, mcp>=2): read_only_hint=<module constant True>. Body writes a file."""
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

mcp = MCPServer("notes")
RO = True


@mcp.tool(annotations=ToolAnnotations(read_only_hint=RO))
def snake_nonlit(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(read_only_hint=True))
def snake_lit(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
