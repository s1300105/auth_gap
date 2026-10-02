"""宣言（ToolAnnotations）の使われ方の資料集（教科書 付録 G）の資料カードを、調査のデータから組み立てる。

入力（evidence/annotations_usage/）:
- sources.json   — 調べた資料（entries）、記載が無かったページ（checked_no_mention）、届かなかったページ（unreachable）
- recheck.json   — scripts/verify_quote.py --batch で、[確認] の全件を新しいキャッシュで照らし合わせ直した結果

出力（docs/textbook/）:
- appendix-g-1.md 〜 appendix-g-13.md — 資料カード（分野ごと）と、記載が無かった / 届かなかったページの一覧
- appendix-g.md の <!-- BEGIN GENERATED --> 〜 <!-- END GENERATED --> の間 — 分野ごとの件数と、使い方の分類の集計

引用（原文）は調査のデータから機械的に写す。手で書き写さないので、写し間違いが入らない。
再照合で一致しなかった [確認] は、カードの上で [未確認] に落とし、理由を書く（黙って [確認] のままにしない）。

使い方:
    python scripts/build_annotations_appendix.py
"""
from __future__ import annotations

import collections
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EV = os.path.join(ROOT, "evidence", "annotations_usage")
TB = os.path.join(ROOT, "docs", "textbook")

# 付録の分冊と、調査の分野の対応
PARTS = [
    ("1", "MCP の公式（仕様・スキーマ・公式サイト・ブログ・SEP・参照サーバ・Inspector）", ["C01_mcp_official"]),
    ("2", "SDK（サーバを作る道具と、クライアント側のライブラリ）", ["C02_sdks"]),
    ("3", "Microsoft と GitHub", ["C03_microsoft_github"]),
    ("4", "Anthropic（Claude）", ["C04_anthropic"]),
    ("5", "OpenAI（ChatGPT・Codex・Apps SDK・Agents SDK）", ["C05_openai"]),
    ("6", "Google と AWS", ["C06_google_aws"]),
    ("7", "エディタとコーディングエージェント", ["C07_ide_agents", "G2_closed_clients_missing", "G3_asia_agents"]),
    ("8", "エージェントの枠組み・利用者向けアプリ・モデルの API", ["C08_frameworks", "G3_consumer_apps_model_apis"]),
    ("9", "サーバの作者と、業務 SaaS のホスト", ["G3_vendor_servers", "G3_saas_hosts"]),
    ("10", "ゲートウェイ・実行基盤・宣言を検査する道具・登録所", ["C09_servers_gateways_security", "G2_gateways_platforms",
                                                     "G2_verifiers_linters", "G2_registries_marketplaces"]),
    ("11", "WebMCP（ブラウザがページのツールを AI に渡す仕組み）", ["G2_webmcp"]),
    ("12", "研究論文・標準・安全の指針", ["C10_research_standards", "G3_standards_protocols"]),
]

USAGE_JA = {
    "auto_approve": "確認を省く（自動で許可）",
    "require_confirmation": "確認を求める",
    "filter_or_hide_tools": "ツールを絞る・隠す",
    "display_label": "表示（印・名前）",
    "policy_rule_input": "規則（ポリシー）の条件に使う",
    "risk_scoring": "危険度を付ける",
    "required_to_declare": "宣言を書くことを求める",
    "author_guidance_how_to_set": "作者への書き方の案内",
    "warn_untrusted": "信頼するなという注意",
    "defaults_when_missing": "宣言が無いときの扱い",
    "passthrough_or_expose": "そのまま渡す・見せる",
    "ignored_or_not_used": "使わない・読まない",
    "verification_or_lint": "宣言を検査する",
    "other": "その他",
}
DOCTYPE_JA = {
    "spec": "仕様", "official_blog": "公式ブログ", "official_docs": "公式の文書", "sdk_docs": "SDK の文書",
    "sdk_code": "SDK のソースコード", "client_docs": "クライアントの文書", "client_code": "クライアントのソースコード",
    "release_notes": "リリースノート", "server_docs": "サーバの文書", "server_code": "サーバのソースコード",
    "policy_guideline": "規約・審査の指針", "gateway_docs": "ゲートウェイの文書", "gateway_code": "ゲートウェイのソースコード",
    "scanner_docs": "検査の道具の文書", "scanner_code": "検査の道具のソースコード", "paper": "論文",
    "standard_guidance": "標準・指針", "issue_or_pr": "issue / PR / 提案の下書き", "third_party": "第三者の記事",
}
HINT_JA = {"readOnlyHint": "readOnlyHint", "destructiveHint": "destructiveHint", "idempotentHint": "idempotentHint",
           "openWorldHint": "openWorldHint", "title": "title", "annotations_general": "宣言全般"}


