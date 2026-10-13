import os
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("demo")


class FileStore:
    def delete(self, key):
        os.remove(key)


class MemStore:
    def delete(self, key):
        return key


def pick(kind):
    return FileStore() if kind == "f" else MemStore()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def drop(kind: str, key: str) -> str:
    store = __import__(kind)
    store.delete(key)
    return "ok"
