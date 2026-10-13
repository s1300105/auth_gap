import os
import shutil
from pathlib import Path

import aiofiles
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l11_fs")
RO = ToolAnnotations(readOnlyHint=True)
ND = ToolAnnotations(readOnlyHint=False, destructiveHint=False)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_os_replace(p: str, q: str) -> str:
    os.replace(p, q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_ctl_os_replace(p: str, q: str) -> str:
    os.replace(p, q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_open_w(p: str) -> str:
    with open(p, "w") as f:
        f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_os_open(p: str) -> str:
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, b"x")
    os.close(fd)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_os_truncate(p: str) -> str:
    os.truncate(p, 0)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_path_rename(p: str, q: str) -> str:
    Path(p).rename(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_replace(p: str, q: str) -> str:
    Path(p).replace(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_replace_var(p: str, q: str) -> str:
    src = Path(p)
    src.replace(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ro_aiofiles_open_w(p: str) -> str:
    async with aiofiles.open(p, "w") as f:
        await f.write("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_rmdir(p: str) -> str:
    Path(p).rmdir()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_path_touch(p: str) -> str:
    Path(p).touch()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_os_removedirs(p: str) -> str:
    os.removedirs(p)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_shutil_copytree(p: str, q: str) -> str:
    shutil.copytree(p, q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
async def nd_aiofiles_os_remove(p: str) -> str:
    await aiofiles.os.remove(p)
    return "ok"