def anchor(eid: str) -> str:
    return "g-" + re.sub(r"[^a-z0-9]+", "-", eid.lower()).strip("-")


def label(eid: str) -> str:
    m = re.match(r"(C\d\d|G\d)_?([A-Za-z_]*?)-(\d+)$", eid)
    if not m:
        return eid
    head, name, num = m.groups()
    if head.startswith("G"):
        short = "".join(w[0] for w in name.split("_") if w).upper()
        return f"{head}{short}-{num}"
    return f"{head}-{num}"


def md_escape_cell(s: str) -> str:
    return (s or "").replace("|", "\\|").replace("\n", " ")


def quote_block(q: str) -> str:
    lines = (q or "").rstrip().split("\n")
    code_like = any(re.match(r"\s{2,}\S", ln) for ln in lines) or any(c in q for c in "{};=") and len(lines) > 1
    if code_like:
        fence = "````" if "```" in q else "```"
        return f"{fence}\n{q.rstrip()}\n{fence}"
    return "\n".join("> " + ln if ln.strip() else ">" for ln in lines)


def recheck_line(r: dict | None) -> str:
    if not r:
        return "再照合の記録なし"
    m = r.get("match")
    if m in ("exact", "loose", "script_only"):
        where = ""
        h = (r.get("hits") or [{}])[0]
        if h.get("heading_path"):
            where = f"、見出し「{h['heading_path']}」"
        elif h.get("lines"):
            where = f"、{h['lines']} 行" + (f"（{h['md_heading']}）" if h.get("md_heading") else "")
        elif h.get("page"):
            where = f"、{h['page']} ページ"
        cnt = r.get("count")
        return f"{m}・{cnt} か所{where}（取得 {r.get('fetched_at', '')}、sha256 {str(r.get('sha256', ''))[:12]}…）"
    return f"{m}（{r.get('error') or r.get('status') or ''}）"


def card(e: dict, r: dict | None) -> str:
    lab = label(e["id"])
    title = f"{e.get('org', '')} — {e.get('product', '')}".strip(" —")
    ok_marks = ("exact", "loose", "script_only")
    verified = e.get("verified")
    down = ""
    local = re.match(r"https?://(127\.0\.0\.1|localhost)[:/]", e.get("fetched_url", ""))
    if verified == "確認" and (r is None or r.get("match") not in ok_marks):
        if local:
            verified = "調査時のみ"
        else:
            verified = "未確認"
            down = "（調査のときは [確認] だったが、2026-10-02 の再照合で一致しなかったので [未確認] に落とした）"
    out = [f'<a id="{anchor(e["id"])}"></a>', f"#### {lab} {title}", ""]
    out.append(f"- **資料**: {e.get('doc_title', '')}（{DOCTYPE_JA.get(e.get('doc_type'), e.get('doc_type', ''))}）")
    out.append(f"- **URL**: {e.get('url', '')}")
    if e.get("anchored_url") and e.get("anchored_url") != e.get("url"):
        out.append(f"- **書いてある見出しへ直接**: {e['anchored_url']}")
    if local:
        out.append("- **照らし合わせた中身**: 配布物（インストーラ・パッケージ）を展開したファイルを、調査のときだけ手元の一時 URL "
                   f"（{e['fetched_url']}）で配って照らし合わせた。配布物の取り方は「補足」を見る。")
    elif e.get("fetched_url") and e.get("fetched_url") != e.get("url"):
        out.append(f"- **照らし合わせた中身の URL**: {e['fetched_url']}")
    out.append(f"- **版**: {e.get('version', '')}")
    out.append(f"- **書いてある場所**: {e.get('location', '')}")
    out.append("- **原文**:")
    out.append("")
    out.append(quote_block(e.get("quote", "")))
    out.append("")
    out.append(f"- **日本語**: {e.get('quote_ja', '')}")
    out.append(f"- **どう使っているか**: {e.get('usage_ja', '')}")
    if e.get("conditions"):
        out.append(f"- **条件**: {e['conditions']}")
    hints = "・".join(HINT_JA.get(h, h) for h in e.get("hints", []))
    uses = "・".join(USAGE_JA.get(u, u) for u in e.get("usage", []))
    out.append(f"- **扱う宣言**: {hints} ／ **使い方の分類**: {uses}")
    if verified == "確認":
        out.append(f"- **確かさ**: [確認] 再照合 {recheck_line(r)}")
    elif verified == "調査時のみ":
        out.append("- **確かさ**: [確認（調査時のみ）] 調査の担当と点検の担当が配布物の展開物で照らし合わせた。"
                   "展開物の一時 URL が無くなったので、2026-10-02 の再照合はしていない。")
    else:
        why = e.get("verify_result", "")
        out.append(f"- **確かさ**: [未確認]{down} {why}".rstrip())
    notes = " ".join(x for x in (e.get("notes"), e.get("verifier_note")) if x)
    if notes:
        out.append(f"- **補足**: {notes}")
    out.append("")
    return "\n".join(out)


