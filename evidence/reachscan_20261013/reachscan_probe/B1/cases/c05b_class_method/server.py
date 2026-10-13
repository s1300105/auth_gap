"""B1 case 5b: FastMCP tools declared through classes and methods. Every tool writes a file."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("notes")


class StaticTools:
    # (i) decorator on a function in a class body (module-level server object)
    @staticmethod
    @mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
    def save_static(path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return "ok"


class NoteServer:
    def __init__(self) -> None:
        self.mcp = FastMCP("notes2")
        # (ii) bound method registered by the call form of the decorator
        self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(self.save_bound)
        # (iii) bound method registered with add_tool
        self.mcp.add_tool(self.save_added, annotations=ToolAnnotations(readOnlyHint=True))
        self._register()

    def save_bound(self, path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return "ok"

    def save_added(self, path: str, content: str) -> str:
        with open(path, "w") as f:
            f.write(content)
        return "ok"

    def _register(self) -> None:
        # (iv) closure decorated with a three-level decorator inside a method
        @self.mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
        def save_nested(path: str, content: str) -> str:
            with open(path, "w") as f:
                f.write(content)
            return "ok"
