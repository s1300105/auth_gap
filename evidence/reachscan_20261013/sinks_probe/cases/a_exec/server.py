import asyncio
import os
import subprocess
import subprocess as sp
from subprocess import run as srun
from re import compile as re_compile
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("a_exec")
RO = ToolAnnotations(readOnlyHint=True)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_sub_run(p: str) -> str:
    return str(subprocess.run(["ls", p]))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_check_output(p: str) -> str:
    return subprocess.check_output(["ls", p]).decode()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_from_run(p: str) -> str:
    return str(srun(["ls", p]))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_alias_sp(p: str) -> str:
    return str(sp.run(["ls", p]))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def ro_async_exec(p: str) -> str:
    proc = await asyncio.create_subprocess_exec("ls", p)
    return str(proc)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_os_popen(p: str) -> str:
    return os.popen("ls " + p).read()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_eval(expr: str) -> str:
    return str(eval(expr))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_re_compile(pattern: str) -> str:
    return str(re_compile(pattern).pattern)
