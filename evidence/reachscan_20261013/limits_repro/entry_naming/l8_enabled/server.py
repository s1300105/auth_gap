"""L8a: jlowin fastmcp 2.x の enabled=False（既定で露出しない）。名前を位置引数で渡すか、name= で渡すかだけが違う。"""
import subprocess

from fastmcp import FastMCP

mcp = FastMCP("l8a")


@mcp.tool("run-cmd-pos", enabled=False)
def run_pos(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@mcp.tool(name="run-cmd-kw", enabled=False)
def run_kw(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
