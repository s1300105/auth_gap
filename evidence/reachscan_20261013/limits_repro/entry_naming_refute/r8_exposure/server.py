import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool("run-cmd-pos")
def run_pos(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@mcp.tool(name="run-cmd-kw")
def run_kw(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
