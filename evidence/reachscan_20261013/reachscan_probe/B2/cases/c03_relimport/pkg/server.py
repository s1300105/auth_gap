"""c03: write in a helper in another module, imported relatively / with an alias."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .io import save_plain
from .io import save_alias as persist
from . import io as store_io
import pkg.io

mcp = FastMCP("c03_relimport")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_plain(path: str) -> str:
    save_plain(path, "x")  # from .io import save_plain
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_alias(path: str) -> str:
    persist(path, "x")  # from .io import save_alias as persist
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_modalias(path: str) -> str:
    store_io.save_modalias(path, "x")  # from . import io as store_io
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_dotted(path: str) -> str:
    pkg.io.save_dotted(path, "x")  # import pkg.io
    return "ok"


if __name__ == "__main__":
    mcp.run()
