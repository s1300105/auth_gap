### 第 9 章

#### 演習 9-1（ファイルを書くか、どこに書くか）

**(1) ログの出し口の対**

| | ファイルを書くか | どこに・いつ |
|---|---|---|
| (ア) `StreamHandler(sys.stdout)` | **書かない** | 記録は標準出力に流れるだけ。ディスクのファイルは変わらない |
| (イ) `FileHandler("/var/log/tool.log")` | **書く** | `/var/log/tool.log`。`FileHandler` を作った時点（この作例ではモジュールの読み込み時）でファイルが無ければ作られ（中身 0 バイト）、`ping` が呼ばれるたびに `called` の 1 行が末尾に足される |

- (ア) の出力先の標準出力は、stdio で動く MCP サーバでは、クライアントへの返事（MCP のやり取りそのもの）に使われる通り道です（第 3 章 3.7 節）。ログをそこに出すとやり取りを乱すおそれがあるので、ふつうは標準エラーに出します（v4 の ccr の `_configure_stdio_logging` の説明文が、その理由を書いている。`corpus/v4-qbit-glitch__ccr/ccr/mcp/server.py:82-85`）。それでも、ファイルが変わらないことに変わりはありません。手引きの下書きの D1 の迷いやすい形は「標準出力・標準エラーへのログ: ファイルではないので反しない」です（`docs/drafts/final_judging_guide_draft.md:323`）。
- (イ) で記録が書かれるのは、ロガーの水準を `INFO` にしてあるからです。水準が既定の WARNING のままなら、`log.info(...)` の記録は書かれません（9.5 節の事実 4）。
- 本記録者が同じ形の作例（`ping_a` が標準出力、`ping_b` が `FileHandler`）を凍結版の解析器で走査すると、**どちらのツールにも効果は 1 つも出ませんでした**（2026-10-01）。(イ) のファイルへの追記は、解析器の出力に出ない形です。見落としの判定なら、原因「語彙」の候補です（9.5 節、第 52 章）。
- 「いつ」を 2 段で答えられていれば十分です: ファイルの作成は設定の時点（読み込み時）、追記はツールの呼び出しのたび。

**(2) 子プロセスの対**

| | ファイルを書くか | 誰が・どこに | 2 回呼んだら |
|---|---|---|---|
| (ウ) `["sort"]` | **書かない** | 子の `sort` は、受け取った行を並べ替えて標準出力（親とつながったパイプ）に出すだけ。親は `out` で受け取る | 何も残らない |
| (エ) `["tee", "/tmp/last_query.txt"]` | **書く** | **子の `tee`** が、受け取ったものを `/tmp/last_query.txt` に書き、同じものを標準出力にも出す。親はファイルを書いていない | `tee` は既定で上書きするので、ファイルの中身は 2 回目の内容になる（`tee -a` なら追記） |

- 本記録者が作業用の場所で、`tee ファイル` を 2 回続けて使うと、ファイルには 2 回目の内容だけが残り、`tee -a` では追記されることを確かめました（2026-10-01）。
- **解析器は区別できません**。本記録者が同じ形の作例（`sort_lines` と `echo_lines`）を凍結版の解析器で走査すると、2 つはまったく同じ報告になりました（2026-10-01）: `subprocess.Popen` の SPAWN は D1 の不（理由 `spawn_command`）、`pipe:communicate` は FS_WRITE で D1 の矛（理由 `fs_write`）。
- 区別できない理由: 解析器は、起動するコマンドが何をするかを名前から知りません。判定表は、モデルが決めないコマンドの SPAWN を「不（コマンドの意味は名前から分からない）」としています（`docs/contradiction_principles.md:165`）。また、argv0 の `sort` も `tee` もインタプリタの一覧に無いので、標準入力への書き込みは、どちらも FS_WRITE の情報行（保守的な上界）になります（9.6 節、`authgap/effects.py:844-847`）。
- 判定の見通し（結論の付け方は第 50・51 章）: (ウ) は「子プロセスの標準入力に流すだけで、子はファイルを変えない」形で、第 51 章の E5 の典型です。(エ) は、子が受け取ったものでファイルを書くので、「流すだけ」とは言えない形です。手引きの「子プロセスがそれを受けて何をするかで決める」の、両側の例になっています（`docs/drafts/final_judging_guide_draft.md:324`）。

**(3) `save_settings`**

