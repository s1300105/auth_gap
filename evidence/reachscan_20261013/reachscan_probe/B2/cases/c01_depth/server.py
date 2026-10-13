"""c01: helper chains of exactly N calls before open(path, "w") (N = 4, 5, 8, 9)."""
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("c01_depth")

# chain a: tool -> a1 -> ... -> a4; open() is in a4 (4 call edges from the tool)
def a1(p):
    return a2(p)

def a2(p):
    return a3(p)

def a3(p):
    return a4(p)

def a4(p):
    with open(p, "w") as f:  # SINK chain4
        f.write("a")
    return "ok"


# chain b: tool -> b1 -> ... -> b5; open() is in b5 (5 call edges from the tool)
def b1(p):
    return b2(p)

def b2(p):
    return b3(p)

def b3(p):
    return b4(p)

def b4(p):
    return b5(p)

def b5(p):
    with open(p, "w") as f:  # SINK chain5
        f.write("b")
    return "ok"


# chain c: tool -> c1 -> ... -> c8; open() is in c8 (8 call edges from the tool)
def c1(p):
    return c2(p)

def c2(p):
    return c3(p)

def c3(p):
    return c4(p)

def c4(p):
    return c5(p)

def c5(p):
    return c6(p)

def c6(p):
    return c7(p)

def c7(p):
    return c8(p)

def c8(p):
    with open(p, "w") as f:  # SINK chain8
        f.write("c")
    return "ok"


# chain d: tool -> d1 -> ... -> d9; open() is in d9 (9 call edges from the tool)
def d1(p):
    return d2(p)

def d2(p):
    return d3(p)

def d3(p):
    return d4(p)

def d4(p):
    return d5(p)

def d5(p):
    return d6(p)

def d6(p):
    return d7(p)

def d7(p):
    return d8(p)

def d8(p):
    return d9(p)

def d9(p):
    with open(p, "w") as f:  # SINK chain9
        f.write("d")
    return "ok"


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def chain4(path: str) -> str:
    return a1(path)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def chain5(path: str) -> str:
    return b1(path)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def chain8(path: str) -> str:
    return c1(path)


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
def chain9(path: str) -> str:
    return d1(path)


if __name__ == "__main__":
    mcp.run()
