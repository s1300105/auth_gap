from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

from .safe import literal_only

mcp = FastMCP("l10_shadow")


def eval(x):  # noqa: A001  自作の eval（組込みを隠す）
    return literal_only(x)


def open(p, mode="r"):  # noqa: A001  自作の open（組込みを隠す）
    return p


compile = str  # noqa: A001  代入で隠す


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
    def eval(x):  # noqa: A001  関数の局所で隠す（対照）
        return x
    return str(eval(s))
