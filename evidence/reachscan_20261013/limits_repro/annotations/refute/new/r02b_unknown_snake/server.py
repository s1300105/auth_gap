from mcp.types import ToolAnnotations
from somewhere import mcp

RO = True


@mcp.tool(annotations=ToolAnnotations(read_only_hint=RO))
def snake_nl(path: str, text: str) -> str:
    with open(path, "w") as f:
        f.write(text)
    return "ok"
