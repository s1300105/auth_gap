# 矛盾の判定原理 — **件数を見ずに**選ぶための文書（2026-09-24 に §6 で確定、D56）

**この文書には母集団の件数を載せない。** マス（`docs/contradiction_matrix.md` の決めが要る行と
O23 #6 / #7）を 1 つずつ件数を見て決めると、主指標（CONTRADICTION）の定義を結果に合わせて
選ぶことになる。そこで、**仕様の文言から導ける少数の原理を先に選び、コミットしてから、
各マスへは機械的に当てはめる**（CLAUDE.md 規則 5 と同じ考え方）。

手続き:

1. 学生が下の原理 1〜4 を選ぶ（この文書だけを見て）。
2. 選んだ原理をこの文書に書き込み、**実装より先にコミットする**。
3. §5 の対応表に従って各マスを決め、実装し、run を取り直す。
4. 本文には、採った原理での結果に加え、**マスごとの 3 値（矛盾 / 宣言内 / 不明）の件数**と
   **各原理を反対側にしたときの件数（感度分析）**を載せる。

**開示**: この案を書いた者（解析の実装者）は run11 の件数を見ている（`docs/o23_cells.md`）。
原理の選択肢は仕様の文言と設計の前提（§0）だけから立てたつもりだが、偏りがありうる。
**判定者は 1 人**（2 人目は確保できない。2026-09-24 学生）。これは限界として本文に書く。

---

## 0. 前提（すでに決まっていること）

* 宣言の原文（MCP `ToolAnnotations`、2025-06-18 / 2025-11-25 / draft で同一）:
  * `readOnlyHint` — If true, the tool does not modify its environment.
  * `destructiveHint` — If false, the tool performs only additive updates.
  * `idempotentHint` — If true, calling the tool repeatedly with the same arguments will have
    no additional effect on its environment.
  * `openWorldHint` — If false, the tool's domain of interaction is closed. For example, the
    world of a web search tool is open, whereas that of a memory tool is not.
* **AuthGap が推定するのは実効権限 M（ツールが「できること」の上界）であって、ある 1 回の
  実行で「すること」ではない。** 値の主体（USER ⊑ OP ⊑ MODEL）を追うのはそのため。
* 規則 4: 解決できなかったものは「不明」として記録する。黙って安全側に倒さない。
* 表 D41 ですでに決めたマス（ファイルの削除・上書きは readOnly / destructive=false に矛盾、
  `mkdir` / `open('a')` は destructive=false に対して宣言内、DB のデータ変更は D55 で実装）は
  ここでは動かさない。

---

## 1. 原理 1 —「環境（its environment）」に何を含めるか

### 1-i. 永続する設定（データではないが、呼び出しを越えて残るもの）

例: SQLite の `PRAGMA journal_mode=WAL`（DB ファイルに記録され、`-wal` ファイルができる）。
対比: `PRAGMA foreign_keys=ON` / `busy_timeout` / `BEGIN` / `COMMIT` は接続が閉じれば消える。

* **1-i-a 含めない**: 環境はデータ（ファイルの中身、DB の行とスキーマ）と起動したプロセス。
  設定は含めない。
* **1-i-b 含める**: 呼び出しを越えて残るものはすべて環境。接続単位のものだけ除く。

### 1-ii. リモートの状態（ツールが通信する相手の側の状態）

* **1-ii-a 含めない**: 環境はツールが動いているホストの状態。相手側の状態の扱いは
  `openWorldHint` の領分とする。→ NET は readOnly / destructive=false に対して矛盾にならない。
* **1-ii-b 含める**: 相手側の状態を変えることも「環境の変更」。→ 相手側を変えるかどうかを
  判定する必要があるが、静的には相手のサーバの意味が分からない（原理 2 に回る）。

---

## 2. 原理 2 — 静的に決まらない性質をどう扱うか

例: HTTP の `POST` が相手を変えるか（RPC の照会も `POST` で送る）/ `write_text` の書き先が
既にあるか（新規作成なら追記、既存なら上書き）/ 開くモードが読めない / 定数コマンドが
環境を変えるか（`nvidia-smi` と `tscon` の違いは名前からは分からない）。

