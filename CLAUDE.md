# AuthGap — 作業の約束

**仕様の正本は `AUTHGAP_BRIEF_v3.md`（1210 行）。** 作業前に読むこと。
`RESUME.md` は経緯の記録で、参考程度。

## この repo で守る規則（破りやすいので先に書く）

1. **未検証の統計を引用しない。** 仕様書から転記した数値は
   `docs/cve_triage.csv` の `verified_by_me = none` のように**未検証と明示する**。
2. **CVE の修正コミットは脆弱性 DB の記載を信用しない。** `git log -S` で
   自分で特定し、diff を目視する（誤記載の実例が 4 件確定している）。
3. **閾値には必ず測定手続きと分母の定義を付ける。**
4. **解決できなかったものは「不明」として記録する。黙って安全側に倒さない。**
   記録先は `docs/open_questions.md`。
5. **仕様書が「凍結」と書いた項目は、凍結後に見た結果で変えない。**
   期待値ファイル（`fixtures/*/expected.json`）は採点器より**先に**コミットする。

## 語彙は 1 か所でしか定義しない

| 語彙 | 定義点 | 数 |
|---|---|---|
| validator 形状 | `authgap/catalog/validators.py: VALIDATOR_SHAPES` | 11 |
| weak 理由 | 同 `WEAK_REASONS`（月 6 凍結） | 19 |
| 格下げ属性 | 同 `DOWNGRADES`。**`self_granted` は weak 理由ではない** | 4 |
| config atom の源 | 同 `CONFIG_ATOM_SOURCES` | 4 |
| ゲート側 OPAQUE | `authgap/ir.py: GATE_OPAQUE_REASONS` | 8 |
| ゲート側 NODOM | 同 `GATE_NODOM_REASONS` | 4 |
| val 側 opaque | 同 `VAL_OPAQUE_REASONS`。**ゲート側とは別語彙** | 8 |
| 効果 kind と slot | `authgap/catalog/sinks.py: SLOTS` | 7 kind |

**語彙外の値は構築時に例外になる。** `DomResult(DomKind.NODOM, "made_up")` は
`ValueError`。新しい理由が要ると思ったら、まず `docs/open_questions.md` に書く。

## よく踏む落とし穴（全部一度踏んだ）

- **入れ子定義を落とさない。** 低レベル MCP のハンドラは `serve()` の中にある。
- **条件つき import を落とさない。** 任意依存は `try: import X` で包まれる。
- **`self.<attr>` の受け手推論が無いと proxy sink が 1 つも当たらない。**
- **主語一致は root で取る。** `arguments["a"]` と `arguments["b"]` を同じ root に
  潰すと、片方への検証が他方の位置に付く。
- **`startswith` の境界正規化は前の文にある。** `abs_dir += os.sep` を見ないと
  `strong-path` が `weak` に落ちる。
- **同一キーの衝突で MODEL 行を落とさない**（両側比較で変化が消える）。
- **形状語彙の語が本体に出るだけでは検証子にしない。** `split` や `Path()` は
  値の変換であって検証ではない。
- **コーパスの pin は SHA 一致を検証する。** 浅い fetch は黙って default branch に
  落ちる。

## 手順

```bash
uv venv .venv --python 3.10
uv pip install --python .venv/bin/python -r requirements.txt

.venv/bin/python scripts/check_gates.py        # B3a 8/8, B3b 15/15
.venv/bin/python scripts/mutation_test.py      # 実装変異 生存 <= 2
.venv/bin/python -m pytest tests/ -q
.venv/bin/ruff check .

.venv/bin/python scripts/fetch_corpus.py --spec docs/corpus_spec.json
.venv/bin/python scripts/two_sided.py --spec docs/corpus_spec.json   # T1 の主指標
.venv/bin/python scripts/ablation.py <木> ...                        # §3 の交差行
.venv/bin/python -m authgap probe <木>                               # F0a
.venv/bin/python -m authgap scan <木> --determinism 3                # 決定論
```

**手検証の入口は `docs/verification_guide.md`。**

## コミットの約束

- 何を直したかだけでなく、**なぜそれが誤りだったか**（どちらの方向に間違って
  いたか）を書く。誤 clear（false-clean）方向の誤りは特に明記する。
- 仕様書と食い違ったら、**仕様書の値を黙って書き換えない。**
  両方を記録して `docs/open_questions.md` に決定待ちとして残す。
