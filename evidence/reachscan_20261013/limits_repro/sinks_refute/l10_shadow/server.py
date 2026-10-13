from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("l10_shadow")


def eval(x):
    return x


def open(p, mode="r"):
    return p


compile = str


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_shadow_eval(s: str) -> str:
    return str(eval(s))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_shadow_open_w(p: str) -> str:
    return str(open(p, "w"))


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_shadow_compile_assign(s: str) -> str:
    return compile(s)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_ctl_local_shadow(s: str) -> str:
    def eval(x):
        return x
    return str(eval(s))
