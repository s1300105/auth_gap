# scan_v2_gi_run1 — 矛盾と GAP_INJECT の重なりを数えるための取り直し（2026-10-13、探索。決定ではない）

- 凍結版（実装の結合 sha256 `35606ba9…` が `docs/fingerprint.json` と一致、`--require-fingerprint`）で母集団 v2（開発用、87 木）を
  `scripts/scan_v2.py --label gi_run1` で走らせ直した。**run24 と summary・木ごとの結果・contradictions.json が完全に一致した**
  （run24 には木ごとの manifest が残っていないため取り直した）。最終評価・練習のデータには走らせていない。
- `gap_inject_count.py`（`python -I gap_inject_count.py evidence/scan_v2_gi_run1 gi_counts.json`）で、矛盾の効果の位置を 4 段に分けて数えた。
  木ごとの manifest（`v2-*.json`）は追跡しない（`.gitignore`）。

| 段 | 定義 | 効果の位置 | ユニット × (site, kind) | ユニット | 木 |
|---|---|---|---|---|---|
| G0 | CONTRADICTION（D と M のギャップ） | 221 | 193 | 121 | 20 |
| G1 | G0 かつ同じ効果のどれかの制御位置に GAP_INJECT | 22 | 22 | 21 | 8 |
| G2 | G1 のうち主 slot（path / argv0 / shell_string / sql / url.host / code_text） | 8 | 8 | 8 | 4 |
| G3 | G2 のうち値が MODEL かつ resolved（D57 の「選べる」） | 1 | 1 | 1 | 1 |

G2 の 8 件は 4 か所: anybox の `os.remove`（同じ行に 5 ツール、path は MODEL・opaque）、canvas-mcp の `os.unlink`（opaque）、
godsaeng-salon の SQL（`sql` slot が MODEL・opaque。O33 の「流れ込むだけ」の可能性）、code-rag の `httpx` の `url.host`（resolved、G3）。
G1 から G2 で落ちた 14 件は、SQL の params・HTTP の body / url.path にモデルの値が入るもの（何をするかはコードが決める）。

数値は解析器の出力で、人の判定は通していない。
