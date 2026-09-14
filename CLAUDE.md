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
6. **仕様書と実データが食い違ったら、実データを採り、仕様書の値も残す。**
   決定は `docs/decisions.md` に根拠つきで書く。**仕様書本体は書き換えない**
   （設計の記録として残す）。学生の入力が要るものだけ
   `docs/open_questions.md` に置く。

## 語彙は 1 か所でしか定義しない

| 語彙 | 定義点 | 数 |
|---|---|---|
| validator 形状 | `authgap/catalog/validators.py: VALIDATOR_SHAPES` | 12 |
| weak 理由 | 同 `WEAK_REASONS`（月 6 凍結） | 22 |
| 格下げ属性 | 同 `DOWNGRADES`。**`self_granted` は weak 理由ではない** | 4 |
| config atom の源 | 同 `CONFIG_ATOM_SOURCES` | 4 |
| ゲート側 OPAQUE | `authgap/ir.py: GATE_OPAQUE_REASONS` | 8 |
| ゲート側 NODOM | 同 `GATE_NODOM_REASONS` | 4 |
| val 側 opaque | 同 `VAL_OPAQUE_REASONS`。**ゲート側とは別語彙** | 8 |
| 効果 kind と slot | `authgap/catalog/sinks.py: SLOTS` | 7 kind |

**語彙外の値は構築時に例外になる。** `DomResult(DomKind.NODOM, "made_up")` は
`ValueError`。

語彙を仕様書から動かしたときは `VOCABULARY_REVISIONS` に日付と理由を残す。
**月 6 の凍結後は語彙を動かさず、`docs/preregistration.md` に逸脱として記録する。**

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
  値の変換であって検証ではない。**これは Def 5 のゲート等級の話。** §6 F0a の
  validator 形状は**構文的**で語の出現で数える（仕様どおり。混同して点検基準を
  作ったことがある — D17）。
- **コーパスの pin は SHA 一致を検証する。** 浅い fetch は黙って default branch に
  落ちる。**中断した worktree は HEAD が一致したまま空**なので、checkout の完了
  （sparse パターン設定済み・作業木が index と一致）も確かめる。
- **ソースは `ast.parse` にバイト列で渡す。** 文字列で読むと BOM 付きファイルが
  parse 失敗として黙って消える。
- **末尾名だけの解決を「やめる」と真の経路が消える。** 受け手型で裏付けられない
  解決は、降りたうえで効果の確度に `opaque(unresolved)` を合流する（D17 の改訂）。
- **列の分岐合流で要素を捨てない。** 形だけ残すと argv0 のリテラルが列全体の
  主体（MODEL）になる。共通の先頭は要素ごとに join する。
- **解析器を直したら `scripts/diff_effects.py` で較正対の効果行を突き合わせる。**
  受け入れテストが「両側 7/7」のまま通っても、経路の効果行は黙って消えうる。
- **`.gitignore` で親ディレクトリごと除外すると `!` の例外が効かない。**
  `evidence/*` と書く。

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

# 解析器を直したら（コミット前に）
.venv/bin/python scripts/diff_effects.py --before <直す前の commit> corpus/A9__vuln corpus/A9__fixed corpus/A18__vuln corpus/A18__fixed

# 野外 F0a（D14 / D16）。run 2 以降は Python 3.12
uv venv .venv312 --python 3.12 && uv pip install --python .venv312/bin/python -r requirements.txt
.venv312/bin/python -u scripts/f0a.py --sample docs/corpus_sample.json --label run2
.venv/bin/python scripts/compare_f0a_runs.py                          # run の差を処理系 / 解析器に分解
```

**手検証の入口は `docs/verification_guide.md`。**
**判断の履歴は `docs/decisions.md`。** 仕様書と違う値を出しているときは
まずここを見る。

## コミットの約束

- 何を直したかだけでなく、**なぜそれが誤りだったか**（どちらの方向に間違って
  いたか）を書く。誤 clear（false-clean）方向の誤りは特に明記する。
- 仕様書と食い違ったら、**仕様書の値を黙って書き換えない。**
  両方を記録して `docs/open_questions.md` に決定待ちとして残す。