* **2-a 不明とする**（規則 4 どおり）。CONTRADICTION には数えず、マスごとに件数を別に出す。
* **2-b 矛盾に倒す**（保守側。見逃しは減るが誤警報が増える）。
* **2-c 宣言内に倒す**（楽観側。誤警報は減るが見逃しが増える）。

---

## 3. 原理 3 — 値をモデルが決められるとき、何を「できること」とみなすか

例: `open(path, mode)` の `mode` や `write_text` の `path`、`subprocess.run(argv)` の
`argv0`、HTTP の宛先ホスト、実行する SQL がモデル（MODEL）由来。

* **3-a 能力として読む**: モデルが値を選べるなら、**その引数が取りうる値の全体**を
  ツールが「できること」とみなす。モデルが既存ファイルを指せば上書きでき、任意の SQL を渡せば
  `DELETE` できるので矛盾。（§0 の「M は上界」と同じ読み方。）
* **3-b 観測できた値だけで読む**: 定数に解決できた値だけで判定し、モデル由来の値は
  「決まらない」として原理 2 に回す。

---

## 4. 原理 4 — CONTRADICTION の対象をどの宣言まで広げるか

D32 は CONTRADICTION を「破壊的な kind（EXEC / SPAWN / FS_WRITE）」に限った（D55 で表どおり
DB を足した）。

* **4-a 仕様の 4 つの主張すべて**: `openWorldHint: false`（関わる範囲が閉じている）と
  `idempotentHint: true`（繰り返しても追加の効果が無い）にも、反例が静的に示せるなら矛盾を出す。
* **4-b 破壊性の 2 つだけ**（readOnly / destructive=false）。openWorld と idempotent は
  未実装として限界に書く。

---

## 5. 原理からマスへの対応（機械的な適用。件数は載せない）

表の記号: **矛** = CONTRADICTION、**内** = 宣言内、**不** = 不明（原理 2 が 2-a のとき。
2-b なら矛、2-c なら内）、**→2** = 原理 2 に回る。

| マス | 1-i | 1-ii | 3 | 4 | 結果 |
|---|---|---|---|---|---|
| #1 接続単位の `PRAGMA` / `BEGIN` / `COMMIT` | どちらでも | — | — | — | **内** |
| #1 `PRAGMA journal_mode`（D1 readOnly） | a → 内 / b → 矛 | — | — | — | 1-i による |
| #1 `PRAGMA journal_mode`（D2 destructive=false） | a → 内 / b → →2 | — | — | — | 「追記か破壊か」は設定の変更に当てはまらない |
| #2 NET（D1 / D2） | — | a → 内 / b → →2 | — | — | 1-ii による |
| #3 FS_WRITE、mode 不明（D2） | — | — | a: mode が MODEL 由来 → 矛 / それ以外 → →2。b: →2 | — | |
| #7 `write_text` / `write_bytes` / `open('w')`（D2） | — | — | a: path が MODEL 由来 → 矛 / それ以外 → →2。b: →2 | — | 削除・移動・置換は表どおり矛のまま |
| #6 SPAWN、argv0 が MODEL 由来（D1 / D2） | — | — | a → 矛 / b → →2 | — | |
| #6 SPAWN、argv0 が定数（D1 / D2） | — | — | — | — | →2（コマンドの意味は名前から分からない） |
| DB、SQL が読めない（D1 / D2） | — | — | a: SQL が MODEL 由来 → 矛 / それ以外 → →2。b: →2 | — | |
| #4 openWorld=false × NET、宛先が localhost / private | — | — | — | a → 内 / b → 未実装 | |
| #4 同、宛先が定数の外部ホスト | — | — | — | a → 矛 / b → 未実装 | |
| #4 同、宛先が MODEL 由来 | — | — | a → 矛 / b → →2 | a のとき | |
| #4 同、宛先が読めない（OP の設定値など） | — | — | — | a のとき →2 | |
| #5 idempotent=true × `open('a')` | — | — | — | a → 矛 / b → 未実装 | 2 回呼べば 2 回追記される（静的に確定） |
| #5 同 × `INSERT` | — | — | — | a のとき →2 | 一意制約があれば冪等。スキーマを見ないと分からない |
| #5 同 × NET `POST` | — | 1-ii-b のとき →2 | — | a のとき | 相手の意味が分からない |

