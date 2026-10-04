"""付録 H（判定の手引きを最初から読む）の原文の引用が、手引きの下書きの行と一字一句同じかを確かめる。

引用の書き方（付録 H の約束）:

    > 【原文 L98-110】
    > （下書きの 98 行目）
    > …
    > （下書きの 110 行目）

`> 【原文 La-b】`（1 行だけなら `> 【原文 La】`）の次の行から、`>` で始まる行が続くあいだを引用とみなし、
各行の先頭の `> `（空行は `>` だけ）を外したものが、下書きの a〜b 行目と完全に一致するかを見る。

使い方:
    python scripts/check_guide_quotes.py docs/textbook/appendix-h-*.md
    python scripts/check_guide_quotes.py --draft docs/drafts/final_judging_guide_draft.md FILE...

一致しない引用が 1 件でもあれば終了コード 1。引用の範囲が重なっていても構わない。
最後に、下書きの行のうちどの引用にも入らなかった行の範囲を出す（全部を写したかの確認用）。
"""
from __future__ import annotations

import argparse
import re
import sys

HEAD = re.compile(r"^> 【原文 L(\d+)(?:-(\d+))?】\s*$")


def _unquote(line: str) -> str | None:
    if line == ">":
        return ""
    if line.startswith("> "):
        return line[2:]
    return None


def check(paths: list[str], draft_path: str) -> int:
    draft = open(draft_path, encoding="utf-8").read().split("\n")
    covered = [False] * (len(draft) + 1)
    n_ok = n_bad = 0
    for p in paths:
        lines = open(p, encoding="utf-8").read().split("\n")
        i = 0
        while i < len(lines):
            m = HEAD.match(lines[i])
            if not m:
                i += 1
                continue
            a = int(m.group(1))
            b = int(m.group(2) or a)
            body: list[str] = []
            j = i + 1
            while j < len(lines):
                u = _unquote(lines[j])
                if u is None or HEAD.match(lines[j]):
                    break
                body.append(u)
                j += 1
            # 引用の後ろの空の `>` 行は区切りとして許す
            while body and body[-1] == "" and len(body) > b - a + 1:
                body.pop()
            want = draft[a - 1:b]
            if a < 1 or b > len(draft) or a > b:
                print(f"BAD  {p}:{i + 1} L{a}-{b}: 下書きの範囲外（下書きは {len(draft)} 行）")
                n_bad += 1
            elif body != want:
                n_bad += 1
                print(f"BAD  {p}:{i + 1} L{a}-{b}: 原文と一致しない")
                for k in range(max(len(body), len(want))):
                    got = body[k] if k < len(body) else "<無い>"
                    exp = want[k] if k < len(want) else "<無い>"
                    if got != exp:
                        print(f"     下書き L{a + k}: {exp!r}")
                        print(f"     引用        : {got!r}")
                        break
            else:
                n_ok += 1
                for k in range(a, b + 1):
                    covered[k] = True
            i = j
    print(f"一致 {n_ok} / 不一致 {n_bad}")
    gaps: list[tuple[int, int]] = []
    k = 1
    while k <= len(draft):
        if not covered[k] and draft[k - 1].strip():
            s = k
            while k <= len(draft) and (not covered[k]):
                k += 1
            e = k - 1
            while e > s and not draft[e - 1].strip():  # 範囲の末尾の空行は含めない
                e -= 1
            gaps.append((s, e))
        else:
            k += 1
    if gaps:
        print("どの引用にも入っていない下書きの行（空行を除く）: "
              + ", ".join(f"L{s}" if s == e else f"L{s}-{e}" for s, e in gaps))
    else:
        print("下書きの空でない行は、すべてどれかの引用に入っている")
    return 1 if n_bad else 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--draft", default="docs/drafts/final_judging_guide_draft.md")
    args = ap.parse_args()
    return check(args.files, args.draft)


if __name__ == "__main__":
    sys.exit(main())
