from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from helpers import eval

mcp = FastMCP("l10_import")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_imported_eval(s: str) -> str:
    return str(eval(s))
