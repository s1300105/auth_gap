# 決定した事項（根拠つき）

仕様書 `AUTHGAP_BRIEF_v3.md` の記述と実データが食い違った点、および仕様書が
決めていなかった点について、**実装側で判断して確定させた**内容を残す。
後から追認できるように、どの証拠でそう決めたかを必ず書く。

**仕様書本体は書き換えていない。** 仕様書は設計の記録として残し、
食い違いはここと `docs/cve_triage.csv` に併記する。

最終更新 2026-09-20（D22 を追加）。

---

## D22. D_prev 層の配線を通す（`r_prev` は測れない状態だった）

**本項は「直すと決めた」記録である。期待値は `tests/test_d_prev.py` に
修正より先にコミットした**（`CLAUDE.md` 規則 5）。結果は末尾の「結果」に追記する。

### 事実

仕様書 §10 の「**方向そのものを疑うべき条件**」は 3 つの連言である:

> 両母集団で `r_D < 5%` **かつ** `r_prev < 50%` **かつ** validator 保有 < 5%

`r_D` と validator 保有は run1〜6 で測られているが、**`r_prev` はどの run にも
出ていない**。理由は配線が 3 か所切れているからで、値が悪かったのではなく
**原理的に測れない状態だった**。

| # | 場所 | 状態 |
|---|---|---|
| 1 | `dparse.py: DPrev.load` | `units[i]["unit_id"]` を引くが、manifest の unit id は `units[i]["unit"]["unit_id"]` にある。自分の `scan` 出力を `--prev-manifest` に渡すと `KeyError: 'unit_id'` で落ちる |
| 2 | `report.py: probe_json` | `n_units_with_D_prev_join` が `0` の決め打ち |
| 3 | `scripts/f0a.py` | `r_prev` が存在しない（`grep -c r_prev` が 0） |

**1 は「自分の出力を自分で読めない」という形なので、この層は一度も通って
いない。** `grep -rn prev_manifest scripts/ tests/` の該当も 0 件だった。

### なぜ重いか

§10 は `r_prev ≥ 50%` のときのみ D_prev を主張に使うと定めており、分岐 3
（`r_D < 5%`）に落ちた母集団の fallback がここに乗っている。run6 は 3 母集団
すべてが分岐 3 なので、**fallback が成立するかどうかが未判定のままである**。

仕様書の前測では「静的に取得できるリリースが 2 本以上ある」のが 60 サーバ中
54 件 = 90.0%（**仕様書の値。本 repo では未追試**）なので、分母は十分あると
見込まれる。測っていないのは取得の問題ではなく実装の問題である。

### 決定

1. `DPrev.load` の join キーを manifest の実構造に合わせる。
2. `n_units_with_D_prev_join` を実際の join 数にする。
3. `r_prev` を `scripts/f0a.py` の `PopStats` に足し、§10 の他の率と**同じ分母**
   （`docs/preregistration.md` §2.2 の `dangerous_fp_excluded`）で出す。
   併記規則（§3）も同じく適用する。
4. そのうえで 2 リリースを取得して野外で測る。**取得手順と分母は
   `docs/preregistration.md` に先に書く**（後から分母を選べないようにする）。

**1〜3 は実装の修正であり、値を動かす意図は無い。** 現在の `r_prev` は
「未測定」であって「0」ではない。修正後に初めて値が出るので、
**その値を見てから分母や閾値を動かさない。**

### 結果

（修正コミットで追記する。）

---

## D21. Def 5 の値検証等級を 1 経路に統一する（両方向の誤りを直す）

**本項は「直すと決めた」記録である。期待値は `tests/test_value_grade.py` に
修正より先にコミットした**（`CLAUDE.md` 規則 5）。結果は末尾の「結果」に追記する。

### 事実（8 ケースで再現。`tests/test_value_grade.py` の fixture）

同一の Def 5 strong-path 条件を満たす検証子が、**書いた場所で等級が変わる**。

| ケース | 形 | 修正前の等級 | 修正前の verdict | Def 5 の期待 | 誤りの向き |
|---|---|---|---|---|---|
| a1 | inline `realpath` + `commonpath` | `weak(no_symlink_resolution)` | GAP_INJECT | `strong-path` | **false-dirty** |
| a2 | inline `Path.resolve` + `is_relative_to` | `weak(no_symlink_resolution)` | GAP_INJECT | `strong-path` | **false-dirty** |
| a3 | inline `realpath` + `startswith(base+os.sep)` | `weak(prefix_no_canon)` | GAP_INJECT | `strong-path` | **false-dirty** |
| b1 | helper が `realpath(root)` だけ通し、検査対象も sink も生の `path` | **`strong-path`** | **なし** | `weak(no_symlink_resolution)` | **false-clean** |
| b2 | `join(realpath(ROOT), path)` | `weak(prefix_no_canon)` | GAP_INJECT | weak | 正しい |
| b3 | 正規化した値を使わず生の値を sink へ | `weak(prefix_no_canon)` | GAP_INJECT | weak | 正しい |
| c1 | 検証なし | `None` | GAP_INJECT | `None` | 正しい |
| c2 | 付録 G `_prelude.validate_path` と同じヘルパー形 | `strong-path` | なし | `strong-path` | 正しい |

**b1 が最も重い。** `_validate_root_only` は `os.path.realpath(root)` しか通さず
`os.path.commonpath([path, base])` で**生の `path`** を照合するので
`/srv/data/../../etc/passwd` がそのまま通るが、現行の解析器はこれを clear する。

### 原因

Def 5 が 1 つなのに、実装が**互いに矛盾する 2 つの近似**になっている。

1. **inline 経路** `gate.py: _call_candidate` は形状 1 つを
   `_grade_from_shape` に渡し、docstring どおり「単独で strong にはしない」ので
   **構造的に weak 止まり**。囲み関数の本体をまとめて採点する経路が無い。
2. **helper 経路** `gate.py: _value_grade` は本体に現れた正規化子名の集合
   （`_transform_names`）と包含述語名の集合（`_containment_forms`）の**積**だけで
   strong-path を返す。どの値に適用されたかを見ない。
3. `analyze.py: _grade_of` は `value_grade.startswith("strong")` なら即 return し、
   `Value.attrs` も `ValResult.alias_facts` も参照しない。
   `validators.py: strong_path_requirements` と `ROOT_EQUAL_STEPS` は
   **定義のみで呼び出し元が 0 件**である。

**val は既に必要な証拠を出している。** `TRANSFERS` は symlink 解決子に
`canon_class="symlink"` と `attrs=("canonicalised",)` を持ち、
`engine.py` は `(root, site, transform)` を `alias_facts` に記録している。
**gate 側がそれを読んでいないだけである。**

### 決定

**strong-path を返す前に val の証拠で裏づける。** 判定を 1 か所に集約する:

* 条件 1（canonical alias の存在）= `alias_facts` に
  `root ∈ value.roots` かつ symlink 系 transform の行があること。
* root-equal = sink に届く値そのものが `canonicalised` 属性を持つこと。

この 2 条件は 8 ケースすべてを正しく分離する（b1 は canon 属性を持たず、
b2 は root `path` の alias を持たない）。**symlink 系 transform の集合は
`TRANSFERS` の `canon_class == "symlink"` から導出し、新しい語彙を作らない。**

inline 経路は `_grade_from_shape` をやめ、囲み関数の本体に対して helper 経路と
同じ採点を行う。**inline を strong に到達可能にするのは false-clean 方向の変更
なので**（`CLAUDE.md`）、上の 2 条件による裏づけと敵対的レビューを必須とする。

### 結果

（修正コミットで追記する。）

---

## D20. `validator_holding_ratio` の分母を `docs/preregistration.md` で固定した（遡及させない）

- **いつ決めたか（正直に書く）: run6 の点推定と区間を見た後。** さらに
  「分母を変えると関門が反転する」ことを実測した後である。D18 と同じく、
  この順序を隠さずに書く。
