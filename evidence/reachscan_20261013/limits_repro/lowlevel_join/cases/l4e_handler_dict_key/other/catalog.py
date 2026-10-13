"""A client-side catalog in the same tree (not served by server.py)."""
import mcp.types as types

CATALOG = [
    types.Tool(name="status", description="", inputSchema={},
               annotations=types.ToolAnnotations(readOnlyHint=True)),
]
