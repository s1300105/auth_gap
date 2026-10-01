### 第 3 章

#### 演習 3-1（起動の形を見分ける）

**1. `python X.py` で起動したとき、`_init()` はツールの受付の前に走るか**

| ファイル | 走るか | 理由 |
|---|---|---|
| A | 走る | 直接実行なので `if __name__ == "__main__":` が真になり、`main()` が `mcp.run()` の前に `_ensure_ready()` を呼ぶ（③ の形） |
| B | 走る | `mcp.run()` はサーバの `run` に進み、要求を読む前に lifespan に入る。lifespan が `yield` の前に `_ensure_ready()` を呼ぶ（3.9 節） |
| C | 走る | `_ensure_ready()` は一番上の文なので、ファイルを実行した時点で走る（3.6 節） |
| D | 走る | 直接実行なので `main()` が呼ばれ、`mcp.run()` の前に `_ensure_ready()` を呼ぶ |

**2. ④ `fastmcp run X.py:mcp` で起動できる形か。できるなら `_init()` は受付の前に走るか**

| ファイル | ④ で起動できる形か | 受付の前に走るか | 理由 |
|---|---|---|---|
| A | できる（`mcp` が一番上にある） | **走らない** | ④ はファイルを `"server_module"` として読み込むので `if __name__ == "__main__":` は偽。`main()` は呼ばれない。`_init()` は最初の `lookup` の呼び出しの中で走る |
| B | できる | 走る | ④ でも最後はサーバの `run` を呼ぶので、要求を読む前に lifespan に入る |
| C | できる | 走る | 一番上の文は、④ の読み込みでも実行される |
| D | **できない** | — | `mcp` は `main()` の中の変数で、モジュールの一番上には無い。外から `D.py:mcp` という名前で取り出せない（公式 SDK 1.30.0 の `mcp run` なら「Server object 'mcp' not found」のエラーで止まる。`mcp/cli/cli.py:196-203`） |

**3. `lookup` の道筋で、`_init()` の中のディレクトリの作成に到達するか（D67 の 2 の表）**

- A: **到達する**。表の 1 行目（`main()` の中だけで先に済ませる）。④ の起動では `main()` を通らず、最初の `lookup` の呼び出しで `_init()` が走るから。条件の種類は `起動の方法`（`docs/drafts/final_judging_guide_draft.md:254`）。
- B: **到達しない**。表の 2 行目（lifespan の中）。誤の原因は **E1**。ただし、問題文のとおり lifespan が条件なしに `_ensure_ready()` を呼び、後で `_ready` を `False` に戻す行が無いことを確かめたうえで、の結論（3.9 節の見分け方 2・3）。
- C: **到達しない**。表の 3 行目（モジュールの読み込み時）。誤の原因は **E1**。
- 補足: D は 3 で問わなかった。手引きの表の 1 行目の理由は「一番上の `mcp = FastMCP(...)` は ④ で `main()` を通らずに起動できる」なので、D のようにサーバの本体が関数の中で作られている形は、その理由の前提から外れる。この形の扱いは手引きの下書きに名指しでは書かれていないので、実際に出会ったら手引きの 19 節（読み切れなければ不明）と 22 節（手引きで決まらない事例）に従う（`docs/drafts/final_judging_guide_draft.md:541,664-669`）。

#### 演習 3-2（`__name__` を自分で確かめる）

`a.py` と `load.py` を同じフォルダに置き、そのフォルダで動かす。本記録者が repo の `.venv`（Python 3.10）と作業用の Python 3.11 で確かめた出力は次のとおり（どちらも同じ）。

1. `python a.py`
   ```
   一番上の文: __name__ は __main__
   直接実行されたときだけ
   main の中
   ```
2. `python -c "import a"`
   ```
   一番上の文: __name__ は a
   ```
3. `python -c "import a; a.main()"`
   ```
   一番上の文: __name__ は a
   main の中
   ```
4. `python load.py`
   ```
   一番上の文: __name__ は server_module
   ```

- 4 は 2 に似ている。どちらも「読み込むだけ」で、一番上の文は実行されるが、`__name__` が `"__main__"` ではないので `if __name__ == "__main__":` の中（`print("直接実行されたときだけ")` と `main()`）は実行されない。違いは `__name__` の値（`"a"` と `"server_module"`）だけ。
- ④ のコマンドは、`load.py` と同じやり方（`spec_from_file_location("server_module", …)` と `exec_module`）でファイルを読み込む（SDK 1.30.0 の `mcp/cli/cli.py:135,141`、`fastmcp` 4.0.10 の `fastmcp/utilities/mcp_server_config/v1/sources/filesystem.py:98,105`）。その後でコマンドが呼ぶのは、取り出したサーバの `run`（または `run_async`）であって、`main()` ではない。だから 4 と同じく `main()` は誰にも呼ばれない。3 のように読み込んだ側が自分で `main()` を呼べば実行されるが、④ のコマンドはそれをしない。