- **事実**: 仕様書 §10 は `validator_holding_ratio` に閾値 5% を置くが
  **分母を書いていない**（:1101、:1143）。実装 `scripts/f0a.py:180` は
  `n_with_validator / n_units`（全ユニット）を採るが、根拠はどこにも無い。
  一方、仕様書 §6 の指標表は D 層別存在率について
  「分母は危険効果を持つユニットで、偽陽性クラスを除いた値と粗い値の両方を出す」、
  §10 は「分母はすべて危険効果を持つユニットであり、ツール全体ではない」と明記する。
  **`validator_holding_ratio` だけがこの原則の外にある。**
- **実測（`.venv/bin/python scripts/denominators.py evidence/f0a_run6`）**:
  ユニット分母 3 種 × パス分母 2 種 × 母集団 3 = 18 セルのうち、
  **関門 ≥5% に落ちるのは 2 セルだけ**（`all_paths × all_units` の mcp_server 4.43%、
  tool_package 3.26%）。残る 16 セルは通過する。公表済みの「関門 ×」は
  **最も分母が大きい 1 通りで計算した値**である。

**決定:**

1. **解析器の修正を先に行う。** 等級づけ（strong-path 判定）が両方向に壊れている
   間は validator の数を数え直しても意味が無い。修正の内容は別途。
2. **両側通過率の分子**（`expected_tuple_change` との照合が無い）は分母の問題では
   ないが同類型なので、同じ時期に手当てする。
3. **標本の拡大は (1)(2) の後。** 壊れた物差しで木を増やさない。
4. **分母の定義を `docs/preregistration.md` に固定した。** 主分母は
   `dangerous_fp_excluded × all_paths`、6 通りすべてを併記する。
   **ただしこれは「実装側の案」であり、学生の承認待ちである**
   （`docs/open_questions.md` O7）。選択が関門の合否を反転させる方向にあるので、
   実装側で黙って確定させない。

**遡及させない理由（この決定が判定を有利にしない理由）:**

主分母 `dangerous_fp_excluded` の根拠は仕様書の明文の原則であって観測値ではない。
しかし**選択が関門を × → ○ に反転させると知った後の選択**である以上、
その反転を「関門を通過した」という主張に使ってはならない。したがって:

- run6 の関門判定は公表済みのまま据え置く。`docs/f0a.md` / `docs/f0a_ci.md` /
  `docs/f0a_run*.md` の数値と判定は**書き換えない**。
- 新分母での値は「分母を変えるとこうなる」という**感度分析**として報告する。
- 関門の再判定は、preregistration.md のコミット後・(1)〜(3) の後に取る run で行う。
- §10 A5 の対処（validator 保有 < 5% → クラス 2 は T1+T2 のみ）は
  **その再判定まで保留**。run6 の × を根拠にクラス 2 を落とさないし、
  新分母の ○ を根拠に維持するとも主張しない。

**仕様書は書き換えていない。** §10 が分母を書いていないという事実はそのまま残し、
埋めた内容を preregistration.md に置いた（`CLAUDE.md` 規則 6）。

---

## D1. 語彙を拡張した（形状 11→12、weak 理由 19→22）

**月 6 の凍結前なので逸脱ではない。** 凍結後に動かす場合は
`docs/preregistration.md` に逸脱として記録すること。
実装の記録は `authgap/catalog/validators.py: VOCABULARY_REVISIONS`。

| 追加 | 何 | なぜ |
|---|---|---|
| 形状 | `absolute`（`os.path.isabs` / `Path.is_absolute`） | §2.6 の fixture F7 が `absolute_only` を weak 理由として要求しているのに、絶対パス検査を形状として数える語が無かった |
| weak | `absolute_only` | 同上。絶対パス検査だけの検証子が `unknown`（判定不能）に落ち、weak と区別できなかった |
| weak | `existence_only` | 同上（F7 が名指ししている） |
| weak | `statement_type_only` | **A18（langroid）で実際に当たった。** 修正は `sqlglot.parse` で正規化してから**文型**の allowlist を掛ける。値そのものは自由な SQL のままなので strong ではなく、拒否リストでもないので `denylist_enum` でもない。既存語彙のどれにも当たらず `unknown` になっていた |

witness も同時に足した（`WITNESS_TEMPLATES` は全 weak 理由を覆う。テストで固定）。

**Def 5 が「19 語」と書いている箇所は、この改訂後は 22 語として読む。**

## D2. 付録 G の G12 の reason は `deny_reaches_effect`

- 仕様書の付録 G は G12 の期待を `NODOM` とだけ書き、reason クラスを書いていない。
  §2.5.6 B3b は 3 つ組一致を要求するので空にできない。
- **導出**: 承認の拒否辺は `finally(exc)` 複製へ入り、その複製が効果そのものなので
  `d ∈ Reach(s)` が成り立つ。
- あわせて、実装変異 `no_finally_copies` が生存する件も確定させた:
  - 付録 G の 15 件は `finally` 複製の有無を判別しない（G12 で効果行に対応する
    CFG ノードは 2 個対 1 個になるが、3 つ組は一致する）。`(G-i)∧(G-ii)` が
    先に同じ誤りを捕まえるため。
  - **生存数は 1/15 のまま報告する。** §2.5.6 の定義どおり、生存数は付録 G と
    支配 mutant の fixture テストだけで数える。
  - ただし複製の性質そのものは `tests/test_cfg_structure.py` で構造的に固定した。
    **この単体テストは生存数の計算に入れない**（入れると定義が変わる）。

## D3. §8-7: in-tree の露出宣言を D_op に**含める**

- Def 6 の D_op 節の条件をそのまま課す — `enabled=` の式が真偽 config atom に
  解決でき、**かつ atom の既定が閉**のときのみ D として読む。既定が開なら
  `D ⊭ e` 側に倒し、解決できない式は `opaque` として記録して**どちらにも数えない**。
- 前測の実使用は 0 件なので数値影響は無い見込みだが、§8-7 は「含めるか否かを
  先に決める」ことを要求しているので既定を明示した。
- 実装: `authgap/dparse.py: INCLUDE_IN_TREE_EXPOSURE = True` と
  `in_tree_exposure` / `exposure_as_d_op`。

## D4. A1 / A2 の期待タプルは測定値を採る

- 一次確認の結果、仕様書 §6 T1.2 の**脆弱側**が 2 件とも誤っていた。

  | 対 | 仕様書 | 一次確認した実際 |
  |---|---|---|
  | A1 | `weak(prefix_no_canon)` | **検証子が 1 つも無い**（`Path(arguments["repo_path"])` が直接 `git.Repo` へ） |
  | A2 | `weak(no_dash_reject)` | **検証子が 1 つも無い**。さらに仕様書は `git_checkout` しか挙げていないが `git_diff` も同じ修正を受けている |

- **`docs/cve_triage.csv` の `expected_tuple_change` を採点前の凍結値とする。**
  仕様書の値は同じ行の `spec_expected_tuple_change` に残す（監査用）。
- 両側判別可能性は変わらず成立するので §6 T1.5 の算入数は動かない。
  消滅理由は A1 が `normalisation-add` 単独ではなく `validator-add` を含む。

## D5. セレクタ（`req_occ` の主語）の運用定義

Def 5 は「ディスパッチキー（セレクタ）そのものを主語とする allowlist」としか
書いていないので、機械的な決め方を次で確定した。

1. 被呼び出しが `Subscript`（`TOOLS[name](args)`）なら添字がセレクタ。
2. ユニット本体で dispatch キーの位置に現れる式（`REGISTRY[x]` / `X.get(x)` /
   `if x == "..."` / `match x:`）の名前を val の env で root へ写す。
3. どちらも取れなければ、ユニット入口の仮引数のうち効果の実引数に現れないもの。

3 は暫定だが、G11（主語不一致 → `non_binding_gate`）と G15（`dispatch(name, argstr)`
から `git_log(argstr)` を直接呼ぶ形で `name` がセレクタ）の両方を満たす最小の規則である。

## D6. 主語一致は root で取る

- `Value.roots`（MODEL 導入点の集合）を主語一致の照合に使う。root は名前の
  書き換え（`safe = validate_path(path)`）を跨いで保たれるので AST 名の一致より正確。