**すでに決まっていて動かないもの**（参考）: readOnly × FS_WRITE（新規作成を含む）は矛、
readOnly / destructive=false × EXEC は矛、destructive=false × 削除・移動・置換は矛、
readOnly × DB のデータ変更・destructive=false × `UPDATE` / `DELETE` / `DROP` などは矛（D55）。

**注**: #6 の「argv0 が MODEL 由来」を 3-a で矛にするのは、現行（SPAWN は全件矛）と同じ向き。
現行と違うのは、**argv0 が定数のとき原理 2 に回る**点（2-b なら現行と同じ）。

---

## 6. 選んだ原理（2026-09-24、学生。**実装より先にコミットする**）

学生の方針: **研究の観点を優先し、実務の観点（出力の見せ方・雑音の多さ）は判断に使わない。**
（実務と研究で分けた意見は会話で示した。両者が分かれたのは 1-i と 4 の idempotent。）

| 原理 | 選択 | 理由（1 行） |
|---|---|---|
| 1-i 永続する設定 | **b 含める** | "does not modify its environment" の字義。データに限る根拠は文言に無い |
| 1-ii リモートの状態 | **b 含める** | readOnly は「変更するか」、openWorld は「外と関わるか」で別の軸（仕様の例: web 検索は open world かつ読み取り） |
| 2 静的に決まらない性質 | **a 不明** | 規則 4。b / c は測定を既知の向きに偏らせる。不明の件数は必ず併記する |
| 3 モデルが決める値 | **a 能力として読む** | AuthGap の M は「できること」の上界。b にすると M の定義が 2 つになる |
| 4 対象の宣言 | **a 4 つすべて。宣言ごとに分けて報告** | 「宣言側は閉じているので網羅できる」が主張の芯。D3 / D4 の規則は結果を見た後に作ったので**探索的な分析**として別列にし、事前登録済みの D1 / D2 と合算しない |

---

## 7. 導いた判定表（§6 を §5 に機械的に当てはめたもの。**実装とテストはこの表に従う**）

記号: **矛** = CONTRADICTION、**内** = 宣言内、**不** = 不明（原理 2-a。CONTRADICTION に数えず、
行の注記 `contradiction_unknown:<宣言>:<理由>` として数える）。「MODEL 由来」= その slot の値の主体が
MODEL。「定数」= 確度が resolved の定数（`Value.const`）。

### 7.0 §5 から直した 2 点（導く途中で見つけた。原理の選択は変えていない）

1. **D4（idempotent）には原理 3 を当てない。** 冪等性は「**同じ引数で**繰り返したとき」の性質なので、
   引数が取りうる値の範囲（能力）は関係しない。モデル由来のコマンドや SQL も、繰り返しの間は同じ値で、
   それが冪等かはコマンドの意味による → 不。
2. **#3（mode 不明）は #7 と同じ理屈にそろえる。** mode がモデル由来で `'w'` を選べても、書き先が
   既にあるか（上書きか新規作成か）は path による。→ path が MODEL 由来なら矛、そうでなければ不。
   **実装の限界**: mode の主体は記録していないので、mode 不明は path だけで決める（母集団に該当 0）。

### 7.1 D1 `readOnlyHint: true`（事前登録済みの主指標）