#### 演習 3-3（lifespan の順番を予想して確かめる）

**1・2.** 出る順番は次のとおり（本記録者が repo の `.venv`、Python 3.10.20 で確かめた）。

```
A: lifespan の起動時の処理
B: 要求を読み始める
D: 一覧を返した
C: ツール search が動いた。query = 猫 db = 接続
C: ツール search が動いた。query = 猫 db = 接続
E: lifespan の終了時の処理
F: サーバが止まった
```

A・B・D・E・F は 1 回ずつ、C は 2 回（`tools/call` が 2 つあるため）。

**3.** 走る。`async with app_lifespan(None) as ctx:` で lifespan に入り、`yield` の前（A）を実行してから、要求を読む繰り返し（B 以降）が始まる。だから A は最初の C より必ず前に出る。SDK 1.30.0 の本物の `Server` の `run` も同じ順で、663 行で lifespan に入ってから、681 行で要求を読み始める（`mcp/server/lowlevel/server.py:662-681`）。本記録者が本物の SDK 1.30.0 で動かした実験でも、③ と ④ のどちらでも lifespan の起動時の処理はツールの 1 回目より前に走った（3.9 節の表）。

**4.** `print("A: …")` を `finally:` の中（E の前）に移すと、次の順になる（本記録者が確かめた）。

```
B: 要求を読み始める
D: 一覧を返した
C: ツール search が動いた。query = 猫 db = 接続
C: ツール search が動いた。query = 猫 db = 接続
A: lifespan の起動時の処理
E: lifespan の終了時の処理
F: サーバが止まった
```

`yield` の後は終了時の処理なので、A はツールの呼び出しがすべて済んでサーバが止まるときに出る。表示の文は「起動時の処理」のままだが、実際には終了時に走っている。判定で lifespan の中を読むときは、問題の初期化が `yield` の**前**にあるかを必ず確かめる（3.9 節の見分け方 2）。

#### 演習 3-4（判定の予行）

- **(a) 到達しない**。3.8 節の表の 2 行目（lifespan の中）。3.9 節の見分け方 1（`lifespan=` で渡した関数の中を見る）、2（`yield` の前で条件なしに呼ぶ）、3（`None` に戻す行が無い）がすべて確かめられているので、ツールの呼び出しのときには `_index` は準備済みで、`os.makedirs` には届かない。誤にするなら原因は **E1**。
- **(b) 到達する**。3.8 節の表の 1 行目（`main()` の中だけ）。`mcp` が一番上にあるので、④ の起動では `main()` を通らず、最初の `find` の呼び出しで `_ensure_index()` が `os.makedirs` を実行する。条件の種類に必ず書くのは **`起動の方法`**（`docs/drafts/final_judging_guide_draft.md:254`）。
  - 補足（承認の前に決めておくとよい点）: このとき作成が起きるのは最初の呼び出しだけなので、`初回` も重なっていると読んで `起動の方法; 初回` と並べる書き方も考えられる（手引き 14.3 の「条件が重なるときは全部を `;` で並べる」、同 `:258`）。一方、`起動の方法` の行の説明自体が「`main()` を通らない起動で届く」場合を指しているので、`起動の方法` だけでよいとも読める。手引きの文面だけでは決めきれない。ただし、どちらで書いても `起動の方法` が入っていれば (B)・(C) には数えないので、数は変わらない（同 `:254,258-259`）。
  - さらに、(b) を矛の組として判定するなら、もう 1 つの問い「宣言に反するか」も答える。D1（読むだけ）に対してディレクトリの作成は「反する」（同 `:309`、原理 1-i-b）なので、2 つの問いがどちらも「はい」になり、正になりうる。
- **(c) 到達する**。lifespan は `_ensure_index()` を条件つき（`PREBUILD` という環境変数が設定されているときだけ）でしか呼ばないので、3.9 節の見分け方 2 の「条件つきなら、条件が偽のときはツールの呼び出しで届くので到達する」に当たる（同 `:287-288`）。`PREBUILD` が設定されていない起動では、最初の `find` の呼び出しで `os.makedirs` が走る。条件の種類は、手引きの条件の種類の表（環境変数で決まる条件を扱う「運用者の設定」の行など）と合わせて第 49 章で考える。
- **`ctx.info`（3 行目）と `ctx.report_progress`（5 行目）**: どちらもクライアントへの通知で、ファイル・DB・相手のサーバの状態を変えないので、D1 に**反しない**（`docs/drafts/final_judging_guide_draft.md:325`、`docs/final_evaluation_procedure.md:998`）。