- 添字は root を精緻化する（`arguments["repo_path"]` と `arguments["target"]` を
  同じ root に潰さない）。**潰すと片方への検証が他方の位置に付く**（Def 5 が
  禁じている型エラーが主語一致をすり抜ける）。
- 付録 G のハーネスだけは名前一致に落ちる（val を走らせずゲート層だけを試す
  ためで、期待値は 15/15 で通っている）。

## D7. §8-1 の (d)（SELECT 格下げ分岐）は承認を要さない

§3 と §10 が「この条項は撤回しない」と書いているので、指導教員の合意事項では
なく**仕様内規則**として扱う。拒否分岐は作らない。

## D8. config atom は 4 源すべてを読む

Def 5 の 4 源（コンストラクタ kwarg / モジュール定数 / `os.environ` /
CLI オプションの既定値）を `authgap/atoms.py` で実装した。

- **同じ名前で既定値が食い違うときは解決しない**（`AMBIGUOUS`）。推定で片方を
  採ると既定閉と既定開を取り違え、`req` を誤って引き上げる（false-clean 方向）。
- pydantic の `Field(default=...)` は読むが `default_factory=` は読まない
  （値が静的に決まらない）。

## D9. 低レベル MCP の `trig` は `traced`（測定）

仕様書 §3 / §10 は「MCP サーバでは dispatch が framework 内にあるので trig は
常に `assumed`」と書くが、**低レベル経路では `traced` になる**。

| 登録形 | trig | 測定した木 |
|---|---|---|
| 低レベル `@server.call_tool()` | **traced** | mcp-server-git（3/3 ユニット） |
| 高レベル `@mcp.tool` | assumed | langroid 同梱の MCP fixture |
| `@command(名前, 説明, {スキーマ})` | assumed | AutoGPT |
| `tools=[f, g]` の裸の関数 | assumed | PraisonAI |
| `ToolMessage` 派生 + 同名ハンドラ | assumed | langroid |

影響:

- §3 の「MCP サーバだけにすると交差行は fixture からしか出ない」は
  **高レベル経路についてのみ正しい**。
- §10 の B1 関門「T3-app の traced 率 ≥ 20%」は、低レベル MCP サーバ自体が
  traced ユニットを供給するので T3-app に頼らず満たせる可能性がある。
- **`traced_ratio` は母集団別（低レベル / 高レベル / ツールパッケージ）に出す。**
  1 つに平均するとこの構造差が消える。

## D10. 交差行は低レベル MCP からしか出ない → §3 は現時点で不合格

- 4 プロジェクト 7 木で測って交差行 12 行、**すべて mcp-server-git 由来 = 1
  プロジェクト**。§3 は「3 行が異なるプロジェクト由来」を要求するので不合格。
- AutoGPT が 0 行なのは**正しい**。ディスパッチは
  `agent.command_registry.get_command(command_name)` で `self.commands` は
  実行時に埋まる辞書なので、Def 4 の `OPAQUE(dynamic_registry)` に当たる。
  推定で候補を埋めてはならない。
- **決定**: 高レベル登録形をいくら足しても交差行は増えないので、C1 の標本設計で
  **低レベル MCP サーバを意図的に含める**か、§3 の「統一の証拠は逸話的」／
  「三部品として報告する」分岐に入るかを、**標本抽出の前に**決める。
  抽出後に決めると事後選択になる。

## D11. `verdict-clearing` は 2 通り出す

§6 T1.1 の副次指標は「修正版で verdict が GAP から外れる対の数」だが、
実データでは厳密版がほぼ常に 0 になる。理由は `GAP_SELECT` が
「モデルがそのツールを呼ぶかを決めており、承認割り込みも宣言も無い」ことを
言うので**値検証を足しても消えない**から。

したがって次の 2 つを**必ず並べて**出す（`scripts/two_sided.py`）。

- `pair_cleared`（厳密）: 変化した経路に GAP が一切残らない
- `pair_cleared_inject`: 変化した経路に `GAP_INJECT` が残らない

**片方だけを書くと、SELECT 座標が常に残ることを隠すか、値検証の効果を
見落とすかのどちらかになる。**

## D12. R2 カタログに 4 形を追加した

較正対がそれ無しでは入口 0 件になるので、Def 2 の R2 カタログを拡張した。

| 追加 | 形 | 必要だった対 |
|---|---|---|
| `autogpt` | `@command(名前, 説明, {スキーマ}, ...)` | A5 |
| `langroid` | `ToolMessage` 派生の `request` と同名のハンドラ | A18 |
| `tools-list` | `tools=[f, g]` / `tools=["f","g"]` / `def get_*_tools(): return [f, g]` | A9 |
| （既存の精密化） | `@command` のスキーマ辞書のキーに無い仮引数は MODEL としない | A5（`agent` を MODEL にしない） |

**限界（2026-09-14 追記）: `tools-list` 形は呼び出しの `tools=[...]` キーワードを
すべて手がかりにするので、登録ではない呼び出しも拾う。** 野外の w-giak__mnemo-lite は
`logger.info("...registered", tools=["get_indexing_errors", ...])` とログにツール名を並べて
おり、これが入口の手がかりになった。そこに並ぶのが本当に登録済みのツールなら被害は
重複だけ（同じ関数が `mcp` と `tools-list` の 2 ユニットになる欠陥。修正待ちで
`tests/test_f0a_defects.py` 12 節に固定）だが、無関係な関数名を並べれば誤った入口になる。
呼び出し先を Agent / Crew などに限る案は、F0a の標本を見た後にカタログを絞ることになるので
採らず、この広さを限界として報告する。

**スキーマ辞書による除外は名前のブラックリストより強い根拠である**
（フレームワークが機械可読に「モデルが埋める引数」を宣言しているため）。
`@click.command()` と末尾名が同じなので、位置引数 3 個と第 1 引数が文字列定数で
あることを構造条件にして分けた。

## D13. Semgrep baseline は強化してから比べる

- **弱い baseline は AuthGap を実際より良く見せる。** 最初のルールは
  R2 デコレータの引数しか source にしておらず、mcp-server-git のような
  低レベル経路で所見 0 になっていた（比較が成立しない）。
- 強化した内容: 低レベル MCP ハンドラの `arguments` を source に追加、
  GitPython の proxy 形を sink に追加、過剰一致していた `$S.run(...)` を削除。
- **結果は変わらなかった**（AuthGap 7/7、Semgrep 0/7）。強化前後で同じ結論に
  なったこと自体が、結論が baseline の弱さに依存していないことの根拠になる。
- **増減を分けて報告する。** 「所見の集合が変わったか」だけで数えると、
  修正でコードが増えて所見が増えた対（A9）が「両側通過」になり、baseline が
  修正を検出したように見える。`two_sided_pass_by_disappearance` を主指標にする。
- §6 T1.5 (ii) は Semgrep と Pysa の両方を要求する。**Pysa は未実施**
  （pyre 環境の構築が要る）。§6 は「D13 までに環境が立つ repo が 0 なら
  baseline から落として『pyre 依存 baseline は環境コストにより不成立』と
  報告する」としている。

## D14. F0a は「直す前の解析器」で 1 回測り、直したら run を分けて両方出す

**状況。** 野外 3 木の煙試験で効果サイトが 21/21 `opaque` になった。原因の候補は
モジュール大域の名前（`github_client = GitHubClient(...)` のような木内の束縛）を
val エンジンが読まず `opaque(unresolved)` にしていること。Def 4 は
`opaque(unresolved)` を「**木内で解決できない**呼び出し」に限っており、
config atom の源にモジュール定数を数えている（§2.3）ので、仕様より弱い実装である
可能性が高い。一方で §10 は `in_tree_resolution_ratio < 50%` なら母集団を
切り替えると定めており、**実装の弱さが母集団の性質として報告されうる。**

**決定。**