| 効果 | 判定 |
|---|---|
| EXEC | 矛（表 D41 で決定済み） |
| SPAWN | `argv0` または `shell_string` が MODEL 由来 → 矛（3-a）/ それ以外 → 不（コマンドの意味は名前から分からない） |
| FS_WRITE（すべて。新規作成を含む） | 矛（決定済み） |
| DB: データ・スキーマの変更（`SQL_MODIFY_HEADS`） | 矛（D55） |
| DB: 永続する設定・保守（下の `SQL_PERSISTENT`） | 矛（1-i-b） |
| DB: 接続・トランザクション単位（下の `SQL_CONNECTION`） | 内 |
| DB: 読み取り（`SELECT` / `SHOW` / `EXPLAIN` / `DESCRIBE` / `WITH`、値を設定しない `PRAGMA`） | 内（`WITH` は O24 のまま） |
| DB: 先頭語が上のどれでもない | 不 |
| DB: SQL が定数に読めない | SQL が MODEL 由来 → 矛（3-a）/ それ以外 → 不 |
| NET: メソッドが `GET` / `HEAD` / `OPTIONS` | 内（HTTP の意味論で安全なメソッド） |
| NET: `PUT` / `PATCH` / `DELETE` | 矛（1-ii-b。HTTP の意味論で相手を変える） |
| NET: `POST` | 不（相手を変えるかはサーバの意味による。RPC の照会も `POST`） |
| NET: メソッドが読めない | メソッドが MODEL 由来 → 矛（3-a）/ それ以外 → 不 |
| FS_READ / DISPATCH | 内 |

### 7.2 D2 `destructiveHint: false`（`readOnlyHint: true` が無いとき。事前登録済みの主指標）

| 効果 | 判定 |
|---|---|
| EXEC | 矛（決定済み） |
| SPAWN | D1 と同じ（MODEL 由来 → 矛 / それ以外 → 不） |
| FS_WRITE: 追記型（`destructive=False`: `mkdir` / `makedirs` / `symlink` / `open('a' / 'x')`） | 内（決定済み） |
| FS_WRITE: 既存のものを消す・動かす・変える（`unlink` / `remove` / `rmdir` / `rmtree` / `rename` / `replace` / `move` / `chmod`） | 矛（決定済み） |
| FS_WRITE: 書き出し（`write_text` / `write_bytes` / `open('w' / '+')` / `copy` / `copy2` / `copyfile` / `unpack_archive` / `urlretrieve`） | path が MODEL 由来 → 矛（3-a）/ それ以外 → 不（#7。新規作成か上書きか静的に分からない） |
| FS_WRITE: mode 不明・`destructive` が決まらないもの | path が MODEL 由来 → 矛 / それ以外 → 不（#3、7.0 の 2） |
| DB: `INSERT` / `CREATE` | 内（D55） |
| DB: `SQL_DESTRUCTIVE_HEADS`（`UPDATE` / `DELETE` / `DROP` / `REPLACE` / `MERGE` / `TRUNCATE` / `ALTER`） | 矛（D55） |
| DB: 永続する設定・保守（`SQL_PERSISTENT`） | 不（1-i-b だが「追記か破壊か」が設定の変更に当てはまらない） |
| DB: 接続単位 / 読み取り | 内 |
| DB: 先頭語が分類に無い | 不 |
| DB: SQL が読めない | MODEL 由来 → 矛 / それ以外 → 不 |
| NET: `DELETE` / `PATCH` | 矛（既存の資源を消す・変える） |
| NET: `PUT` | URL（`url.host` / `url.path`）が MODEL 由来 → 矛 / それ以外 → 不（作成か置換か分からない。#7 と同じ理屈） |
| NET: `POST` | 不 |
| NET: `GET` / `HEAD` / `OPTIONS` | 内 |
| NET: メソッドが読めない | MODEL 由来 → 矛 / それ以外 → 不 |
| FS_READ / DISPATCH | 内 |

### 7.3 D3 `openWorldHint: false`（**探索的**。別列で報告）

| 効果 | 判定 |
|---|---|
| NET: 宛先が定数で `localhost` / private / loopback | 内 |
| NET: 宛先が定数の外部ホスト | 矛 |
| NET: 宛先が MODEL 由来 | 矛（3-a） |
| NET: 宛先が読めない（それ以外） | 不 |
| EXEC | `code_text` が MODEL 由来 → 矛 / それ以外 → 不（実行されるコードが通信するか分からない） |
| SPAWN | `argv0` / `shell_string` が MODEL 由来 → 矛 / それ以外 → 不 |
| FS_READ / FS_WRITE / DB / DISPATCH | 内（表 D41: ローカルの操作は閉じた範囲） |

