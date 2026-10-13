import subprocess
from fastmcp import FastMCP

mcp = FastMCP("demo")


@mcp.tool(enabled=False)
def run_noname(cmd: str) -> str:
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