1. **run 1 = `authgap/` が commit `9c2bb11` と同一の解析器で F0a を測る。**
   実行時の HEAD は `730c948`（スクリプトと文書だけが違う。
   `git diff 9c2bb11 730c948 -- authgap` は空）で、これが
   `evidence/f0a/f0a.json` の `run_meta.analyzer_commit` に入っている。
   関門の判定はまず run 1 で出す。
2. run 1 のユニット行を**読む前に**、検証標本の抽出手続き
   `scripts/sample_f0a_checks.py`（seed 20260914、6 層、効果サイトは
   (木, relpath, lineno, kind) で重複除去）をコミットする。検証対象を結果を
   見てから選ばないため。
3. 標本の各件を原ソースに当てて「木内で解決できるのに opaque」「本当に
   解決できない」などに分類し、**解析器の欠陥として数えたものだけ**を直す。
   直したら run 2 を取り、**run 1 と run 2 を commit で区別して両方報告する**。
   関門を通すために直したと読まれうるので、片方だけを出さない。
4. **ゲート語彙（weak 理由・strong の定義・OPAQUE/NODOM）には触らない。**
   held-out G16–G20 は F0a コーパスから seed 付きで抽出する規定（§2.5.7）なので、
   F0a の木を見てゲート語彙を動かすと held-out が汚れる。val エンジンの名前解決は
   ゲート語彙ではない。
5. 検証標本の分類は**機械による事前点検であり C2 のラベルではない。**
   論文に載せる検証は学生が `docs/verification_guide.md` の手順で行う。

## D15. §10 の解決率・opaque 率は「効果サイト」単位で判定し、行単位を併記する

**決めた時点: 野外 run 1 の結果を 1 件も見る前**（煙試験 3 木のみ）。

- **食い違い。** §1 は `in_tree_resolution_ratio` を「**効果サイト**の解決率」と
  書くが、実装（`report.py` の probe と `f0a.py`）は**効果行**を数えていた。
  効果行は呼び出し経路ごとに複製される（§2.6「指数項は出力側に現れる」）。
  煙試験では 1 サイト（`github_client.py:82`）に 21 行が集中しており、行で数えると
  そのサイト 1 つの確度が母集団の率をほぼ決める。
- **決定。** 関門の判定は仕様の文言どおりサイト単位（(木, relpath, lineno, kind)
  で重複除去）で行う。opaque 率も同じくサイト × slot 単位。**行単位の値も必ず
  併記する**（`f0a.json` の `*_sites` と無印の両方）。
- **同一サイトに異なる確度の行があるとき**は `prov_merge` と同じ
  `opaque > remote > resolved` で合流する。**1 経路でも opaque ならそのサイトは
  opaque**（resolved を優先すると無言の false-clean になる）。
- **この決定は結果を見る前に固定したので、結果によって行 / サイトを選び直さない。**

## D16. 野外 run 2 以降は解析器を Python 3.12 で走らせる（run 1 の 3.10 は残す）

- **状況。** run 1 の parse 失敗 91 ファイルのうち 67 件は PEP 695（`type X = ...`、
  `def f[T]`）と PEP 701（f-string 内の同種引用符）で、**解析器を 3.10 で走らせて
  いるから読めない**だけだった（`uv python find 3.12` の 3.12.13 で再 parse すると
  全件 parse できる。`evidence/f0a/parse_failures.json` の `parses_in_newer_python`）。
  野外の MCP サーバは新しい Python で書かれていることが多く、この損失は偏りを持つ
  （新しいコードほど落ちる）。
- **仕様との関係。** §5.3 は「**Python 3.10+**」であり、3.12 で走らせるのは仕様内。
  前身の実測が 3.10.12 だったのは前身の事情。
- **3.12 に替えても較正結果が変わらないことを確かめた**（2026-09-14、`authgap/` は
  commit `9c2bb11` と同一）:

  | 確認 | 3.10.12 | 3.12.13 |
  |---|---|---|
  | B3a 支配 mutant | 8/8 | 8/8 |
  | B3b 付録 G | 15/15 | 15/15 |
  | 実装変異の生存 | 1/15 | 1/15（同じ `no_finally_copies`） |
  | pytest | 70 passed | 70 passed（`-W error::DeprecationWarning`） |
  | 両側条件 | 7/7、厳密 0/7、INJECT 1/7 | 同じ |
  | `scan corpus/A1__fixed` の 4 出力 | — | volatile を除いてバイト同一 |

- **決定。** run 2 以降は `.venv312`（`uv venv .venv312 --python 3.12`）で走らせ、
  `run_meta.python` に版を記録する。**run 1（3.10）はそのまま残し、run 2 と並べる。**
  run 1 と run 2 の差には「解析器の修正」と「処理系の変更」が混ざるので、
  **処理系だけを替えた run（解析器は run 1 と同一）も取って差を分解する。**
- **3.12 でも読めない 18 件**（雛形 5、壊れたファイル 13）は parse 失敗として残る。

## D19. レビューと修正の繰り返しを止める条件（F0a に使う解析器の凍結）

- **いつ決めたか: 4 回目のレビュー（ea35672 の差分）を走らせる前。** 結果を見て条件を
  選び直さないため、ここに先に書く。
- **状況。** F0a run 1 の後の解析器の修正は、敵対的レビューのたびに新しい欠陥が見つかった
  （1 回目: 確認 8、2 回目: 確認 5、3 回目: 確認 6。棄却はいずれも 0）。多くは「解決を
  増やす修正」が作った false-clean で、深刻度は回を追って下がっているが 0 にはなっていない。
  止める規則が無いと、関門の数字を好きな回で止めて選べてしまう。
- **決定。**
  1. **凍結の条件:** 直前の修正の差分だけを対象にしたレビューで、**false-clean・効果行の
     消失・クラッシュの向きの確認済み指摘が 0 件**になったら、その解析器を F0a の報告に使う
     版として凍結し、`fingerprint` とタグを付ける。
  2. **精度の損失（誤警報の向き、opaque を増やす向き）の指摘は凍結を妨げない。** 限界として
     件数と形を記録し、報告の前には直さない（直すと解決を増やす変更になり、再びレビューが要る）。
  3. **上限:** 4 回目のレビューで上の向きの指摘が確認されたら、テストを先に固定して直し、
     その差分だけを 5 回目のレビューにかける。**5 回目でもなお確認されたら、繰り返しを止め、
     残った指摘を向きと件数つきで既知の欠陥として報告する**（直した版の run は取るが、
     その版を「欠陥が無い」とは書かない）。
  4. **各回の run を残す。** run 2〜5 はそれぞれ、どの指摘で中間状態になったかを
     `docs/f0a_runs.md` と `verification_guide.md` §3.2 に書く。関門の数字は凍結した版の run の
     ものだけを使い、区間（D18）を併記する。
- **この規則の限界。** 敵対的レビューで指摘が 0 件でも欠陥が無いことは示せない。凍結は
  「この手続きで見つからなかった」ことの記録であり、論文にもそう書く。

### D19 の結果（2026-09-14）: 凍結しない。150e06a（run 6）を、既知の欠陥を明記して報告に使う

- **4 回目のレビュー**（ea35672 の差分、`wf_0befeae9-69c`）: 確認 6・棄却 0、6 件すべて凍結を妨げる向き。
  D19(3) により、テストを先に固定して直した（D17 改訂 5、150e06a）。
- **5 回目のレビュー**（170a7b2..150e06a、`wf_bca6c11f-6f1`、3 観点）: 指摘 4・確認 4・棄却 0。
  4 件すべてが凍結を妨げる向き（false-clean 1、効果行の消失 3。うち 2 件は同じ欠陥 K1 を 2 観点が
  独立に指摘）。精度の観点（run 5 と HEAD の実データ比較）は指摘 0。
- **D19(3) により繰り返しをここで止め、直さない。** `scripts/freeze_f0a.py` は走らせない（確認済み指摘が
  0 でないときは exit 3 で拒む設計）。タグも打たない。run 6 は「この手続きで欠陥が見つからなかった版」
  ではなく、**「5 回目のレビューで下の既知の欠陥が確認された版」**として報告する。

