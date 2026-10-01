# AuthGap の repo の中で、判断の層に LLM を差し込める箇所

調べたのは `/home/user/auth_gap` だけで、どのファイルも変更していません。作業ファイルも作っていません。パスは `/home/user/auth_gap` からの相対で書きます。

**確かさの付け方**
- repo のコードと文書は自分で読んだので、事実はすべて**高**です。
- 外部研究の中身は repo の記録を写したものなので、repo 側の印（◎' / ○ / 中 など）をそのまま付けます。
- 【判断】と書いたものは私の分類か推論です。

## 0. 結論（この担当の範囲から）

| 箇所 | 使えるか | 主な根拠 |
|---|---|---|
| (i) 解析器の中 | **使えない** | 凍結（decisions.md:3749）、仕様書の 1 文「LLM を判定入力に使わず決定的に」（AUTHGAP_BRIEF_v3.md:36） |
| (ii) 「不」を解析器の外の後段で分ける別の腕 | **条件つきで使える**（副次の分析として別列。主指標は変えない） | 0-14 で人が判定する 100 組を正解にできる（final_evaluation_procedure.md:250-255） |
| (iii) 判定者が原ソースを読む補助 | **使える**（すでに 0-9 の選択肢にある） | final_evaluation_procedure.md:214「原ソースを読む補助に使う（判定と記録は本人）」 |
| (iv) 2 人目の判定者の代わり | **代わりにはならない** | decisions.md:3784「判定者間の一致（κ）に依存する主張はしない」 |
| (v) 語彙の見落とし候補を探す | 条件つき（解析器には足さない） | decisions.md:3870 の CodeQL 案と同じ扱い |
| (vi) 判定の手引きの曖昧さを見つける | **使える**（データを見る前だけ） | final_evaluation_procedure.md:508「段階 1 に戻って手引きを直す」 |
| (vii) LLM だけで宣言の矛を判定するベースライン | 可能だが費用が大きく、仕様書が一度削ったもの | AUTHGAP_BRIEF_v3.md:678、:951 |

**時期の制約（高）**: 事前登録の最終評価の節（§2.12）はまだ書かれていません。final_evaluation_procedure.md:264 に「D67 の 1〜4 はまだ事前登録に入っていない」とあります。LLM をどこかで使うなら、最終評価のデータを見る前の今が、書き込める最後の機会です。

**この研究に特有の事情（高）**: 仕様書は「判定経路に LLM を置かない（決定的）」ことを、先行研究との差の 1 つとして書いています。
- AUTHGAP_BRIEF_v3.md:140「MCP-BiFlow を除く 3 件は LLM を判定経路に置く。測定量 = §5.2 の 3 回一致」
- AUTHGAP_BRIEF_v3.md:82「本研究は「LLM を verdict 入力に使わない」ことを主張の一部にしている」

したがって、LLM を解析器の判定に混ぜると、自分で立てた比較の軸を失います。

---

## 1. 解析器が「不」を出す理由（v4。件数は `evidence/population_v4/contradiction_by_decl_v4_run1.md:18-53` の「組」列）

類の記号（【判断】私の分類。根拠は右の列と原理の文書の行）:
- **意** = 意味の判断。相手の API・コマンド・ライブラリの意味で決まる。LLM が原理的に答えうる。
- **読** = 原ソースを読めば決まるが、解析器が追わない形。人も LLM も読めるが、読み違えうる。
- **実** = 実行時の値か木の外で決まる。LLM でも決まらない。
- **定** = 採った原理が答えを持っていない。LLM に決めさせてはいけない。

