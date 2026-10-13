"""Run frozen AuthGap with a different Options(max_depth) in memory (no file changes)."""
import sys, json
sys.path.insert(0, "/home/user/auth_gap")
from authgap.runner import RunConfig, run
from authgap.val import Options
from authgap.report import manifest_json, probe_json
case, md = sys.argv[1], int(sys.argv[2])
res = run(RunConfig(src_root=case, population="mcp_server", options=Options(max_depth=md), full=True))
m = manifest_json(res, "x")
for u in m["units"]:
    print(u["unit"]["tool_name"], "opaque", u["opaque_reasons"], "cap", u["cap_hits"],
          [(e.get("site") or e.get("callee"), e["kind"], e.get("lineno"), e["resolution"]) for e in u["effects"]],
          [r["verdicts"] for r in u["rows"]])
p = probe_json(res, "x")
print({k: p[k] for k in p if "ratio" in k or "resolution" in k})