**既知の欠陥**（`tests/test_f0a_defects.py` 15 節の `KNOWN` 印。直したら XPASS で知らせる）:

| id | 形 | 向き | いつから | 出所 | F0a 標本 98 木の構文上の候補 |
|---|---|---|---|---|---|
| K1 | spawn の argv0 がモジュール水準のリスト、または shell= が `global` で書き換えられる名前のとき、`_pipe` が判定できないのに FS_WRITE の側だけを出し、pipe 書き込みの EXEC(code_text) 行が消える | 効果行の消失 | 改訂 5 の退行（170a7b2 は EXEC） | 5 回目（2 観点が独立に指摘、検証者が再現） | 0 |
| K2 | 関数内の `global run_command` と入れ子 def で書き換えられる名前を、モジュール直下の安全な def に resolved で決め打ちする | false-clean | 改訂 5 の退行（170a7b2 は行 0 / opaque） | 5 回目（検証者が再現） | 0 |
| K3 | 同じく関数内の `global run_command; run_command = f`（代入） | false-clean | 改訂 5 より前 | 5 回目の指摘者が件数上限の外として挙げた形。150e06a と 170a7b2 を自分で走らせて再現 | 0 |
| K4 | メソッドの中の入れ子 def と同名の、モジュール直下の def に決め打ちする（入れ子 def に classname が付き候補から外れる） | false-clean | 改訂 5 より前 | 同上 | 0 |
| K5 | 囲む関数の局所 import と同名の、モジュール直下の def に決め打ちする | false-clean | 改訂 5 より前 | 同上 | 0 |
| K6 | 3 段入れ子のモジュール水準 dict の要素に tool が書き込む URL が、`_opaque_deep` の深さ上限（2）を超えて url.host = OP / resolved になる | false-clean | 改訂 5 より前 | 同上 | 0 |
| K7 | 別名つき from-import（`from .net import fetch_url as http_get; http_get(url)`）で木内の関数へ降りず、被呼び出しの効果行が全部消える。import 表は `pkg.net.fetch_url` を正しく引くが、定義を探す名前に呼び出し式の局所の別名を使う（`_resolve_in_tree` の `last`） | 効果行の消失 | 最初の解析器の commit から（検証者が 04e5f9b / 0662b39 / 170a7b2 / 150e06a で確認） | 5 回目（検証者が再現） | **32 木・693 箇所**（mcp_server 23 木 469、tool_package 5 木 86、app 4 木 138） |

候補の数え方は `scripts/scan_known_defect_forms.py`（構文だけの走査。K1〜K6 は検証用の 7 fixture をすべて検出し、
K7 は別名ありの 2 形を検出して別名なしの対照を検出しないことを確かめてから標本に当てた）。**K7 の数は、
テスト・スクリプトを含み、ユニットから到達するかを見ていない上限値である。** K1 / K2 は改訂 5 で出力が
変わる形なので、run 5 と run 6 のバイト一致とも整合する。

**K7 は run 6 の数字に効いている。** 検証者は、run 6 で w-datawhalechina__video-devour の 5 ユニットすべてと
w-saiyandev17__agent-sentinel の 23 ユニット中 21 が効果 0 件であり、別名の元の名前で定義を引く実験パッチ
（コミットしない）でそれらに FS_READ / DB / NET の行が現れることを示した。影響の大きさは下の感度分析で
見積もるが、**感度分析の数字は関門の数字として使わない**（D19 の順序を守る）。K7 を直して run 7 を取るかは
D19 を破る判断になるので、学生に委ねる（`docs/open_questions.md` O6）。

**K7 の感度分析（関門の数字ではない）:** 150e06a の `git archive` に 3 行の実験パッチ（呼び出し式の局所の別名では
なく、import 表が指す元の名前で定義を引く。`evidence/f0a_sens_k7/sensitivity_patch.diff`。**コミットしない**）を
当て、run 6 と同じ標本・上限・処理系（3.12.13）で F0a を取った（`evidence/f0a_sens_k7/`。archive なので
`analyzer_commit` は null。`authgap/` の差がこのパッチだけであることは 150e06a の全ファイルとの `cmp` で確かめた）。
走らせる前に、パッチが別名あり 2 形の fixture で NET 行を出し、別名なしの対照を変えないことを確かめた。

| mcp_server（60 木） | run 6 | 感度分析 |
|---|---|---|
| 危険効果を持つユニット（偽陽性クラス除外） | 431 | 457（+26。すべて効果 0 件だったユニット） |
| 効果サイト / 効果行 | 444 / 1251 | 460 / 1405 |
| `in_tree_resolution_ratio_sites`（関門 ≥ 50%） | 33.6% [18.6%, 51.3%] ×（境界） | 32.6% [18.0%, 49.5%] ×（区間も閾値の下） |
| `opaque_ratio_primary_slots_sites`（関門 ≤ 40%） | 43.5% [20.8%, 68.0%] ×（境界） | 44.1% [22.2%, 68.1%] ×（境界） |
| `validator_holding_ratio`（関門 ≥ 5%） | 4.4% [2.4%, 7.4%] ×（境界） | 4.4% [2.4%, 7.4%] ×（境界） |

- 変わったのは mcp_server の 6 木・47 ユニット行だけで、tool_package と app は全指標が同一。効果行の消失 0、
  危険効果から外れたユニット 0（`lost_units.py evidence/f0a_run6 evidence/f0a_sens_k7`、およびユニットの重複キーを
  考慮した行単位の突き合わせの両方で確かめた）。
- 構文上の候補（mcp_server 23 木）より実際に変わった木（6 木）が少ないのは、候補にユニットから到達しない
  呼び出し（テスト・スクリプト・CLI）が多いため。
- **K7 は mcp_server の効果サイトを 16（感度分析の 3.5%）少なく数え、危険効果を持つユニットを 26（同 5.7%）
  見落としていた。** 関門の判定（点推定の ○ / ×）は変わらないが、解決率の区間は「境界」から「閾値の下」に移る。
  **run 6 の数字を書くときはこの表を併記する。**
- 区間は `scripts/f0a_ci.py` の `per_tree` / `bootstrap`（seed 20260914、2000 回）を感度分析の証拠に当てて求めた
  （`docs/f0a_ci.md` には入れていない。関門の表と混ぜないため）。

**別に見つかった記録事項:** run 6 の `units.jsonl` には、(母集団, 木, `unit_id`) が同じで中身の違う行が
194 キー・234 行ある（例: w-eggressive__mcp-build の `mcp:get_weather:985793b628ca` が 3 行）。`unit_id` は
木の中で一意ではない。キーで辞書を作る突き合わせは重複行を潰すので、上の突き合わせは位置を揃えて行ごとに
比べ直した。`scripts/lost_units.py` はユニットを (母集団, 木, `unit_id`, relpath, 入口の行) で識別しており、
このキーでは run 6 と感度分析の証拠のどちらにも衝突が 0 件なので、`lost_units.py` の結果はこの重複の影響を
受けない。**`unit_id` 単独で行を突き合わせる新しいスクリプトを書くときは、relpath と行をキーに含める。**

**手続きの限界として書くこと:** 確認件数は 8 → 5 → 6 → 6 → 4 で、0 に近づかなかった。回ごとの指摘の多くは
直前の修正が作った退行だったが、K7 のように**最初からあって影響の大きい欠陥が 5 回目で初めて見つかった。**
各回のレビューは直前の差分に焦点を当てたので、差分の外にある欠陥を系統的には拾わない。

## D18. §10 関門の率には木単位のブートストラップ区間を併記する（判定は点推定のまま）

- **いつ決めたか（正直に書く）: run 2 の点推定を見た後。** run 2 で mcp_server の
  `in_tree_resolution_ratio_sites` が 51.0%（閾値 50% の 1 pt 上）、tool_package が
  49.5%（0.5 pt 下）になった。60 木 / 30 木の標本で、サイトは木に集まる（1 木に数十
  サイト）ので、この差を合否として読める精度が無い。
