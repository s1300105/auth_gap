import os


def _load():
    from mcp.server.fastmcp import FastMCP
    from mcp.types import ToolAnnotations
    return FastMCP, ToolAnnotations


srv = FastMCP("demo")


@srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
def purge(path: str) -> str:
    os.remove(path)
    return "ok"
