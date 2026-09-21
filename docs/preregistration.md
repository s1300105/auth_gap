# 事前登録（分母・閾値・判定規則）

仕様書 `AUTHGAP_BRIEF_v3.md` が閾値を置きながら**分母を書いていない**指標について、
分母の定義を固定する。併せて、仕様書が分母を書いている指標については
「仕様書の定義」と「実装が計算している量」が一致しているかを照合して記録する。

作成 2026-09-20。**最終更新 2026-09-20（§0 に枠組み検討の post-hoc 告知、§5 に逸脱 #1〜#2 を追加）。**

---

## 0. この文書の汚染状態（最初に読むこと）

**本文書は純粋な事前登録ではない。** 作成時点で以下を既に見ている。

| 見たもの | 場所 |
|---|---|
| F0a run1〜run6 の点推定（`validator_holding_ratio` 4.3〜6.5% ほか全関門） | `docs/f0a.md`、`docs/f0a_run*.md` |
| 木単位ブートストラップ区間（D18。9 セル中 8 が「境界」） | `docs/f0a_ci.md` |
| run6 の分母別の値（本文書 §2.2 の表そのもの） | `evidence/f0a_run6/units.jsonl` を集計 |
| **分母の選び方で `validator_holding_ratio` の関門が反転すること** | 同上 |
| **2026-09-20 追記 2**: 母集団を「宣言を持つ Python MCP サーバ」に変えた（`docs/decisions.md` D29、`docs/population_v2.md`）。**旧枠の r_D = 0.0%（run6）と §2.8 の全数調査を見た後の決定**である。旧枠の結果は対照として残す | D29 |
| **2026-09-20 追記**: 研究の枠組み変更（4 案 + 現状維持）の検討を行った。検討は run6・D23（D_prev 適用 16/98）・`evidence/w0/two_sided.json` を見た後であり **post-hoc** である。結論は「**今は枠を選ばない**。§10 の 3 連言を `r_prev` まで測って完成させ、既存 14 較正木での判別実験（§5 の逸脱 #2 参照）の判定規則を先に書いてから、仕様書自身の規則で枠を選ぶ」。`docs/decisions.md` D24 | `docs/decisions.md` D24 |

したがって本文書の §2.2 と §2.3 で「新規に固定する」定義は **post-hoc である**。
論文では「分母は run6 の結果を見た後に固定した」と明記する。この告知を落として
「事前登録した」と書いてはならない。

**純粋に事前であるもの**（本文書の固定が事前登録として機能する対象）:

- 標本を拡大した後の run（60/30/8 木を超える分）
- 月 6 凍結後の held-out advisory
- 月 10 の解析指紋凍結後の実行
- 解析器の修正（`docs/decisions.md` D20 の (1)〜(3)）**後**に取り直す evidence

**したがって §4 の判定規則は「run6 に遡って適用しない」。** 理由は §4 に書く。

---

## 1. 固定する理由

仕様書 §10 は率に閾値を置きながら、`validator_holding_ratio` の分母を定義していない
（`grep "validator 保有" AUTHGAP_BRIEF_v3.md` の該当は :1101 と :1143 の 2 行で、
どちらも分母を書いていない）。実装 `scripts/f0a.py:180` は
`n_with_validator / n_units`（**全ユニット**）を採っているが、この選択の根拠は
どこにも記録されていない。

一方で仕様書 §6 の指標表は D 層別存在率について
「**分母は危険効果を持つユニットで、効果検出器の偽陽性クラスを除いた値と粗い値の
両方を出す**」と明記しており、§10 も「**分母はすべて危険効果を持つユニットであり、
ツール全体ではない**」と書いている。**`validator_holding_ratio` だけが
この原則の外にある。**

実測すると、分母の選び方で関門の合否が反転する（§2.2 の表）。
**分母を固定しないまま標本を拡大すると、結果を見てから分母を選べてしまう。**
これは `CLAUDE.md` 規則 3（閾値には必ず測定手続きと分母の定義を付ける）に対する
違反であり、査読で最初に突かれる点でもある。

---

## 2. 分母の定義

### 2.1 母集団

母集団は 3 つ（`mcp_server` / `tool_package` / `app`）で、**母集団を跨いで合算しない**。
仕様書 §10 の D 規則が「母集団別に別々に適用する」と定めているのに従う。
出力順も `mcp_server → tool_package → app` に固定する（再現時の diff を安定させる）。

### 2.2 ユニット分母

**3 つすべてを計算し、3 つすべてを報告する。** 主分母は 1 つだけ指定する。

| 分母 | 定義 | 主 / 併記 |
|---|---|---|
| `all_units` | R1/R2 の入口として認識された全ユニット | 併記 |
| `dangerous` | 危険効果 kind（`EXEC` / `SPAWN` / `FS_READ` / `FS_WRITE` / `NET` / `DB` / `DISPATCH`）を 1 つ以上持つユニット | 併記 |
| **`dangerous_fp_excluded`** | `dangerous` から効果検出器の偽陽性クラス（非 DB の `.execute()` 等、§10 の機械判定規則）を除いたもの | **主分母** |

**主分母を `dangerous_fp_excluded` とする理由（原理による選択）**:

1. 仕様書 §6 の指標表と §10 が、D 層別存在率について明文で同じ分母を指定している。
   **`validator_holding_ratio` だけを別の分母にする根拠が仕様書に無い。**
2. validator は「危険効果の制御位置を守るもの」なので、危険効果を持たないユニットは
   validator を持つ動機が無い。それを分母に入れると「不要だから無い」と
   「必要なのに無い」が混ざる。§10 A5 の関門が問うているのは後者である。

**注記（run6 時点の事実）**: `dangerous` と `dangerous_fp_excluded` は現在**恒等**である
（3 母集団すべてで `n_units_with_dangerous_effect == _fp_excluded`）。
偽陽性クラスの判定が構造的に発火しないためで、原因は別に記録済み。
**2 つが恒等であることは、恒等でなくなった時点で分母の意味が変わることを意味する。**
したがって両方を出し続ける。

### 2.3 パス分母

**2 つとも計算し、2 つとも報告する。** 主分母は `all_paths`。

| 分母 | 定義 | 主 / 併記 |
|---|---|---|
| **`all_paths`** | 木の中の全 `.py`（`_SKIP_DIRS` の VCS / venv / cache を除く。現行どおり） | **主分母** |
| `src_only` | `path_class == "src"` のユニットのみ | 併記 |

