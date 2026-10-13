"""Independent tracer: patch ValResult.note_opaque in memory; record caller line and node per unit."""
import ast, collections, json, sys
sys.path.insert(0, "/home/user/auth_gap")
import authgap.val.engine as E
from authgap.runner import RunConfig, run
from authgap.report import manifest_json, probe_json
hits = []
orig = E.ValResult.note_opaque
def note(self, reason):
    f = sys._getframe(1)
    node = f.f_locals.get("node")
    try: src = ast.unparse(node)[:70] if isinstance(node, ast.AST) else None
    except Exception: src = None
    hits.append((id(self), reason, f.f_code.co_name, f.f_lineno, src, getattr(node, "lineno", None)))
    return orig(self, reason)
E.ValResult.note_opaque = note
case = sys.argv[1]
res = run(RunConfig(src_root=case, population="mcp_server", full=True))
m = manifest_json(res, "x")
# map ValResult ids to unit names
idmap = {}
for ur in res.tree.units:
    v = getattr(ur, "val", None)
    if v is not None: idmap[id(v)] = ur.unit.tool_name
by = collections.defaultdict(list)
for h in hits:
    k = idmap.get(h[0], "?")
    t = h[1:]
    if t not in by[k]: by[k].append(t)
for u in m["units"]:
    n = u["unit"]["tool_name"]
    print(n, "opaque", u["opaque_reasons"], "eff", [(e.get("site"), e["kind"], e["resolution"]) for e in u["effects"]], [r["verdicts"] for r in u["rows"]])
    for t in by.get(n, []): print("    ", t)
p = probe_json(res, "x")
print({k: p[k] for k in p if "ratio" in k or "resolution" in k})
