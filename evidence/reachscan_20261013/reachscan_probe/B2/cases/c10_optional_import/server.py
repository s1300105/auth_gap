"""c10: optional import guarded write, import alias of os.remove, conditional def."""
from os import remove as rm

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

try:
    import yaml
except ImportError:
    yaml = None

mcp = FastMCP("c10_optional_import")

if yaml is not None:
    def _dump(path, data):
        with open(path, "w") as f:  # SINK conditional def
            yaml.safe_dump(data, f)
else:
    def _dump(path, data):
        with open(path, "w") as f:  # SINK conditional def (fallback)
            f.write(repr(data))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def dump_yaml(path: str, key: str, value: str) -> str:
    if yaml is None:
        return "yaml missing"
    with open(path, "w") as f:  # SINK behind optional import
        yaml.safe_dump({key: value}, f)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def delete_alias(path: str) -> str:
    rm(path)  # SINK from os import remove as rm
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def dump_cond_def(path: str, key: str) -> str:
    _dump(path, {key: 1})  # helper defined under `if yaml is not None:` (extra)
    return "ok"


if __name__ == "__main__":
    mcp.run()