#### 確認問題 3-1

`call_tool(name, arguments)` という 1 つの関数が、すべてのツールの呼び出しを受け取る。引数 `name` に、クライアントが頼んだツールの名前が入るので、`if name == "read_file":`・`elif name == "delete_file":` のように名前を比べて、どのツールの処理をするかを振り分けている。各ツールの引数は `arguments` という辞書に入っていて、`arguments["path"]` のように取り出す。申告は `call_tool` ではなく `list_tools` が返す `Tool(...)` の中に書く。

#### 確認問題 3-2

**走らない。**

- `fastmcp run server.py:mcp` は、`server.py` を `"server_module"` という名前のモジュールとして読み込み、一番上の文を実行し、その中の `mcp` を取り出して、そのサーバを動かす（`run_async`。公式 SDK の `mcp run` なら `run`）。
- 読み込みのときの `__name__` は `"server_module"` で `"__main__"` ではないので、`if __name__ == "__main__":` の中は実行されず、そこから呼ぶはずの `main()` も実行されない。コマンドの側も `main()` を呼ばない。
- 根拠: 公式 SDK 1.30.0 の `mcp/cli/cli.py:119-141`（135 行で `"server_module"` として読み込み、141 行で一番上の文を実行）と `:350`（`server.run()`）、`fastmcp` 4.0.10 の `fastmcp/utilities/mcp_server_config/v1/sources/filesystem.py:98,105` と `fastmcp/cli/run.py:271`。本記録者が SDK 1.30.0 の `mcp run server.py:mcp` で実際に動かした実験でも、`__name__` は `server_module` で、`main()` の中の記録は残らず、準備は最初のツールの呼び出しの中で走った（3.7 節）。
- 判定への帰結: 初期化が `main()` の中だけにある形は、ツールの呼び出しで届きうるので「到達する」とし、条件の種類に `起動の方法` と書く（D67 の 2。`docs/decisions.md:3773-3778`、`docs/drafts/final_judging_guide_draft.md:254,279`）。起動の方法はコードだけから決める（同 `:275`）。

#### 確認問題 3-3

**走る。**

- 根拠 1（コード）: `mcp.run()` は `run_stdio_async` を経て低レベルの `Server` の `run` を呼び（SDK 1.30.0 の `mcp/server/fastmcp/server.py:311-312,769-776`）、`Server` の `run` は 663 行で lifespan に入って `yield` の前を実行してから、681 行でクライアントからの要求を読み始める（`mcp/server/lowlevel/server.py:662-681`）。`tools/call` はこの要求を読む繰り返しの中で処理されるので、lifespan の起動時の処理はどの起動の形（①〜④）でも最初のツールの呼び出しより前に済む。
- 根拠 2（実験）: 本記録者が SDK 1.30.0 で ③ `python server.py` と ④ `mcp run server.py:mcp` の両方を動かしたところ、どちらでも lifespan の起動時の処理はツールの 1 回目より前に記録された（3.9 節の表）。
- 補足: HTTP で待ち受ける形では、lifespan は接続ごと（状態を持たない設定では要求ごと）に走るが、どちらでもその接続でのツールの呼び出しより前である（`mcp/server/streamable_http_manager.py:238,367`）。
- 注意: これは「lifespan の中で**必ず**済ませた初期化」の話である。lifespan の中の呼び出しが条件つき、初期化した値を後で `None` に戻す、失敗しても受付が始まる、のどれかなら、ツールの呼び出しで届きうるので別に確かめる（`docs/drafts/final_judging_guide_draft.md:286-290`）。必ず済ませているなら、判定は「到達しない」、誤の原因は E1（D67 の 2）。

#### 確認問題 3-4

**環境を変える操作ではない。** `ctx.info(...)` は、クライアントにログのメッセージを送る通知（MCP の `notifications/message`）で、サーバのファイル・データベース・相手のサーバの状態のどれも変えない（SDK 1.30.0 の `mcp/server/fastmcp/server.py:1299-1319,1380-1382`）。判定の手引きも「クライアントへの通知（`ctx.info()` / `ctx.report_progress()`）: 環境を変えないので反しない」としている（`docs/drafts/final_judging_guide_draft.md:325`、`docs/final_evaluation_procedure.md:998`）。したがって「読むだけ」（D1）の宣言に反しない。ただし、Python の `logging` で出力先がファイルのログを書いているなら、それは別の行として扱い、出力先を確かめる（同 `:323`）。また、同じツールのほかの行の操作は、それぞれ確かめる。
