from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("r_eval_shadow")


def eval(x):
    return x


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def ro_custom_eval(s: str) -> str:
    return str(eval(s))
