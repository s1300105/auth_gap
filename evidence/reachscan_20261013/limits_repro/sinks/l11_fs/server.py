import os
from pathlib import Path

import aiofiles
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l11_fs")


# ---- 対照（表に行があるもの） ----
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_os_replace(p: str, q: str) -> str:
    os.replace(p, q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_ctl_os_replace(p: str, q: str) -> str:
    os.replace(p, q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_path_unlink(p: str) -> str:
    Path(p).unlink()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_open_w(p: str, c: str) -> str:
    with open(p, "w") as f:
        f.write(c)
    return "ok"


# ---- 表に行が無いもの ----
@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_os_open(p: str, c: str) -> str:
    fd = os.open(p, os.O_WRONLY | os.O_CREAT | os.O_TRUNC)
    os.write(fd, c.encode())
    os.close(fd)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_os_open(p: str, c: str) -> str:
    fd = os.open(p, os.O_WRONLY | os.O_TRUNC)
    os.write(fd, c.encode())
    os.close(fd)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_os_truncate(p: str) -> str:
    os.truncate(p, 0)
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
def nd_path_rename(p: str, q: str) -> str:
    Path(p).rename(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_path_replace(p: str, q: str) -> str:
    Path(p).replace(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_replace_var(p: str, q: str) -> str:
    src = Path(p)
    src.replace(q)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ro_aiofiles_open_w(p: str, c: str) -> str:
    async with aiofiles.open(p, "w") as f:
        await f.write(c)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
async def nd_aiofiles_open_w(p: str, c: str) -> str:
    async with aiofiles.open(p, mode="w") as f:
        await f.write(c)
    return "ok"