### 7.4 D4 `idempotentHint: true`（`readOnlyHint: true` が無いとき。**探索的**。別列で報告）

原理 3 は当てない（7.0 の 1）。

| 効果 | 判定 |
|---|---|
| FS_WRITE: `open` 系で mode が定数の `'a'`（追記） | 矛（2 回呼べば 2 回追記される） |
| FS_WRITE: それ以外（上書き・作成・削除・移動・mode 不明を含む） | 内（同じ引数で繰り返しても状態は同じか、2 回目は失敗する）。mode 不明だけは不 |
| DB: `INSERT` / `UPDATE` / `REPLACE` / `MERGE` | 不（一意制約や `x = x + 1` かどうかで決まる） |
| DB: それ以外の先頭語 / 読み取り / 接続単位 | 内 |
| DB: SQL が読めない | 不 |
| NET: `POST` / `PATCH` | 不（HTTP の意味論で冪等とは限らない） |
| NET: `GET` / `HEAD` / `OPTIONS` / `PUT` / `DELETE` | 内（HTTP の意味論で冪等） |
| NET: メソッドが読めない | 不 |
| EXEC / SPAWN | 不 |
| FS_READ / DISPATCH | 内 |

### 7.5 SQL の分類（先頭語、大文字）

* `SQL_MODIFY_HEADS`（D55）: `INSERT UPDATE DELETE REPLACE MERGE TRUNCATE DROP CREATE ALTER`
* `SQL_CONNECTION`（接続・トランザクション単位。接続が閉じれば残らない）:
  `BEGIN COMMIT ROLLBACK SAVEPOINT RELEASE END SET RESET DETACH LISTEN UNLISTEN`、
  および `PRAGMA <名前> = …` で名前が接続単位のもの
  （`foreign_keys busy_timeout synchronous cache_size temp_store locking_mode recursive_triggers
  query_only case_sensitive_like cache_spill mmap_size threads defer_foreign_keys trusted_schema
  automatic_index secure_delete`）
* `SQL_PERSISTENT`（DB ファイルに残る設定・保守）: `VACUUM ANALYZE REINDEX`、
  `PRAGMA <名前> = …` で名前が `journal_mode user_version application_id auto_vacuum page_size
  encoding schema_version`、値を取らなくても書き込む `PRAGMA wal_checkpoint / optimize /
  incremental_vacuum`
* 読み取り: `SELECT SHOW EXPLAIN DESCRIBE WITH`、および `=` の無い `PRAGMA`（上の 3 つを除く）
* それ以外（`ATTACH`（無ければファイルを作る）、`NOTIFY`、分類に無い `PRAGMA` など）→ 不

### 7.6 HTTP メソッドの読み方

sink の名前の末尾（`requests.put` → `PUT`、`httpx.AsyncClient.post` → `POST`）。末尾が `request` の
sink（`requests.request` / `httpx.request` / `httpx.AsyncClient.request` など）は第 1 引数を読む
（定数なら大文字にして使い、MODEL 由来なら「MODEL 由来」、それ以外は読めない）。
`urlopen` / `urlretrieve` / `arun` などは読めない。

---

## 8. 結果（D56、run13）

件数と感度分析は `docs/contradiction_by_decl.md`、手検証は `docs/decisions.md` D56。
主指標（D1 + D2 の矛）165、不明 181（D1 86 / D2 95）。原理を 1 つずつ反対側にすると 153〜165、
原理 2 を b（不明を矛盾に倒す）にしたときだけ 346。

---

## 9. D56 の後に見つけた 3 つの問題の直し方（D57。**実装より先にコミットする**）

学生の指示は「O30・O32・O33 を直す」。選択肢のうちどれで直すかは、**§6 で選んだ原理から導けるもの**を
採った（件数を見て選ばない）。規則だけをここに書き、件数は D57 に書く。

### 9.1 O30 — 末尾名の解決がテストファイルの定義に結びつく