- **決定。** `scripts/f0a_ci.py` で、抽出単位の**木**を復元抽出するクラスタ・
  ブートストラップ（seed 20260914、2000 回、パーセンタイル 95%）の区間を付ける。
  **関門の判定規則（§10 の点推定と閾値）は変えない。** 区間が閾値を跨ぐものは
  「境界」と書き、**点推定だけで「関門を通過した」「通過しなかった」と主張しない。**
- **この決定が判定を有利にしない理由。** 区間は判定を変えず、「○」を「境界」に
  格下げする方向にしか働かない。区間を見て閾値や分母を選び直すことはしない。
- run 1 / run1py312 / run 2 すべてに同じ手続きを当てる（`docs/f0a_ci.md`）。
- **run 2 の `run_meta`**: `analyzer_commit` は実行終了時の HEAD（`d6b608c`）だが、
  `authgap/` は `0662b39` と同一（間のコミットはスクリプトと文書だけ）。標本は
  訂正前（`b3aa2c8` の `corpus_sample.json`。run 2 は開始時に読み込んだ後で標本を
  引き直した）。run 2 以降は `sample_sha256` で内容を記録する。

## D17. 事前点検の所見のうち「直すもの」と「直さないもの」

根拠: `docs/f0a_checks.md`（`evidence/f0a/check_results.json`）。**点検者の
analyzer_wrong をそのまま欠陥と読まない。** 仕様の定義に照らして振り分けた。

**直す（仕様がすでに要求している挙動、またはカタログにある形の取りこぼし）:**

| 所見 | 誤りの向き | 仕様の根拠 |
|---|---|---|
| `list.append` 等を受け手への書き込みとして扱わない（RES[7]） | **false-clean** | §2.6「決して clean に潰さない」 |
| 受け手型が付かず sink を落とす: 局所変数の `Path`、callee クラスの `__init__` で束縛した `self` フィールド、木内関数の戻り値注釈、クロージャ変数（NOE[1,4,6,10,11]） | **false-clean** | §2.6 の heap / Obj.fields / 受け手アクセスパス |
| 受け手型なしで末尾名が唯一の関数へ解決する（EFF[6]） | false-alarm | Def 4「木内で解決できない呼び出しは `opaque(unresolved)`」。**直し方を改訂（下記）** |
| URL slot 分割規則が未実装（OPQ 9 件） | precision loss | §2.6 の URL 分割規則（falsifiable な形で書かれている） |
| モジュール大域の名前を読まない（OPQ 8 件） | precision loss | Def 4（木内で解決できる）、§2.3 の config atom の源 |
| `os.environ` 読み出しを config として扱わない（OPQ 4 件） | precision loss | §2.3 の config atom の源 4 種 |
| BOM 付きファイルを parse 失敗にする（6 件） | false-clean（ユニットが消える） | §5.2 |
| `@mcp.tool(annotations=...)` を読まない、明示の `annotations=None` を unreadable にする | D の過小評価 / `D_unknown` の過大 | Def 6（3 形のパーサ、読めない形だけが `D_unknown`） |
| AutoGPT `@command` の名前 list 形・キーワード形、`tools=[...]` の入れ子関数 | false-clean（ユニットが消える） | R2 カタログにある形（D12） |

**直さない:**

1. **VAL 層の 13 件（`split` / `Path()` / 正規化の `startswith` を形状と数える）。**
   §6 F0a の validator 形状は**構文的**であり、語彙（月 3 凍結、11 語）に `split` と
   `ctor_path` を含む。点検プロンプトは「拒否の形で使われているか」を基準にしたので
   仕様より厳しい。**解析器は仕様どおりである。** この 13/20 は「構文的形状の保有が
   実際の検証の保有を表さない率」という**妥当性の注記**として本文に書く
   （§10 の「validator 保有 ≥ 5%」はこの構文的な量で判定する。定義は動かさない）。
2. **unit id の衝突**（同じツールが 5 ファイルに複製）。§5.1 は unit id を
   `framework:qualified_name:schema_hash` と定義し「ファイル移動に安定」を意図している。
   複製されたサーバが同じ id になるのは定義どおり。
3. **カタログに無いツールの形**（llama-index `FunctionTool.from_defaults`、SuperAGI の
   `_execute`、OpenHands の `ToolDefinition` など）。**F0a の標本を見てカタログを
   広げると測定集合で調整することになる。** 取りこぼしとして件数を報告する
   （ユニット 0 件の木 26 本中 9 本 + 混在 2 本）。カタログの拡張は月 10 の指紋凍結前に、
   標本外の根拠（フレームワークの公式文書）で行う。
4. **3.12 構文**は D16（処理系の変更）で扱い、解析器の修正とは分けて報告する。

**改訂（2026-09-14、較正対の差分による）: 末尾名だけの解決は「やめる」のではなく
「opaque にする」。** 最初は受け手型の無いメソッド呼び出しを解決しない（降りない）
ように直したが、較正対 A9 / A18 の効果行を直す前後で突き合わせたところ、**真の経路が
消えていた**:

- A18（langroid）`LanceDocChatAgent.query_plan` → `self.vecdb.compute_from_docs` の
  `compile` / `eval`（`vecdb: LanceDB` は `VectorStore` の派生で、受け手型が推論できない
  だけ）
- A9（PraisonAI）`acp_*` → `ActionOrchestrator.apply_plan` → `_apply_step` の `subprocess.run`
- A9 `stt` → `AudioAgent.transcribe` の `open`

一方で消えて正しかったのはテストの模擬クラス 1 件（`MockSpeechResponse.stream_to_file`）
だけだった。**効果を落とすのは false-clean で、EFF[6] の false-alarm より重い**（§2.6
「決して drop しない」）。したがって: 末尾名で一意に決まるなら降りて効果を出すが、その
経路の上の行の確度に `opaque(unresolved)` を合流する（resolved と数えない）。EFF[6] は
「resolved の誤った効果」から「opaque の効果」に変わる。この改訂は
`tests/test_f0a_defects.py` の `test_untyped_receiver_by_name_hop_*` が固定する。

**同じ差分で見つけた退行（直した）:** `append` を受け手への書き込みとして扱うように
したことで、`cmd = ["sg", ...]; if f: cmd.append(x)` の分岐合流が長さの違う列の join に
なり、`_shape_join` が要素を全部捨てて argv0 のリテラル `"sg"` が列全体（MODEL）に
なっていた（A9 `ast_grep_rewrite`）。共通の先頭を要素ごとに join し、はみ出しを tail に
畳むようにした（`test_branch_join_keeps_argv0_literal`）。

**改訂 2（2026-09-14、0662b39 の敵対的レビューによる）: D17 の修正そのものが
false-clean を 5 系統作っていた。** 観点別の点検者 4 名が指摘し、独立の検証者が最小
fixture で再現した 8 件（棄却 0）と、検証者が見つけた変形を、すべて修正より先に
`tests/test_f0a_defects.py` に固定してから直した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| モジュール水準の束縛 | 直下の代入だけを join したので、関数内の `global X; X = model`、別ツールの `SETTINGS["k"] = model`、入れ子関数が掴む同名の外側局所変数を見落とし、**定数の OP / resolved** にした（以前は opaque） | false-clean（verdict が消える） | 関数内で束縛・`global` 宣言される名前、どこかで変更される名前、他モジュールから `m.NAME = ...` と書かれる名前は読まない（`_WriteScan`、`_tree_attr_writes`） |
| `os.environ` | env を見る前に config 値へ短絡したので、同じ関数で書いた MODEL の読み戻しが OP になり、別モジュールの書き込みも無視した | false-clean（MODEL → OP） | 読み戻しに env の書き込みを含める。木内のどこかで非定数を書き込むなら環境変数を config とみなさず opaque |
| URL 分割（テンプレート） | `"%s://%s/api" % (...)` / `"https://{}/x".format(...)` のプレースホルダを host のリテラルとして切り出した | false-clean（MODEL の host を OP） | scheme / host の文字列に `%` `{` `}` があれば分割しない |
| URL 分割（非リテラル枝） | `f"{prefix}{host}/v1"`（prefix は scheme だけ）で url.host を prefix にした | false-clean | 直後が `/?#` で始まるリテラルのときだけ分割する |
| 木内クラスの構築 | 外部 import（`requests.sessions`）を末尾成分一致で木内の `sessions.py` と取り違え、基底（`pydantic.BaseModel`）を名前だけで木内の同名クラスと取り違えて `__init__` を実行した | false-alarm（到達しない resolved の効果） | import 名と木内モジュールの dotted 名が一致するか `.<import 名>` で終わるときだけ採る（`resolve_module_strict`）。基底もクラスのモジュールの import 表で厳密に引く |

