"""c06: destructiveHint=False with readOnlyHint=False, deleting in several ways."""
import os
import shutil
import subprocess
from pathlib import Path

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c06_destructive")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_os_remove(path: str) -> str:
    os.remove(path)  # SINK os.remove
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_subprocess(path: str) -> str:
    subprocess.run(["rm", "-rf", path], check=True)  # SINK subprocess rm -rf
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_path_unlink(path: str) -> str:
    Path(path).unlink()  # SINK Path.unlink
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_rmtree(path: str) -> str:
    shutil.rmtree(path)  # SINK shutil.rmtree
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_rmdir(path: str) -> str:
    os.rmdir(path)  # SINK os.rmdir (extra)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_truncate(path: str) -> str:
    os.truncate(path, 0)  # SINK os.truncate (extra)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def rm_move(src: str, dst: str) -> str:
    shutil.move(src, dst)  # SINK shutil.move (extra)
    return "ok"


if __name__ == "__main__":
    mcp.run()
