"""c07: openWorldHint=False tools that talk to the network."""
import socket

import httpx
import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c07_openworld")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def post_nonliteral(url: str, body: str) -> str:
    r = requests.post(url, json={"b": body})  # SINK requests.post(non-literal url)
    return r.text


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def get_loopback() -> str:
    r = httpx.get("http://127.0.0.1:8000/health")  # SINK httpx.get(loopback literal)
    return r.text


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def sock_connect(host: str) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 9000))  # SINK socket connect via instance
    s.close()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def sock_create_connection(host: str) -> str:
    c = socket.create_connection((host, 9000))  # SINK socket.create_connection(non-literal) (extra)
    c.close()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def sock_create_connection_loopback() -> str:
    c = socket.create_connection(("127.0.0.1", 9000))  # SINK socket.create_connection(loopback) (extra)
    c.close()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def get_external_literal() -> str:
    r = httpx.get("https://example.com/")  # SINK httpx.get(external literal) (control)
    return r.text


if __name__ == "__main__":
    mcp.run()
