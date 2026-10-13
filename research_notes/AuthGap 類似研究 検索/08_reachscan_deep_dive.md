# reachscan の詳説 — 仕組み、評価の主張、動かした結果、AuthGap との異同

調査日は 2026-10-12〜13。対象は reachscan の commit `4f6509d812b3c40769ddce0ea0bee548bfe24e02`（タグ v0.4.0）である。
この文書で reachscan のコードの行番号を書くときは、すべてこの commit の repo からの相対パスを使う（例: `src/reachscan/reachability.py:64`）。
AuthGap の行番号は HEAD `8fbbed4`（2026-10-12）のもの。

**検証の水準**（上げない）

- ◎ コードを自分で読んだ、または自分で走らせた。
- ○ README、CHANGELOG、PR 本文、コミットメッセージに書かれた**著者の主張**。PR 本文は WebFetch（要約モデル経由）で取ったもので、一字一句は照合していない（api.github.com は 403 だった）。
- △ 二次。この文書から見て別の記録に書かれたもの（例: `docs/related_work.md` の HintLint / mcp-doctor の結果、ノート 07 の記述）。

§3〜§5 のコードの事実は、断りが無ければ ◎ である。著者が出した数値はすべて**著者の主張・未検証**（`verified_by_me = none`。CLAUDE.md 規則 1）。
引用の中の「 / 」は改行を表す。

**この文書の元**: 読み手 6 人の報告と、その報告を敵対的に検証した 6 本の報告、合成ケースを走らせた 3 つの probe（A・B1・B2）。
検証で refuted または partly とされた記述は、検証の訂正に従って書き直した。読み手が予想しただけで誰も走らせていないものには「未実行」と書いた。

**走らせなかったもの**: AuthGap の評価・練習データには、reachscan も AuthGap も一度も走らせていない。対象は `evidence/annotation_fixes_frame*`、`evidence/annotation_fixes_v234`、`evidence/practice_*`、`evidence/population_v3`、`evidence/population_v4`、`corpus/` である。
入力にしたのは 3 つだけ: `evidence/related_work_20261002/depth_probe/` の写し、`fixtures/` の写し、scratchpad に作った合成ケース。
`authgap/` は変えていない。

**急ぐ人へ**: §1（何か）、§4（規則の表）、§5（未解決の扱い）、§8（異同の表）、§9（論文での書き方と比較の手順）を読めば足りる。

---

## 1. 一言で

reachscan は、AI エージェントと MCP サーバのコードを静的に調べ、「ツールの入口から届く危険な能力」を探す OSS の CLI である。

- 説明文: `pyproject.toml:8` `description = "Reachability-based capability scanner for AI agent and MCP server codebases."`
- 作者: Vinmay Nair 個人（`pyproject.toml:10` `authors = [{name = "Vinmay Nair", email = "vinmay.nair@gmail.com"}]`）
- ライセンス: Apache-2.0（`pyproject.toml:11` `license = "Apache-2.0"`。`LICENSE` の冒頭は `Apache License` / `Version 2.0, January 2004`）
- 以上 ◎。

仕事は 3 段に分かれる（◎）。

1. Python と TS/JS のソースから、能力（capability）を AST の名前の照合で見つける。能力は EXECUTE / READ / WRITE / SEND / SECRETS / DYNAMIC / AUTONOMY の 7 種（`src/reachscan/suppressions.py:30`）。
2. ツールの入口から AST の呼び出しグラフを最大 8 hop まで辿り、各 finding を reachable / unreachable / unknown / module_level / no_entry_points に分ける。
3. v0.3.0（2026-10-05）からは、Python の MCP ツールについて、明示された `readOnlyHint` / `openWorldHint` / `destructiveHint` を、そのツールから届く能力と照らす。矛盾は `ANNOTATION_MISMATCH`（SARIF の rule id は `mcp-risk-mismatch`）として、経路をつけて出す。`idempotentHint` を照らす規則は無い。

AuthGap と重なるのは 3. である。設計は `src/reachscan/analysis/annotation_mismatch.py:22-26` の docstring に要約されている（◎）。

```
Only explicit hints are checked. Defaulted hints are the spec's conservative
values and claim nothing; unresolvable hints never produce findings. Every
mismatch carries the call path from the tool's entry point to the
contradicting sink, and a contradiction without such a path is not reported
(module-level code, which runs on import, is not a tool call path).
```

つまり reachscan は「明示されたヒントだけを照らし、経路を示せる矛盾だけを報告し、決められないものについては黙る」。
AuthGap は、決められなかった値に `opaque(reason)` を付けて残す（効果の行の確度と、ユニットの `opaque_reasons`）。率として出しているのは F0a の probe の slot の率（`probe_json` の `opaque_ratio_*`）である。
ただし AuthGap にも穴がある。降りなかった呼び出しの先の効果は行が残らず、`authgap scan` の manifest には率が無く、非リテラルのヒントの値は黙って捨てる（§5）。
両者の違いの中心はここにある（§5）。

**版**: 調べたのは v0.4.0（`4f6509d`。2026-10-07 09:52:27 -0400、「Merge pull request #45 … release-0.4.0」）。

- 2026-10-12 23:19 UTC の `git fetch` と 23:34 UTC の `git ls-remote` では、`refs/heads/main` は `4f6509d812b3c40769ddce0ea0bee548bfe24e02` のままで、これより新しいコミットは無かった（◎）。
- main に入っていない PR head は 2 つある。どちらも `src/` には触れていない（◎）。
  - #23（composite GitHub Action、`ff0010f`）: 変えるのは `integrations/github-action/*` だけ。
  - #39（T16a registry sweep、`6c8b971`）: 変えるのは `research/registry_scan/` だけ。
- 2026-10-04〜07 の 4 日で 5 版（v0.2.0、v0.3.0、v0.3.1、v0.3.2、v0.4.0。`git for-each-ref refs/tags` で確認、◎）を出した直後なので、論文には版、commit、参照日を必ず書くこと（推論）。

**決定論**: probe A で同じ入力を 2 回走らせ、`generated_at` を除いた JSON がバイト一致した（◎）。
LLM は呼ばず、AST の照合だけで動く（ノート 07 が src を grep した記録。△）。

---

## 2. 歴史

時刻はコミットの時刻（タイムゾーンは git の表示のまま）。水準: git で読んだ日時・差分は ◎、コミット本文や PR に書かれた理由は ○。

| 日時 | commit / タグ | 出来事 | 水準 |
|---|---|---|---|
| 2026-02-21 02:07 -0500 | `fd05637` | 最初のコミット。パッケージ名は `src/agent-scan/`。19 ファイルのうち、README.md（20 行）以外はすべて空 | ◎ |
| 2026-02-23 01:12 -0500 | `a5ced97` | `mcp+https://…` の MCP HTTP エンドポイントから Python のリソースを取り出して走査する機能。`git log -S'mcp'` で最も古いコミット | ◎ |
| 2026-02-27 00:13 -0500 | `7e8cbe6` | README に FP 率 0.47% の記述が入る。到達性解析より前 | ◎（記述の中身は ○） |
| 2026-02-28 02:41 -0500 | `825941a` | JS/TS の入口検出。MCP SDK の `server.tool("name", schema, handler)` を含む | ◎ |
| 2026-02-28 15:36 -0500 | `da0ec9f` | Python の入口検出（`@mcp.tool()` を含む）。深さ 8 の呼び出しグラフと到達性 | ◎ |
| 2026-03-04 22:11 -0500 | `92c3eb0`（その前に `70d8d42`） | `70d8d42` で agent-scan → agent_scan、`92c3eb0` で agent_scan → reachscan と改名 | ◎ |
| 2026-03-05 00:51 -0500 | v0.1.0（`4de2231`、軽量タグ） | 最初の版 | ◎ |
| 2026-03-12 22:02 -0400 | v0.1.1（`8bfadff`） | | ◎ |
| 2026-03-26 00:17〜00:26 -0400 | `3be6fab`、`07809a9`（PR #17 のマージ）、`e038727` | vinmay のコミット 3 つ（検出の更新と到達性の修正、README とフック） | ◎ |
| `e038727`（03-26 00:26）の後〜2026-10-03 | | dependabot のコミット 3 つだけ（06-24 `78e7478`・`97dea06`、07-22 `43b4ddf`） | ◎ |
| 2026-10-04 16:28 -0400 | `83e2748`、`3d758f0` | vinmay が dependabot の PR（#18 ほか）をマージ | ◎ |
| 2026-10-04 19:33 -0400 | v0.2.0（`1797146`。注釈つきタグ自体は 19:33:58） | | ◎ |
| 2026-10-04 23:16 -0400 | `784483e`（PR #28、T10） | Python ソースから MCP ツールの注釈を抽出 | ◎ |
| 2026-10-05 00:04 -0400 | `2596a8b` | snake_case のヒントを解決不能とし、ファイルをまたぐ定数を 1 段だけ解く。本文に「Found by running the phase-3 corpus:」 | ◎（本文は ○） |
| 2026-10-05 10:30 -0400 | `9215b03` | PR #28 のマージ | ◎ |
| 2026-10-05 13:22 -0400 | `65c8ca6`（PR #32、T11） | `ANNOTATION_MISMATCH` を追加。EXECUTE を destructiveHint から外す規則（「V decision」）はこの時点で既に入っている。openWorldHint は「届く SEND」で反証する（generic な connect は、根が socket / ssl / websocket / websockets / asyncio のときだけ数える） | ◎ |
| 2026-10-05 14:34 -0400 | `87aad16` | openWorldHint を HTTP、websocket、socket connect の 3 種に絞り、socket のリテラル loopback を除外（65c8ca6 の 71 分後） | ◎ |
| 2026-10-05 14:45 / 14:48 -0400 | `277d8d8`（PR #32 マージ）、v0.3.0（`cbacd8f`、タグ 14:53:54） | 0.3.0rc1 を準備したコミット `d8c688d` はあるが、rc のタグも PyPI の版も見つからなかった | ◎ |
| 2026-10-05 23:34 -0400 | v0.3.1（`4a5fa7e`） | 低レベルの分岐で `and` の連言も結ぶようになる。PyPI へのアップロードは 2026-10-06T12:56Z。sdist の src はタグと同一 | ◎ |
| 2026-10-06 | PR #39 を閉じる | T16a registry sweep（公式 MCP registry の Python サーバ上位 300）。「Closed for now; this will be reopened later.」 | ○ |
| 2026-10-06 13:57 -0400 | v0.3.2（`3aab3b0`） | TS の到達性解析（T8） | ◎ |
| 2026-10-06 23:39 -0400 | `7dc4104` | 不一致を終了コードに数えるようにする。openWorldHint の不一致を high から medium に下げる（理由の記述は、コミット本文、PR #42、CHANGELOG のどこにも見つからなかった） | ◎ |
| 2026-10-06 23:54 -0400 | `d2b001d`（T8a） | 解決できないメソッド呼び出しの先を unreachable ではなく unknown にする | ◎ |
| 2026-10-07 08:36 -0400 | `8bfa5bf`（T21） | 理由を必須にしたインライン抑制 | ◎ |
| 2026-10-07 09:52 -0400 | `4f6509d` = v0.4.0 | 本調査の版。PyPI は 2026-10-07T13:54:44Z | ◎ |
| 2026-10-12 23:34 UTC | `git ls-remote` | main は `4f6509d` のまま | ◎ |

**経緯の要点**: 2〜3 月に能力検出器、入口検出、深さ 8 の到達性を作り、そこから半年ほど動かなかった。
2026-10-04〜07 の 4 日間で、注釈の抽出 → 不一致 → unknown → 抑制 → 終了コードへの算入 を一気に入れている。
ブランチ名にタスク ID（T8 / T8a / T10 / T11 / T16a / T21）が付いていて、PR 本文には次のような語がある（○）。

- PR #32: 「agreed decision」
- PR #44: 「your decision」「your T21 decisions」

ここから、著者以外に決定者か依頼者がいるように読めるが、これは推測（△）。「V decision」の V が何を指すかは書かれていない。

**日付の食い違い**（◎）: `CHANGELOG.md:74` は `## [0.2.0] - 2026-10-05` と書くが、タグも PyPI も 10-04 である。
0.3.1 も、CHANGELOG（`CHANGELOG.md:38`）は 10-05、PyPI へのアップロードは 10-06 である。
PyPI の版の集合（0.1.0、0.1.1、0.2.0、0.3.0、0.3.1、0.3.2、0.4.0）はタグと一致し、rc は載っていない。
`reachscan.dev` は `https://github.com/vinmay/reachscan` への 302 転送だけだった（◎ curl）。
ブログや告知は読み手の Web 検索では見つからなかったが、検証者はこの点を確かめていない。

**ノート 07 の記述から更新する点**

- ノート 07 は openWorldHint の規則に「literal の loopback は除く」と書いた。除くのは **socket connect だけ**で、HTTP と websocket は宛先が `localhost` や `127.0.0.1` でも矛盾に数える（§4）。
- ノート 07 は「確認済み TP の詳細は非公開」と書いた。その後の PR #42 が、サーバ（awslabs）とツール（`suggest_aws_commands`）、上流への修正 PR `https://github.com/awslabs/mcp/pull/4734` を挙げている（○）。
- ノート 07 は「同じツールで reachable と unknown が混ざったときの注記は未確認」とした。unknown の finding は**どのツールにも帰属されない**ことを確かめた（§5）。
- ノート 07:202（A5）は「結びつかない lowlevel のツールは数（linked / unlinked）だけ報告する」と書いた。この件数は **JSON にもテキストにも SARIF にも出ない**（`scanner.py:445` `# Internal (not in JSON): --explain notes and lowlevel linkage counts`。§3.8）。報告されるのは宣言そのもの（`declared_tools`）だけである。
- ノート 07:208 は、openWorldHint を medium に下げたことを「corpus を見ながらの調整」の例に挙げた。本ノートでは、下げた理由の記述は見つからなかった（`7dc4104`、PR #42、CHANGELOG）。corpus を見て決めたと記録があるのは、EXECUTE を destructiveHint から外すことと、openWorldHint を 3 種の送信に絞ることの 2 つである（「V decision」、PR #32。§6）。medium 化をその例に数えるのは根拠が無い。

---

## 3. 仕組み

パイプラインは次の順に進む。

1. ファイル集合
2. 読み込み
3. 入口の検出
4. 注釈の抽出
5. 呼び出しグラフ
6. 能力の検出
7. 到達性
8. 不一致の判定
9. 出力と終了コード

### 3.1 走査するファイル

ファイルを集めるのは `src/reachscan/scanner.py` の `_gather_py_files` である。除外の判定は 2 つある。

- ディレクトリ名の集合 `_EXCLUDED_DIR_PARTS`（`scanner.py:56-65`）。tests / test / benchmark / benchmarks / venv / .venv / site-packages / .git / .github / `__pycache__` などを含む。
- ファイル名（`scanner.py:213-214` `if name.startswith("test_") or name.endswith("_test.py"):` / `return True`。212 行は `name = p.name.lower()`）。

ディレクトリ名は resolve した**絶対パスの全成分**と照らされる。
`scanner.py:55` のコメントは「Any .py file whose absolute path contains one of these as a directory part is excluded.」と書き、`src/reachscan/source_loader.py:349` は `p = maybe_local.resolve()` である。
そのため、走査の根より上の祖先に `test` などの名前があると、木全体が 0 ファイル・exit 0 になる（実行例は入口-c14、B1-c12、sink-p_proj）。

入口検出の側にも別の除外集合がある（`py_entry_points.py:316-330`）。`node_modules` は入口側にしか無い。
単一ファイルを指定した場合、`_gather_py_files` は除外の判定をせずにそのまま返す（`scanner.py:203-204`）。しかし入口検出は除外するので、finding は no_entry_points になる（入口-c14_file）。
PyPI の対象ではさらに docs / doc / scripts / .dist-info を除く（`scanner.py:67-70`）。ただしこの除外は入口検出には渡らない（コードの読み）。

AuthGap の scan はテストのパスを除かない。`tests/` や `benchmarks/` に置いたサーバも走査する（B1-c10）。

### 3.2 ソースの読み方

読み方は 3 か所で違い、どれも文字列のまま `ast.parse` に渡す。

| 箇所 | 読み方 |
|---|---|
| 入口検出（`py_entry_points.py:1124`） | `content = path.read_text(encoding="utf-8", errors="ignore")` |
| 呼び出しグラフ（`call_graph.py:145`） | 同じ（`errors="ignore"` つき） |
| 能力検出器（`scanner.py:270`） | `src = p.read_text(encoding="utf-8")`（strict） |

UTF-8 の BOM は文字列に U+FEFF として残り、`SyntaxError: invalid non-printable character U+FEFF` になる（Python 3.10.20、3.12.3、3.13.16 で確認）。
この例外は 3 か所とも握りつぶされる。

- `py_entry_points.py:983-985` `except SyntaxError:` / `return []`
- `call_graph.py:149-150`
- `detectors/registry.py:107-110`

`num_files_scanned` は集めたファイルの数（`scanner.py:435` `"num_files_scanned": len(py_files)`）であって、解析できたファイルの数ではない。
そのため BOM 付きのファイルは、警告も出ないまま消える。
1 ファイルの木では「1 ファイル走査、入口 0、finding 0、exit 0」という出力になった（入口-c13、sink-g_bom、MM-c18、注釈-v08）。
CG-c16 は 2 ファイルの木（server.py と、BOM の付いた util.py）で、`num_files_scanned` は 2、入口は server.py の 1 つ、finding は 0 だった。util.py の `os.remove` の finding だけが黙って消えた。

