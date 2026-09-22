# 矛盾関係の表（宣言 D × 効果）— **判定器より先に書く仕様**

**この文書は測定結果ではなく定義である。** 実装を直す**前**に書き、先にコミットする
（CLAUDE.md 規則 5「期待値ファイルは採点器より先にコミットする」と同じ理由）。
表の各マスは**仕様の文言から導ける**ので、母集団の結果を見なくても書ける。

参考に載せた「母集団 v2 の効果数」は **現状の把握**であって、マスの値の根拠ではない。
根拠は下の「一次資料」の節にある仕様の文言だけである。

---

## 1. なぜ表を書けるのか — 宣言側は有限で閉じている

MCP の `ToolAnnotations` は**これで全部**である。挙動を主張するのは **4 つ**
（`title` は表示名なので挙動の主張ではない）。

**3 つの版で完全に同一であることを確認した**（2026-09-22 取得）:

| 版 | URL |
|---|---|
| 2025-06-18 | `https://raw.githubusercontent.com/modelcontextprotocol/modelcontextprotocol/main/schema/2025-06-18/schema.ts` |
| 2025-11-25 | 同上（`2025-11-25`） |
| draft | 同上（`draft`） |

`ToolAnnotations` の本文（3 版で 1 文字も違わない）。**したがって「宣言のパターンは有限で、
今後も増えない」は現時点で検証済みの事実である**（仕様が新しい注釈を足せば変わる。
その場合は表に行を足す）。

### 一次資料（仕様の文言。訳ではなく原文）

> * `readOnlyHint` — If true, the tool does not modify its environment. **Default: false**
> * `destructiveHint` — If true, the tool may perform destructive updates to its environment.
>   If false, the tool performs only additive updates.
>   (This property is meaningful only when `readOnlyHint == false`) **Default: true**
> * `idempotentHint` — If true, calling the tool repeatedly with the same arguments
>   will have no additional effect on its environment.
>   (This property is meaningful only when `readOnlyHint == false`) **Default: false**
> * `openWorldHint` — If true, this tool may interact with an "open world" of external
>   entities. If false, the tool's domain of interaction is closed.
>   For example, the world of a web search tool is open, whereas that of a memory tool is not.
>   **Default: true**

同じファイルの冒頭にこうある（この研究の動機の一次資料）:

> NOTE: all properties in ToolAnnotations are **hints**. They are not guaranteed to provide
> a faithful description of tool behavior (including descriptive properties like `title`).

### 既定値がすべて「許容側」であることの帰結

| 注釈 | 既定値 | その値は制約を作るか |
|---|---|---|
| `readOnlyHint` | `false`（変更しうる） | **作らない** |
| `destructiveHint` | `true`（破壊しうる） | **作らない** |
| `idempotentHint` | `false`（追加の効果がありうる） | **作らない** |
| `openWorldHint` | `true`（外部と関わりうる） | **作らない** |

**4 つとも既定値は制約を作らない。** したがって `authgap/dparse.py` が「annotation の不在に
既定値を補完しない」としているのは、**仕様と一致する**（補完しても上界は動かない）。
これは設計上の保守性ではなく、**仕様からの帰結**である。この文が書けるのは今回が初めてなので、
本文の設計節に入れる。

**制約を作るのは次の 4 つの値だけ**である。表はこの 4 行しかない。

| # | 制約を作る値 | 主張 |
|---|---|---|
| D1 | `readOnlyHint: true` | 環境を変更しない |
| D2 | `destructiveHint: false`（`readOnlyHint != true` のとき） | 追記だけ |
| D3 | `openWorldHint: false` | 関わる範囲が閉じている |
| D4 | `idempotentHint: true`（`readOnlyHint != true` のとき） | 繰り返しても追加の効果が無い |

---

## 2. 矛盾の定義（規則は 1 本）

```
CONTRADICTION(D, e)  ⟺  e の sub_kind が D の上界の外にある
```

**粒度は kind ではなく sub_kind である。** ここが実装の肝で、`kind` 粒度の `upper` を
そのまま使うと誤警報になる。

