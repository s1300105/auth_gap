#!/usr/bin/env python3
"""母集団 v2 の manifest から「矛盾（D と M のギャップ）」と、その内側の
「ツール引数（モデル）の値が危険な処理の制御位置に届く」ものを数える（探索。決定ではない）。

段:
  G0  矛: 効果の行に CONTRADICTION が付く
  G1  G0 かつ 同じ効果のどれかの制御位置の行に GAP_INJECT
  G2  G1 のうち、その制御位置が主 slot（catalog/sinks.py PRIMARY_SLOTS）
  G3  G2 のうち、その slot の値が prin=MODEL かつ prov=resolved（D57 の「選べる」）

数える単位: 効果の位置 (tree, unit_id, relpath, lineno, site, kind)。併せて
contradictions.json と同じ「ユニット × (site, kind)」と、ユニット・木の数を出す。

使い方: python -I gap_inject_count.py <scan_dir> [<out.json>]
"""
import collections
import glob
import json
import os
import sys

PRIMARY = {"code_text", "argv0", "argv[*]", "shell_string", "path", "url.host", "sql"}


def decls(notes):
    return sorted({n.split(":")[1] for n in notes if n.startswith("contradiction:")})


def main():
    scan_dir = sys.argv[1]
    files = sorted(f for f in glob.glob(os.path.join(scan_dir, "v2-*.json")))
    eff_level = {}  # key -> dict
    for f in files:
        tree = os.path.basename(f)[:-5]
        m = json.load(open(f))
        for u in m.get("units", []):
            uid = u["unit"]["unit_id"] if isinstance(u.get("unit"), dict) else u.get("unit")
            slotval = {}
            for e in u.get("effects", []):
                k = (e["relpath"], e["lineno"], e["site"], e["kind"])
                for s, v in (e.get("slots") or {}).items():
                    slotval.setdefault(k, {}).setdefault(s, []).append(v)
            for r in u.get("rows", []):
                k = (r["relpath"], r["lineno"], r["site"], r["kind"])
                key = (tree, uid) + k
                d = eff_level.setdefault(key, {"contra": False, "decls": set(), "inject_slots": set(),
                                               "kind": r["kind"]})
                if "CONTRADICTION" in r["verdicts"]:
                    d["contra"] = True
                    d["decls"] |= set(decls(r.get("notes", [])))
                if "GAP_INJECT" in r["verdicts"]:
                    d["inject_slots"].add(r["slot"])
                d.setdefault("slotval", slotval.get(k, {}))

    def stage(d):
        if not d["contra"]:
            return None
        st = "G0"
        if d["inject_slots"]:
            st = "G1"
            prim = d["inject_slots"] & PRIMARY
            if prim:
                st = "G2"
                for s in prim:
                    for v in d["slotval"].get(s, []):
                        if v.get("prin") == "MODEL" and v.get("prov") == "resolved":
                            st = "G3"
        return st

    order = ["G0", "G1", "G2", "G3"]
    res = {"n_manifests": len(files)}
    sets = {g: [] for g in order}
    for key, d in eff_level.items():
        st = stage(d)
        if st is None:
            continue
        for g in order[: order.index(st) + 1]:
            sets[g].append((key, d))
    for g in order:
        items = sets[g]
        res[g] = {
            "effect_sites": len(items),
            "unit_site_kind": len({(k[0], k[1], k[4], k[5]) for k, _ in items}),
            "units": len({(k[0], k[1]) for k, _ in items}),
            "trees": len({k[0] for k, _ in items}),
            "by_kind": dict(collections.Counter(d["kind"] for _, d in items)),
            "by_decl": dict(collections.Counter(x for _, d in items for x in d["decls"])),
        }
    res["G3_examples"] = [
        {"tree": k[0], "unit": k[1], "relpath": k[2], "lineno": k[3], "site": k[4], "kind": k[5],
         "decls": sorted(d["decls"]), "inject_slots": sorted(d["inject_slots"])}
        for k, d in sorted(sets["G3"])
    ]
    out = json.dumps(res, ensure_ascii=False, indent=1, default=list)
    if len(sys.argv) > 2:
        open(sys.argv[2], "w").write(out)
    print(json.dumps({g: {kk: vv for kk, vv in res[g].items()} for g in order}, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