**精度の代償（書いておく）:** 木内で非定数を `os.environ` に書き込む木では、すべての
環境変数の読み出しが opaque に戻る（`main()` で CLI 引数を書き込むだけの木も含む）。
モジュール水準の名前も、同名の局所変数がどこかの関数にあるだけで読まなくなる。
**どちらも resolved を opaque に戻す向きで、clean を作らない。**

**どうして最初に見落としたか:** D17 の修正は「解決できるのに opaque」を減らす向きの
変更で、較正対の受け入れテストも効果行の突き合わせも「消える」側を見ていた。
**opaque → resolved に変わった行が正しく resolved かは、突き合わせだけでは分からない**
（`diff_effects.py` は「slot 変化」として出すが、向きの判断は読む人に任せている）。
解決率を上げる変更は、敵対的レビューで「resolved にしてよい根拠」を 1 件ずつ崩しに
行く必要がある。

**改訂 3（2026-09-14、854f71b の 2 回目の敵対的レビューと run 3 による）: 改訂 2 の直し方が
効きすぎて効果行を落とし、残っていた false-clean もあった。** 3 観点（残る false-clean /
クラッシュ・性能・決定論 / 効きすぎ）の点検で 5 件を確認（棄却 0）。run 3 の突き合わせで
1 件を自分で見つけた。すべて修正より先に `tests/test_f0a_defects.py` の 10・11 節に固定した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| 変更されるモジュール水準のオブジェクト | 改訂 2 が `conn.row_factory = ...` / `session.headers.update(...)` を「書き込み」とみなして名前を読まなくしたので、受け手の型が消え **DB / NET の効果行ごと消えた** | false-clean（drop） | 再束縛（関数内の束縛・`global`・`m.NAME = ...`・`globals()` / `vars()` / `exec`）だけを「読まない」にし、**コンテナ / オブジェクトは常に型と主体を保ったまま確度を opaque に落とす**（`_opaque_deep`）。別名・補助関数経由の変更（`c = CONFIG; c[k] = ...`、`_put(d, k, v)`）もこれで resolved の定数にならない |
| 相対 import の基底 | import 表が相対の点を捨てるので、厳密化で `from .base import BaseTool` を同じパッケージの `base` と区別できず、基底の `__init__` の `self.conn` 経由の効果が消えた | false-clean（drop） | `SourceIndex.resolve_import_module`: 同じパッケージの `<pkg>.<name>` を先に、無ければ厳密な絶対解決。`from . import X` は親パッケージ |
| TRANSFER 表の実引数 | 変換が subject（受け手 / 第 0 引数）の主体しか採らず、`"ls {d}".format(d=d)` / `os.path.join("/data", name)` / `urljoin(base, url)` / `tpl.replace("H", host)` の MODEL を捨てた（改訂 2 以前からの欠陥。改訂 2 の `.format` の修正は**テストが弱くて効いていないのを見逃した**） | false-clean（MODEL → OP） | subject 以外の実引数の主体・確度・root を結果に入れる。非リテラルの実引数が混ざる文字列変換は形を捨てる（テンプレートのリテラルを host として切り出させない） |
| `os.environ` の別名 | `env = os.environ; env["K"] = cmd` を書き込みとして検出しなかった | false-clean | `os.environ` を名前に束縛する形を書き込みとみなす（複製 `dict(os.environ)` / `.copy()` / `{**os.environ}` は除く） |
| 再帰の走査 | 木全体を走査する再帰の NodeVisitor が、無関係なファイルの深い式（550 項の連結）で RecursionError を出し、**木 1 本の出力を全部落とした** | クラッシュ（全ユニットが消える） | 明示的なスタックで走査する（`_iter_nodes`） |
| 同名関数による解決の喪失（run 3 で発見） | `import spotify_api as sp; sp.get_followed_artists(...)` を末尾名だけで木全体から引いていたので、BOM を直して parse できるようになった別ファイルの同名関数と衝突し、NET 効果が 6 ユニットで消えた | false-clean（drop） | import 表で指したモジュール / 同じモジュールの定義を先に引く（`_pinned_function`）。末尾名の木全体検索はその後 |

**確認:** 較正対 A9 / A18 の効果行を 854f71b と突き合わせて消えた行 0、w-jitz10__spotify_mcp は
0 → 40 行。受け入れ（B3a 8/8、B3b 15/15、実装変異の生存 1/15、両側 7/7 で変化サイトは
evidence/w0 と同一）と決定論は不変。

**改訂 4（2026-09-14、8f24cbd の 3 回目の敵対的レビュー（確認 6・棄却 0）と run 3 / run 4 の
突き合わせによる）:** すべて修正より先に `tests/test_f0a_defects.py` 12・13 節と 11 節の追加に固定した。

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| `_pinned_function` の一意判定 | `lookup_function(name, module)` が索引の setdefault で最初の定義 1 件しか返さず、`@overload` のスタブ・再定義・if / else の def・import を上書きするローカル def で最初の定義に決め打ちした | false-clean（opaque → resolved） | 全定義で一意性を判定し、同名の入れ子 def・import・モジュール水準の代入があるときも pin しない |
| 入れ子ハンドラの素の名前 | `serve()` の中のハンドラが呼ぶ `prepare(...)` を、外側の `serve.prepare` ではなくモジュール直下の同名 def に決め打ちした | false-clean | 同じモジュールに同名の入れ子 def があれば pin しない |
| `"*"`（`exec` / `globals()` / `vars()`）で名前を読まない | 改訂 3 がモジュール全体の名前を読まない側に倒したので、オブジェクトの受け手の型が消え NET / DB の効果行が丸ごと消えた（2 観点が独立に指摘） | false-clean（drop、改訂 3 の退行） | 書き込みがある名前も「読まない」ではなく、**型と主体を保って確度を opaque に落とす** |
| val エンジンの再帰 | tool が読む 550 項の連結式で `_eval` の再帰が RecursionError を出し、木 1 本の出力を全部落とした（854f71b から残存） | クラッシュ | 左結合の `+` の連鎖を反復で畳む。runner がユニット単位で RecursionError を捕まえ `TRUNCATED(recursion)` として残す |
| 定数ホストの `.format` | 改訂 3 が非リテラル実引数の混ざる文字列の形を丸ごと捨てたので、`"https://api.github.com/repos/{}".format(x)` の host が MODEL になった（f 文字列では OP） | 精度の損失（誤警報） | テンプレートの最初のプレースホルダより前のリテラルを part として保つ |
| 同じ関数の 2 ユニット（run 3 で発見） | `@mcp.tool()` で登録した入れ子関数の名前をログの `tools=[...]` に並べる形で、同じ関数が `mcp` と `tools-list` の 2 ユニットになった | 過大計上 | tools-list の候補がすでにほかの規則のユニットならユニットにしない |

**確認:** 較正対の効果行は 8f24cbd と比べて消えた行 0。w-giak__mnemo-lite の 42 行の消失は
すべて重複していた `tools-list:` ユニットの行で、同じ qualname / 経路 / サイトの `mcp:` ユニットの
行が残っていることを機械的に確かめた。

**記録する限界（新たに受け入れたもの）:** `os.environ` を関数に渡してその中で書き換える形、
`setattr(sys.modules[...], ...)` による再束縛は見ない。モジュール水準のコンテナ / オブジェクトは
書き込みの有無にかかわらず opaque になる（resolved → opaque の向きで clean を作らない）。
相対 import の判定は「同じパッケージに同名モジュールがあればそれ」で、絶対 import が
同名の兄弟モジュールと衝突する木では誤りうる。

