"""L8b: 運用者の exposure ファイル（--exposure）が登録名で deny する。名前の渡し方だけが違う。"""
import subprocess

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("l8b")


@mcp.tool("run-cmd-pos")
def run_pos(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@mcp.tool(name="run-cmd-kw")
def run_kw(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
