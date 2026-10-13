import asyncio
import socket
import httpx
import importlib as il
from importlib import import_module
from os import remove
from shutil import move
from psycopg2 import connect as pg_connect
from urllib.request import Request
from httpx import BasicAuth
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("m_misc")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_from_import_module(name: str) -> str:
    return str(import_module(name))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_il_import_module() -> str:
    return str(il.import_module("json"))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_from_remove(p: str) -> str:
    remove(p)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False))
def nd_from_move(a: str, b: str) -> str:
    move(a, b)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_from_pg_connect(dsn: str) -> str:
    pg_connect(dsn)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_disconnect(obj) -> str:
    obj.disconnect()
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_socket_obj_connect(host: str) -> str:
    s = socket.socket()
    s.connect((host, 80))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
async def cw_asyncio_open_connection() -> str:
    r, w = await asyncio.open_connection("example.com", 80)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_socket_create_connection_ext() -> str:
    socket.create_connection(("example.com", 80))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_urllib_request_obj(url: str) -> str:
    req = Request(url)
    return req.full_url


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_httpx_basicauth(u: str, p: str) -> str:
    a = BasicAuth(u, p)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_annassign_client(url: str) -> str:
    hc: httpx.Client = httpx.Client()
    return hc.get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_kw_url_literal() -> str:
    return httpx.Client().get(url="https://example.com/x").text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_posarg_url_literal() -> str:
    return httpx.Client().get("https://example.com/x").text
