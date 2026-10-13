import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


def create_server() -> FastMCP:
    srv = FastMCP("demo")

    @srv.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def purge(path: str) -> str:
        os.remove(path)
        return "ok"

    return srv


app = create_server()