AuthGap はバイト列で parse し（`authgap/srcindex.py:127` `with open(path, "rb") as fh:`）、失敗は `parse_failures` に出す。
CLAUDE.md の落とし穴「ソースは `ast.parse` にバイト列で渡す」と同じ穴である。

### 3.3 入口の検出（`src/reachscan/py_entry_points.py`）

入口は表に載った 3 つの形で照合する。

**(a) デコレータ**: 辞書 `ENTRY_POINT_DECORATORS` の 10 個のキー（`py_entry_points.py:115-126`）と、デコレータの末尾名を照らす。キーは tool, tool_plain, function_tool, kernel_function, register_for_llm, call_tool, list_tools, register_tool, fn, ai_model である。

```
ENTRY_POINT_DECORATORS: Dict[str, str] = {
    "tool":             "langchain_or_crewai",   # @tool, @mcp.tool(), @agent.tool
...
    "call_tool":        FRAMEWORK_MCP,           # @app.call_tool()   — MCP lowlevel dispatch handler
    "list_tools":       FRAMEWORK_MCP,           # @app.list_tools()  — MCP lowlevel tool listing
```

受け手が何であるかは照合に使わない（`py_entry_points.py:536-538`）。受け手はラベル付け（下の framework）にだけ使う。
デコレータは `@name` と `@obj.name` の 2 段までしか読まない（`py_entry_points.py:514-519`）。

```
    if isinstance(inner, ast.Attribute):
        # Only match when the receiver is a simple name (two-level)
        if isinstance(inner.value, ast.Name):
            return inner.attr, inner.value.id
        # Three-level or deeper — skip
        return None, None
```

主走査はモジュール直下とクラス本体だけを見る。関数の本体にも、if / try / with の本体にも降りない（`py_entry_points.py:960-966`）。

```
    for node in ast.iter_child_nodes(parent):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node
            # Do NOT recurse: anything inside this function body is skipped
        elif isinstance(node, ast.ClassDef):
            yield node
            yield from _iter_detectable_nodes(node)  # recurse into class body only
```

docstring（`py_entry_points.py:957-958`）は「Real user-defined tools are always at / module or class scope, never nested inside other functions.」と書く。これは著者の前提である（○）。
例外として、キーが `call_tool` / `list_tools` のデコレータだけは、2 回目の走査で `ast.walk` を使い、入れ子の中も拾う（`py_entry_points.py:1036-1041`、`_MCP_HANDLER_KEYS = frozenset({"call_tool", "list_tools"})`）。
そのため `serve()` の中の低レベルハンドラは入口になる（入口-c08b、B1-c04a）。
ただしこの走査も `_decorator_key` を通るので、2 段の制限は残る。メソッドの中の `@self.server.call_tool()` は入口にならなかった（入口-t2）。

ツール名の決め方（`py_entry_points.py:591-598`）は次の順である。

1. デコレータの第 1 位置引数が文字列リテラルなら、それを使う。
2. 次に `name=` の文字列リテラル。
3. どちらも無ければ関数名。

`name=TOOL_NAME` のような定数の参照は解かず、関数名に落ちる（入口-t9）。
クラスに付いたデコレータでは、クラス本体の静的な `name` 属性がデコレータ引数の名前より優先する（`py_entry_points.py:545-549`）。

**(b) 基底クラス**: BaseTool / StructuredTool / Toolkit の派生クラスを入口にする。本体に静的な文字列 `name` が無いものは入口にしない（`py_entry_points.py:654-655` `if tool_name is None:` / `return None`）。
起点は「class 行より後ろで最初に現れる `._run` / `._arun` / `.__call__`」（`reachability.py:155-162`）。この探し方はクラスの範囲を確かめない。
そのため、直後にある別のクラスの `_run` を起点に取ることがある。入口-t1 では、agno Toolkit の入口から、ツールでない `Janitor._run` の `os.remove` が reachable と出た。

**(c) 工場呼び出し**: 表 `ENTRY_POINT_FACTORIES` の 6 形（`py_entry_points.py:175-220`）。LlamaIndex の 2 形、DSPy `Tool`、Swarm `Agent(functions=)`、Google ADK `Agent(tools=)`、CAMEL `FunctionTool` である。
照合は呼び出し名の完全一致（`py_entry_points.py:727-729`）と import 元のヒントで行い、モジュール直下の `Expr` / `Assign` だけを見る（`py_entry_points.py:781-790`）。
次の書き方は入口にならない。

- 別名で import したもの（`AgnoAgent(...)`、`SwarmAgent(...)`）
- 別名の無い agno の `Agent(tools=[...])`（import 元のヒントに当たらない。入口-t10）
- 注釈つき代入 `root_agent: Agent = Agent(tools=[...])`（google.adk でも同じ。入口-t11）

**入口にならないと確かめた書き方**（どれも ◎ 実行）

- `mcp.add_tool(fn, annotations=...)` と `mcp.tool(annotations=...)(fn)`（入口-c04、MM-v10、B1-c05a）。著者もこの限界を書いている（`py_annotations.py:38-39`、○）。
- 3 段以上のデコレータ: モジュール直下の `@Holder.mcp.tool`（入口-c03）、メソッドの中の `@self.server.call_tool()`（入口-t2）
- 関数の中で定義したツール（入口-c02、B1-c11）
- モジュール直下の if / try の中で定義したツール（入口-c16）
- 低レベル v2 の `Server("demo", on_call_tool=h)`（入口-c26）。src の Python 側を `on_call_tool|add_request_handler` で検索したが、見つからなかった。

**framework のラベルと注釈**: 注釈を付けるのは、framework が `mcp` と判定されたデコレータ形の入口だけである（`py_entry_points.py:1067-1070`）。

```
    by_lineno = {
        ep.lineno: ep for ep in results
        if ep.framework == FRAMEWORK_MCP and ep.pattern_type == PATTERN_DECORATOR
    }
```

docstring（`py_entry_points.py:5-6`）とコメント（`py_entry_points.py:75` `# Framework label constants (metadata only — do not use in detection logic)`）は「ラベルはメタデータで、検出には使わない」と書く。実装はこれと食い違っている（◎）。
ラベルは次の順で決まる（`py_entry_points.py:446-478`。検証の訂正どおり）。

1. 受け手名かキー（`tool` など）が、既知のフレームワークのモジュールから import されている → 0.95
2. モジュール直下の `x = Cls(...)` から推論できる → 0.80
3. 未知のモジュールから import されている → 0.70（名前がヒントに当たれば mcp、当たらなければ unknown）
4. 受け手名がヒント集合に当たる（`py_entry_points.py:256` `_MCP_RECEIVER_HINTS: frozenset = frozenset({"mcp", "server", "app", "fastmcp"})`。大文字小文字は区別しない）→ mcp 0.60
5. デコレータ表の既定ラベル → 0.60（`tool` なら `"langchain_or_crewai"`）
6. unknown

この順序から、次のことが起きる（いずれも注釈を読まず、不一致は 0、Not checked にも出ない）。

- `srv = fastmcp.FastMCP("a")` の `@srv.tool(annotations=...)`、別モジュールから import した `my_server`、工場関数の戻り値を受け手にしたもの（入口-c05、入口-c06、B1-c08）
- 同じファイルに `from langchain_core.tools import tool` があると、`mcp = FastMCP("demo")` の `@mcp.tool(annotations=...)` も手順 1 で langchain 0.95 になる（入口-t14）

**import 表**: `_collect_imports` の docstring（`py_entry_points.py:394-395`）は「Only top-level imports are examined. Local imports inside functions are / intentionally skipped.」と書く。
しかし実装は `py_entry_points.py:404` `for node in ast.walk(tree):` で、木全体の import を集める（入口-c27、入口-t12 で確認）。
上書きは訪問順の後勝ちである。そのため `try: from mcp.types import Tool` / `except ImportError: from mylib import Tool` と書くと、`Tool` は mylib 由来とされ、低レベルの宣言がすべて落ちる（注釈-v05）。

### 3.4 注釈の抽出（`src/reachscan/py_annotations.py`）

**読むヒント**: 4 つの camelCase キーだけ（`py_annotations.py:56` `HINT_KEYS = ("readOnlyHint", "destructiveHint", "idempotentHint", "openWorldHint")`）。
`title` は読まない。`title` だけの注釈は declared=True で、4 ヒントすべてが default になる（注釈-v09）。
綴りを誤ったキー（`"readonlyHint"`）は unresolvable にならず、黙って無視されて default になる（注釈-v06c）。

**読む場所**: デコレータと `Tool(...)` の `annotations=` キーワードだけである（`py_annotations.py:328-333`）。

- `annotations=` が無く `**kwargs` があるときは、全ヒント unresolvable・declared=True とする。
- `annotations=None` は宣言なしとして扱う。
- 位置引数は読まない。

**読む式**: 3 つ。

- `ToolAnnotations(...)`: 呼び出し先の末尾名だけで判定する（`py_annotations.py:183-184` `return isinstance(node, ast.Call) and _callee_name(node.func) == "ToolAnnotations"`）。import 元は確かめない。別名（`ToolAnnotations as TA`）は認識されない。
- 辞書リテラル。
- 名前参照: 1 段だけ追う（`py_annotations.py:266-277`）。追う先は、同じファイルのモジュール直下で 1 回だけ代入された式か、project root 内のファイルからの from-import である。追えないものは全ヒント unresolvable・`unresolved_reference=True` になる。

```
    if isinstance(node, ast.Name) and depth == 0:
        ref = ctx.assignments.get(node.id)
        if ref is not None:
            return _raw_hints(ref, ctx, depth + 1)
        if node.id in ctx.import_from and ctx.external is not None:
            resolved = ctx.external(node.id)
            if resolved is not None:
                expr, ext_ctx = resolved
                return _raw_hints(expr, ext_ctx, depth + 1)

    # Anything else: a reference or expression we can't resolve statically.
    return {key: _MISSING for key in HINT_KEYS}, True
```

**ヒントの値**: explicit になるのは次の 2 つだけである（`py_annotations.py:205-211`）。

- bool のリテラル
- 「注釈式が定義されたモジュール」のモジュール直下にある bool 定数。他ファイルから 1 段で解いた注釈なら、定義側のモジュールの定数も解ける（注釈-v13b）。

`None` のリテラルは explicit にならない。「未設定」として扱い、raw に入れないので DEFAULT になる。

- `py_annotations.py:204` `"""Resolve one hint value: True/False, None (unset), or _MISSING (unresolvable)."""`
- `:232-233` `if value is not None:` / `raw[kw.arg] = value`
- `:285-286` `if key not in raw:` / `return HintValue(default, DEFAULT)`

例外として、同じ呼び出しに `**` 展開、位置引数、camelCase の対が無い snake_case があると、`None` を書いたキーも setdefault で unresolvable になる（`:236-240`。注釈-v06a / v06b）。

属性、呼び出し、int や str のリテラル、使う側で import した bool 定数は unresolvable になる。

**モジュール定数の「1 回だけ」**: 代入の回数は `tree.body` 直下の Assign / AnnAssign だけで数える（`py_annotations.py:132-146`。143-146 は `# A name assigned more than once at module level isn't a reliable constant.` / … / `assignments.pop(name, None)`）。
if / try の中の再代入、関数内の global による再代入、AugAssign は数えない。
`RO = True` の後に `if …: RO = False` と書くと、実行時の値と逆の explicit True で照合し、high の誤警報を出した（MM-v06）。

**snake_case**: camelCase の対が無ければ、SDK の版を見ずに unresolvable にする（`py_annotations.py:234-237`、辞書は 255-260）。

```
            elif kw.arg in SNAKE_HINT_KEYS:
                snake.add(SNAKE_HINT_KEYS[kw.arg])
        for key in snake:
            raw.setdefault(key, _MISSING)  # SDK-version-dependent spelling
```

著者の理由（`py_annotations.py:28-32`、○）: 「the MCP Python SDK 1.x accepts only camelCase fields / (readOnlyHint) and silently ignores snake_case ones (read_only_hint) because / extra fields are allowed; SDK 2.x accepts both.」。
2.x 側は、このマシンに入っている mcp 2.2.0 のソースを読んで確かめた（◎ 読んだだけ。`mcp_types/_types.py:48` `model_config = ConfigDict(alias_generator=to_camel, populate_by_name=True)`）。1.x 側は確かめていない（○）。

**展開と計算キー**: `**` 展開、位置引数、計算キーがあると、明示されていないヒントを unresolvable にする。明示されたキーは setdefault なので explicit のまま残る（`py_annotations.py:236-240`、257-263）。
辞書の中の順序は見ない。そのため `{"readOnlyHint": True, **EXTRA}`（EXTRA が False で上書きする）は True と読む（B1-c03。AuthGap も同じに読む）。

**既定値**: 不在のヒントは仕様の既定値で埋め、source=DEFAULT とする（`py_annotations.py:292-300`）。

```
    read_only = resolve("readOnlyHint", False)

    if "destructiveHint" in raw:
        destructive = resolve("destructiveHint", True)
    elif read_only.source == UNRESOLVABLE:
        destructive = HintValue(None, UNRESOLVABLE)
    else:
        # Default true, but only meaningful when readOnlyHint is false.
        destructive = HintValue(not read_only.value, DEFAULT)
```

readOnlyHint が unresolvable のときに destructiveHint も unresolvable になるのは、destructiveHint が不在のときだけである。
destructiveHint を明示していれば、explicit のまま残る（注釈-v01）。ただし規則の側では照合されない（§4）。

**低レベルの `Tool(...)`**: 呼び出し名がちょうど `Tool` で、import 表で mcp に解けるものを宣言とする（`py_annotations.py:192-193`）。
属性の連鎖の根が mcp に解ける `types.Tool(...)` や `mcp.types.Tool(...)` も認める（`py_annotations.py:194-199`）。
別名の `McpTool(...)` と `mylib.Tool(...)` は対象外である。

ツール名として読める形は次の 4 つ（`py_annotations.py:345-351`）。

- 文字列リテラル
- 同じファイルのモジュール直下の文字列定数
- 同じファイルのモジュール直下のクラスの文字列属性（enum のメンバを含む）
- それを指すモジュール直下の別名（`ALIAS = Tools.WIPE`）

どれでもなければ、その宣言は**統計にも入れずに黙って捨てる**（`py_annotations.py:369-371` `name = _tool_name(node, ctx)` / `if name is None or (node.lineno, name) in seen:` / `continue`）。
f-string の名前や `Tools.WIPE.value` がこれに当たる。

宣言を集める範囲は、`list_tools` ハンドラの本体と、同じファイルのモジュール直下の def / class 以外の文だけである（`py_entry_points.py:1073-1076`、1092-1093）。
モジュール直下の if / try / with の中にあるヘルパ関数の `Tool(...)` は集まる（注釈-v04）。
次のものは集まらない（入口-c10、B1-c09、入口-c12）。

- モジュール直下の def の中
- クラス本体の中
- 別ファイル

**解決できなかったヒントの出し方**: 2 か所に出る。

