#!/usr/bin/env python3
"""事前定義（カタログと語彙）の地図を作る。**解析器は触らない。**

この script が答える問いは 3 つ:

1. **どの表が核で、どれが降ろした主張（D36）のものか。** 核 = 「宣言 D と実効 M の照合」に
   要るもの。付録 = 等級づけ / ゲート / SELECT のためのもの。索引 = 他の表から機械的に作る派生。
2. **どの表が既知の知識の転記で、どれをこの研究で決めたか。** 転記 = Python と主要ライブラリの
   常識で、既存の静的解析器も同等の表を持つもの。領域固有 = MCP / エージェント枠組みに固有で、
   既存にないもの。engine = 解析器が自分の限界を申告する語彙（世界の定義ではない）。
3. **核の主張が実際に使っている行はどれだけか。** full scan の証拠から、CONTRADICTION を
   出した効果の site を数える。

**役割と出所の分類は判断であって測定ではない。** 根拠は `docs/decisions.md` D37 に書いた。
分類を変えるときは D37 も直すこと。行数と使用実績は測定値で、再実行すれば再現する。

    .venv/bin/python scripts/catalog_map.py evidence/scan_v2_run4 --md docs/catalog_map.md
"""

from __future__ import annotations

import argparse
import collections
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

#: 表 → (役割, 出所, 一言)。役割: core / appendix / index。出所: 転記 / 領域固有 / engine / meta。
#: **ここに無い表が見つかったら「未分類」として出す**（黙って落とさない）。
CLASSIFY: dict[str, tuple[str, str, str]] = {
    # -- 危険な呼び出し（何がどの能力か） -------------------------------------
    "DIRECT_SINKS": ("core", "転記", "subprocess.run / open / rmtree / httpx.get。ただし destructive 印は領域固有"),
    "PROXY_SINKS": ("core", "転記", "receiver 型経由の sink（git.Git.checkout など）"),
    "PIPE_SINKS": ("core", "領域固有", "stdin.write 形。仕様が「構造的理由のみ、CVE の裏付け無し」と明記"),
    "INTERPRETER_ARGV0": ("core", "転記", "argv0 がインタプリタかの判定"),
    "PIPE_HANDLE_SOURCES": ("core", "転記", "pipe ハンドルを生む spawn"),
    "DB_RECEIVER_TYPES": ("core", "転記", "非 DB の .execute() を数えないための受け手型"),
    # -- 能力の語彙（MCP の宣言に合わせた分類） --------------------------------
    "SLOTS": ("core", "領域固有", "効果 kind 7 種と slot。宣言の語彙に合わせて決めた"),
    "FORMS": ("core", "領域固有", "direct / proxy / pipe"),
    "SUB_KINDS": ("core", "領域固有", "kind 粒度の副分類"),
    "DANGEROUS_KINDS": ("core", "領域固有", "危険とみなす kind"),
    "PRIMARY_SLOTS": ("core", "領域固有", "主 slot 7 種（指標の分母）"),
    # -- 値を見失わないための補助 ---------------------------------------------
    "TRANSFERS": ("core", "転記", "realpath / Path.resolve / shlex.quote / urlparse"),
    "INDIRECTS": ("core", "転記", "multiprocessing.Process / Thread / partial / submit"),
    "CTORS": ("core", "転記", "sqlite3.connect / httpx.Client / git.Repo"),
    "CALL_TYPE_TRANSITIONS": ("core", "転記", "受け手型 × メソッド → 戻り値の型（conn.cursor() → Cursor など）。D50"),
    "ANNOTATION_TYPED_RECEIVERS": ("core", "転記", "型注釈から受け手型を付けてよい型（DB の型だけ）。D50"),
    "ATTR_TYPE_TRANSITIONS": ("core", "転記", "repo.git → git.cmd.Git のような型の伝播"),
    # -- 入口（この研究の領域固有の中心） --------------------------------------
    "ENTRY_RULES": ("core", "領域固有", "**既存の静的解析はどれも知らない。この研究の貢献の中心**"),
    "R2_EXCEPTIONS": ("core", "領域固有", "MODEL としない仮引数の例外"),
    "LOWLEVEL_V2_KWARGS": ("core", "領域固有", "低レベル MCP v2 の kwargs"),
    "TOOLMESSAGE_META_FIELDS": ("core", "領域固有", "langroid ToolMessage のメタ欄"),
    # -- 解析器の自己申告 -------------------------------------------------------
    "VAL_OPAQUE_REASONS": ("core", "engine", "値を解決できなかった理由 8 語"),
    "VALUE_ATTRS": ("core", "engine", "値に付く属性 8 語"),
    "VOCABULARY_REVISIONS": ("core", "meta", "語彙を動かした記録"),
    # -- 降ろした主張（D36）: 等級づけ / ゲート / SELECT -------------------------
    "VALIDATOR_SHAPES": ("appendix", "領域固有", "**自作**。Def 5 の検証子の形"),
    "WEAK_REASONS": ("appendix", "領域固有", "**自作**。弱い検証の理由 22 語。設計に最も時間がかかった"),
    "WITNESS_TEMPLATES": ("appendix", "領域固有", "weak 理由ごとの witness 文言"),
    "GRADES": ("appendix", "領域固有", "値検証の等級"),
    "DOWNGRADES": ("appendix", "領域固有", "格下げ属性"),
    "CONTAINMENT_PREDICATES": ("appendix", "転記", "包含述語（commonpath / relative_to …）"),
    "NOT_STRONG_DOMAINS": ("appendix", "領域固有", "strong にしない slot 領域"),
    "ALLOWED_OPERANDS": ("appendix", "領域固有", "Def 5 (iii) の被演算子"),
    "ROOT_EQUAL_STEPS": ("appendix", "領域固有", "root-equal と認める変換"),
    "DASH_REJECT_FORMS": ("appendix", "領域固有", "`--` 拒否の形"),
    "WITNESS_VIEWS": ("appendix", "領域固有", "witness の見せ方"),
    "ARGV_MODE_SUPPRESSED_WITNESS": ("appendix", "領域固有", ""),
    "DOWNGRADE_WITNESS": ("appendix", "領域固有", ""),
    "SYMLINK_RESOLVERS": ("appendix", "転記", "Def 5 (i) の正規化子"),
    "LEXICAL_CANONS": ("appendix", "転記", "字句正規化子"),
    "PATH_DOMAIN_SLOTS": ("appendix", "領域固有", "strong-path が効く slot（D25）"),
    "CONFIG_ATOM_SOURCES": ("appendix", "領域固有", "config atom の源"),
    "DEFAULT_OPEN_VALUES": ("appendix", "領域固有", "既定が開いている値"),
    "CONFIG_ATOM_OPAQUE_FORMS": ("appendix", "領域固有", ""),
    "ENUM_BINDING_FORMS": ("appendix", "領域固有", ""),
    "MODE_GATE_ATOMS": ("appendix", "領域固有", "モードのゲート"),
    "APPROVAL_INTERRUPTS": ("appendix", "領域固有", "承認割り込みの認識"),
    "LEAK_REASONS": ("appendix", "領域固有", "Def 5-b の Leak"),
    "EXPOSURE_GATE_FORMS": ("appendix", "領域固有", "露出ゲートの形"),
    "POLICY_FILE_PATTERNS": ("appendix", "領域固有", "D_op の方針ファイル"),
    "LLM_CALLS": ("appendix", "転記", "SELECT 座標（trig）。traced 0.6% で §3 の格下げ条項が発火（D36）"),
    "LLM_PROJECTIONS": ("appendix", "転記", "同上"),
    "GATE_OPAQUE_REASONS": ("appendix", "engine", "ゲート側の OPAQUE 8 語"),
    "GATE_NODOM_REASONS": ("appendix", "engine", "ゲート側の NODOM 4 語"),
    "_DOM_PRIORITY": ("appendix", "engine", "3 値支配の優先順"),
    # -- 索引（他の表から機械的に作る派生。定義ではない） ------------------------
    "KINDS": ("index", "-", "SLOTS の鍵"),
    "TRANSFER_BY_NAME": ("index", "-", "TRANSFERS の索引"),
    "METHOD_TRANSFERS": ("index", "-", "TRANSFERS の受け手主語だけ"),
    "INDIRECT_BY_NAME": ("index", "-", "INDIRECTS の索引"),
    "CTOR_BY_NAME": ("index", "-", "CTORS の索引"),
    "WEAK_REASON_SET": ("index", "-", "WEAK_REASONS の集合"),
    "SHAPE_NAMES": ("index", "-", "VALIDATOR_SHAPES の名前"),
    "APPROVAL_NAMES": ("index", "-", "APPROVAL_INTERRUPTS の名前"),
}