- 2 行目: `tempfile.mkstemp(dir=...)` が、`SETTINGS_PATH` と**同じディレクトリ**に、ほかと重ならない名前の一時ファイルを新しく作ります（`/tmp` ではない点に注意）。
- 3〜4 行目: `os.fdopen(fd, "w")` で、その一時ファイルを `'w'` で開き直し、`json.dump` で中身を書きます。
- 5 行目: `os.replace(tmp, SETTINGS_PATH)` で、一時ファイルを `SETTINGS_PATH` の名前に置き換えます。**`SETTINGS_PATH` の前の中身が消えるのは 5 行目**です。一時ファイルは消されるのではなく、新しい設定のファイルになります（atomic write。9.4 節）。
- 解析器の出力に効果として出るのは、**5 行目の `os.replace` だけ**と予想できます。`tempfile.mkstemp` は 9.4 節の表で「無い」、`os.fdopen` と `json.dump` も sink 表にありません。本記録者が同じ形の作例を凍結版の解析器で走査すると、実際に `os.replace`（D1 の矛、理由 `fs_write`）だけが出ました（2026-10-01）。

#### 演習 9-2（lifespan と `main()` の初期化）

**1.** **初期化 A**（lifespan の中）です。

- 理由 1: lifespan の `yield` の前は、サーバが要求を読み始める前に必ず走ります。SDK 1.30.0 の低レベルの `Server` の `run` は、663 行で lifespan に入り、681 行から要求を読む繰り返しを始めます（9.1 節）。どの起動の形でも、最後はこの `run` を通ります。
- 理由 2: 初期化 B は `main()` の中にあります。④ の `fastmcp run server.py:mcp` はファイルを `"server_module"` として読み込み、一番上の `mcp` を直接起動するので、`main()` を通りません（第 3 章 3.7 節）。だから、B が受付の前に走るとは限りません。

**2.** 起きる順番

| 順 | ③ `python server.py` | ④ `fastmcp run server.py:mcp` |
|---|---|---|
| 1 | B が走る（`main()` の中、`mcp.run()` の前） | A が走る（lifespan の `yield` の前） |
| 2 | A が走る（`mcp.run()` の中で lifespan に入る） | `lookup` の 1 回目。この中で `_ensure_index()` の守りが真になり、**B の中身（`os.makedirs`）がツールの呼び出しの中で走る** |
| 3 | `lookup` の 1 回目（A も B も済んでいるので、どちらの初期化も走らない） | `lookup` の 2 回目（どちらも走らない） |
| 4 | `lookup` の 2 回目（どちらも走らない） | |

- ③ で B が A より先なのは、`main()` が `mcp.run()` の**前に** `_ensure_index()` を呼び、lifespan は `mcp.run()` の中で入るからです。

**3.** `reset_index` が `_index = None` に戻した後の、次の `lookup` の呼び出しで、`_ensure_index()` の守り（`_index is None`）が再び真になり、**初期化 B の中身がもう一度走ります**。ディレクトリが消えていれば作り直されます。
`reset_index` はツールなので、サーバの受付の途中で走ります。だから、③ でも ④ でも、この再実行はツールの呼び出しの中で起きえます。
手引きの下書きは「初期化が済んでいても、その後にどこかで `None` に戻すなら、ツールの呼び出しで再び届く。戻す箇所が無いかを grep で確かめる」と書いています（`docs/drafts/final_judging_guide_draft.md:289-290`）。

**4.** 書き留める行（作例の行で）:

- `lookup` の本体の、`_ensure_index()`（と `_ensure_cache()`）を呼ぶ行。
- `_ensure_index` の守りの行（`if _index is None:`）と、`os.makedirs(...)` の行。`_ensure_cache` も同じ。
- lifespan: `mcp = FastMCP("demo", lifespan=app_lifespan)` の行、`app_lifespan` の中の `_ensure_cache()` の行、`yield {}` の行（`_ensure_cache()` が `yield` より前で、条件なしであること）。
- `main()` の中の `_ensure_index()` の行と `mcp.run()` の行、`if __name__ == "__main__":` の行、`mcp` がモジュールの一番上で作られていること（④ で起動できる形であること）。
- `None` に戻す行を探した grep の命令と、その結果（3 の `reset_index` の行、または「無かった」こと）。

参考（規則の当て方は第 49 章で学ぶ。第 3 章 3.8 節で予告した D67 の 2 の表）: A の中の `makedirs` は lifespan で必ず済む形なので「到達しない」（誤の原因 E1）、B の中の `makedirs` は `main()` の中だけで先に済ませる形なので「到達する」（条件の種類 `起動の方法`）の側になります。ただし 3 のように `None` に戻すツールがあれば、話が変わります（第 49 章）。

