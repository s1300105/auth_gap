"""c02: writes reached only through method calls on instances."""
import os

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c02_unresolved_method")


class Store:
    def save(self, path, data):
        with open(path, "w") as f:  # SINK Store.save
            f.write(data)


class Exporter:
    def __init__(self):
        self._store = Store()

    def export(self, path):
        self._store.save(path, "x")  # self._store.save(...)

    def export_direct(self, path):
        self._write(path)  # self.<method>() in the same class

    def _write(self, path):
        with open(path, "w") as f:  # SINK Exporter._write
            f.write("y")


class Trash:
    def clear(self, path):
        os.remove(path)  # SINK Trash.clear (no tool calls Trash().clear)


STORE = Store()
EXPORTER = Exporter()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def save_new_instance(path: str) -> str:
    Store().save(path, "x")  # instance created in the tool
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def save_module_instance(path: str) -> str:
    STORE.save(path, "x")  # module-level instance
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def export_via_self_attr(path: str) -> str:
    EXPORTER.export(path)  # -> self._store.save(...)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def export_via_self_method(path: str) -> str:
    EXPORTER.export_direct(path)  # -> self._write(...)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def name_only_match(key: str) -> str:
    cache = {key: 1}
    cache.pop(key, None)  # control: no method named clear
    return "ok"


if __name__ == "__main__":
    mcp.run()
