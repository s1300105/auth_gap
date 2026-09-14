#!/usr/bin/env python3
"""§9-6: Python MCP サーバの母集団規模を測り、標本フレームを作る。

**§10 の最初の関門。** これだけは A5 まで待てない（待つと 98 木を取り直す）。

取得手段は次の順に試し、**最初に 300 件以上を返した手段を採用**して
手段名・取得日・クエリを `docs/population.md` に記録する（§9-6）。

1. libraries.io の dependents（`pypi/mcp`、`pypi/fastmcp`）
2. PyPI 公開 BigQuery `distribution_metadata.requires_dist`
3. GitHub code search
4. 公開レジストリ（`modelcontextprotocol/servers`、Smithery、PulseMCP）

**(3)(4) は PyPI 逆依存ではない。** 採用した場合は母集団の定義が
「PyPI 上の `mcp`/`fastmcp` 依存者」から「公開 Python MCP サーバ」に
変わることを明記する。

**重複除去の単位は GitHub リポジトリ**（`owner/name` を小文字化）。
1 リポジトリが複数の PyPI プロジェクト / 複数サーバを出荷していても 1 件。
リポジトリ URL が取れない配布物は別カウントで報告し 300 の判定に含めない。

**300 未満のときの切り替え先を先に固定する**（§9-6）: 母集団を
LangChain / CrewAI / agno / llama-index / openai-agents のツールパッケージに
切り替え、T3-tool の 60 ツールもそこから抽出する。

使い方::

    python scripts/fetch_frame.py                 # 4 案を順に試して記録
    python scripts/fetch_frame.py --method github # 手段を指定
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import subprocess
import time
from dataclasses import dataclass, field

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAME_JSON = os.path.join(ROOT, "docs", "frame.json")
POPULATION_MD = os.path.join(ROOT, "docs", "population.md")

#: §10 の関門。
THRESHOLD = 300

#: 300 未満のときの切り替え先（**先に固定する**）。
FALLBACK_POPULATION = (
    "langchain-ai/langchain",
    "crewAIInc/crewAI-tools",
    "agno-agi/agno",
    "run-llama/llama_index",
    "openai/openai-agents-python",
)

#: ツールパッケージ母集団のクエリ（Def 2 の R2 カタログの登録形に対応させる）。
#: **MCP サーバ母集団とは別フレームにする**（§10 の D 規則は母集団別に適用する）。
TOOLPKG_QUERIES = (
    '"from langchain_core.tools import BaseTool" language:Python',
    '"from crewai.tools import" language:Python',
    '"from agno.tools" language:Python',
    '"@function_tool" language:Python',
    '"from llama_index.core.tools" language:Python',
)

#: GitHub code search のクエリ。**PyPI 逆依存ではない**ことに注意。
GITHUB_QUERIES = (
    '"from mcp.server" language:Python',
    '"@mcp.tool" language:Python',
    '"from mcp.server.fastmcp" language:Python',
    '"server.call_tool" language:Python',
)


@dataclass
class MethodResult:
    """1 つの取得手段の結果。**失敗も記録する。黙って次へ行かない。**"""

    method: str
    queries: list[str] = field(default_factory=list)
    repos: set[str] = field(default_factory=set)
    #: リポジトリ URL が取れなかった配布物の数（300 の判定に含めない）。
    without_repo: int = 0
    ok: bool = False
    error: str = ""
    fetched_at: str = ""

    def to_json(self) -> dict:
        return {
            "method": self.method,
            "queries": self.queries,
            "n_repos": len(self.repos),
            "without_repo": self.without_repo,
            "ok": self.ok,
            "error": self.error,
            "fetched_at": self.fetched_at,
        }


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


# --------------------------------------------------------------------------
# 手段 1: libraries.io の dependents
# --------------------------------------------------------------------------


def method_librariesio() -> MethodResult:
    r = MethodResult("libraries.io dependents", fetched_at=_now())
    key = os.environ.get("LIBRARIES_IO_API_KEY")
    if not key:
        r.error = (
            "LIBRARIES_IO_API_KEY が無いので試行不能。"
            "**「試さなかった」ではなく「鍵が無くて試せなかった」と記録する。**"
        )
        return r
    import urllib.error
    import urllib.request

    for pkg in ("mcp", "fastmcp"):
        page = 1
        r.queries.append(f"libraries.io pypi/{pkg} dependents")
        while page <= 10:
            url = (
                f"https://libraries.io/api/pypi/{pkg}/dependents"
                f"?api_key={key}&per_page=100&page={page}"
            )
            try:
                with urllib.request.urlopen(url, timeout=30) as fh:
                    data = json.loads(fh.read().decode("utf-8"))
            except (urllib.error.URLError, TimeoutError, ValueError) as exc:
                r.error = f"{type(exc).__name__}: {exc}"
                return r
            if not data:
                break
            for item in data:
                slug = _repo_slug(item.get("repository_url") or "")
                if slug:
                    r.repos.add(slug)
                else:
                    r.without_repo += 1
            page += 1
    r.ok = True
    return r


# --------------------------------------------------------------------------
# 手段 2: PyPI 公開 BigQuery
# --------------------------------------------------------------------------


def method_bigquery() -> MethodResult:
    r = MethodResult("PyPI BigQuery distribution_metadata.requires_dist", fetched_at=_now())
    if not _has("bq"):
        r.error = (
            "`bq` CLI が無いので試行不能（GCP の課金プロジェクトも要る）。"
            "**「試さなかった」ではなく「環境が無くて試せなかった」と記録する。**"
        )
        return r
    r.error = "未実装（課金プロジェクトの指定が要るため手動で回す）"
    return r


# --------------------------------------------------------------------------
# 手段 3: GitHub code search
# --------------------------------------------------------------------------


def method_github(max_pages: int = 10, queries: tuple = GITHUB_QUERIES, label: str = "GitHub code search") -> MethodResult:
    r = MethodResult(label, fetched_at=_now())
    if not _has("gh"):
        r.error = "`gh` CLI が無いので試行不能"
        return r
    for q in queries:
        r.queries.append(q)
        for page in range(1, max_pages + 1):
            code, out = _run(
                [
                    "gh", "api", "-X", "GET", "search/code",
                    "-f", f"q={q}", "-f", "per_page=100", "-f", f"page={page}",
                ]
            )
            if code != 0:
                if "rate limit" in out.lower():
                    time.sleep(20)
                    continue
                r.error = out[:300]
                break
            try:
                data = json.loads(out)
            except json.JSONDecodeError:
                break
            items = data.get("items", [])
            if not items:
                break
            for it in items:
                full = (it.get("repository") or {}).get("full_name")
                if full:
                    r.repos.add(full.lower())
                else:
                    r.without_repo += 1
            if len(items) < 100:
                break
            time.sleep(7)  # code search は認証時 10 req/min
    r.ok = bool(r.repos)
    return r


# --------------------------------------------------------------------------
# 手段 4: 公開レジストリ
# --------------------------------------------------------------------------


def method_registry() -> MethodResult:
    r = MethodResult("public registry (modelcontextprotocol/servers ほか)", fetched_at=_now())
    if not _has("gh"):
        r.error = "`gh` CLI が無いので試行不能"
        return r
    r.queries.append("modelcontextprotocol/servers の README にあるリンク")
    code, out = _run(
        ["gh", "api", "-H", "Accept: application/vnd.github.raw",
         "/repos/modelcontextprotocol/servers/contents/README.md"]
    )
    if code != 0:
        r.error = out[:300]
        return r
    import re

    for m in re.finditer(r"https://github\.com/([A-Za-z0-9_.-]+)/([A-Za-z0-9_.-]+)", out):
        r.repos.add(f"{m.group(1)}/{m.group(2)}".lower().removesuffix(".git"))
    r.ok = bool(r.repos)
    return r


# --------------------------------------------------------------------------
# 補助
# --------------------------------------------------------------------------


def _has(cmd: str) -> bool:
    return subprocess.run(["which", cmd], capture_output=True).returncode == 0


def _run(args: list[str]) -> tuple[int, str]:
    p = subprocess.run(args, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).strip()


def _repo_slug(url: str) -> str:
    if "github.com/" not in url:
        return ""
    tail = url.split("github.com/", 1)[1].strip("/")
    parts = tail.split("/")
    if len(parts) < 2:
        return ""
    return f"{parts[0]}/{parts[1]}".lower().removesuffix(".git")


METHODS = (
    ("librariesio", method_librariesio),
    ("bigquery", method_bigquery),
    ("github", method_github),
    ("registry", method_registry),
)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--method",
        choices=[m for m, _ in METHODS] + ["toolpkg"],
        help="toolpkg はツールパッケージ母集団だけを取り直す（MCP 側の結果は保持）",
    )
    ap.add_argument("--max-pages", type=int, default=10)
    args = ap.parse_args()

    # `--method toolpkg` は既存の frame.json を読み込んでツールパッケージ側だけ
    # 取り直す。**MCP 側の採用結果と取得日を壊さない。**
    prior: dict = {}
    if args.method == "toolpkg" and os.path.exists(FRAME_JSON):
        with open(FRAME_JSON, encoding="utf-8") as fh:
            prior = json.load(fh)

    results: list[MethodResult] = []
    adopted: MethodResult | None = None
    for name, fn in METHODS:
        if args.method and name != args.method:
            continue
        print(f"-- 試行: {name}")
        r = fn(args.max_pages) if name == "github" else fn()
        results.append(r)
        print(f"   {r.method}: repos={len(r.repos)} ok={r.ok} {('error=' + r.error) if r.error else ''}")
        if r.ok and len(r.repos) >= THRESHOLD:
            adopted = r
            print(f"   → **採用**（{len(r.repos)} >= {THRESHOLD}）")
            break

    all_repos: set[str] = set()
    for r in results:
        all_repos |= r.repos

    # ツールパッケージ母集団は**別フレーム**として常に集める。
    toolpkg = MethodResult("(skipped)")
    if args.method in (None, "github", "toolpkg"):
        print("-- 試行: toolpkg（ツールパッケージ母集団）")
        toolpkg = method_github(args.max_pages, TOOLPKG_QUERIES, "GitHub code search (tool packages)")
        print(f"   {toolpkg.method}: repos={len(toolpkg.repos)} ok={toolpkg.ok}")

    if args.method == "toolpkg" and prior:
        prior["toolpkg_method"] = toolpkg.to_json()
        prior["toolpkg_repos"] = sorted(toolpkg.repos)
        with open(FRAME_JSON, "w", encoding="utf-8") as fh:
            json.dump(prior, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        print(f"\nツールパッケージ母集団 {len(toolpkg.repos)} 件を frame.json に追記した")
        return 0

    frame = {
        "threshold": THRESHOLD,
        "adopted_method": adopted.method if adopted else None,
        "adopted_n": len(adopted.repos) if adopted else None,
        "dedup_unit": "GitHub リポジトリ（owner/name を小文字化）",
        "definition_note": (
            "GitHub code search / 公開レジストリを採用した場合、母集団の定義は"
            "「PyPI 上の mcp/fastmcp 依存者」ではなく「公開 Python MCP サーバ」である"
        )
        if adopted and "github" in adopted.method.lower() or (adopted and "registry" in adopted.method.lower())
        else None,
        "methods": [r.to_json() for r in results],
        "repos": sorted(adopted.repos) if adopted else sorted(all_repos),
        "toolpkg_method": toolpkg.to_json(),
        "toolpkg_repos": sorted(toolpkg.repos),
        "fallback_population": list(FALLBACK_POPULATION),
    }
    os.makedirs(os.path.dirname(FRAME_JSON), exist_ok=True)
    with open(FRAME_JSON, "w", encoding="utf-8") as fh:
        json.dump(frame, fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")

    _write_population_md(results, adopted, len(all_repos))
    print(f"\nwrote {FRAME_JSON} / {POPULATION_MD}")
    if adopted is None:
        print(f"**{THRESHOLD} 件に届かない（最大 {len(all_repos)}）。**")
        print("§9-6 の切り替え先: framework のツールパッケージへ母集団を切り替える。")
        return 1
    return 0


def _write_population_md(results, adopted, n_union: int) -> None:
    lines = [
        "# 母集団（§9-6 / §10 の最初の関門）",
        "",
        f"関門: **重複除去後の Python MCP サーバが {THRESHOLD} 件以上**。",
        "**この関門だけは A5 まで待てない**（待つと 98 木を取り直すことになる）。",
        "",
        "**重複除去の単位は GitHub リポジトリ**（`owner/name` を小文字化）。",
        "1 リポジトリが複数の PyPI プロジェクト / 複数サーバを出荷していても 1 件。",
        "リポジトリ URL が取れない配布物は別カウントで報告し 300 の判定に含めない。",
        "",
        "再現: `python scripts/fetch_frame.py`",
        "",
        "## 試行した手段（優先順。**失敗も記録する**）",
        "",
        "| 順 | 手段 | 件数 | 成否 | 取得日時 | 備考 |",
        "|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(results, 1):
        note = r.error.replace("\n", " ") if r.error else ""
        lines.append(
            f"| {i} | {r.method} | {len(r.repos)} | {'○' if r.ok else '×'} | "
            f"{r.fetched_at} | {note} |"
        )
    lines += ["", "## クエリ", ""]
    for r in results:
        if not r.queries:
            continue
        lines.append(f"**{r.method}**")
        lines.append("")
        for q in r.queries:
            lines.append(f"- `{q}`")
        lines.append("")
    lines += ["## 判定", ""]
    if adopted:
        lines += [
            f"**採用: {adopted.method}（{len(adopted.repos)} 件 ≥ {THRESHOLD}）。関門を通過。**",
            "",
        ]
        if "code search" in adopted.method or "registry" in adopted.method:
            lines += [
                "**採用手段は PyPI 逆依存ではない。** したがって母集団の定義は",
                "「PyPI 上の `mcp` / `fastmcp` 依存者」ではなく**「公開 Python MCP サーバ」**である。",
                "この差を本文に明記すること（§9-6 の要求）。",
                "",
                "GitHub code search は 1 クエリあたり最大 1000 件しか返さないので、",
                "**得られた件数は母集団の下限である**（`total_count` は信用しない）。",
                "関門は「≥ 300」なので下限で判定できるが、**母集団規模そのものを",
                "論文に数として書くときはこの上限を併記する。**",
                "",
            ]
    else:
        lines += [
            f"**{THRESHOLD} 件に届かない（全手段の和集合で {n_union} 件）。**",
            "",
            "§9-6 の切り替え先（**先に固定してある**）: 母集団を LangChain / CrewAI /",
            "agno / llama-index / openai-agents のツールパッケージに切り替え、",
            "T3-tool の 60 ツールもそこから抽出する。切り替えても §10 の D 規則は",
            "母集団別に適用する。",
            "",
        ]
    with open(POPULATION_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    raise SystemExit(main())