#### 演習 9-3（grep で呼び出し元を探す）

**1.** 命令（`<木>` = `corpus/final-owner__repo`）

```bash
grep -rn 'def _save_cache' corpus/final-owner__repo --include='*.py'       # 定義を探す
grep -rnE '\b_save_cache\(' corpus/final-owner__repo --include='*.py'      # 呼び出し元を探す
grep -rnw '_save_cache' corpus/final-owner__repo --include='*.py'          # かっこの無い形も探す
```

テストを除いて見たいときは、2 つ目の後ろに `| grep -v '/tests/'` を付けます。

**2.** 6 行の見分け

| 行 | 種類 | 次に確かめること |
|---|---|---|
| `app/cache.py:12` | 定義（`def`） | 定義がこれ 1 つか（1 つ目の命令の結果）。複数あれば、どれの話かを受け手の型で決める |
| `app/cache.py:40` | コメント（`#` の後） | 呼び出しではない。ただし「CLI からも使う」という手がかりなので、`scripts/` などの別の入口を確かめる |
| `app/search.py:31` | 呼び出し | どの関数の中かを開いて確かめる（たとえば `_lookup`）。その関数の呼び出し元を同じ手順で探し、ツールの本体までさかのぼる |
| `scripts/warm_cache.py:8` | 呼び出し（CLI・スクリプト） | ツールの道筋ではない別の入口。ただし、このスクリプトの関数がツールの側から import されて呼ばれていないかを確かめる |
| `tests/test_cache.py:15` | テストの呼び出し | ツールの道筋には数えない |
| `app/remote.py:57` | **受け手が `self` のメソッド呼び出し** | モジュールの関数 `_save_cache` ではなく、`app/remote.py` のクラスの**同じ名前のメソッド**かもしれない。1 つ目の命令で `app/remote.py` に `def _save_cache(self, ...)` があるかを見る。あれば別物なので、取り違えない（9.9 節の考え方） |

- 6 行目が出たのは、`\b_save_cache\(` の `\b` が、`.`（単語の文字ではない）と `_`（単語の文字）のあいだの境目に当たるからです。

**3.** `register_hook("after_search", _save_cache)` は、`_save_cache` を**かっこを付けずに値として渡している**行です。つまり、`_save_cache` はコールバックとして登録され、後で `"after_search"` の合図のときに、`register_hook` を管理する側から呼ばれます（9.9 節）。
次に探すもの: `register_hook` の定義（`grep -rn 'def register_hook' ...`）と、`"after_search"` の合図を出して登録された関数を呼ぶ行（`grep -rn 'after_search' ...`）。その行がツールの道筋にあれば、`_save_cache` はその経路でもツールから届きます。

**4.** `evidence` の例:

「`grep -rnE '\b_save_cache\(' corpus/final-owner__repo --include='*.py'` で 6 行。app/search.py:31 は `_lookup` の中の呼び出しで、`_lookup` はツール `search` の本体から呼ばれる（app/search.py の本体の行 → :31 → app/cache.py:12 の定義の中の書き込みの行）。scripts/warm_cache.py:8（CLI）と tests/test_cache.py:15（テスト）はツールの道筋ではない。app/remote.py:57 は同じファイルのクラスの同名メソッドで別物。`grep -rnw` で app/hooks.py:22 のコールバックの登録を見つけた（呼び戻す側は別に確かめた／確かめられなかった）。」

- 要点は 3 つです: 使った命令を書く、出た行の見分けの結果を書く、ツールの道筋につながる行をファイルと行で書く。
- 「確かめられなかった」ことがあれば、そのまま書きます（黙って安全側に倒さない）。

#### 演習 9-4（gemini の標準入力を読む）