| 宣言 | 理由 | 組 | なぜ静的に決まらないか（根拠） | 類 |
|---|---|---|---|---|
| D1 | `net_post` | 78 | POST が相手を変えるかはサーバの意味による（contradiction_principles.md:175「RPC の照会も `POST`」） | 意 |
| D1 | `spawn_command` | 64 | 定数のコマンドが環境を変えるかは名前から分からない（:165、:64「`nvidia-smi` と `tscon` の違いは名前からは分からない」） | 意＋実 |
| D1 | `net_method_unknown` | 17 | メソッドが読めない（:252「`urlopen` / `urlretrieve` / `arun` などは読めない」） | 読 → POST と分かれば意 |
| D1 | `spawn_model_opaque` | 14 | モデルの値が流れ込むが、モデリングしない関数を通るので「選べる」かが決まらない（:299-301） | 読 |
| D1 | `db_sql_unreadable` | 7 | SQL が定数に読めない（:172） | 読＋実 |
| D1 | `db_sql_model_opaque` | 2 | モデルの値がバインド変数として入るだけか、文の種類まで決めるかが決まらない（:303-305 の SQLAlchemy の例） | 意（ライブラリの意味） |
| D2 | `fs_writeout` | 121 | 新規作成か上書きか（書く前にファイルがあるか）が分からない（:187） | 実。手引きの規則で一部は読になる（final_evaluation_procedure.md:978 の「毎回同じファイルを上書きするなら反する」） |
| D2 | `net_post` | 93 | 同上（:197） | 意 |
| D2 | `spawn_command` | 19 | 同上（:184） | 意＋実 |
| D2 | `db_sql_unreadable` | 15 | 同上（:194） | 読＋実 |
| D2 | `fs_writeout_model_path_opaque` | 9 | 書き先にモデルの値が流れ込むが、選べるかが決まらない（:299-301） | 読 |
| D2 | `db_persistent` | 2 | 「追記か破壊か」が設定の変更に当てはまらない（:191） | **定** |
| D2 | `fs_unknown` | 2 | モードと破壊性が決まらない（:188）。v4 の例は子プロセスの標準入力への `pipe:write` | 読＋意 |
| D2 | `spawn_model_opaque` / `db_sql_model_opaque` | 2 / 1 | 上と同じ | 読 / 意 |
| D3 | `spawn_command` | 42 | 起動するコマンドが外部と通信するか（:211） | 意 |
| D3 | `net_host_unknown` | 22 | 宛先が設定値などで読めない（:209） | 実（一部は意。手引きは「分からなければ不明」final_evaluation_procedure.md:1000） |
| D3 | `spawn_model_opaque` / `net_model_host_opaque` | 12 / 6 | 流れ込むが選べるかが決まらない | 読 |
| D4 | `net_nonidempotent_method` | 67 | POST / PATCH の冪等性は API の意味による（:225） | 意 |
| D4 | `db_nonidempotent_statement` | 5 | 一意制約や `x = x + 1` かどうかで決まる（:222） | 読＋実（木の中の DDL や SET 式なら読める。外部の DB のスキーマなら決まらない） |
| D4 | `db_sql_unreadable` / `exec_or_spawn` | 3 / 1 | :224 / :228 | 読＋実 / 意＋実 |

**補足（すべて高。断りがあるものを除く）**
- **理由の和が「不」の件数より多い。** 理由の和は D1 182・D2 264・D3 82・D4 76 で、不の件数は 171・257・74・73 です（同ファイル:11-14）。スクリプトが (組, 理由) を数え、「理由は組の中の理由の集合」とするためです（scripts/contradiction_by_decl.py:15、:106-111）。組全体が矛でも、不の理由が数えられうるというのは私の読みで、重なりの実数は数えていません。
- **LLM の腕が動かしうる幅の上限**: 原理 2 を b（不明を矛盾に倒す）にすると、矛は D1 323→494、D2 155→412、D3 0→74、D4 3→76 になります（同:60、:63）。
- **【判断】大きい理由の性質**:
  - 意が主の理由: `net_post`（D1 78・D2 93）、`net_nonidempotent_method`（D4 67）、D3 の `spawn_command`（42）。
  - 実か定が主の理由: D2 で最大の `fs_writeout`（121）、`net_host_unknown`（22）、`db_persistent`。
- **`_opaque` の理由は意味の問題ではありません。** 値の追跡の限界で、語彙は `authgap/ir.py:126-137` の `VAL_OPAQUE_REASONS`（depth / unresolved / receiver / recursion / dynamic / cap / loop / context）です。【判断】dynamic 以外は原ソースを読めば決まりえます。ゲート側の語彙（ir.py:140-161）は付録で、矛の判定（dparse.py:372-570）には使っていません。
- **`spawn_command` の定数コマンドの例**: docker, osascript, git, grep, which, rg, ip, uptime, ping, ffmpeg, arp, dig, open, xdg-open, whois。
  - 出典は `evidence/scan_v2_v4_run1/v4-*.json` の行で、私が拾いました。これらの manifest は git で追っていません（追っているのは 2 ファイルだけ）。
  - argv0 が設定値の行もあります（rails-lens の `config.ruby_command`、v4_judgments.json:1250）。

