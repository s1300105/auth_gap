"""x04: read-only tools that only call str.replace / list.remove on values whose name starts with os."""
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x04_replace_fp")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fp_env_replace() -> str:
    return os.environ.get("HOME", "").replace("\\", "/")  # str.replace on os.environ.get(...)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fp_join_replace(a: str, b: str) -> str:
    return os.path.join(a, b).replace("\\", "/")  # str.replace on os.path.join(...)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fp_getcwd_replace() -> str:
    return os.getcwd().replace("\\", "/")  # str.replace on os.getcwd()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def fp_list_remove(x: int) -> str:
    ostrich = [1, 2, 3]
    ostrich.remove(x)  # list.remove on a local named ostrich
    return str(ostrich)


if __name__ == "__main__":
    mcp.run()
