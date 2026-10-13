"""x03: process / code execution spellings (all readOnlyHint=True)."""
import asyncio
import os
import subprocess
import subprocess as sp
from subprocess import run as run_cmd

from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("x03_exec_variants")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_subprocess_run(arg: str) -> str:
    subprocess.run(["ls", arg], check=False)  # SINK subprocess.run (control)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_module_alias(arg: str) -> str:
    sp.run(["ls", arg], check=False)  # SINK import subprocess as sp
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_from_import(arg: str) -> str:
    run_cmd(["ls", arg], check=False)  # SINK from subprocess import run as run_cmd
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_check_output(arg: str) -> str:
    return subprocess.check_output(["ls", arg]).decode()  # SINK subprocess.check_output


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_os_popen(arg: str) -> str:
    return os.popen("ls " + arg).read()  # SINK os.popen


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def e_asyncio_exec(arg: str) -> str:
    proc = await asyncio.create_subprocess_exec("ls", arg)  # SINK asyncio.create_subprocess_exec
    await proc.wait()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_os_system(arg: str) -> str:
    os.system("ls " + arg)  # SINK os.system (control)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def e_eval(expr: str) -> str:
    return str(eval(expr))  # SINK eval


if __name__ == "__main__":
    mcp.run()
