#!/usr/bin/env python3
"""O23 の「決めが要るマス」に、母集団のどの効果が落ちているかを数える（判断材料）。

**判定の規則はここに無い**（`authgap/dparse.py: contradiction()`）。この script は
「マスをどちらに決めたら何件が CONTRADICTION に入る / 出るか」を出すだけで、決めない。

    .venv/bin/python scripts/o23_cells.py evidence/scan_v2_run11 --md docs/o23_cells.md

数え方（分母を明示する。CLAUDE.md 規則 3）:

* 単位は **効果の位置** = (木, ユニットの qualname, site, kind, relpath, lineno)。同じ位置に
  別経路で届く効果は 1 件に数える。「プロジェクト」は木の数。
* 宣言は 2 つの読み方を使い分ける:
  - `readOnlyHint: true` / `destructiveHint: false` は `D_kind.explicit`（`contradiction()` と同じ）。
    D2 は `readOnlyHint: true` が無いユニットだけ（仕様: D1 が優先）。
  - `openWorldHint: false` / `idempotentHint: true` は `unit.annotations` の生の値
    （`D_kind` は上界を動かさないので、ここからしか読めない）。
* SQL の先頭語・HTTP メソッド・argv0・ホストは、slot の値が**定数に解決できたときだけ**読む。
  読めないものは「読めない」として別に数える（黙って片側に倒さない）。
"""

from __future__ import annotations

import argparse
import collections
import ipaddress
import json
import os
import re
from urllib.parse import urlparse

NET_WRITE = {"post", "put", "patch", "delete"}
NET_READ = {"get", "head", "options"}
SQL_DATA_WRITE = {"INSERT", "UPDATE", "DELETE", "REPLACE", "UPSERT", "MERGE", "TRUNCATE",
                  "DROP", "CREATE", "ALTER"}
SQL_SESSION = {"PRAGMA", "BEGIN", "COMMIT", "ROLLBACK", "SET", "SAVEPOINT", "RELEASE", "VACUUM",
               "ANALYZE", "ATTACH", "DETACH", "LISTEN", "NOTIFY"}


def _const(slot: dict | None):
    if not isinstance(slot, dict):
        return None
    sh = slot.get("shape") or {}
    if "const" in sh:
        return sh["const"]
    base = sh.get("base")
    if isinstance(base, dict):
        return _const(base)
    return None


def _argv0(e: dict):
    s = (e.get("slots") or {}).get("argv0")
    c = _const(s)
    if isinstance(c, str):
        return os.path.basename(c)
    sh = (s or {}).get("shape") or {}
    items = sh.get("items")
    if items:
        c = _const(items[0])
        if isinstance(c, str):
            return os.path.basename(c)
    return None


def _sql_head(e: dict):
    c = _const((e.get("slots") or {}).get("sql"))
    if not isinstance(c, str) or not c.strip():
        return None
    return c.split(None, 1)[0].upper().rstrip(";")


def _net_method(e: dict):
    m = e["site"].rsplit(".", 1)[-1].lower()
    if m in NET_WRITE | NET_READ:
        return m
    c = _const((e.get("slots") or {}).get("method"))
    if isinstance(c, str):
        return c.lower()
    return None


def _host_class(e: dict):
    slots = e.get("slots") or {}
    for k in ("url.host", "url"):
        c = _const(slots.get(k))
        if isinstance(c, str) and c:
            host = urlparse(c).hostname if "://" in c else c.split("/")[0].split(":")[0]
            if not host:
                return "読めない"
            if host in ("localhost",) or host.endswith(".local"):
                return "localhost"
            try:
                ip = ipaddress.ip_address(host)
                return "private / loopback" if (ip.is_private or ip.is_loopback) else "外部"
            except ValueError:
                return "外部"
    return "読めない"


def load(run_dir: str):
    for fn in sorted(os.listdir(run_dir)):
        if not fn.startswith("v2-") or not fn.endswith(".json"):
            continue
        t = fn[:-5]
        for u in json.load(open(os.path.join(run_dir, fn), encoding="utf-8"))["units"]:
            yield t, u