1. **何も書きません**。Linux では `os.name` が `'nt'` ではないので、184〜192 行の枝に入り、`stdin_mode` は `DEVNULL`、`stdin_data` は `None` です。`communicate(input=None)` は標準入力に何も書きません（9.6 節の「動かして確かめた」事実）。プロンプトは、187 行の `-p` の**引数**として渡されます。
2. **プロンプトのバイト列を書きます**。Windows では 170〜183 行の枝に入り、`stdin_mode` は `PIPE`、`stdin_data` は `prompt.encode("utf-8")` です。子（`cmd /c` を通した Gemini の CLI）の標準入力に、プロンプトが流れます。
3. **ありません**。204 行は、子の標準入力への書き込み（Windows）か、何もしない（Linux）かのどちらかで、親のプロセスがファイルを書く行ではありません。ファイルが変わるとすれば、子（Gemini の CLI）の中です。
4. site 名は `pipe:communicate`、効果の種類は FS_WRITE（`form` は `pipe`）、注記は `contradiction:D1` と `contradiction_reason:D1:fs_write` で、**D1 の矛（理由 `fs_write`）**です（`evidence/scan_v2_v4_run1/v4-ankitdotgg__making-gemini-useful-with-claude.json` のユニット `gemini_prompt`）。同じユニットの 195 行の `asyncio.create_subprocess_exec` は SPAWN で、`contradiction_unknown:D1:spawn_model_opaque`（D1 の不）です。
5. 調べること（結論は出さない）:
   - 子（Gemini の CLI）は、受け取ったプロンプトで何をするのか。ファイルを書いたり、コマンドを実行したりすることがあるのか（Gemini の CLI の文書で調べる）。
   - Windows の枝（`os.name == 'nt'`）でしか標準入力を使わないことを、どう扱うか（条件の種類の付け方。第 49 章）。
   - 標準入力ではなく、`-p` の引数や `cwd`（作業ディレクトリ）など、ほかの形でモデルの値が子に渡ること。これは 195 行の SPAWN の組の話として、別に読む（第 50 章の SPAWN の扱い）。
   - この組は v4 では判定していないので、判定の例はありません。

#### 確認問題 9-1

- `open(p, "a")`: **壊さない**。前の中身はそのままで、末尾に足すだけ（`seek(0)` しても末尾に足された。9.3 節の事実 5）。
- `open(p, "x")`: **壊さない**。ファイルがもうあれば `FileExistsError` で失敗し、何も書かない。無ければ新しく作る。
- `open(p, "r+")`: **壊しうる**。前の中身を消さずに、書いた所を上書きする（`abc` に `Z` を書くと `Zbc`）。
- `open(p, "w")`: **壊す**。開いた時点で前の中身を全部消す（何も書かなくても空になる）。

#### 確認問題 9-2

- 同じプロセスの中では、**最初の 1 回だけ**走ります。引数の無い関数なので「同じ引数」は毎回同じで、2 回目からは覚えた結果が返り、中身は走りません。
- もう一度走るのは、`関数名.cache_clear()` で覚えた結果を消した後の、次の呼び出しです（本記録者が確かめた。9.2 節）。wikimind の `close_db` のように、`cache_clear()` が見つかったら、それが**いつ**走るか（終了時か、ツールの道筋の中か）を確かめます。
- なお、サーバのプロセスを起動し直せば、新しいプロセスで覚えた結果は空なので、そこでも 1 回走ります。

#### 確認問題 9-3

- 最初に走るのは、`ensure_session` が返した **wrapper の中の、本体を呼ぶ行より前の処理**です（texas-grocery なら `auto_refresh_session_if_needed()`）。`mcp.tool(...)(f)` で登録されるのは、`@ensure_session` で `f` の名前に入った wrapper だからです（9.8 節の「形 1」）。
- 解析器は、任意のデコレータの wrapper を呼び出しとしてたどらないので、**そこを読みません**（O43、O42 の RC5、U16。`docs/open_questions.md:1194,1167,1110`）。
- 人は、デコレータの定義を grep で探して開き、wrapper の中を、本体と同じように深さを数えてたどります。見落としの判定で、wrapper の中に宣言に反しうる動作があり、解析器が何も出していなければ、原因は「その他（デコレータの wrapper の中）」の候補です（`docs/drafts/final_judging_guide_draft.md:465-467`）。いつ走るか（条件）も書き留めます。

#### 確認問題 9-4

- 道筋の `CacheManager.set` の段について、その段を呼んでいるはずの行を、1 つ手前の段（または本体）の中で探します。
- その行の**受け手**を見ます。`x.set(...)` なら、`x` に何が代入されたかをさかのぼり、`CacheManager` のオブジェクト（`CacheManager(...)` で作ったもの、またはそれを返す関数から受け取ったもの）かを確かめます。
- `set()` と受け手なしで呼んでいる行（`visited = set()` など）や、受け手が `set()`・`{}`・`[]` で作られた値なら、組み込みの型で、`CacheManager.set` との取り違え（E3）です。
- エディタの「定義へ移動」の飛び先はうのみにせず、grep（`grep -rnE '\bset\(' ...` や `grep -rn '\.set(' ...`）と、代入の行で確かめます（9.10 節）。v4 の rails-lens（M04）では、本体は `cache.set` を一度も呼んでおらず、道筋の段は 192 行の `visited: set[str] = set()` でした（`evidence/population_v4/v4_judgments.json:141`）。