> **具体例（母集団 v2 で実測）**: `readOnlyHint: true` の上界は現在 `{FS_READ, NET}` で
> **DB を丸ごと外している**。この上界を素直に使うと、**DB の読み取り 72 件が矛盾になる**。
> `SELECT` は環境を変更しないので、これは偽陽性である。
> **したがって上界は `{FS_READ, NET_READ, DB_READ}` のように sub_kind で書く必要がある。**

判定の結果は 3 通りしかない。**「不明」を clean に倒さない**（CLAUDE.md 規則 4）。

| 結果 | 意味 |
|---|---|
| **矛盾** | sub_kind が確定していて、上界の外 |
| **宣言内** | sub_kind が確定していて、上界の中 |
| **不明** | sub_kind が確定しない（SQL が読めない / HTTP メソッドが実行時引数 …） |

---

## 3. 表

母集団 v2（`evidence/scan_v2_run4`、87 木）の効果数を参考に併記する。
`現行` 列は今の `authgap/dparse.py: contradiction()` の挙動。

### D1. `readOnlyHint: true` — 「環境を変更しない」

上界（あるべき姿） = `{FS_READ, NET_READ, DB_READ}`

| 効果（sub_kind） | 矛盾か | 根拠 | 現行 | v2 の効果数 | 中身（実測） |
|---|---|---|---|---|---|
| `EXEC` | **矛盾** | 任意コードは環境を変更しうる | 報告 | 0 | — |
| `SPAWN`（両 sub_kind） | **矛盾** | 別プロセスは環境を変更しうる | 報告 | 16 | — |
| `FS_WRITE`（削除・上書き） | **矛盾** | ファイルシステムの変更 | 報告 | 45 | — |
| `FS_WRITE`（追記） | **矛盾** | 追記も変更である（D2 と違い readOnly に例外は無い） | 報告 | 12 | — |
| `DB_WRITE`（データの変更） | **矛盾** | 記憶域の変更 | 報告しない | **0** | 該当なし |
| `DB_WRITE`（`PRAGMA`） | **決めが要る（下の #1）** | 接続設定であってデータの変更ではない。ただし `journal_mode=WAL` は `-wal` ファイルを作る | 報告しない | **54** | `PRAGMA journal_mode=WAL` 52 / `busy_timeout=5000` 2 |
| `DB_READ`（`SELECT`） | 宣言内 | `SELECT` は変更しない | 報告しない | 72 | — |
| `DB`（SQL が読めない） | **不明** | 読み / 書きが決まらない | **黙っている** | 1 | — |
| `FS_READ` | 宣言内 | — | 報告しない | 75 | — |
| `NET`（書き込み系メソッド） | **決めが要る（下の #2）** | リモートの状態を変更する。`its environment` にリモートを含めるかによる | 報告しない | **9** | `httpx.AsyncClient.post` |
| `NET`（読み系メソッド） | 宣言内 | — | 報告しない | 72 | — |
| `NET`（メソッドが実行時引数） | **不明** | `httpx.AsyncClient.request(method, …)` | **黙っている** | **780** | — |
| `DISPATCH` | 合流 | 呼び先の効果を合流する | — | 0 | — |

**この行に「確実な見逃し」は無い。** 報告していない 54 + 9 件は
**表がまだ決めていないマス**に落ちているのであって、規則の取りこぼしではない。
**決めれば増える。決めるまでは報告しないのが正しい。**

### D2. `destructiveHint: false` — 「追記だけ」

仕様が「`readOnlyHint == false` のときだけ意味がある」と書いているので、
`readOnlyHint: true` が同時にあるときは D1 が優先する（現行の実装も同じ）。

上界（あるべき姿） = `{FS_READ, NET_READ, DB_READ, FS_WRITE_追記, DB_INSERT}`

