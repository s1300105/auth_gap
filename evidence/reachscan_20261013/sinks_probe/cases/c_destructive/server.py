import os
import shutil
import subprocess
from pathlib import Path
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c_destructive")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_os_remove(p: str) -> str:
    os.remove(p)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_shutil_copy(a: str, b: str) -> str:
    shutil.copy(a, b)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_with_two_opens(a: str, b: str) -> str:
    with open(a, "a") as f, open(b, "w") as g:
        g.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_copy_then_remove(a: str, b: str) -> str:
    shutil.copy(a, b); os.remove(a)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_subprocess_rm(p: str) -> str:
    subprocess.run(["rm", "-rf", p])
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_rmtree(p: str) -> str:
    shutil.rmtree(p)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_unlink(p: str) -> str:
    Path(p).unlink()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_open_w(p: str) -> str:
    f = open(p, "w")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_os_str_replace(s: str) -> str:
    os_name = s
    return os_name.replace("a", "b")


@mcp.tool(annotations=ToolAnnotations(destructiveHint=False))
def nd_default_ro_remove(p: str) -> str:
    os.remove(p)
    return "ok"
