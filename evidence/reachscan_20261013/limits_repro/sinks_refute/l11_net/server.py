import socket
import webbrowser

import aiohttp
import httpx
import requests
import websockets
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l11_net")
CW = ToolAnnotations(openWorldHint=False)
ROCW = ToolAnnotations(readOnlyHint=True, openWorldHint=False)


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_ctl_requests_get(url: str) -> str:
    return requests.get(url).text


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def rocw_ctl_requests_delete(url: str) -> str:
    return requests.delete(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_ctl_requests_get_localhost() -> str:
    return requests.get("http://localhost:8000/x").text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_webbrowser_open(url: str) -> str:
    webbrowser.open(url)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def cw_websockets_connect(url: str) -> str:
    async with websockets.connect(url) as ws:
        await ws.send("x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_socket_create_connection(host: str) -> str:
    s = socket.create_connection((host, 443))
    s.sendall(b"x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_httpx_stream(url: str) -> str:
    with httpx.stream("GET", url) as r:
        return r.text


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def rocw_httpx_stream_delete(url: str) -> str:
    with httpx.stream("DELETE", url) as r:
        return r.text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def cw_aiohttp_session_get(url: str) -> str:
    async with aiohttp.ClientSession() as s:
        r = await s.get(url)
        return await r.text()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
async def rocw_aiohttp_session_delete(url: str) -> str:
    async with aiohttp.ClientSession() as s:
        r = await s.delete(url)
        return await r.text()


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def cw_aiohttp_request(url: str) -> str:
    async with aiohttp.request("GET", url) as r:
        return await r.text()


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def rocw_client_stream_delete(url: str) -> str:
    with httpx.Client() as c:
        with c.stream("DELETE", url) as r:
            return r.text