| 効果（sub_kind） | 矛盾か | 根拠 | 現行 | v2 の効果数 | 中身（実測） |
|---|---|---|---|---|---|
| `EXEC` | **矛盾** | 追記に限れない | 報告 | 0 | — |
| `SPAWN` | **矛盾** | 同上 | 報告 | 5 | — |
| `FS_WRITE`（削除・上書き） | **矛盾** | 追記ではない | 報告 | 52 | — |
| `FS_WRITE`（追記 = `mkdir` / `open('a')`） | 宣言内 | 仕様の "additive updates"（**D32 の学生の決定**） | 報告しない | 73 | — |
| `FS_WRITE`（mode 不明） | **決めが要る（下の #3）** | D32 は矛盾側に倒している。**規則 4 に照らすと「不明」が正しい** | 矛盾に倒す | 0 | 該当なし |
| `DB_WRITE`（`INSERT`） | 宣言内 | 追記そのもの | 報告しない | **9** | `INSERT` 9 件。**正しく宣言内** |
| `DB_WRITE`（`DELETE` / `DROP` / `UPDATE`） | **矛盾** | 追記ではない | **報告しない** | **0** | 該当なし |
| `DB_READ` | 宣言内 | — | 報告しない | 7 | `SELECT` |
| `FS_READ` | 宣言内 | — | 報告しない | 22 | — |
| `NET`（`DELETE` メソッド） | **矛盾** | リモートの削除 | **報告しない（語彙に無い）** | **0** | 該当なし |
| `NET`（`POST` / `PUT` / `PATCH`） | **決めが要る（#2 と同じ）** | 追記とは限らない | 報告しない | 57 | — |
| `NET`（メソッドが実行時引数） | **不明** | — | **黙っている** | 52 | — |
| `NET`（読み系） | 宣言内 | — | 報告しない | 37 | — |
| `DISPATCH` | 合流 | — | — | 0 | — |

**この行にも「確実な見逃し」は無い。** `DB_WRITE` 9 件はすべて `INSERT` で、
**追記なので宣言内が正しい**。現行の挙動は正しい。

### D3. `openWorldHint: false` — 「関わる範囲が閉じている」

上界（あるべき姿） = 外部ホストへの `NET` を含まない。**それ以外の kind は制約しない。**

| 効果 | 矛盾か | 根拠 | 現行 | v2 の効果数 |
|---|---|---|---|---|
| `NET`（宛先が外部ホスト） | **矛盾** | "domain of interaction is closed" に反する | **未実装** | — |
| `NET`（宛先が localhost / private range） | 宣言内 | 閉じた範囲 | 未実装 | — |
| `NET`（宛先が解決できない） | **不明** | — | 未実装 | — |
| `NET` 合計（宛先を問わず） | — | — | **未実装** | **151** |
| `EXEC` / `SPAWN` | **不明** | 起動した先が通信するかは静的に分からない | 未実装 | 17 |
| `FS_READ` / `FS_WRITE` / `DB` | 宣言内 | ローカルの操作は閉じた範囲 | 未実装 | 287 |
| `DISPATCH` | 合流 | — | — | 0 |

**`openWorldHint: false` は上界を一切動かしていない**（`parse_d_kind` は
`present_no_bound` に入れるだけ）。**この行は丸ごと未実装である。**
母集団で `NET` 効果が 151 件ある。

### D4. `idempotentHint: true` — 「繰り返しても追加の効果が無い」

**静的に「冪等である」ことは判定できない**（任意のプログラムの等価性に帰着する）。
**しかし「冪等でない」ことの証拠は見つけられる。**片側の判定である。

| 効果 | 判定 | 根拠 |
|---|---|---|
| `open(path, 'a')`（追記） | **非冪等の証拠 → 矛盾** | 2 回呼べば 2 回追記される |
| `DB` の `INSERT`（`ON CONFLICT` 無し） | **非冪等の証拠 → 矛盾** | 行が 2 つできる |
| カウンタの加算 | **非冪等の証拠 → 矛盾** | — |
| `NET` の `POST` | **非冪等の証拠 → 矛盾** | HTTP の意味論で POST は非冪等 |
| `NET` の `PUT` / `DELETE` / `GET` | 宣言内 | HTTP の意味論で冪等 |
| それ以外すべて | **判定不能** | — |