**改訂 5（2026-09-14、ea35672 の 4 回目の敵対的レビュー（確認 6・棄却 0。6 件すべて false-clean /
効果行の消失の向き）による）:** 6 件は下の 4 系統に重なる（URL 分割の件は 3 観点が独立に指摘した）。
**D19 の凍結条件を満たさない**ので、D19(3) に従い、すべて修正より先に `tests/test_f0a_defects.py`
14 節に固定し（xfail 17 件。「連結で作った Str」の形はレビューの指摘には無く、再現の途中で自分で
見つけた同じ系統の形）、直した差分だけを 5 回目のレビューにかける。**5 回目が最後の繰り返しである。**

| 系統 | 何が起きていたか | 誤りの向き | 直し方 |
|---|---|---|---|
| opaque の値の定数を URL 分割がリテラルとして読む | 改訂 4 の `_opaque_deep` が Atom の定数と Str の part の確度を残し、`_split_url` がその定数から url.scheme / url.host = OP / resolved を作った。`global` / `exec(..., globals())` / 読む側の再束縛で MODEL が書き換えるベース URL の host が resolved の定数になり、行の確度も resolved になった | false-clean（opaque → resolved。"*" 形と import 形は MODEL → OP も。改訂 4 の退行） | `Value.const` / `is_literal()` は**確度が resolved の値の定数しか返さない**。`_opaque_deep` は Str の part にも opaque を合流する（`_make_str` が part を平らに展開するので、外側だけでは足りない） |
| `shell=` / `open` の mode | `_exec_mode` / `_mode_is_write` が再束縛される名前の opaque な定数（False / "r"）をリテラルとして読み、shell=True 側の SPAWN 行と FS_WRITE 行が消えた | 効果行の消失（改訂 4 の退行） | 同上（定数を読めなくなるので「判定できない」側に回り、両方の行を出す） |
| 差し替えられる dict の URL テンプレート | tool が `ENDPOINTS[name] = tmpl` で差し替える要素（opaque）の `.format(q)` で、改訂 4 のテンプレート先頭の part が確度を捨てて host = OP / resolved を作った。`ENDPOINTS[k] + q` の形は 8f24cbd の時点から同じ | false-clean（`.format` は改訂 4 の退行、`+` は既存） | 同上 |
| 同名の定義による効果行の消失 | `_pinned_function` がモジュール内の同名の def を、呼び出し位置から見えない入れ子 def（別の関数の中）まで数えて pin をやめ、末尾名の木全体検索も 2 候補で降りなかった。if / else の 2 つの def、import した名前と読む側の無関係な入れ子 def、`helpers.run_command(...)` と helper 側の入れ子 def でも同じ。helper の中の SPAWN 行が丸ごと消えた | 効果行の消失（改訂 4 の退行） | **呼び出し位置から見える定義だけを数える**（`_visible_defs`: モジュール直下の def と、素の名前の呼び出しなら呼び出し行を囲む関数の中の def）。見える定義が複数ある、または同じ名前が import / 代入でも束縛されるときは、**全候補へ降りて戻り値を join し、行と戻り値を opaque にする**（1 つを選ぶと他方の行が消え、降りなければ全部消える） |

**警報の向きの判定は、確度に関係なく形の定数を読む:** `_is_policy_path`（方針ファイルへの書き込み
`write_policy`）と `sep.join` の受け手の型判定は `shape.const` を読む。`Value.const` の変更で
再束縛されうる方針ファイルのパスへの書き込みを見落とさないため。

**記録する限界（新たに受け入れたもの）:**
- モジュール水準のリスト / dict の要素（改訂 4 から、書き込みの有無にかかわらず opaque）の定数も
  リテラルとして読まなくなる。`CMD = ["ls", "-la"]` の argv0 は副 kind `SPAWN_CONST_ARGV` にならない
  （resolved → opaque の向き。精度の損失）。
  **訂正（5 回目のレビューによる）:** ここには当初「pipe の argv0 の判定にも使わない（精度の損失）」とも
  書いたが、**向きの判断が誤りだった。** `_pipe` は判定できないときに FS_WRITE の側だけを出すので、
  argv0 / shell が opaque の値だと pipe 書き込みの **EXEC(code_text) 行が消える**（効果行の消失）。
  D19 の「結果」の既知の欠陥 K1。
- 見える同名の定義が複数ある呼び出しは、全候補の効果を opaque で出す（どれが効くかを決めない。
  使われない分岐の行は誤警報になりうる）。
- 呼び出し関数自身の局所 def と同名の呼び出し（`func.id in scope.local_bindings`）は、従来どおり
  pin を引かず末尾名の木全体検索に回る。

**確認（修正の commit の時点）:** テスト 177 件が `.venv`（3.10）と `.venv312`（3.12）の両方で通る
（14 節の 17 件は、未修正の 56f61c5 / 170a7b2 を worktree に取り出して走らせると xfail）。
受け入れ B3a 8/8、B3b 15/15、実装変異の生存 1/15、決定論（A1__fixed / A9__vuln で 3 回バイト一致）は
不変。両側 7/7 で、**変化した経路・判定・verdict-clearing は `evidence/w0/two_sided.json` と同一**。
違うのは不変の経路の数 `n_unchanged_paths` だけで、3 対で増えた（対 1: 10 → 12、対 5: 13 → 14、
対 6: 23 → 55）。**これは改訂 5 によるものではない**: 170a7b2 を `git archive` で取り出して同じ手続きで
走らせると（`authgap` がその展開先から import されることを確かめた）すでに 12 / 14 / 55 で、
170a7b2 と 150e06a の出力 JSON の違いは木の絶対パス（`vuln_root` / `fixed_root`）だけだった。
w0 の後、改訂 2〜4 のどこで増えたかは切り分けていない（不明。変化した経路と判定は同一なので、
T1 の主指標には効かない）。
較正対 14 木の `diff_effects.py --before 170a7b2 --after 150e06a`: 消えた行 0・増えた行 0。slot 変化は
A9 の 86 件（両側 43 件ずつ、`BasicSkillMutator` の経路）で、**すべて行の確度の理由が
`opaque(unresolved)` → `opaque(depth+unresolved)` になっただけ**（主体・確度の種類の変化 0）。
野外: run 6（150e06a、Python 3.12）の `units.jsonl` / `trees.jsonl` は run 5 と**バイト一致**
（改訂 5 が直した形は標本の 98 木に無かった。関門の数字も区間も run 5 と同じ）。

**フレームの誤り（直す。結果とは独立の事実誤認）:** `APP_FRAME` の
`OpenManus/OpenManus` は RL 用の openmanus_rl で、選定根拠に書いた「§2.6 の負例
F5/F6/F7 の出所」（FoundationAgents 版 `app/tool/python_execute.py` ほか）ではない。
選定根拠が偽なので、根拠どおりの repo に置き換える。**置き換えは結果を見て選び
直したのではなく、名前の取り違えの訂正である**が、run 1 には誤った repo が入って
いることを run 1 の表の注記に残す。

**訂正後の `FoundationAgents/OpenManus`（3309bf4e）もユニット 0 件である。** ツールは
`class PythonExecute(BaseTool)` の `async def execute(...)` 形で、Def 2 の R2 カタログ
（`@mcp.tool`、低レベル MCP 2 形、`@tool`、`BaseTool._run`、CrewAI `_run`、
`@function_tool`、`@kernel_function`、agno、gptme `ToolSpec`）に `execute` は無い。
§2.6 の F5–F8 は **val エンジンの受け入れ fixture**（関数本体の値の解析）であって、
OpenManus を R2 の入口として認識することを要求していない。**上の「直さない 3」に
従いカタログは広げず、アプリ母集団のカタログ外の形の取りこぼしとして数える。**
（F1–F10 の fixture `fixtures/val/expected.json` 自体はまだ作っていない。
`docs/open_questions.md` の作業一覧に置いた。）