**規則**: 型の裏付けの無い末尾名の解決（`_resolve_in_tree` の木全体の名前検索）では、**呼び出し元が
テストファイルでなければ、テストファイルの定義を候補から外す。**

* 根拠: 実行中のツールのコードがテストのモジュールに届くことは無い（テストは実行時に import されない）。
  届くのは、ツール自体がテストファイルで定義されているときだけ。
* 変えないもの: import 表で明示的に結ばれた定義（`from tests.helpers import f`）、受け手の型で
  裏付けられた解決、ユニットの発見（テストファイル内のツールは今までどおりユニットにする）。
* テストファイル: パスの途中に `tests` / `test` / `testing` という名前のディレクトリがある、
  またはファイル名が `test_*.py` / `*_test.py` / `conftest.py`。
* 結果として、テストの候補が外れて**本体の候補が 1 つだけ残る**ときは、今までどおり末尾名で降りる
  （`opaque(unresolved)` を合流する。D17 改訂の規則のまま）。

### 9.2 O32 — 相対 URL の値全体を `url.host` に入れる

**規則**: URL の値の定数の先頭が `/` で、**その次の文字が `/` でない**（`"/items/" + x`）とき、それは
相対 URL なので、値全体を `url.path` にし、`url.host` は置かない。受け手が `base_url` を持つ
（`httpx.Client(base_url=…)` の `from_ctor` で `url.scheme` に入っている）ときは、`base_url` を
分割して `url.host` を取る。

* 根拠: 相対 URL の宛先はクライアントの `base_url` が決める。モデルが入れられるのはパスとクエリだけ。
* 先頭が `"/"` だけ（`"/" + x`）や `"//"` のときは**分割しない**（今までどおり値全体を `url.host`）。
  モデルが `"/evil.example/x"` を渡すと `"//evil.example/x"` になり、`urljoin` 系のクライアントでは
  宛先が変わる（誤 clear を作らない）。
* **`url.host` への `GAP_INJECT`（SSRF の座標）が減る向きの変更**なので、消える行を 1 件ずつ見る。

### 9.3 O33 —「モデル由来」は「選べる」ではなく「流れ込む」

**規則（§7 の「MODEL 由来」の定義を直す）**: 原理 3-a の「モデルが値を選べる」は、slot の値の
**主体が MODEL で、かつ確度が resolved** のときに限る。主体が MODEL でも確度が opaque（モデリング
していない関数を通った値）なら、モデルが選べるのか値が流れ込むだけなのかは静的に決まらないので、
**原理 2-a により不明**とする。

* 根拠: SQLAlchemy の `select(T).where(T.c.in_(値))` ではモデルの値はバインド変数として入るだけで、
  文の種類はコードが決める。解析器の主体 MODEL は「流れ込む」の意味で、それだけでは「選べる」と
  言えない。確度 resolved の値は、モデルの入力が**モデリングした操作だけ**（連結・書式・`Path` など）で
  slot に届いたことを表す。
* `GAP_INJECT` は変えない。注入の座標が問うのは「流れ込むか」なので、今の主体の意味で正しい。
* **帰結**: 野外ではモデルの値の多くがモデリングしていない関数を通るので、3-a が効く場面は減り、
  結果は感度分析の 3-b の行に近づく。書き出し先のパスのように実際にはモデルが選べているものも
  「不明」に移る（誤 clear ではなく「不明」への移動。規則 4 どおり）。

**あわせて直す: SQL の先頭語を定数の接頭辞から読む。** SQL の値が連結（`Str`）で、先頭の部分が
確度 resolved の定数で、その中で**最初の語の後に空白がある**とき（`"UPDATE t SET a = 1 WHERE id IN (" + …`）、
文の種類は接頭辞で決まるので先頭語を読む。`PRAGMA` の類は、接頭辞の中に名前と `=` / `(` が
揃うときだけ決め、揃わなければ不明。9.3 の規則だけを入れると、この形の本物の矛盾（readOnly のツールの
`UPDATE`）が「モデル由来で opaque」として不明に落ちるので、同時に直す。