**現行は未実装。** この行は「**片側だけ判定できる**」が完全な答えであって、空欄ではない。

---

## 4. 完全性の主張と、その限界

### 主張できること

> **宣言側は完全である。** MCP 仕様の `ToolAnnotations` は 4 つの挙動主張しか持たず、
> 3 つの版（2025-06-18 / 2025-11-25 / draft）で同一であることを確認した。
> **本表はその 4 つすべてについて矛盾関係を定義している。**

### 主張できないこと（正直に書く）

1. **効果の分割が完全であることは、仕様が保証しない。** 7 kind
   （`EXEC` / `SPAWN` / `FS_WRITE` / `FS_READ` / `NET` / `DB` / `DISPATCH`）は
   **この研究の設計**であって、MCP 仕様から導けない。
   **反論の形**: 「IPC は？ 環境変数の書き換えは？ プロセス内の大域状態は？」
   **答え方**: これらは `readOnlyHint` の意味では「環境の変更」に当たる。
   7 kind に無いので**検出できない**。**表の行としては D1 に属するが、
   実装が届かないマスとして数える。**
2. **検出が完全であることは主張しない。** opaque 52.8%、`AST_NODE_CAP` の打ち切り、
   入口カタログ外の形（`docs/open_questions.md` O21 / D17「直さない 3」）。
3. **`idempotentHint` は片側しか判定できない。**

**表が完全なのは「定義」であって「検出」ではない。** 本文ではこの 2 つを別の節に分ける。

---

## 5. 現行実装との差（実測）

`authgap/dparse.py: contradiction()` は `parse_d_kind` が作った `upper` を使わず、
手書きの kind 一覧で判定している。

```python
if kind in ("EXEC", "SPAWN"):
    return True
if kind == "FS_WRITE":
    ...
```

**上界と判定器が別々に書かれている。** ただし母集団 v2 で突き合わせた結果、
**この食い違いによる確実な見逃しは 0 件だった。**

| | 効果数 | 向き |
|---|---|---|
| 現行が報告している矛盾 | **130** | — |
| 表が**矛盾**と決めていて報告していないもの | **0** | — |
| **決めが要るマスに落ちているもの** | `DB_WRITE(PRAGMA)` 54 + `NET` 書き込み 9 + 57 = **120** | 決めれば増える |
| **「不明」と報告すべきなのに黙っているもの** | `NET` メソッド不明 780 + 52、SQL 不明 1 = **833** | **規則 4 違反** |
| `openWorldHint: false` の `NET`（丸ごと未実装） | **151** | **未実装** |

**当初「確実な見逃し 63 件」と見積もったが、これは誤りだった。**
SQL の中身を見ると `readOnlyHint: true` + `DB_WRITE` の 54 件はすべて `PRAGMA`
（接続設定）で、`destructiveHint: false` + `DB_WRITE` の 9 件はすべて `INSERT`
（追記なので宣言内。**現行の挙動が正しい**）だった。
**効果の kind だけを見て「見逃し」と数えると過大になる。sub_kind と中身まで見ないと判らない。**

### 表を書く作業そのものが見つけた解析器のバグ 2 件

**(B1) 改行で始まる `SELECT` が `DB_WRITE` に誤分類される。**

```python
head = text.strip().split(" ", 1)[0].upper()   # authgap/effects.py: _sub_kind
```

`" "` だけで切るので、`"\n  SELECT\n    id, ..."` は `strip()` 後も
`head == "SELECT\n"` になり、読み取り語の一覧に当たらず `DB_WRITE` になる。
母集団 v2 で **2 件**（どちらも宣言なしのユニットなので verdict には出ていない）。
**誤りの向きは誤警報（false-positive）**。`split()`（空白全般）にすれば直る。

**(B2) `PRAGMA` / `BEGIN` / `COMMIT` / `ROLLBACK` が `DB_WRITE` に入る。**

