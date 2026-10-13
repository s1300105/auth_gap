import os
import shutil
from pathlib import Path

import aiofiles
import aiofiles.os
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l11_adjacent")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_path_rmdir(p: str) -> str:
    Path(p).rmdir()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_path_touch(p: str) -> str:
    Path(p).touch()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_open_then_truncate(p: str) -> str:
    with open(p, "r+") as f:
        f.truncate(0)
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


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def rocw_client_stream_delete(url: str) -> str:
    with httpx.Client() as c:
        with c.stream("DELETE", url) as r:
            return r.read().decode()


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_client_get_ctl(url: str) -> str:
    with httpx.Client() as c:
        return c.get(url).text