def collect(run_dir: str) -> dict:
    cells: dict[str, dict[str, dict]] = collections.defaultdict(lambda: collections.defaultdict(dict))

    def put(cell: str, bucket: str, t: str, u: dict, e: dict, detail: str = "") -> None:
        key = (t, u["unit"]["qualname"], e["site"], e["kind"], e["relpath"], e["lineno"])
        cells[cell][bucket].setdefault(key, detail)

    for t, u in load(run_dir):
        explicit = set((u.get("D_kind") or {}).get("explicit") or [])
        ann = u["unit"].get("annotations") or {}
        ro = "readOnlyHint" in explicit
        nd = "destructiveHint" in explicit and not ro
        for e in u.get("effects", []):
            k, sk = e["kind"], e.get("sub_kind")
            decl = "D1 readOnly" if ro else ("D2 destructive=false" if nd else None)
            # #1 readOnly / destructive=false × DB（先頭語で分ける）
            if decl and k == "DB":
                head = _sql_head(e)
                if sk == "DB_READ":
                    b = "DB_READ（宣言内）"
                elif head is None:
                    b = "SQL が読めない"
                elif head in SQL_SESSION:
                    b = f"接続・トランザクション（{head}）"
                elif head in SQL_DATA_WRITE:
                    b = f"データの変更（{head}）"
                else:
                    b = f"その他（{head}）"
                put("1", f"{decl} × {b}", t, u, e, head or "")
            # #2 readOnly / destructive=false × NET の書き込み系メソッド
            if decl and k == "NET":
                m = _net_method(e)
                b = ("書き込み系 " + m.upper()) if m in NET_WRITE else ("読み系" if m in NET_READ else "メソッドが読めない")
                put("2", f"{decl} × {b}", t, u, e, m or "")
            # #3 destructive=false × FS_WRITE（mode 不明）
            if nd and k == "FS_WRITE" and e.get("destructive") is None:
                put("3", "mode 不明", t, u, e)
            # #4 openWorldHint: false × NET の宛先
            if ann.get("openWorldHint") is False and k == "NET":
                put("4", _host_class(e), t, u, e)
            # #5 idempotentHint: true × 非冪等の証拠
            if ann.get("idempotentHint") is True:
                if k == "NET" and _net_method(e) == "post":
                    put("5", "NET POST", t, u, e)
                elif k == "DB" and _sql_head(e) == "INSERT":
                    c = _const((e.get("slots") or {}).get("sql")) or ""
                    b = "INSERT（ON CONFLICT / OR REPLACE あり）" if re.search(r"ON\s+CONFLICT|OR\s+REPLACE|OR\s+IGNORE", c, re.I) else "INSERT（衝突時の指定なし）"
                    put("5", b, t, u, e)
                elif k == "FS_WRITE" and e.get("destructive") is False and e["site"] in ("builtins.open", "io.open"):
                    put("5", "open（追記）", t, u, e)
            # #6 readOnly / destructive=false × SPAWN（argv0 で分ける）
            if decl and k == "SPAWN":
                a0 = _argv0(e)
                put("6", f"{decl} × {sk}", t, u, e, a0 or "（argv0 が読めない）")
            # #7 destructive=false × FS_WRITE（上書き型の site）
            if nd and k == "FS_WRITE" and e.get("destructive") is True:
                put("7", e["site"], t, u, e)
    return cells


def to_md(run_dir: str, cells: dict) -> str:
    o = ["# O23 の決めが要るマス — 母集団での件数（判断材料）", "",
         f"再現: `python scripts/o23_cells.py {os.path.relpath(run_dir)}`", "",
         "単位は**効果の位置**（木, ユニット, site, kind, relpath, lineno）。「木」はプロジェクト数。", ""]
    titles = {
        "1": "#1 `readOnlyHint: true` / `destructiveHint: false` × DB（SQL の先頭語）",
        "2": "#2 `readOnlyHint: true` / `destructiveHint: false` × NET（HTTP メソッド）",
        "3": "#3 `destructiveHint: false` × FS_WRITE（mode 不明）",
        "4": "#4 `openWorldHint: false` × NET（宛先）",
        "5": "#5 `idempotentHint: true` × 非冪等の証拠",
        "6": "#6 `readOnlyHint: true` / `destructiveHint: false` × SPAWN（**現行は全件 CONTRADICTION**）",
        "7": "#7 `destructiveHint: false` × FS_WRITE の上書き型（**現行は全件 CONTRADICTION**）",
    }
    for c in "1234567":
        o += [f"## {titles[c]}", "", "| 区分 | 位置 | 木 | 例（木 / ユニット / site / 位置 / 詳細） |", "|---|---|---|---|"]
        buckets = cells.get(c, {})
        if not buckets:
            o += ["| 該当なし | 0 | 0 | — |", ""]
            continue
        for b in sorted(buckets, key=lambda b: -len(buckets[b])):
            items = buckets[b]
            trees = {k[0] for k in items}
            ex = sorted(items)[:3]
            exs = "<br>".join(f"`{k[0][3:]}` / `{k[1][:50]}` / `{k[2]}` / {k[4]}:{k[5]}" + (f" / `{items[k][:40]}`" if items[k] else "") for k in ex)
            o.append(f"| {b} | {len(items)} | {len(trees)} | {exs} |")
        if c == "6":
            cnt = collections.Counter(v for b in buckets.values() for v in b.values())
            o += ["", "argv0（定数に解決できたもの）: " + ", ".join(f"`{a}` {n}" for a, n in cnt.most_common(30))]
        o.append("")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run")
    ap.add_argument("--md")
    args = ap.parse_args(argv)
    md = to_md(args.run, collect(args.run))
    if args.md:
        with open(args.md, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
    print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
