import subprocess
from fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool("run-cmd-pos", enabled=False)
def run_pos(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@mcp.tool(name="run-cmd-kw", enabled=False)
def run_kw(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