ROLE_ORDER = ("core", "appendix", "index", "未分類")
ROLE_LABEL = {
    "core": "核（宣言 D と実効 M の照合に要る）",
    "appendix": "付録（D36 で降ろした主張のもの）",
    "index": "索引（派生。定義ではない）",
    "未分類": "**未分類（分類表に無い。D37 を更新すること）**",
}
ORIGIN_LABEL = {
    "転記": "既知の知識の転記",
    "領域固有": "この研究で決めた",
    "engine": "解析器の自己申告",
    "meta": "記録",
    "-": "-",
}


def collect_tables() -> list[dict]:
    import authgap.catalog.entries as E
    import authgap.catalog.sinks as S
    import authgap.catalog.transfers as T
    import authgap.catalog.validators as V
    import authgap.ir as IR

    out: list[dict] = []
    for mod_name, mod in (("sinks", S), ("transfers", T), ("validators", V), ("entries", E), ("ir", IR)):
        for name in dir(mod):
            if not name.isupper() and name != "_DOM_PRIORITY":
                continue
            val = getattr(mod, name)
            if not isinstance(val, (tuple, list, frozenset, set, dict)) or not len(val):
                continue
            role, origin, note = CLASSIFY.get(name, ("未分類", "-", ""))
            out.append({"module": mod_name, "name": name, "rows": len(val),
                        "role": role, "origin": origin, "note": note})
    return out


