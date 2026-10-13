"""LangChain のエージェントが使うツール。MCP には登録されない。"""
import subprocess

from langchain_core.tools import tool


@tool
def lc_shell(cmd: str) -> str:
    """Run a shell command."""
    return subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout


@tool("lc-search", return_direct=True)
def lc_search(q: str) -> str:
    """Search."""
    with open("/tmp/log.txt", "a") as f:
        f.write(q)
    return q