- テキストの `--explain` の「Not checked (annotations couldn't be resolved statically):」に、理由を付けて出る（`analysis/annotation_mismatch.py:611-613`、`reporters/text_reporter.py:137-144`）。理由の文は 2 種類だけ: 「annotations passed by a reference that couldn't be resolved」と「non-literal or SDK-version-dependent hint values」。
- JSON の `py_entry_points[].annotations`（低レベルは `declared_tools[].annotations`）に、各ヒントの `{"value": …, "source": "explicit" | "default" | "unresolvable"}` として出る（`py_entry_points.py:305-308`）。

JSON に無いのは、理由の文の一覧 `annotation_notes` だけである（`scanner.py:445` `# Internal (not in JSON): --explain notes and lowlevel linkage counts`）。

### 3.5 呼び出しグラフ（`src/reachscan/call_graph.py`）

**節点**: (絶対パス, 修飾名) である。トップレベルのクラスの直下のメソッドは `"Class.m"`、それ以外は素の名前になる。入れ子の関数も素の名前である（`call_graph.py:460-467`）。

```
        if self._class_stack and self._func_depth == 0:
            qual = f"{self._class_stack[-1]}.{node.name}"
        else:
            qual = node.name

        self.lineno_index[node.lineno] = (qual, getattr(node, "end_lineno", None))
        fn: FunctionNode = (self._file, qual)
        self.graph.setdefault(fn, set())
```

**解決先になれる関数**（project_functions）は、`tree.body` 直下の関数と、トップレベルのクラスの直下のメソッドだけである（`call_graph.py:389-395`）。
入れ子の関数、関数の中で定義したクラスのメソッド、モジュール直下の if / try の中の def は入らない。

**解決**は 4 段だけである（`call_graph.py:507-515` ほか）。

1. 素の名前 → 同じファイルのトップレベル関数（`call_graph.py:519-521`）。ここでクラス直下のメソッドには当たらない。
2. 素の名前 → モジュール直下の import で結んだファイルの同名関数（`call_graph.py:523-525` `source = self._file_imports.get(name)` / `if source and name in self._project_functions.get(source, set()):` / `return (source, name)`）。ローカル名をそのまま元の関数名として引くので、`from util import purge as p; p()` は解決しない（CG-c02、B2-c03）。
3. `self.m()` → 同じクラス、同じファイルの `"Class.m"`。
4. `Name.m()` → その Name が import で結ばれたファイルのトップレベル関数 m（`call_graph.py:537-542`）。

4 段目には誤った結び付けがある。import したクラスを受け手にした `from mod import Klass; Klass.run(p)` が、mod.py にある無関係なトップレベル関数 `run` に結ばれた（CG-n01。high の誤警報）。

解決できない例は次のとおり。

- `a.b.c()`、`get().m()`、`super().m()`、受け手が self でないインスタンスのメソッド
- コンストラクタ（`Cleaner(p)` の `__init__`。CG-c05）

**import 表**はモジュール直下の文だけから作る（`call_graph.py:325` `for node in tree.body:`）。try / if の中の import と関数の中の import は辿らない（CG-c14、CG-c15、B2-x05）。
`from pkg import mod` の mod は `pkg/__init__.py` に結ばれるので、`mod.f()` は解決しない（`call_graph.py:344-351`。CG-c07）。`pkg.mod.f()` も解決しない（CG-c07c、B2-c03）。
`__init__.py` の再 export は、プロジェクト全体で名前をキーにした表に入り、後勝ちになる。しかも普通のモジュールからの import より優先される（`call_graph.py:351` `result[local] = reexport_map.get(local, source_file)`）。
無関係な `a/__init__.py` に `from .x import helper` があるだけで、`from b.tools import helper` が `a/x.py` に結ばれ、不一致が消えた（CG-n13。対照の CG-n13b では出る）。
絶対 import の予備手段は `root.rglob("__init__.py")` で探す（`call_graph.py:282-285`）。走査から除外される `.venv` の中のパッケージにも import が結ばれる。
木の中に `.venv/lib/python3.12/site-packages/requests/__init__.py` を置くと、`import requests` が木内扱いになって外部名から外れ、`requests.delete` の名前 `delete` が未解決名として残った。その結果、無関係な `Repo.delete` の `os.remove` が unknown になった（CG-n04b。`.venv` の無い対照 CG-n04a では unreachable）。

**解決できなかった呼び出し**: 属性呼び出しで、根が外部 import でもリテラルでもないものだけ、メソッド名を記録する（`call_graph.py:478-484`）。

```
        if self._func_stack:
            caller: FunctionNode = (self._file, self._func_stack[-1])
            callee = self._resolve_call(node)
            if callee is not None:
                self.graph.setdefault(caller, set()).add(callee)
            elif isinstance(node.func, ast.Attribute) and not self._external_root(node.func):
                self.unresolved.setdefault(caller, set()).add(node.func.attr)
```

次の呼び出しは**何も残らない**。

- 素の名前の呼び出し（入れ子関数、別名 import、コンストラクタ）
- 関数部分が Call の呼び出し（`getattr(h, "do_" + op)(p)`）
- 添字による呼び出し（`HANDLERS[name](arguments)`）

デコレータの中の呼び出しは、装飾された関数のものとして記録される（`call_graph.py:469-471`）。
そのため全ツールの `@mcp.tool(...)` が未解決名 `tool` を残し、どこからも呼ばれない `Registry.tool` の `os.remove` が unknown になった（CG-n02）。

**入れ子の関数**: docstring は「unknown になる」と書く（`call_graph.py:53-54`、○の記述）。

```
  - Nested functions appear in LinenoIndex but not in project_functions.
    Findings inside them get UNKNOWN reachability (static analysis limitation).
```

`reachability.py:22-25` も、unknown の例に「nested functions not in the call / graph」を挙げる。
`README.md:63` は unknown の例を「(method calls on instances, dynamic dispatch, parse failure)」とだけ書き、入れ子関数には触れていない（○）。
しかし実際には、入れ子の def もグラフの節点になる（`call_graph.py:466-467`）。そのため「グラフに無い → UNKNOWN」の枝に入らず、**unreachable** になる（CG-c01、入口-c21、B2-x01、B1-c05b）。
`tests/test_reachability.py:414` の `test_nested_function_finding_gets_unknown` は、inner を含まない手組みのグラフで UNKNOWN を確かめている。実際に組まれるグラフとは前提が違う。

素の名前の節点なので、同じファイルのトップレベル関数と同名の入れ子関数は 1 つの節点に合流する。
無害なトップレベルの `helper` を呼ぶツールに、別の関数の中の入れ子 `helper` の `os.remove` が付き、high の誤警報になった（CG-c12）。

### 3.6 能力の検出（`src/reachscan/detectors/`）

ファイルごとの検出器が 6 つある（`detectors/__init__.py:1-6`: shell_exec / network / file_access / secrets / dynamic_exec / autonomy）。
これに加えて、プロジェクト全体で 1 回だけ走る `client_factories` がある（`scanner.py:311`）。
出力は capability と evidence の文字列、それに数値の confidence だけである。AuthGap のような slot、値の主体、確度は持たない。confidence は不一致の判定に使われない。

検出器ごとの範囲は次のとおり。

- **shell_exec**: import 表を持たない（`detectors/shell_exec.py:21` `mod = getattr(func.value, "id", None)`）。EXECUTE になるのは 3 通りだけで、別名、from-import、`check_output`、`os.popen`、`asyncio.create_subprocess_exec` は落ちる（sink-a_exec、B2-x03）。
  - `:23` `if mod == "subprocess" and name in {"run", "Popen", "call"}:`
  - `:27` `elif mod == "os" and name == "system":`
  - `:30` `if func.id in {"exec", "eval"}:`
- **dynamic_exec**: 名前 eval / exec / compile / `__import__` と、import 元の完全名がそれで終わるものを DYNAMIC にする（`detectors/dynamic_exec.py:83` `if name in DYNAMIC_FUNC_NAMES or (full and any(full.endswith(f".{n}") for n in DYNAMIC_FUNC_NAMES)):`）。そのため `from re import compile as re_compile` が DYNAMIC になり、high の誤警報を出した（sink-a_exec）。属性形の `importlib.import_module` と `runpy.*` も DYNAMIC にする。
- **file_access**:
  - `open` のモードが `{"w", "wb", "a", "ab", "x"}` と完全一致するときだけ WRITE（`detectors/file_access.py:20`）。'w+'、'wt'、'r+'、'a+'、変数のモードは READ になる（`:97` `# treat default/read modes and unknown modes conservatively as READ`）。
  - `write_text` / `write_bytes` は受け手を問わず WRITE（`:23`）。
  - `shutil` で始まる名前の copy / copyfile / copy2 / move は WRITE（`:25`）。
  - `os` で**始まる**名前の remove / unlink / replace / rename は WRITE（`:26`、`:128` `if resolved.startswith("os") and func_attr in OS_WRITE_FUNCS:`）。
  - 同じ行の同じ capability は 1 件にまとめる（`:164` `key = (f.capability, f.lineno)`）。
- **network**:
  - 属性形の表（`detectors/network.py:16-35`）: requests / httpx の動詞、`urllib.request.urlopen`、`socket.socket`、`websockets.connect`、`websocket.create_connection`。照合は「解決名が mod で始まり attr で終わる」（`:167`）なので、属性形の `urllib.request.urlretrieve(url, p)` はどの行にも当たらず 0 件だった（sink-u_hyp）。
  - from-import した名前は `:196` `if full.endswith(full_prefix) or full == full_prefix or full.startswith(full_prefix):` で照らす。`("urllib", "request")` の行（`:30`）があるので、`urllib.request` から from-import した名前はすべて SEND になる（`urlretrieve` も `Request` も。sink-u_hyp、sink-m_misc）。
  - connect / create_connection / socket で終わる属性呼び出しは SEND（`:54`、`:179-180`。sqlite3 / aiosqlite / duckdb を除く）。
  - from-import した名前に `http` を含むものは SEND（`:213`、`:218`）。
  - HTTP クライアントを代入した変数名（スコープを区別しない）への動詞（`:43-51`、`:242`、`:245`、`:260`）。
  - 位置引数に http(s) の URL 定数がある get / post / open / fetch / send など（`:76-79`、`:297`）。
- **client_factories**: クライアントを返すトップレベル関数を 1 段だけ追う。
- **DB / SQL / ORM / クラウド SDK の書き込みを検出するコードは見つからなかった**。src の Python 側（ts_* を除く）を `sqlite|.execute|cursor|sqlalchemy|boto3|INSERT|DELETE FROM|DROP TABLE|psycopg|pymongo|redis` で検索した。

finding の risk_level は SEND / WRITE / EXECUTE / DYNAMIC / SECRETS がすべて high である（`src/reachscan/analysis/finding_enrichment.py:8-34`）。

検出器ごとの対照表は §4 の後半に置いた。

### 3.7 到達性（`src/reachscan/reachability.py`）

入口ごとに BFS をする。深さは `reachability.py:64` `TRAVERSAL_DEPTH = 8   # max call hops the BFS will follow`。
循環は visited 集合で止める。BFS 1 回あたり、訪問する節点は最大 50,000 である（`:224`、`:242-247`）。
上限の深さにある節点の子は数えるだけで辿らない（`:252-257`）。超えたことは warnings.warn で stderr に出すだけである（`:351-355`）。

```
    if total_nodes_skipped > 0:
        warnings.warn(
            f"Reachability: {total_nodes_skipped} nodes skipped — "
            "consider raising TRAVERSAL_DEPTH"
        )
```

JSON にも、テキストにも、SARIF にも、深さを超えた印は残らない。超えた先の finding は unreachable になる（B2-c01_depth、CG-c04）。
テキストは unreachable を「exist in codebase, not on any LLM call path」と表示する（`reporters/text_reporter.py:230`）。

状態は次の順で付く（`:313-316`、`:367-394`）。

1. 入口が 1 つも無い → 全 finding が no_entry_points
2. ファイルが lineno 索引に無い → unknown
3. `<module>` → module_level
4. どれかの入口から届く → reachable（全入口の最短経路で決め、同じ長さなら入口名の辞書順。`:347-349`）
5. 含む関数がグラフに無い → unknown
6. `maybe_reached` に入る → unknown
7. それ以外 → unreachable

T8a の `_maybe_reached`（`:399-432`）は、記録した未解決のメソッド名に一致する `"X.m"` 形の節点すべてを、名前だけで候補にする（`:413-415`）。

```
    for node in graph:
        if "." in node[1]:
            methods.setdefault(node[1].rsplit(".", 1)[1], set()).add(node)
```

受け手は見ない。ローカルの dict に対する `d.get()` で、プロジェクトの `Cache.get` が unknown になった（CG-c08）。
`cache.clear()` を `cache.pop()` に替えただけで、`Trash.clear` が unknown から unreachable に戻った（B2-c02 と B2-c02_ctl）。
よくある名前は unknown を広げる。到達したメソッドが `super().__init__()` を呼ぶと名前 `__init__` が残り、無関係なクラス `Danger` の `__init__` の `os.remove` が unknown になった（CG-n08b。`super` の呼び出しを除いた対照 CG-n08c では unreachable）。
トップレベル関数と、関数の中で定義したクラスのメソッドは表に載らない（CG-n03）。

モジュール直下のシングルトン `svc = Svc()` の `__init__` にある finding は、import 時に実行されるのに module_level ではなく unreachable になった（CG-n09b）。コンストラクタの呼び出しが辺にならないためである（§3.5）。

### 3.8 不一致の判定と出力

**入力**: `find_annotation_mismatches` に渡るのは、Python の finding と入口だけである（`scanner.py:323` `py_findings = [entry["finding"] for entry in findings]`、`scanner.py:418-421`）。
TS の finding は、この後で足される。そのため **TS のツールは不一致を出さない**（A-depth_probe_ts、MM-c19。`README.md:142`「TypeScript support is planned.」○）。

**デコレータのツール**: 到達集合は入口ごとの BFS の結果 `index.reached[idx]` である（`annotation_mismatch.py:480`、`:487`）。

**低レベルのツール**: 次の順で結び付ける。

1. ファイルごとに、同じファイルの `list_tools` 入口の `declared_tools` をまとめる（`:403-406`）。
2. 同じファイルで `ast.walk` を使い、最初に見つかった `call_tool` を 1 つだけ採る（`:417-421` の `break`）。
3. その第 1 位置仮引数（self / cls を除く）を選択子とする（`:422-426`）。見つからなければ、宣言は全部 unlinked になる。
4. 読む分岐は次の 2 形だけ。値はリテラル、同じファイルの定数、クラス属性（enum）。
   - 選択子との `==` の単一比較（`and` の連言の中も可）（`:275-276`）
   - ガードの無い `match` の case（`:349` `values = _case_values(case.pattern, ctx) if case.guard is None else None`）。`case "a" | "b":` は両方に結ぶ。
5. `if` / `elif` の連鎖は、名前判定でない test に当たるとそこで追跡をやめる（`:359-362`）。後ろの `elif` は結ばれない。

```
            while current is not None:
                value = _tool_name_test(current.test, param, ctx)
                if value is None:
                    break
```

結べない形の例: `in`、辞書表、選択子の再束縛、`or`、ガード付き case、別ファイルのハンドラ、2 つ目の `call_tool`。

ツールの範囲は「自分の分岐の文」と「ハンドラ本体の最上位の文のうち dispatch でないもの（共通部）」である（`:429-431`、`:440`）。

```
        branches, dispatch_nodes = _dispatch_branches(handler, params[0], ctx)
        dispatch_ids = {id(n) for n in dispatch_nodes}
        shared = [stmt for stmt in handler.body if id(stmt) not in dispatch_ids]
...
            stmts = [*branch, *shared]
```

分岐を try や with で包むと、最上位の Try / With 文が丸ごと共通部になる。他のツールの書き込みが読み取り専用のツールに付き、**誤警報**になる（入口-c08a、入口-c08c、入口-t3、MM-c02b）。

分岐から先の経路は、名前の照合で作る。分岐の文と共通部の文から呼び出し名の末尾を集め、ハンドラの callee のうち末尾名が一致するものがちょうど 1 つのときだけ、深さ `TRAVERSAL_DEPTH - 1` の BFS を足す（`:442-446`）。

```
            for name in set(_callee_names(stmts)):
                candidates = [n for n in callees if n[1].split(".")[-1] == name]
                if len(candidates) != 1:
                    continue  # unknown or ambiguous: no claimed path
```

これには 2 つの方向の誤りがある。

- 候補が 2 つあると黙って経路を落とす（入口-t13、MM-h03）。
- callee の集合はハンドラ全体のものなので、ある分岐の未解決の呼び出し（`arguments.delete("k")`、`cache.purge(...)`）が、**別の分岐が呼ぶ同名の関数**に結ばれ、誤警報になる（CG-n11、MM-v01）。

結べなかったツールは `stats.unlinked` に入るだけである。この件数（`scanner.py:447` `"lowlevel_tool_linkage": {"linked": linkage.linked, "unlinked": linkage.unlinked},`）は、JSON にもテキストにも SARIF にも出ない（`scanner.py:445` のコメント）。
宣言そのものは JSON の `declared_tools` に出るので、「宣言はあったが検査されなかった」ことは利用者には見えない。

**照合**: 明示のヒントが 1 つも無いツールは飛ばす（`:519-520`）。finding を含む関数が、そのツールの到達集合に入っていることを要件にする（`:523-527`）。

```
            node = index.containing.get(fid)
            if node is None or node not in target.reach:
                continue
            if node == target.entry_node and not _in_ranges(finding.get("lineno"), target.entry_line_ranges):
                continue
```

unknown の finding は到達集合に入らないので、ここで黙って落ちる。規則の中身は §4 に置いた。

**まとめ方**: (tool, entry file, rule) ごとに 1 件にする（`:544-548`）。経路長、file、行の順で最小のものを主の観測にし（`:586`）、残りは `additional_observations` に入れる。
`mismatch_id` は `"tool|file|rule"` の sha1 の先頭 12 桁で、file は入口ファイルの絶対パスである（`:574-576`）。
同じ server.py を別のディレクトリに置くと、ID が `1a73ed11de57` と `13669aa00376` に変わった（◎）。そのため、run をまたいだ突き合わせにこの ID は使えない。

**出力**: JSON の `annotation_mismatches`、テキスト、SARIF の 3 つ。

- SARIF では、規則 `mcp-risk-mismatch` の defaultConfiguration が error、security-severity は 8.0 で固定（`reporters/sarif_reporter.py:96-117`）。
- 結果の level は high が error、medium が warning（`:379`）。
- codeFlows に、ツールから各ホップを経て sink に至る threadFlow が入る。
- 低レベルの「declares」の位置は call_tool の def の行で、`types.Tool` の行ではない（`:365-370`）。
- 既定の SARIF に入る finding は reachable と module_level だけ（`:25` `DEFAULT_STATES = frozenset({"reachable", "module_level"})`）。不一致は常に入る。

**抑制**: 不一致を抑制できるのは、宣言の側に理由付きで付けた `reachscan:allow-mismatch` だけである。デコレータなら最初のデコレータの行から def の行まで、低レベルなら `types.Tool(` の開始行の 1 行に付ける（`suppressions.py:183-195`、`annotation_mismatch.py:458`、`:467-474`）。
sink に付けた `allow-write` などは不一致を抑制しない（MM-c15）。
抑制した不一致は出力に残り、`suppression` が付いて、終了コードから外れる。

**終了コード**: `cli.py:42-50` で決まる。

```
        if f.get("reachability") == "reachable" and f.get("risk_level") in trigger_levels:
            return 1
    # Annotation mismatches are reachable by construction (each carries the call
    # path from the tool to the sink); one without a path never gates.
    for m in results.get("annotation_mismatches", []):
        if m.get("suppression"):
            continue
        if m.get("reachability_path") and m.get("risk_level") in trigger_levels:
            return 1
```

`--severity` は既定が high である（`cli.py:9` `_SEVERITY_LEVELS = {"high": {"high"}, "medium": {"high", "medium"}}`。none は常に 0）。
終了コード 2 になるのは `scan_target` の例外だけである（`cli.py:99-103` `try:` / `results = scan_target(...)` / `except Exception as e:` / … / `sys.exit(2)`）。その後の報告器（JSON / SARIF / テキスト）の例外は捕まえない。
反証に使われる sink の finding は risk_level が high なので、sink が reachable なら、不一致があっても無くても finding の側から exit 1 になる（3.6 の末尾）。
**終了コードは不一致の信号にならない**。比較には `annotation_mismatches` の配列を数える必要がある。

---

## 4. 不一致の規則の正確な意味

規則は 3 つだけである（`annotation_mismatch.py:233-245`、◎）。

```
    ro = annotations.read_only
    if ro.source == EXPLICIT and ro.value is True and capability in _READ_ONLY_CONTRADICTIONS:
        yield RULE_READ_ONLY, "readOnlyHint", True, "high"
    ow = annotations.open_world
    if ow.source == EXPLICIT and ow.value is False and capability == "SEND" and send_kind:
        yield RULE_CLOSED_WORLD, "openWorldHint", False, "medium"
    de = annotations.destructive
    if (
        de.source == EXPLICIT and de.value is False
        and ro.value is False  # destructiveHint is meaningful only when readOnlyHint is false
        and capability == "WRITE" and is_destructive_write(evidence)
    ):
        yield RULE_NON_DESTRUCTIVE, "destructiveHint", False, "medium"
```

| 規則（JSON の rule） | 照らすヒント | 発火の条件 | 数える capability | 重大度 | 外れるもの |
|---|---|---|---|---|---|
| `read_only_contradicted` | `readOnlyHint` が explicit で True | そのツールの到達集合に capability がある | WRITE / EXECUTE / DYNAMIC（`:67` `_READ_ONLY_CONTRADICTIONS = {"WRITE", "EXECUTE", "DYNAMIC"}`） | high | SEND（HTTP の DELETE / POST を含む）、READ、SECRETS、AUTONOMY。DB は capability 自体が無い |
| `closed_world_contradicted` | `openWorldHint` が explicit で False | SEND の送信の種類が決まる | SEND のうち HTTP / websocket / socket connect | medium（docstring `:10-11` は high のまま） | socket connect でホストがリテラルの loopback（`:186-188`）。根がプロジェクト内のモジュール（`:177-178`）。DB ドライバとその他のプロトコル。EXECUTE（`curl` の起動など） |
| `non_destructive_contradicted` | `destructiveHint` が explicit で False、**かつ** readOnlyHint の値が False（明示でも既定でもよい） | WRITE の evidence 文字列が破壊的の正規表現に当たる（`:71-79`） | WRITE だけ | medium | EXECUTE（`:18-20`）、DYNAMIC、追記 'a'・'x'・mkdir・copy（`:70`「Appends, exclusive creates ("x"), mkdir, and copies are treated as additive.」）。readOnlyHint が unresolvable のとき（値が None）。readOnlyHint=true のとき |
| （無し） | `idempotentHint` | — | — | — | 抽出はする（`py_annotations.py:305`）が、規則が無い（MM-x26、B2-c05） |

**3 規則に共通する前提**（§3.8）

- 明示のヒントが 1 つ以上ある。
- 経路がある（unknown、unreachable、unlinked は数えない）。
- Python のツールである。
- (tool, file, rule) ごとに 1 件にまとめる。

**EXECUTE を destructiveHint から外した理由**（`annotation_mismatch.py:18-20`。著者の判断の記述で、○）:

```
EXECUTE doesn't count against destructiveHint: reachscan can't tell what a
command does, and on the phase-3 corpus every EXECUTE hit was a harmless
launch (V decision, 2026-10-05). It still contradicts readOnlyHint: true.
```

逆に readOnlyHint=true の側では、argv0 が定数の `subprocess.run(["ls", p])` も high の矛盾になる。

**送信の種類の決め方**（openWorldHint。`:176-196`）:

```
        if root in _HTTP_ROOTS:
            return "HTTP"
        if root in _WEBSOCKET_ROOTS:
            return "websocket"
        call = parts[-1]
        if call not in _SOCKET_CONNECT_CALLS:
            return None  # e.g. socket.socket(): creating a socket isn't an outbound connect
        host = _socket_host_literal(file, finding.get("lineno"), call)
        if host is not None and _is_loopback(host):
            return None
        return "socket"
```

- 根の名前が requests / httpx / aiohttp / urllib / urllib3 / http なら HTTP、websocket / websockets なら websocket で、**宛先は見ない**。そのため `httpx.get("http://127.0.0.1:8000/health")` も矛盾になる（B2-c07、MM-c04）。
- 根がそれ以外のときは、evidence の ` -> ` の後ろにある URL の scheme で決める（`:191-195`）。
- `_is_loopback`（`annotation_mismatch.py:102-110`）は、名前 `localhost` と `*.localhost` を loopback として扱い、それ以外は `ipaddress.ip_address(host).is_loopback` で決める（`:104-106` `host = host.strip().strip("[]").lower()` / `if host == "localhost" or host.endswith(".localhost"):` / `return True`）。`CHANGELOG.md:54` も「(`localhost`, `127.0.0.0/8`, `::1`)」と書く（○）。MM-c04 で localhost 宛ての socket が不一致 0 だったのはこのためである。
- 10/8 などの私設アドレスは外向きとして扱う（MM-c04 の 10.0.0.5）。
- `s = socket.socket(); s.connect(...)` は evidence の根が `s` になり、分類されない（B2-c07、MM-c05）。
- `asyncio.open_connection` は network 検出器が SEND にしない。そのため `_SOCKET_CONNECT_CALLS` の open_connection には、Python から届く経路が見つからなかった（MM-v08）。

`README.md:131` のループバック除外の書き方は HTTP にも掛かるように読める（○）。コード（◎）と `CHANGELOG.md:54`（○）では、除外は socket だけである。

**「破壊的な WRITE」の正規表現**（`:71-79`）には rmtree / rmdir / truncate / `w+` が入っている。しかし Python の file_access はそれらを WRITE として出さないので（§3.6）、**Python では一度も当たらない**。
rmSync / writeFile などは TS の名前である。照合には Python の finding しか渡らないので、v0.4.0 では使われない。

**Python の書き方ごとの capability と、AuthGap の kind**（すべて合成ケースで確かめた。◎）

| 書き方 | reachscan | AuthGap | ケース |
|---|---|---|---|
| `open(p, "w")` / `"wb"` / `"a"` / `"ab"` / `"x"` | WRITE | FS_WRITE | 多数 |
| `open(p, "w+")` / `"wt"` / `"r+"` / `"a+"`、モードが変数 | READ（不一致なし） | FS_WRITE。読めない変数のモードは FS_READ と FS_WRITE の両方 | B2-x02、sink-b_write_ro、MM-c09 |
| `Path(p).open("w")`、`io.open(p, "w")` | なし | FS_WRITE | B2-x02 |
| `os.open(p, O_WRONLY…)`、`os.truncate`、`Path.rename` / `replace`、`aiofiles.open` | なし | なし | B2-x02、B2-c06、sink-u_hyp、sink-b_write_ro |
| `os.remove` / `unlink` / `replace` / `rename`、`shutil.copy` / `move` | WRITE | FS_WRITE | B2-c06、B2-c08 |
| `shutil.rmtree`、`os.rmdir`、`os.makedirs`、`Path.unlink`、`Path.mkdir`、`os.chmod` | なし | FS_WRITE | B2-c06、B2-c08、A-destructive_sinks |
| `"os"` で始まる変数の `.remove` / `.replace`（`oset`、`ostrich`、`os_name`、`os.path.join(...).replace(...)`） | WRITE（誤） | なし | B2-x04、MM-v04、sink-c_destructive |
| 自作クラスの `.write_text()`、`shutil_log.copy()`（list.copy） | WRITE（誤） | なし | sink-h_extra、sink-v_prefix |
| `subprocess.run` / `Popen` / `call`（字面が `subprocess`）、`os.system` | EXECUTE | SPAWN | B2-x03 |
| 別名や from-import の subprocess、`check_output`、`os.popen`、`asyncio.create_subprocess_exec` | なし | SPAWN | B2-x03、sink-a_exec、MM-v09 |
| `eval` / `exec` | EXECUTE と DYNAMIC | EXEC | B2-x03 |
| `from re import compile as re_compile` | DYNAMIC（誤） | なし | sink-a_exec |
| `importlib.import_module`（属性形）、`runpy.*` | DYNAMIC | なし | sink-m_misc |
| SQL の `execute("UPDATE / DELETE / DROP …")`（sqlite3、psycopg） | なし | DB（`db_modify`） | B2-c04、sink-e_ro_send_db、MM-c07 |
| `requests` / `httpx` の get / post / delete … | SEND（メソッドは区別しない） | NET（メソッドつき） | B2-x07、MM-c06 |
| `requests.request("DELETE", url)`（URL が変数）、`httpx.stream` | なし | requests.request は NET（第 1 引数のメソッドを読む）。httpx.stream はなし | sink-h_extra |
| `socket.create_connection((host, port))` | SEND（socket） | なし | B2-c07 |
| `websockets.connect("ws://localhost:…")` | SEND（websocket。loopback でも矛盾） | なし | sink-u_hyp |
| `webbrowser.open("https://…")`、型の分からない受け手の `client.request("GET", "https://…")` | SEND（URL 定数の規則） | なし | sink-d_closed_world |
| `from http import HTTPStatus`、`httpx.BasicAuth`、`urllib.request.Request` | SEND（誤） | なし | sink-d_closed_world、sink-m_misc |
| 属性に持った `self.http = httpx.Client()` の `.get` | なし | NET | sink-d_closed_world |
| `client = httpx.Client(); client.delete(url)` | SEND | なし（AuthGap の O39、既知の限界） | sink-h_extra |
| 別の関数にある同名の `client` 変数（実は dict）の `.get` | SEND（誤） | なし | sink-f_clientvar |
| `os.environ[...]`、`threading.Thread(...)`、`open(p).read()` | SECRETS / AUTONOMY / READ（照合に使わない） | — | sink-u_hyp |

---

## 5. 解決できないものの扱い — AuthGap との最大の違い

**reachscan の扱い**（◎ コードと実行）は、次のどれかに分かれる。

1. **unknown として残るが、ツールには付かない**。インスタンスのメソッド呼び出し（`Store().save`、`STORE.save`、`self._store.save`、`svc.run → self.store.delete`）がこれに当たる。名前の一致する `"X.m"` に届けば、finding は unknown になる。
   unknown は不一致にも終了コードにも数えず、既定の SARIF にも出ない。どの入口から届きうるのかも書かれない（`py_entry_points.py:295-309` の `as_dict` が出すのは `reachable_findings` だけ）。
   README も「They can't produce an annotation mismatch and don't affect the exit code.」と書く（`README.md:73`、○。コードと実行の結果も同じ、◎）。
   実行では CG-c03、B2-c02（4 経路）、MM-c10 がすべて unknown、不一致 0、exit 0 だった。
2. **unreachable と断定される**。docstring と README が unknown と説明しているものも含まれる。
   - 入れ子の関数（CG-c01、B2-x01）
   - `getattr(...)()`（CG-c06）
   - 辞書による dispatch（B2-x01）
   - コンストラクタ（CG-c05）
   - 別名 import（CG-c02、B2-c03）
   - `pkg.mod.f()`（B2-c03）
   - try の中の import と関数の中の import（CG-c14、B2-x05、CG-c15）
   - モジュール直下の if の中の def（CG-n06、B2-c10）
   - 関数の中のクラス（CG-n03）
   - 深さ 8 を超えた先（B2-c01_depth。stderr の警告だけ）

   テキストでは「not on any LLM call path」と表示される。これは「調べた結果、届かない」と区別がつかない。
3. **入口にならない**。§3.3 の書き方がこれに当たる。finding は no_entry_points か unreachable になり、注釈も読まれない。
4. **宣言を捨てる、または検査しない**。
   - 名前が非リテラルの `Tool(...)` は統計にも入らない。
   - 低レベルで結べないツールは、件数を出さない。
   - readOnlyHint が unresolvable なら、destructiveHint=false が明示されていても検査しない。このことは Not checked にも出ない。`unresolvable_annotations` は source が unresolvable のヒントしか並べないためである（`annotation_mismatch.py:608`）。
5. **unresolvable として開示される**。ヒントの値が解けないものは、`--explain` の Not checked と JSON の source=unresolvable に出る。ヒントの値については、ここは AuthGap より丁寧である（§8）。

なお、finding の状態としての unknown も出力には出る。JSON では各 finding の `reachability: "unknown"`、テキストでは Reachability Summary の件数である（`reporters/text_reporter.py:233-237` `f"{len(unknown):>4} unknown       — reachability not determined "`）。`docs/related_work.md:267` も「reachscan の `unknown` の件数」を挙げている。
つまり reachscan は**走査単位の状態別の件数は出す**。出さないのは、ツール単位・注釈単位の率であり、unknown を不一致の判定に使わない。

**AuthGap の扱い**（◎）: 値と効果に `opaque(reason)` を付ける。

- val 側の語彙は 8 種（`authgap/ir.py:126-137`。`:129` `"unresolved",  # 木内で解決できない呼び出し`）。ゲート側の OPAQUE も 8 種で、別の語彙である（`ir.py:140-151`）。
- `ir.py:169` は Prov について `**決して clean に潰さない。決して drop しない。**` と書く。
- 末尾名だけで降りた経路の効果には `opaque(unresolved)` を合流し、同じ行に CONTRADICTION と行の UNKNOWN を並べる（`authgap/val/engine.py:1038-1041`、`authgap/effects.py:243`）。
- 候補が 2 つ以上なら降りず、`unresolved_in_tree_calls` に件数を残す。
- 判定は矛（CONTRA）と不（CONTRA_UNKNOWN）に分ける（`authgap/dparse.py:241-242`）。
- **語の注意**: 「不」と行の verdict の `UNKNOWN` は別のものである。
  - 「不」は宣言との照合の結果で、行の notes に `contradiction_unknown:D1:spawn_command` のように出る（`dparse.py:242` `CONTRA_UNKNOWN = "unknown"`）。
  - `UNKNOWN` は行の verdict で、効果の値の確度が resolved でない行に付く（`authgap/verdict.py:180-181` `if unresolved or value.prov.kind != "resolved":` / `row.verdicts.add("UNKNOWN")`）。
  - 定数コマンドの起動は「不」だが、行の verdict に `UNKNOWN` は付かない（A-depth_probe_py の生の出力: `ROW subprocess.run SPAWN argv0 line 16 verdicts= [] … notes= [... 'contradiction_unknown:D1:spawn_command']`）。
  - 論文で「UNKNOWN の件数」と書くと、どちらを数えたかで数が食い違う。本ノートでは、前者を「不（`contradiction_unknown`）」、後者を「行の UNKNOWN」と書く。
- 木単位の opaque 率は `probe_json` の `opaque_ratio_*`（`authgap/report.py:238-239`）にある。

**ただし AuthGap の「落とさない」にも範囲がある**（検証の訂正。◎ 実行）。

- 降りなかった呼び出しの先にある効果の**行**は残らない。深さ 4 を超えた先（B2-c01_depth の chain5・chain8・chain9）、`getattr`（CG-c06）、lambda（B2-x01）、辞書の dispatch（B2-x01）では、効果の行は 0 本である。CONTRADICTION も行の UNKNOWN も立たず、残るのはユニット水準の `opaque_reasons`（`depth` や `unresolved`）と `cap_hits` だけである。`authgap scan` の manifest には `opaque_ratio_*` が無い（CG-c06 の manifest のキーで確認）。
- 非リテラルのヒントの値は、`authgap/entries.py:2756-2759` の `except (ValueError, TypeError, SyntaxError):` / `pass` で黙って捨てられる。捨てられるのは**そのキーだけ**で、D_unknown の印は付かない。
  - 上界を動かすほかのキーが残らなければ、結果は ⊥（宣言なし）になる（B1-c02 の bool 定数、B1-c06 の 3 件、MM-c13、MM-v06）。
  - ほかのキーが残れば ⊥ にはならず、**宣言の種類が変わる**。`readOnlyHint=非リテラル` と `destructiveHint=False` の組は D2 になる（`dparse.py:212` `if destructive is False and read_only is not True:`。B1-c06 の mixed_nonliteral、MM-c11）。readOnlyHint の値が真なら本当は D1 が当たり、destructiveHint は意味を持たない。
  - reachscan はこれらの値を Not checked に出す。
- モジュール直下の辞書表のキーは dispatch の候補にならない（`authgap/entries.py:2615` `for node in ast.walk(fn):`）。入口-c09 の zap は、宣言の join からも件数からも黙って外れた。
- ほぼ全ユニットの `opaque_reasons` に `unresolved` が立つ。そのため、ユニット水準の印から個別の未解決を見分けられない。どの呼び出しが立てているかは特定していない（不明）。

**まとめ**: 違いは「決められないものを数えて出すか」にある。

| | reachscan | AuthGap |
|---|---|---|
| 効果に届いて未解決のとき | unknown（ツールに帰属しない。不一致・終了コードに入らない） | 同じ行に CONTRADICTION と行の UNKNOWN（末尾名で降りたとき） |
| 降りなかったとき（深さ超過・動的） | unreachable と断定（深さだけは stderr に警告） | 行は出ないが、ユニットに opaque(reason) が残る |
| ヒントの値が決まらないとき | unresolvable として Not checked と JSON に開示 | 一部は D_unknown。非リテラルの値はそのキーごと黙って捨て、⊥ に混ざるか、宣言の種類が変わる |
| 件数・率の報告 | 走査単位の状態別の件数は出す（テキストの Reachability Summary、JSON の `reachability`）。ツール単位・注釈単位の率は出さず、unknown を不一致の判定に使わない | F0a の probe が slot の opaque の率を出す（`probe_json` の `opaque_ratio_*`。`authgap scan` の manifest には無い） |

AuthGap の新規性として書けるのは「未解決を扱う」ことではない。reachscan も unknown を持ち、その件数も出す。
書けるのは、`docs/related_work.md:268-269` と同じ狭さの「Python で、効果の単位の `opaque(reason)` の率を主な結果にした例は見つからなかった」までである。
その率として今あるのは、F0a の probe が出す slot の率（`opaque_ratio_primary_slots` / `opaque_ratio_all_slots`。`authgap/report.py:238-239` は `probe_json` の中にある）だけである。
論文で書くときは、上の穴も併せて書く。降りなかった先の効果は行が 0 本になる（B2-c01_depth の chain5・chain8・chain9 は `opaque_reasons: ['depth']` だけ）。ほぼ全ユニットに `unresolved` が立つ。非リテラルのヒントの値は黙って捨てる。

---

## 6. 評価の主張と、その強さ・弱さ

**著者が示している評価**（すべて ○、著者の主張・未検証）

- **PR #32**（v0.3.0）: 「Phase-3 corpus (38 repos + the official git server)」で不一致は 16 件、内訳は read-only 15・closed-world 1。「1 confirmed true positive in a third-party server: a tool declares openWorldHint: false but POSTs to a remote API.」「Details are kept out of this public PR.」とある。
- **PR #32 の「Precision fixes made during review」**:
  - closed-world の FP 52 件は、あるプロジェクトの自前の loopback bridge から出ていた。「The fix is in the rule, not the detector, so findings are unchanged.」
  - 「9 destructiveHint hits came from app launches.」「Per the agreed decision, EXECUTE no longer counts against destructiveHint.」
  - openWorld の改訂の見出しは「decision C, modified」で、「16 → 16 mismatches, the same set.」
  - read-only の 15 件は「That contradicts the hint as written (it starts a process), so they're kept.」として残した。
- **PR #42**（0.4.0、phase-3、38 repo、0.3.2 で）:
  - 「Every call path was checked against the source and is a real chain to a real sink.」
  - 15 件は davinci の `get_*` ツールが `get_resolve()` → `_launch_resolve()` → `subprocess.Popen(...)` で DaVinci Resolve を起動するもの。これが readOnlyHint に反するかは「the spec ambiguity raised on SEP-2793」として残している。
  - closed-world の 1 件は awslabs の `suggest_aws_commands`。「Confirmed by hand, with a fix proposed upstream」で、上流の PR `awslabs/mcp#4734` へのリンクがある。WebFetch によると、この PR の作者は vinmay で、状態は Open。本文は「Spotted while testing ReachScan's annotation checks, then traced by hand.」と書いている。
  - 「8-server registry sample: the same, no changes.」
- **PR #28**: 「Corpus totals: 906 FastMCP tools and 45 lowlevel tools; 85 declare annotations; 54 have at least one explicit hint.」。
  走らせたスクリプト `tools/run_phase3_scans.sh` は、公開 repo のどのブランチにも PR ref にも見つからなかった（◎ `git log --all -- 'tools/*'` と全 rev の `git grep`）。
- **CHANGELOG**:
  - 0.3.1（`CHANGELOG.md:42`）: lowlevel の linked が 28 → 45、unlinked が 29 → 12。
  - 0.4.0（`CHANGELOG.md:19`）: 「110 of 1,257 unreachable Python findings become unknown (7 repos); exit codes, combined risks, and annotation mismatches are unchanged.」
  - 0.3.2: TS の入口が 366 → 690、16 repo の exit が 0 → 1 など。
- **README の FP 率 0.47%**（`README.md:216`、`:226`、`:230`）: 10 の agent リポジトリ、約 3,900 ラベルでの値である。これは **Python の能力検出器の監査であって、不一致の評価ではない**。`git log -S'0.47%'` の最古は `7e8cbe6`（2026-02-27）で、到達性解析（02-28）より前に書かれている（◎）。ラベラー、基準、データは見つからなかった。

**「規則は結果を見てから決めた」ことの記録**

- 「V decision」の語は、コードのコメント 2 か所とテスト 1 か所にだけある（◎ grep）: `annotation_mismatch.py:20`、`:87`、`tests/test_annotation_mismatch.py:188`。指しているのは、EXECUTE を destructiveHint から外すことと、openWorldHint を 3 種の送信に絞ることである。
- PR #32 はこれを「agreed decision」「decision C, modified」と呼ぶ（○）。
- 公開されている最初のコミット `65c8ca6` の時点で、EXECUTE の除外と loopback bridge の除外は既に入っている（◎）。つまり**直す前の規則は公開の git に残っていない**。
- openWorldHint を medium に下げた理由（`7dc4104`）は、コミット、PR #42、CHANGELOG のどこにも見つからなかった。

**この評価の弱さ**（推論。根拠の水準は各項目の括弧内）

1. **母集団が非公開**で、再現できない。38 repo の一覧、選び方、版が出ていない（○）。registry sweep（上位 300）の結果も非公開で、「responsible disclosure only」と明記されている（`refs/pull/39/head` の `research/registry_scan/README.md:16`、◎）。
2. **規則を同じ corpus の結果を見て直している**。事前の固定と凍結は見つからなかった（◎ repo と PR の範囲）。別データについては、著者は別の小さな標本（registry の 8 サーバ）でも同じだったと書く（PR #42「8-server registry sample: the same, no changes.」○）が、その構成と結果は公開されていない。
3. **件数が小さく偏っている**。不一致 16 件のうち 15 件が 1 サーバの同じ形（アプリの起動）で、意味のうえで確認された TP は 1 件だけである（○）。
4. **再現率（見逃し）を測った記録は見つからなかった**。§5 のとおり、unknown や unreachable に落ちたもの、結べなかったツールは不一致として出ないので、見逃しは出力からは数えられない。合成ケースでは見逃しの型が多数見つかった（§7）。野外での頻度は不明。
5. **判定者と判定の手順の記録は見つからなかった**。判定の基準も見つからなかった。決定者は不明である（§2 と §10。PR の「agreed decision」「your decision」からは著者以外がいる可能性も読めるが、推測）。
6. **0.47% は不一致の精度ではない**。不一致の精度の数値は、16 件の経路を確かめたという記述だけである。
7. 2026-10-04〜07 の 4 日で 5 版（v0.2.0〜v0.4.0）を出しており、数値の版がまちまちである（0.3.2 で数えた、など）。

**強いところ**（◎）

- 不一致ごとに、入口から sink までの経路（JSON の `reachability_path`、SARIF の codeFlows）を出す。人が確かめやすい。
- 明示のヒントだけを照らすので、既定値で主張させない（ただし readOnlyHint の既定値 false は、D2 を検査する条件として使われる）。
- テストがある（◎ AST で数えた）。`tests/test_py_annotations.py` はテスト関数 34。`tests/test_annotation_mismatch.py` は HEAD でテスト関数 32、parametrize を展開すると 67。
  PR #32 の「57 tests」は PR head `87aad16` の数（28 関数、展開すると 57）、「(42 tests)」は `65c8ca6` の数（26 関数、展開すると 42）と一致した。
- 決定論的に動く（probe A）。
- 実際に第三者のサーバの修正提案にまでつなげている（○）。

---

## 7. 実際に動かした結果

**環境**（◎）

- reachscan 0.4.0: scratch venv（`$SP/rs_venv`、CPython 3.12.3）に clone から入れた CLI。site-packages の `reachscan` と clone の `src/reachscan` は `diff -r -x __pycache__` で同一だった。PyPI の 0.4.0 wheel と同一かは確かめていない。clone は実行の後も `git status --ignored` が空。
- AuthGap: HEAD `8fbbed4` の `.venv`（CPython 3.10.20）で `python -m authgap scan <木> --population mcp_server`。
  - `authgap/` の 27 ファイルの sha256 は `docs/fingerprint.json` の implementation_sha256 と全部一致した。
  - fingerprint の analyzer_commit は `b87c022` である。`docs/decisions.md:3705-3708` は、`analyzer-freeze-3` をこの解析器の版（9dc3bc3）に打ち直したと記録し、fingerprint の tag 欄が `analyzer-freeze-2` のままであることも書いている。
  - タグそのものは、ローカルに無いので確かめていない。
  - probe A の 4 入力（depth_probe_py と fixtures の 3 つ）と、B1・B2 の全入力で `--determinism 3` がバイト一致した。
- `$SP` は `/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad`。ケースの置き場は付録にまとめた。

**読み方の注意**: §7.3 の合成ケースは、**両者の違いが出そうな書き方を、コードを読んだうえで狙って作ったもの**である。件数は頻度を表さず、どちらが野外で多く見つけるかの証拠にはならない。

さらに**作り方が非対称**である。合成ケースの大半は、reachscan のコードを読んでその弱点を狙って作った。AuthGap の弱点を狙って作ったケースは少ない（B1-c04b、B1-c07ctl_attribution、B2-c02 name_only_match などは、reachscan を調べる途中で見つかったもの）。
そのため表に「RS 見逃し」が多いのは、この作り方の偏りによる。両者の優劣を示すものではない。

また、両者が**規則の選び方として**違う判断をしているところは「設計の違い」と書き、「見逃し」とは書かない。
例: 定数コマンドの起動を readOnlyHint の矛盾にするか、HTTP の loopback を宣言内とするか、`shutil.copy` を破壊的とするか、テストのパスを読むか。

### 7.1 depth_probe（`evidence/related_work_20261002/depth_probe/` の写し。sha256 一致）

| 道具（版） | `body_write`（0 段） | `helper_write`（1 段） | `helper_purge`（1 段、destructiveHint=False も宣言） | 水準 |
|---|---|---|---|---|
| HintLint（5a51f2a4、Python の経路） | 指摘 | 指摘なし | 指摘なし | △（`docs/related_work.md` 144-148 行の記録。再実行していない） |
| HintLint（同、TS の同じ形 `server.ts`） | — | 指摘（`typescript-local-callgraph`、深さ 1） | — | △ |
| mcp-doctor（4def567） | 指摘 | 指摘なし | 指摘なし | △ |
| **reachscan 0.4.0（Python）** | `read_only_contradicted` high。WRITE `with open(..., mode='w')` server.py:21、経路 [body_write] | high。server.py:10、経路 [helper_write, _save] | high。WRITE `os.remove()` server.py:15、経路 [helper_purge, _purge]。EXECUTE `subprocess.run()` :16 は additional_observations | ◎ |
| **reachscan 0.4.0（TS）** | — | 入口は helper_write（server.ts:11）。WRITE `fs.writeFileSync()` server.ts:8 は reachable、経路 [helper_write, save]。**不一致 0**（TS の注釈は読まない） | — | ◎ |
| **AuthGap（8fbbed4）** | CONTRADICTION D1 `fs_write`（:21） | CONTRADICTION D1（:10、witness [_save]） | CONTRADICTION D1（:15、witness [_purge]）。`subprocess.run(["rm","-rf",…])` は argv0 が定数なので不（`contradiction_unknown:D1:spawn_command`。行の verdict は空で、行の UNKNOWN は付かない） | ◎ |

**結論**

- Python では、reachscan はこの probe で AuthGap と同じく 3/3 のツールを指摘する。記録にある HintLint の Python の経路と mcp-doctor を上回る。HintLint が「規則に無く見つからない」とした `os.remove` も、reachscan は WRITE として拾う。
- TS では、reachscan は効果まで届くのに宣言と照らさないので、HintLint の TS の経路に及ばない。AuthGap は Python 専用で、TS は units 0 だった。
- helper_purge の `destructiveHint=False` は、どちらの道具も検査しない。readOnlyHint=true が同時にあるためである（reachscan `:242`、AuthGap `dparse.py:212` と `:584-592`）。
- EXECUTE / SPAWN の扱いは違う（設計の違い）。reachscan は常に矛盾、AuthGap は argv0 / shell_string をモデルが選べるときだけ矛盾とし、それ以外は不とする（`dparse.py:377-378`）。

### 7.2 fixtures（写しに走らせた。期待値ファイルは読んだだけで、変えていない）

| 入力 | 内容 | reachscan | AuthGap | 差の理由 |
|---|---|---|---|---|
| `fixtures/entries` | FastMCP の 2 ツール、低レベル call_tool、list_tools の無いモジュール直下の `TOOLS` | 不一致 0。`TOOLS` を読まない（宣言を集めるのは list_tools 入口があるときだけ。`py_entry_points.py:1092-1093`） | CONTRADICTION 0。`TOOLS` は読んで join したが、`subprocess.run(["git", …])` は不（`contradiction_unknown:D1:spawn_command`。行の verdict に UNKNOWN は無い） | 理由が違う。reachscan は宣言を読んでいない。AuthGap は読んだうえで不とした |
| 対照 A-entries_ctl_listtools（list_tools を足しただけ） | | git_log に `read_only_contradicted` high（EXECUTE `subprocess.run()` :17、経路 [handle_call_tool, git_log]）。run_shell の snake_case は Not checked | 同じ（不） | 設計の違い（EXECUTE / SPAWN の規則） |
| `fixtures/destructive_sinks`（`expected.json` と比べた） | destructiveHint=False の 9 ツール | **AuthGap の規則に照らすと 5/9 一致**。nd_rmtree・nd_mixed（`shutil.rmtree` を検出しない）、ro_mkdir（`os.makedirs` を検出しない）、nd_unknown_mode（変数のモードを READ にする）の 4 件が食い違った。4 件とも矛盾を出さない向き | **9/9 一致（作りから当然）** | 効果の語彙と、モードが不明なときの倒し方。下の注意を参照 |
| `fixtures/dispatch_join`（`expected.json` と比べた。期待値は AuthGap の規則から書いたもの） | list_tools と call_tool。共通部に `os.makedirs`、名前が環境変数の宣言 | 不一致 0（makedirs を検出しない）。`Tool(name=DYN_NAME)` は黙って捨て、件数も出ない | 期待どおり CONTRADICTION 1（:35 の makedirs が両ツールに帰属。read_note の D1）。unjoined_literals=1 | 効果の語彙。結び付けは同じ方向 |
| 対照 A-dispatch_join_ctl_remove（:35 を `os.remove` に替えた） | | read_note に high（dispatch=lowlevel、経路 [call_tool]） | 同じ行に CONTRADICTION | 一致。共通部の帰属は両者とも働く |

**注意（fixtures の比較は循環している）**: `fixtures/destructive_sinks/expected.json` と `fixtures/dispatch_join/expected.json` は、AuthGap 自身の規則から書いた期待値で、AuthGap の単体テストにもなっている（◎）。

- `fixtures/destructive_sinks/expected.json` の `"_note": "D32 / prereg §5 #7 の規則から書いた期待値。実装より先にコミットする。"`
- `tests/test_destructive_sinks.py:3` と `tests/test_dispatch_join.py:3` は、どちらも「期待値 … は規則から書き、実装より先にコミットした」と書く。

したがって AuthGap の 9/9 は作りから当然であり、どちらが正しいかの証拠にはならない。reachscan の 5/9 も「AuthGap の規則に照らした一致数」であって、精度や正しさの比較としては引かない。
たとえば ro_mkdir（`os.makedirs` を D1 の矛とする）と nd_unknown_mode（モードが分からない書き込みを D2 の矛とする）は、AuthGap の規則の選択である。

### 7.3 合成ケース（差の向きで整理。すべて ◎）

記号: 「RS」は reachscan、「AG」は AuthGap。
「RS 見逃し」「AG 見逃し」は矛盾を出さない誤 clear の向き、「誤警報」は矛盾を出す false-dirty の向き。
「設計の違い」は、両者が規則として違う選択をしているもので、どちらかの誤りとは言えない。
「対象の違い」は、片方が対象にしていないもので、矛盾の見逃しではない。
AuthGap の「不」は `contradiction_unknown`、「行の UNKNOWN」は行の verdict である（§5 の語の注意）。

**7.3.1 入口と登録の形**

| ケース | 書き方 | RS | AG | 差 |
|---|---|---|---|---|
| 入口-c02、B1-c11 | 工場関数 `create_server()` の中の `@srv.tool` / `@mcp.tool(...)` | 入口にならない。効果は no_entry_points か unreachable | CONTRADICTION | RS 見逃し |
| 入口-c03 | モジュール直下の `@Holder.mcp.tool`（3 段） | 入口にならない | CONTRADICTION | RS 見逃し |
| 入口-t2 | メソッドの中の `@self.server.call_tool()` | 入口 0 | `mcp-lowlevel-v1:S._setup.call_tool` で CONTRADICTION | RS 見逃し |
| 入口-c16 | モジュール直下の if / try の中の `@mcp.tool` | 入口にならない | CONTRADICTION | RS 見逃し |
| 入口-c04、MM-v10、B1-c05a | `mcp.add_tool(fn, annotations=…)`、`mcp.tool(…)(fn)` | 入口にならず unreachable（B1-c05a は exit 0） | CONTRADICTION（`catalog/entries.py:138` の `"add_tool"`、`entries.py:1568-1571`） | RS 見逃し |
| B1-c05b | クラス本体の `@staticmethod` ＋ `@mcp.tool` / `self.mcp.tool(…)(self.m)` / `self.mcp.add_tool` / メソッド内の入れ子 | 1 つ目だけ | 4 つとも | RS 見逃し 3 |
| 入口-c26 | `Server("demo", on_call_tool=h)`（低レベル v2） | 入口 0 | `mcp-lowlevel-v2` のユニット | RS 見逃し |
| 入口-c08b、B1-c04a | `serve()` の中の低レベルハンドラ | 検出する | 検出する | 一致 |
| 入口-c05、入口-c06、B1-c08 | 受け手が `fastmcp.FastMCP()`、別モジュールの `my_server`、工場関数の戻り値 | framework が langchain_or_crewai / unknown になり、注釈を読まない。Not checked にも出ない | CONTRADICTION | RS 見逃し |
| 入口-t14 | 同じファイルに `from langchain_core.tools import tool` | `@mcp.tool` も langchain 0.95 になり、不一致 0 | CONTRADICTION | RS 見逃し |
| 入口-c17 | `name` 属性の無い BaseTool 派生 | 入口にならない | ユニット | 対象の違い（注釈の無い非 MCP のツール。矛盾の見逃しではない） |
| 入口-c31 | agno Toolkit のメソッド、gptme ToolSpec、AutoGPT command、langroid ToolMessage | unreachable か入口 0 | 4 ユニット | 対象の違い（同上） |
| 入口-t1 | agno Toolkit の直後に、ツールでない `class Janitor: def _run` | `Janitor._run` の `os.remove` が reachable（誤） | ユニットにしない | RS 誤り |
| 入口-c30 | pydantic_ai `@agent.tool_plain`、AutoGen `@register_for_llm`、LlamaIndex、DSPy、MetaGPT `@register_tool` | 入口として 5 つ列挙（MetaGPT のクラスは起点が決まらず unreachable。別名の SwarmAgent は落ちた） | ユニット 0 | 対象の違い（AuthGap の 14 規則の外。注釈の無い非 MCP のツールで、矛盾の見逃しではない。c17・c31 と対称） |
| 入口-c13、sink-g_bom、MM-c18 | 先頭に UTF-8 BOM | 入口 0、finding 0、exit 0 | CONTRADICTION | RS 見逃し |
| 入口-c14、B1-c12、B1-c10 | 祖先のディレクトリが `test`、木の中の `tests/`・`benchmarks/`・`test_server.py` | 走査しない（B1-c12 は 0 ファイル、exit 0） | CONTRADICTION | 設計の違い（RS はテストのパスを除く。野外では `tests/` や `benchmarks/` の中は誤警報の源にもなりうる。AuthGap の母集団のスクリプトがテストのパスをどう扱うかは不明。B1-c10）。祖先の名前で木全体が 0 ファイルになるのは、比較の置き場所の落とし穴（入口-c14、B1-c12） |

**7.3.2 注釈の書き方**

| ケース | 書き方 | RS | AG | 差 |
|---|---|---|---|---|
| B1-c01a | mcp 2.x 形の木で `ToolAnnotations(read_only_hint=True)` と `{"read_only_hint": True}` | unresolvable。Not checked に出て、不一致なし（camelCase を含む 2 ツールは high） | 版を ge2 と決め、camelCase に写して 4/4 CONTRADICTION | RS 見逃し 2（2.x では snake_case が正規の宣言） |
| B1-c01b | 同じものを mcp 1.x 形の木で | 同じ | snake の 2 件は malformed（宣言なし） | 一致（記録の仕方が違う） |
| B1-c01c | 版が決まらない木で | 同じ | D_unknown | 一致（どちらも未検査として残す） |
| B1-c02 | 同じファイルの注釈定数、import した注釈定数、bool 定数 `RO = True`、2 回代入、辞書定数 | 4/5 で high。2 回代入は unresolvable（Not checked） | 0/5。4 件は unreadable（D_unknown）、bool 定数は ⊥（黙る） | AG 見逃し 4 |
| MM-v06 | `RO = True` の後に `if …: RO = False` | explicit True として high | ⊥ | RS 誤警報 |
| B1-c03 | `{"readOnlyHint": True}` / `dict(readOnlyHint=True)` / `ToolAnnotations(**{…})` / `{"readOnlyHint": True, **EXTRA}`（EXTRA が False） | 辞書は検出。`dict()` と `**{}` は Not checked。最後は True と読んで high | 辞書と `**{}` は検出。`dict()` は D_unknown。最後は True と読んで CONTRADICTION | `**{}` は AG だけが読む。最後は**両者に共通の誤警報** |
| B1-c06 | `readOnlyHint=os.environ.get(…)=="1"`、関数の戻り値、`bool(os.getenv(…))`、工場関数、`is_read_only()` ＋ `destructiveHint=False` ＋ `os.remove` | 不一致 0、5 件とも Not checked | 3 件は ⊥（黙る）。工場関数は D_unknown。最後は D2 CONTRADICTION（readOnlyHint のキーだけを捨て、残った destructiveHint=False で D2 になった。`dparse.py:212`） | 最後の 1 件は、矛という AG の**結論**は値によらず正しい（真なら D1、偽なら D2 で、どちらでも `os.remove` は矛盾）。ただし D2 という**理由**は値しだいで、正しいとは限らない（真なら D1 が当たり、destructiveHint は意味を持たない）。RS は readOnly が unresolvable なので D2 を飛ばす。3 件の ⊥ は AG の規則 4 上の穴 |
| 入口-c11、B1-c09 | `from mcp.types import Tool as McpTool` | 宣言として読まない | 読まない | 共通の見逃し |
| 入口-c11 | `ToolAnnotations as TA` | unresolvable（Not checked） | unreadable（D_unknown） | 一致（どちらも開示） |
| 注釈-v14（RS）。AG 側は別の入力 `annx_probe` の c13_enum_name | `serve()` の中で `Tool(name=Tools.WIPE)`（str Enum）と `match name: case Tools.WIPE:` | high（dispatch=lowlevel） | join の段で外れる（literal name=None、unjoined=1）。これは読み手が AuthGap の抽出関数（`annx_probe/scripts/ag_units.py` ほか）を走らせた結果で、`authgap scan` は走らせていない | ◎ と言えるのは AG の join の段（unjoined=1）まで。同じ入力で判定まで通したかは未確認。名前を enum で書いた Tool が join されないこと自体は、B1-c07 の `authgap scan` でも見えた（unjoined_literals=2） |
| MM-x26、B2-c05 | `idempotentHint=True` で `open(p, "a")` | 規則が無い | D4 CONTRADICTION `fs_append` | RS 対象外 |

**7.3.3 低レベルの dispatch**

| ケース | 書き方 | RS | AG | 差 |
|---|---|---|---|---|
| 入口-c08a、入口-c08c、MM-c02b | 分岐を try で包む | readOnlyHint=True の読み取りツールに、他の分岐の `os.remove` で high | 分岐に正しく帰属させ、矛盾なし | RS 誤警報 |
| 入口-t3 | `with contextlib.suppress(Exception):` で包む | 同じ誤警報 | 矛盾なし | RS 誤警報（`async with` は未実行） |
| 入口-c09、MM-v02 | `if name in ("wipe", …)` | 結べず 0 | CONTRADICTION（`entries.py:2620`） | RS 見逃し |
| 入口-c09 | `tool = name; if tool == "erase"` | 0 | CONTRADICTION。ただし変数が選択子かどうかを確かめずに読んだ結果（`analyze.py:635-644`） | RS 見逃し |
| 入口-c09、B1-c09 | モジュール直下の `HANDLERS[name](arguments)` | 0（先は unreachable） | 効果の行なし。zap は宣言の join からも件数からも黙って外れる | 両方見逃し |
| MM-v03、B1-c07 | elif の連鎖の途中に `name.startswith(…)` や `name == ToolName.PURGE.value` | それより後ろのツールが結ばれず 0（B1-c07ctl_chain_order で順序を替えると出る） | v03 は CONTRADICTION | RS 見逃し |
| B1-c07ctl_attribution | モジュール定数・enum メンバとの `==`（他のツールは readOnlyHint=False を明示） | 正しく memo だけ | 他のツールの書き込み 3 行を memo に寄せ、CONTRADICTION（`entries.py:2618` は Constant しか読まない） | AG 誤警報 3 |
| B1-c04b | `match name:` | 正しく save だけ | erase の `os.remove` にも CONTRADICTION（全ツールに帰属。`analyze.py:655-656`「その効果は全ツール帰属になる（保守的）。」） | AG 誤警報（設計上の保守側） |
| 入口-t4 | 同じファイルの `serve_a` と `serve_b` に、それぞれ call_tool | 2 つ目の wipe_b は 0（`:417-421` の break） | `serve_b.call_tool` で CONTRADICTION | RS 見逃し |
| 入口-t13、MM-h03 | 2 つの分岐が、末尾名の同じ `a.purge` と `b.purge` を呼ぶ | 経路を作らず 0 | CONTRADICTION | RS 見逃し |
| CG-n11 | 読み取りツールの分岐の `arguments.delete("k")` が、別の分岐の `util.delete` に結ばれる | high（誤） | D1 CONTRADICTION ＋ 同じ行に行の UNKNOWN | RS 誤警報。AG も矛を立てるが不明の印を付ける |
| MM-v01 | 読み取りツールの分岐の `cache.purge(...)` と、別の分岐のモジュール関数 `purge` | high（誤） | 矛盾なし | RS 誤警報 |
| 入口-c10、入口-c12、B1-c09 helper_listed | ヘルパ関数の中、または別ファイルで Tool を宣言 | 0 | CONTRADICTION | RS 見逃し |
| MM-h09 | dispatch の前に共通の書き込み | 読み取りツールに high | D1（全ツールに帰属） | 一致 |

**7.3.4 呼び出しの解決と深さ**

| ケース | 書き方 | RS | AG | 差 |
|---|---|---|---|---|
| B2-c01_depth、MM-c20、CG-c04 / c04b | 補助関数を N 回呼んだ先で書く | N≤8 で high。N=9 は unreachable（stderr の警告だけ） | N≤4 で CONTRADICTION。N≥5 は効果の行 0、ユニットに `opaque(depth)` と `cap_hits` | 深さ 5〜8 は RS だけが出す。9 以上はどちらも出さない |
| CG-n05 | 同じ sink に、別のツールからは 2 hop、readOnly のツールからは 9 hop | finding は「reachable（別のツール）」と表示。readOnly のツールの不一致はなし | readOnly のツールは opaque(depth) | どちらも出さない（RS の表示は誤解を招く） |
| CG-c03、B2-c02（4 経路）、MM-c10 | `Store().save`、`STORE.save`、`self._store.save`、`H.store.purge` | unknown、不一致 0、exit 0 | 受け手の型で解決し CONTRADICTION | RS 見逃し |
| B2-c02 name_only_match | dict の `cache.clear()` と、同名の `Trash.clear`（`os.remove`） | `Trash.clear` が unknown（名前だけで） | 末尾名で降りて CONTRADICTION と行の UNKNOWN。patch にも入る | AG 誤警報 |
| CG-c05 | コンストラクタ `Cleaner(p)` の `__init__` | unreachable | CONTRADICTION | RS 見逃し |
| CG-c06、B2-x01 | `getattr(h, "do_" + op)(p)`、`ACTIONS[action](p)` | unreachable | 効果の行なし（ユニットに opaque だけ） | 両方見逃し |
| CG-c01、入口-c21、B2-x01 nested_def | 入れ子の `def inner` | unreachable | CONTRADICTION | RS 見逃し |
| CG-c12 | 入れ子の helper とトップレベルの helper が同名 | 無害なツールに high | 効果なし | RS 誤警報 |
| CG-c02、B2-c03 | `from .io import save as persist` | unreachable | CONTRADICTION | RS 見逃し |
| B2-c03、CG-c07、CG-c07c | `pkg.io.save()`、`from pkg import mod; mod.f()` | unreachable（`from . import io as m` は解決する） | CONTRADICTION | RS 見逃し |
| CG-c14、CG-c15、B2-x05 | try の中の import、関数の中の import | unreachable（B2-x05 は exit 0） | CONTRADICTION（try は opaque） | RS 見逃し |
| CG-n06、B2-c10 | モジュール直下の if の中の def | unreachable | CONTRADICTION | RS 見逃し |
| CG-n01 | `from mod import Klass; Klass.run(p)`。mod.py に無関係なトップレベル関数 `run`（`os.remove`） | high（誤） | 効果なし | RS 誤警報 |
| CG-n13 | 無関係な `a/__init__.py` に `from .x import helper` | `b/tools.py` の helper が `a/x.py` に結ばれ、不一致が消える | （走らせていない） | RS 見逃し |
| CG-n02 | どこからも呼ばれない `Registry.tool`（`os.remove`） | unknown（全ツールの `@mcp.tool(...)` が名前 `tool` を残すため） | 効果なし | 表示だけの差 |
| CG-n08b（対照 n08c） | 到達したメソッドの `super().__init__()` と、無関係なクラス `Danger.__init__` の `os.remove` | `Danger.__init__` の finding が unknown（名前 `__init__` が残るため）。`super` を除いた n08c では unreachable | 効果の行なし（`opaque_reasons: ['unresolved']`） | 表示だけの差（RS の unknown は無関係な先に広がる） |
| CG-n04b（対照 n04a） | 木の中の `.venv/…/site-packages/requests/__init__.py` と、ツールの `requests.delete(url)`、無関係な `Repo.delete` | rglob の予備手段で `requests` が木内扱いになり、`Repo.delete` の `os.remove` が unknown。`.venv` の無い n04a では unreachable | （走らせていない） | RS の表示の誤り |
| CG-n09b | モジュール直下のシングルトン `svc = Svc()` の `__init__` で `os.remove` | module_level ではなく unreachable | ツール `ping` に効果の行なし | 両者ともツールの効果としては出さない（RS の状態の名前は誤り。import 時に実行される） |
| CG-n03 | 関数の中で定義したクラスの `build().delete(p)` | unreachable | 効果の行なし（opaque だけ） | 両方見逃し |
| B2-x01 | `lambda p: _write(p)` / `functools.partial(_write, …)` / `asyncio.to_thread(_write, p)` | lambda だけ high | partial と to_thread は CONTRADICTION（`authgap/catalog/transfers.py:132`、`:136`）。lambda は `opaque(dynamic)` で効果 0 | 向きが互いに逆 |
| MM-v11 | `asyncio.to_thread(os.remove, p)`（ライブラリの sink を値として渡す） | 0 | 0 | 共通の見逃し |
| B2-c09 | 自己再帰、相互再帰 | high | CONTRADICTION | 一致 |
| sink-l_bfs | 関数の中の `import shutil as os` が、モジュール水準の `import os` を上書き | `os.remove` が WRITE にならず 0（import 表は ast.walk の訪問順で後勝ち） | CONTRADICTION | RS 見逃し |

**7.3.5 能力（sink）の差**

主な対応は §4 の後半の表にまとめた。判定に効いた差だけを挙げる。

| ケース | 書き方 | RS | AG | 差 |
|---|---|---|---|---|
| B2-x03 | readOnlyHint=True で `subprocess.run(["ls", …])`（argv0 が定数） | high | 不（`contradiction_unknown:D1:spawn_command`。行の verdict は空） | 設計の違い。RS は起動を readOnlyHint の矛盾として残すと明言している（PR #32「That contradicts the hint as written (it starts a process), so they're kept.」○） |
| B2-x03 | 別名・from-import の subprocess（`sp.run`、`run_cmd`）、`check_output`、`os.popen`、`asyncio.create_subprocess_exec` | 0（能力そのものを検出しない） | 5 件とも SPAWN を検出する。ただし argv0 が定数の 4 件（`sp.run`、`run_cmd`、`check_output`、`asyncio.create_subprocess_exec`）は不（`contradiction_unknown:D1:spawn_command`、行の verdict は空）。矛は `os.popen`（shell_string をモデルが選ぶ。`spawn_model`）の 1 件だけ | RS は能力そのものを検出しない。AG は SPAWN を検出するが、argv0 が定数のものは不 |
| sink-c_destructive | 同じ行の 2 つ目の WRITE（`with open(a, "a") as f, open(b, "w") as g:`、`shutil.copy(a, b); os.remove(a)`） | 重複除去で破壊的な方が消え、D2 なし | 2 つとも出し D2 CONTRADICTION | RS 見逃し（2 行に分けると RS も出る。sink-s_multiline_with） |
| sink-c_destructive、MM-c17、B2-c08 | destructiveHint=False で `shutil.copy(a, b)` | 0（copy は追加的扱い） | D2 CONTRADICTION `fs_writeout_model_path` | 設計の違い（copy を破壊的とするか） |
| B2-c08 | readOnlyHint=True で `Path(__file__)…/"cache"` を `.mkdir()`（D43 の形） | 0 | CONTRADICTION（opaque） | RS 見逃し |
| B2-c04、sink-e_ro_send_db | readOnlyHint=True で UPDATE、destructiveHint=False で DELETE / DROP | 0 | D1 / D2 CONTRADICTION `db_modify`。SELECT は宣言内 | RS 対象外 |
| MM-c06、B2-x07 | readOnlyHint=True で `requests.post` / `requests.delete` | 0 | POST は不（`contradiction_unknown:D1:net_post`）、DELETE は CONTRADICTION `net_modify` | RS 対象外（SEND は readOnlyHint の規則に入らない） |
| B2-x07 | openWorldHint=False で `subprocess.run([cmd])`（cmd はツール引数） | read_only だけ | D1 と D3 の CONTRADICTION `spawn_model` | RS は起動を openWorld に数えない |
| B2-c07、MM-c04 | openWorldHint=False で `httpx.get("http://127.0.0.1:8000/…")` | medium | 矛盾なし（host が local） | 設計の違い（RS は loopback の HTTP も外向きとする） |
| B2-c07 | `socket.create_connection((host, 9000))` | medium | 効果なし（AuthGap に socket の行は無い） | AG 見逃し |
| sink-u_hyp | `websockets.connect("ws://localhost:8765")` | medium | 効果なし | 向きは逆だが、AG は効果自体を持たない |
| sink-d_closed_world | `webbrowser.open("https://…")`、型の分からない受け手の `client.request("GET", "https://…")` | medium | 効果なし | AG 見逃し |
| sink-d_closed_world | `self.http = httpx.Client()` を経由した `.get(url)` | 0 | D3 CONTRADICTION | RS 見逃し |
| sink-h_extra | `client = httpx.Client(); client.delete(url)` | SEND（openWorld の照合には使う） | 効果なし（O39） | AG 見逃し（既知の限界） |
| sink-n_factory | try の中の import を使う factory、2 段の factory | 0 | D3 CONTRADICTION | RS 見逃し |
| sink-u_hyp | `urllib.request.urlretrieve(url, p)`（属性形 / from-import） | 属性形は 0、from-import は SEND で closed_world | どちらも NET ＋ FS_WRITE で D1 / D3 CONTRADICTION | RS は書き込みを見ない |
| sink-r_eval_shadow | 同じファイルで `def eval(x)` を定義して呼ぶ | EXECUTE / DYNAMIC で high | EXEC で CONTRADICTION | **共通の誤警報**（AG の限界でもある） |
| B2-x04、MM-v04、sink-v_prefix、sink-d_closed_world、sink-a_exec | `os.path.join(...).replace(...)`、`ostrich.remove`、`requests_seen.get(k)`、`HTTPStatus(code)`、`re_compile(p)` | high / medium | 効果なし | RS 誤警報 |

**7.3.6 出力、抑制、終了コード**

- B2-x06: 読み取りの不一致は `allow-mismatch` で抑制できた。closed_world の不一致（medium）は抑制せずに残したが、既定の `--severity high` では exit 0、`--severity medium` で exit 1 だった。抑制を外した対照（B2-x06_ctl）は exit 1。
- MM-c15: sink に付けた `allow-WRITE` は不一致を抑制しない。
- MM-x22: medium の不一致だけが残り、sink を `allow-WRITE` で抑制した場合、既定は exit 0、`--severity medium` は exit 1、`none` は exit 0。
- ほぼすべてのケースの exit 1 は、reachable な high の finding によるもので、不一致の有無とは関係ない（`cli.py:42`）。exit 0 になったのは次のケースで、どれも宣言に反するツールを含んでいた。入口として見落とした（B1-c05a、B1-c12）、unknown にした（B2-c02 と、その対照 B2-c02_ctl。`B2/out/exit_codes.tsv` で 4 モードとも 0）、効果を検出しなかった（B2-c04 の SQL）、unreachable にした（B2-x05 の try の中の import）、抑制した（B2-x06）。
- AuthGap の `authgap scan` は CONTRADICTION があっても exit 0 を返す（`authgap/cli.py:112`）。`--determinism` でバイトが一致しないときだけ 3 を返す（`:105`）。インラインの抑制の仕組みは見つからなかった。

---

## 8. AuthGap との異同

| 軸 | reachscan 0.4.0 | AuthGap（HEAD 8fbbed4 の `authgap/`。§7 の指紋の照合を参照） | どちらが先か |
|---|---|---|---|
| 対象言語 | 不一致は Python だけ。TS/JS は入口、能力、到達性（8 hop）まで扱い、注釈は読まない | Python だけ | TS の到達性は RS だけ。TS の照合はどちらも無い |
| 入口の規則 | デコレータ 10 語（2 段まで、モジュール直下とクラス本体だけ）、基底クラス 3 つ（静的な name が必須）、工場呼び出し 6 形。call_tool / list_tools だけは入れ子も拾う | 14 規則、7 種類（decorator / method / lowlevel_v1 / lowlevel_v2 / spec_object / tools_list / toolmessage_handler。`authgap/catalog/entries.py:130-231`）。`:6` に `**このカタログの外から MODEL を導入してはならない。**` とある。入れ子、if / try / with の中、add_tool、呼び出し形も読む | MCP については AG が広い。pydantic_ai / AutoGen / LlamaIndex / DSPy / Swarm / MetaGPT / Marvin / CAMEL は RS だけ |
| 注釈を読む条件 | framework が mcp のデコレータ入口だけ。受け手名や import で決まる | 規則に当たれば、受け手名に関係なく読む（`entries.py:504`） | AG |
| 注釈の式 | ToolAnnotations、辞書、名前参照（1 段、同じファイルか project 内の from-import）。bool 定数の値も読む | ToolAnnotations、`ToolAnnotations(**{辞書})`、辞書。名前参照は unreadable（D_unknown）。非リテラルの値はそのキーだけ捨てる（ほかに上界を動かすキーが無ければ ⊥） | 名前参照と定数は RS（B1-c02 で 4 対 0）。`**{}` は AG |
| 解けない値の扱い | unresolvable として Not checked と JSON に出す | 一部は D_unknown。非リテラルの値はそのキーだけ黙って捨てる（⊥ になるか、宣言の種類が変わる。§5） | RS のほうが開示的 |
| snake_case | 版を見ずに常に unresolvable | mcp の主版で読み分ける。ge2 は写す、lt2 は malformed、不明は D_unknown（`entries.py:2746` 前後、D64 / U38） | AG（2.x の木で差が出る） |
| 低レベルの宣言の収集 | 同じファイルの list_tools の本体とモジュール直下の文。mcp 由来の `Tool` だけ。名前はリテラル、定数、enum | パッケージの全ファイルから末尾名が `Tool` の呼び出しを集める（import 元は見ない。`entries.py:2689`、`:2699`）。名前は文字列リテラルだけ | 範囲は AG、enum の名前は RS |
| 低レベルの帰属 | 構文上の分岐の行範囲（`==`、`and`、ガードの無い match）。try / with で包むと誤警報。結べないものは黙る | CFG の支配で帰属させ、どの判定にも当たらない効果は全ツールに帰属させて宣言の積で判定する（`analyze.py:668-673`）。`==` と `in` の文字列リテラルだけを読む。match と定数・enum の比較は全ツール帰属（誤警報の側） | 失敗したときの倒れ方が逆。RS は黙り、AG は過剰に指す |
| 照らす宣言 | D1（readOnlyHint=true）、D2（destructiveHint=false。readOnlyHint の値が false のときだけ）、D3（openWorldHint=false） | D1〜D4 の 4 つを、宣言ごとに主指標として報告する（`dparse.py:580`、D62） | D4 は AG だけ |
| D1 の効果 | WRITE / EXECUTE / DYNAMIC | FS_WRITE、EXEC、SPAWN（argv0 / shell_string をモデルが選べれば矛、それ以外は不）、DB（変更の文）、NET（PUT / PATCH / DELETE は矛、POST は不） | 粒度は AG。定数コマンドの起動は RS が矛、AG が不（設計の違い） |
| D2 の効果 | WRITE の evidence 文字列に正規表現。EXECUTE は外す。copy、追記、mkdir は追加的扱い | EXEC は矛、SPAWN はモデル次第。FS_WRITE は append / remove / writeout / unknown の類に分ける。DB は破壊的な先頭語、NET は DELETE / PATCH（`dparse.py:397-427`、`DESTRUCTIVE_KINDS = frozenset({"EXEC", "SPAWN", "FS_WRITE"})` `:49`） | AG |
| D3 の効果 | HTTP（宛先は見ない）、websocket、socket connect（リテラル loopback を除く） | NET の宛先の類（local / external / model / 不明。local には loopback、RFC 1918、ULA、link-local、`*.local` を含む。`dparse.py:295-301`）。EXEC / SPAWN もモデル次第で入れる。socket と websocket の行は無い | 宛先を区別するのは AG（HTTP の loopback を宣言内とするかは設計の違い）。socket / websocket は RS |
| 能力（sink）の語彙 | 7 capability と evidence 文字列。確度なし | 7 kind に slot、値の主体、確度（resolved / opaque(reason)） | AG（ただし RS だけが持つ行もある） |
| DB / HTTP メソッド | どちらも無い | SQL の先頭語の類（複文は文ごと）、RFC 9110 のメソッドの類（`authgap/catalog/statements.py`） | AG |
| 深さ | 8 hop（BFS） | 4（`ir.py:42` `MAX_DEPTH = 4`。仕様書は 3、D54 / 逸脱 #17 で 4）。補助関数を N 回呼ぶ鎖で較正すると、RS は N≤8、AG は N≤4 を検出した | RS |
| 受け手の型 | `self.m()` と `ModuleName.f()` だけ。インスタンスのメソッドは名前だけで unknown | 型を推論する。コンストラクタ、`self.<attr>`、`super()` も解く | AG |
| 未解決の扱い | §5。unknown はツールに帰属せず、多くは unreachable と断定 | `opaque(reason)` を値と効果に付け、行の UNKNOWN を並べ、ユニットに理由を残す。ただし降りなかった先の行は無い | AG（数える設計）。ただし AG にも穴がある |
| ソースの読み方 | 文字列で読む（BOM で黙って消える）。テストのパスを絶対パスで除外 | バイト列で読み、parse_failures を出す。テストのパスは除かない | AG |
| 決定論 | 同じ入力で JSON が一致（generated_at を除く）。`mismatch_id` は絶対パスに依存 | `--determinism 3` でバイト一致 | 同等 |
| 出力と運用 | JSON / テキスト / SARIF（codeFlows）、終了コードで CI を止める、理由必須の抑制 | manifest、SARIF、annotation-patch。終了コードは常に 0。抑制なし | 道具としての運用は RS |
| 測定の設計 | 事前登録、凍結、人の判定の記録、再現率は見つからなかった。corpus は非公開。規則は結果を見て直した（○） | 事前登録（汚染状態を先頭に開示。`docs/preregistration.md:11-13`）。解析器の凍結（指紋とタグ）。人の判定（D82。D85 は判定そのものではなく、実態調査の名簿を解析器を使わずに作る決定。`docs/decisions.md:4383`）。再現率は、開発者が宣言を直した件 352 件と実態調査。352 の単位はコミットではなく（群, ツール, 宣言）の件である（D79、`docs/decisions.md:4199`「**352 件・73 群・97 版**（D1 68・D2 151・D3 55・D4 78…）」。群単位の bootstrap 10,000 回、seed 20261005）。AuthGap の文書の中でも単位の書き方は揃っておらず、`docs/decisions.md:4298` は「コミット 352 件」と書く。論文では D79 の単位を使う。精度は矛からの抜き取り（主、D1〜D4）と実態調査（D82） | AG |

**reachscan が AuthGap より先にいるところ**（正直に。すべて ◎ 実行）

1. **深さ 5〜8 の経路**（B2-c01_depth、MM-c20）。
2. **TS の到達性**（照合はしない）。
3. **MCP 以外のフレームワーク**の入口（入口-c30）。
4. **注釈の名前参照とモジュール定数**（B1-c02 の 4 件）。解けない値を Not checked として開示する（B1-c06）。
5. **enum や定数で書いた低レベルの名前と dispatch**（注釈-v14、B1-c07）、**match 文の分岐ごとの帰属**（B1-c04b）。AuthGap はここで join から外れるか、誤警報を出す（B1-c07、B1-c07ctl_attribution、B1-c04b）。注釈-v14 の AuthGap 側は、別の入力で抽出関数を走らせた join の段（unjoined=1）までしか確かめていない（§7.3.2）。
6. **AuthGap に無い sink の行**: `socket.create_connection`、`websockets.connect`、URL 定数を渡す `webbrowser.open` など、HTTP セッションの `.delete` / `.put` / `.patch`（AuthGap の O39）、aiohttp の `ClientSession().get`（AuthGap は sink-u_hyp で効果 0）。
   ただし、これらはどれも SEND で、SEND は readOnlyHint の規則に入らない（`annotation_mismatch.py:67` `_READ_ONLY_CONTRADICTIONS = {"WRITE", "EXECUTE", "DYNAMIC"}`）。効くのは openWorldHint の照合だけである。
   `importlib.import_module` / `runpy` も DYNAMIC にするが、定数の `il.import_module("json")` でも high の `read_only_contradicted` になった（sink-m_misc）。誤警報とも読めるので、利点としては数えない。
7. **T8a の unknown（インスタンスのメソッドの名前だけの一致）では矛盾を出さない**。B2-c02 の name_only_match は、AuthGap では誤警報になる。
   ただし reachscan も、別の経路では名前だけで結んで high の誤警報を出す。CG-n01（`Klass.run` が同名のトップレベル関数に結ばれる）、CG-c12（同名の入れ子関数とトップレベル関数の節点が合流する）、CG-n11 と MM-v01（低レベルの分岐で末尾名だけで結ぶ）。「名前だけの一致で矛盾を出さない」とは言えない。
8. **経路つきの出力、SARIF の codeFlows、抑制、終了コード**による CI での運用。

**AuthGap が先にいるところ**（同上）

1. D4 を照らす。
2. DB と HTTP メソッドを区別する。
3. 入口が広い: add_tool、呼び出し形、入れ子、3 段のデコレータ、if / try の中、低レベル v2、受け手名に依らない。
4. snake_case を版で読み分ける。
5. 受け手の型を推論する。
6. 別名 import、try の中の import、入れ子の関数、コンストラクタを解く。
7. sink が広い: rmtree、makedirs、Path.unlink、`w+`、`io.open`、`Path.open`、`check_output`、`os.popen`、asyncio の subprocess、属性に持ったクライアント。
8. BOM 付きのファイルも読む。
9. 未解決に理由を付けて残す設計（ただし §5 の穴がある）と、測定の設計がある。

**設計の違い**（どちらが先とも言えない。規則の選び方の違い）

- 定数コマンドの起動: reachscan は readOnlyHint の矛盾にし、AuthGap は不とする。著者は、起動はヒントに反するので残すと明言している（PR #32「That contradicts the hint as written (it starts a process), so they're kept.」○）。
- HTTP の loopback: reachscan は外向きとして数え、AuthGap は宣言内とする。
- `shutil.copy`: reachscan は追加的な書き込みとし、AuthGap は破壊的とする。
- テストのパス: reachscan は `tests/`・`benchmarks/`・`test_*.py` を走査せず、AuthGap の scan は読む。野外では、テストの中のサーバは誤警報の源にもなりうる。AuthGap の母集団のスクリプトがテストのパスをどう扱うかは不明（B1-c10）。

**両者に共通の穴**（すべて ◎ 実行）: 次のものはどちらも矛盾として出さないか、誤って出す。

- `Tool as McpTool`
- 辞書による dispatch、`getattr`
- `**EXTRA` による上書き（両者とも誤警報）
- `asyncio.open_connection`
- `asyncio.to_thread(os.remove, p)`
- `Path.rename` / `replace`、`os.truncate`、`os.open`
- 自作の `eval`（両者とも誤警報）
- 深さ 9 以上

**語彙の対応の注意**: reachscan の EXECUTE（subprocess、os.system）は AuthGap の SPAWN に、reachscan の DYNAMIC（eval / exec）は AuthGap の EXEC に当たる。
「reachscan は EXEC を D2 に数えない」と書くと、語が混ざって誤りになる。

---

## 9. 論文でどう書くか

### 9.1 言えないこと

- 「Python の MCP サーバについて、宣言を読み、呼び出し先まで追う静的解析は AuthGap が初めて」。2026-10-05 以降は reachscan がある（`docs/related_work.md` の「2026-10-12 の再検索」1.）。
- 「reachscan は未解決を扱わない」「reachscan は関数の本体しか見ない」。どちらも誤り。unknown（T8a）と深さ 8 の到達性がある。
- 「AuthGap は reachscan より見逃しが少ない」「検出力で勝る」。共通のデータで測っていない。§7 の合成ケースは違いを狙って作ったもので、reachscan が勝つケースも含む。
- reachscan の「16 件・確認済み TP 1 件」や「FP 率 0.47%」を、検証された値として引くこと。引くなら著者の主張・未検証と書く。0.47% は不一致の精度ではない。
- 「reachscan には事前登録が無い」と断定すること。言えるのは「repo と PR の範囲では見つからなかった」まで。

### 9.2 言えること（水準つき）

- reachscan が照らすのは readOnlyHint・openWorldHint・destructiveHint の 3 つで、idempotentHint は照らさない（◎ コード）。
- 能力は 7 種で、SQL 文や HTTP メソッドを区別しない（◎ コード）。
- 解決できないインスタンスのメソッド呼び出しの一部（名前がプロジェクト内の `"Class.m"` と一致するもの）の先を unknown とし、unknown を不一致にも終了コードにも数えない（◎ コードと実行。README も同じことを書く ○）。入れ子関数、別名 import、`getattr`、辞書の dispatch、コンストラクタ、try の中の import、深さ 8 を超えた先などは unknown ではなく unreachable と断定する（◎。§5 の 2）。
- 評価は、著者が 38 リポジトリと公式の git サーバ（一覧は非公開。一部の名前は PR #28 にある）で数えた件数で、規則はその結果を見て改められている（○ PR 本文）。
- AuthGap の違いは 3 つある。(1) D1〜D4 を効果の粒度（SQL 文の類、HTTP メソッド、宛先の類）で照らす。(2) 決められなかった値に `opaque(reason)` を付けて残し、F0a の probe で slot の opaque の率を出す。言えるのは「Python で、効果の単位の `opaque(reason)` の率を主な結果にした例は見つからなかった」まで（`docs/related_work.md:268-269` と同じ狭さ）。降りなかった先の行が残らないなどの穴も併記する（§5）。(3) 凍結した解析器を、事前に固定した規則のもとで、人の判定と、開発者が宣言を直した件（D79 の単位）で測る。

### 9.3 関連研究の節に置く文の案（2〜3 文）

> reachscan（Nair, 2026。v0.4.0、commit 4f6509d、2026-10-12 参照）は、Python の MCP ツールについて、明示された readOnlyHint・openWorldHint・destructiveHint を、ツールの入口から AST の呼び出しグラフで最大 8 段辿って届く能力（書き込み、プロセスの起動、送信など）と照らし、矛盾を経路つきで報告する OSS のスキャナである。インスタンスのメソッド呼び出しの一部を unknown として分けるが、unknown も矛盾には数えず（入れ子関数や動的な呼び出しなど、ほかの未解決の多くは到達しないものとして扱う）、idempotentHint、SQL 文、HTTP メソッドの区別は扱わない。著者の評価は、38 リポジトリと公式の git サーバ（一覧は非公開。一部の名前は PR #28 にある）での不一致 16 件・確認済みの真陽性 1 件で（著者の主張）、規則はその結果を見て改められている。

AuthGap との差を一文で足すなら:

> 本研究は同じ照合を 4 つの宣言について効果の単位で行い、決められなかった値には理由を付けて残して slot の単位の率を報告し、凍結した解析器を事前に固定した規則のもとで、人の判定と、開発者が宣言を直した件によって評価する。

（この文の「率」は F0a の probe の slot の率に限る。降りなかった呼び出しの先は行が残らない、などの限界を本文の限界の節に書くこと。§5。）

関連研究では、HintLint・mcp-doctor（呼び出し先を追わない）と並べ、「呼び出し先を追う道具」の側に reachscan を置くのが正確である（推論）。

### 9.4 比較するなら — 手順

reachscan との数の比較は、**まだ決めていない**。学生の決定が要る。選択肢は 3 つある。

- (A) 数の比較をしない。関連研究の文と、本ノートの合成ケースの表（探索的、と明示する）だけを使う。
- (B) D80 と同じように、D79 の 352 件（`corpus/fx-*`、直す前の版）で再現率を並べる。
- (C) 最終評価のデータで並べる。

(B) や (C) にするなら、**走らせる前に**次を `docs/decisions.md` に決定として書く。D80 が HintLint・mcp-doctor でしたのと同じ形である。

1. **道具と版**: reachscan 0.4.0（`4f6509d`。clone から入れたか PyPI の wheel か、Python の版）。走らせる直前に upstream の新しい commit を確かめ、版を固定する。
2. **「見つけた」と数える規則**（ツール名が一致した `annotation_mismatches` の要素だけ）:
   - D1 は `read_only_contradicted`、D2 は `non_destructive_contradicted`、D3 は `closed_world_contradicted`。D4 は「対応する規則が無い」。
   - 抑制の付いた不一致を数えるか決める。
   - **終了コードは使わない**（§3.8）。`mismatch_id` で突き合わせない（絶対パスに依存する）。
   - unknown の finding を「参考」として別に数えるかを決める（不一致ではない）。
3. **ツール名の突き合わせ**: reachscan の名前は「位置引数か `name=` の文字列 → 関数名」の順で決まり、`name=CONST` は関数名に落ちる。AuthGap は FastMCP の位置引数の名前を読まない（B1-c07）。低レベルでは `declared_tools[].name` を使う。突き合わせの規則を事前に書く。
4. **分母**: D80 と同じく 2 つを並べる。(i) 宣言ごとの全件、(ii) AuthGap の分母に入った件だけ。道具が木で失敗した件は「失敗」として別に数える。
   - reachscan は絶対パスに test / tests / benchmark / venv などを含むファイルを走査しないので、木の置き場所の名前を確かめる。木の中の `tests/` の扱いの差は、分母の差として記録する。
   - BOM 付きのファイルは黙って消えるので、件数を数えて報告する。
5. **深さ**: AuthGap の深さ 0 と 4（D80 の追記と同じ）に reachscan の 8 を並べ、深さの効果と照合の規則の差を分けて書く。
6. **宣言の読み取りと効果の到達を分けて見る**: reachscan の JSON の `py_entry_points[].annotations` / `declared_tools` から、宣言を読めたかどうかは機械的に取れる。低レベルで結べなかったツールは出力に出ないので、「宣言は読めたが不一致が出ない」件が、未結合によるのか効果が届かないことによるのかは区別できない。これを限界として書く。
7. **事前登録上の位置づけ**: 解析器の凍結と事前登録の後に足す比較なので、`docs/preregistration.md` §5 に追加として記録する（変更前、変更後、理由、日付、その時点で見ていた数値）。または「探索的」と明示する。
   **このノートの合成ケースの結果（§7）は、決定を書く前に既に見ている**。D80 の HintLint・mcp-doctor の結果も見ている。そのことも開示する。
8. **評価・練習データには、決定をコミットする前に reachscan を走らせない**。対象は `evidence/annotation_fixes_frame*`、`evidence/annotation_fixes_v234`、`evidence/practice_*`、`evidence/population_v3`、`evidence/population_v4`、`corpus/`。
   最終評価のデータ（D82 の実態調査を含む）を使うなら、D82 の順番（実態調査を最初に、解析器の出力を見ずに判定する）を崩さないよう、reachscan の出力を見る時点も決める。

---

## 10. 不明なこと・確かめていないこと

**reachscan について**

- phase-3 corpus の中身（38 repo の一覧、選び方、版、公式 git サーバの版）は不明。一部は PR #28 が名前を挙げている（awslabs、davinci-mcp、dbt-mcp。○）。`tools/run_phase3_scans.sh` は公開されていない。
- README の 0.47%（約 3,900 ラベル）のラベラー、基準、データの所在は不明。
- 「V decision」の V が何を指すか、決定者が誰かは不明。PR の「agreed decision」「your decision」からの推測は △ にとどまる。
- openWorldHint を medium に下げた理由は不明（見つからなかった）。
- registry sweep（上位 300）と「8-server registry sample」の結果と構成は非公開。
- SEP-2793（walbis/modelcontextprotocol @49f25cf）の本文と、著者が出したという仕様の曖昧さの議論は読んでいない。
- PR 本文は WebFetch の要約経由で、一字一句は照合していない（○ のまま）。
- 使った CLI は clone から入れたもので、PyPI の 0.4.0 wheel と同一かは確かめていない。0.3.1 の sdist はタグと同一だった。
- TS 側（`ts_entry_points.py`、`ts_callgraph.py`、`ts_capabilities.py`）は一部しか読んでいない。TS の能力の表、TS の unknown の扱いが Python と同じかは不明。
- 古い記述が 2 か所残っている（◎）: plugin の README（`integrations/agent-plugins/README.md:64`）と `ts_entry_points.py:21` は「TS の本体は解析しない」と書くが、0.3.2 で到達性が入っている。
- 未実行の予想:
  - `or` の分岐（CHANGELOG は結ばないと書く。○）
  - ガード付きの case（コードの読みだけ）
  - f-string の Tool 名
  - `async with` で包んだ dispatch
  - 同名の入れ子 closure
  - 50,000 節点の cap
  - 名前空間パッケージ
  - 同名の入れ子クラスの節点の合流
  - UTF-8 でないファイル
  - 相対パスで渡したときの除外
  - CG-n13 の AuthGap 側
- 合成ケースで見つけた見逃しと誤警報の型が、野外の MCP サーバでどれだけの頻度で起きるかは測っていない。
- 実行で確かめたが、野外での影響の大きさが分からないもの（◎ 実行。詳細は §3.5、§3.7、§7.3.4）:
  - `super().__init__()` が名前 `__init__` を残し、無関係なクラスの `__init__` がすべて unknown になる（CG-n08b、対照 n08c）。
  - 絶対 import の rglob の予備手段が、走査から除外した `.venv` の中のパッケージに import を結び、unknown を広げる（CG-n04b、対照 n04a）。
  - モジュール直下のシングルトンの `__init__` が module_level ではなく unreachable になる（CG-n09b）。

**AuthGap について**（凍結中なので直していない。限界として `docs/open_questions.md` に書くかは学生の判断。CLAUDE.md 規則 4）

この比較の中で次のものが見えた。読み手と検証者が `docs/open_questions.md` と `docs/decisions.md` を grep した範囲では、記載が見つからなかった。

- 非リテラルのヒントの値は、そのキーだけが D_unknown の印なしに捨てられる（`entries.py:2756-2759`）。ほかに上界を動かすキーが無ければ ⊥ になり、あれば宣言の種類が変わる（B1-c06 の mixed は D2 になった。§5）。
- 辞書の `**` と計算キーを黙って無視する（`entries.py:2792-2794`）。
- `Tool(name=Enum.X)` は join できない（`entries.py:2701`）。
- モジュール直下の辞書表のキーは候補にならず、宣言が件数ごと外れる（`entries.py:2615`）。
- 定数・enum との `==` を読まないための誤帰属（B1-c07ctl_attribution）。
- FastMCP の位置引数のツール名を読まない（`entries.py:491-495`、`catalog/entries.py:114`）。
- `Tool(...)` のリテラルを、木全体からツール名だけで join するので、別のサーバの同名のツールに付きうる（A-entries）。
- `Tool(...)` のリテラルを、import 元を確かめずに末尾名だけで集める（`entries.py:2698-2700` `fname = dotted_of(node.func) or ""` / `if fname.split(".")[-1] != "Tool":` / `continue`）。dspy や LangChain の `Tool(name=…)` も宣言として join されうる（未実行）。
- デコレータを末尾名で照らす（`entries.py:286-291`）ので、LangChain の `@tool` が `mcp:lc_helper` という **mcp のユニット**になった（入口-t14、◎ 実行。manifest の unit は `framework: mcp`）。MCP ユニットの分母に効く。mcp 規則の names（`catalog/entries.py:138`）に `"tool"` があり、langchain 規則（`:163` `EntryRule("decorator", "langchain", ("tool", "langchain.tool", "tools.tool"))`）より先に照合され、`_match_decorator` は最初に当たった規則を返すためである（`entries.py:287-292`）。`docs/decisions.md:153` は langchain の `@tool` を入口の 1 形に挙げるが、それが mcp と名づけられることの記載は見つからなかった。
- 低レベルの帰属に使う `_dispatch_test_names`（`analyze.py:635-644`）は、比べている変数が選択子かを確かめない（`tool = name; if tool == "erase"` も読む。入口-c09）。また `comparators[0]` しか見ないので、`"x" == name` のように左にリテラルを置く形は読まず、全ツール帰属になる（コードの読み、未実行）。
- 自作の `eval` を組込みと区別しない（sink-r_eval_shadow）。
- sink の行が無いもの: webbrowser、aiofiles、websockets、`socket.create_connection`、`httpx.stream`、`Path.rename` / `replace`、`os.truncate`、`os.open`、aiohttp。

既知か設計どおりのもの:

- match 文の全ツール帰属は設計どおり（`analyze.py:655-656`）。
- HTTP セッションの `.delete` などは O39 で既知。
- 末尾名だけで降りた誤警報（B2-c02 name_only_match）は O30 / D57 と同じ類に見えるが、D57 が何を変えたかは確かめていない。

AuthGap 側で原因を特定していないもの:

- ほぼ全ユニットの `opaque_reasons` に `unresolved` が立つ。どの呼び出しが原因かは特定していない。
- B1-c09 の `HANDLERS[name](...)` の先の効果が行に出ない（dispatch_sites には resolved と出る）。
- B2-x05 で `fast.py` の側が効果に出ない。

その他:

- 凍結のタグ `analyzer-freeze-3` はローカルに無く、fetch もしていないので、タグとの一致は確かめていない。実行した `authgap/` の 27 ファイルは `docs/fingerprint.json` と一致した（§7）。
- MCP Python SDK 1.x の挙動（snake_case を無視する、位置引数の名前）は、reachscan の docstring と AuthGap のコメントの主張に頼っている。2.x は mcp 2.2.0 のソースを読んで確かめた。

---

## 付録: 再現の置き場

`$SP` = `/tmp/claude-0/-home-user-auth-gap/47888d26-b392-5abf-8b68-d6c4b0285b05/scratchpad`。
scratchpad はこのセッション用の一時領域なので、下の表の 11 のディレクトリを **`evidence/reachscan_20261013/` に同じ名前で写した**
（2026-10-13、1,846 ファイル。`__pycache__` と `.pyc` は除いた。下の表の `$SP/` を `evidence/reachscan_20261013/` に読み替える）。
出力ファイルの中に書かれた絶対パスは scratchpad のままである。reachscan の venv（`$SP/rs_venv`）と clone は写していない
（再現するときは commit `4f6509d` を clone し、`uv pip install` で入れる）。`cg_verify_1012/cases_new/n04b_venv/.venv/` は
偽の `.venv` そのものが入力なので、`.gitignore` に例外を足して追跡している。

| 本文での接頭辞 | 内容 | 置き場（ケース / reachscan の出力 / AuthGap の出力） |
|---|---|---|
| 入口- | 入口の検出と低レベルの結び付け（c01〜c31、検証で追加した t1〜t14） | `$SP/rs_entry_probe/{cases,out,ag_out}`、`$SP/rs_entry_verify/{cases,new,out,ag_out}`（c14 は `under_tests/tests/` の下） |
| 注釈- | 注釈の抽出（v01〜v14） | `$SP/annx_probe/{cases,scripts}`（AuthGap の抽出関数だけ）、`$SP/annx_verify/{cases,out}` |
| CG- | 呼び出しグラフと到達性（c01〜c18、検証で追加した n01〜n13） | `$SP/cg_probe_1012/{cases,out,ag_out}`、`$SP/cg_verify_1012/{cases,cases_new,out,out_new,ag_out,ag_out_new}` |
| sink- | 能力の検出器（a_exec ほか） | `$SP/sinks_probe/{cases,out,authgap_out}`、`$SP/sinks_adv/{cases,out,ag_out}` |
| MM- | 不一致の規則、出力、抑制（c01〜c21、x22〜x26、検証で追加した v01〜v11、h03〜h10） | `$SP/mm_probe/{cases,run,run2,authgap_out}`、`$SP/mm_verify/{cases*,run*,ag*}` |
| A- | probe A（depth_probe、fixtures、対照 2 つ） | `$SP/reachscan_probe/a/{inputs,synthetic,out}` |
| B1- | probe B1（注釈と入口、c01a〜c12） | `$SP/reachscan_probe/B1/{cases,out}` |
| B2- | probe B2（深さ、未解決、sink、出力。c01〜c10、x01〜x07） | `$SP/reachscan_probe/B2/{cases,out}` |

reachscan の実行（probe B2 の形）:

```bash
$SP/rs_venv/bin/reachscan <ケース> --json    > rs_<n>.json
$SP/rs_venv/bin/reachscan <ケース> --explain > rs_<n>_explain.txt
$SP/rs_venv/bin/reachscan <ケース> --sarif   > rs_<n>.sarif
```

AuthGap の実行（`/home/user/auth_gap` から）:

```bash
.venv/bin/python -m authgap scan <ケース> --sarif ag_<n>.sarif --annotation-patch ag_<n>_patch.json --determinism 3 > ag_<n>.manifest.json
```
