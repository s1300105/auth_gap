import smtplib
import socket
import subprocess
import webbrowser
from http import HTTPStatus
import httpx
import psycopg2
import requests
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("d_closed_world")


class Holder:
    def __init__(self):
        self.http = httpx.Client()


HOLDER = Holder()


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_requests_get(url: str) -> str:
    return requests.get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_attr_client(url: str) -> str:
    return HOLDER.http.get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_session_inline(url: str) -> str:
    return requests.Session().get(url).text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_http_status(code: int) -> str:
    return str(HTTPStatus(code))


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_psycopg(dsn: str) -> str:
    conn = psycopg2.connect(dsn)
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_webbrowser() -> str:
    webbrowser.open("https://example.com/x")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_request_method_first(client) -> str:
    return client.request("GET", "https://example.com/x").text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_localhost_http() -> str:
    return requests.get("http://localhost:8080/health").text


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_socket_loopback() -> str:
    s = socket.create_connection(("127.0.0.1", 8080))
    return "ok"


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_subprocess_curl(url: str) -> str:
    return str(subprocess.run(["curl", url]))


@mcp.tool(annotations=ToolAnnotations(openWorldHint=False))
def cw_smtp(host: str) -> str:
    s = smtplib.SMTP(host)
    s.sendmail("a@x", ["b@y"], "hi")
    return "ok"