def exercised_sinks(evidence_dir: str) -> dict:
    """full scan の証拠から、CONTRADICTION を出した効果の site と形を数える。"""
    sites: collections.Counter = collections.Counter()
    forms: collections.Counter = collections.Counter()
    depth: collections.Counter = collections.Counter()
    for fn in sorted(os.listdir(evidence_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        with open(os.path.join(evidence_dir, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        for u in man.get("units", []):
            keys = {(r["site"], r["kind"]) for r in u.get("rows", []) if "CONTRADICTION" in r.get("verdicts", [])}
            if not keys:
                continue
            for e in u.get("effects", []):
                if (e["site"], e["kind"]) in keys:
                    sites[e["site"]] += 1
                    forms[e["form"]] += 1
                    depth[len(e.get("witness_chain", []))] += 1
    return {"sites": dict(sites.most_common()), "forms": dict(forms), "depth": dict(sorted(depth.items()))}


def declaration_split(evidence_dir: str, min_units: int = 3) -> dict:
    """同じ API を呼ぶツールの宣言が割れている site（D37 の「裁定が要る行」の見積り）。"""
    per_site: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    for fn in sorted(os.listdir(evidence_dir)):
        if not fn.endswith(".json") or fn in ("summary.json", "contradictions.json"):
            continue
        with open(os.path.join(evidence_dir, fn), encoding="utf-8") as fh:
            man = json.load(fh)
        for u in man.get("units", []):
            ex = tuple(sorted((u.get("D_kind") or {}).get("explicit", [])))
            label = "+".join(ex) if ex else "(宣言なし)"
            for site in {e["site"] for e in u.get("effects", [])}:
                per_site[site][label] += 1
    split = {}
    for site, c in per_site.items():
        if sum(c.values()) < min_units:
            continue
        ro = sum(v for k, v in c.items() if "readOnlyHint" in k)
        de = sum(v for k, v in c.items() if "destructiveHint" in k)
        if ro and de:
            split[site] = dict(c.most_common())
    return {"n_sites_total": len(per_site), "n_sites_split": len(split), "min_units": min_units, "split": split}


def to_md(tables: list[dict], ex: dict, sp: dict, evidence_dir: str) -> str:
    o: list[str] = []
    o.append("# 事前定義の地図（何を先に決めているか、なぜ、どれが自分で考えた部分か）")
    o.append("")
    o.append(f"再現: `python scripts/catalog_map.py {evidence_dir} --md docs/catalog_map.md`")
    o.append("")
    o.append("**役割と出所の分類は判断であって測定ではない**（根拠は `docs/decisions.md` D37）。")
    o.append("行数と、下の「実際に使われた行」は測定値。")
    o.append("")

    by_role: dict[str, list[dict]] = collections.defaultdict(list)
    for t in tables:
        by_role[t["role"]].append(t)
    o.append("## まとめ")
    o.append("")
    o.append("| 役割 | 表の数 | 行の合計 |")
    o.append("|---|---|---|")
    for r in ROLE_ORDER:
        if r not in by_role:
            continue
        o.append(f"| {ROLE_LABEL[r]} | {len(by_role[r])} | {sum(t['rows'] for t in by_role[r])} |")
    o.append("")
    core = by_role.get("core", [])
    by_origin: dict[str, int] = collections.Counter()
    for t in core:
        by_origin[t["origin"]] += t["rows"]
    o.append("核の内訳（出所別の行数）:")
    o.append("")
    o.append("| 出所 | 行 |")
    o.append("|---|---|")
    for k, v in sorted(by_origin.items(), key=lambda kv: -kv[1]):
        o.append(f"| {ORIGIN_LABEL.get(k, k)} | {v} |")
    o.append("")
    o.append("**自分で一から考える必要があったのは「この研究で決めた」の行だけで、その中心は")
    o.append("`ENTRY_RULES`（ツールの入口 14 形）である。** 既存の静的解析はどの枠組みの入口も")
    o.append("知らないので代替が無い。危険な呼び出しと値の変換は Python と主要ライブラリの常識で、")
    o.append("既存ツールも同等の表を持つ（量はあるが難しさは無い）。")
    o.append("")

    o.append("## 核の主張が実際に使っている行")
    o.append("")
    o.append(f"`{evidence_dir}` の CONTRADICTION から逆に数えた。")
    o.append("")
    o.append(f"- 関係した API: **{len(ex['sites'])} 種類**（`DIRECT_SINKS` 67 行のうち）")
    o.append(f"- 効果の形: {ex['forms']}")
    o.append("- 呼び出しを何段降りたか: " + ", ".join(f"{k} 段 {v}" for k, v in ex["depth"].items()))
    o.append("")
    o.append("```")
    o.append("  " + "  ".join(sorted(ex["sites"])))
    o.append("```")
    o.append("")

    o.append("## 母集団の宣言が割れている API")
    o.append("")
    o.append("同じ API を呼ぶツールで、readOnly と destructive の明示が両方現れるもの。")
    o.append(f"{sp['min_units']} ユニット以上から呼ばれる site が対象。")
    o.append("")
    o.append(f"- 効果 site の総数: {sp['n_sites_total']}")
    o.append(f"- 宣言が割れている site: **{sp['n_sites_split']}**")
    o.append("")
    o.append("| API | 宣言の分かれ方 |")
    o.append("|---|---|")
    for site, c in sorted(sp["split"].items(), key=lambda kv: -sum(kv[1].values())):
        o.append(f"| `{site}` | {c} |")
    o.append("")
    o.append("**多数決を真理として使ってはならない。** `subprocess.run` は readOnly の宣言が")
    o.append("多数派になるが、プロセス起動が読み取り専用であるはずがない。多数派が誤っている。")
    o.append("この表は「少なくとも一方が誤っている」を言うためのもので、正解を決める材料ではない。")
    o.append("")

    o.append("## 表の一覧")
    o.append("")
    for r in ROLE_ORDER:
        if r not in by_role:
            continue
        o.append(f"### {ROLE_LABEL[r]}")
        o.append("")
        o.append("| 表 | 場所 | 行 | 出所 | 備考 |")
        o.append("|---|---|---|---|---|")
        for t in sorted(by_role[r], key=lambda x: (-x["rows"], x["name"])):
            o.append(f"| `{t['name']}` | {t['module']} | {t['rows']} | "
                     f"{ORIGIN_LABEL.get(t['origin'], t['origin'])} | {t['note']} |")
        o.append("")
    return "\n".join(o)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("evidence_dir", help="evidence/scan_v2_<label>（木ごとの manifest がある所）")
    ap.add_argument("--md", help="Markdown をこのパスに書く")
    args = ap.parse_args(argv)

    d = args.evidence_dir if os.path.isabs(args.evidence_dir) else os.path.join(ROOT, args.evidence_dir)
    if not os.path.isdir(d):
        raise SystemExit(f"{d} が無い")

    tables = collect_tables()
    unknown = [t["name"] for t in tables if t["role"] == "未分類"]
    md = to_md(tables, exercised_sinks(d), declaration_split(d), os.path.relpath(d, ROOT))
    print(md)
    if args.md:
        p = args.md if os.path.isabs(args.md) else os.path.join(ROOT, args.md)
        with open(p, "w", encoding="utf-8") as fh:
            fh.write(md + "\n")
        print(f"\nwrote {args.md}", file=sys.stderr)
    if unknown:
        print(f"\n**未分類の表がある: {unknown}**（D37 と CLASSIFY を更新すること）", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
