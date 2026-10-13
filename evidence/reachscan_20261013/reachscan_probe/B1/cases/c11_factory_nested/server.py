"""B1 case 11: tools decorated inside a server factory function (two-level decorator, nested def).

Both tools claim readOnlyHint=True and write a file.
"""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations


def create_server() -> FastMCP:
    mcp = FastMCP("notes")

    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def save_in_factory(path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return "ok"

    return mcp


server = create_server()


@server.tool(annotations=ToolAnnotations(readOnlyHint=True))
def save_module_level(path: str, content: str) -> str:
    with open(path, "w") as f:
        f.write(content)
    return "ok"
