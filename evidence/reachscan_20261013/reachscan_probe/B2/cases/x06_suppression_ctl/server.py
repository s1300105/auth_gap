"""x06: suppression tags and the exit code (closed-world mismatch is medium)."""
import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x06_suppression_ctl")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_write_suppressed(path: str) -> str:
    with open(path, "w") as f:
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def cw_get_send_suppressed(url: str) -> str:
    return requests.get(url).text


if __name__ == "__main__":
    mcp.run()
