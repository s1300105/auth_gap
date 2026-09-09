# 決定した事項（根拠つき）

仕様書 `AUTHGAP_BRIEF_v3.md` の記述と実データが食い違った点、および仕様書が
決めていなかった点について、**実装側で判断して確定させた**内容を残す。
後から追認できるように、どの証拠でそう決めたかを必ず書く。

**仕様書本体は書き換えていない。** 仕様書は設計の記録として残し、
食い違いはここと `docs/cve_triage.csv` に併記する。

最終更新 2026-09-09。

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
