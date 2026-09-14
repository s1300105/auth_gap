#!/usr/bin/env python3
"""§6 の標本設計に従って解析対象を抽出する（§7.6 D14）。

    F0a の分母 = 60 MCP サーバ + 30 ツールパッケージ
    T3-app     = 8 アプリ（§7.3 で 15 → 8 に切り詰め済み）

**probe（項目 A5）は同じコーパスで走らせる。別抽出にしない**（§6 標本設計）。

規則:

* **固定 seed**。`--seed` の既定 20260909 を動かさない。動かすと標本が変わる。
* **取得失敗を件数として記録する。黙って落とさない**（`docs/fetch_failures.md`）。
* repo ごとの commit SHA を `docs/frame.csv` に記録する。
* sparse パターンに `/**/*.txt` と `/**/*.lock` を含める（`fetch_corpus.py` が担当）。

出力: `docs/sampling.md`（抽出手続きと seed と一覧）、`docs/corpus_sample.json`
（`fetch_corpus.py --spec` に渡せる形）。
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import random
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRAME_JSON = os.path.join(ROOT, "docs", "frame.json")
SAMPLE_JSON = os.path.join(ROOT, "docs", "corpus_sample.json")
SAMPLING_MD = os.path.join(ROOT, "docs", "sampling.md")

#: **固定 seed。動かさない。**
DEFAULT_SEED = 20260909

#: §6 の標本設計。
N_MCP_SERVER = 60
N_TOOL_PACKAGE = 30
N_APP = 8

#: 較正対の repo は標本から除く（採点集合と野外集合を混ぜない）。
CALIBRATION_REPOS = frozenset(
    {
        "modelcontextprotocol/servers",
        "significant-gravitas/autogpt",
        "mervinpraison/praisonai",
        "langroid/langroid",
    }
)

#: T3-app（in-tree dispatch を持つエージェントアプリ）。
#: **code search で機械抽出できないので、名前つきの固定集合にする。**
#: 選定根拠を 1 件ずつ書く（事後選択を避けるため抽出前に固定する）。
APP_FRAME: tuple[tuple[str, str], ...] = (
    ("gptme/gptme", "§4 のケーススタディ 3 件のうちの 1 つ。in-tree の ToolSpec レジストリ"),
    ("TransformerOptimus/SuperAGI", "同上。RESTRICTED モードの承認リストを出荷している"),
    ("OpenHands/agent-sdk", "同上。ConfirmationPolicy.should_confirm を持つ"),
    ("OpenManus/OpenManus", "§2.6 の負例 fixture F5/F6/F7 の出所"),
    ("microsoft/autogen", "登録 API 経由の dispatch。assumed 側の対照"),
    ("crewAIInc/crewAI", "同上"),
    ("Significant-Gravitas/AutoGPT", "CommandRegistry による実行時 dispatch（D10 の測定対象）"),
    ("smol-ai/developer", "小さい木での挙動確認"),
)


def load_frame() -> dict:
    if not os.path.exists(FRAME_JSON):
        print(f"{FRAME_JSON} が無い。先に scripts/fetch_frame.py を走らせる", file=sys.stderr)
        sys.exit(2)
    with open(FRAME_JSON, encoding="utf-8") as fh:
        return json.load(fh)


def sample(frame: dict, seed: int, oversample: float) -> dict:
    """seed 固定の無作為抽出。

    :param oversample: 取得失敗を見込んだ割り増し率。**割り増し分も抽出順で
        固定する**（失敗したら次を繰り上げる。その場で選び直さない）。
    """
    rng = random.Random(seed)
    mcp_all = sorted(set(frame.get("repos", [])) - CALIBRATION_REPOS)
    tool_all = sorted(set(frame.get("toolpkg_repos", [])) - CALIBRATION_REPOS - set(mcp_all))

    def pick(pool: list[str], n: int) -> list[str]:
        k = min(len(pool), int(n * oversample))
        return rng.sample(pool, k) if k else []

    return {
        "seed": seed,
        "oversample": oversample,
        "sampled_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "frame_sizes": {"mcp_server": len(mcp_all), "tool_package": len(tool_all)},
        "targets_wanted": {
            "mcp_server": N_MCP_SERVER,
            "tool_package": N_TOOL_PACKAGE,
            "app": N_APP,
        },
        "mcp_server": pick(mcp_all, N_MCP_SERVER),
        "tool_package": pick(tool_all, N_TOOL_PACKAGE),
        "app": [r for r, _why in APP_FRAME],
        "app_rationale": {r: why for r, why in APP_FRAME},
    }


def to_corpus_spec(s: dict) -> dict:
    targets = []
    for pop, key in (("mcp_server", "mcp_server"), ("tool_package", "tool_package"), ("app", "app")):
        for repo in s[key]:
            targets.append(
                {
                    "repo": repo,
                    "ref": "HEAD",
                    "name": f"w-{repo.replace('/', '__')}",
                    "population": pop,
                    "note": f"F0a 標本（seed={s['seed']}）",
                }
            )
    return {
        "_note": (
            f"§6 の標本設計による野外集合。seed={s['seed']} で固定。"
            "**取得失敗は docs/fetch_failures.md に件数として残す。黙って落とさない。**"
        ),
        "targets": targets,
    }


def write_md(s: dict) -> None:
    lines = [
        "# 標本設計（§6 / §7.6 D14）",
        "",
        f"抽出日時 {s['sampled_at']}　**seed = {s['seed']}（固定。動かさない）**",
        "",
        "| 母集団 | フレーム件数 | 目標 | 抽出（割り増し込み） |",
        "|---|---|---|---|",
        f"| MCP サーバ | {s['frame_sizes']['mcp_server']} | {N_MCP_SERVER} | {len(s['mcp_server'])} |",
        f"| ツールパッケージ | {s['frame_sizes']['tool_package']} | {N_TOOL_PACKAGE} | {len(s['tool_package'])} |",
        f"| アプリ（T3-app） | {len(APP_FRAME)} | {N_APP} | {len(s['app'])} |",
        "",
        f"割り増し率 {s['oversample']}。**取得に失敗したら抽出順で次を繰り上げる。**",
        "その場で選び直すと事後選択になる。失敗は件数として",
        "`docs/fetch_failures.md` に残す。",
        "",
        "較正対の repo は野外集合から除いている（採点集合と混ぜない）:",
        "",
    ]
    for r in sorted(CALIBRATION_REPOS):
        lines.append(f"- `{r}`")
    lines += [
        "",
        "## T3-app のフレーム（**機械抽出できないので名前つきで先に固定する**）",
        "",
        "| repo | 選定根拠 |",
        "|---|---|",
    ]
    for r, why in APP_FRAME:
        lines.append(f"| `{r}` | {why} |")
    lines += [
        "",
        "## 抽出された repo",
        "",
        "<details><summary>MCP サーバ</summary>",
        "",
    ]
    for r in s["mcp_server"]:
        lines.append(f"- `{r}`")
    lines += ["", "</details>", "", "<details><summary>ツールパッケージ</summary>", ""]
    for r in s["tool_package"]:
        lines.append(f"- `{r}`")
    lines += ["", "</details>", ""]
    with open(SAMPLING_MD, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=DEFAULT_SEED)
    ap.add_argument(
        "--oversample",
        type=float,
        default=1.5,
        help="取得失敗を見込んだ割り増し率（既定 1.5）",
    )
    args = ap.parse_args()

    frame = load_frame()
    s = sample(frame, args.seed, args.oversample)
    with open(SAMPLE_JSON, "w", encoding="utf-8") as fh:
        json.dump(to_corpus_spec(s), fh, ensure_ascii=False, indent=2, sort_keys=True)
        fh.write("\n")
    write_md(s)
    print(f"MCP サーバ {len(s['mcp_server'])} / ツールパッケージ {len(s['tool_package'])} / アプリ {len(s['app'])}")
    print(f"wrote {SAMPLE_JSON} / {SAMPLING_MD}")
    if s["frame_sizes"]["mcp_server"] < N_MCP_SERVER:
        print(f"**フレームが目標 {N_MCP_SERVER} に足りない。** 母集団の取得手段を見直すこと")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
