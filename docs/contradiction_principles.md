# 矛盾の判定原理（案）— **件数を見ずに**選ぶための文書

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

## 6. 選んだ原理（学生が記入する。記入後にコミットしてから実装する）

| 原理 | 選択 | 日付 | 理由（1 行） |
|---|---|---|---|
| 1-i 永続する設定 | | | |
| 1-ii リモートの状態 | | | |
| 2 静的に決まらない性質 | | | |
| 3 モデルが決める値 | | | |
| 4 対象の宣言 | | | |
