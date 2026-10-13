"""x02: open() mode spellings and other open APIs (all readOnlyHint=True)."""
import io
import os
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x02_open_modes")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_w(path: str) -> str:
    with open(path, "w") as f:  # SINK mode w (control)
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_wplus(path: str) -> str:
    with open(path, "w+") as f:  # SINK mode w+
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_aplus(path: str) -> str:
    with open(path, "a+") as f:  # SINK mode a+
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_rplus(path: str) -> str:
    with open(path, "r+") as f:  # SINK mode r+
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_wt(path: str) -> str:
    with open(path, "wt", encoding="utf-8") as f:  # SINK mode wt
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_modevar(path: str) -> str:
    mode = "w"
    with open(path, mode) as f:  # SINK mode from a local variable
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_path_open(path: str) -> str:
    with Path(path).open("w") as f:  # SINK Path.open("w")
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_io_open(path: str) -> str:
    with io.open(path, "w") as f:  # SINK io.open("w")
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def m_os_open(path: str) -> str:
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)  # SINK os.open(O_WRONLY|O_TRUNC)
    os.write(fd, b"x")
    os.close(fd)
    return "ok"


if __name__ == "__main__":
    mcp.run()