def nav(prev: tuple[str, str] | None, nxt: tuple[str, str] | None) -> str:
    parts = []
    if prev:
        parts.append(f"[← {prev[1]}]({prev[0]})")
    parts.append("[付録 G の表紙](appendix-g.md)")
    parts.append("[目次](README.md)")
    if nxt:
        parts.append(f"[{nxt[1]} →]({nxt[0]})")
    return " ｜ ".join(parts)


def main():
    src = json.load(open(os.path.join(EV, "sources.json"), encoding="utf-8"))
    rc = {r["id"]: r for r in json.load(open(os.path.join(EV, "recheck.json"), encoding="utf-8"))}
    entries = src["entries"]
    by_cat = collections.defaultdict(list)
    for e in entries:
        by_cat[e["category"]].append(e)
    files = [(f"appendix-g-{n}.md", f"付録 G-{n} {t.split('（')[0]}") for n, t, _ in PARTS]
    files.append(("appendix-g-13.md", "付録 G-13 記載が無かったページと届かなかったページ"))
    stats = []
    for i, (n, title, cats) in enumerate(PARTS):
        es = [e for c in cats for e in by_cat.get(c, [])]
        prev = files[i - 1] if i > 0 else None
        nxt = files[i + 1]
        lines = [nav(prev, nxt), "", "---", "", f"# 付録 G-{n} {title}", "",
                 "<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->", ""]
        n_ok = n_only = 0
        prods = collections.OrderedDict()
        for e in es:
            prods.setdefault((e.get("org", ""), e.get("product", "")), []).append(e)
        lines.append(f'<a id="ag-{n}-0"></a>')
        lines.append("## この分冊の資料の一覧")
        lines.append("")
        lines.append("| カード | 組織 — 製品 | 資料の種類 | 使い方の分類 | 確かさ |")
        lines.append("|---|---|---|---|---|")
        cards = []
        for (org, prod), group in prods.items():
            cards.append(f"### {org} — {prod}".rstrip(" —"))
            cards.append("")
            for e in group:
                r = rc.get(e["id"])
                c = card(e, r)
                cards.append(c)
                tail = c.split("- **確かさ**: ")[1]
                ok = tail.startswith("[確認]")
                only = tail.startswith("[確認（調査時のみ）]")
                n_ok += ok
                n_only += only
                lines.append(f"| [{label(e['id'])}](#{anchor(e['id'])}) | {md_escape_cell(org)} — {md_escape_cell(prod)} | "
                             f"{DOCTYPE_JA.get(e.get('doc_type'), '')} | "
                             f"{md_escape_cell('・'.join(USAGE_JA.get(u, u) for u in e.get('usage', [])))} | "
                             f"{'[確認]' if ok else ('[確認（調査時のみ）]' if only else '[未確認]')} |")
        lines.append("")
        lines.append(f"この分冊の資料は {len(es)} 件で、うち [確認] は {n_ok} 件、[確認（調査時のみ）] は {n_only} 件。")
        lines.append("")
        lines.append(f'<a id="ag-{n}-1"></a>')
        lines.append("## 資料カード")
        lines.append("")
        lines.extend(cards)
        lines.extend(["---", "", nav(prev, nxt), ""])
        open(os.path.join(TB, f"appendix-g-{n}.md"), "w", encoding="utf-8").write("\n".join(lines))
        stats.append((n, title, len(es), n_ok, n_only))
    # G-13: 記載が無かった / 届かなかった
    neg = src.get("checked_no_mention", [])
    unr = src.get("unreachable", [])
    lines = [nav(files[11], None), "", "---", "", "# 付録 G-13 記載が無かったページと届かなかったページ", "",
             "<!-- このファイルは scripts/build_annotations_appendix.py が evidence/annotations_usage/ から作る。手で直さない。 -->", "",
             '<a id="ag-13-1"></a>', "## 記載が無かったページ", "",
             "ここに並ぶのは、調べた語（「調べた語」の列）が、そのページの中身に見つからなかったものです。"
             "**そのページに書かれていない**ことの証拠で、その製品が宣言を使わないことの証拠ではありません"
             "（別のページやソースコードに書かれていることがあります）。", "",
             f"{len(neg)} ページ。", "",
             "| 組織 — 製品 | ページ | 調べた語 | 結果 |", "|---|---|---|---|"]
    for x in neg:
        lines.append(f"| {md_escape_cell(x.get('org', ''))} — {md_escape_cell(x.get('product', ''))} | {x.get('url', '')} | "
                     f"{md_escape_cell(x.get('terms', ''))} | {md_escape_cell(x.get('result', ''))} |")
    lines += ["", '<a id="ag-13-2"></a>', "## 届かなかったページ", "",
              f"{len(unr)} ページ。中身を読めなかったので、何も言えません（不明）。", "",
              "| ページ | 理由 |", "|---|---|"]
    for x in unr:
        lines.append(f"| {x.get('url', '')} | {md_escape_cell(x.get('reason', ''))} |")
    lines += ["", "---", "", nav(files[11], None), ""]
    open(os.path.join(TB, "appendix-g-13.md"), "w", encoding="utf-8").write("\n".join(lines))
    # 表紙の生成部分
    gen = ["<!-- BEGIN GENERATED（scripts/build_annotations_appendix.py が作る。手で直さない） -->", "",
           "| 分冊 | 分野 | 資料 | うち [確認] | うち [確認（調査時のみ）] |", "|---|---|---|---|---|"]
    tot = ok_t = only_t = 0
    for n, title, cnt, ok, only in stats:
        gen.append(f"| [G-{n}](appendix-g-{n}.md) | {title} | {cnt} | {ok} | {only} |")
        tot += cnt
        ok_t += ok
        only_t += only
    gen.append(f"| [G-13](appendix-g-13.md) | 記載が無かったページ / 届かなかったページ | {len(neg)} / {len(unr)} | — | — |")
    gen.append(f"| | **計（G-1〜G-12）** | **{tot}** | **{ok_t}** | **{only_t}** |")
    gen.append("")
    uc = collections.Counter(u for e in entries for u in e.get("usage", []))
    gen += ["使い方の分類ごとの資料の数（1 つの資料に複数の分類が付くので、足しても資料の数にならない）:", "",
            "| 使い方の分類 | 資料の数 |", "|---|---|"]
    for u, c in uc.most_common():
        gen.append(f"| {USAGE_JA.get(u, u)} | {c} |")
    gen += ["", "<!-- END GENERATED -->"]
    p = os.path.join(TB, "appendix-g.md")
    if os.path.exists(p):
        s = open(p, encoding="utf-8").read()
        s = re.sub(r"<!-- BEGIN GENERATED.*?<!-- END GENERATED -->", "\n".join(gen), s, flags=re.S)
        open(p, "w", encoding="utf-8").write(s)
    else:
        open(os.path.join(EV, "generated_block.md"), "w", encoding="utf-8").write("\n".join(gen))
    print(f"cards {tot}, confirmed {ok_t}, no-mention {len(neg)}, unreachable {len(unr)}")


if __name__ == "__main__":
    main()
