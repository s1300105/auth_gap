"""c05: idempotentHint=True tools that append to a file."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c05_idempotent")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, idempotentHint=True))
def append_log(path: str, line: str) -> str:
    with open(path, "a") as f:  # SINK append (ro=False, idem=True)
        f.write(line + "\n")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(idempotentHint=True))
def append_log_idem_only(path: str, line: str) -> str:
    with open(path, "a") as f:  # SINK append (idem=True only)
        f.write(line + "\n")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
def append_log_nondestructive(path: str, line: str) -> str:
    with open(path, "a") as f:  # SINK append (ro=False, destr=False, idem=True)
        f.write(line + "\n")
    return "ok"


if __name__ == "__main__":
    mcp.run()