## 2. v4 の手判定で迷った、または意味の理解が要った事例（`evidence/population_v4/v4_judgments.json`、行は note か error_class の位置）

| id（行） | 何が要ったか（逐語） | 類【判断】 | LLM に向くか【判断】 |
|---|---|---|---|
| R01（:1166） | "The call updates an existing project (name, prefix, public flag) in place."（POST の意味） | 意 | 向く |
| R08（:1264） | "a POST to a chat-completions API, which is a query" | 意 | 向く |
| R29（:1558） | 「POST の中身は products の照会…書き込みの mutation ではない」 | 意 | 向く |
| R09/R10（:1278） | "The POST issues a GitHub App installation token, conditionally" | 意＋定（トークンの発行は相手の変更か） | 半分 |
| R22〜R24（:1460） | 「トークン交換の POST は MCP_DOWNSTREAM_TOKEN_EXCHANGE が無ければ呼ばれない」 | 意＋実（運用者の設定） | 半分 |
| R27（:1530） | 「名前空間の新規作成は追加型」（boto3。解析器は効果 0 件） | 意（SDK） | 向く |
| E00〜E02（:20） | 「書く前に内容を確かめる追記は同じ引数で繰り返しても状態が変わらない」 | 読＋意（冪等） | 向く |
| M59（:1136） | 「stdin に流すのはコードではなくデータ（pickle）」 | 意＋読 | 向く |
| M00（:74） | "Semantically the UPDATE only sets a revoked_at timestamp…, but the table decides by the head word." | 意味と表の衝突。表が優先 | **危険**。意味の読みが表から外れる |
| M01〜M03（:92）、M07 ほか（:197）、M06（:182）、R15（:1362） | 起動時の初期化（lifespan か `main()` か） | 読（起動の順序） | 読む補助に向く。規則は 14.4 で決まっている |
| M58（:1118） | 「一時ファイルを「環境を変える」に含めるかは本記録者の見直しで確認してほしい」 | **定** | 向かない |
| R19（:1418） | 「ログ出力の枠組みの書き込みを宣言違反に数えるかは原理で明示されていない」（のちに手引きで決着: final_evaluation_procedure.md:966、:700-702） | **定** | 向かない |
| M13（:308）、M57（:1100）ほか reaper、M12/M15（:287） | 監査ログ、IPC ファイル（「ツールごとの独立した事例ではない」）、自分で作ったロックの削除 | 定（ラベル）＋読 | ラベル案だけ |
| M18（:398） | 引数の説明 'Path to save the report file' から本来の動作と判断 | 意（文書） | 向く（ラベル） |
| R07（:1250） | "The Ruby scripts … are not in the corpus checkout" | 実（木の外） | 向かない |
| R11（:1306） | "Whether the language server actually changes anything cannot be decided statically" | 実 | 向かない |
| R25（:1502） | ライブラリが呼び戻す POST。相手を変えるか決まらない | 実＋意 | 向かない |

**【判断】まとめ**
- **意の類（API・SDK・コマンドの意味）**: LLM が効く所です。手引き自身が人にこの調査を求めています。
  - final_evaluation_procedure.md:960「相手の API の意味を調べて決める」
  - 同:954「そのコマンドが実際に何をするかを調べ」
- **定の類（何を「環境」に含めるか、どれくらい重いか）**: LLM に決めさせてはいけません。実世界でも割れていると repo に記録があります（open_questions.md:1232-1233「OpenAI の提出ガイドはログも readOnlyHint: false、HTTP の safe method（RFC 9110）はログを safe に含める」）。決めるのは原理 §6 と D67 のラベルです。
- **実の類（木の外、運用者の設定）**: LLM を使っても決まりません。

## 3. LLM を差し込みうる箇所と、repo の約束とぶつかるか

