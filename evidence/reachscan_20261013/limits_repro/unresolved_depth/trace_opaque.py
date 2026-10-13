"""Instrument the frozen AuthGap (read-only, monkeypatch only) to see which AST node raises each
opaque reason. Usage: trace_opaque.py <case dir> [reason ...]. Writes JSON to stdout.

Does not modify /home/user/auth_gap. Patches ValResult.note_opaque in memory only.
"""
import ast
import collections
import contextlib
import io
import json
import sys

sys.path.insert(0, "/home/user/auth_gap")

import authgap.analyze as A  # noqa: E402
import authgap.val.engine as E  # noqa: E402
from authgap.cli import main  # noqa: E402

case = sys.argv[1]
want = set(sys.argv[2:]) or {"unresolved"}
current = {"unit": None}
hits = collections.defaultdict(list)

orig_f0a = A.analyze_unit_f0a


def wrapped_f0a(index, unit, options=None, *a, **k):
    prev = current["unit"]
    current["unit"] = getattr(unit, "tool_name", None) or getattr(unit, "qualname", None)
    try:
        return orig_f0a(index, unit, options, *a, **k)
    finally:
        current["unit"] = prev


A.analyze_unit_f0a = wrapped_f0a

orig_note = E.ValResult.note_opaque


def note(self, reason):
    if reason in want:
        f = sys._getframe(1)
        node = f.f_locals.get("node")
        scope = f.f_locals.get("scope")
        src = None
        if isinstance(node, ast.AST):
            try:
                src = ast.unparse(node)[:80]
            except Exception:
                src = type(node).__name__
        hits[current["unit"]].append({
            "reason": reason,
            "engine_fn": f.f_code.co_name,
            "engine_line": f.f_lineno,
            "node_type": type(node).__name__ if node is not None else None,
            "src": src,
            "relpath": getattr(scope, "relpath", None),
            "lineno": getattr(node, "lineno", None),
        })
    return orig_note(self, reason)


E.ValResult.note_opaque = note

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rc = main(["scan", case, "--population", "mcp_server"])
out = {}
for unit, lst in hits.items():
    seen = []
    for h in lst:
        key = (h["engine_fn"], h["engine_line"], h["relpath"], h["lineno"], h["src"])
        if key not in [tuple(s[k] for k in ("engine_fn", "engine_line", "relpath", "lineno", "src")) for s in seen]:
            seen.append(h)
    out[str(unit)] = seen
print(json.dumps({"rc": rc, "hits": out}, ensure_ascii=False, indent=1))