**`path_class` の規則（本節が唯一の定義点）**: ユニットの `relpath` を `/` と `\` で
分割し、**最後の要素（ファイル名）を除く**いずれかの構成要素が次の集合に
（大文字小文字を無視して）一致すれば `non_src`、そうでなければ `src`。

```
test, tests, testing, script, scripts, example, examples,
sample, samples, doc, docs, benchmark, benchmarks, demo, demos
```

- **ディレクトリ名の構文規則のみで判定し、ファイルの中身を見ない。**
  測定集合を見て調整できないようにするため。
- 機械可読な実体は `scripts/denominators.py: NON_SRC_DIRS`。
  **規則を変えるときは先に本節を直し、§5 に逸脱として記録する。**

**主分母を `all_paths` とする理由**: 現行実装・過去 run1〜6・`docs/f0a_ci.md` の
区間がすべてこの分母で計算されており、主分母を変えると過去の run との継続性が切れる。
`src_only` は「配布されるツールの実装だけを測るとどうなるか」を示す併記値とする。

**`src_only` が必要な理由**: run6 のユニットの一定割合が `tests/` `scripts/` `examples/`
配下にあり（§2.4 の表の分母の差がそれを示す）、
「repo の全 `.py` を測った」のか「配布されるツールの実装を測った」のかで
量の意味が変わる。論文の母集団節には**両方の値と、この区別**を書く。

### 2.4 固定した分母での実測値（run6、`evidence/f0a_run6`）

再現:

```bash
.venv/bin/python scripts/denominators.py evidence/f0a_run6
```

| 母集団 | パス分母 | ユニット分母 | 分子 | 分母 | 率 | 関門 ≥5% |
|---|---|---|---|---|---|---|
| mcp_server | all_paths | all_units | 74 | 1669 | 4.43% | × |
| mcp_server | all_paths | dangerous | 52 | 431 | 12.06% | ○ |
| **mcp_server** | **all_paths** | **dangerous_fp_excluded** | **52** | **431** | **12.06%** | **○** |
| mcp_server | src_only | all_units | 68 | 1321 | 5.15% | ○ |
| mcp_server | src_only | dangerous | 48 | 405 | 11.85% | ○ |
| mcp_server | src_only | dangerous_fp_excluded | 48 | 405 | 11.85% | ○ |
| tool_package | all_paths | all_units | 17 | 521 | 3.26% | × |
| tool_package | all_paths | dangerous | 11 | 97 | 11.34% | ○ |
| **tool_package** | **all_paths** | **dangerous_fp_excluded** | **11** | **97** | **11.34%** | **○** |
| tool_package | src_only | all_units | 15 | 257 | 5.84% | ○ |
| tool_package | src_only | dangerous | 11 | 78 | 14.10% | ○ |
| tool_package | src_only | dangerous_fp_excluded | 11 | 78 | 14.10% | ○ |
| app | all_paths | all_units | 28 | 431 | 6.50% | ○ |
| app | all_paths | dangerous | 11 | 49 | 22.45% | ○ |
| **app** | **all_paths** | **dangerous_fp_excluded** | **11** | **49** | **22.45%** | **○** |
| app | src_only | all_units | 27 | 229 | 11.79% | ○ |
| app | src_only | dangerous | 11 | 44 | 25.00% | ○ |
| app | src_only | dangerous_fp_excluded | 11 | 44 | 25.00% | ○ |

**18 セル中、関門に落ちるのは 2 セルだけである**（`all_paths × all_units` の
mcp_server と tool_package）。**公表済みの「validator 保有 < 5%、関門 ×」は、
18 通りのうち最も分母が大きい 1 通りで計算した値である。**

この事実は §4 の判定規則の直接の根拠になる。

### 2.5 仕様書が既に分母を書いている指標（照合のみ。**新規に固定しない**）

| 指標 | 仕様書の分母 | 実装 | 一致 |
|---|---|---|---|
| `r_kind` / `r_op` / `r_prev` / `r_D` | 危険効果を持つユニット（偽陽性クラスを除いた値と粗い値の両方） | `scripts/f0a.py` の `branch` は `r_d`（偽陽性除外）で分岐 | **一致** |
| opaque 率 | 主 slot 7 種に限定、`opaque / (resolved + opaque)`、`remote` は分母外、省略既定引数の slot は分母外。粗い分母も併記 | `opaque_ratio_primary_slots_sites` と `_all_slots` を両方出力 | **一致** |
| `in_tree_resolution_ratio` | §10 の関門はサイト単位 | `in_tree_resolution_ratio_sites` を関門に使用、効果行単位も併記 | **一致** |

**これらは仕様書の定義をそのまま使い、本文書では動かさない。**

### 2.6 分母ではないが同じ整合性の問題を持つもの（本文書の対象外。参照のみ）

**両側通過率の分子**が、事前登録した期待タプル（`docs/cve_triage.csv` の
`expected_tuple_change`）とも変化の向きとも照合されない「任意座標の変化」で
実装されている。これは分母ではなく分子の定義の問題なので本文書では扱わないが、
**同じ「閾値に測定手続きが付いていない」類型である。**
対処は `docs/decisions.md` D20 の (2) に置く。

### 2.7 `r_prev` の測定手続きと分母（**測定前に固定する**）

仕様書 §10 の「方向そのものを疑うべき条件」の 3 つ目が `r_prev < 50%` である。
`r_prev` は配線が切れていて**これまで一度も測られていない**（`docs/decisions.md`
D22）。配線は直したので、**値を見る前に**手続きと分母をここで固定する。

**本節は §0 の汚染告知の例外である。** `r_prev` の値はまだ誰も見ていないので、
本節は**純粋な事前登録**として機能する。見ているのは「前リリースが 2 本以上
取れるのが 60 サーバ中 54 件 = 90.0%」という**仕様書の値**（本 repo では未追試）
だけで、これは分母の大きさの見込みであって `r_prev` の値ではない。

#### (a) 測る量

`r_prev` = **直前リリースと unit id で join できたユニットの割合**。
join は Def 6 のとおり **unit id の完全一致のみ**（`framework:qualified_name:schema_hash`）。
閾値は §10 の `50%`。**閾値は動かさない。**

#### (b) 対象の木

**run6 で解析した 98 木**（mcp_server 60 / tool_package 30 / app 8）。
run6 の他の指標と同じ標本にして比較可能にする。標本を選び直さない。

「現リリース」は `evidence/f0a_run6/trees.jsonl` に記録された `commit_sha` とする。
**新しく `HEAD` を取り直さない**（取り直すと run6 の他の値と別の木を測ることになる）。

#### (c) 「リリースタグ」の定義

タグ名に `\d+\.\d+` を含むものをリリースタグとする。ただし名前に
`rc` / `alpha` / `beta` / `dev` / `pre` / `snapshot` / `nightly` を
（大文字小文字を無視して）含むものは**プレリリースとして除く**。

接頭辞つきのタグ（`python-servers-0.6.2` のような形）も**含める**。
`modelcontextprotocol/servers` が実際にこの形なので、素朴な `^v?\d+\.\d+` で
判定すると当該リポジトリのタグが 1 本も取れない（確認済み）。

#### (d) 「直前リリース」の定義（**主**）

解析した commit の**祖先**であるリリースタグのうち、tagged commit の
**committer date が最も新しいもの**。解析した commit 自身を指すタグは除く。

* **祖先条件が要る理由**: 古いブランチへの backport リリースがタグ名の
  バージョン順では「直前」に見えることがある。祖先に限ると履歴上の直前になる。
* **日付順で並べる理由**: タグ名のバージョン順と履歴順は一致しない。

#### (e) 感度分析（**併記する**）

**5 リリース前**でも測る。仕様書の D_prev 節が引用する前測の数値
（新規または変化したユニット 5.4%、効果 kind の変化 0.20%）は
「約 5 リリース離れた 2 タグ」で得たものなので、その値と比較可能にするため。

(d) と (e) の**両方を報告する**（§3 の併記規則）。**主は (d)** である。
Def 6 の本文が「直前リリース」を第一の定義としており、「事前登録した基準
リリース」はその代替として置かれているため。

#### (f) 取得できない木の扱い（**ここが結果を動かす**）

| 状況 | 分母 | 記録先 |
|---|---|---|
| リリースタグが 0 本または 1 本 | **入れない** | `n_trees_without_prev`。Def 6 の適用条件「静的に取得できるリリースが 2 本以上」に当たる |
| タグはあるが取得（clone / checkout）に失敗 | **入れない** | `n_trees_prev_fetch_failed`。**件数を必ず報告する** |
| 前リリースは取得できたがユニット 0 件 | **入れる** | `n_trees_prev_no_units` |

**3 行目を分母に入れるのは、`r_prev` を下げる方向の選択である。**
「前リリースにそのツールがまだ存在しなかった」は、D_prev が宣言として
使えないケースそのものなので分母に入れる。この選択は §10 の
「方向そのものを疑うべき条件」（`r_prev < 50%`）を**成立させやすくする**、
つまり**自分に不利な側**である。測定前にこちらを採ることを記録しておく。

1 行目と 2 行目を分母から外すのは、**取得の失敗が「join できなかった」に
化けるのを防ぐため**である。取得できなかったことは `r_prev` ではなく
適用条件の充足率として別に報告する。

#### (g) ユニット分母

§2.2 の主分母（`dangerous_fp_excluded`）を使い、粗い分母も併記する（§3）。
§10 の他の率と同じ分母である。

#### (h) 手続き（再現可能な形で）

```bash
# 1. 各木のリリースタグを列挙し、(c)(d)(e) の規則で前リリースを決める
#    → docs/prev_releases.json に {tree: {prev_sha, prev_tag, steps_back, reason}} を記録
# 2. 前リリースを corpus/prev/<tree> に取得（fetch_corpus.py と同じ SHA 一致検証）
# 3. 前リリースを scan して manifest を作る
#    .venv/bin/python -m authgap scan corpus/prev/<tree> > prev/<tree>.json
# 4. 現リリースを --prev-manifest 付きで scan
# 5. r_prev を集計（scripts/f0a.py の PopStats.r_prev / r_prev_crude）
```

**手順 1 の出力（`docs/prev_releases.json`）は測定より先にコミットする。**
どの木にどのタグを選んだかを後から動かせないようにするため
（`CLAUDE.md` 規則 5 と同じ趣旨）。

#### (i) 既知の限界（測定前に記録する）

* **monorepo で別サブパッケージのタグが選ばれうる。** `modelcontextprotocol/servers`
  は `python-servers-*` と `typescript-servers-*` を同じ履歴に打つので、(d) の
  規則では TypeScript 側のタグが「直前リリース」になることがある。
  タグ名でサブパッケージを判定する規則は**入れない**（リポジトリごとの
  命名規約に依存し、標本を見て調整することになるため）。該当件数を記録する。
* `r_prev` は「join できるか」だけを測る。**join できた後に何が変わったか
  （`GAP_DRIFT` の収量）は別の量**であり、§10 の閾値はこれにかからない。

#### (j) 測ったあとにしてはいけないこと

* (c)〜(g) の規則を値を見てから変えない。変えるなら §5 に逸脱として記録する。
* 閾値 50% を動かさない（§10 が「動かすのは分母の定義だけ」と定めている。
  その分母を今ここで固定した）。
* **`None`（未測定）を `0` と書かない。** 実装は区別する（D22）。

---

### 2.8 宣言 D の全数調査（**数える前に書く**。2026-09-20）

**目的**: run6 の r_D = 0.0%（annotations 保有 1/2621）が「野外に宣言が無い」のか
「D パーサが見落としている」のかを分ける。**r_D の定義（§10、Def 6）は変えない。**
ここで数えるのは「宣言らしい文字列 / 構文の出現」であり、D_kind の値ではない。

#### (a) 段 A: run6 の 98 木での全数調査（パーサの再現率）

- **対象**: run6 と同じ 98 木・同じ commit（`evidence/f0a_run6/trees.jsonl` の
  `commit_sha`）。取得は `scripts/fetch_corpus.fetch`（SHA 一致検証つき）。
- **数える形（族ごとに別々に数え、合算しない）**:
  1. `mcp_hint_key`: `readOnlyHint` / `destructiveHint` / `idempotentHint` /
     `openWorldHint` のいずれかの語（文字列検索。JSON / dict / kwarg のどれでも）。
  2. `mcp_ToolAnnotations`: `ToolAnnotations` の語。
  3. `mcp_annotations_kwarg`（AST）: 呼び出しの keyword `annotations=` で、被呼び出し名の
     末尾が `tool` / `Tool` / `add_tool` / `ToolDefinition` のもの（`annotations=None` も
     数え、値の種類 = `ToolAnnotations` 呼び出し / dict / Name / None / その他 を記録）。
  4. `openhands_ToolDefinition`: `ToolDefinition(` の語（OpenHands。R2 カタログ外）。
  5. `agno_confirmation`: `requires_confirmation` / `external_execution` の語
     （agno の承認宣言。D_kind ではないが「承認が要る」という開発者宣言）。
  6. `openai_needs_approval`: `needs_approval` / `require_approval` の語。
- **分母**: 木（98）、Python ファイル（parse できたもの）、および
  `scripts/denominators.py: path_class` による **src / non-src（tests・examples・
  vendored・docs）** の別。**同梱 SDK（`mcp` パッケージ自身の複製、`site-packages`、
  `node_modules`、`.venv`）は non-src。**
- **パーサとの突き合わせ**: 族 3 のヒットのうち、`entries.find_tool_literals` /
  デコレータ読み取り（`entries.py:386`）が `annotations` として読んだ数
  （run6 は 1）との差を、木ごとに **「パーサが読んだ / 読めなかった（形）/
  R2 カタログ外の入口」** に分類する。
- **判定規則（結果を見る前に書く）**:
  - 族 1〜3 の src 側ヒットが **1 木でも**パーサ未読なら → パーサの再現率の欠陥として
    D28 で直し、r_D を**同じ 98 木で**測り直す（run6 の公表値は据え置き、D20 と同じ）。
  - src 側ヒットが 0（non-src のみ）なら → 「この枠（GitHub code search 由来の公開
    Python MCP サーバ）の自前コードには宣言が無い」が立つ。r_D = 0.0% はパーサの
    欠陥ではない。
  - 族 4〜6 のヒットは R2 カタログ / Def 6 の外なので r_D を動かさない。件数を
    「Def 6 が扱わない宣言」として記録し、Def 6 の拡張は別途判断（学生）。

#### (b) 段 B: 生態系全体（標本の外。**枠が違うので r_D と比べない**）

- GitHub code search（`docs/population.md` と同じ手段・同じ上限。1 クエリ最大
  1000 件、`total_count` は下限としてのみ使う）で次を数え、取得日時を記録する:
  - Python: `"readOnlyHint" language:Python`、`"ToolAnnotations" language:Python`、
    `"destructiveHint" language:Python`、`"openWorldHint" language:Python`
  - TypeScript / JavaScript: 同じ 4 語（宣言が **どの言語圏に**あるかを見る）
  - 参照値: 枠のクエリ `"from mcp.server" language:Python` 等の件数（`population.md`）
- **読み方（結果を見る前に書く）**: Python 側で宣言を含むファイル数が枠（2299 件）に
  対して小さければ、「宣言との差」を主張できる母集団は Python 公開 MCP サーバの中に
  **小さな部分母集団としてしか存在しない**。その部分母集団だけを標本にすることは
  **母集団の定義の変更**であり、やるなら第 2 の枠として事前登録してから抽出する
  （事後に絞ると事後選択）。TypeScript 側に多ければ、「宣言 vs 実効」の研究対象は
  言語の選択で決まっていたことを本文に書く（本解析器は Python のみ）。

#### (c) 数えた後にしてはいけないこと

- 族の定義や分母を値を見てから変えない（変えるなら §5 に逸脱として記録）。
- 段 B の件数を r_D の分子や分母に流用しない。
- パーサ未読が見つかった場合、run6 の公表値を書き換えない（再測定を run として足す）。

#### (d) 結果（2026-09-20。(a)(b) の規則は数えた後に変えていない）

**段 A**（97/98 木。`w-archsec-emman__financial-orchestrator` は消滅、O9）
`evidence/decl_census_run6/`（`scripts/declaration_census.py`）:

| 族 | 総ヒット | src | src の木 | non-src | non-src の木 |
|---|---|---|---|---|---|
| `mcp_hint_key` | 389 | 169 | 5 | 220 | 12 |
| `mcp_ToolAnnotations` | 229 | 76 | 4 | 153 | 8 |
| `mcp_annotations_kwarg`（AST） | 46 | 12 | 3 | 34 | 7 |
| `openhands_ToolDefinition` | 4 | 2 | 2 | 2 | 1 |
| `agno_confirmation` | 47 | 43 | 3 | 4 | 1 |
| `openai_needs_approval` | 127 | 55 | 5 | 72 | 10 |

**判定規則の適用**: 族 1〜3 の src ヒットがある木 5、うちパーサ未読 5 → 規則どおり
**`parser_recall_defect` が発火した。** ただし 5 木のヒットを目視で分類すると:

| 木 | 中身 | 分類 |
|---|---|---|
| `w-OpenHands__agent-sdk` | `ToolDefinition(... annotations=ToolAnnotations(readOnlyHint=..., destructiveHint=...))` が `openhands-tools/*/definition.py` 15 ファイル + SDK 自身の `ToolAnnotations` モデル定義 | **本物の宣言だが R2 カタログ外の枠組み**（app 母集団） |
| `w-mastermindx-market-intelligence__mastermind` | 低レベル `mcp_types.Tool(annotations=ToolAnnotations(...))` 4 サーバ。明示（`readOnlyHint=True`）は 1 リテラルで `name` が文字列リテラルでない | **O5**（低レベルハンドラと名前 join できない）+ 名前が非リテラル |
| `w-ancientdev0x__nanodistill` | `types.Tool(annotations=<属性参照>)`、hint はレジストリのデータ構造にある | 間接形（データフローが要る） |
| `w-Significant-Gravitas__AutoGPT` | `copilot/sdk/tool_adapter.py`（別 SDK へ変換するアダプタ） | 変換器（宣言の生成側ではない） |
| `w-gptme__gptme` | `mcp_adapter.py` / `cli_confirm.py`（hint を**読む**側） | 消費者 |

つまり「パーサが認識する形を読み損ねた」ものは無く、**未読の原因は R2 カタログの
範囲（OpenHands）と Def 6 の join 規則の欠落（O5）**である。run6 の 1/2621 は
同梱 MCP SDK のテスト（`tests/server/test_lowlevel_tool_annotations.py`）だった。

**探索的補助**（`scripts/declaration_join_probe.py`、`join_probe.json`。**r_D の定義は
変えていない**）: 97 木の `Tool(...)` リテラル 676 のうち明示 hint を持つものは **2**
（上の SDK テスト 1 + mastermind 1）。低レベルハンドラの `dispatch_names` で join する
規則を入れても明示宣言を持つユニットは 1/2533 のまま（mastermind の 1 件は名前が
非リテラルで join できない）。**O5 を直しても、この枠では r_D は 0 のままである。**

**段 B**（`github_counts.json`、GitHub API の `total_count`。ファイル単位の参考値で、
fork と vendored の複製を含む。母集団の数として本文に書かない）:

| 語 | Python | TypeScript |
|---|---|---|
| `readOnlyHint` | 28,928 | 79,744 |
| `ToolAnnotations` | 22,144 | 9,120 |
| `destructiveHint` | 19,328 | 53,504 |
| `openWorldHint` | 15,616 | 50,112 |
| `annotations=ToolAnnotations(`（呼び出し形） | 9,328 | — |
| 参照: `from mcp.server` | 172,544 | — |

読み（(b) に書いた規則どおり）: Python 側で呼び出し形の宣言を含むファイルは枠の
参照値に対して約 5%（9,328 / 172,544、ファイル単位・参考値）。**宣言との差を主張
できる母集団は、公開 Python MCP サーバの中の小さな部分母集団としてしか存在しない。**
TypeScript 側の hint 語は Python の 2〜3 倍で、宣言の慣行は TypeScript 圏に偏る
（本解析器は Python のみ）。この部分母集団を対象にするなら**第 2 の枠として事前登録
してから抽出する**（事後の絞り込みは事後選択）。決定は O14（学生）。

#### (e) 追加の照合（**結果 (d) を見た後に行った探索的な調査**。枠が違うので r_D と比べない）

学生の疑問「もっと宣言を持つ repo はあるはず。推奨されているのでは」への確認
（`evidence/decl_census_run6/top30_check.json`）:

- **標本内の再確認**: 97 木の `@x.tool(...)` デコレータ 1,506 個（47 木）のうち
  `annotations=` を渡すものは 2 個（同梱 SDK のテスト）。JSON / YAML / TS 側にも
  自前の宣言は無い（hint 語が出る JSON はベンチマーク fixture と MCP schema の複製）。
  **標本内で宣言が無いのは数え方の問題ではない。**
- **別の枠での宣言率**: `topic:mcp-server language:Python`（10,781 repo）を星数順に
  上位 30 取り、SDK 自身を除く 29 repo に `ToolAnnotations` の有無を当てると
  **9/29 = 31%** が使っている（Scrapling、serena、awslabs/mcp、Klavis、
  excel-mcp-server、FinanceToolkit、tradingview-mcp、QuantDinger、unstract）。
  公式 `modelcontextprotocol/servers` の Python サーバでも git / time が使う。
- **読み**: 宣言は「推奨されているのに誰も書かない」のではなく、**成熟した /
  組織が保守するサーバでは 3 割程度が書き、code search の import 文で拾った
  標本（小規模・チュートリアル・生成コードが多い）ではほぼ書かれない**。
  つまり r_D = 0.0% は **標本の枠の性質**であり、母集団の定義を
  「星数 / 保守されているサーバ」に変えれば D を持つ部分母集団は取れる。
  それは第 2 の枠として事前登録してから抽出する（O14）。
- 仕様の原文（`schema.json` 2025-03-26 の `ToolAnnotations` の説明）は
  `top30_check.json` に転記した。annotation は任意の **hint** であり、クライアントは
  信頼できないサーバの hint に基づいて判断してはならないとされる（= 宣言は
  「守られる保証の無い自己申告」で、AuthGap が D と M を比べる動機そのもの）。

### 2.9 低レベル MCP ハンドラと宣言の join（O5 の規則。**実装より先に書く**。2026-09-20）

新母集団（`docs/population_v2.md`）では低レベル形 `Tool(name="x", annotations=...)`
+ `call_tool` ハンドラの分岐が主流になるので、Def 6 に無かった join 規則を置く。
**r_D の定義（明示 = `readOnlyHint==true` / `destructiveHint==false` /
`openWorldHint==true` のいずれか）は変えない。**

- **(a) join**: ハンドラ unit `u` に対し、`Tool(...)` リテラル `L` は
  `L.name ∈ u.dispatch_names`（ハンドラ本体の `name == "<literal>"` 分岐から得た
  候補名）のとき join する。名前が文字列リテラルでない `Tool(name=<式>)` は join
  しない（件数を出す）。
- **(b) 効果の帰属**: ハンドラ内の効果 `e` は、`e` を支配する `name == "<t>"` 判定が
  あればツール `t` に帰属する（支配判定は `authgap/dominance.py` の既存機構）。
  どの名前判定にも支配されない効果（分岐の外の共通処理）は、join した全ツールに
  帰属する。
- **(c) D_kind の当て方**: 効果ごとに、帰属先ツールの宣言で D_kind を作る。
  複数ツールに帰属する効果は、**最も厳しい宣言**（readOnly を宣言するツールが
  1 つでもあればそれ）で判定する。方向: 厳しい側に倒すので **false-dirty**
  （共通処理の書き込みが read-only ツールの GAP に見える）。**false-clean 側には
  倒さない。** 該当件数を `notes` に出す。
- **(d) 未 join**: join できないリテラル（名前非リテラル / 対応する分岐が無い）と、
  リテラルの無い dispatch 名（ハンドラにあるが `Tool(...)` が無い）は件数を出す。
- **(e) 期待値を先に置く**: `fixtures/entries` または新規 fixture に、
  (i) 2 ツール・別宣言・分岐内効果、(ii) 共通処理の効果、(iii) 名前非リテラル、
  (iv) FastMCP デコレータ形（既存経路が壊れないこと）の 4 形を、実装より先に
  コミットする（規則 5）。
- **(f) 変えてはいけないこと**: 値を見てから (c) の「最も厳しい宣言」を緩めない。
  緩めるなら §5 に逸脱として記録する。
- **(g) 実装時の具体化（2026-09-20、母集団 v2 を測る前）**: (c) の「最も厳しい宣言」は
  帰属先の宣言の**積**（`dparse.meet_d_kind`）として実装した: `upper` はどれか 1 つでも
  ⊥ なら ⊥、全部にあれば積; `explicit` / `present_no_bound` は和; `unknown` はどれか
  1 つでも; `open_world` は全部が宣言したときだけ。これは「帰属先の各ツールで判定した
  verdict の和集合」と同じで、(c) の文言（readOnly が 1 つでもあればそれ）より厳しいか
  等しい（false-clean には倒れない）。ユニット水準の `D_kind`（`r_D` の分子）も
  join した全ツールの積にする = ハンドラは全ツールが明示宣言を持つときだけ分子に入る
  （保守的）。ツール単位の数（明示宣言を持つツール / join したツール）は
  `D_kind_by_tool` から別途集計して併記する。`match` 文の分岐は CFG の test に文字列
  定数として現れないので全ツール帰属（保守的）。fixture `fixtures/dispatch_join`
  5 件 XPASS、既存の受け入れ関門は不変。

### 2.10 NET 込み / 除きの分母（2026-09-21。**値を出す前に書く**）

審査パネルの指摘（D24「見落とし」8）: `NET` は `DANGEROUS_KINDS` と verdict の両方で
無条件に危険扱いだが、仕様書 Def 6 の P0 は private-range の NET に限る。旧枠では
危険ユニット 577 のうち NET のみが 300 で、577 を分母にする全指標が NET の扱いで動く。

- 追加するユニット分母: **`dangerous_non_net`** = NET 以外の危険効果
  （EXEC / SPAWN / FS_WRITE / FS_READ / DB）を 1 つ以上持つユニット。
  既存の `dangerous`（NET 込み）と**必ず併記**する。主分母は §2.2 のまま
  （`dangerous_fp_excluded × all_paths`、NET 込み）で動かさない。
- tests / examples 除外は既存の `src_only`（§2.3、`NON_SRC_DIRS`）で足りるので新設しない。
- 適用先: validator 保有率（`scripts/denominators.py`）。`r_D` / `r_prev` の分母にも
  同じ区別を出せるが、本節では validator 保有率だけを先に固定する。
- 変えてはいけないこと: `NET` を `DANGEROUS_KINDS` から外さない（verdict の問題で
  はなく分母の問題として扱う）。値を見てから主分母を替えない。

## 3. 併記規則

1. **§2.2 の 3 分母 × §2.3 の 2 分母 = 6 通りをすべて計算し、すべて報告する。**
   論文本文に載せるのは主分母（`dangerous_fp_excluded × all_paths`）の値とし、
   残り 5 通りは付録の表に置く。**「主分母の値だけを出す」ことをしない。**
2. `scripts/denominators.py` は 6 通りすべてを出力する。
   **片方だけを出力する経路を実装しない**（意図的な設計）。
3. D18 の木単位ブートストラップ区間を主分母に併記する。
   **区間が閾値を跨ぐセルは「境界」と書き、点推定だけで合否を主張しない**（D18 を継承）。
4. 論文の母集団節に「ユニットは repo 内の全 `.py` から抽出し、テスト・例示コードを
   含む」と明記し、`src_only` との差を数値で示す。

---

## 4. 判定規則（**run6 に遡及しない**）

**本文書で固定した分母を run6 の合否判定に遡って適用しない。**

理由: §0 のとおり、主分母 `dangerous_fp_excluded` は
「run6 の `all_paths × all_units` が 4.43% で関門に落ちている」ことを見た後に選んだ。
選択の根拠は §2.2 の原理 2 点であって観測値ではないが、**選択が関門を
× → ○ に反転させる方向であることを知った後の選択である以上、
その反転を「関門を通過した」という主張に使ってはならない。**

したがって:

- **run6 の関門判定は、公表済みのまま（`all_paths × all_units` で ×）据え置く。**
  `docs/f0a.md` / `docs/f0a_ci.md` / `docs/f0a_run*.md` の数値と判定は書き換えない。
- 本文書の主分母での値（12.06% / 11.34% / 22.45%）は
  **「分母を変えるとこうなる」という感度分析として報告する。**
- **関門の再判定は、本文書の固定後に取る次の run で行う。**
  そこでは分母が事前に固定されているので、判定を主張してよい。

**次の run が満たすべき条件**（これを満たさない run で関門を再判定しない）:

1. 本文書（`docs/preregistration.md`）が先にコミットされていること
2. `docs/decisions.md` D20 の解析器修正 (1)〜(3) が済んでいること
   （等級づけが両方向に壊れたまま validator を数え直しても意味が無いため）
3. 標本が拡大されていること、または拡大しない理由が記録されていること

**§10 A5 の対処の扱い**: 「validator 保有 < 5% → クラス 2 は T1+T2 のみ」は、
上記の再判定が済むまで**保留**とする。run6 の × を根拠にクラス 2 を落とさないし、
本文書の ○ を根拠にクラス 2 を維持するとも主張しない。

---

## 5. 逸脱の記録

本文書の定義を変えたときは、**変更前の定義・変更後の定義・理由・日付・
変更時点で見ていた数値**をこの節に追記する。追記せずに定義を変えてはならない。

仕様書 §6「凍結」の規定により、月 6 のゲート語彙凍結後に語彙を変更した場合も
この節に逸脱として記録する。

| # | 日付 | 対象 | 変更前 | 変更後 | 理由 | その時点で見ていた数値 |
|---|---|---|---|---|---|---|
| 1 | 2026-09-20（記録日。逸脱自体は本文書より前） | **T1 の採点集合**（仕様書 §6 T1.6） | 事前登録: `{A1, A2, A3, A5, A7, A9(+A10), A11, A15}`（4 プロジェクト）。補充順序 `A18 → A14 → A4 → A13` | 実際に走らせた対: `{A1, A2, A3, A4, A5, A9(+A10), A18}`（`docs/corpus_spec.json`）。**A7 / A11 / A15 が未検証のまま落ち、補充順序の A14 を飛ばして A18 と A4 が入っている** | 記録が無い。本文書の作成時点で `docs/decisions.md` / `docs/open_questions.md` / `docs/preregistration.md` のいずれにも無かった（審査パネルが指摘、本人が確認）。**理由は本項の記録者には分からない**ので「不明」とし、学生が理由を知っていれば追記する | `evidence/w0/two_sided.json`（7/7）は既に見ていた。**この逸脱を記録する前に「7/7」を根拠に使っていた**ことを認める |
| 2 | 2026-09-20 | **判別実験の判定規則**（§2.7 と同じ趣旨。**未実施なので純粋な事前登録**） | 無し | 既存 14 較正木だけで 3 実験を行う: (a) `two_sided.py` の分子を `expected_tuple_change` との照合に直し、厳密一致 / 座標一致 / any-change の 3 列を出す。(b) `ARMS` に等級潰し腕 `C0`（位置をゲートする検証子があれば等級に関係なく `req_val=OP`）を足し、`C − C0` の差集合を出す。(c) CodeQL `py/path-injection` を A1 / A4 / A10 に当て、「引き分け / 脆弱側 false-clean / 修正側 clear 不能 / **その構文を被覆しない**」の 4 類型で記録する（4 番目は仕様書 §1.5.4 に無いのでここで足す）。**判定規則**: `C − C0` に A10 が残り、かつ CodeQL が A10 脆弱側の `abspath + startswith` を clear する → 等級づけを主張の章として立てる。`C − C0 = ∅`、または CodeQL も A10 を両側判別 → 等級づけは manifest 属性と fixture / mutant のカタログに降ろし、較正表として報告する | 枠を選ぶ前に「等級づけが二値モデルと分かれるか」を決めるため。**結果を見てから規則を決めない** | 7/7、厳密 0/7、INJECT 1/7、A10 が等級だけで分かれた唯一の検証済み対であること。**判別実験の結果はまだ見ていない** |
| 3 | 2026-09-20 | **判別実験 (b) の fixture 水準の期待 `C − C0`**（`tests/test_value_grade.py` D 節、`d2b501a`） | `{b1, b2}` | `{a1, a2, a3, b1, b2, b3}` | D21 の inline 採点（`_grade_inline`）が敵対的レビューで false-clean 25 形を入れたことが確定し、D25 で撤回した。inline 形は一律 weak に戻るので a1〜a3 / b3 が C で MODEL になり、C0 との差に入る。**結果を見て期待を動かしたのではなく、等級規則の撤回の機械的な帰結**。a1〜a3 が差に入るのは false-dirty 側であり、「等級づけが正しく verdict を動かした位置」は依然 b1 / b2 の 2 つ。較正対での `C − C0` は撤回後に `scripts/two_sided.py`（腕 C / C0）で取り直す | `docs/decisions.md` D21「結果」・D25 | 撤回前（HEAD `654bca2`）に較正対 A1 / A4 / A9-A10 の C / C0 探針を**見ていた**: A1 / A4 は両腕で同じ（脆弱側に検証子が無いので C0 は何も変えない）、A10 は C0 で脆弱側の `req_val` が MODEL → OP に変わり（`grade` は両腕とも weak → strong-path）、**事前登録どおりの照合（`req_val MODEL → OP`）では C0 で落ちる = A10 ∈ C − C0**。any-change では両腕とも通過。この観察は撤回前の解析器のものなので、撤回後に取り直した値を正とする |
| 4 | 2026-09-20 | **判別実験 (c) の結果と、公平な比較の規則**（**この行の規則は結果を見る前に書く**） | (c) は CodeQL `py/path-injection` を既定の source model のまま当てる | **結果（既定 source model）**: A1 脆弱 0 / 修正 0、A4 脆弱 0 / 修正 0、A9-A10 脆弱 2 / 修正 2（2 件とも `examples/python/api/secondary-market-research-api.py` の FastAPI 経路で、A10 の `write_file` とは無関係。両側で同一）。**3 対とも第 4 類型「その構文を被覆しない」**: 既定の source は remote flow source（Flask / FastAPI 等）であり、MCP ツール引数も praisonai のツール関数引数も source にならない。よって #2 の判定規則の前提（CodeQL が A10 脆弱側を clear するか両側判別するか）が**成立せず、(c) は判別に使えない**。**規則 #4（公平な比較。未実施）**: source を AuthGap と同じ入口集合にした CodeQL クエリ（`PathInjectionCustomizations::Source` を拡張し、`docs/corpus_spec.json` の各木で AuthGap が入口と認識したユニットの引数を source にする）で同じ 3 対を回し、同じ 4 類型で記録する。判定規則は #2 と同じ（CodeQL が A10 脆弱側の `abspath + startswith` を clear（第 2 類型）→ 等級づけを章に、両側判別 → 降ろす）。**source を揃えても第 4 類型になった場合**（sink model が `open` / `os.makedirs` を被覆しないなど）は、(c) を「決定不能」として記録し、(a)(b) だけで #2 の規則を適用する | 既定の CodeQL は MCP ツール引数を source にしないので、比較が「解析器の差」ではなく「入口モデルの有無の差」を測ってしまう。**入口を揃えないと等級づけの主張と無関係な差が出る** | 既定 source model での 6 木の結果（上）。**規則 #4 の実行結果はまだ見ていない** |
| 5 | 2026-09-20 | **A18 の期待タプル**（`docs/expected_tuples.json`、`d2b501a`） | `sql: grade None → unknown` | `sql: grade None → weak` かつ `weak_reason None → statement_type_only` | 転記元 `docs/cve_triage.csv` の `expected_tuple_change` は D1（2026-09-09、語彙改訂で `statement_type_only` を新設）より前の文で、D1 自身が A18 の形を「値そのものは自由な SQL のままなので strong ではなく、拒否リストでもない」= `weak(statement_type_only)` と定めている。転記が D1 を反映していなかった（**転記の誤り**であり、解析器の出力に合わせた変更ではない。根拠は D1 の日付）。**結果を見た後の変更なので両方の値を報告する**: 転記どおり 7/8、D1 どおり 8/8 | 判別実験 (a) の最初の照合（腕 C、D25 後）で A18 だけが落ちた: 観測 `None → weak(statement_type_only)`。他の 7 対は事前登録照合・座標一致・any-change とも通過。逆向き 4 対と `open → read_text` の対は事前登録照合で不通過（期待どおり） |
| 6 | 2026-09-20 | **手順 1 の機械化（`scripts/prev_releases.py`）の欠陥と `docs/prev_releases.json` の訂正**（規則 §2.7 (c)(d) は変えていない） | `72bc952`: crewAI の直前 = `v0.5.2`（2024-02-06）、5 つ前 = `1.14.5a5` | crewAI の直前 = `1.15.21`（2026-09-09）、5 つ前 = `1.15.17`。**他の 15 木は不変** | `_run` が stdout と stderr を連結していたため、`git show -s --format=%cI` が stderr に出した gc の案内（`See "git help gc" for manual housekeeping.`）が日付として記録され、文字列比較で最大になって最古のタグが「最新」になった。**規則の適用誤り（実装の欠陥）であり、規則の変更ではない。** 日付が ISO 形式でなければ例外にするよう直した | **run1 の値を見た後に見つけた**（欠陥は run1 の結果の不自然さ — crewAI の直前が 14 ユニット、5 つ前が 282 ユニット — から辿った）。run1（as-run）: `prev` 全体 64.2%（97/151）、app 8.3%（4/48）、mcp_server 87.7%（71/81）、tool_package 100%（22/22）；`prev5` 全体 84.8%。run2（訂正後）を正とし、run1 を併記する（`evidence/r_prev_run1/README.md`） |
| 7 | 2026-09-20 | **CONTRADICTION の規則と sink 表の属性**（Def 7、`authgap/catalog/sinks.py`） | `destructiveHint==false` の明示があれば FS_WRITE 全部を矛盾に数える（`dparse.contradiction`）。sink 表に削除 / 追記の区別なし | FS_WRITE 行に `destructive` 属性（削除・上書き型 True / 追記型 False / `open` は mode 依存、読めなければ True）を足し、`destructiveHint==false` に対しては削除・上書き型だけを矛盾に数える。`readOnlyHint==true` は従来どおり全部 | `d_kind_from` は destructiveHint==false の上界に追記型 FS_WRITE を含めるのに、`contradiction` は FS_WRITE を無条件に矛盾としていた（同じ効果が宣言内かつ矛盾）。学生の決定 O16（D32）。kind / slot の語彙は変えず属性を足すだけ | 母集団 v2 の CONTRADICTION 80 件（うち destructiveHint==false のみ 32 件: mkdir 6 / makedirs 1 / open 5 / write_text 2 / write_bytes 3 / rmtree 3 / unlink 3 / remove 1 / replace 2 / chmod 1 / Path.open 1 / subprocess.run 4）を見た後の変更。変更前後を併記する |
| 8 | 2026-09-21 | **母集団 v2 の tree budget**（§2.1 の手続きは run6 と同じ 180 s） | 180 s（run1: 716 ユニットを飛ばした） | **主結果は 180 s のまま。** 900 s の再走（`evidence/f0a_v2_run2_budget900`）を感度分析として併記する | 飛ばした 716 ユニットが**すべて 1 木**（`david-li0406/meta-skill-evloving`、.py 36,900）のものだと分かり、欠損がランダムではないため。budget を上げて主結果を差し替えることはしない（D34） | run1: validator 保有 3.51%（主分母）×。再走: 8.38% ○（当該 1 木を除くと 3.51%）。木単位の区間は両方とも閾値を跨ぐ |
| 9 | 2026-09-21 | **決定論チェックの主張の範囲**（§0 の「`scan --determinism 3` 3 回一致」） | manifest 全体のバイト一致 | **壁時計 cap の印（`TRUNCATED(wall_clock)`、`WALL_CLOCK_CAP = 10 s`）を除いた manifest** のバイト一致 | 87 木中 85 木で一致。`xorbitsai/xagent` は 1 プロセス内 2 回目で cache が温まり、1 ユニットの壁時計の印だけが消えた（効果行・等級・判定は同じ）。巨大木 1 本は 3 回分の index で OOM（未測定）。壁時計に依存する印は設計上、決定論の対象にできない（`evidence/determinism_v2/README.md`） | 85 / 1 / 1 |

### 5.1 判別実験の結果（2026-09-20。#2 の規則を、結果を見た後に変えていない）

すべて D25（`2d981de`）後の解析器。木の対 7 = CVE 8（A9 と A10 が corpus を共有）。

**(a) 分子の照合（腕 C）**

| 列 | 値 | 備考 |
|---|---|---|
| 事前登録照合（主指標） | **7/8**（転記どおり）/ **8/8**（D1 どおり、#5） | 落ちたのは A18 の転記誤りだけ |
| 座標一致 | 8/8 | |
| any-change（旧） | 8/8 | 逆向き 4 対（A1/A2/A4/A10）と `open → read_text` の対も通す |
| 厳密 verdict-clearing | 0/8 | `GAP_SELECT` は値検証では消えない（従来どおり） |
| INJECT verdict-clearing | 1/8（A4） | 従来どおり |

逆向き 4 対と `open → read_text` の対は事前登録照合で**不通過**（`tests/test_two_sided_preregistered.py`）。

**(b) 等級潰し腕 C0 との差**

| 列 | 腕 C | 腕 C0 | C − C0 |
|---|---|---|---|
| 事前登録照合 | 7/8（8/8） | 6/8（7/8） | **{A10}** |
| 座標一致 | 8/8 | 7/8 | **{A10}** |
| any-change | 8/8 | 8/8 | ∅ |

A10 の差は `path` 3 位置の `req_val MODEL → OP`。C0 では**脆弱側も OP** になる
（脆弱側の `abspath + startswith` を「検証子あり」として OP に潰す = 二値モデルは
脆弱側を clear する）。`grade weak → strong-path` は両腕で残るので any-change では
差が出ない。A1 / A4 は脆弱側に検証子が無いので C0 は何も変えない。
**C − C0 = {A10} は事前登録照合と座標一致でのみ現れる。** 分子を (a) で直したことが
(b) の結果を作っている（(a) の分子は #2 で C0 を回す前に事前登録した）。

**(c) CodeQL `py/path-injection`**（`evidence/codeql_fair/`）

| 対 | 既定 source（#2 (c)） | 入口を揃えた source（#4） | 類型 |
|---|---|---|---|
| A1 | 脆弱 0 / 修正 0 | 脆弱 0 / 修正 1 | **第 4（被覆しない）**。修正側の 1 件は修正で足した `repo_path.resolve()` 自身が sink として報告されたもの（`Path.resolve` は CodeQL の path-injection sink）。CVE の sink（`git.Git.*` の `cwd`）は sink でない |
| A4 | 脆弱 0 / 修正 0 | 脆弱 1 / 修正 2 | **第 4**。同じく `.resolve()` 由来（A1 の修正が A4 脆弱側に既にある + A4 の修正で 1 件増）。`repo.git.add` の argv は sink でない |
| A9-A10 | 脆弱 2 / 修正 2（無関係な FastAPI 経路） | 脆弱 24 / 修正 24、**A10 の `write_file` 経路 8 件が両側で同一** | **第 3（修正側 clear 不能）**。`is_path_within_directory`（helper の `abspath`/`realpath` + `startswith`）を sanitizer と認識せず、脆弱側も修正側も報告する |

**判定規則（#2）の適用**

- 前提「`C − C0` に A10 が残る」: **成立**（事前登録照合・座標一致）。
- 枝 1「CodeQL が A10 脆弱側の `abspath + startswith` を clear する」: **不成立**（脆弱側を報告する）。
- 枝 2「`C − C0 = ∅`、または CodeQL も A10 を両側判別」: **不成立**（両側とも報告 = 判別しない）。

**規則はどちらの枝にも当たらない。** 第 3 類型（両側とも報告）を、規則を書いたとき
想定していなかった。post-hoc の読みは 2 つあり、**ここでは決めない**
（`docs/open_questions.md` O12、`docs/decisions.md` D26）:

- (α) CodeQL は修正を認識できず両側を報告する。等級づけは既存道具に無い判別
  （脆弱 = GAP、修正 = clear）を与える → 章に立てる側。
- (β) 規則が「章に立てる」条件として置いたのは「二値モデル / CodeQL が脆弱側を
  false-clean にする」ことであり、それは観測されなかった → 事前登録した形では
  示せない。降ろす側。

どちらの読みでも、**判別の根拠は較正対 1 対（A10）**である。#2 を書いた時点で
「A10 が等級だけで分かれた唯一の検証済み対」と記録しており、標本の小ささは新しい
情報ではないが、章に立てるならこの n = 1 を本文に書く。

### 5.2 `r_prev` の結果（2026-09-20、run2。規則 §2.7 は測定後に変えていない）

| 分母（§2.7 (f)、手順 1 で `ok` の 16 木） | 直前 | 5 リリース前（感度 (e)） |
|---|---|---|
| 危険ユニット（主） | **88.1%（133/151）** | 85.4%（129/151） |
| 全ユニット（粗） | 90.5%（910/1006） | 89.5%（900/1006） |
| distinct unit id（危険 / 粗） | 87.5% / 89.5% | 84.7% / 88.4% |
| 母集団別（危険） | app 83.3%、mcp_server 87.7%、tool_package 100% | app 79.2%、mcp_server 86.4%、tool_package 95.5% |

併記（事前登録した分母ではない）: 無条件（98 木を分母、前リリースの無い木を join
不可）で危険 23.1%（133/577）、全ユニット 34.7%（910/2621）。run1（as-run、#6 の
欠陥あり）は全体 64.2%、app 8.3%。

§10 の 3 連言（`r_D < 5%` ∧ `r_prev < 50%` ∧ validator 保有 < 5%）は**事前登録の
分母では不発火**（`r_D` のみ真）。併記の分母を 2 つとも採ると mcp_server と
tool_package で発火する。判定は `docs/decisions.md` D27、分母の選択は O7。

---

## 6. 未決（学生の判断が要る）

`docs/open_questions.md` の O7 を参照。要点のみ:

- 主分母の選択（§2.2）を承認するか。承認しない場合、`all_units` を主分母に
  据え置くか、別の分母にするか。
- §4 の「遡及しない」方針を承認するか。
- 論文で run6 の関門をどう書くか（× と報告し感度分析を付ける / 保留と書く）。
- §2.7 の `r_prev` 測定手続き。特に (d)「直前リリース」の定義と (f) の
  「前リリースにユニットが無い木を分母に入れる」判断。**後者は `r_prev` を
  下げる方向（自分に不利な側）**だが、下げすぎだと判断するなら別の扱いにする。