| 箇所（段階） | 凍結（D66 ほか） | 規則 4 | 事前登録・規則 5 | 判定者 1 人（D67 の 4） | 0-9 | 判定 |
|---|---|---|---|---|---|---|
| (i) 解析器の中（`authgap/`。段階 5） | **ぶつかる**: decisions.md:3749、final_evaluation_procedure.md:13「最終評価のどの段階でも `authgap/` を変えない」、CLAUDE.md:82-83 | 解決率を上げる向きは誤 clear を作りやすい（CLAUDE.md:76-77） | 走査後の変更は禁止（final_evaluation_procedure.md:327） | — | — | **使えない** |
| (ii) 後段の別の腕で「不」を分ける（段階 7〜8） | ぶつからない（manifest と原ソースを読むだけ） | **主の「不」を置き換えればぶつかる**: CLAUDE.md:13、contradiction_principles.md:139「b / c は測定を既知の向きに偏らせる。不明の件数は必ず併記」、decisions.md:3861「解析できなかったものを分母から黙って消せない」。別列ならぶつからない | **§2.12 に事前に書くことが必須**。モデル ID・温度・プロンプト・回数を固定する。後で足すなら事後の分析（final_evaluation_procedure.md:1346） | 人の判定に混ぜない | 範囲外（0-9 は判定の補助の話） | **条件つきで可** |
| (iii) 原ソースを読む補助（矛・見落とし・不の中身・ラベル。段階 7） | ぶつからない | ぶつからない | 使う範囲を事前登録して論文で開示（final_evaluation_procedure.md:216、:1354、:1378） | 判定は本人（:214）。「AI の結論をそのまま記録しない」（:1266-1267） | **この項目そのもの**。大学の規程の確認が要る（:216） | **可** |
| (iv) 2 人目の判定者の代わり | — | — | 事前登録が要る | **ぶつかる**: decisions.md:3784「κ に依存する主張はしない」、:3786「将来 2 人目を用意できたら追加の検証として足す」 | 0-9 が想定していない使い方 | **代わりとしては不可**。参考の一致率としてなら事前登録して可 |
| (v) 語彙の見落とし候補探し（loguru の `logger.add`、`wave.open`、ORM の `add/commit`） | 解析器への追加は**ぶつかる**（CLAUDE.md:46、open_questions.md:1041 の O39、:1193 / :1197 の O43） | 見落としを数える側なので向きは安全 | 見落とし判定の補助にするなら事前登録（decisions.md:3870 の CodeQL 案と同じ） | 判定は本人 | 補助の一種 | **条件つきで可** |
| (vi) 手引きの曖昧さの検出（段階 1〜2） | ぶつからない | ぶつからない | **データを見る前に限る**（final_evaluation_procedure.md:508。途中で変えないこと :1275） | 規則を決めるのは学生 | — | **可** |
| (vii) LLM だけで矛を判定するベースライン（比較実験） | ぶつからない | — | 仕様書が削ったもの（AUTHGAP_BRIEF_v3.md:678「LLM baseline は削除した」、:951「LLM baseline を落とす」は予算表の行、:814、:1060）。復活させるなら仕様書を書き換えず decisions.md に書き（CLAUDE.md:18）、事前登録する | 正解づくりの判定が増える（見込み 170〜380 時間、final_evaluation_procedure.md:1419） | — | 可能だが費用が大きい |
| 付随: 書き込み先の種類・誤の原因・条件の種類のラベル案（16・17・14.3 節） | — | 迷えば「その他・不明」（:1051） | 定義を途中で足さない | 本人 | (iii) と同じ | 可 |
| 付随: 関連研究の要約（段階 9） | — | — | AUTHGAP_BRIEF_v3.md:82「LLM 要約に依拠したまま提出しない」 | — | — | 原文で確かめれば可 |

**項目ごとの注意（【判断】と書いたもの以外は高）**
- **(ii)**
  - 正解は 0-14 で人が判定する 100 組で作れます（final_evaluation_procedure.md:250-255）。「LLM の分類は人とどれだけ一致したか」を副次の結果として出せます。
  - 先行研究に課した決定性の測り方（3 回一致、AUTHGAP_BRIEF_v3.md:93、:140）を自分の腕にも課すのが筋です。
  - 再現性は、解析器の利点「標準ライブラリだけで再現できる」（decisions.md:3863）を持ちません。
- **(iii)**
  - 見落としの判定は「解析器の出力を見る前に判定する…先に見ると引っぱられる」（final_evaluation_procedure.md:167、:1093）です。【判断】LLM の要約も同じように引っぱるので、最初の読みは自分で行い、LLM は道筋や呼び出し元の確認に使うのが安全です。
  - D60 に「評価データを本記録者が一度も見ない・開発に使わない」（decisions.md:3400）とあり、本記録者は開発の AI です（final_evaluation_procedure.md:1236）。読む補助の LLM がこれに当たるかは文書に定義がなく、**学生の解釈が要ります**。
