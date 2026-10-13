"""L14: project-local helper imported inside try/except ImportError (the try branch is the one that
normally runs)."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

try:
    from .fast import save
except ImportError:
    from .slow import save

mcp = FastMCP("l14_try")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def cond_import(path: str) -> str:
    return save(path)
