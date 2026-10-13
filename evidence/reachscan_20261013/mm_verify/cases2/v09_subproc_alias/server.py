import os
import asyncio
import subprocess
import subprocess as sp
from subprocess import run
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("v09")

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_alias() -> None:
    sp.run(["echo", "x"])

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_from() -> None:
    run(["echo", "x"])

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_check_output() -> bytes:
    return subprocess.check_output(["echo", "x"])

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def t_popen() -> str:
    return os.popen("echo x").read()

@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def t_async() -> None:
    await asyncio.create_subprocess_exec("echo", "x")