- **(iv)**: v3・v4 の判定はすでに AI です（population_v4.md:15、final_evaluation_procedure.md:1236「最終評価の判定の正解ではない」）。【判断】(iii) と同じ LLM を補助にも使うと、人と独立でなくなります。
- **(vii)**
  - 【判断】正解の標本は AuthGap の出力から抜きます（矛の抜き取りと、矛の無いユニット）。LLM だけが出した矛は標本に入らないので、LLM の精度を測るには別の判定が要ります（検証の偏り）。
  - 仕様書は、審査での答えを「精度ではなく出力形式（決定性・witness・宣言照合）の違い」と決めています（AUTHGAP_BRIEF_v3.md:678）。

## 4. repo の中ですでに LLM を使った箇所（事実、高）
- **v3・v4 の判定**: 本記録者（AI）が行い、原ソースの確認を木ごとに agent に分けました（population_v4.md:15、:67-68、textbook.md:1790）。論文には使いません（decisions.md:3754）。
- **添削（敵対的レビュー）**: 探す作業と確かめる作業を AI のエージェントに分担させました（textbook.md:1962）。
- **練習（6.8）**: AI の v4 の判定で答え合わせをします（final_evaluation_procedure.md:501-508）。【判断】AI の読みに合わせてしまう危険があります。食い違いは手引きの穴として扱い、AI 側を正とみなさないことです。

## 5. repo が記録している「判定層に LLM を置く」先行研究（参考。担当外なので repo の印のまま）

| 研究 | repo の記録 | repo の確かさの印 |
|---|---|---|
| DCIChecker | 「一致の判定は LLM」（implementation_base_survey.md:37）、「判定が LLM 仲裁で非決定的」（AUTHGAP_BRIEF_v3.md:93。CONTRADICTION の比較対象） | 中 / ◎'（自動要約に依拠し原文は未読） |
| TaintP2X | sanitizer の妥当性判定を DeepSeek-V3 で行う（AUTHGAP_BRIEF_v3.md:103） | ◎ / 高 |
| VIPER-MCP | 悪用の確認は LLM エージェント（implementation_base_survey.md:27） | 中 |
| antgroup/MCPScan | Semgrep + LLM（同:32） | 高 |
| Semia | 事実基盤の合成は LLM（AUTHGAP_BRIEF_v3.md:94） | ◎' |

## 確かめられなかったもの
- 所属大学の生成 AI の規程。repo に無いため、0-9 の条件（final_evaluation_procedure.md:216）が満たせるかは分かりません。
- 外部研究の本文。担当外です。DCIChecker と Semia は repo でも ◎'（原文未読）のままです。
- LLM が各理由をどれだけ正しく答えるか。測っておらず、推測もしていません。
- 理由の和が「不」の件数を超える件で、重なっている組の実数。スクリプトの読みからの推論にとどまります。
- `spawn_command` の定数コマンドの例は、git で追っていない手元の manifest から拾いました。学生の環境では走査し直さないと再現できません（final_evaluation_procedure.md:503）。
- D60 の「本記録者」に、読む補助の LLM が含まれるか。定義がありません。
- LLM の補助で判定時間がどれだけ減るか。未測定です。
- `docs/incidental_writes_practice.md` は直接読んでおらず、O44（open_questions.md:1230-1236）の要約を通して参照しました。

## 参照したファイル（絶対パス）
- /home/user/auth_gap/CLAUDE.md
- /home/user/auth_gap/AUTHGAP_BRIEF_v3.md
- /home/user/auth_gap/docs/contradiction_principles.md
- /home/user/auth_gap/docs/final_evaluation_procedure.md
- /home/user/auth_gap/docs/decisions.md
- /home/user/auth_gap/docs/open_questions.md
- /home/user/auth_gap/docs/population_v4.md
- /home/user/auth_gap/docs/textbook.md
- /home/user/auth_gap/docs/implementation_base_survey.md
- /home/user/auth_gap/evidence/population_v4/contradiction_by_decl_v4_run1.md
- /home/user/auth_gap/evidence/population_v4/v4_judgments.json
- /home/user/auth_gap/evidence/scan_v2_v4_run1/（manifest。git で追っていない）
- /home/user/auth_gap/authgap/ir.py
- /home/user/auth_gap/authgap/dparse.py
- /home/user/auth_gap/authgap/catalog/statements.py
- /home/user/auth_gap/scripts/contradiction_by_decl.py