`_sub_kind` は「読み取り語の一覧に無ければ `DB_WRITE`」なので、接続設定と
トランザクション制御がデータの書き込みと同じ sub_kind になる。母集団 v2 で
`PRAGMA` 101 件 / `BEGIN` 1 / `COMMIT` 2 / `ROLLBACK` 1。
**`DB_WRITE` を「データの変更」の意味で使う判定（D1 / D2）を入れる前に分けないと、
101 件の誤警報になる。**

**どちらも `SUB_KINDS` の語彙（月 3 凍結）には触れず、`_sub_kind` の分類規則の修正で済む。**

---

## 6. 決めが要るマス（`docs/open_questions.md` へ）

| # | マス | 判断が要る点 | v2 の件数 |
|---|---|---|---|
| 1 | D1 × `DB_WRITE(PRAGMA)` | 接続設定は「環境の変更」か。`journal_mode=WAL` は `-wal` ファイルを作る | 54 |
| 2 | D1 / D2 × `NET`（書き込み系） | `its environment` に**リモートの状態**を含めるか。含めないなら `openWorldHint` の領分 | 9 + 57 |
| 3 | D2 × `FS_WRITE`（mode 不明） | D32 は矛盾に倒している。規則 4 なら「不明」。**D32 を見直すか** | 0 |
| 4 | D3 の宛先判定 | 「外部ホスト」の定義（private range / localhost / 環境変数由来のホスト） | 151 |
| 5 | D4 | 片側判定（非冪等の証拠探し）を実装するか、未対応と書くか | — |

**#1 と #2 は「今どちらでもない」のが正しい状態である。**決めるまで報告しない。
決めたら `docs/decisions.md` に根拠つきで書き、件数の前後を出す。

---

## 7. 実装の順序

**確実な見逃しが 0 件だったので、急ぐのは「矛盾を増やすこと」ではない。**
効いてくるのは規則 4（不明を黙って落とさない）と未実装の D3 である。

1. **この文書を先にコミットする**（済ませてから 2 に進む）。
2. **(B1) と (B2) を直す。**`_sub_kind` の分類規則だけ。`SUB_KINDS` の語彙には触れない。
   **これをやらずに D1 × `DB_WRITE` を入れると 101 件の誤警報になる。**
3. **「不明」を verdict として出す経路を作る。** 現在 833 件が黙って落ちている
   （`NET` のメソッドが実行時引数、SQL が読めない）。**規則 4 の違反であり、
   向きは誤 clear。ここが一番効く。**
4. `contradiction()` を sub_kind 粒度の上界に基づく形に書き換える。
   **`kind` 粒度の `upper` をそのまま使わない**（`DB_READ` 72 件が偽陽性になる）。
5. `openWorldHint: false` を上界に反映する（決めが要るマス #4 を決めてから）。
6. **変更の前後で件数を両方出す。** `docs/preregistration.md` に逸脱として記録する。

---

## 8. この表を書いて分かったこと（本文に書く）

**「宣言のパターンは有限だから、矛盾関係は網羅できる」は正しい。** 実際に 4 行
（`readOnlyHint:true` / `destructiveHint:false` / `openWorldHint:false` /
`idempotentHint:true`）で閉じ、仕様の 3 版で同一であることを確認した。

**しかし表を埋めてみると、当初の見立てとは違う結果になった。**

| 当初の見立て | 実際 |
|---|---|
| 「63 件の確実な見逃しがある」 | **0 件。**すべて「まだ決めていないマス」だった |
| 「判定器が `upper` を使えば直る」 | **直らない。**`kind` 粒度で使うと `DB_READ` 72 件が偽陽性 |
| 「網羅できていないのが問題」 | **問題は「不明を黙って落としている」833 件の方**だった |

**これが表を先に書く価値である。** 実装を先に触っていたら、`upper` をそのまま使って
偽陽性を 72 件作り、`PRAGMA` を 101 件警告していた。
**表は「何を検出するか」ではなく「何を検出しないと決めたか」を書く道具である。**
