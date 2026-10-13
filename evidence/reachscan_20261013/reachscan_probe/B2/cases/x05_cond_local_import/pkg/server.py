"""x05: a project-local helper imported inside try/except ImportError."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

try:
    from .fast import save
except ImportError:
    from .slow import save

mcp = FastMCP("x05_cond_local_import")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def cond_import_write(path: str) -> str:
    save(path, "x")
    return "ok"


if __name__ == "__main__":
    mcp.run()
