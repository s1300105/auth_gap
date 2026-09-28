# 添削の「直す単位」（採否の表。`scripts/review_triage.py` で再生成）

所見 151 件を根本原因ごとに **55 単位**にまとめた（`evidence/review/triage.json`。全所見がちょうど 1 回ずつ入ることをコードで確かめた: 欠け 0 / 重複 0）。
整理は Opus のエージェント（単位分け 1 本 + 単位ごとの記述 55 本）。**「推奨」は整理役の推奨、「段階」は本記録者の提案で、採否（直す / 限界として記録）は学生が決める。**

| 重大度 | 直す | 一部直す | 限界として記録 |
|---|---|---|---|
| 高 | 4 | 8 | 0 |
| 中 | 10 | 18 | 0 |
| 低 | 3 | 0 | 12 |

## 本記録者の提案: 段階

- **A（先に直す）**: 最終評価の数字を直接狂わせるもの。評価の道具・非決定・打ち切りの痕跡・書いた規則（§7）との食い違い。多くは `scripts/` だけで直り、解析器の凍結の指紋に触れない。
- **B（直すかを選ぶ）**: 新しいデータで頻出しうる書き方で、D1〜D4 の判定が系統的に変わる high。ほぼすべて解決率を上げる向き（CLAUDE.md の敵対的レビューが要る）で、規模は M〜L。直すと解析器が変わり、再凍結・run21 の取り直しが要る。
- **C（既定は限界として記録）**: それ以外。論文の限界節に書く一覧にする。

| 段階 | 単位 | 重大度 | 推奨 | 向き | 宣言 | 一般に正しい直し方 | 解決率↑ | 規模 | 語彙の追加 | scripts だけ | 所見 | 名前 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | U25 | 高 | 直す | 混在 | D1 D2 tooling | 条件つきである |  | M |  |  | 2 | _self_fields の cache（鍵と番兵） |
| **A** | U33 | 中 | 一部直す | 混在 | D1 D2 D4 | 条件つきである | ○ | M |  |  | 4 | SQL の先頭語の読み方 |
| **A** | U36 | 中 | 一部直す | 混在 | D3 | 条件つきである | ○ | M |  |  | 3 | URL の分解（権威部・相対参照・列） |
| **A** | U49 | 中 | 直す | 混在 | D1 D2 tooling | 条件つきである |  | M |  |  | 3 | 打ち切り・落としたファイルの痕跡がユニット水準に残らない |
| **A** | U50 | 中 | 一部直す | 混在 | tooling D1 D2 D3 D4 | 条件つきである |  | M |  | ○ | 4 | 評価スクリプトの鍵の作り方（同一性の鍵に区別に要る成分が無い / 処理系に依存する） |
| **A** | U51 | 中 | 直す | 誤警報 | tooling D1 D2 | 条件つきである |  | S |  | ○ | 2 | contradictions.json（手検証の候補表）の行の位置と destructive が、同じ組の別の行・別の効果から取られる |
| **A** | U52 | 中 | 直す | 数え落とし | tooling D1 D2 D3 D4 | 条件つきである |  | M |  | ○ | 3 | run ディレクトリの manifest の集合が summary.json と結びついていない（書く側・読む側の両方） |
| **A** | U32 | 低 | 限界として記録 | 数え落とし | tooling | 条件つきである |  | S |  | ○ | 1 | 効果行の重複（ループ 2 周と中間関数の複数呼び出しで、中身がまったく同じ行が manifest に何本も出る） |
| **A** | U34 | 低 | 直す | 混在 | D4 D1 D2 tooling | 条件つきである |  | S |  |  | 2 | DB の分類から判定・理由への写像 |
| **A** | U53 | 低 | 直す | 数え落とし | tooling | 条件つきである |  | S |  | ○ | 1 | diff_effects の比較の値 |
| **A** | U54 | 低 | 直す | 規則との食い違い | tooling | 条件つきである |  | M |  | ○ | 1 | run と解析器の実装の指紋 |
| **A** | U55 | 低 | 限界として記録 | 規則との食い違い | tooling | 条件つきである |  | M |  | ○ | 1 | two_sided の片側だけのサイト（「サイトが無い」を「等級なし（null）」と取り違える） |
| **B** | U01 | 高 | 一部直す | 誤 clear | D1 D2 D3 D4 | 条件つきである | ○ | L |  |  | 6 | INDIRECT 形の降下（実引数・受け手・lambda・target） |
| **B** | U02 | 高 | 一部直す | 混在 | D1 D2 D3 | 条件つきである | ○ | L |  |  | 4 | env_join / _shape_join の合流が情報を落とす（属性・global の片側鍵、別名の同一性、None との合流、Map のキーごとの合流） |
| **B** | U03 | 高 | 直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 2 | 属性の書き込みの記憶（path 鍵と Obj.fields） |
| **B** | U06 | 高 | 一部直す | 誤 clear | D1 D2 D3 | 条件つきである | ○ | L |  |  | 4 | 組込みのコンテナ操作の穴（_builtin_value_op） |
| **B** | U09 | 高 | 直す | 誤 clear | D1 D2 | 条件つきである | ○ | L |  |  | 5 | モジュール・クラス水準の値の読み（_module_value） |
| **B** | U12 | 高 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 3 | 受け手型によるメソッド解決（継承・同名クラス） |
| **B** | U13 | 高 | 直す | 誤 clear | D1 D2 | 条件つきである | ○ | L |  |  | 3 | 実引数と仮引数の対応（* / **・self / cls） |
| **B** | U23 | 高 | 一部直す | 誤 clear | D1 D2 D3 | 条件つきである | ○ | L |  |  | 4 | 入口の仮引数の種付け（注釈の型・Context） |
| **B** | U26 | 高 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 3 | sink の slot に実引数を当てる処理が、Python の引数の渡し方の片方しか扱わない（`*` 展開とキーワード渡し） |
| **B** | U38 | 高 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | L |  |  | 5 | mcp 2.x の読み方（SDK の署名どおりに読まない） |
| **B** | U40 | 高 | 一部直す | 混在 | D1 D2 D3 D4 tooling | 条件つきである | ○ | M | 要 |  | 2 | 呼び出し形の登録（tool(...)(fn) / add_tool / ToolSpec）が入口にならない |
| **C** | U04 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | L |  |  | 6 | 列（Seq / Argv）の位置の操作が Python の意味を保たない |
| **C** | U05 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | L |  |  | 3 | コンテナの要素の読み（_element_of と辞書） |
| **C** | U07 | 中 | 直す | 誤 clear | D1 D2 D3 | 条件つきである | ○ | M |  |  | 3 | 値を保つ変換の TRANSFER 行の穴（rstrip 系・str()/os.fspath/as_posix・Path を返す pathlib メソッド） |
| **C** | U08 | 中 | 直す | 混在 | D1 D2 D3 | 条件つきである | ○ | M |  |  | 2 | リテラルの純関数の畳み込み（定数どうしの文字列演算の結果が「定数」として読めない） |
| **C** | U10 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 3 | G3 の import による pin（読む側の束縛を 1 件に決め打つ） |
| **C** | U11 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | L |  |  | 4 | 木内 / 外部の区別を名前の一致で決める |
| **C** | U14 | 中 | 直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 2 | 構築するクラスの特定（別名・再公開・cls） |
| **C** | U15 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 2 | dataclass 形の構築（`__init__` を書かないクラス） |
| **C** | U16 | 中 | 一部直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 4 | 暗黙に呼ばれる木内コード（__call__ / with の __enter__・__exit__ / @property の getter / 木内デコレータの wrapper） |
| **C** | U17 | 中 | 直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 2 | 入れ子のスコープ（閉包・内包） |
| **C** | U18 | 中 | 直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 1 | ジェネレータの yield が呼び出し元に届かない |
| **C** | U22 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 4 | G4 / D50 の注釈による受け手型付け（経路の欠け・Optional の書き方・None リテラル） |
| **C** | U24 | 中 | 一部直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 3 | _self_fields の作り方（メソッド形ツール / 閉包の self の種） |
| **C** | U28 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 3 | pipe 形の EXEC 判定（argv0 の字面とクラス名の部分一致に頼る） |
| **C** | U30 | 中 | 一部直す | 誤 clear | D1 D2 D3 D4 | 条件つきである | ○ | M | 要 |  | 2 | sink に届く名前・構築子の表の穴（受け手型を作る表と再公開別名の表が欠ける） |
| **C** | U39 | 中 | 一部直す | 誤 clear | D1 D2 | 条件つきである | ○ | M |  |  | 3 | デコレータ構文の照合（束縛したデコレータ・式の受け手・2 段重ね） |
| **C** | U42 | 中 | 一部直す | 混在 | D1 D2 D3 D4 | 条件つきである | ○ | L |  |  | 4 | 低レベルの name 判定の認識 |
| **C** | U43 | 中 | 一部直す | 混在 | D1 D2 D4 | 条件つきである | ○ | M |  |  | 5 | 低レベルの効果のツール帰属 |
| **C** | U44 | 中 | 一部直す | 混在 | D1 D2 | 条件つきである | ○ | M |  |  | 2 | Tool リテラルの検出と join（別名の見落としと、木全体からの名前だけの join） |
| **C** | U45 | 中 | 直す | 混在 | tooling | 条件つきである | ○ | M |  |  | 2 | tools_list の要素の解決（import 表を使わない裸名引きと、裸名の already による遮蔽） |
| **C** | U47 | 中 | 直す | 数え落とし | D1 D2 D3 D4 | 条件つきである | ○ | M |  |  | 2 | _index_body の走査（ループ本体の定義の取りこぼしと、深い入れ子での木全体の落ち） |
| **C** | U48 | 中 | 一部直す | 誤 clear | D1 D2 D3 D4 tooling | 条件つきである | ○ | M |  |  | 3 | SourceIndex の衝突と symlink |
| **C** | U19 | 低 | 限界として記録 | 数え落とし | D1 D2 | 条件つきである | ○ | M |  |  | 1 | match 文の capture の束縛 |
| **C** | U20 | 低 | 限界として記録 | 誤警報 | D1 D2 | 条件つきである | ○ | M |  |  | 1 | O31 の静的判定が条件式・短絡に効かない |
| **C** | U21 | 低 | 限界として記録 | 誤警報 | D1 D2 | 条件つきである | ○ | S |  |  | 1 | try の else の到達性 |
| **C** | U27 | 低 | 限界として記録 | 誤 clear | D1 D2 | 条件つきである |  | S |  |  | 1 | 文字列の args の argv0 の射影 |
| **C** | U29 | 低 | 限界として記録 | 混在 | D1 D2 | 条件つきである |  | M | 要 |  | 2 | git.cmd.Git の proxy 行（method *）が全メソッドに当たる |
| **C** | U31 | 低 | 限界として記録 | 誤警報 | D1 D2 tooling | 無い | ○ | M |  |  | 1 | sqlalchemy.text と execute の 2 組 |
| **C** | U35 | 低 | 限界として記録 | 誤警報 | D2 | 条件つきである |  | S | 要 |  | 1 | open の mode（a+ / x+）の破壊性 |
| **C** | U37 | 低 | 限界として記録 | 誤警報 | D3 | 条件つきである |  | S |  |  | 1 | §7.3 の private な名前の定義 |
| **C** | U41 | 低 | 限界として記録 | 混在 | D1 D2 D3 D4 tooling | 条件つきである | ○ | M |  |  | 5 | 宣言（デコレータ引数・annotations）の読み取りが SDK の署名と pydantic の変換どおりでない |
| **C** | U46 | 低 | 限界として記録 | 混在 | tooling | 条件つきである | ○ | L | 要 |  | 4 | クラス形の入口（method 規則・langroid）がクラスの構造を Python の意味で解かない |

## 単位ごとの記述

### U01 INDIRECT 形の降下（実引数・受け手・lambda・target）（段階 B・重大度 高・推奨 一部直す）

`asyncio.to_thread(f, a, b)`、`functools.partial(f, ...)`、`Thread(target=f, ...)`、`loop.run_in_executor(None, f, ...)` のように「関数を渡して後で呼んでもらう」書き方（INDIRECT 形）を、解析器は f が木の中の関数名であるときしかたどれません。たどれる場合でも、渡した実引数は 1 つしか届かず、`store.delete` のようなメソッドを渡したときは `store`（受け手）が届きません。f が lambda のとき、`subprocess.run` のようなライブラリ関数のとき、`loop` が局所変数のとき、同じ名前の関数が tests/ などにもあるときも、その先の危険な操作（効果行）が丸ごと消えます。向きは「矛盾あり」が「矛盾なし」か「不明」に化ける誤 clear です。直接呼ぶ `f(a, b)` では同じ木で矛盾が出るので、書き方を変えただけで結果が変わってしまいます。

- **宣言**: D1 / D2 / D3 / D4　**向き**: 誤 clear　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_descend_indirect` が INDIRECT 行（to_thread / partial / run_in_executor / submit / Thread(target=)）の target を「木内の関数名」としてしか扱わない: 実引数は `args_pos` の 1 つ（または `args=`）だけ渡して 2 つ目以降とキーワード・`kwargs=` を捨て、target が bound method のとき受け手を評価も受け渡しもせず（`self.<field>` 経由の sink が消える）、target が lambda（`_ev_Lambda` は dynamic を返すだけで本体を評価しない）・ライブラリ sink（`subprocess.run` / `os.remove`）・`map(sink, xs)` のときは何も出さず、target の解決を `scope=None` で走らせるので G3 の import 表の pin と O30 のテスト除外が効かない。さらに `_ev_Call` の INDIRECT 行の照合が dotted 名の完全一致なので、受け手が局所変数の `loop.run_in_executor` や呼び出し連鎖には当たらない。
- **コードの場所**: authgap/val/engine.py:1109-1147 _descend_indirect, authgap/val/engine.py:721-723 _ev_Lambda, authgap/val/engine.py:795 _ev_Call の INDIRECT 行の照合, authgap/val/engine.py:955-967 _resolve_in_tree(scope=None), authgap/catalog/transfers.py:114-139 INDIRECT 行
- **重大度の根拠**: 代表の R4-r2-1 と R4-r2-2 は、探索役・設計・一般性の 3 つの意見がそろって high（review_rows.json）。理由は 3 つ。(1) 非同期の MCP ツールが同期の処理を呼ぶときの標準の書き方で、系統的に起きる。(2) 被呼び出し側の効果行が丸ごと消えるか、MODEL（モデルが決める値）が OP/resolved（運用者の定数）にすり替わる。(3) `_descend_indirect` は `unresolved_in_tree` を記録しないので、G5 の列にも痕跡が残らない。残りの 4 件（R1-r1-4、R1-r1-5、R4-r1-10、R1-r4-3）の代表値は medium。R1-r1-4 だけは探索役が high、検証役 2 人が medium で、下げた理由は「sink を lambda の本体に書く特定の書き方」（§4.2 の medium の定義）。D3 / D4 は理由に使われていない。件数はすべて検証役・探索役が v2 の構文で数えた上限で、ツール経路への到達性と矛盾の件数への影響は未測定（vendored を含むかどうかは数えた人によって違う）。数えたもの: to_thread に位置引数 2 つ以上 198、キーワードあり 403、partial の位置引数 2 つ以上 34、Thread の kwargs= 7（R4-r2-1 の一般性）。bound method の target は to_thread で属性 634 + self.method 75、Thread で属性 61 + self.method 116（R4-r2-2 の一般性）。INDIRECT に渡した lambda は v2 で 112 箇所 / 10 木、v3 で 71 / 19、うち本体に sink らしい呼び出しを含むものは v2 で 4 / 2、v3 で 13 / 5（R1-r1-4）。名前を渡す run_in_executor 116、.submit(<名前>) 343（26/87 木）（R1-r1-5）。run20 の全木で `<indirect>` の連鎖は 4 木 71 件しかなく、受け手つきの行は 0 件（R1-r1-5 の設計）。宣言の列について: 探索役の自己申告は D1+D2 だけ。ただし消えるのは効果行そのもの（NET / FS_WRITE / DB を含む）なので、D3 / D4 の判定も同じ行に依存するのは論理的な帰結として列に入れた。D3 / D4 への影響は誰も測っていない（未測定）。
- **直し方（一般に正しいか: 条件つきである）**: `_descend_indirect` を「直接呼び出し `f(*a, **kw)` と同じ経路」にそろえる。3 つの欠陥は同じ関数にあり、検証役も「一体で規則を書く」としているので、D 番号で先に規則をコミットし、反例テスト、実装の順で進める。

(A) 実引数（R4-r2-1）。行ごとに Python の仕様どおり渡す。
- target_pos 行（to_thread / partial / submit）: `node.args[args_pos:]` を位置引数として 1 つずつ渡し、行の target_kw / args_kw 以外のキーワードはすべて kwargs として転送する。
- run_in_executor: キーワードは転送しない（API がキーワードを受けない）。
- args_kw 行（Thread / Process）: `args=` の tuple を展開し、`kwargs=` の Map を kwargs にする。`name=` / `daemon=` / `group=` は target に渡さない。
- 守り 1: target_pos 行で今の `_elements` による展開をやめる。反例は `to_thread(_run_argv, ["git","log",x])` で、今は argv[*] が OP 'git' になって x の MODEL が消える。
- 守り 2: 長さ不明の Starred より後ろの仮引数、partial の未束縛の仮引数、`kwargs=` の Map の不明キーは、OP/resolved の formal ではなく opaque(unresolved) で種付けする（Starred の主体と root を持たせる）。
- 守り 3: `defaults_ok=False` と D58 2(a)（間接の降下は静的な仮引数を持たない）は残す。反例の検討: `to_thread(rm_if, p, False)` は直接形なら O31 で枝が刈られるが、2(a) が残るので間接形では刈られず、新しい誤 clear は生まれない。

(B) 受け手（R4-r2-2）。
- target が `ast.Attribute` なら、`target_node.value` を呼び出し側の env で評価する（`_ev_Call` の受け手と同じ。`_receiver_with_path_writes` を含む）。その値を `_resolve_in_tree` と `_descend` の receiver に渡す。
- `_by_name_hint` を by_name として渡す（今は名前だけの降下が resolved と記録されている）。
- `_write_back_self` は別スレッドなので省く（保守的）。
- 反例の検討（cx_r2_2）: 外部型の受け手 `to_thread(client.get, path)` は直接形と同じ by_name の行になり、退行しない。同名メソッドが 2 クラスにある場合は、受け手の型で絞れて改善する。

(C) scope（R1-r4-3）。
- `_resolve_in_tree(fake, resolve_call_name(target_node, scope), None, scope)` とする。`dotted_of` ではなく `resolve_call_name` を使うのが要点で、これで同じモジュールの見える def の pin、import 先の pin、G3 の別名、O30 のテスト除外が掛かる。
- `ast.copy_location` で `_fake_call` に行番号を写す（`_visible_defs` が呼び出し行を使う）。
- `len(callees) != 1` の要求をやめ、ambiguous のときは D17 改訂 5 どおり全候補へ降りて opaque にする（`_ev_Call` (4) と同じ）。
- 試作 p3 で壊れる形は見つからなかった: f3_fallback は直接形と同じになり、f3_shadow の `global` 再束縛は resolved から opaque に下がり、f3_caller_in_tests は変わらない。pytest は対照と同一。
- 残る既存の限界（f3_param）: target が局所変数の場合は値を見ない。これは別件として記録する。

(D) lambda（R1-r1-4、R4-r1-10 (2)）。本体は「呼ばれることが確かな位置」でだけ評価する。
- INDIRECT の target が `ast.Lambda` なら、仮引数を inner_args で種付けして本体の式を `_eval` する。
- 名前に束縛した lambda は、Value に Lambda ノードを持たせ、`_ev_Call` で末尾名の `_resolve_in_tree` より先に横取りする。横取りしないと `run = lambda: …; run()` が木内の無関係な `run` に降りる。
- 守り: 仮引数を種付けし忘れると、`to_thread(lambda c: os.system(c), "ls")` が外側の MODEL の c を読んで誤警報になる。自由変数は囲む env を閉包として読む。深さの勘定は `_descend_env` と同じにする。未解決の呼び出しやコンテナへ逃げる lambda は opaque(dynamic) のまま残す。
- **定義した時点で本体を評価する案は採らない。** 反例 ce4_dead_lambda: 呼ばれない `remover = lambda p: os.remove(p)` を持つ readOnly ツールで FS_WRITE の矛が 2 本出る（AG_PATCH=d で確認）。呼び出し位置で評価する案（AG_PATCH=4）は to_thread の lambda を直し、使われない lambda の木は変えない。

(E) ライブラリ sink の target（R4-r1-10 (1)）。
- target を `resolve_call_name` で dotted 名に正規化する。DIRECT_SINKS に当たるか、(B) の受け手で proxy / pathlib に当たるなら、(A) の実引数で CallEvent を合成し、chain に "<indirect>" を足して on_call に渡す。
- 前提: `to_thread(subprocess.run, cmd, shell=True)` の shell=True は (A) が無いと届かず、`to_thread(path.replace, …)` / `collection.delete` は (B) が無いと当たらない。
- 局所で束縛し直した名前（`run = print`）は `resolve_call_name` が None なので sink に当たらず、正しい。
- 「生成 = 呼び出し」（呼ばれない partial / 開始されない Thread でも行が出る）は既存の設計の過大近似で、それを sink にも広げることになる点を記録する。

(F) 局所の loop / 呼び出し連鎖（R1-r1-5）。探索役の fix_sketch（末尾名で引き、`_in_tree_method` で守る）は一般に正しくない。受け手の型が不明な形では守りが効かず、反例 2 件で壊れた。
- ce_r5_untyped_submit: 今出ている Uploader.submit の FS_WRITE の矛が消える（誤 clear）。
- ce_r5_queue_handler: FS_WRITE が消え、検証されていない SPAWN の矛が出る。
- 採るなら条件を絞る: dotted が解決できず、かつ target 引数がちょうど 1 つの木内関数に解決し、かつその末尾名（run_in_executor / submit）の木内メソッドが無いときだけ INDIRECT として扱う。木内メソッドがあれば今までどおり末尾名で降りる。受け手の型が無い降下には by_name（opaque(unresolved)）を付ける。
- もう 1 つの正しい直し方（get_running_loop の戻り値を AbstractEventLoop に型付けし、ThreadPoolExecutor() を CTOR 表に足して、受け手型で引く）は、月 3 凍結の CTOR / 型遷移の表への追加になるので、ここでは採らない。

(G) `map(sink, xs)` は採らない。INDIRECT 表への追加になり、map は遅延評価なので「呼ぶ」と決め打ちできない。

(H) 手順（CLAUDE.md）。どれも「行が無い → 行が出る」または opaque → resolved の向きなので、敵対的レビューを通す。diff_effects で較正対を突き合わせ、compare_scans で消えたユニット / CONTRADICTION を 1 件ずつ確かめる。v2 / v3 の件数に合わせて条件を足さない（D61）。解析器の凍結後に入れるなら、preregistration に逸脱として記録し、指紋を取り直す。
- **記録済みの限界・決定との重なり**: D58 の改訂 (A')（decisions.md:3208）は「間接の降下は args の要素だけを渡し、キーワード引数を渡さない」を誤 clear の原因として記録した。ただし直したのは省いた仮引数に既定値を入れない側（規則 3）だけで、渡された実引数を捨てることは意図した限界として記録されていない。しかも「値の分からない仮引数」の実装は OP/resolved の `Atom(formal)` で、D58 自身の意図（値が分からない）と食い違っている。D58 2(a)（間接の降下に静的な仮引数は無い）は設計上の決定なので、直し方でも残す。D17 改訂 3 / 5・§9.1（O30）・D61 G3 は、直接呼び出しについて書いた解決規則で、INDIRECT には適用されていない（R1-r4-3 は review_plan §1 の (b)「書いた規則と実装が違う」に当たる）。`_ev_Lambda` が返す opaque(dynamic) は、語彙上「動的な属性 / 添字アクセス」の理由の流用で、lambda の限界として記録したものではない。review_plan §5 の既知の問題・O1〜O41・K1〜K7 のどれにも当たらない。6 件とも、設計の観点でも一般性の観点でも反証されていない（fix_is_general は全観点で true）。単位の中で記録に回すべき部分は 3 つ。(1) `map(sink, xs)`: INDIRECT 表への追加で、D17 の「直さない 3」と同じ論理なので学生の D 番号で決める。遅延評価なので言語の意味からも導けない。(2) 局所の Executor / loop を受け手型で引く直し方: 月 3 凍結の CTOR 表への追加が要る。(3) lambda の定義時評価: 反例があるので採らない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。6 件とも探索役の影響の申告は D1+D2 で、検証役の severity_opinion の理由に「D3 / D4 だけなら low」の文言は出てこない。R1-r1-4 は探索役の high から検証役 2 人が medium に下げたが、理由は「sink を lambda の本体に書く特定の書き方」（§4.2 の medium の定義）で、旧文言によるものではない。
- **推奨の理由**: 代表の 2 件（R4-r2-1 実引数、R4-r2-2 受け手）は high で、Python の標準ライブラリの仕様から正解が決まり、INDIRECT 表も sink 語彙も変えずに直せる。設計の観点での反証も無い。R1-r4-3（scope）・R1-r1-4（lambda を呼び出し位置で評価）・R4-r1-10 (1)（ライブラリ sink の target）も medium で、検証役の条件つきで一般に正しい直し方があり、語彙の追加は要らないので、同じ関数の中で一緒に直すのがよい（(E) は (A)(B) が前提）。一方、次の部分は fix の基準を満たさないので限界として記録に回す: `map(sink, xs)`（表の追加、遅延評価）、局所の Executor / loop を受け手型で引く直し方（月 3 凍結の CTOR 表への追加）、lambda の定義時評価（反例あり）。R1-r1-5 は条件を絞った末尾名の照合なら語彙を足さずに直せるが、探索役の素案のままでは反例 2 件で壊れる。採るかは学生が決める。どれも「行が出る / 解決率が上がる」向きなので、敵対的レビューと diff_effects / compare_scans が要り、作業の規模は大きい（L）。
- **所見**:
  - R4-r2-1: 代表（high、3 観点とも high）。実引数を args_pos の 1 つしか渡さず、MODEL が OP/resolved の formal にすり替わる（矛 → 不）。fix（(A)。Starred / partial の未束縛の仮引数は opaque、target_pos 行では展開をやめる、D58 2(a) は残す）（INDIRECT 表は `args_pos` の位置引数 1 つ（または `args=`）しか渡さず、`to_thread(f, a, b)` / `partial(f, a, b)` の 2 つ目以降の実引数と `Thread(targe）
  - R4-r2-2: 代表と並ぶ high（3 観点とも high）。bound method の target で受け手を渡さず、self.<field> 経由の DB / NET / pipe の行が丸ごと消える。fix（(B)。受け手の評価と by_name の受け渡し）。R4-r1-10 (1) の proxy 形の前提（INDIRECT 形（to_thread / partial / Thread(target=)）の target が bound method（`store.delete` / `self._delete`）のとき受け手を評価も受け渡しも）
  - R1-r4-3: 同じ関数の別の表れ（medium）。scope=None なので pin と O30 のテスト除外が効かず、同名の関数があるだけで解決できなくなる。書いた規則（§9.1 / D17 改訂 3・5）と実装の食い違い。fix（(C)。試作 p3 で反例なし）（INDIRECT 形（`asyncio.to_thread` / `threading.Thread(target=)` / `functools.partial` / `submit` / `run_in_executor`）の targ）
  - R1-r1-4: 同じ根本原因の別の表れ（medium。探索役は high）。lambda の本体を評価しない。fix は呼び出し位置での評価だけ（(D)）。定義時評価は反例 ce4_dead_lambda（誤警報）があるので採らない。via_executor_lambda は R1-r1-5 も要る（`lambda` の本体を一度も評価しない（`_ev_Lambda` は `dynamic` を返すだけ）ので、`asyncio.to_thread(lambda: ...)` / `run_in_executor(None, lambda）
  - R4-r1-10: 同じ根本原因の別の表れ（medium）。target がライブラリ sink のとき・lambda・map のときに行が消える。(1) sink の target は fix（(E)。(A)(B) が前提）、(2) lambda は R1-r1-4 と同じ、(3) map(sink, xs) は表の追加で遅延評価なので記録に回す。executor_remove / executor_lambda は R1-r1-5 が要る（INDIRECT 形（to_thread / run_in_executor / partial）の target がライブラリ sink（subprocess.run / os.remove / os.chmod）のとき、また lambd）
  - R1-r1-5: 入口の照合の表れ（medium）。INDIRECT 行が dotted 名の完全一致なので、局所の loop や呼び出し連鎖の run_in_executor / submit に当たらない（9 行中 5 行が実質死んでいる）。探索役の素案は反例 2 件で壊れる。条件を絞った末尾名の照合（(F)）なら語彙を足さずに直せるが、受け手型で引く正攻法は凍結した CTOR 表への追加になるので、部分的に記録へ回すかは学生が判断する（INDIRECT 行 `loop.run_in_executor` は受け手がローカル変数（`loop = asyncio.get_event_loop()`）だと `resolve_call_name` が None を返すので当たらず、）

### U02 env_join / _shape_join の合流が情報を落とす（属性・global の片側鍵、別名の同一性、None との合流、Map のキーごとの合流）（段階 B・重大度 高・推奨 一部直す）

if / for / try のあと、2 つの経路で作った値を 1 つにまとめる処理（合流）が、4 通りの書き方で情報を落とします。(1) `if tmp: self.path = "/tmp/x"` のように片方の枝だけで属性や global 名を書くと、もう片方の経路で読める元の値（ツール引数から来た値）と混ぜないので、モデルが決める値が固定値に見えて矛盾を見逃します（誤 clear、high）。(2) `x = Path(...) if c else None` や `self.log = None` のあとで Path を入れる書き方で、None と混ぜた Path / 列 / 辞書が「形の分からない値」になります。その結果、ファイル書き込みの行が丸ごと消えたり（誤 clear）、定数の argv0 がモデル由来に見えたり（誤警報）します。(3) 定数キーの辞書にキーを足すか分岐で作り分けると定数の項目が全部消え、`cfg["exe"]` の "ping" や "GET" がモデル由来に見えて誤警報になります。(4) `alias = r` の別名が分岐を 1 つ通ると切れて、別名経由の書き込みが元の名前に届きません（誤 clear、low でまれ）。

- **宣言**: D1 / D2 / D3　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 分岐・ループ・try の合流（`env_join` → `value_join` → `_shape_join`）が情報を落とす: 片側だけの鍵をその側の値のまま残す規則（D59 O36-3。局所名なら他方の経路は NameError という根拠）を属性パス `self.x` / `OBJ.x` と `global` 名にも当て、他方の経路で読める既存の値（Obj.fields・モジュール値）と合流しない; 両側が同一の Value でも `value_join` が新しいオブジェクトを作るので `is` による別名の追跡が切れる; 「None リテラルとの合流は None 側が dead」（D35 (a)）が Obj にしか無く Path / Seq / Map / Str / Atom(定数) ⊔ None が Unknown / Atom() に潰れる; 同種の Map を `Map((), None)` にし、添字代入 / update も `_append_tail` → `value_join(Map, v)` で Unknown にする（キーごとに合流しない）。
- **コードの場所**: authgap/val/engine.py:137-154 env_join, authgap/ir.py:464-476 value_join, authgap/ir.py:479-539 _shape_join, authgap/val/engine.py:343, 365-370, 427 合流点（_exec_stmt / _exec_loop）, authgap/val/engine.py:465-473 _bind Subscript → _append_tail, authgap/val/engine.py:1197-1200 _builtin_value_op の別名
- **重大度の根拠**: 代表の R1-r1-1 は探索役・設計・一般性の 3 意見とも high。MODEL → OP の誤 clear で、行は残るので compare_scans の「消えた行」には出ない。`if self.x is None: self.x = DEFAULT` の常套句がそのまま当たる。構文上の上限（vendored を含み、到達性は未測定）は、条件つきの `self.x = <定数>` のあと同じ関数で `self.x` を読む形が v2 で 66 箇所 / 13 木、v3 で 42 / 18。global の同じ形は v2 で 10 / 4、v3 で 7 / 5。R1-r3-4 と R1-r5-1 は 3 意見とも medium、R1-r3-11 は 3 意見とも low（別名＋分岐＋別名経由の変更＋元の名前での読み出しの組み合わせが要り、まれ）。R1-r3-4 は NET の url.host を MODEL/resolved Unknown にするので D3 にも効く。D62 以降は D3 も主指標なので、重大度を下げる理由にはならない。v2 / v3 の矛の件数への影響は未測定。
- **直し方（一般に正しいか: 条件つきである）**: 共通の手順: 規則 → 反例テスト → 実装の順でコミットし、scan_v2_run21 を取る。diff_effects / compare_scans で slot の変化（OP→MODEL、resolved→opaque、行の増減）を 1 件ずつ確かめる。逸脱 #24 に記録する。

【R1-r1-1（直す）】If / Try の handler 入口と合流 / match / `_exec_loop` の 2 つの env_join のすべてで、片側にしか無い鍵を他方で読める値と value_join する。鍵に `.` を含むときは他方の基底 Obj の同名フィールド、global 宣言名はモジュール値が相手になる。他方に記録された値が無いときだけ、今の片側の挙動を残す。局所名は D59 O36-3 のまま（Python の意味どおり NameError）。
守り: (a) 素の value_join は壊す。他方の記録値が Unknown（未解決の外部呼び出しで作ったフィールドやモジュール値）だと `_shape_join(Obj, Unknown)` = Unknown になり、受け手型が落ちて proxy sink の行が消える。試作 AG_PATCH=1 では、反例 ce1_unknown_field の NET 行と D3 の矛が消えた。global 版の `_CLIENT2 = build_default()` も同じだった。避け方は、他方が Unknown 形なら片側の形を保ち、主体・root は join し、確度だけを opaque に落とすこと（D17 改訂 4 / `_opaque_deep` と同じ符号化）。試作 AG_PATCH=1p で所見の期待 4 件がすべて出て、反例 3 形の行は残った。(b) global 宣言名では、`_module_value` が `local_bindings` を迂回しないといけない。迂回しないと global_branch が直らない。(c) `CFG.mode` のようなモジュール水準オブジェクトの基底は `_module_value(CFG)` を基底にする（試作では未実装）。(d) `_resolution_of`（effects.py:231）は受け手の確度を行の resolution に入れない。受け手を opaque にしても行は resolved と表示されるので、合流させるか限界として書く。
この変更の向きは MODEL / opaque を足すほうで、解決率は上げない。

【R1-r3-4（直す）】`_shape_join` の同種の Map は、キーごとに value_join する。片側だけのキーは Obj.fields と同じく opaque(unresolved) を合流して残し、tail は両側を join する。
添字代入: キーが resolved の文字列定数なら、その項目を置き換えるか足す。
守り: 所見の fix_sketch「非定数キーは tail にだけ入れる」は健全でない。`cfg = {"exe": "ping"}; cfg[key] = target`（key がツール引数）では key == "exe" になりうるので、今の spawn_model の矛が正しい。試作 '4n' はこれを 'ping' の OP にして、矛 → 不の誤 clear を作った。`for k in keys: cfg[k] = target` も同じ。構文上限で v2 の 10 箇所 / 9 木。非定数キーの store は値を「既存の全項目と tail」に合流する。`update(**kw)` は定数キーの置き換えとして扱う。`update(d)` は、d が resolved の Map で tail が無いときだけ項目ごとに併合し、それ以外は非定数 store として扱う（update_const_key / update_from_unknown を誤 clear にしないため）。entries は K=16 で widening。試作 '4' は所見の 4 ユニットを直し、model_key_store / loop_model_key_store / update_const_key の矛を保った。較正 14 木では効果行・矛盾の注記の増減が 0 で、pytest は 685 passed。
同じ規則で直らない隣の穴: `_ev_Dict` の `{"exe": "ping", key: target}`、`setdefault`、helper の中の store、`_ev_Dict` が K を超える項目を黙って捨てること。R1-r1-9（Seq の添字代入）と同じコミットにするのが自然。
定数の回復（MODEL Unknown → OP 定数）になるので敵対的レビューを通す。

【R1-r5-1（形の部分は直す、Atom の部分は記録）】D35 (a) を広げる。他方が None リテラル（Atom.none）で、こちらが Obj / Path / Seq / Argv / Map / Str なら、こちらの形を返す。両方向で対称にする。主体・確度・root は今までどおり value_join が合流するので、MODEL は落ちない。
守り: `Atom(定数) ⊔ Atom(none)` は D59 O36-2 で明示的に決めた規則で、可換性を保つために `Atom()` にしている。これは `_shape_join` の水準では一般化できない。`shell = True if x else None` では None が偽として効くので、今の config-conditional の 2 行が正しく、真偽の Atom を含めると argv 側の行が消える。`cwd=` / `env=` / `timeout=` なども None が値として意味を持つ。真偽・数・formal つきの Atom と `Atom()` は変えない。
opaque → resolved の向き（受け手型の回復で FS 行が増える）なので、CLAUDE.md の敵対的レビューを通す。`_receiver_typed_key` で新しく出た行を 1 件ずつ確かめる。

【R1-r3-11（記録を推奨）】所見の素朴な直し方「value_join は a is b なら a を返す」は、それだけ入れると壊れる。`_element_of` は tail の Value そのものを返すので、`a = runners[i]; b = runners[j]` が偽の別名になる。しかも `_receiver_with_path_writes` は別名側のフィールドを上書き（強い更新）する。反例 ce11b の list_with_branch / pool_with_branch は今は正しく矛になっているが、誤 clear に変わる。
一般に正しい直し方: 別名経由の書き込みを弱い更新（value_join）にし、`_receiver_with_path_writes` の別名側の `fields[f] = v` の上書きをやめる。そのうえで `a is b → a` と、`_builtin_value_op` の別名への書き戻しを入れる。これで既存の分岐無しの誤 clear（list_no_branch / pool_no_branch）も直る。ただし片方の枝で両方の名前を書き戻した形は、なお切れる（部分的）。
**R1-r1-1 の実装で `a is b` の近道を単独で入れないこと。**
- **記録済みの限界・決定との重なり**: D59 O36-3（片側だけの束縛はその側の値を残す）は局所名についての決定で、根拠の NameError は属性パスと global には成り立たない。設計の観点は、R1-r1-1 はこの決定の適用範囲の穴で、呼び直しではないと判定した。
D35 (a)(c)（Obj ⊔ None = Obj、`_write_back_self` の合流）は Obj と呼び出し元への書き戻しにしか入っていない。同じ根拠が Path / Seq / Map / Str にも成り立つ。
D59 O36-2（Atom は none・型・値がすべて等しいときだけ同じ）は明示の決定で、帰結（定数 → Atom() で矛 → 不）も先に受け入れている。そのため設計の観点は、R1-r5-1 のうち atom_none_sql / atom_none_mode を「規則どおり」（反証相当）とした。
D17 は Seq / Argv を要素ごとの合流に直したが、Map は残した。R1-r1-9 の fix は「Map は今のまま」と明記しているので、R1-r3-4 を覆わない。
D17 改訂 2 / 3（global で再束縛される名前は resolved の定数として読まない）と、R1-r1-1 の global_branch の今の出力（fs_mode=a resolved）は食い違う。
D35 の限界 1（コンテナ / 引数 / 戻り値経由の別名は追わない）は、単純な `b = a` は追うと書いている。R1-r3-11 はこの主張と実装の食い違いで、限界の言い直しではない。
別経路の近い所見（この単位の直し方では直らない）: R1-r4-7（`**` 展開）、R1-r3-2（属性書き込みが fields に載らない）、R1-r4-10（再束縛で古い属性鍵が残る）。
review_plan §5 の既知の問題 / K1〜K7 / O41 には、4 件とも当たらない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 重大度を下げた形跡は無い。R1-r3-4 の設計の観点が「url.host の MODEL 化は D3 の探索列にも効くが記録のみ」と書いており、旧文言で D3 の効きを対象外に扱っている。ただし重大度は D1 / D2 の誤警報で medium と付けていて、下げてはいない。D62 以降は、この D3 の誤警報（NET の url.host が MODEL/resolved Unknown）も同じ直し方の対象に入る。R1-r1-1 の一般性の反例（素朴な直し方で NET 行と D3 の矛が消える）は D3 に効く壊れ方として守りに写した。R1-r3-11 の low は、組み合わせがまれなことが理由で、旧文言によるものではない。
- **推奨の理由**: R1-r1-1（high）・R1-r3-4（medium）・R1-r5-1 の形の部分（medium）は、どれも「直す」の基準を満たす。検証役の条件つきで一般に正しい直し方があり、語彙の追加は要らず、設計の観点の反証も受けていない。R1-r1-1 と R1-r3-4 は試作で所見の期待と反例の保持を確かめてある（R1-r3-4 は較正 14 木で増減 0）。
R1-r5-1 の `Atom(定数) ⊔ None` の部分は D59 O36-2 の明示の決定どおりで、`shell=` / `cwd=` などの反例があり、`_shape_join` では一般化できない。こちらは限界として記録する。
R1-r3-11 は low でまれな書き方で、しかも素朴な直し方が今正しく出ている矛を誤 clear に変える。正しい直し方は別名経由の書き込みを弱い更新にする設計変更を伴い、それでも部分的にしか直らないので、限界として記録するのを推奨する。記録には、ce11b の分岐無し版の既存の誤 clear も含める。
直す部分は opaque → resolved や定数の回復の向きを含むので、CLAUDE.md の敵対的レビューを通す。
- **所見**:
  - R1-r1-1: 代表（high、3 意見とも high、再現 22/22 行）。属性パスと global の片側鍵が既存のフィールドやモジュール値と合流しない。条件 (a)〜(d) をつけて直すのを推奨。守りは、Unknown 相手では形を保って確度だけ落とすこと、global では local_bindings を迂回すること。（`env_join` の「片側だけの束縛はその側の値を残す」規則が属性パス（`self.x` / `OBJ.x`）と `global` 名にも適用され、片方の枝の書き込みが他方の経路で読める既存の値（フィールド / モジュール値）と合流せず）
  - R1-r3-4: 同じ合流機構の別の表れ（medium、誤警報、D1/D2 と D3 の url.host）。Map を `Map((), None)` にし、添字代入 / update で Unknown にする。非定数キーは全項目と tail に合流する条件で直すのを推奨（sketch の「tail だけ」は誤 clear を作る）。（`Map` の widening が定数の項目を全部捨てる: 分岐の合流（`_shape_join` の同種 Map → `Map((), None)`）と添字代入 / `update`（`_bind` Subscript → `_appe）
  - R1-r5-1: 同じ `_shape_join` の別の表れ（medium、第 5 回で事前登録の手続きの外 †）。Path / Seq / Argv / Map / Str ⊔ None は直すのを推奨。Atom(定数) ⊔ None は D59 O36-2 どおりと設計の観点が判定したので、限界として記録。（`_shape_join` の「None リテラルとの合流は None 側が dead」の規則（D35 (a)）が `Obj` にしか無く、`Path` / `Seq` / `Map` / `Atom(定数)` と `None` の合流が ）
  - R1-r3-11: 同じ value_join の別の表れ（low、3 意見とも low、件数未測定）。`is` による別名が合流で切れる。素朴な直し方（a is b → a）は偽の別名で誤 clear を作る。正しい直し方は弱い更新を伴う設計変更で部分的にしか直らないので、限界として記録するのを推奨。（別名（`alias = r` / `argv = cmd`）の追跡が `is` 同一性だけで、`env_join` は両側に同じ Value がある鍵にも `value_join` で新しいオブジェクトを作るため、分岐・ループ・try を ）

### U03 属性の書き込みの記憶（path 鍵と Obj.fields）（段階 B・重大度 高・推奨 直す）

解析器は、オブジェクトの属性に書いた値（c.cmd = cmd）を 2 か所で覚えています。1 つは変数名に付いた「c.cmd」という鍵、もう 1 つはオブジェクト自身の中身（Obj.fields）です。問題は、書き込みを鍵にしか置かないことです。そのためオブジェクトを別の関数に渡す、関数から返す、2 段の属性（h.config.cmd）に書いてから h.save() を呼ぶ、のどれかをすると、呼ばれた側には __init__ の既定値（定数 'ls'）しか見えません。モデルが決めたコマンドが「作者が固定した確かな定数」に置き換わり、本当は矛盾（矛）なのに「判定できない（不）」に落ちます。これは誤 clear の向きです。逆に、名前を新しいオブジェクトに束縛し直しても古い「s.path」の鍵が消えず、新しいオブジェクトの値を古い定数で上書きしてしまうので、こちらも同じ向きの誤 clear になります。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 局所オブジェクトへの属性の書き込み `c.cmd = v` を `_bind` が env の path 鍵（`c.cmd`）にだけ置いて `Obj.fields` に写さず、`_ev_Attribute` は Obj.fields より先に env の鍵を読む。そのため、そのオブジェクトを実引数として渡す / 関数から返す / 2 段の属性に書いてから外側のメソッドを呼ぶと被呼び出しは `__init__` の既定値（OP/resolved）を読み（`_receiver_with_path_writes` は直接の受け手 1 段にしか効かない）、名前を束縛し直しても古い `name.*` 鍵が消えずに新しいオブジェクトの読み出し・書き戻しを上書きする。
- **コードの場所**: authgap/val/engine.py:445-455 _bind（Name / Attribute）, authgap/val/engine.py:517-521 _ev_Attribute の env 鍵の先読み, authgap/val/engine.py:1438-1454 _receiver_with_path_writes, authgap/val/engine.py:1401-1436 _write_back_self, authgap/val/engine.py:814-820, 1096-1107 呼び出しでの受け渡し
- **重大度の根拠**: 代表は R1-r3-2 です。重大度の見立ては探索役が high、一般性の観点が high、設計の観点が medium でした。誤りの値は opaque ではなく「OP/resolved の定数」なので、D17 改訂 2 が最も重いとした「MODEL が定数の OP/resolved に化ける」向きにあたります。一般性の観点は v2 の 100 木で構文上の上限を数えています。属性に書き込んだ後に引数として渡す形が 519 箇所 / 27 木、書き込んだ後に返す形が 248 箇所 / 35 木、2 段の属性に書き込んだ後にメソッドを呼ぶ形が 401 箇所 / 41 木です。ただし到達できるか、sink があるかは見ていないので、実際に判定が変わる件数は未測定です。設計の観点が medium にしたのは、4 形のうち 3 形（引数・キーワード引数・戻り値）が D35 の「残る既知の限界 1」（コンテナ / 引数 / 戻り値経由の別名は追わない）と根本原因が同じで、未記録なのは 2 段パスの形だけ、と見たからです。同じ観点が「一括で直すなら high 相当の頻度になりうる」とも書いています。R1-r4-10 は 3 観点とも low でした（同じ変数を 2 つのオブジェクトに使い回す、まれな書き方のため）。D3 / D4 に効くかは探索役・検証役とも見ておらず、未測定です。
- **直し方（一般に正しいか: 条件つきである）**: 基本の方針は「書き込みを Obj.fields にも書き通し、2 つの記憶を一致させる」ことです（R1-r3-2 の fix_sketch の案 A。一般性の観点が試作 AG_PATCH=2 で確かめた形）。
(1) _bind の Attribute の枝では、基底パス（c、または 2 段なら h.config）の値が Obj のとき、fields を更新した新しい Obj を基底パスに束縛し直します。2 段の h.config.cmd なら、h の Obj の config field も新しい値に差し替えます（深さは RECEIVER_DEPTH = 2 まで）。
[条件 1] Value は不変で、別名は同一性（v is old）で見分けています。そのため a だけを差し替えると、b = a の b 側の別名が切れて書き込みが失われます（設計の観点の反例 b = a; a.cmd = cmd; b.run()）。_write_back_self と同じく、env の中で同一の Value を指す別名すべてを、同じ新しい Value に束縛し直してください。
[条件 2] 他の Obj の fields の 1 段（h.config = c の後の c.cmd = cmd）も、同一性で見つけて差し替えます。
(2) 案 B「実引数にも _receiver_with_path_writes を当てる」は採りません。束縛し直し（c = Config()）の後も古い鍵 c.cmd が残るので、渡した Obj に MODEL を運び、誤警報になります。案 A なら新しい Obj の fields を読むので、rebound_after_write は 'ls' のまま正しく保たれます。
(3) R1-r4-10 の直し方として、_bind の Name の枝で名前を束縛し直すとき、name + '.' で始まる env の鍵を消します。Tuple / List の展開・for の対象・with-as・walrus（:=）・del にも同じ扱いをかけます。別名（t = s）の鍵 t.* は消しません。
[反例・避ける条件] 素朴に「同一の値でなければ name.* を消す」とすると、s = s or Store('/tmp/other') と s = Store(...) if fresh else s で、今は正しい D2 の矛が不に落ちます（一般性の観点の cx10b。新しい誤 clear）。除外を s = s だけにしても足りません。避け方は 2 通りあります。(a) 消すのを、右辺が新しい割り当て（木の中のクラスの構築やリテラル）で古いオブジェクトと別物と分かるときに限る。(b) 束縛し直す前に name.* の鍵を古い Obj の fields に畳み込んでから右辺を評価し、その後で鍵を消す（右辺が古いオブジェクトを返せば、書き込みも一緒に運ばれる）。(1) の案 A を先に入れれば、書き込みはもともと fields に載っているので (b) と同じ効果になります。そのうえで cx10b を反例テストに必ず入れてください。
(4) 変えないもの: 被呼び出し側の書き込みを呼び出し側へ戻すこと（callee_sanitizes）は今までどおり戻しません（保守側）。受け手が Unknown のときは OP/opaque のまま、渡した後の書き込み（write_after_pass）は 'ls' のままです。
(5) 直しても残る限界として記録するもの: 分岐の片側だけで束縛し直す形（合流の後に古い鍵が残る。R1-r4-10 の一般性の観点）、コンテナ経由の別名（D35 限界 1 の残り）。D35 限界 1 の文言は、引数・戻り値経由が直った範囲に合わせて decisions.md に書き直します。
(6) 確かめ方: D35 と同じ反証 13 形（条件つき書き込み・別名・再束縛・ループ）、ce2_attr_boundary の 6 形、cx10b、所見の再現の木を使います。そのうえで diff_effects を較正 14 木にかけ（試作では増減 0、pytest 685 passed）、scan_v2 を取り直して compare_scans で消えた CONTRADICTION を 1 件ずつ見ます。
- **記録済みの限界・決定との重なり**: D35 の「残る既知の限界 1」（docs/decisions.md。「コンテナ / 引数 / 戻り値経由の別名は追わない」）が、R1-r3-2 の 3 形（位置引数・キーワード引数・戻り値）と根本原因で重なります（設計・一般性の両観点が指摘）。ただし、どちらの観点も反証（refuted）にはしていません。2 段パスの形（h.config.cmd → h.save()）は、仕様書の深さ 2 のアクセスパス（AUTHGAP_BRIEF_v3.md:515、RECEIVER_DEPTH = 2）に収まるのに D35 (b) の修正が 1 段しか畳まないことによるもので、どこにも記録がありません（D35 の修正の未完）。R1-r4-10 については、意図した決定・限界の記録は見つかりませんでした（設計の観点）。review_plan §5 の O 番号・K1〜K7・設計上の決定には、どちらも該当しません。関連する別の所見として、R1-r1-1（env_join の片側の属性鍵。経路が別）と R1-r3-11（別名の同一性）があります。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R1-r3-2 の設計の観点が medium にした理由は「3 形が D35 限界 1 と重なり、未記録なのは 2 段パスだけ」です。R1-r4-10 が low なのは「使い回しのまれな書き方」と「D1 では FS_WRITE が常に矛なので効かず、影響は D2 と、値で判定が分かれる slot に限られる」ためです。どちらも「D3 / D4 だけなら low」という旧文言によるものではありません。
- **推奨の理由**: 代表の重大度は high で、向きは最も重い「MODEL が定数の OP/resolved に化ける」誤 clear です。一般に正しい直し方（案 A と、条件つきの鍵の削除）があり、試作で壊れる正しいケースは見つからず、較正 14 木の増減も 0 でした。凍結した語彙の追加は要りません。設計の観点は反証しておらず、D35 限界 1 との重なりは一部にとどまります（2 段パスは未記録）。R1-r4-10 は low ですが根本原因が同じで、案 A を入れると素朴な削除の反例（cx10b）も避けられるので、同じ変更でまとめて直すのが自然です。ただし直した後も、分岐の片側だけでの束縛し直しとコンテナ経由の別名は限界として記録してください。学生がより小さな変更を選ぶなら、R1-r4-10 を記録に回して案 A だけを入れることもできます（その場合も案 B は使わないこと）。解析器（authgap/）を変えるので指紋が変わり、再凍結と、CONTRADICTION が増える向きの敵対的レビューが必要です。
- **所見**:
  - R1-r3-2: 代表。属性への書き込みが path 鍵にしか載らないため、引数・キーワード引数・戻り値・2 段パスの 4 形で被呼び出しが既定値 'ls'（OP/resolved）を読み、D1 の矛が不に落ちる。重大度は探索 high / 設計 medium / 一般性 high。3 形は D35 限界 1 と根本原因が同じで、2 段パスは未記録。直し方は案 A（別名とほかの Obj の fields 1 段も同一性で差し替える条件つき）。案 B は誤警報を生むので採らない（ローカルのオブジェクトへの属性書き込み `c.cmd = cmd` は env の鍵 `c.cmd` にしか記録されず `Obj.fields` に載らないので、そのオブジェクトを**引数（位置 / キーワード）として渡す / 関数から返す）
  - R1-r4-10: 同じ原因の逆向きの表れ（鍵が残りすぎる）。名前を束縛し直しても古い name.* の鍵が消えず、新しい Obj の値を古い定数で上書きして D2 の矛が不に落ちる。3 観点とも low。素朴な鍵の削除は cx10b（s = s or Store(...) など）で新しい誤 clear を作るので、R1-r3-2 の案 A と組み合わせるか、右辺が新しい割り当てのときだけ消す。分岐の片側だけで束縛し直す形は直らないので、限界として記録する（名前を束縛し直しても古い属性パスの鍵（`s.path`）が env に残る: `_bind`（Name）は `env[name]` だけを置き換え `name.*` を消さず、`_ev_Attribute` は env の鍵を `Obj.f）

### U06 組込みのコンテナ操作の穴（_builtin_value_op）（段階 B・重大度 高・推奨 一部直す）

解析器は、よく使う Python の組込み（`dict.get` / `pop` / `setdefault` / `getattr`、`enumerate` / `zip` / `sorted` / `reversed` / `.items()` / `.values()`、`set()` / `list()` / `dict()` / `deque()`）の意味を知りません。知らない呼び出しとして扱うので、値は「確度が不明（opaque）」になります。O33 では「モデルが選べる」と言えるのは MODEL かつ resolved の値だけです。そのため `arguments["url"]` なら 矛 になる同じプログラムが、`arguments.get("url")` や `for i, c in enumerate(cmds)` と書くだけで 不 に落ちます。どれも見逃しの向き（誤 clear）です。特に `setdefault` の後の読み出しは、MODEL の値を運用者の定数（OP/resolved）と取り違えます。`set()` + `add` は MODEL そのものが消えます。

- **宣言**: D1 / D2 / D3　**向き**: 誤 clear　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_builtin_value_op` と組込み名の解決がよく使う組込みを持たず、未解決の呼び出し（D44）として MODEL/opaque（または OP/opaque）の Unknown を返す: `dict.get` / `pop` / `setdefault` / `getattr`、要素をそのまま渡す `enumerate` / `zip` / `sorted` / `reversed` / `dict.items` / `values`、コンテナの構築子 `set()` / `list()` / `dict()` / `deque()`（形が付かないので後の `add` / `append` も container 条件に当たらない）。O33（選べる = MODEL かつ resolved）の下で、同じ意味のプログラムの判定が書き方で 矛 ↔ 不 に変わる。
- **コードの場所**: authgap/val/engine.py:1149-1205 _builtin_value_op, authgap/val/engine.py:861-885 _ev_Call の未解決呼び出し → opaque(unresolved), authgap/catalog/transfers.py:273-284 組込み名の表
- **重大度の根拠**: 代表は R1d-r6-2。3 意見は 高 / 高 / 中 で、中央値は high。`arguments.get(...)` は低レベル MCP ハンドラの主流の書き方で、検証役（設計）の数えでは次のとおり。corpus の `.call_tool()` を含む 196 ファイルで `arguments.get(` は 2,135、`arguments[` は 570。`arguments` を読む 43 木のうち 39 木が `.get` を使う。これらの木では D1 / D2 / D3 の 3-a の行（SPAWN の argv0 / shell、書き出し先、SQL、NET の宛先）が系統的に 矛 → 不 になる。一般性の検証役は medium とした。理由は v2 run20 への効きが 0 行であること（低レベルのユニットは 2,231 中 6、矛盾の注記 0）。ただし D61 の方針で、検証データ（v2）の件数には合わせない。他の 3 件は 3 意見とも medium。件数の上限は、反復の組込み 82 木 6,405 箇所、pop / setdefault 62 木 1,608 箇所、`set()` + add 254 箇所 / 43 木。どれも到達性と MODEL の有無を見ていない上限で、真の件数は未測定。setdefault は MODEL を OP/resolved の定数に潰すので、§2.6「clean に潰さない」に反する。1 件でも重い向きである。旧文言「D3 / D4 だけなら low」で下がった形跡は無い（old_wording_downgrade 参照）。
- **直し方（一般に正しいか: 条件つきである）**: 組込みの意味（Python 仕様で木に依らない）で値を返すように _builtin_value_op / _ev_Call を拡張する。ただし素案のままでは新しい誤 clear と誤警報を作るので、検証役が見つけた次の守りをすべて付ける。

【守り A: 木内の同名メソッドより先に取らない】
- 素案は `_ev_Call` の (0) で木内解決（(4) `_resolve_in_tree`）より先に横取りするが、これは誤り。
- 反例は受け手を束縛し直す形。`self.store = {}` を connect() で木内クラスに束縛し直す（ce_get_intree1 / ce_get_intree2 / get_shadow の DiskCache）、`global CLIENT` を束縛し直す、`self.q = []` / `self.p = {}` を start() で TaskQueue / Prefs に束縛し直す（ce10a_intree_pop）、`self.cmds = {}` を Registry() に束縛し直す（ce7d_values_obj）。
- 素案を当てると、正しい 矛（D1 fs_write、D3 net_external_host）と logger 行が消える。値の形は型の証明ではない（D61 G2 取り消しと同じ誤り）。
- 正しい形: 木内に同名の定義が無いとき（`index.lookup_function(attr)` がテストを除いて空。D57 と同じ除外）だけ、D44 の fallback の直前でモデル化する。候補があるなら降下の結果と join する形でもよい。
- 効く範囲を広げるなら、値に「型の証明」を持たせる。付けるのは入口の種と、同じ流れで評価した dict / list 表示だけ。`_self_fields` のフィールドと `_module_value` のモジュール名には付けない。

【守り B: 名前で呼ぶ組込み（enumerate / zip / sorted / reversed / getattr / list / set / dict / tuple / deque）は、本当に組込みに束縛されているときだけ】
- 次の 4 条件をすべて満たすこと（D61 G3 の条件 3 と同じ判定）。
  - `scope.local_bindings` に無い
  - `scope.lookup(name)` が None
  - 読む側モジュールの `_module_assignments` / `_module_writes` に無く、`*` import も無い
  - 木のどこにも `builtins.<name> =` / `setattr(builtins, ...)` / `__builtins__` への書き込みが無い（`_attr_stores` と同じ走査を足す。`import builtins` の別名も追う）
- 反例は 2 つ。ce7a_shadow（同じモジュールの `def enumerate`、`from .compat import zip`、`sorted = quiet_sorted`、局所の `reversed = ...`）と、ce3_builtins_rebind（`builtins.set = MySet`）。素案だと誤警報になり、効果行が消える。
- 閉包（囲む関数での `set = X`）が捕まるかは設計の観点が疑っている。実装の前に反例テストで確かめる。

【守り C: `dict.get` は定数キーだけ】
- 非定数キーは fallback のまま。
- 定数キーの場合の値:
  - entries にある: 項目 ⊔ 既定値
  - entries に無く tail がある: tail ⊔ 既定値。root は `arguments["k"]` に精緻化する（D6）
  - entries があって tail が無く、キーも無い: (None ⊔ 既定値) に opaque(unresolved) を合流する
  - entries も tail も無い（`arguments = arguments or {}` の後）: `_element_of` ⊔ 既定値
- 反例 ce_get_missing の cfg_setdefault_get: 素案（_element_of で既存項目を resolved で読む）だと 不 → 内 の新しい誤 clear になる。

【守り D: 実引数に `ast.Starred` があれば fallback のまま】
- `zip(*rows)` は転置である。素案は `zip(rows)` として扱い、誤警報を出す（ce7c_zip_star）。

【守り E: 辞書の反復はキー】
- 対象: `sorted(d)` / `list(d)` / `reversed(d)` / `enumerate(d)` / `zip(d, …)` / `d.keys()`。定数キーの Map なら OP/resolved の Atom、tail があれば tail の主体・確度で Unknown。値の join を返してはいけない（ce7b_dict_keys。素案は誤警報）。
- 既存の素の `for k in d` も値を束縛している（既存の誤警報、所見の範囲外）。同時に直すか、別件として記録する。

【各操作の値】
- enumerate: `Seq((), tail=Seq((OP Atom, elem)))`
- zip: 要素の組
- sorted / reversed: 要素そのまま（`key=` は要素を変えない）
- `.values()` は `_element_of`、`.items()` は (キー, 値)
- pop:
  - Seq / Argv の `pop(i)`: i が定数で tail が無ければ `elems[i]`、それ以外は `_element_of`。要素は受け手から除かなくてよい
  - Map の `pop(k[, d])`: 守り C と同じ扱い
- `setdefault(k, v)`: 項目を prev ⊔ v で書き、その値を返す
- `getattr(o, "名前"[, d])`: `_ev_Attribute` と同じ field ⊔ d。非定数名なら全 field の join に opaque(dynamic) を合流する

【安全網（resolved → opaque の向きなので健全）】
- 局所の容器形の受け手に未解決のメソッド呼び出しがあり、MODEL の実引数があれば、`_append_tail` で受け手に opaque で書き戻す。
- `_ev_Subscript` で無いキーを読むときは、`_element_of` に opaque(unresolved) を合流する。
- これで ce10b の `missing_key_read` / `unknown_mutator_then_read`（OP/resolved Atom=True の誤定数）も消える。

【R1-r5-3 の狭い直し方】
- 構築子に形を付ける直し方は入れない（D61 G2 取り消しの範囲）。
- 代わりに、`add` / `update` の container 条件を外す。形の分からない受け手でも `append` と同じく「書き込みは反映し、呼び出しは通常の解決に回す」にする。型を主張せずに MODEL と root が残る（OP/opaque が MODEL/opaque の 不 に変わる）。

【手順（CLAUDE.md）】
1. 正例（argsget、iter_consumers の 6、builtin_pop の 3 + getattr_const、builtin_ctors）と、上の反例すべてを tests に先に固定する。
2. 実装する。
3. diff_effects.py で較正対 A9 / A18（と A1 / A2）を突き合わせる。
4. compare_scans.py で run20 → 新 run の消えた行 / 消えた CONTRADICTION を 1 件ずつ見る。
5. 解決率を上げる変更なので、「resolved にしてよい根拠」を 1 件ずつ崩す敵対的レビューを通す。

参考: guarded 版 `.get` の模擬（メモリ上の差し替え）では、v2 の 8 木と較正対 A1 / A2 / A9 / A18 の両側で、消えた効果 0・矛盾の注記の変化 0 だった（検証役の測定）。

【凍結との関係】
authgap/ を変えるので指紋が変わる。再凍結（freeze_analyzer.py）と、preregistration.md への逸脱の記録が要る（D61 の最終凍結の文言）。
- **記録済みの限界・決定との重なり**: - D61 G2 の取り消しと O41「末尾名だけの解決で、組込み型の値のメソッドを木の中の同名メソッドに結ぶ」は記録済みの限界で、review_plan §5 は設計上の決定としている。
  - R1-r5-3 の直し方（構築子 `set()` / `list()` / `dict()` に空リテラルと同じ形を付ける）は、G2 の実装（672f0f0 の `_builtin_container_shape`）とほぼ同じ。94c40b4 で取り消されたもので、tests/test_fix_d61.py の test_g2_withdrawn_effect_is_kept / with_shadowed_list が固定している。
  - このため設計の観点は R1-r5-3 を反証（refuted=true、fix_is_general=false）した。
  - 一般性の観点は、builtins の書き換えを走査する守りを足せば一般に正しいとして反証しなかった。2 観点で割れている。
- O33（選べる = MODEL かつ resolved）、D17 の opaque(unresolved) 合流、§9.3 の「不明への移動は誤 clear ではない」は設計上の決定である。この単位はこれらを争わない。「どの組込みを opaque に回すか」は決めた記録が無い、と 3 件の設計の観点が判定した（D44 は fallback の主体の規則にすぎない）。
  - 前例は逆向きで、D17 RES[7]（append 等）と D35 (e)（encode / decode）は組込みの取りこぼしを欠陥として直した。
  - R1-r3-7 の設計の観点は、Def 4 の字義では仕様どおりと読める余地があり、限界として記録する選択肢も大きいと付記している。
- Def 4 / 仕様 241 行はディスパッチ鍵として「subscript / `.get` / `getattr`」を既に語彙に持ち、D6 は添字で root を精緻化すると決めている。`.get` が roots=arguments に潰れる今の挙動は D6 の意図にも反する（R1d-r6-2 の設計の観点）。
- 範囲外の関連:
  - 木内に `def get(` があると O41 の経路に入る。低レベルで `.get` を使う 39 木中 15 木、v2 では 87 木中 29 木（見積もり）。守りつきの直し方はここを変えない。
  - 素の `for k in d` が値を束縛する既存の誤警報。
  - R4-r2-3（`str()` 等の恒等変換）は同じ「組込みの語彙」の穴で、TRANSFER 側の別単位。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。
- R1d-r6-2 は D62 の後の文言で検証した（Opus、§7.7）。一般性の観点の medium は、v2 run20 での効き 0 行と、直し方の届く範囲を理由にしている。「D3 / D4 だけ」は理由にしていない。設計の観点は、D1 / D2 / D3 の 3-a 行に効くと明記して high とした。
- R1-r3-7 / R1-r3-10 / R1-r5-3 は旧文言で検証したが、影響は D1+D2 で、3 意見とも medium。判定の本文に「D3 / D4 だけ」を理由にした記述は無い（grep で 0 件）。
- ただし .get の直し方は D3（NET の宛先）にも効く。R1-r3-10 / R1-r3-7 の同じ形も、NET の宛先・メソッドなどの D3 の 3-a 行に効きうる。この点はどの検証役も数えていない（未測定）。
- **推奨の理由**: 直すもの: R1d-r6-2 / R1-r3-10 / R1-r3-7 の 3 件。条件をすべて満たす。
- 代表の重大度が high / medium
- 設計・一般性の両観点が反証せず、どちらも fix_is_general=true
- 凍結した語彙（sink / 入口 / weak 理由）の追加が要らない（_builtin_value_op / TRANSFER は凍結の対象外）
- 素案の反例を避ける守り（木内候補の有無、組込み名の束縛の確認、定数キー、Starred、辞書の反復はキー）を検証役が具体的に示している
- guarded 版は v2 と較正対で消えた効果 0 を確かめている

記録に回すもの: R1-r5-3 の構築子に形を付ける直し方。
- 設計の観点が D61 G2 の取り消し（記録済みの限界 O41、review_plan §5 の設計上の決定）の呼び直しと判定した。
- 閉包・`builtins.set =` を除けるかに争いがある。
- R1-r5-3 のうち `add` / `update` の container 条件を外す狭い直し方は、opaque の向きで型を主張しない。G2 に触れないので、直す側に入れてよい（O42 候補）。

`list(xs)` / `set(xs)` のような引数つきの構築子を R1-r3-7 に含めるかは、G2 と同じ注意が要る。守り A / B が揃う場合に限る。

規模は L（守りの設計と反例テストが多い）で、opaque → resolved の向きなので敵対的レビューが必須。再凍結と逸脱の記録も要る。工数が見合わないと学生が判断するなら、R1-r3-7 は設計の観点の付記どおり O42 に「内容不変の組込み反復」として記録する選択肢がある。R1d-r6-2（high）と R1-r3-10 の setdefault（resolved の誤定数）を優先する。
- **所見**:
  - R1d-r6-2: 代表（high、3 意見は 高/高/中）。`dict.get` の未モデル化で、低レベル MCP の標準形 `arguments.get(...)` の D1/D2/D3 の 3-a 行が 矛→不 になる。守り A（木内候補の有無）と守り C（定数キー・キーの有無の場合分け・D6 の root 精緻化）をつけて直す。（`dict.get(k[, d])` が `_builtin_value_op` に無く未解決呼び出し（D44）として MODEL/opaque(unresolved) になるため、低レベル MCP の標準形 `arguments.get(）
  - R1-r3-10: 同じ原因の別の表れ（`pop` / `setdefault` / `getattr`）。medium×3。setdefault は OP/resolved の誤定数を作る最も重い向き。守り A・B と、未解決の変更メソッドの書き戻しと無いキー読み出しの opaque 合流という安全網をつけて直す。（`_builtin_value_op` に無い組込みの読み書き: `parts.pop(0)` / `opts.pop("cmd")` は MODEL/opaque（矛 → 不）、`opts.setdefault("cmd", cmd)` ）
  - R1-r3-7: 同じ原因の別の表れ（要素を変えない反復の組込み enumerate/zip/sorted/reversed/.items/.values）。medium×3。守り A・B・D・E（Starred は fallback、辞書の反復はキー）をつけて直す。設計の観点は、限界として記録する余地も大きいと付記している。（要素をそのまま渡す組込みの反復（`enumerate` / `zip` / `sorted` / `reversed` / `dict.items` / `dict.values`）が未解決の呼び出し（D44）として扱われループ変数が MO）
  - R1-r5-3: 設計の観点で反証済み（D61 G2 の取り消し・O41 の呼び直し）。一般性の観点は守りつきで可とし、2 観点で割れている。構築子に形を付ける部分は限界として記録する。`add` / `update` の container 条件を外す狭い直し方（MODEL/opaque に留まり、型を主張しない）は直す側に含められる。（組込みのコンテナ構築子 `set()` / `list()` / `dict()` / `collections.deque()` が未解決の呼び出し（OP/opaque の Unknown）になるため、その後の `parts.add(cm）

### U09 モジュール・クラス水準の値の読み（_module_value）（段階 B・重大度 高・推奨 直す）

解析器が「ファイルの一番外側（モジュール直下）で決めた名前の値」を読めるのは、`NAME = 値` と書いて別のファイルから `from m import NAME` で持ってくる形だけです。同じ値を `config.ROOT`（モジュールを丸ごと import して属性で読む）、`pkg/__init__.py` で再公開した名前、`A, B = ...` のタプル代入、関数の中の `global` で後から入れた接続、`class Settings: ROOT = ...` のクラス属性の形で読むと「分からない（opaque）」になります。その結果、定数の SQL・パス・mode が読めずに「矛盾」が「不明」に下がり、モジュールやクラスに置いたクライアント・DB 接続は型が分からなくなって NET / DB の効果行が丸ごと消えます。どれも「本当は矛盾があるのに出ない」向き（誤 clear）の誤りで、書き方を変えただけで結果が変わります。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: モジュール / クラスに束縛された名前の値を読む `_module_value` / `_module_assignments` が、同じモジュール直下の単純代入 `NAME = expr` を `from m import NAME` の形でしか引かない: モジュール別名の属性 `config.ROOT` / `cfg.X`（`_ev_Attribute` はモジュール表を引かない）、`pkg/__init__.py` の再公開（`_follow_reexport` は関数の pin にしか使わない）、タプル代入 `A, B = ...`、関数内の `global` 再束縛（候補にせず、被呼び出しの global 書き込みも呼び出し側に戻さない）、クラス属性 `Cls.ATTR`（ClassDef を見ない）がどれも opaque(unresolved) になり、定数の SQL / パス / mode が読めず、モジュール水準のクライアント / 接続は受け手型を失って NET / DB 行が消える。
- **コードの場所**: authgap/val/engine.py:1207-1272 _module_value, authgap/val/engine.py:2268-2288 _module_assignments, authgap/val/engine.py:509-553 _ev_Attribute の fallback, authgap/val/engine.py:1717-1754 _follow_reexport, authgap/val/engine.py:1353-1399 _class_body_defaults, authgap/val/engine.py:1030-1107 _descend_env（global の書き戻し）
- **重大度の根拠**: 代表は R1-r4-1 で、探索・設計・一般性の 3 意見がそろって high。`config.X` / `settings.X` はモジュールを import して属性で読む書き方で、設定モジュールでは from-import と並ぶ主な 2 形の片方。定数は矛から不に下がり、クライアント・接続は NET / DB 行が 1 本も出ない（数え落とし）。探索役が数えた v2 での構文上の上限は、テスト dir を除く 99 木で 2,471 箇所 / 22 木（うち str 定数 403 / 15 木、呼び出しで作った値 198 / 9 木）。到達性と判定 slot に届く件数は未測定。ほかの所見: R4-r2-7 は 3 意見とも medium（設計役は「high 寄りの medium」とした。消失は黙って起き、G5 の列にも出ない。DB の受け手だけは db_unresolved に跡が残る）。構文上の候補は 101 箇所 / 13 木で、狭めた数え直しは走らせた途中のまま結果が無いので未測定。R1-r3-9 は 3 意見とも medium（61 木で 17,002 箇所。classmethod 呼び出しも数えた緩い上限で、slot に届く件数は未測定）。R1-r4-11 は探索が low、設計と一般性が medium で、中央値は medium。R1-r4-13 は 3 意見とも low（まれな書き方）。5 件とも D1 / D2 に効くので、D62 の文言を変えたことによる重大度の見直しは無い。
- **直し方（一般に正しいか: 条件つきである）**: 共通の方針。`_module_value` の後半を `(module, attr)` で読む内部関数に分ける。D17 改訂 2〜5 の検査（writes / rebound / `_tree_attr_writes` / `_opaque_deep` / reader_rebinds）はどの読み方にもそのまま掛ける。コンテナとオブジェクトは今までどおり `_opaque_deep` にし、型と主体は保って確度だけを opaque にする。進め方は「規則をコミット → 正例と反例のテスト → 実装 → diff_effects / compare_scans で消えた行と増えた行を 1 件ずつ見る」の順。解決率を上げる変更なので、CLAUDE.md の敵対的レビューを通す。凍結後の変更なので preregistration に逸脱として書き、指紋を取り直す。

(1) モジュール別名の属性 `config.X`（R1-r4-1）。`_ev_Attribute` の汎用の fallback の前に、次の条件をすべて満たすときだけ別名先のモジュール直下の値を返す。(i) 別名の先頭が env に無く、`scope.local_bindings` にも無い。(ii) 読む側のモジュール直下で、その名前の束縛がちょうど 1 つの Import / ImportFrom である（`_module_bindings`、G3 の条件 3 と同じ。関数内の import は local_imports で許す）。(iii) `resolve_import_module` で木内のモジュールに解け、その親パッケージの `__init__.py` が同じ葉の名前を代入・書き換えしていない。(iv) 属性の読みは遅延束縛なので、木のどこかに `setattr(alias, <非定数>, …)` / `vars(alias)` / `alias.__dict__` があるモジュールは "*" として全束縛を opaque にする。(v) `_module_value(scope,'config')` がモジュール名に None を返す今の振る舞いは保つ。素朴な直し方で壊れた反例は 3 つ（検証役 p1）。f1_shadow: `__init__.py` で `config = _load()` と束縛し、`pkg/config.py` も在る。f1_dynattr: `setattr(config, key, value)` / `vars(config)[key] = value`。f1_condimport: `try: from . import config` の予備に `except ImportError: config = SimpleNamespace(...)`。どれも MODE="a" が resolved になり、誤 clear の「内」になった。条件を足した版 p1g では 8 ユニットが期待どおりになり、反例 4 形（f1_local を含む）は opaque のまま、pytest は対照と同じ結果だった。残る限界（from-import 形と共通で、D17 改訂 4 に記録済み）: `setattr(sys.modules[...])`、`importlib.reload`、`mock.patch`。

(2) 関数内の `global` 束縛（R4-r2-7）。(a) 同じモジュールの関数（入れ子・メソッドを含む）で `global attr` を宣言している関数の `attr = <expr>` の右辺を候補に加える。右辺は、その関数のスコープで評価する（モジュールのスコープで評価すると、仮引数名が同名のモジュール水準の名前に化ける）。(b) 候補は型を保つ join で合わせる。素の value_join で `Obj ⊔ Unknown` を `Unknown` に倒すと、今は正しく D1 矛が出ている `Y = sqlite3.connect(); def swap(): global Y; Y = external_factory()` の行が消える（反例 r7_unknown_join の purge_y。同じ join を直下で書いた purge_w は今も行 0 で、これは同じ族の既存の誤 clear）。classes を残して、確度に opaque を合わせる。これは `_module_value` の中だけで済み、`_shape_join` 全体は変えなくてよい。(c) 被呼び出しの書き込みを呼び出し側の env に書き戻す直し方は任意。入れるなら、呼び出し側で同名が local_bindings にあり global 宣言が無いときは書き戻さない（反例 r7_local_shadow。`ast.Global` は別に見る）。流れに沿って精度を上げるのはこちらだけなので、敵対的レビューもここに集める。(a)(b) だけで期待の出力（DB 行と D1 db_model_sql、受け手は opaque）が出る。確かめること: 型が 2 つ以上の Obj になった受け手の分割降下（D35 (d) の再発）、`global X; X = None` の後始末関数との合流。期待の細部の訂正: 行の resolution は resolved のままで、UNKNOWN は付かない。

(3) `__init__.py` の再公開（R1-r4-11）。`_module_assignments` が空のとき、G3 と同じ健全性の条件（束縛がちょうど 1 つ、直下の from-import、level で解く、関数内で書き換えない）で再公開元をたどる。`_follow_reexport` は終端が `_visible_defs`（関数）なので、値に使うには「再公開元に `_module_assignments` がある」を終端にする変種が要る。そのまま呼ぶと None が返る。rebound の判定は、再公開するモジュールと元のモジュールの両方に掛ける。反例テストに cx11（`__init__.py` で `global ROOT; ROOT = r`）と、try/except の予備 import を入れる。

(4) タプル代入（R1-r4-13）。対象が Tuple / List で、右辺も同じ長さの Tuple / List のときだけ、位置の対応で右辺を返す。どちらかに Starred があれば読まない。入れ子は再帰で対応を取る。単純代入と同じ再束縛の検査を掛ける。今の実装は `SQL_A, SQL_B = SQL_B, SQL_A`（swapped）や、単純代入の後のタプル代入（plain_then_tuple）で、先の定数を resolved と決め打ちしている（今ある誤 clear）。直すと opaque(recursion) か join になり、正しい向きに移る。壊れる形は見つからなかった。

(5) クラス属性 `Cls.ATTR`（R1-r3-9）。先に規則を決める（学生の判断）。A: モジュール定数と同じ扱い（不変の値で、再束縛が無ければ resolved）。B: D17 改訂 3 の「オブジェクト」として常に opaque（型と主体は保つ）。B でも受け手の型は付くので、NET 行が消える問題は直る。実装は `_ev_Attribute` の fallback の前に置き、名前が env と local_bindings に無く、木内クラスに `get_class(strict=True)` で解け、Cls 自体が再束縛されないときだけ `_class_body_defaults` の field を返す。再束縛の走査は fix_sketch より広くする。`Cls.ATTR =` / `del` / `setattr(Cls, ...)` に加え、メソッド内の `cls.ATTR =` / `type(self).ATTR =` / `self.__class__.ATTR =` / `setattr(cls, ...)`、別名（`C = Cfg; C.MODE = v`）、非定数の setattr / vars / `__dict__`（そのクラスは "*"）も見る。簡単に済ませるなら「self. 以外の受け手への同名 ATTR の store が木のどこかにあれば opaque」でよい。反例 ce9a_cls_store では、クラス名だけを見る guard だと MODE="r" が resolved になり、FS_WRITE 行と D2 矛が消えた。外部の基底を持つクラス（Enum メンバー、pydantic BaseSettings、Django）は opaque のままにする。StrEnum は可。
- **記録済みの限界・決定との重なり**: 設計の観点で反証された所見は無い（5 件とも refuted=false）。関わる記録は次のとおり。D17 改訂 2〜5 は、モジュール水準で再束縛される名前は確度を opaque にし、コンテナ / オブジェクトは _opaque_deep にすると決めた。これは直すときの条件になるが、別名の属性・再公開・タプル・クラス属性・global 側の候補を「読まない」と決めた記録は無い。D17 の直す表と Def 4（木内で解決できる名前を opaque にしない）は、むしろ読む向きの根拠である。D61 G3 は再公開を名前一般について決めたのに、実装は関数の pin にしか当てていない。R1-r4-11 はその値の版で、クラス版の R1-r2-5 は直す場所が別。D35 (a) の `Obj ⊔ None = Obj` は、R4-r2-7 と同じ型の問題を欠陥として直した前例。O41 の「関数が返すモジュール」は動的に得たモジュールの話で、静的な import の別名は含まない。K1〜K7 と review_plan §5 の設計上の決定のどれにも当たらない（K2 / K3 は callable の pin の別経路）。D17 改訂 4 に記録済みの限界（setattr(sys.modules)・reload・mock.patch）は直した後も残る。D61 の最終凍結の後の変更なので、直すなら preregistration に逸脱として書き、指紋を取り直す。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。5 件とも D1 / D2 に効き、D3 / D4 だけに効く所見は無い。検証役の理由にも旧文言は出てこない。R1-r4-11 は探索役の low を設計役・一般性役が medium に上げている。
- **推奨の理由**: 代表の R1-r4-1 は 3 意見とも high。5 件とも設計の観点で反証されず、一般性の観点で条件つきの一般的な直し方が示されている（R1-r4-1 は検証役が条件つきの版 p1g を実装して反例を避けられることを確かめた）。凍結した語彙にも触れない。誤りの向きはすべて誤 clear で、設定モジュール・グローバル接続・名前空間クラスは新しいデータでも出る常套の書き方なので、D61 の「検証データに合わせない、一般に正しい直し方」に当てはまる。優先順は R1-r4-1 → R4-r2-7 → R1-r4-11 → R1-r3-9 → R1-r4-13。R1-r4-13 は low でまれだが、同じ関数の小さな直しで、今ある resolved の誤 clear（swap の形）も一緒に消えるので、同じ変更に入れてよい。R1-r3-9 は先に規則 A / B を学生が決める必要がある。決めきれないなら B（型だけ付けて確度は opaque。受け手の行が消える問題はこれで直る）で入れ、定数を resolved にする部分は限界として記録する、という分け方もできる。解決率を上げる変更なので、反例テストを先に置き、敵対的レビューと compare_scans を通すことが条件。
- **所見**:
  - R1-r4-1: 代表（high×3）。モジュール別名の属性 config.X を _ev_Attribute がモジュール表に引かない。定数は矛から不に、mode は D2 の誤警報に、クライアント / 接続は NET / DB 行が消える。素朴な直し方の反例 3 形と、それを避ける条件 (i)〜(v) は検証役 p1g で確認済み。（モジュール別名経由の属性読み出し `config.ROOT` / `cfg.SQL_PURGE` / `config.client`（`from . import config` / `import pkg.config as cfg`）が）
  - R4-r2-7: 同じ原因の別の表れ（medium×3）。`_conn = None` の後に関数内の `global _conn; _conn = connect()` で束縛する形。候補が None だけになり受け手の型が消えて、行が黙って消える。直すときは、型を保つ join と、右辺をその関数のスコープで評価することが必要（反例 r7_unknown_join / r7_local_shadow）。（モジュール水準の名前を関数内の `global` 再束縛で初期化する形（`_conn = None` + `init_db(): global _conn; _conn = sqlite3.connect(...)`）で、`_module_）
  - R1-r4-11: 同じ原因の別の表れ（low / medium / medium で中央値 medium）。pkg/__init__.py で再公開した値を _module_value がたどらない（G3 が関数にしか当たっていない、の値の版）。_follow_reexport の終端を値向けに変えた変種が要る。（値（定数・モジュール水準のインスタンス）の再公開 `pkg/__init__.py: from .config import ROOT, client` を経た `from pkg import ROOT, client` が解けない: `）
  - R1-r3-9: 同じ原因の別の表れ（medium×3）。クラス属性 Cls.ATTR を読まない。定数を resolved にするか（規則 A / B）は学生が先に決める。guard は cls. / type(self). / 別名 / setattr(cls) / 外部基底まで広げる（反例 ce9a_cls_store）。（クラス名経由の属性読み出し `Cls.ATTR`（`class Settings: ROOT = "/data"` の名前空間クラス、`class Clients: http = httpx.Client()`）が `_module_val）
  - R1-r4-13: 同じ原因の別の表れ（low×3、まれな書き方）。タプル代入を _module_assignments が読まない。単純代入と混ざる形では、今の実装が resolved の誤 clear を作る。直しは小さく、壊れる形は見つからなかった。（モジュール水準のタプル代入 `SQL_PURGE, SQL_COUNT = "DELETE FROM sessions", "SELECT ..."` を `_module_assignments` が読まない（`ast.Name` の対象）

### U12 受け手型によるメソッド解決（継承・同名クラス）（段階 B・重大度 高・推奨 一部直す）

`t = Tool(); t.save(...)` のように、変数の型（クラス）が分かっているときに呼ばれるメソッドを選ぶ処理に 3 つの穴がある。1 つ目: メソッドが親クラスから受け継いだもので、しかも木の中の無関係なクラスにも同じ名前のメソッドがあると、呼び先を 1 つに決められずに諦める。2 つ目: `super().m()` は直接の親しか見ないので、何も定義しない中間のクラスを挟むと呼び先が見つからない。3 つ目: 別のモジュールに同じ名前のクラスがあると、2 文で書いた呼び出しだけが諦めることになり、1 文で書くと降りる。どれも効果の行が消えるか MODEL が不明に落ちるので、あるはずの矛盾が「矛盾なし」や「不明」になる（見逃しの向き。誤警報は増えない）。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 受け手の型でメソッドを選ぶ経路がクラスを末尾名だけ（定義モジュール無し）で持ち、基底の家族を経路ごとに違う幅で辿る: `_resolve_in_tree` の型絞り込み（typed_classes）は受け手の自クラス名だけで `_class_family`（基底 3 段）を使わないので、継承したメソッドは木の別クラスに同名メソッドがあるだけで解決されず、`Obj.classes` にモジュールが無いので別モジュールの同名クラスがあると 2 文形 `r = Runner(); r.go()` は `[]`（1 文形は全候補へ降りる。D51 に反する）、`_super_callees` は直接の基底しか見ず中間クラスを挟む継承の `super().__init__` / `super().m()` が消える。
- **コードの場所**: authgap/val/engine.py:966-1008 _resolve_in_tree の typed_classes, authgap/val/engine.py:1557-1572 _class_family, authgap/val/engine.py:1456-1475 _super_callees, authgap/val/engine.py:1477-1495 _resolve_on_expression_receiver, authgap/ir.py:296-310 Obj.classes
- **重大度の根拠**: 代表は R1-r1-3 で、重大度は 3 意見（探索 high / 設計 high / 一般性 medium）の中央値の high。一般性の観点が medium にした理由は「G5 の列（解決できなかった木の中の呼び出しの数）に跡が残るので、黙った誤 clear ではない」で、D3 / D4 とは関係しない。継承は言語の仕組みそのもので、`save` / `run` / `execute` / `close` のような名前はどの木でもぶつかりやすい。BaseTool → ConcreteTool の継承は MCP サーバでよく見る構造。R1-r4-4 は 3 意見とも medium（何も定義しない中間クラスがあるときだけ起きる）。R1-r5-2 は中央値 medium（別モジュールの同名クラス・同名メソッド・2 文形・厳密な構築の 4 条件が重なるときだけ）。件数: R1-r1-3 は構文上の上限だけ数えてある。継承したメソッドと同じ名前のメソッドを家族の外のクラスも持つ (クラス, メソッド) の対は v3 で 4,051 対 / 34 木、v2 で 108,084 対 / 27 木（そのうち mcparmory__registry の vendored の塊が 93,039）。R1-r5-2 は v2 の 99 木で 423 組 / 25 木（到達性は見ていない上限。ly-ads-mcp-server の生成クライアントだけで 323 組）。ツールから届く数と run20 の G5（1,510 ユニット・16,047 呼び出し）のうちこの形がいくつかは未測定。R1-r4-4 の件数も未測定。影響は 3 件とも D1 + D2 で、D3 / D4 の旧文言は重大度に関係していない。
- **直し方（一般に正しいか: 条件つきである）**: 【R1-r1-3（継承したメソッド）】所見の fix_sketch どおり「`c.classname in _class_family(...)` で絞る」と、正しく動いている形が 2 つ壊れる（検証役が試作 AG_PATCH=3 で行の消失を確かめた）。反例 (a): Tool が Base.save を上書きする形（`super().save()` を呼ぶかどうかに関係なく）で、Tool.save と Base.save の 2 候補が残って `[]` になり、今出ている D1 の矛が消える。反例 (b): 2 型の受け手を型ごとに分けて降りる形（Local / Sandbox の write）で、基底 BaseOp.write も候補に残ると `set(by_class) == typed_classes` が崩れて、2 本とも行が消える。避ける条件（一般に正しい形）: 受け手の型ごとに MRO を近い順に歩く（自クラス → 基底を 1 段ずつ、`_class_family` と同じ 3 段まで）。最初にメソッドの定義が見つかった段で候補がちょうど 1 つならそれを採る。2 つ以上あるとき、または同じ名前のクラスが木に複数あるとき（`_class_name_unique` が偽）は今の規則に戻す（`[]` と G5）。外部の型は D61 G4 どおり家族に入れない。基底は `_base_classes` が import 表で厳密に解く（D17 改訂 2）。同じ MRO を `_resolve_on_expression_receiver`（`Cls().m()` の 1 文形）にも当てる。試作 AG_PATCH=m では inherit_collide が Base.save に降りて D1 の矛になり、上書き形・分割形・repo に固定してある RELATIVE_BASE の形は今と同じ出力だった。残る穴（`self.save = fn` のようなインスタンス属性による隠れ、クラス属性の書き換え）は自クラスのメソッドを解決するときにも同じくあるので、新しい種類の不健全さは増えない。
【R1-r4-4（super() の遡り）】fix_sketch の「幅優先・左から・最初に定義したクラスで止める」だと、所見の 2 形（中間クラス 1 段）と今正しい形（mixin を先に書く形 / base を先に書く形 / ダイヤモンド）は保てる。ただし多重継承の 2 段目以降で C3 とずれる。反例 NonDiamond(Left, Right)、Left(Deep)、Deep.run = os.system、Right.run = print では、C3 の順は NonDiamond, Left, Deep, Right なので正しい呼び先は Deep.run（矛）。幅優先だと同じ段の Right.run を先に採る（今と同じ誤 clear のまま）。深さ優先にするとダイヤモンドで Root.run を採って誤警報になる。もう 1 つ、`_base_classes` が外部の基底を黙って落とすので、ExtFirst(Ext, InTree)、Ext(subprocess.Popen) の `super().wait()` を InTree.wait に解いて誤警報を出す（1 段でも今起きている）。一般に正しい形（試作 p4c で確かめた）: 木の中のクラスについて C3 線形化で MRO を作る（`cd.bases` の順を保ち、外部の基底は葉の印として置く）。自クラスの次から順に歩き、先に外部クラスに当たったら unresolved にする（そこで m が定義されているかもしれないため）。木の中のクラスが m を定義していればそれを採る。深さは `_find_init` / `_class_family` と同じ 3 段にそろえる。p4c では所見の two_level_init / two_level_method が期待どおり（MODEL/resolved の矛）になり、mixin_first / base_first / diamond は今と同じ、non_diamond は Deep.run の矛に直り、ext_first の誤警報は消えた。pytest は対照と同じ（1 failed / 741 passed、落ちた 1 件は対照でも落ちている）。残る近似（今と同じで悪くはならない）: 本来 `super()` は `type(self)` の MRO で解くが、実装は実行中のメソッドを定義したクラス（`_class_stack[-1]`）の階層で解く。そのため協調的多重継承で兄弟クラスへ渡る形は追えない。ext_first のような誤警報が消えると compare_scans で「消えた行」として出るので、1 件ずつ確かめる。
【R1-r5-2（別モジュールの同名クラス）】直すなら次の形になる（大きさは L）: `_construct_in_tree`（と `_descend_env` の self）が作る Obj に定義モジュールを持たせる。`_resolve_in_tree` / `_resolve_on_expression_receiver` / `_class_family` / `_in_tree_method` の絞り込みを (module, classname) の組で行う。同時に `_shape_join` の classes の和、`_receiver_typed_key`、`_is_external_class` も見直す。モジュールを持たない Obj（注釈による型付け・外部型・合流したもの）は今までどおり末尾名で扱い、一致が取れなければ今までどおり `[]`（G5）。一般性の観点が見つけた ce2_dup_inherit（基底が別モジュールにあり、別モジュールに同名の Runner がある形）では、今の解析器が誤ったクラスへ resolved で降り、sink が 1 文形でも 2 文形でも黙って消える（G5 にも数えられない）。この直し方はその穴も塞ぐが、誤ったクラスへ降りていた行が消えるので、compare_scans で 1 件ずつ確かめる。設計の観点はこれを D35 の限界 2 の再発見として反証しているので、今回の推奨では直さない側に置く。1 文形と 2 文形の食い違い（D51 の by_name 降下と D35 (d) の非降下）は記録されていない。どちらに揃えるかは学生が決めることで、O42 の候補にする。2 文形を 1 文形に揃えて全候補へ by_name で降り、opaque の行を出す形なら D17 改訂 5 の規則に近い。ただし行が増える向きなので敵対的レビューが要る。
【共通】3 件とも opaque → resolved か行が増える向きなので、CLAUDE.md どおり「resolved にしてよい根拠」を崩しに行く敵対的レビュー、diff_effects.py、compare_scans.py（run20 と突き合わせ、消えた行・消えた CONTRADICTION を 1 件ずつ）を通す。authgap/ を変えるので再凍結（D59 の freeze_analyzer と preregistration の逸脱の記録）が要る。
- **記録済みの限界・決定との重なり**: R1-r5-2 は設計の観点で反証された（confidence 0.6）。理由は、根本原因（`Obj.classes` が末尾名でモジュールを持たない）が D35 の「残る既知の限界」2（docs/decisions.md:314-316）に記録済みであること。D35 (d) の敵対的レビュー d4 で、別モジュールの同名クラスへ降りるのをやめて opaque に留めると選んでおり、2 文形の「行なし + G5 の 1 件 + ユニット opaque(unresolved)」は D61 G5 どおりの出力で、tests/test_fix_d61.py:350-397 が固定している。所見の期待（resolved で降りる）は、Obj にモジュールを持たせた後でしか出てこない。一般性の観点は反証せず（情報を持っていたのに捨てた穴だとした）、判定は割れている。1 文形と 2 文形の食い違い（D51 の原則「1 文で書くか 2 文で書くかで結果が変わってはならない」への抵触）は未記録で、O42 の候補。また review_plan §5 は D35 の「残る既知の限界」を挙げていないので、再発見を防ぐにはそこに足すとよい。R1-r1-3 と R1-r4-4 は両観点とも反証されていない。D35 の限界 3（継承メソッドは 2 型受け手を分けて降りる対象から外す）は分割降下の話で、単一型の継承の解決や super() の深さには触れていない。関連する別件（根本原因が別）: R4-r2-5（`_self_fields` が基底の `__init__` を見ない）、R1-r2-6（`Base.__init__(self, …)` の明示形）。R1-r5-2 は第 5 回の所見で、review_plan §7.3 の「事前登録の手続きの外」の印がつく。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも影響は D1 + D2 で、検証役の notes に D3 / D4 を理由にした格下げは見当たらない。R1-r1-3 で一般性の観点が medium にしたのは「G5 の列に跡が残る」ことが理由。
- **推奨の理由**: R1-r1-3（high）と R1-r4-4（medium）は両観点とも反証されていない。どちらも Python の MRO から正解が決まり、v2 / v3 と関係なく一般に正しい直し方がある（型ごとに MRO を歩く、C3 線形化 + 外部基底で止める）。検証役が試作して、今正しい形を壊さないことを確かめている。語彙の追加も要らないので、fix の基準を満たす。直すときは、所見の素朴な直し方（家族で絞る / 幅優先）ではなく、検証役の条件つきの形にすること。R1-r5-2 は、設計の観点が D35 の限界 2 として記録済みと判定した。正しく直すには Obj にモジュールを持たせて、7 か所前後の末尾名の読み方を同時に見直す必要があり（L）、凍結の直前に入れるには範囲が広い。そのため限界として記録する側に置く（D35 の限界 2 の記述を「opaque のまま」から「単一型でも候補が割れると行が出ず G5 に数えるだけ、継承と重なると誤ったクラスへ降りうる」に正確にする）。1 文形と 2 文形の食い違いは O42 として学生の判断に回す。R1-r1-3 の直し方は `_class_name_unique` で守るので、R1-r5-2 を直さなくても単独で入れられる。
- **所見**:
  - R1-r1-3: 代表（high、D1 + D2、count_loss）。`_resolve_in_tree` の typed_classes が自クラス名だけで、基底の家族を使わない。直す側に置く。直し方は型ごとに MRO を近い順に歩くことで、家族で絞るだけでは上書き形と分割降下形が壊れる。（継承したメソッドの呼び出しが、木の別のクラスに同名メソッドがあるだけで解決されず効果が消える（`_resolve_in_tree` の `typed_classes` の絞り込みが受け手の自クラス名だけで、基底を含む家族 `_class_f）
  - R1-r4-4: 同じ根（継承の家族を経路ごとに違う幅で辿る）の別の表れ。`_super_callees` が直接の基底 1 段で止まる（medium、false_clean）。直す側に置く。直し方は C3 線形化 + 外部基底で止めることで、幅優先は多重継承の 2 段目でずれる。（`super().m(...)` の解決（`_super_callees`）が**直接の基底だけ**を見て止まる（`_find_init` / `_class_family` の「基底 3 段まで」と食い違う）ので、メソッドを定義しない中間）
  - R1-r5-2: 同じ根（クラスを末尾名だけで持つ）の別の表れ（medium、count_loss、第 5 回で手続きの外）。設計の観点で D35 の限界 2 の再発見として反証済み、一般性の観点は反証せず。限界として記録する側に置く。1 文形と 2 文形の食い違いは O42 の候補。（`Obj.classes` が末尾名だけ（モジュール無し）なので、木の中の別モジュールに同名クラスがあり同名メソッドを持つと、`r = Runner(cmd); r.go()` の 2 文形は `_resolve_in_tree` の型絞り）

### U13 実引数と仮引数の対応（* / **・self / cls）（段階 B・重大度 高・推奨 直す）

関数を呼ぶとき、解析器は「呼び出し側で渡した値」を「呼ばれた関数の引数」に対応づけます。この対応づけが素の位置引数・キーワード引数しか扱っていません。`f(**opts)` のように辞書を展開して渡す値は捨てられ、受け取る引数は「運用者が決めた、完全に分かった値」（OP / resolved）として扱われます。そのため、モデル由来のパスやコマンドが届いていても矛盾が出ず、実際より安全に見えます（誤 clear）。`*args` / `**kwargs` を受け取る側も値が入りません。また、メソッドの第 1 引数を「名前が self / cls かどうか」で見分けるので、`def run(this, p)` や、クラス名を通して呼ぶ `Base.__init__(self, cmd)` / `Base.run(self, line)` では実引数が 1 つずれるか、呼び出し先が解決されません。多くは誤 clear か効果行の数え落としですが、`sh(*["ls", user])` のように逆に誤警報になる形もあります。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 被呼び出しの仮引数を種付けする `_seed_params_raw` / `_static_params` が素の位置・キーワード実引数しか扱わない: `f(**d)` の `d` は評価も受け渡しもせず（`*args` / `**kwargs` の仮引数も種付けしない。`sink(**kw)` は slot が無く行が出ない）、self / cls のずらしを第 1 仮引数の名前で決めるので別の名前の第 1 仮引数で実引数が 1 つずれ（O31 の静的な枝刈りも誤る）、クラス経由の非束縛呼び出し `Base.m(self, x)` は第 1 実引数をインスタンスとして扱わない（同名候補が複数だと解決もしない）。
- **コードの場所**: authgap/val/engine.py:1812-1850 _seed_params_raw, authgap/val/engine.py:1944-1962 _static_params, authgap/val/engine.py:731 _ev_Call の keywords（kw.arg is None）, authgap/val/engine.py:1641-1669 クラス名経由の呼び出しの解決, authgap/effects.py:656 _materialise
- **重大度の根拠**: 代表は R1-r1-2 で、探索役・設計・一般性の 3 意見がすべて high。理由は、`**kwargs` の転送が wrapper の常套形であること（D58 が野外の memory-hub `**_forward(opts)` で既に見ている）。加えて、`**` を通る値は書き方によらずすべて落ち、MODEL が OP で確度 resolved（完全に解けたと主張する最悪の誤 clear）になるか、`sink(**kw)` では行そのものが消える。構文上の上限（vendored を含み、到達性は未測定）は、木内関数への `**` 呼び出しが 2,017 箇所 / 58 木（v2）と 1,465 / 55（v3）、`*args` / `**kwargs` を持つ def が 5,909 / 81 と 4,099 / 78。R1-r2-6 は medium（探索 medium / 設計 low / 一般性 medium の中央値）。設計役の low は母集団での頻度（v2 の `Cls.m(self, …)` が 6 木 15 箇所、うち `__init__` 5 木 11 箇所）によるもので、旧文言「D3 / D4 だけなら low」によるものではない。R1-r1-11 は 3 意見とも low（self / cls 以外の名前はまれ。件数は未測定）。影響は D1 / D2 で確認済み。D3 / D4 への影響（例: HTTP クライアントに `**kw` を渡す形）は探していないので未測定。
- **直し方（一般に正しいか: 条件つきである）**: 【A. `**` / `*` と `*args` / `**kwargs`（R1-r1-2）】検証役の試作 AG_PATCH=2 で確かめた直し方:
(1) `_ev_Call` で `kw.arg is None` の値を評価し、展開値として保持する。中の呼び出し（`write_file(**build(path, text))` の `build` など）が on_call に届くようになる。
(2) `**` の Map を仮引数の名前で束縛するのは、Map が resolved で、キーがすべて定数で、tail が無いときだけ。`opts.update(x)` と `_opaque_deep` は tail を足す。`_bind` の Subscript 代入（engine.py:470-473）はキーを置き換えず tail に積む。`del opts[k]` は `_exec_stmt` が無視するので、それがあった Map も未知として扱う。未知の展開値の場合、対応の無い仮引数は `Value(prin=展開値の主体の join, prov=opaque("unresolved"), Atom(formal), roots=展開値の root)` にする（D44 と同じ原理）。
(3) `*` の展開を要素に広げるのは、tail の無い既知の Seq だけ。それ以外は (2) の未知の展開と同じに扱う。今は `*` を 1 つの位置引数にしているので、`sh(*["ls", user])` が誤警報の矛になっている。直すとこれは不になる。
(4) `vararg` には余った位置引数を Seq として、`kwarg` には余ったキーワードを Map として種付けする。
(5) 既定値を入れるのは、展開値をすべて展開・束縛できた呼び出しだけ。それ以外は D58 規則 3 の保守側のまま。O31 の静的名は、`*` / `**` のある呼び出しでは今までどおり使わない。
(6) `sink(**kw)` は effects.py 側で Map を読む。定数キーは名前の slot へ、それ以外は主 slot へ要素の join を opaque で入れる。
守り（試作で不 / 内のまま残ることを確認した反例、trees/ce2_forms）: `sh(*["ls", user])` は 'ls' で不、`run_first("ls", user)` は 'ls' で不、`run_kw_cmd(**{"cmd": "ls", "extra": user})` は 'ls' で不、`run_kw_cmd(**build_opts(user))` は MODEL/opaque で `spawn_model_opaque` の不、`opts.update(overrides); write_file(**opts)` は path MODEL/opaque で不。今正しい判定を壊す反例は作れなかった（opaque は `_by_choice` で矛にならないので、変化は「誤った OP/resolved → MODEL/opaque」の向きに限られる）。
この単位では直らないもの: `callee_kwargs`（`subprocess.run(args=cmd, shell=True)`）は、直接書いても sink 表が位置引数しか見ないので行が出ない（D59 追記の Popen kw-only の既知の限界。sink の slot の論点で、R4 の領域）。`callee_varargs` の `list(parts)` は `list()` が TRANSFER に無いので `spawn_model_opaque` 止まり（別の論点）。

【B. クラス名を通した非束縛呼び出し `Cls.m(obj, …)`（R1-r2-6）】所見の fix_sketch は「名前が木内のクラスに解決できれば非束縛呼び出しとして扱う」だが、そのままでは誤 clear を作る。必要な条件（proto2 で確認）:
(i) `func.value` の Name が局所 / env に無い。モジュール直下でちょうど 1 回束縛される（ClassDef、または import 表 → `resolve_import_module` → `get_class(strict=True)` で解ける単一の from-import）。`_module_writes` に無い（G3 改訂 3 と同じ判定）。
(ii) `@staticmethod` はずらさず、`@classmethod` は cls ← 受け手（今の挙動）のままにする。
(iii) 第 1 位置引数があり、それが `ast.Starred` でないときだけ使う。無ければ今の経路に戻す。
(iv) 呼び出し先の `self.<f>` は、`access_path(node.args[0])` に対して `_write_back_self` で書き戻す（`super()` の分岐と同じ）。
(v) 候補は `lookup_function(f"{cls}.{attr}", module)` で、基底 3 段まで引く（`_find_init` と同じ）。
素朴な直し方が壊す反例:
- ce6_singleton: `class Runner: …` の後に `Runner = Runner()` とする形。`Runner.run(cmd)` は束縛呼び出しで、今は正しく矛。(i) が無いと self ← cmd になり不（誤 clear）。
- ce6_local_shadow: 局所変数がクラス名を隠す形。(i) が無いと同じく誤 clear になる。
- ce6_starred: `Base.run(*pair)`。今は Seq が MODEL を運ぶので矛（正しい）。(iii) が無い最初の試作 proto は `args[0]` の Seq を self に当て、不にした（誤 clear）。
- ce6_classmethod / ce6_staticmethod: ずらすと誤 clear になる。
proto2 の確認結果: 所見の 2 形と委譲形（ce6_mixin_delegate）、`Base.__init__(self, cmd=cmd)` は矛。誤警報の `Base.run_default(cmd)`（ce6_override）は不に直る。A9 / A18 の較正対は変化 0。tests の pytest は exit=0。
残る限界（悪化はしない）: `type(self).m(self)` / `self.__class__.m(…)`、`k = Base; k.run(self, x)`、descriptor 経由、`Base.__init__(self, *args, **kwargs)`（A に依存）、メソッド名が TRANSFER の語と同じ `Codec.encode(self, x)`、`run = staticmethod(_run)` のように FunctionDef が無い形。

【C. 第 1 仮引数の名前で受け手を決める（R1-r1-11）】offset=1 にするのは、FuncDef.classname があり、デコレータにもクラス体の再束縛（`name = staticmethod(name)` / `classmethod(...)`）にも staticmethod が無いときだけにする。classmethod の受け手はクラスとして扱う。クラス体で名前が再束縛されるなど判定できないときは、今の self / cls の名前による判定に戻す。`_seed_params_raw` と `_static_params` は同じ判定を共有する（D58 改訂の「割り当ての添字は同じにする」を保つ）。
反例 c11 static_by_assign（`def run(p, force=False)` の後にクラス体で `run = staticmethod(run)`）: 今は正しく矛。デコレータだけを見ると offset 1 になり、force の既定値 False で枝が刈られて誤 clear になる。

【共通の手順】A と B は解決を上げる変更を含む（`**` の中の呼び出しが on_call に届く、Map の名前束縛、`Base.__init__` の解決）。CLAUDE.md どおり「resolved にしてよい根拠」を崩す敵対的レビューを通す。そのうえで diff_effects（A9 / A18）と compare_scans で、消えた行と slot の変化（OP → MODEL、resolved → opaque）を 1 件ずつ確かめる。
- **記録済みの限界・決定との重なり**: - D58 改訂 (A)（docs/decisions.md:3205-3207）は、`**kwargs` / `*args` の扱いを run15 の誤 clear の原因として記述している。規則 3（:3232-3233）は「`*` / `**` のある呼び出しでは既定値を入れず『値の分からない』仮引数にする」と決めただけ。その実体 `_seed_from_annotation` は OP / resolved で、名前と中身が食い違う。`**` を捨てることを受け入れた決定・限界の記録は無い（O36 に置かれたのは (B)(C)(D) だけ。O41 にも無い）。`_descend_env` のコメント（engine.py:1054-1057）自身が欠陥と認めている。
- 設計の観点では 3 所見とも refuted=false で、§5 の既知の問題・K1〜K7・O38 / O41・D35 の残る限界のどれにも当たらない。D35 改訂が扱ったのは `super()` だけ。
- 隣接する別の単位（この単位には含めない）: R4-r2-1（INDIRECT 表の `to_thread` / `partial` / `Thread(kwargs=)` が 2 つ目以降の実引数を捨てる。D58 の (A')）と、R1-r4-4（`super()` の MRO が 1 段で止まる）。
- `callee_kwargs` の期待（kw-only の `subprocess.run(args=…)`）は D59 追記の既知の限界（Popen の kw-only）と重なり、この単位の直しだけでは出ない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 所見とも影響は D1 + D2 で、検証役の重大度の理由は頻度（R1-r2-6 の設計役 low は v2 で 6 木 15 箇所と数えたため）と書き方のまれさ（R1-r1-11）だった。「D3 / D4 だけなら low」を理由にした形跡は無い。
- **推奨の理由**: 推奨の基準を次のように満たす。
- 代表（R1-r1-2）は 3 意見一致の high、R1-r2-6 は medium。
- 直し方は Python の呼び出しの意味そのもので、v2 / v3 に合わせたものではない（D61 の基準 1・2 を満たす）。検証役の条件つきで一般に正しいことを試作（AG_PATCH=2、proto2）で確かめてある。
- 凍結した語彙は増やさない（sink 表は変えず、effects.py が既存の slot へ Map を読むだけ）。
- 設計の観点の反証は無い。
R1-r1-11 は単独なら low でまれな書き方なので、記録に回す選択肢もある。ただし R1-r2-6 の条件 (ii)（staticmethod / classmethod をデコレータで判定する）と同じ「offset の決め方」を直すことになるので、一緒に入れても追加の費用はほとんど無い。
注意点が 3 つある。(a) 解決を上げる変更を含むので、敵対的レビューと diff_effects / compare_scans が必須。(b) 変更は数関数にまたがり、条件も多い（サイズ L）。(c) `callee_kwargs` の kw-only sink slot と `list()` の TRANSFER は、この単位の外の論点として別に扱う。
- **所見**:
  - R1-r1-2: 代表。`**` を捨て、`*args` / `**kwargs` を種付けせず、`sink(**kw)` の行が消える。high（3 意見一致）。直す: 条件 (1)〜(6) つき。kw-only sink slot と `list()` の TRANSFER は単位外。（`**` 実引数と呼び出し先の `*args` / `**kwargs` を捨てる: `f(**d)` の `d` は評価も受け渡しもされず受け取る仮引数が OP/resolved の `Atom(formal)` になる、`*args` ）
  - R1-r2-6: 同じ原因（第 1 実引数の対応）の別の表れ。`Base.__init__(self, …)` は解決されず、`Base.run(self, x)` は実引数がずれる。medium。直す: 条件 (i)〜(v) つき。誤警報の `Base.run_default(cmd)` も直る。（クラス名を通した非束縛メソッド呼び出し `Base.__init__(self, cmd)` / `Base.run(self, line)` を Python の意味（第 1 位置引数がインスタンス）で扱わない: `Base.__init）
  - R1-r1-11: 同じ原因の別の表れ。self / cls 以外の名前の第 1 仮引数で実引数がずれ、O31 の枝刈りで誤 clear になる。low でまれ。R1-r2-6 と同じ offset の判定を直すので一緒に入れる（クラス体の `staticmethod(...)` 再束縛を見ることが条件）。単独なら記録に回してもよい。（O31 の静的仮引数: 第 1 仮引数が `self` / `cls` 以外の名前のインスタンスメソッドでは実引数が 1 つずれて割り当てられ（`_seed_params_raw` / `_static_params` の offset を）

### U23 入口の仮引数の種付け（注釈の型・Context）（段階 B・重大度 高・推奨 一部直す）

ツールの入口では、モデルが埋める引数に最初の値（種）を置きます。今はこの種が、注釈の型に関係なくほぼ一律に「中身の分からない 1 個の値」になっています。そのため三つの取りこぼしが起きます。(1) `path: Path` の引数に `path.write_text()` を呼んでも、受け手がファイルパスだと分からず、書き込みが 1 行も出ません。(2) pydantic や dataclass で型を付けた引数（`req: WriteReq`）の `req.path` は「モデルが選べる」値と判定されず、readOnly や非破壊を宣言したツールへの書き込みやシェル実行が「矛盾」ではなく「不明」に回ります。(3) サーバ起動時に用意した DB やクライアントを `ctx.request_context.lifespan_context` から取り出すと、その先の DB / NET / SPAWN の効果が 1 行も出ず、黙って「矛盾なし」側に倒れます。どれも矛盾を見落とす向き（誤 clear）の誤りです。ほかに `ctx: Context` 自体をモデルの引数として扱う点を指摘した所見がありましたが、設計と一般性の両方の観点で反証されています。

- **宣言**: D1 / D2 / D3　**向き**: 誤 clear　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: ツール入口の仮引数の種（`params_of` → `_seed` / `seed_model_param`）が、注釈とフレームワークの型を形に反映せず平らな Atom にする: `Path` 注釈の引数は Path 形にならず pathlib sink の受け手型が付かない、pydantic BaseModel / dataclass 注釈の引数はフィールドごとに MODEL/resolved を持つ Obj にならず `req.path` が MODEL/opaque（選べない → 不）、`ctx` の `request_context.lifespan_context`（lifespan の yield 値）に型が付かず DB / NET / SPAWN の proxy sink が出ない。`ctx: Context` 自体を MODEL として種付けする点（R2-r1-10。検証で落ちた所見）も同じ種付けの場所の話。
- **コードの場所**: authgap/analyze.py:224-253 _seed, authgap/val/engine.py:2420-2431 seed_model_param, authgap/val/engine.py:2399 _seed_from_annotation, authgap/entries.py:184-232 params_of, authgap/catalog/entries.py:107-152 入口規則（Context / lifespan）
- **重大度の根拠**: 代表は R4-r4-1（lifespan）と R4-r4-2（pydantic / dataclass）で、3 観点の重大度は R4-r4-1 が high / high / high、R4-r4-2 が high / high / medium（中央値 high）。
- R4-r4-1 は公式 SDK の README に載っている推奨の書き方で起きる。v2 で `lifespan_context` を読む木は 87 木中 9 木（76 行。設計の検証役が数えた）、v2+v3 ではツール本体で直接読むツール定義が 121（11 木）、ヘルパ経由を含めると 273 行 / 40 木（探索役。一般性の検証役も 40 木で一致）。該当するツールでは proxy の DB / NET / pipe の行が 0 になり、残るのはユニットの opaque_reasons だけ。
- R4-r4-2 は v2 の粗い AST 数え（過大計上）で、同じファイルで定義したモデルで型付けした仮引数を持つツール定義が 395 / 18 木、または 399 / 19 木。そのうちフィールドが制御 slot に届く数は未測定。行は `contradiction_unknown`（不）として残る。§9.3 はこれを「誤 clear ではなく不明への移動」と呼ぶ。
- R4-r1-6 は medium。v2 に Path 注釈の仮引数は 0 件（一般性の検証役）。
- R2-r1-10 は 3 意見とも low。
- 旧文言の影響: 4 件とも影響は D1+D2（探索役の自己申告）。「D3 / D4 だけなら low」を理由に下げた重大度は無い。
- D3 への効き: NET の proxy 行が消えるので D3 にも効くはずだが、件数は未測定。D4 は未確認。
- **直し方（一般に正しいか: 条件つきである）**: 【R4-r4-1（lifespan 値。直すなら）】
直し方: `ctx.request_context.lifespan_context`（fastmcp 2.x の `ctx.lifespan_context`、低レベル形の `server.request_context.lifespan_context` も）に、lifespan 関数の yield 値を種として置く。値は既存の D51 `<yield>` の経路で、`_descend_env` を `on_call=None` で呼んで取る。ツールには起動時の効果を付けない。yield が読めないときは戻り値注釈 `AsyncIterator[X]` の X を木内クラスとして `Obj` にする。主体は OP。

素朴な直し方で壊れる反例（一般性の検証役、ce_lifespan_rebound）: yield 値を RESOLVED で種付けると壊れる。lifespan_context は呼び出しをまたいで共有される可変オブジェクトなので、別のツール `set_query` が `st["sql"] = sql`（MODEL の値）と書き込める。すると readOnly の `run_saved` の `st["db"].execute(st["sql"])` が、起動時の定数 "SELECT 1" だけを見て READ → 内 になり、`st["method"]` も "GET" → HTTP_SAFE → 内 になる。今は「不明」として痕跡が残っているのに、それが消えて新しい誤 clear を作る。

避ける条件:
- (1) 種は D17 改訂 4 / 5 のモジュール水準の可変オブジェクトと同じ規則で作る。`_opaque_deep` で形と主体を保ち、確度だけ opaque にする。`Value.const` は resolved でなければ None。受け手型は残るので `"DELETE…" + item_id` は `db_model_sql` の矛になる。共有状態に置いた定数は `db_sql_unreadable` 等の不にする。
- (2) 種を置くのは、装飾子の受け手名が指す自分の構築式（`FastMCP(...)` / `Server(...)`）を import 表で厳密に解け、`lifespan=` が木内の CM 関数名のときだけ。mount・合成・閉包・工場関数・partial では何もしない（今日と同じ行 0 のまま）。
- (3) `Context` 注釈は D61 追記の条件で mcp / fastmcp のものに限る。注釈の先頭名がモジュール直下で 2 回以上束縛される場合、相対 import の場合、木内モジュールの場合は付けない。利用者定義の `Context` を誤って種付けしないため。
- (4) `ctx` 自体は凍結した語彙のもとで MODEL の仮引数のまま残す（R2-r1-10 は採らない）。部分パスだけが OP になるので、付録の INJECT 座標から ctx を根にする行が消える。この点を記録する（D1 / D2 の類は不 → 不で変わらない）。

その他の条件:
- 構築子 / 属性遷移のカタログの追加に当たる。凍結後の逸脱として preregistration に書く（D50 の逸脱 #15 が前例）。
- 解決率を上げる向きなので、CLAUDE.md の敵対的レビューと `compare_scans.py` / `diff_effects.py` を通す。
- D51 / O29 その 2（dejavu の注釈付き代入 `db: DejavuDB = ctx.request_context.lifespan_state["db"]`。今も行 0）と同じ項目に束ねる。

【R4-r4-2（pydantic / dataclass 引数。直すなら）】
直し方: 注釈を、`Optional` / `Annotated` / 文字列注釈をほどいてから、D61 追記の条件と `resolve_module_strict` で木内クラスに厳密に解く。クラスの家族（木内の基底まで）が BaseModel / dataclass / NamedTuple のときだけ、`Obj((C,), fields)` を種にする。各フィールドは `Value(MODEL, RESOLVED, Atom(formal=f"{name}.{f}"), roots={f"{name}.{f}"})` とし、root をフィールドごとに分ける（主語一致 D25 / O34 のため）。入れ子は RECEIVER_DEPTH で打ち切り、`shape_from=annotation` を記録する。

素朴な直し方で壊れる反例（ce_pydantic_hooks）: フィールドを無条件に RESOLVED にすると壊れる。`field_validator` で `os.path.join(BASE, basename(v))` に変換する形、`model_validator` が `self.path = FIXED`（OP の定数）に置き換える形、dataclass の `__post_init__`、`Annotated[str, AfterValidator(...)]` の 4 つで、`.path` がすべて `fs_writeout_model_path` の矛になる。§9.3（モデリングしていない関数を通った値は opaque）と食い違い、write_fixed は誤警報になる。

避ける条件:
- クラス家族に構築時フックが 1 つでもあれば、今日どおり `opaque("unresolved")` を合流した MODEL にする。フックは pydantic / dataclasses の import で解いた `field_validator` / `validator` / `model_validator` / `root_validator`、`Annotated` の中の `*Validator`、`model_post_init` / `__post_init__` / `__init__` の定義。
- 外部の基底を持つクラスは種付けしない。
- `ClassVar`、`_` で始まる名前、`PrivateAttr`、`field(init=False)` はフィールドから外す。外さないと OP の定数を MODEL にする誤警報になる。
- `@property` / `computed_field` は今までどおり opaque。
- 入口規則ごとに、フレームワークが注釈どおりに構築することを執行表（§2 :332-334）で確かめてから当てる。
- langroid の `message_fields` にも同じ穴があるので、同じ条件を入れる。
- §2.6:517（その他 → Atom、型環境は構築しない）の字義からの逸脱になる。

【R4-r1-6（Path 注釈。直すなら）】
直し方: 入口の仮引数に限り、形だけを `Path(base=MODEL/RESOLVED Atom)` にする。主体と root は変えない。

素朴な直し方で壊れる反例（ce6_intree_path）: 注釈の文字列が `Path` で始まるかで決めると壊れる。木内に `class Path`（`write_text` が HTTP POST）があるとき、偽の `pathlib.Path.write_text` FS_WRITE と D1 の矛が足される。

避ける条件: `_annotation_type` と同じ守りを通す。注釈の先頭名がモジュール直下でちょうど 1 回、level 0 の `from pathlib import Path` / `import pathlib` で束縛され、木内モジュールでないときだけにする（patchB2_guarded で確認済み）。受け手型は sink 表の `pathlib.Path` から機械的に導く。`Annotated[Path, ...]` は対象外（限界として書く）。§2.6:517 からの逸脱として D 番号を付けて記録する。

【R2-r1-10（ctx を OP にする）: 直さない】
素朴な直し方で壊れる反例（c10_sampling）: ctx を除外すると壊れる。`ctx.session.create_message` / `ctx.sample` の結果は LLM が生成した文字列なのに、LLM_CALLS に無いため、今それを MODEL に保っているのは ctx の種だけ。ctx を OP にすると、SELECT の前置き + サンプリング結果の SQL が READ → 内 になり、誤 clear になる。

避けるには R2_EXCEPTIONS への Context の追加、R1 の LLM_CALLS へのサンプリングの追加、elicit / read_resource の主体の決定が必要で、どれも月 3 凍結の語彙の追加に当たる。
- **記録済みの限界・決定との重なり**: - R4-r4-1: 設計の検証役は既知の限界として反証した。根拠は D51（decisions.md:2758-2766 の dejavu の lifespan_state。「DB を超えた一般的な変更なので手を付けない」）、O29 その 2（open_questions.md:866-868「未着手」）、D61 G4（注釈による型付けを一般機構に選んだ）、§2.6:515/517/1118（深さ 2 まで、ctx は Atom、解決できない `.execute()` は db_unresolved）。ただし同じ検証役が、D51 は所見の機構（yield 値の種付け）を検討して退けた記録ではなく、D51 の診断「型は注釈付き代入でしか分からない」は SDK の意味から見て不正確と認めている。一般性の検証役も、O29 は限界ではなく着手待ちの記録と判定した。review_plan §5 の既知の一覧に O29 / D51 は入っていない。
- R4-r4-2: 設計の検証役は仕様どおり（§2.6:517 その他 → Atom(formal)、型環境は構築しない）として反証した。§9.3（contradiction_principles.md:308-310）は「書き出し先のパスのようにモデルが選べているものも不明に移る（誤 clear ではなく不明への移動）」とこの帰結まで記録している。D50 / D61 G4 は注釈で型を付ける範囲を意図的に絞っている。一般性の検証役は、添字 `req["path"]` が注釈に関係なく resolved を保つのに属性だけ opaque になる非対称は実装の産物だとして生き残らせた。
- R4-r1-6: 設計の検証役は仕様どおり（§2.6:517）、D50 の「注釈は証明ではない」の範囲の決定として反証した。所見の「§2.6 は Path を範囲とする」は読み違え。
- R2-r1-10: 設計・一般性の両方で反証され、143 件中ただ 1 件落ちた所見。R2_EXCEPTIONS（Semantic Kernel の 1 件）への追加は月 3 凍結の入口規則の追加に当たり、review_plan §2 の対象外。一般性の検証役はサンプリングの反例で、直し方が一般に正しくないことを示した。探索役の「run20 で ctx 根の MODEL slot 0 件」も誤りで、dejavu の `dejavu_reindex` に 20 件ある（D3 の net_model_host_opaque）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも影響は D1+D2 で、検証役の重大度の理由は露出の少なさ（R4-r1-6 の low は v2 で 0 件）、類が変わらないこと・語彙の追加が要ること（R2-r1-10）、行が不として残ること（R4-r4-2 の medium）。「D3 / D4 だけなら low」を理由に下げた形跡は無い。R2-r1-10 の検証役は dejavu の 20 slot が D3 だけに効くと事実として書いているが、low の根拠にはしていない。
- **推奨の理由**: 単位の中に直すべきものと記録に回すべきものが混ざっている。

直す: R4-r4-1（lifespan）。
- 重大度 high で、公式 SDK の推奨の書き方で起きる。
- 行そのものが消え（NET / git / pipe はサイトに痕跡も残らない）、規則 4「黙って安全側に倒さない」に反する。
- 一般に正しい直し方がある。条件は、可変の共有状態として `_opaque_deep` で種付けすることと、自分の構築式を厳密に解くこと。
- sink / 入口 / weak 理由の語彙の追加は要らない。構築子カタログの逸脱記録は要る。
- 設計の反証の根拠 D51 / O29 は「未着手」の記録で、機構を退けた決定ではない（設計の検証役自身もそう認めている）。
- ただし設計の観点は反証しているので、学生が「記録済みの限界」と読むなら記録に回すのも一貫した判断。
- サイズ L、解決率を上げる向きなので敵対的レビューが要る。

限界として記録: R4-r4-2 / R4-r1-6。
- 設計の観点が §2.6:517 の書かれた規則どおりと判定した。R4-r4-2 の帰結は §9.3 に「不明への移動」として明記済み。
- 直すことは仕様の字義からの逸脱で、R4-r4-2 には構築時フックなどの条件が多い。
- R4-r4-2 は high で直し方も条件つきで一般に正しいので、学生が逸脱として直す判断も妥当。直すなら fix_outline の条件をすべて入れる。
- R4-r1-6 は v2 に該当 0 件で、直すなら小さい（S）。

記録: R2-r1-10。
- 2 観点で反証済み。語彙の追加が要り、一般に正しい直し方が無い。
- **所見**:
  - R4-r4-1: 代表。lifespan の yield 値に型が付かず、proxy の DB / NET / SPAWN 行が消える（high / high / high）。設計の観点は D51 / O29 の記録として反証したが、その記録は着手待ち。一般性の観点は条件つきで生存（RESOLVED ではなく _opaque_deep で種付けし、自分の構築式を厳密に解く）。推奨: 直す（FastMCP / 低レベル Server の lifespan 文脈（`ctx.request_context.lifespan_context` / `server.request_context.lifespan_context`）経）
  - R4-r4-2: 同じ原因の別の表れ（注釈を種付けに使わない → フィールドの主体の確度が opaque になる）。重大度 high（中央値）。設計の観点は §2.6:517 / §9.3 どおりとして反証、一般性の観点は構築時フックの条件つきで生存。推奨: 限界として記録（逸脱として直す選択肢も妥当）（pydantic BaseModel / dataclass で型付けしたツール引数（`req: WriteReq`）のフィールド読み出し `req.path` が MODEL/opaque(unresolved) になり、原理 3-a の）
  - R4-r1-6: 同じ原因の別の表れ（Path 注釈 → 受け手型が付かず pathlib の sink を落とす）。medium。設計の観点は §2.6:517 どおりとして反証、一般性の観点は D61 の守りつきで生存。v2 に該当 0 件。推奨: 限界として記録（直すなら S）（ツール引数の注釈が Path / pathlib.Path のとき種が Atom になり、その引数への write_text / unlink（語彙にある sink）が受け手型で照合されず消える）
  - R2-r1-10: 同じ種付けの場所の話で、設計・一般性の両方で反証済み（落ちた唯一の所見）。ctx を OP にするとサンプリング結果で誤 clear になり、R2_EXCEPTIONS と LLM_CALLS の語彙追加が要る。low。推奨: 限界として記録（ctx の MODEL の種は保守的な符号化）（FastMCP が実行時にスキーマから除く `ctx: Context` 仮引数を MODEL として種付けし、ctx 由来の path / argv が主体 MODEL になる（D1 / D2 の理由が *_model_opaque に付）

### U25 _self_fields の cache（鍵と番兵）（段階 A・重大度 高・推奨 直す）

解析器は、クラスの `__init__` で `self.conn = sqlite3.connect(...)` のように書かれたフィールドの中身を一度調べると、表（cache）に覚えて使い回します。この表の見出しに「解析中の木の索引オブジェクトのメモリ番地（id）」を使っているため、1 つのプロセスで木を続けて解析すると（scan_v2.py / two_sided.py）、捨てられた前の木の番地が次の木で再利用され、同じモジュール名・クラス名を持つ別の木のフィールドがそのまま使われます。その結果、`self.conn.execute(sql)` の DB 効果と D1 の矛が消えたり（誤 clear）、無い効果が立ったり（誤警報）し、結果が「前に何を解析したか」で変わりますが、`--determinism` は同じ木を繰り返すだけなので見えません。もう 1 つ、`__init__` の評価が深すぎて RecursionError になると、途中に置いた仮の空の値が表に残り、同じクラスの 2 つ目以降のツールは打ち切りの印なしで「フィールド無し」として解析されます（まれ）。

- **宣言**: D1 / D2 / tooling　**向き**: 混在　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `analyze._SELF_FIELD_CACHE` の鍵が `id(index)` なので、1 プロセスで複数の木を解析すると（scan_v2.py / two_sided.py）解放された index の id が別の木で再利用されて別の木のクラスのフィールドが流用され、また再帰打ち切りの番兵 `()` を RecursionError の後も cache に残すので同じクラスの 2 つ目以降のユニットは印なしで self のフィールドを失う（結果がプロセス履歴・ユニットの順に依存し、`--determinism` では見えない）。
- **コードの場所**: authgap/analyze.py:313-331, 376 _SELF_FIELD_CACHE, authgap/runner.py:139 RecursionError の捕捉, scripts/scan_v2.py:139 / scripts/two_sided.py:157 同一プロセスでの複数の木
- **重大度の根拠**: 代表は R5-r1-1。3 観点の意見は探索 high / 設計 medium / 一般性 high で、中央値は high。high とする理由（一般性の観点）: 出力が入力だけで決まらなくなり（仕様 §5.2 と cli.py の「同一入力で決定的」の約束に反する）、核の経路（self.<field> 経由の proxy sink。run20 ではメソッド形のユニットが 2231 中 567、うち効果あり 325、CONTRADICTION あり 83）で両方向に黙って誤り、事後に再現できない。設計の観点が medium に下げた根拠は旧文言「D3 / D4 だけなら low」ではなく、衝突の頻度の実測: v2 の corpus（100 ディレクトリ、51,953 ファイル）でフィールドを持つ (module, class) の組 65,466 のうち、2 木以上で共有されるのは ('src.config', 'Settings') の 1 組だけ。実害の実測はいずれも 0: run20 の 87 木で鍵 213 個、木をまたいで共有される鍵 0（run20 の数字はこの欠陥で動いていない）。two_sided の 7 対は vuln/fixed で鍵を共有する（A9 70、A18 65、A1〜A4 各 1）が、共有鍵の値は両側で全部同じ（7/8 は動かない）。check_gates.py と pytest を 1 プロセスで走らせた汚染の発生も 0。ただし最終評価の新しいデータでは同じ (module, class) を持つ木が並ぶかどうかは未測定で、起きれば誰も気づけない。再現の頻度は合成の対 A→B で 300 回中 22 回、別の 300 回で 35 回、検証役の 80 回で 6 回汚染（run ごとに cache を空にした対照では 300 回中 0 回）。R5-r1-9 は 3 意見とも low（引き金は `__init__` の評価での RecursionError で、v2 では 550 項の連結 1 件だけ、それも `+` の畳み込みで解消済み）。D62 は関係しない（この単位は D1 / D2 と評価の道具に効き、D3 / D4 を理由に下がった重大度は無い）。
- **直し方（一般に正しいか: 条件つきである）**: (1) 鍵（R5-r1-1）: cache を index ごとに持つ。`SourceIndex` のインスタンス属性にする（寿命が index と一致）か、`weakref.WeakKeyDictionary` で index を鍵にする（SourceIndex は素のクラスで同一性による hash を持つので使える）。どちらも生きた同じ index では (id, module, class) と (module, class) が 1 対 1 なので同じ木の値は変わらず、正しいケースを壊す反例は作れない（検証役が index ごとの cache の変種で A→B を 60 回まわし汚染 0、B 単独と一致を確認）。**素朴な直し方で壊れる反例（一般性の観点）: fix_sketch の 3 案目「`_ATOM_INDEX_CACHE` と同じく src_root を鍵にする」は不可。** 同じパスの木を中身を書き換えて同じプロセスで解析し直すと前の中身のフィールドが残る（httpx.Client → sqlite3.connect に書き換えた 2 回目で Store.query の DB 効果と contradiction:D1 が消えた）。scripts/mutation_test.py は SourceIndex.parse を差し替えて同じ fixture パスに変異体を流すので、この状況は repo の道具に実在する。index ごとに持てば runner.run() 冒頭の clear は不要（あっても害は無い）。姉妹の `gate.py:116-128` `_ATOM_INDEX_CACHE`（src_root 鍵）も同じ家族で、同一パスの再走査で古くなりうる（本単位の外。設計の観点は run() 冒頭で両方捨てる形が安全と記載）。(2) 番兵（R5-r1-9）: 再帰の打ち切り（`cache[key] = ()` を計算前に置くこと）自体は残す。**素朴な直し方で壊れる反例（一般性の観点）: 例外時に番兵を pop して再計算する案は不可。** 同じクラスの query_b が `os.remove(path)` も直接呼ぶと、今は D1 の矛（fs_write）が正しく出るが、pop 案では再計算で RecursionError が再発してユニット全体が TRUNCATED(recursion) になり、正しい矛が消えた（検証役が確認）。**避ける条件: 失敗を表す印（例 `_SELF_FIELD_FAILED`）を cache に入れ、呼び出し側（analyze.py:236 の _seed と :286 の _closure_seed の両方）で self.<attr> を `opaque(unresolved)`（D17。既存の語彙）として扱ってユニットの残りの解析を続け、そのフィールドを使う各ユニットに打ち切りの印（例 `TRUNCATED(recursion:self_fields)`）を付ける。** 印は `res.wall_clock_truncations` 側の件数にも載せ、TRUNCATED の接頭辞で数える集計から漏れないようにする（規則 4）。(3) テスト: 「同じ module 名・クラス名を持つ 2 木を 1 プロセスで A→B の順に解析し、B の効果行・判定行が B 単独と一致する」「同じパスの木を書き換えて再解析すると新しい中身が使われる」「`__init__` が RecursionError を起こすクラスの 2 ユニットが両方とも印を持ち、直接の sink の矛は残る」を固定する（--determinism では見えないので必須）。(4) 手順: authgap/ を変えるので指紋が変わる。規則 → 反例テスト → 実装、scan_v2_run21 を取り compare_scans / diff_effects で run20 と突き合わせる。run20 は共有鍵 0 なので一致するはずで、差が出たら 1 件ずつ理由を確かめる（汚染の除去でありうることも記録）。
- **記録済みの限界・決定との重なり**: 記録済みの限界との重なりは無い。review_plan §5（O35〜O41、K1〜K7、MAX_DEPTH など）のどれでもない。関連する記録: evidence/determinism_v2/README.md:24-30、D34（decisions.md:397-403）、逸脱 #9（preregistration.md:547）は「同じ木の 2 回目で cache が温まり壁時計の印だけが変わる。効果行・等級・判定は同じ」とだけ書いており、別の木のフィールドの流用を受け入れた記録は無い（むしろ「解析結果は同じ」という記録と反する）。D52（decisions.md:2801）の「--determinism 3 は 1 プロセスの中で繰り返すので見えていなかった」と同じ盲点。R5-r1-9 は D17 改訂 4（decisions.md:1718、RecursionError をユニット単位で捕まえて TRUNCATED(recursion) として残す）の意図から漏れた形。設計の観点は R5-r1-9 について「query_b の DB 呼び出しは db_unresolved（D49）に記録されるので完全に黙って消えるわけではなく、query_a も効果 0 なので両ユニットとも D1 の矛は出ていない。誤 clear より打ち切りの数え落としに近い」と向きを count_loss に修正したが、反証（refuted）はしていない。両所見とも設計・一般性の両観点で refuted=false。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R5-r1-1 の設計の観点が medium に下げた根拠は v2 での (module, class) の衝突頻度の実測（65,466 組中 共有 1 組）で、D3 / D4 の旧文言ではない。R5-r1-9 の low は 3 観点とも引き金の稀さ（`__init__` での RecursionError）による。この単位は D1 / D2 と評価の道具に効くもので、D3 / D4 を理由にした格下げは無い。
- **推奨の理由**: 代表の重大度が high（3 意見の中央値。設計の観点の medium でも基準を満たす）。一般に正しい直し方がある（index ごとの cache と失敗の印。検証役の条件つき: src_root 鍵と pop 再計算は不可）。凍結した語彙の追加は要らない（opaque(unresolved) は既存の語彙で、打ち切りの印はメモの文字列で sink / 入口 / weak 理由ではない）。設計の観点は両所見とも反証していない。何より、学生の最終評価は scan_v2.py で新しいデータの木を 1 プロセスで続けて解析するので、この欠陥はまさに最終評価の経路で起き、起きても --determinism でも事後の再走でも見えない（review_plan §1 の (c)「数字が静かに変わり、誰も気づかない」に当たる）。run20・two_sided・凍結の門の実測の実害は 0 なので、直しても v2 の数字は動かないはずで、run21 との突き合わせが直しの正しさの確認になる。R5-r1-9 は low だが同じ関数の同じ cache の扱いで、直しは小さく正しいケースを壊さない（失敗の印の方式に限る）ので、同じコミットで直すのが安い。学生が範囲を絞りたい場合は R5-r1-9 だけを限界として記録に回す選択は成り立つ。
- **所見**:
  - R5-r1-1: 代表。cache の鍵が id(index) なので、1 プロセスで複数の木を解析すると死んだ index の番地の再利用で別の木の同名クラスのフィールドが流用される（誤 clear / 誤警報の両方、非決定性）。3 観点とも生存、重大度 high / medium / high。直し方は index ごとの cache に限る（src_root 鍵は同一パスの書き換えで壊れる反例あり）。実測の実害は run20・two_sided 7 対・check_gates/pytest で 0。（analyze._SELF_FIELD_CACHE が id(index) を鍵にするため、1 プロセスで複数の木を解析すると（scan_v2.py / two_sided.py）別の木のクラスのフィールドが流用され、self.<field）
  - R5-r1-9: 同じ cache の別の表れ（番兵の後始末）。`__init__` の RecursionError 後に仮の () が残り、同じクラスの 2 つ目以降のユニットが印なしでフィールドを失う。3 観点とも生存、重大度は 3 意見とも low（まれ）。設計の観点は向きを count_loss（打ち切りの数え落とし）と見る。直し方は失敗の印を cache に入れて opaque(unresolved) + 打ち切りの印に限る（pop して再計算は正しい直接の矛を消す反例あり）。R5-r1-1 と同じ関数で同時に直せる。（_self_fields の再帰打ち切り用の番兵 `()` が、__init__ の評価で RecursionError が出た後も cache に残るため、同じクラスの 2 つ目以降のユニットは印なしで self のフィールドを失う（順序）

### U26 sink の slot に実引数を当てる処理が、Python の引数の渡し方の片方しか扱わない（`*` 展開とキーワード渡し）（段階 B・重大度 高・推奨 一部直す）

危険な関数（sink）の表は「第 N 引数がコマンド名・パス」のように引数の位置を指定しており、解析器はそれを呼び出しの実引数に当てはめる。ところが (1) `create_subprocess_exec(*cmd)` のようにリストを `*` で展開して渡すと、展開せずリスト全体を「コマンド名（argv0）」とみなすので、コマンド名が定数 "git" でも中にモデル由来の要素があれば「モデルがコマンドを選べる」と誤って矛盾にする（誤警報）。(2) `open(file=p, mode="w")`、`subprocess.run(args=cmd, shell=True)`、`shutil.copy(src=, dst=)`、`proc.communicate(data)`（位置渡し）のように、表が想定していない側の渡し方（仮引数名つき、または位置）で書くと slot が空になり、効果の行ごと消えるか書き出し先のパスが消えて、本来の矛盾が出ない（誤 clear）。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: sink 行の実引数の指定 `A(pos, kw)` を呼び出しに当てる `_arg_value` / `_materialise` と、行の書き方が Python の実引数の渡し方の片方しか扱わない: `*cmd` の Starred を要素に展開しないので `create_subprocess_exec(*cmd)` の program（argv0）が列全体になり、多くの行が位置 `A(0)` だけで仮引数名 `kw` を持たないので `run(args=…)` / `open(file=…)` / `shutil.copy(src=, dst=)` / `os.remove(path=)` などキーワード渡しで slot（または行全体）が落ち、`communicate` 行は `KW("input")` だけで位置渡し `communicate(data)` を引かない。
- **コードの場所**: authgap/effects.py:173-210 _arg_value, authgap/effects.py:656 _materialise, authgap/catalog/sinks.py:243-403 DIRECT 行の A(pos), authgap/catalog/sinks.py:294 create_subprocess_exec 行, authgap/catalog/sinks.py:650 communicate の PipeRow
- **重大度の根拠**: 代表は R4-r1-1（探索 high / 設計 medium / 一般性 high の中央値 = high）。主指標 D1 / D2 の判定が「不 → 矛」に転ぶ誤警報で、可変長 API へ組み立てたリストを渡す普通の書き方（corpus 全体で 39 箇所。一般性の検証役の数え）で、リストが resolved なら必ず起きる。設計の観点が medium にした理由は「v2 run20 では argv0 が Seq の 8 行がすべて opaque で、判定が転んだ行は 0」で、旧文言「D3 / D4 だけなら low」とは関係ない。R4-r1-2 と R4-r1-3 は 3 観点とも medium（EXEC や FS_WRITE の矛が行ごと消える誤 clear。v2 では該当 0 件〜判定不変）。
- **直し方（一般に正しいか: 条件つきである）**: 3 つとも、正しい答えは Python の言語の意味とライブラリの関数の書き方（シグネチャ）から決まる（D61 の基準 1・2 を満たす）。検証役がパッチを当てた複製では、凍結済みのテストが 830 passed / 0 failed、B3a 8/8、B3b 15/15 だった。

(A) R4-r1-1（`*` 展開）: 展開は sink の束縛（`effects._arg_value` / `_materialise`）の中でだけ行う。`ev.node.args[i]` が `ast.Starred` で、その値の形が Seq / Argv のときは位置 i 以降に要素を並べて引く。argv0 = A(0) は展開した列に `_first_element` を当てた値（elems[0]、無ければ tail）。`subprocess.run(cmd)` の elem0 と同じ意味にする。`argv[*]`（varargs）は展開した後の列にする。形が Atom / Unknown のときは今どおり値全体を使う（MODEL のまま残り、誤 clear を作らない）。
【避ける条件】
- `engine._ev_Call`（engine.py:727-728）の args で展開してはいけない。木の中の関数へ降りるときの仮引数の束縛まで変わる。D58 規則 2(a) は構文の `*` を見ているので、この直し方で枝刈りが再び有効になることはない。
- Seq に tail（長さの分からない部分）があるときは、それより後ろの位置引数を特定の位置に結ばない。tail に畳む。
【素朴に直すと壊れる反例（一般性の検証役）】
`cmd = args + ["--oneline"]; create_subprocess_exec(*cmd)`（args: list[str]）。本当の argv0 は args[0] で MODEL（= 矛）だが、fix_sketch だけを当てると argv0 = '--oneline'（OP）になり、新しい誤 clear になる。原因は既存の `_concat`（engine.py:596-599 の `elems = a.elems + b.elems, tail = a.tail or b.tail`）で、左の列に tail があるのに右の要素を先頭に置いてしまう。直すには `_concat` もあわせて直す必要がある。左に tail があるときは、左の既知の先頭だけを elems に残し、右の要素と tail は join して左の tail に畳む。この欠陥は fix と関係なく今すでに起きている。`subprocess.run(model_list + [const])` が誤 clear になり、`subprocess.run(config_list + [model])` が誤警報になる。後者は Seq(elems, tail) の表し方では位置の区間を書けないので、`_concat` を直しても残る。fix が新しく作る誤りではないが、限界として記録する。`_concat` の欠陥はどの所見にも無いので、`docs/open_questions.md` に別に記録する。`_register_handle`（effects.py:775）と CtorRow の `spawn_argv: arg0` は、列全体から先頭を引くので今のままで正しい。

(B) R4-r1-2: sinks.py:650 を `PipeRow("communicate", {"stdin": A(0, kw="input")})` にする（既存の A(pos, kw) の仕組み。F8 / D59 と同じ）。第 2 位置引数の timeout は読まない。`communicate()` と `communicate(timeout=…)` は今どおり行を出さない。`communicate(None)` は、キーワード形 `input=None`（O41 の既知の挙動で、EXEC OP → 矛）と同じ扱いになり一貫する。反例は 9 形試して見つからなかった。

(C) R4-r1-3: 各行の A(pos) に、そのライブラリの正確な仮引数名を kw として足す。open → file、subprocess.* → args、makedirs → name、mkdir / remove / unlink / rmdir / chmod / rmtree → path、glob → pathname、os.walk → top、os.popen → cmd、os.system → command、unpack_archive は content → filename と path → extract_dir、urlretrieve の path → filename、copy / copy2 / copyfile / move → src / dst、rename / replace / symlink → dst、sqlalchemy.text → text。A(pos, kw) は位置に値が無いときだけ kw を引くので、既存の位置渡しの結果は変わらない。
【避ける条件】
- 位置でしか渡せない（positional-only）仮引数には kw を足さない（eval / exec の source）。
- 抜けやすい所: CtorRow `subprocess.Popen` の `spawn_argv: "arg0"`（transfers.py:178）と `_register_handle` の `ev.args[0]`（effects.py:775）も args= を読むようにする。そうしないと `Popen(args=["python3"], stdin=PIPE).communicate(input=code)` の pipe 行は、EXEC ではなく FS_WRITE のまま残る（D1 は fs_write の矛で変わらないが、kind が誤る）。

【共通】`raises_resolution` の向きの変更なので、敵対的レビューを通す（CLAUDE.md）。直した後は `scripts/diff_effects.py` と `scripts/compare_scans.py` を必ず通す。(A) は CONTRADICTION が消える向きなので、消えた 1 件ごとに argv0 が本当に定数であることを確かめる。
- **記録済みの限界・決定との重なり**: - D59 の追記（decisions.md:3340-3357）: 「HTTP 以外の行は変えない。Popen 4 件・pipe 1 件は既知の限界」と決めている。設計の観点は R4-r1-3 をこの記録済みの限界として反証した（確信度 0.6、refuted=true）。所見の dbt-mcp `Popen(args=…)` の 4 行は、この「Popen 4 件」そのものである。ただし設計の観点は迷いも書いている。D59 の測定には盲点があり、全部の slot をキーワードで渡す呼び出し（open(file=, mode="w")、shutil.copy(src=, dst=)、subprocess.run(args=, shell=True)）は行ごと消えるので数えられていない。unpack_archive / urlretrieve の path が消える件は、run17 に該当が無かっただけである。
- R4-r1-2 は D59 の「pipe 1 件」とは別物（位置渡しの communicate は行ごと消えるので、その測定に出ない）と設計の観点は判断した。しかし直し方は非 HTTP の行を変えるので、D59 の「HTTP 以外の行は変えない」の文言からは外れる。
- D58 改訂 (A)（decisions.md:3205-3209）は、`_ev_Call` が `*` を 1 つの位置引数にすることを O31 の原因として記録している。対処は `_is_plain_call` による枝刈りの停止で、sink の束縛を正しいと認めた決定ではない。
- 次のものとは根本原因が別: O35（argv 要素の中の分解）、F9 仕様（非 `*` 形では argv0 = Seq.tail。直し方はこれを保つ）、O41 / K1（communicate(input=None) と EXEC の分類）、D61 G1 の取り消し（pipe の未判定行を落とさない。直し方は行を足す向きなのでこれに反しない）。
- 隣にあるが別の所見: R1-r1-7（K=16 を超える要素を `_concat` などが捨てる）、R4-r2-1（INDIRECT 表の 2 つ目以降の実引数を捨てる）。
- `_concat` が tail の後ろの要素を先頭に置く欠陥は、検証役が見つけたがどの所見にも無い。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも影響は D1 + D2 で、検証役の重大度の理由に D3 / D4 は出てこない。R4-r1-1 の設計の観点が medium にしたのは「v2 run20 で判定が転んだ行が 0」のためで、旧文言によるものではない（代表値は中央値で high のまま）。
- **推奨の理由**: R4-r1-1（high）と R4-r1-2（medium）は fix の基準をすべて満たす。3 観点とも生き残り、一般に正しい直し方があり、語彙の追加は要らず、設計の観点の反証も無い。ただし R4-r1-1 は `_concat` の順序もあわせて直すことを条件にする（直さないと新しい誤 clear を作る）。R4-r1-3 は、設計の観点が D59 の記録済みの限界（「HTTP 以外の行は変えない」）として反証したので、基準に従えば限界として記録する側になる。その場合も、D59 の限界の文言を広げて記録する必要がある。今の記録は「Popen 4 件・pipe 1 件」だけで、「全部キーワードで渡すと FS_WRITE / SPAWN の行が丸ごと消える」「書き出し先の path が消えて矛が不に落ちる」という新しく分かった盲点を含んでいないので、open_questions / O41 に足す。学生が D59 の前提（影響が無視できる）を見直して直す場合は、D59 からの逸脱として decisions.md と preregistration に書く。その際は非 HTTP の行を一括で直し、CtorRow Popen と `_register_handle` の args= も含める。R4-r1-2 を直すことも、D59 の文言上は非 HTTP の行の変更になる。そのことを決定の記録に一言書いておくとよい。
- **所見**:
  - R4-r1-1: 代表（high、誤警報）。`create_subprocess_exec(*cmd)` の argv0 に、要素ではなくリスト全体が入る。直す。条件: 展開は sink の束縛の中だけで行う / tail がある列の後ろの位置は決めない / `_concat` の順序もあわせて直す（反例 `args + ["--oneline"]`）。v2 run20 では該当 8 行がすべて opaque で、判定の変化は 0。（asyncio.create_subprocess_exec(*cmd) の * 展開で argv0 がリスト全体になり、定数の program でも MODEL 由来として矛（本来は不））
  - R4-r1-2: 同じ原因の別の現れ（逆向き: 表が KW("input") だけで、位置渡しを引かない）。medium・誤 clear で、EXEC の矛が行ごと消える。A(0, kw="input") で直す。反例は 9 形試して無し。v2 の位置渡しは 0 件で、corpus の実例は OpenManus / praisonai / mastermind / v3 の 4 箇所。（proc.communicate(data)（位置引数）は pipe 行にならず、インタプリタへのコード投入 EXEC が消える（KW("input") しか引かない））
  - R4-r1-3: 同じ原因の別の現れ（表が A(pos) だけで kw を持たない）。medium・誤 clear。設計の観点が D59 の記録済みの限界として反証（確信度 0.6、盲点があるとの注記つき）しているので、既定は限界として記録（D59 の限界の文言を広げる）。直すなら D59 からの逸脱として記録し、CtorRow Popen と _register_handle の args= も含める。v2 への影響は dbt-mcp の Popen(args=) 2 箇所・4 行で判定不変、FS 側のキーワード渡しは 0 件。（A(pos) に kw が無い行は、仮引数名で渡した呼び出しで slot（または効果行全体）を落とす: Popen/run(args=…)、open(file=…)、unpack_archive(…, extract_dir=…)、urlr）

### U38 mcp 2.x の読み方（SDK の署名どおりに読まない）（段階 B・重大度 高・推奨 一部直す）

MCP の公式 SDK は 2.x で書き方が変わりました。解析器はまだ 1.x の書き方を前提に読んでいて、5 か所で読み違えます。2 つが重いものです。(1) 2.x の正しい書き方である snake_case の宣言（`read_only_hint=True`）を常に「綴りの誤り」として捨てる。(2) 2.x の低レベル形で、モデルからの入力が入る `params.arguments[...]` を「出どころが追えない値」として扱う。どちらも、本当は「宣言と食い違う（矛）」と出るべき行が「矛なし」か「判定不能（不）」に落ちる向き、つまり見逃しの誤りです。残り 3 つは軽いものです。`add_request_handler` の引数の位置の読み違い、`Server` のサブクラスや別名 import の見落としでツールが丸ごと消えること、そしてハンドラを名前だけで木全体から探すので tests/ の同名関数を拾って誤警報を出すことです。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: mcp 2.x の SDK を SDK の署名どおりに読まない: 低レベル入口の照合は書かれた呼び出し名の末尾 `Server` だけ（サブクラス・`super().__init__(on_call_tool=)`・別名 import を見ない）、`add_request_handler` は `(method, params_type, handler)` の 3 引数なのに `args[1]` を handler として読みキーワード形も読まない、`on_call_tool=h` の handler は作った import 表を捨てて裸の末尾名で木全体から引く（tests/ の同名関数を拾う）; v2 ハンドラの `params` を `CallToolRequestParams` の形でなく裸の Atom で種付けするので `params.arguments[...]` が MODEL/opaque（v2 低レベル全体で 矛 → 不）; snake_case の ToolAnnotations（`read_only_hint=`）は版を見ずに常に D_malformed（⊥）にする。
- **コードの場所**: authgap/entries.py:645-722 find_lowlevel_units（v2 の枝）, authgap/catalog/entries.py:147-152, 225-227 lowlevel_v2 の入口規則, authgap/analyze.py:224-240 _seed（v2 の params）, authgap/entries.py:799, 864 / authgap/dparse.py:105-119 snake_case の扱い
- **重大度の根拠**: 代表は R2-r1-1 と R2-r3-1 で、どちらも 3 観点すべてが high、向きは誤 clear、効くのは D1+D2。R2-r1-1: 探索役の見積もり（件数にだけ使う）では、v2 で snake_case の ToolAnnotations を持つ木が 5 あり、うち 3 は lockfile で mcp 2.1.1 に確定。canvas-mcp だけで 108 ユニットがすべて ⊥（run20）。camelCase として読み直すと 79 ユニットに上界が付き、D1 の確定した矛が 1 行、D1 の不が 426 行、D2 の不が 110 行現れる。設計観点の検証役は、D48 が「綴りが正しければ CONTRADICTION」とした 2 件（canvas-mcp download_course_file / apk-preview-desktop）がどちらも 2.1.1 に確定する木であることを確かめた。つまり v2 で既に D1/D2 の矛が 2 件見逃されている。2.x では Python 側の属性名そのものが snake_case なので、新しいデータ（D60）では増える向き。R2-r3-1: v2 低レベル形のユニットすべてで、原理 3-a に頼る行（D2 の書き出し、SPAWN の argv0、DB、NET の PUT）が矛から不へ落ちる。コーパスで `on_call_tool=` を持つ木は 413 中 8（探索役の数え）。run20 では R2-r1-1 などで ⊥ になっているため表に出ていない。上限もある。検証役が数えたところ、5 木の中の `args.get(...)`（21/17/95/8/32 行）は v1 でも opaque で、別の既存の限界として直した後も不のまま残る。直して動くのは添字 `args["..."]` の行（12/0/27/0/12 行）だけ。R2-r3-2 / R2-r3-3 / R2-r4-1 は 3 観点すべてが low。理由は書き方がまれなこと（`add_request_handler` の出現はコーパスで 0、サブクラス / 別名もコーパスで 0、run20 の lowlevel_v2 ユニットは napjon の 1 件だけ）で、D3/D4 の旧文言は理由になっていない。
- **直し方（一般に正しいか: 条件つきである）**: 【R2-r1-1 snake_case】版で条件づける。順番は Def 6 の執行表と同じ「(1) API の形 → (2) 版の確定」で、既存の read_dep_pins（lockfile を優先）を使う。`mcp.server.mcpserver` の import、`Server(on_call_tool=)`、fastmcp>=4 のどれかがあれば >=2.0 とみなす。`mcp.server.fastmcp` の import か `@server.call_tool()` があれば <2.0 とみなす。>=2.0 に決まったら SNAKE_ALIASES で camelCase に写して宣言として数え、<2.0 に決まったら今のとおり D_malformed、決まらなければ D_unknown にする（⊥ とも malformed とも混ぜない）。守る条件（一般性の検証役）は 5 つ。(1) API の形で版を決めるのは、木全体で形が一通りのときだけ。try/except で両方の API を import する移行用の shim や、`mcp.server.fastmcp` を import しながら lockfile が 2.x の木は D_unknown にし、どちらにも倒さない（反例 cx_r1_1_ambiguous）。(2) read_dep_pins は os.walk で最初に見つかった lock を採るので、lock が食い違う monorepo も D_unknown にする。(3) mcp==1.30.0 に確定した木（反例 cx_r1_1_pinned1x）では snake_case を malformed のまま保つ。そうしないと誤警報になる。(4) 版が決まらない木の snake_case を ⊥ から D_unknown に移しても verdict は動かない。ただし r_malformed（O27）と r_D の分母は動くので、D48 の表を版ごとに出し直し、compare_scans で run20 と 1 件ずつ突き合わせる。(5) 仕様書 322 行目は書き換えず、decisions.md に D 番号で版の条件を記録し、preregistration に逸脱として書く（CLAUDE.md 規則 5・6）。R2-r2-1（abyss-stack は read_only_hint 37 / readOnlyHint 1）と連動する。
【R2-r3-1 params の種付け】`_seed` で entry_kind == lowlevel_v2 のとき、第 2 位置の仮引数に CallToolRequestParams の形を与える。仮引数は名前でなく位置で選び、self/cls を除いてから数える。与える値は `Obj(("CallToolRequestParams",), name: MODEL Atom, arguments: MODEL Map(tail=MODEL Atom))` を MODEL/resolved にしたもの。`ctx`（第 1 位置）は変えない（R2-r1-10 は反証済み）。一般性の検証役が確かめたこと: 修正を当てた複製で t70 は期待どおり矛になり、v1 の t71 は出力がバイト単位で同一。反例の候補 A2（木の中の非 mcp の Server）、A3（装飾子で (name, arguments) に変える形）、A10（別の同名関数に当たる lookup）、A2b（10 形）は、どれも修正の前後で verdict 行が同じ。pytest 741 passed（失敗 1 は無修正の複製でも同じく落ちる環境要因）、check_gates 15/15。任意の硬化策として、`Server` が import 表で mcp SDK に解けるときだけ種を与える（D61 追記の束縛回数の条件つき）。解決率を上げる向きなので CLAUDE.md の敵対的レビューを通し、増えた矛は v2 低レベルの木に限って compare_scans で 1 件ずつ確かめる。
【R2-r3-2 add_request_handler】method は args[0] か `method=`、handler は `handler=` キーワードを見て、無ければ**最後の位置引数 args[-1]**（len(args) >= 2）から取る。素朴な直し方で壊れる反例（一般性の検証役）: 探索役の案どおり「len(args) > 2 のときだけ args[2]」にすると、自前の JSON-RPC の 2 引数形 `rpc.add_request_handler("tools/call", handle_two)`（ce_r3_2。今はユニットになり contradiction:D1 が出る）が消える。args[-1] にすれば避けられる。
【R2-r3-3 ハンドラの名前の解き方】捨てている scope（import 表）を使い、次の 3 段で解く。(1) import 表で一意に解けるとき（G3 改訂の 3 条件: モジュール直下の束縛がちょうど 1 つ、関数の中で書き換えられない、level で厳密に解ける）だけ、その定義 1 つに絞る。(2) 解けなければ、今の裸名一致に**落とす**。ただし §9.1 / O30 と同じく、登録元がテストでなければテストファイルの候補を外す。(3) dotted 名でない handler 式（partial / lambda）は `unresolved_handler` として件数を manifest に残す（判定は変えない）。素朴な直し方で壊れる反例: 探索役の案どおり「解けなければ記録だけで裸名一致に落とさない」にすると、`from .handlers import *` 経由のハンドラ（ce_r3_3。今は正しく contradiction:D1）が消えて新しい誤 clear になる（CLAUDE.md の落とし穴「末尾名だけの解決をやめると真の経路が消える」と同じ形）。
【R2-r4-1 サブクラス / 別名】別名は、構築子の名前を scope.lookup で解き、`mcp.server.lowlevel.Server` / `mcp.server.Server` に当たれば Server とみなす。サブクラスは、木の中のクラスで基底が Server のものについて、その構築と `super().__init__` / `Base.__init__(self, …)` の `on_call_tool=` を読む。素朴な直し方で壊れる反例（一般性の検証役、ce_r4_1）: `super().__init__(name, on_call_tool=on_call_tool)` のように仮引数をそのまま渡すサブクラスで、ハンドラ名 `on_call_tool` を裸名で引くと、tests/ の同名 test double がユニットになって誤警報を出す。避ける条件は 3 つ。値が囲む関数の仮引数なら名前で引かず、サブクラスを構築している呼び出し点で解く。`self.x` は囲むクラスのメソッドに絞る。R2-r3-3 のテスト候補の除外を併用する。どの形でも `on_call_tool=` キーワードを要求する条件は残す（uvicorn.Server 派生を拾わない）。
共通: ENTRY_RULES の names・キーワード・LOWLEVEL_V2_REQUEST は変えない。fingerprint の entry_catalog は不変で、実装の sha256 だけが変わる。規則 → 反例テスト → 実装の順にコミットし、scan_v2_run21 を取って diff_effects / compare_scans で確かめ、逸脱 #24 に記録する。
- **記録済みの限界・決定との重なり**: D48・仕様書 322 行目・prereg §5 #13・tests/test_d_malformed.py は「snake_case は常に malformed」を意図した決定。ただし設計観点の検証役は、その唯一の根拠「deserialize されず protocol に届かない」が mcp 1.x でしか真でないことを実測で確かめ、版に依存することを検討した記録も無いので反証していない（refuted=false）。直すなら規則 6 に従って仕様書は残し、D 番号と逸脱の記録を付ける。O27 は「記録があるかどうか」の話で、根本原因が別。R2-r3-1 は O33（選べる = MODEL かつ resolved）にも D17（未解決の**呼び出し**を opaque に合流）にも当たらない。入口の SDK 型のフィールドを読むことは、どちらの決定も unresolved としていないので、種付けの欠落と判定された。`_seed` には langroid の ToolMessage を Obj で種付けする前例がある。R2-r1-10（ctx の種付け）は設計・一般性の両観点で反証済みなので、ctx は変えない。R2-r3-3 に近いものとして §9.1 / O30（呼び出しの解決でテストの候補を外す）があるが、入口のハンドラ解決には入っておらず、別の箇所。R2-r4-1 のうちサブクラスの半分は、「入口規則の追加（月 3 凍結、review_plan §2）」に当たるかが境界だと両観点の検証役が書いている。names・キーワードは変えず、method 規則が既に基底の継承を見ている先例があるので「語彙にある入口が当たらない」側と判断されたが、学生の判断に委ねる余地がある。R2-r1-2（呼び出し形の登録を「カタログ外」とした D17 の直さない 3）とは別の形。R2-r1-3（委譲で ⊥）は別の単位。`args.get(...)` が v1 でも opaque になるのは別の既存の限界で、この単位の修正の後も不のまま。§5 の記録済みの限界と重なるものは無い。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。5 件とも D1+D2 に効く所見で、low の 3 件（R2-r3-2 / R2-r3-3 / R2-r4-1）が下がった理由は「コーパスでの出現が 0 またはまれ」であり、旧文言「D3 / D4 だけなら low」は使われていない。
- **推奨の理由**: 代表の 2 件（R2-r1-1・R2-r3-1）は high の誤 clear で D1+D2 に効く。直し方は SDK の仕様から一般に決まり（条件つき）、語彙の追加は要らず、設計の観点でも反証されていない。基準の「fix」をすべて満たすので直すことを推奨する。2.x が主流になる新しいデータ（D60）では、家族ごとに手判定とずれる向き。R2-r3-2 は Def 2 が名指しした形が構造的に 1 件も当たらない、(b) 型の食い違いで、直す差分は数行（args[-1] / キーワード）なので一緒に直すことを推奨する。R2-r3-3 は同じループの名前の解き方の問題で、R2-r3-2 / R2-r4-1 の直しと同じ import 表を使う。裸名一致への予備を残す最小の形（テスト候補の除外と unresolved_handler の件数記録）で直すのが安全。R2-r4-1 の別名の半分は scope.lookup を使う同じ直しで済むので直す。サブクラスの半分は、コーパスで 0 件のまれな書き方であること、入口規則の拡張かどうかが境界であること、仮引数を渡す形で素朴に直すと誤警報になる反例（ce_r4_1）があることから、限界として記録する（O42 以降）ことを推奨する。どれを採っても解決率・ユニット数が増える向きなので、CLAUDE.md の敵対的レビューと compare_scans での 1 件ずつの確認が要る。
- **所見**:
  - R2-r1-1: 代表（宣言側）。high の誤 clear で、D1+D2 に効く。snake_case を版で条件づけて読む（>=2.0 なら宣言、<2.0 なら malformed、決まらなければ D_unknown）。直す。D48 / 仕様書 322 行目との食い違いは、D 番号と逸脱の記録で扱う（snake_case の ToolAnnotations（read_only_hint= / destructive_hint=）は mcp>=2.0 では protocol に届く宣言なのに、版を見ずに常に D_malformed（⊥）に）
  - R2-r3-1: 代表（値側）。high の誤 clear（v2 低レベル形の 3-a 行が矛から不へ落ちる）。_seed で第 2 位置に CallToolRequestParams の Obj を種付けする。直す。検証役の複製で、v1 は不変・反例 10 余りでも verdict が不変と確かめてある（mcp 2.x 低レベル（Server(on_call_tool=)）のハンドラでは `params` を裸の Atom として種付けするため `params.arguments[...]` が MODEL/opaque(unresolve）
  - R2-r3-2: 同じ原因（SDK の署名を読まない）が入口側に出たもの。low の数え落とし。handler はキーワード、無ければ args[-1] から取る。args[2] だけにすると 2 引数形（ce_r3_2）が消える。小さい差分なので直す（`add_request_handler("tools/call", ...)` の入口規則が SDK の署名と合わず一度も当たらない: mcp 2.x は全リリースで `(method, params_type, handler)` の ）
  - R2-r3-3: 同じ原因がハンドラの名前の解き方に出たもの（import 表を捨てている）。low の誤警報。一意に解けるときだけ絞り、解けなければ裸名一致に落としてテスト候補を外し、partial / lambda は件数を記録する最小の形で直す。予備を消すと star import（ce_r3_3）が消える（`Server(on_call_tool=h)` のハンドラを裸の末尾名で木全体から引く（呼び出し元モジュールの import 表 `scope` は作って捨てている）ので、tests/ の同名の test double や無関係な同名関数）
  - R2-r4-1: 同じ原因が構築子の照合に出たもの。low の数え落とし。別名 import の半分は同じ scope.lookup で直す。サブクラスの半分はコーパスで 0 件、入口規則の拡張かどうかが境界、素朴に直すと誤警報の反例（ce_r4_1）があるので、限界として記録することを推奨（R2-r4-1 [R2] mcp 2.x 低レベルの入口照合が書かれた呼び出し名の末尾 `Server` にしか当たらず、`Server` のサブクラス（`FsServer("fs", on_call_tool=h)` / `super()）

### U40 呼び出し形の登録（tool(...)(fn) / add_tool / ToolSpec）が入口にならない（段階 B・重大度 高・推奨 一部直す）

解析器がツールを見つけるのは「@mcp.tool(...) を関数の上に付ける」書き方と「特定クラスのメソッド」の 2 通りだけです。同じ登録を普通の関数呼び出しで書いた形、つまり mcp.tool(...)(fn)、self.mcp.tool()(self.m)、mcp.add_tool(fn, annotations=...)、それに gptme の ToolSpec(name=..., execute=fn) は、どれもツールとして数えられません。ツールも宣言も記録に残らないまま消えます。readOnlyHint=True と書いたツールがファイルを消していても矛盾が 1 件も出ないので、向きは数え落としで、宣言を持つツールでは誤 clear（見逃し）になります。gptme の ToolSpec は規則表にはあるのに、実装が 1 行もありません。

- **宣言**: D1 / D2 / D3 / D4 / tooling　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 要　**scripts/ だけで直る**: いいえ
- **根本原因**: `find_units` が decorator と method の 2 形しか実装しておらず、関数を実引数として渡す呼び出し形の登録を入口にしない: `mcp.tool(...)(fn)` / `mcp.tool()(fn)` / `self.mcp.tool()(self.m)` / `mcp.add_tool(fn, annotations=...)` と、ENTRY_RULES に規則がある gptme の `spec_object`（`ToolSpec(name=..., execute=fn)`。`find_entry_rule` も未使用）はどれもユニットにならず、ツールが宣言ごと記録なしに消える。
- **コードの場所**: authgap/entries.py:376-476 find_units, authgap/catalog/entries.py:87, 129, 181 ENTRY_RULES（mcp.tool / spec_object）
- **重大度の根拠**: 代表は R2-r1-2 で、探索役 high / 設計 medium / 一般性 high の中央値 high。消えるのはユニットごと（その宣言も含む）なので、D1〜D4 の判定がすべて落ちる。この書き方だけで登録するサーバは木ごと消える。数は探索役と検証役が corpus で確かめたものだけを書く。v2-bwu1234__rag-toolkit は MCPServer と server.add_tool だけで登録しており、run20 のユニットは 0。v2-benjaminwalkerbond__auto_grocer は呼び出し形の登録 26 件（探索役の数えでは約 20 件が readOnlyHint: True）がユニットに無い。呼び出し形 x.tool(...)(fn) は 3 木、非テストの .add_tool( は 8 木（どちらも探索役の grep）。最終評価のデータでの件数は未測定。R2-r5-3 は medium（中央値。探索役 medium / 設計 low / 一般性 medium）。gptme の ToolSpec は MCP 宣言を持たず D=⊥ なので、D1〜D4 の行は作らない。v2/v3 の 200 木に gptme の import は 0 件。影響は F0a の app 母集団の数え落とし（w-gptme__gptme の 38 登録が 0 ユニット）と、論文の「入口 14 形」の説明が事実と違うこと（review_plan §1 (b)）。
- **直し方（一般に正しいか: 条件つきである）**: (A) mcp.tool(...)(fn) / mcp.tool()(fn) / self.mcp.tool()(self.m)。語彙にある名前 mcp.tool の別構文で、ENTRY_RULES は変えない。根拠は 2 つ。PEP 318 で @d(...) def f は f = d(...)(f) の糖衣であること。mcp 1.30.0 の FastMCP.tool も 2.2.0 の MCPServer.tool も、def decorator(fn): self.add_tool(fn, ...) を返すだけであること。直し方: 木の全 ast.Call のうち、func が Call で、その func の dotted 名が _match_decorator に当たるもの（require_positional のある規則は同じ構造条件で見る）について、位置引数 0 をユニットにする。annotations= / name= は外側の tool(...) のキーワードから、既存の _read_annotations / _kwarg_str で読む。二重登録は find_tools_list_units と同じ (module, qualname) の registered 集合で防ぐ。
【一般性の観点の反例（素朴な直し方で壊れる）】所見の fix_sketch どおりに位置引数 0 を index.lookup_function（末尾名の索引）で引くと壊れる木がある（cx_r1_2_extern）。b.py が木の外の vendor_search_lib.search を mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))(search) で登録し、無関係な a.py が同名の危険な search を定義している木。今は 0 ユニットで正しい。素朴な直し方では a.search が readOnlyHint 付きの偽ユニットになり、os.remove に contradiction:D1 の誤警報が出る。
【避ける条件】(1) 位置引数 0 の Name は「登録文のあるモジュールのスコープ」（module_scope と import 表）で引く。木外を指せば採らない。木内モジュールなら resolve_import_module / resolve_module_strict で厳密に解く（D17 改訂 2/3、D61 G3 条件 1 と同じ規律）。(2) self.<attr> は囲むクラスの中だけで厳密に解く。(3) 解決できない引数は採らない。Lambda、partial、ループ変数、Tool.from_function(fn) のような呼び出し式がこれに当たる（数え落としのまま残し、誤警報は作らない）。(4) def register(mcp): mcp.tool()(fn) のような入れ子の登録も落とさない（入れ子 def の @mcp.tool を拾う既存方針と同じ）。jlowin の mcp.tool(fn) や wrapped = mcp.tool(...)(fn) も同じ経路で読める。
【設計上の注意】f0a_checks.md:1185/1205/1265 は、tool("x")(fn) の呼び出し形（CrewAI、claude_agent_sdk）を「カタログ外の形」に分類している。直すなら、D17「直さない 3」の分類を改めることになる。D17 自身が「拡張は指紋凍結前に標本外の根拠（公式文書）で」と書いており、SDK のソースと PEP 318 はその根拠に当たる。必要なのは D 番号の決定と、prereg の逸脱記録。
(B) mcp.add_tool(fn, annotations=...)。add_tool は ENTRY_RULES の names に無い名前なので、入口の規則の追加（月 3 凍結、O39、review_plan §2）に当たる。entry_catalog のハッシュも変わる。技術的には (A) と同じ条件で一般に正しく直せる（SDK の登録の本体そのもの）。それでも採否は語彙の追加として学生が決める。直さない場合は O42 以降に件数つきで限界として記録する（rag-toolkit はサーバ丸ごと 0 ユニット）。
(C) gptme spec_object。規則は凍結物の中に既にあり（catalog/entries.py:181）、git log -S で見ると初回コミットから実装が無い。直し方: ast.Call の被呼び出し名を import 表と resolve_import_module で解き、gptme.tools.base.ToolSpec と、再公開の gptme.tools.ToolSpec（gptme/tools/ の 1 モジュールと下流の書き方）の両方を受ける。execute= が Name / Attribute で、木内の FuncDef に解けるものだけをユニットにする。ユニットは framework gptme、entry_kind spec_object、tool_name は name= の文字列定数、params は全仮引数 MODEL。
【避ける条件】(1) 裸名 ToolSpec の末尾一致にしない。rag-toolkit（handler=）、tg-note、nanodistill、salesagent、OpenHands の ClientToolSpec は別のクラスで、当たると MCP 母集団の分母が動く。import 元で照合するのは規則の文面（末尾一致）からの精密化なので、逸脱として記録する。(2) confirm は MODEL のまま残す。外すには R2 例外語彙（月 3 凍結）の追加が要る。(3) find_tools_list_units より前に置き、registered に入れて二重登録を防ぐ。(4) execute=create_mcp_execute_function(...) のような呼び出し式は採らない。(5) gptme の tests/ の 36 スタブからも ⊥ ユニットが出る。今もテスト由来のユニットを数えているので方針とは一貫する。直さない場合も、Def 2 の gptme、catalog_map の「14 形」、sampling.md の gptme 選定根拠を「13 形を実装、spec_object は未実装」に直す。放置はできない（規則 4）。
共通の手順: ユニットと行が増える向きの変更なので、敵対的レビューを通す。取り直すのは scan_v2_run21 と w-gptme。compare_scans / lost_units / diff_effects で突き合わせ、(C) で scan_v2 が不変であることも確かめる。
- **記録済みの限界・決定との重なり**: 設計の観点は R2-r1-2 を「記録済みの限界」として反証した（refuted=true, confidence 0.7）。根拠は 3 つ。D17「直さない 3」（decisions.md:1636-1640、カタログに無い形は取りこぼしとして件数を報告し、拡張は凍結前に標本外の根拠で行う）。f0a_checks.md:1185 / 1205 / 1258 / 1265 が、tool(...)(fn) と ToolManager.add_tool を「カタログ外の形」「analyzer_correct」に分類していること。EntryRule.kind=decorator は認識の形がデコレータに限られ、entry_catalog にハッシュされていること。ただし設計役自身も迷いを書いている。x.tool(...)(fn) 半分は「語彙にある入口が当たらない」（review_plan §2 の sink の例外の類推）とも読め、ENTRY_RULES を変えずに直せるので候補に戻せる。add_tool 半分は names の追加なので戻らない。一般性の観点は反証せず（confidence 0.85）、x.tool(...)(fn) を review_plan.md:28 の「語彙にある名前が当たらない」に当たると判定した。R2-r5-3 は設計・一般性の両方が反証せず（既知の限界にも設計判断にも当たらない。逆に BRIEF:203、catalog_map、decisions.md:1788、sampling.md:26 は実装済みとして扱っている）。O39（入口規則の追加凍結）には add_tool だけが当たり、spec_object と x.tool(...)(fn) は当たらない。参考: preregistration.md:304 は宣言の数え方（族 3）で、被呼び出し名の末尾が add_tool のものを既に数えている。枠の定義は add_tool 形の宣言を知っていたことになる。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 形跡無し。R2-r1-2 の設計役が medium にした理由は「特定の登録構文でだけ起きる」で、D3 / D4 は関係しない。R2-r5-3 の設計役が low にした理由は「最終評価の母集団に gptme の ToolSpec 形が現れず、⊥ で D1〜D4 のどの行も作らない」で、D3 / D4 だけに効くことを理由にした格下げではない。
- **推奨の理由**: 単位の中に、推奨の基準で分かれるものが混ざっている。(A) mcp.tool(...)(fn) / self.mcp.tool()(self.m) は high で、語彙の追加が要らない（ENTRY_RULES の名前 mcp.tool のまま）。一般性の観点で、スコープ解決の条件つきで一般に正しいと確かめられている。設計の反証は D17 の分類によるが、D17 自体が「凍結前に標本外の根拠で拡張」を予定しており、PEP 318 と SDK のソースはその根拠を満たす。したがって fix（D 番号と逸脱の記録つき）。(C) gptme spec_object は medium で、凍結済みの規則が一度も実装されていない (b) の食い違い。語彙の追加は要らず、import 元で照合する条件つきで一般に正しいので fix。直さないなら「14 形」の説明の訂正が必須。(B) mcp.add_tool は、技術的には同じ条件で正しく直せる。ただし ENTRY_RULES の names への追加（月 3 凍結の語彙追加）に当たるので、基準では record_as_limitation とし、件数つきで O42 以降に記録する。add_tool は SDK の登録の本体そのもので、rag-toolkit はサーバが丸ごと消えるので、採るかどうかは学生が逸脱として判断する余地が大きい。
- **所見**:
  - R2-r1-2: 代表（high、D1+D2）。呼び出し形 x.tool(...)(fn) / self.mcp.tool()(self.m) と add_tool の 2 つの表れを含む。設計の観点は D17「直さない 3」を根拠に記録済みの限界として反証し、一般性の観点は反証しなかった。前者（x.tool(...)(fn)）は fix の対象で、語彙の追加は要らず、スコープ解決の条件がつく。後者（add_tool）は names への語彙追加に当たるので、限界として記録する側（採否は学生）。（デコレータ構文でない登録（mcp.tool(...)(fn) / mcp.tool()(fn) / self.mcp.tool()(self.m) / mcp.add_tool(fn, annotations=...)）を入口にせず、ツール）
  - R2-r5-3: 同じ原因の別の表れ（medium、規則との食い違い）。find_units に spec_object の枝が無く、find_entry_rule も未使用で、gptme の ToolSpec(execute=fn) が 1 つもユニットにならない。設計・一般性の両観点とも反証しなかった。D=⊥ なので D1〜D4 の行は動かないが、「入口 14 形」の説明が偽になる。fix の対象（import 元で照合、再公開形も受ける、confirm は MODEL のまま）。直さない場合も文書の訂正は必須。（ENTRY_RULES の gptme 規則（`spec_object` / `ToolSpec`）を実装しているコードが無い: `find_units` は decorator / method の 2 形しか扱わず（`find_entr）

### U04 列（Seq / Argv）の位置の操作が Python の意味を保たない（段階 C・重大度 中・推奨 一部直す）

解析器は、コマンドのリスト（例: ["git", "log", x]）の要素ごとに、どれが定数でどれがモデルの入力（MODEL）かを覚えています。ところが、リストの要素の位置を変える書き方（`cmd[0] = x` の置き換え、`del cmd[0]`、`base[:]` による複製、`a, *rest = ...`、17 個以上の要素、`"git log".split() + [x]`）を Python と違う意味で扱うため、先頭の要素（実行するコマンドの名前 = argv0）を取り違えます。取り違えの向きは書き方で 2 つに分かれます。本当はモデルが決めるコマンドを定数と見て矛盾を見落とす向き（誤 clear。添字代入・del・拡張アンパック・17 個超え）と、本当は定数 "git" なのにモデル由来と見て矛盾を出しすぎる向き（誤警報。スライス複製・split）です。影響するのは D1 / D2（SPAWN の判定）です。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 列の値（elems + tail）への操作が Python の位置の意味を保たない: 添字代入 `cmd[0] = x` は置換でなく `_append_tail` で末尾に足す、拡張アンパック `a, *rest, c = seq` は `*rest` に列全体を束縛し後ろの対象を左から数える、`del cmds[0]` は無視（`ast.Delete` は no-op）、スライス `base[:]` / `base[1:]` は `_ev_Subscript` が要素の join（Atom）に潰す、K = 16 を超える要素は tail に畳まず捨てる（`_ev_List` / `_ev_Dict` / `_concat` / Path の `/`）、tail 付きの列の `+` は後続の要素を index 0 に置き、`str.split()` / `shlex.split()` は先頭の定数トークンを失う（`Seq((), tail=全体)`）。どれも argv0 / 要素の取り違え（定数 ↔ MODEL）になる。
- **コードの場所**: authgap/val/engine.py:445-473 _bind（Subscript / Tuple・Starred）, authgap/val/engine.py:391-392 _exec_stmt Delete, authgap/val/engine.py:681-698 _ev_Subscript（Slice）, authgap/val/engine.py:596-620 _concat / _ev_List / _ev_Dict, authgap/val/engine.py:2560-2580 _append_tail, authgap/val/engine.py:887-937 _apply_transfer（split）, authgap/catalog/transfers.py:66-71 str.split / shlex.split 行
- **重大度の根拠**: 単位の重大度は、中の所見のうち最も重いもので決めた。R1-r1-7 は 3 観点とも medium で、例外や opaque の印を残さずに MODEL が消える（OP/resolved の誤 clear）。v2 で検証役（一般性）が AST で数えた値は、関数内の 17 要素以上の列リテラル 1,290 件で、そのうち溢れた側に定数でない要素を含むのが 329 件、argv の形のものが 137 件（14 木）。R4-r1-9 は medium / medium / low で、v2 run20 の主指標への影響は 0 件（CONTRADICTION 191 件に SPAWN は 0 件）。ただし最終評価は別の新しいデータ（D60）なので、実際の頻度は未測定。R1-r1-9 / R1-r3-6 / R1-r4-15 / R4-r3-3 は low で、どれもまれな書き方か、v2 での観測が 0 件（R4-r3-3 は v2 で該当 8 関数。どれもデータファイルで、宣言つきのツールは 0 件）。旧文言「D3 / D4 だけなら low」で下がった形跡は無い（全件 D1+D2 で、low の理由は頻度と向き）。
- **直し方（一般に正しいか: 条件つきである）**: 原則: 列の位置を「正確に分かっている（tail が無い）」ときだけ Python の意味どおりに動かす。位置が決まらないときは要素を捨てずに tail へ join し、特定の位置を読むときは opaque を合流する。**個別に直すと、別の所見の欠陥が新しい誤 clear として広がる**（R4-r3-3 の試作 A と R1-r3-6 の ce6 で実証済み）。そのため、変異の操作と `_concat` を先に、または同時に直す。試作 C（scratchpad/verify/R4_hm_1/apply_patch.py の AG_VARIANT=C。リポジトリは未変更）で pytest の失敗 0、check_gates 23/23、反例 5 形と再現 4 形が期待どおりになることを確かめてある。

(1) 添字代入 `_bind` Subscript（R1-r1-9）: 受け手が Seq/Argv で、添字が範囲内の int 定数（負の添字を含む）のときだけ、その位置を置き換える。Map や形の分からない受け手は今の合流のまま。**素朴な直し方で壊れる反例**: 所見の素案「定数でない添字は全要素と tail に join」は expand_loop（`for i,a in enumerate(cmd): cmd[i]=os.path.expanduser(a)`）で argv0 が 'ls'⊔MODEL になり、新しい誤警報を出す。**避ける条件**: 定数でない添字とスライス代入は今の `_append_tail` のままにする（R1-r1-9 の検証役）。試作 C は「全位置と tail に join」を採っており、2 人の検証役の意見が食い違っている。両立させる案（全位置に join したうえで値に opaque(dynamic) を合流し、判定を 不 に保つ）は未検証。付記: 今は `cmd=[exe,'-l']; cmd[0]='ls'` が誤警報になっている（replace_const）。この直しで逆向きの誤りも直る。

(2) `list.insert(i, v)`（未記録。R1-r3-6 と R4-r3-3 の反例で見つかった）: 非負の int 定数なら位置 i に入れる（長さを超えれば末尾、tail があれば tail に合流）。それ以外は全位置と tail に join する。

(3) `del x[i]`（R1-r4-15）: 位置が分かっている列で、範囲内の定数添字のときだけ要素を消す。tail つきの列や定数でない添字では、`note_opaque` を manifest に書くだけでは行の確度に伝わらない（verdict.py:151-156）。その変数の値を opaque(dynamic) に落とすほうが正しい（添字がモデル由来なら、モデルが argv0 を選べるため）。`del name` は env の鍵を消さず、Unknown を束縛する（消すとモジュール水準の値に落ちる）。反例として試した `del d[key]` の後の矛と、分岐合流の矛は、直した後も変わらない。

(4) reverse / sort / pop / remove / clear: 位置を捨てて `Seq((), join)` にする。

(5) スライス `_ev_Subscript`（R4-r3-3）: step が None で、lower / upper が None か非負の int 定数のときだけ `type(shape)(elems[lo:up], tail)` を返す。tail を保つのは up が None か len を超えるときだけ。主体・確度・root は残った要素から計算し直す。それ以外（負の境界・定数でない境界・step つき）は `Seq((), _element_of(base))`。**反例**: step を見ないと `parts[::-1]` の argv0 が逆になり、誤 clear になる。

(6) `_concat`（R4-r3-3 の (f) と R4-r1-9 の (b)）: 左の列に tail があるときは、右の要素と tail をすべて左の tail に畳む（今は右の要素を index 0 以降に置き、`a.tail or b.tail` で右の tail を落としている）。**反例**: 素案の (b) だけを入れると、`"git log".split() + extra` と `os.environ["TOOL_CMD"].split() + extra`（extra は list[str] の仮引数）が、今は正しく 不 なのに MODEL/resolved の矛（新しい誤警報）になる。**避ける条件**: 左の tail が MODEL でないときは、MODEL 要素を tail に畳む際に opaque(unresolved) を合流する（O33: 選べる = MODEL かつ resolved）。あわせて (7) を同時に入れる。

(7) split（R4-r1-9 の (a)）: 対象は引数なしの `str.split()`（sep=None、maxsplit なし）と `shlex.split` に限る。確度 resolved の定数の接頭辞（`Value.const` / `is_literal()`）に「空でないトークン + 空白」があるときだけ、`Seq((OP定数 token0,), tail=全体)` にする。**条件**: transform 名 "str.split" を共有する `rsplit(maxsplit=1)` は、第 0 要素に MODEL が入りうるので対象外（今の矛を保つ）。明示の区切り `split(",")` も対象外。shlex は、接頭辞に \ ' " を含むものを除き、shlex の空白の集合（NBSP を含まない）で判定する。`str.split→[0]` の alias_facts（仕様書 513）は保つ。先頭が定数でない `f"{prog} {x}".split()` と、全体が MODEL の `cmd.split()` は今までどおり矛。**消える「偶然の真の矛」**: `f"python3 -c {code}".split()` や `f"sudo {cmd}".split()` は直すと 不 になる。これはリスト形の `["python3","-c",code]` が既に 不 なのと同じ §7.1 の規則の限界なので、O35 に併記して記録する。

(8) 17 要素以上（R1-r1-7）: `_ev_List` / `_ev_Dict` / `_concat` / Path の `/` で、K を超えた分を `value_join` で tail に畳み、主体と root は全要素から計算する（`_widen_value` と同じ）。**反例**: 素案だけだと、溢れた位置やキーを定数で読む書き方（`cfg["cmd"]` の "cmd" がソート後 17 番目、`cmd[16]`）で tail = join(定数, MODEL) が resolved のまま返り、今は正しい 不 が矛（誤警報）になる（map_literal_read / seq_literal_index）。**避ける条件**: `_ev_Subscript` で、定数のキーや添字が保持した entries / elems に無く tail があるときは、opaque（cap など、既存の語彙）を合流して返す。または (8') リテラルの構築子と直線のコードの連結には K を当てない（K はループの widening のためにある）。(8') にすると、今のコードの鏡像の誤警報（map_model_in_head）も正確に決まる。

(9) 拡張アンパック（R1-r3-6）: 素案の「右から数える / `*` にスライスを渡す」は、(1)(2) が直る前には insert / 添字代入の後の列（ce6 の 3 形）で新しい誤 clear を作る。保守的な案（`*` の対象を `Seq((), join)`、`*` より後を `_element_of`）は MODEL を落とさないが、argv0 が列全体の join になる。これは CLAUDE.md が挙げる落とし穴「形だけ残すと argv0 のリテラルが列全体の主体になる」そのものである。正確な版は (1)〜(4) の後で、tail の無い列に限る。

手順: (5)(7)、(1) の定数添字、(3) の定数削除は、MODEL/resolved を OP/resolved にする（clear を増やす）向きなので、CLAUDE.md の敵対的レビューを通す。そのうえで diff_effects.py と compare_scans.py を使い、消えた矛を 1 件ずつ確かめる。
- **記録済みの限界・決定との重なり**: 設計の観点で反証された所見は無い（6 件とも refuted=false）。近いが根本原因が別の記録: O35（argv の要素の中をオプション名と値に分ける話）、O41（`shlex.quote` した固定のシェル文字列）、§9.4 末尾「SQL 以外の slot は接頭辞を読まない」（Str の slot の判定の規則で、split の要素境界の話ではない）、K1（モジュール水準のリスト。`BASE[:]` はモジュール水準なら D17 改訂 4 で opaque → 不 のままで、判定は変わらない）、O18 / K6（行数の cap・深さ）。逆に、この単位の欠陥を誤りと定めている記録: D17 改訂（decisions.md:1661-1665）と CLAUDE.md の落とし穴「列の分岐合流で要素を捨てない」（argv0 のリテラルが列全体の MODEL になる退行を直したもの。test_branch_join_keeps_argv0_literal で固定）、仕様 §2.6 / ir.py:253 の「K を超えた分は tail に畳む」（R1-r1-7 はこの書いた規則と実装の食い違い）。誤警報の向き（R4-r3-3 / R4-r1-9）は、D19(2) では「凍結を妨げない」とされている。R4-r1-9 を直すと消える偶然の真の矛（`python -c` / `sudo` などのラッパに MODEL を渡す形）は、O35 の領域の規則の限界として併記が要る。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。6 件とも影響は D1+D2 と申告されている。low とした理由は、書き方がまれなこと、v2 run20 の主指標で観測が 0 件（R4-r3-3 / R4-r1-9 の一般性の観点）、誤警報の向き（R4-r3-3）で、「D3 / D4 だけなら low」を理由にした記述は無い。ただし R4-r3-3 と R4-r1-9 の一般性の観点は、v2 / v3 での観測頻度 0 を low の根拠にしている。最終評価は新しいデータ（D60）なので、そこでの頻度は未測定である（R4-r3-3 の検証役自身が medium との境で迷ったと書いている）。
- **推奨の理由**: medium の 2 件（R1-r1-7、R4-r1-9）は推奨の基準を満たす。設計の観点の反証は無く、語彙の追加も要らず、検証役の条件つきで一般に正しい直し方がある。R4-r1-9 の split の直し（先頭に定数の要素を立てる）を単独で入れると、split で作った列に `cmd[0] = x` や `insert(0, x)` をした形で argv0 が 'git' に残り、今は偶然正しい矛が消える。これは R4-r3-3 の試作 A と R1-r3-6 の ce6 で実証された、同じ型の新しい誤 clear である。そのため、low の R1-r1-9（定数添字の置き換え）、R1-r4-15（定数添字の del）、未記録の insert の位置、`_concat` の tail の扱い（R4-r3-3 の (f)。R4-r1-9 の (b) と同じ箇所）は、直すための前提として一緒に入れる。R4-r3-3 のスライスは low だが、試作 C で一式として検証済みで、step の条件を足すだけの局所変更なので、同じ束に入れてよい。R1-r3-6（拡張アンパック）は限界として記録する。low でまれな書き方であり、保守的な直し方は CLAUDE.md の落とし穴（argv0 が列全体になる）を踏み、正確な直し方は (1)〜(4) の全部が正確になった後でしか成り立たないからである。束全体は MODEL/resolved を OP/resolved にする（clear を増やす）変更を含むので、CLAUDE.md の敵対的レビューと diff_effects.py / compare_scans.py が要る（size L）。定数でない添字の扱いは検証役の間で意見が割れている（今の追記のまま vs 全位置への join）ので、学生が決める。
- **所見**:
  - R1-r1-7: 代表（medium、3 観点とも medium、誤 clear）。K = 16 を超えた要素を捨てるので、17 番目以降の MODEL が OP/resolved として黙って消える。直す。条件: 溢れた位置やキーを定数で読むときは opaque を合流する（または、リテラルと直線のコードの連結には K を当てない）。（K = 16 を超える要素を `tail` に畳まず捨てる（`_ev_List` / `_ev_Dict` / `_concat` / Path の `/`）ので、17 番目以降の MODEL 要素が消え、`" ".join(cmd)` の）
  - R4-r1-9: 代表（medium / medium / low、誤警報）。split が先頭の定数トークンを失い、tail つきの列の + が後ろの要素を index 0 に置く。直す。条件: 引数なしの str.split / shlex.split に限り、rsplit(maxsplit) は除く。(b) は (a) と同時に入れ、左の tail が MODEL でなければ opaque(unresolved) を合流する。消える偶然の真の矛は O35 に併記する。（str.split() / shlex.split() の結果は先頭の定数トークンを失い（Seq((), tail=全体)）、さらに tail 付き Seq の + 連結が後続要素を index 0 に置くので、argv0 が定数 "git）
  - R4-r3-3: 同じ原因の別の表れ（low、誤警報）。スライス複製を 1 つの値に潰す。試作 C で一式として検証済み。その (f) の _concat の直しは R4-r1-9 の (b) と共有する。束に入れて直す。条件: step が None で、境界が None か非負の定数のときだけ位置を保つ。（スライスで複製した定数の列（`cmd = base[:]` / `base[1:]`）に MODEL を append / insert / extend / 添字代入すると、`_ev_Subscript` が Slice を要素の joi）
  - R1-r1-9: 同じ原因の別の表れ（low、誤 clear。replace_const の形では誤警報も出す）。添字代入が末尾への追加になる。R4-r1-9 と R4-r3-3 を安全に直すための前提として、定数添字の置き換えだけを直す。定数でない添字は今の追記のまま（join にすると expand_loop が誤警報になる）。（`cmd[0] = exe` のような添字代入が要素を置換せず列の末尾に追加する（`_bind` Subscript → `_append_tail`）ので、argv0 がリテラルのまま残り MODEL の argv0 が不になる）
  - R1-r4-15: 同じ原因の別の表れ（low。向きは値の水準では誤 clear、判定の水準では数え落とし）。del が no-op になる。前提として、位置が分かっている列の定数添字の削除だけを直す。それ以外は値を opaque(dynamic) に落とし、`del name` は Unknown を束縛する。（`del cmds[0]` を無視する（`ast.Delete` は no-op）ので、`cmds = ["ls", cmd]; del cmds[0]; subprocess.run(cmds)` の argv0 が消したはずの定数 'l）
  - R1-r3-6: 同じ原因の別の表れ（low、誤 clear、まれな書き方）。拡張アンパックで `*rest` に列全体が入り、後ろの対象を左から数える。限界として記録する（素案は ce6 で新しい誤 clear を作る。保守的な案は argv0 が列全体になる落とし穴を踏む。正確な案は (1)〜(4) が済んだ後で、tail の無い列に限る）。（拡張アンパック `a, *rest, c = seq` で `*rest` に列全体が束縛され（スライスではない）、`*` より後の対象が左からの添字で割り当てられる（右端から数えない）ので、`_, *rest = ["prefix", e）

### U05 コンテナの要素の読み（_element_of と辞書）（段階 C・重大度 中・推奨 一部直す）

解析器が「リストや辞書の中身のどれか 1 つ」を読む関数（_element_of）に誤りが 3 つ重なっています。(1) 長さの決まらないリスト（例: `cmds = [cmd]` の後で if の中だけ `append("rm ...")`）を for や `cmds[i]` で読むと、後ろに足した定数だけを返し、先頭にあるモデル由来の `cmd` を捨てます。このため「矛盾あり」が「不明」に落ちます（誤 clear）。(2) 辞書を `for k in d` / `", ".join(d)` / 内包で回すと、Python ではキーが返るのに、解析器は値を返します。定数キー・モデル由来の値の辞書で列名を組む INSERT は「矛盾あり」になり（誤警報）、モデル由来のキーは消えます（誤 clear）。(3) `{**base, "k": v}` の base 側の項目を展開しないので、`d["exe"]` の定数 'ls' がモデル由来の値として扱われ、誤警報になります。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 反復・非定数の添字・アンパックで使う `_element_of` が、tail のある列 / 辞書では tail だけを返して既知の elems / entries を捨て、辞書（Map）では Python がキーを返す場所（`for k in d` / `join(d)` / 内包 / `yield from` / アンパック）に値の join を返す。辞書表示の `{**base, ...}` は `_ev_Dict` が base の項目を平らにせず `"<dynamic>"` の 1 項目に置く（非定数キーの式も評価しない）ので、定数キーの読み出しが全値の join になる。
- **コードの場所**: authgap/val/engine.py:2512-2532 _element_of, authgap/val/engine.py:2290-2298 _items_of, authgap/val/engine.py:613-620 _ev_Dict, authgap/val/engine.py:408-421, 456-464, 670-678, 700-717 反復・アンパック・yield from・内包の束縛
- **重大度の根拠**: 代表の重大度は medium とした。R1-r4-2 は探索役・設計・一般性の 3 意見がそろって medium（向きは誤 clear。D1 は spawn_model → spawn_command の不、D2 は fs_writeout_model_path → fs_writeout の不、モジュール水準の辞書では NET 行そのものが消える）。R1-r5-4 も 3 意見そろって medium（誤警報が主で、MODEL キーの辞書では root の無い誤 clear になる）。R1-r4-7 は 3 意見そろって low。base 側の定数を argv0 や HTTP メソッドの slot に使う形でしか起きないため。件数は構文上の上限だけが数えられている（v2 の 99 木、到達性は見ていない）。R1-r4-2 は「if の中で append / extend してから for」が 195 箇所 / 39 木、「非定数の添字で読む」が 137 箇所 / 33 木。R1-r5-4 は `sep.join(辞書)` が 6 箇所 / 4 木、`for k in 辞書` が 36 箇所 / 12 木、内包の `for k in 辞書` が 49 箇所 / 20 木。R1-r4-7 の件数と、v2 の CONTRADICTION が実際に何件動くかは未測定。3 件とも D1+D2 に効くので、旧文言（D3 / D4 だけなら low）は関わらない。D3 / D4 への効き（例: spread した辞書の url が宛先になる形）は誰も調べておらず、未測定。
- **直し方（一般に正しいか: 条件つきである）**: 読み方を「どれか 1 つの値」「位置の分かる値」「キー」の 3 つに分け、辞書表示の評価を言語の意味どおりにする。3 つとも検証役が一般に正しいと判定したが、それぞれに条件がある。

[A] R1-r4-2（列の tail）
- 反復・内包・`yield from`・非定数の添字（`_exec_loop` :421、`_ev_ListComp` / `_ev_DictComp` :703 / :717、`_ev_YieldFrom` :672、`_ev_Subscript` の非定数添字 :691）では、`_element_of` を join(elems…, tail) にする。elems が空なら tail だけ。tail は「添字 >= len(elems) の要素の要約」だからで、`_items_of` と effects.py の `_first_element` はすでにこの規約で書かれている。
- 【素朴な直し方で壊れる反例（検証役の試作 p2）】所見の fix_sketch どおりに `_bind` の Tuple の余りと `_ev_Subscript` まで同じ join にすると、位置の分かる読みが誤警報になる。f2_positional の 2 例がそれで、`cmds = [cmd]; if cleanup: cmds.append("rm -f /tmp/x.lock"); subprocess.run(cmds[1], shell=True)` と `first, second = cmds; os.system(second)` は、どちらも Python では定数か例外にしかならない。今は OP 'rm -f …' で不（正しい）なのに、p2 では MODEL の spawn_model の矛になった。
- 【避ける条件】位置の分かる読みは tail のまま残す（tail が無ければ従来どおり join）。対象は、定数の int 添字で len(elems) 以上のもの、`_bind` の Tuple で位置 i >= len(elems) のもの、Map の定数キーが外れたとき。検証役の試作 p2b はこの条件で、所見の 5 ユニット（loop / index / comp / ifexp / write_loop）を期待どおり spawn_model / fs_writeout_model_path にした。f2_positional の 2 ユニットと対照の 5 ユニットは変わらず、pytest は対照と同じ 741 passed。
- 受け入れる精度の代償（誤りではない）: f2_opaque_prefix2 の `cmds = [ext()]; if extra: cmds.append(cmd); for c in cmds: os.system(c)` は、今は tail だけを読んで偶然 矛 になっている。直すと MODEL/opaque の不（spawn_model_opaque）に動く。同じ選択を IfExp で書いた形と同じ結果で、D57 §9.3 が受け入れた「不明への移動」にあたる。
- 【直らない部分】map_tail（`CLIENTS[name].request(...)`）は、この直し方では NET 行が出ない。`_opaque_deep` が足す tail は Unknown で、ir.py の `_shape_join` は Obj ⊔ Unknown を Unknown にするため、受け手の型が戻らない。直すには「Obj と Unknown の tail を合流しても型を保ち、確度だけ落とす」という格子の規則の変更が要る。これは解決率を上げる向きの別の設計判断で、D35(a) の Obj ⊔ None と違って Unknown 側は dead ではない。したがって別に敵対的レビューが要る。A には含めない。

[B] R1-r5-4（辞書の反復はキー）
- `_keys_of(Map)` を足す。定数キーは Atom(const=key) の OP/resolved にし、tail があれば opaque の tail を合流する。これを使うのは反復の側だけにする: `_exec_loop` の iter、内包の generator、`_items_of` のうち `sep.join` と `extend` の引数、`_ev_YieldFrom`、`_bind` のアンパック、`_elements` の Map の枝。
- 【条件 a】値のまま残す場所: `_ev_Subscript` の非定数キー、`os.environ` の書き込みの読み戻し（:1164-1170）、`_items_of` の `dict.update(m)` 側（:1191-1194）、`.values()` / `.items()`（R1-r3-7）。`_items_of` を一律キーにすると update が壊れる。
- 【条件 b】`_ev_Dict` で非定数キーの式を評価し、その Value を Map に残す。今はキー式を評価すらしないので、`{tag: "echo hi"}` の MODEL の根 `tag` がどこにも残らない。これを直さないと model_keys_lost は直らない。
- 【素朴な直し方で壊れる反例（ce4_dict_iter の dictcomp_keys）】`opts = {n: user_a for n in names}; for k in opts: os.system(k)` は、今は値を経由して偶然 MODEL の矛になっている。DictComp のキー式（MODEL の `names` 由来）を記録しない直し方だと OP に落ち、新しい誤 clear になる。
- 【避ける条件】DictComp のキー式、`{**a}` の展開（`_keys_of(a)`）、添字代入 `d[k] = v` の k も記録する。キーが記録できない Map（tail だけのものなど）は OP と言わず、opaque の Unknown に落とす。
- 直した後も変わってはならない形: 値が届く `for k in opts: os.system(opts[k])` と、`{tag: "echo hi", "x": user_a}` の添字読み。どちらも MODEL のまま残ること。`**kw` と `os.environ` の反復は Map ではないので影響しない。`a, b = {...}` のアンパックは Python ではキーなので、直るのが正しい。R1-r5-3 の `list(x)` / `set(x)` と組み合わせるときは、x が Map ならキーを使う。

[C] R1-r4-7（`{**base, ...}`）
- 【素朴な直し方で壊れる反例（patched7）】spread する Map の entries をそのまま平らにすると、`base = {"exe": "ls", key: target}; d = {**base}` の `d["exe"]` が OP 'ls' の不になる。これは新しい誤 clear で、今は正しく spawn_model の矛になっている（key == "exe" なら後勝ちでモデルがプログラムを選べる）。
- 【避ける条件】平らにするのは、spread する Map に "<dynamic>" の項目も tail も無いときだけにする。そうでないとき（Map でない値、形の分からない `**opts` を含む）は、spread の値と非定数キーの値を、それより前にある定数キーすべてに合流する（後勝ちを守った健全な形）。
- この健全な形は、検証役が見つけた今の実装の別の誤 clear も同時に直す。`{"exe": "ls", **opts}` と `{"exe": "ls", key: target}` の `d["exe"]` が OP 'ls' の不になっている件（later_spread_overrides / direct_dynamic_key）。
- 重複キー `{"a": 1, "a": 2}` は安定ソートで先の値が勝ち、Python と逆になっている。後勝ちに直す。
- 本記録者がコードを読んで気づいた点（未検証）: `_ev_Dict` は entries を K=16 で切り詰めるが tail を付けない（:620）。17 項目以上の辞書リテラルでは項目が黙って消える。所見にはなっていない。

[共通]
- 解析器を変えたら `scripts/diff_effects.py` で較正対を突き合わせる。v2 の取り直しは `scripts/compare_scans.py` にかけ、消えた CONTRADICTION を 1 件ずつ見る。B と C は矛 → 内 / 不 の向きを含むので、特に注意する。
- D61 に従い、v2 の件数に合わせた例外は入れない。
- **記録済みの限界・決定との重なり**: 設計の観点は 3 件とも反証していない（refuted=false）。3 件とも、意図した決定・記録済みの限界・仕様どおりのどれにも当たらない。
- `_element_of` の「tail があれば tail」と Map の枝は、初期コミット b3aa2c8 からあるもので、D 番号の決定ではない。
- `<dynamic>` は docs に記載が無い。
- review_plan §5（O・K1〜K7 ほか）にも該当しない。

近いが根本原因が別のもの（この単位では直らない / 触らない）:
- R1-r3-4: Map の分岐合流と `update` の widening。R1-r4-7 はその fix では直らないと探索役が切り分けている。
- R1-r3-7: `.keys()` / `.values()` / `.items()` が未解決の呼び出しで MODEL/opaque になる件。B では変えない。
- R1-r5-3: `list(x)` / `set(x)` の拡張。組み合わせるときの条件だけを B に書いた。
- K6: `_opaque_deep` の深さ上限。同じ関数に触れるが原因は別。

設計の記録との関係:
- R1-r4-2 の map_tail は、D17 改訂 4（コンテナは型と主体を保って確度だけ opaque に落とす）に反している。ただし直すには格子の規則の変更が要るので、別の判断として扱う。
- opaque の先頭と MODEL の tail を持つ列が矛 → 不 に動くのは、D57 §9.3 が受け入れた精度の代償で、誤りには数えない。
- 検証役（R1-r4-7 の一般性）は `_ev_Dict` の別の誤 clear（定数キーの後ろの動的キーや `**opts` による上書きを見ない件）を見つけ、「別の所見とすべき」と書いた。ただし所見としては登録されていない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 形跡は無い。3 件とも D1+D2 に効く所見で、D3 / D4 だけに効くことを理由にした判定は無い。R1-r4-7 が low なのは、base 側の定数を判定の slot に使う形に限られるという頻度の理由で、3 意見とも同じ。
- **推奨の理由**: 直すもの: R1-r4-2 の列の部分と R1-r5-4 は medium で、言語の意味から導ける一般に正しい直し方がある（条件つき）。語彙の追加は要らず、設計の観点の反証も無いので、基準の fix にあたる。R1-r4-7 は単独なら low だが、R1-r5-4 の条件 b で `_ev_Dict` をどのみち直す。その健全な形（前の定数キーへの合流）は、未登録の誤 clear（`{"exe": "ls", **opts}`）も同時に直すので、一緒に入れることを勧める。単独で扱うなら記録でよい。

記録に回すもの: R1-r4-2 の map_tail（`_opaque_deep` の tail の後ろで受け手の型が消える件）。Obj ⊔ Unknown の格子の規則を変える、解決率を上げる別の設計判断が要るため。

注意点: B と C は矛 → 内 / 不、OP → MODEL、Unknown → 定数と、解決の向きに動く。CLAUDE.md の敵対的レビューを通すこと。Map にキーの値を持たせるには ir.py の Map の形を広げる必要があり、設計を伴う（大きさは L）。列の部分（A）だけなら 1 関数と呼び出し元の分け方で済む（S）ので、先に A を切り出して入れることもできる。
- **所見**:
  - R1-r4-2: 代表。`_element_of` が tail のある列・辞書で tail だけを返し、既知の先頭要素（MODEL の cmd）を捨てる（誤 clear。D1 spawn / D2 writeout、medium ×3）。列の部分は直す。ただし定数添字とタプルの位置 >= len(elems) は tail のまま残す条件つき。map_tail（`_opaque_deep` の Unknown tail で受け手の型が消え NET 行が無くなる）はこの直し方では直らず、格子の変更が要るので記録に回す。（`_element_of` が `tail` のある列 / 辞書で **tail だけ**を返し、既知の先頭要素 `elems` を捨てる: 長さの違う列の分岐合流（`cmds = [cmd]; if flag: cmds.append("）
  - R1-r5-4: 同じ関数の別の表れ。辞書の反復（for / join / 内包 / yield from / アンパック）で、キーの代わりに値を返す（誤警報が主で、MODEL キーでは誤 clear。medium ×3）。反復の側だけ `_keys_of` にする。`_ev_Dict` と DictComp でキー式を評価・記録する条件つきで直す。MODEL キーの回復は解決の向きなので、敵対的レビューが要る。（辞書の反復が**値**を束縛する: `_element_of(Map)` は値の join（または tail）を返すので、`for k in opts:` / `[k for k in opts]` / `sep.join(opts)` /）
  - R1-r4-7: 同じ領域（`_ev_Dict`）の別の表れ。`{**base, ...}` を平らにしないので、base 側の定数が全値の join になる（誤警報、low ×3）。単独なら記録でよい。R1-r5-4 で `_ev_Dict` を直すので同時に入れることを勧める。素朴に平らにすると誤 clear を作るため、<dynamic> も tail も無い Map のときだけ平らにし、それ以外は前の定数キーへ合流する条件つき。（辞書表示の `**` 展開 `{**base, "target": target}` を `_ev_Dict` が `"<dynamic>"` キーの 1 項目（base の Map 全体）として置き、base の項目を平らにしないので、`）

### U07 値を保つ変換の TRANSFER 行の穴（rstrip 系・str()/os.fspath/as_posix・Path を返す pathlib メソッド）（段階 C・重大度 中・推奨 直す）

解析器は「値の中身を変えない、または中身から決まる変換」を表（TRANSFER）で知っています。この表に `str(p)`、`os.fspath(p)`、`p.as_posix()`、`s.rstrip("/")`、`removesuffix`、`Path(x).expanduser()`、`joinpath`、`with_suffix`、`Path.home()`、`Path.cwd()` などが載っていません。載っていない変換を通った値は「分からない値（opaque）」として扱われます。その結果、(1) モデルが渡した値がそのままパスやコマンドになる場合でも「選べる」と言えなくなり、矛盾が不明に落ちます（D1 / D2）。(2) 定数の宛先 URL が読めなくなり、外部ホストの矛盾が不明に落ちます（D3）。localhost のときは「内」が不明に変わり、不明が水増しされます。(3) Path の形が消えるので、その後の `write_text` や `unlink` が効果として 1 行も出なくなります（D1 の矛盾が消える）。どれも主に誤 clear（見逃し）の向きに誤ります。

- **宣言**: D1 / D2 / D3　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_apply_transfer` が引く TRANSFER 表に、内容を保つ変換 `str.rstrip` / `lstrip` / `removesuffix` / `removeprefix`、恒等変換 `str()` / `os.fspath` / `Path.as_posix`（`str` は組込み名の解決にも無い）、Path を返す pathlib のメソッド（`expanduser` / `joinpath` / `with_suffix` / `absolute` / `Path.home()` / `Path.cwd()`）が無いので、MODEL/resolved の値が opaque(unresolved) に落ち（選べる → 不、宛先の定数 → 不明）、Path の受け手が Unknown になって後続の pathlib sink（write_text / unlink / mkdir）が消える。
- **コードの場所**: authgap/catalog/transfers.py:40-94 TRANSFER 行 / METHOD_TRANSFERS, authgap/val/engine.py:887-937 _apply_transfer, authgap/val/engine.py:852-885 未解決呼び出し, authgap/srcindex.py:444-453 組込み名の解決, authgap/effects.py:423 受け手型の照合
- **重大度の根拠**: 代表値は 3 件とも medium です（3 観点の中央値。R4-r1-5 は medium/medium/medium、R4-r2-3 は medium/medium/medium、R1d-r6-3 は medium/medium/low）。どれも特定のメソッド名や組込み名で起きるので、high の条件の「系統的」には当たりません。ただし `str(path)` / `Path.home()` / `expanduser()` / `base_url.rstrip("/")` はよくある書き方です。R4-r1-5 では効果行が丸ごと消えるので、見逃しに加えて数え落としにもなります。

露出について、検証役が数えたもの:
- R4-r1-5: AST で数え直すと、MCP ツール本体（深さ 0）で連鎖メソッドを使うのは 29、pathlib sink と同居するのは 5 です。v2 の宣言ありツールへの深さ 0 の影響は 0 でした。helper を含めた上界は 138 関数 / 26 木です。探索役の grep 行数（.expanduser() 2,080 など）はファイル全体の数なので過大です。
- R4-r2-3: 守り付きの試作で較正対 14 木と prev5 4 木を比べると、消えた行 0、矛盾 note の変化 0、slot の変化 3 でした（A5 execute_python_file と winremote Ping。どちらも MODEL/opaque → MODEL/resolved）。sink 直下の `str(` 94 箇所 / 7 木は未検証の見積もりです。
- R1d-r6-3: v2 run20 の D3 の NET 行（矛 160 / 不 335）で、sink の近傍に rstrip 系があるのは 15 行・2 か所でした。どちらも基底 URL が仮引数なので、fold（リテラルに対して結果を計算する直し方）の影響は 0 行です。1,644 箇所は vendored を含む見積もりです。

R1d-r6-3 の一般性の検証役は low にしました。理由は「D3 だけに効き、効くのはリテラルの基底 URL だけ」です。D62 で D3 だけに効くことは重大度を下げる理由になりません。また設計の検証役は、MODEL の値や SQL の定数（`"DELETE ...;".rstrip(";")` は矛 → 不 db_sql_unreadable）を通じて D1 / D2 にも効くことを試作で確かめています。そのため medium とします。
- **直し方（一般に正しいか: 条件つきである）**: 共通の手順: 「解決率を上げる変更（opaque → resolved、行が増える）」なので、CLAUDE.md の敵対的レビューを通す。規則 → 反例テスト → 実装の順にコミットする。diff_effects / compare_scans で、消えた行と増えた矛を 1 件ずつ確かめる。TRANSFER 表を足すことが月 3 凍結の対象かは O25 で「要確認」のままなので、直すなら decisions.md に決定として書く（凍結の一覧は sink 語彙・入口などで、TRANSFER は入っていない。前例は D35 (e) の encode/decode と D43 の .parent）。

(A) Path を返す pathlib のメソッド（R4-r1-5）
- 対象: expanduser / joinpath / with_suffix / with_name / with_stem / absolute / relative_to、それに dotted 完全一致の pathlib.Path.home / cwd。
- 素朴な直し方で壊れる反例: 探索役の fix_sketch は、名前で引く subject=receiver の TransferRow を無条件に足す。これでは、受け手が Unknown（木の外の工場関数 open_bucket() の戻り値）で、木の中のクラス Bucket が同名のメソッド（joinpath / expanduser / absolute / with_suffix）の中に os.remove / shutil.rmtree を持つ形（ce5_namedmethod）が壊れる。今は出ている 4 ツールの FS_WRITE 矛が、TRANSFER に食われて消える（新しい誤 clear）。`_in_tree_method` は受け手が既知の木内 Obj のときしか除外しないので防げない。
- 避ける条件: pathlib の receiver 行は「受け手の形が既に Path のときだけ」適用する（.parent の保護と同じ。patchA2_guarded で ce5 の 5 ツールすべてが残り、h5 の 6 本も出ることを確認済み）。
- D43 の規則を守る: 主体と roots は引き継ぐ。`canonicalised` などの attrs（Path.resolve 由来）は with_suffix / joinpath の結果に引き継がない。engine.py:913 の分岐で形を保つと subject.attrs が残るので、落とす。
- 確度: Path.cwd() は os.getcwd と揃えて opaque(unresolved)（f0a_checks.md:591）。Path.home() は config atom として OP/resolved でもよい。
- joinpath の実引数は others として主体・確度・root に合流させる。segs には入らないが、核には影響しない。

(B) 恒等変換 str() / os.fspath / Path.as_posix（R4-r2-3）
- 素朴な直し方で壊れる反例: `str` を BUILTIN_SINK_NAMES と TRANSFER に足すと、モジュール直下で `def str(x): os.system(...)` と組込み名を上書きした木（str_shadow）が壊れる。(1) の TRANSFER が (4) の木内解決より先に効き、echo の SPAWN 矛が消える（新しい誤 clear。D61 改訂で G2 を取り消した理由と同じ）。
- 避ける条件:
  (1) `str` がモジュール直下で束縛される、`_module_writes` に str か "*" がある、`global str` で書き換えられる、`globals()` / `exec` を使うモジュールでは、組込みとみなさず TRANSFER にしない。
  (2) 第 0 実引数の形が木内クラスの Obj なら TRANSFER にしない（`__str__` / `__fspath__` を持ちうる。`_is_external_class` で判定）。
  (3) os.fspath にも同じ守りを付ける（試作は builtins.str にだけ付けた）。
  (4) as_posix の shape は "str" にしない。Str((Path,)) で Path の形が落ちるので、"same" か "path" にする。受け手不明の `x.as_posix()` は既存の `_in_tree_method` の除外に従う。
- 試作（R4_hm_4/proto3 + 守り）で、repro 6 件は期待どおり、B3a 8/8・B3b 15/15、tests 全通過（corpus 走査を除く）。

(C) str.rstrip / lstrip / removesuffix / removeprefix（R1d-r6-3）
- 素朴な直し方で壊れる反例: 探索役の fix_sketch は `strip` と同じ shape "str" の行を足す。実引数が全部リテラルのとき `Str((subject,))` は変換前の文字列を残す。そのため `BASE.rstrip("/") + endpoint`（実際の値は "http://localhost:8000" + endpoint。endpoint="@evil.example/x" で宛先が移る）で host を localhost と切り出し、内になる（新しい誤 clear。removesuffix と f 文字列の形も同じ）。逆向きの `(BASE + "items/" + item).rstrip("/")` は 不 → 矛になる（新しい誤警報）。
- 避ける直し方（3 つに分ける）:
  (i) 受け手と実引数がすべて resolved のリテラル（Value.const）なら、Python で計算して Atom(const=…) にする。R3-r2-1 の fix (i) にこの 4 つを足す形。ただし `_apply_transfer` は表に行が無いと None を返すので、名前で引く入口が要る。
  (ii) 受け手の形が定数の文字列を持たない（const の無い Atom / Unknown）なら、主体・確度・root・形を保つ。
  (iii) 受け手が定数の part を含む Str / Path なら、今の opaque のまま。
- `_in_tree_method` と R1-r3-3 の守りに従う。
- 固定する反例テスト: rstrip_then_endpoint / removesuffix_then_endpoint / fstring_rstrip_endpoint は矛。rstrip_whole_url は不。env / global / MODEL の既定値は今のまま。例外を投げる実引数（bytes など）は今のまま。
- fold の模擬で、v2 の 8 木と較正対 A1 / A2 / A9 / A18 の両側で変化 0、敵対的な当て方（env・global 再束縛・既定値つき MODEL 引数・モデルの url）では発火しないことを確認済み。
- 範囲外の同じ機構: 既存の `strip`（と `replace`）の行も変換前の文字列を残す。`BASE.strip("/") + endpoint` が今 内になるのは既存の誤 clear。fold を strip にも当てると直る。直さないなら限界として記録する。
- **記録済みの限界・決定との重なり**: 設計の観点で反証された所見は無い（3 件とも refuted=false、expected_is_correct=true）。

関係する記録:
- O25: `str` / `os.fspath` などの TRANSFER 行を足す案 (a) が「月 3 の凍結の対象か要確認」のまま、答えが無い。
- D44: fallback の主体だけを直し、`str` の確度は扱っていない。テストは prin=MODEL だけを固定している。
- D43 / O22: `.parent` / `.parents` だけ形を保つよう直した。R4-r1-5 は同じ機構の残り。
- D35 (e): 内容を変えない str.encode / bytes.decode を TRANSFER に入れた前例。
- D57 §9.3 と O33: MODEL/opaque = 不、「選べる」= MODEL かつ resolved は設計上の決定で、この所見は争っていない。§9.3 の根拠（静的に決まらない）が値の不変な変換には当てはまらない、という主張である。
- D17: opaque(unresolved) への合流そのものは既知の設計。
- f0a_checks.md:518: `.expanduser()` が未カタログである事実を D14 の時点で記録しているが、直していない。

他の単位・所見との重なり:
- R3-r2-2: R4-r2-3 の重複として除かれた。
- R3-r2-1: fix (i) の fold。R1d-r6-3 の定数の側と同じ直し方。
- R1d-r6-6: urljoin で「実引数が全部リテラルなら結果 = 受け手」という同じ近似の誤り。
- R1-r3-3: 木内メソッドの横取りの守り。
- R4 r3 の checked_but_ok[67]: 「rstrip 等は語彙の問題」としたが、探索役の判断で設計の記録ではない（設計の検証役が確認）。
- review_plan §5 の O39 / O41「語彙に無いライブラリ」は sink 語彙の話で、TRANSFER 表には当たらない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: R4-r1-5 と R4-r2-3 は旧文言「D3 / D4 だけなら low」のもとで検証されたが、どちらも D1 / D2 に効くので medium のままで、下げられた形跡は無い。

R1d-r6-3 は §7.7 によると新しい文言で（Opus で）検証された。ただし一般性の検証役は、low の理由に「D3 だけに効き」と「v2 run20 での影響 0 行」を挙げていて、旧文言と同じ趣旨の理由が混じっている。D62 ではその部分は理由にならない。代表値（中央値）は medium で、設計の検証役は D1 / D2 への効きも確かめているので、medium とした。
- **推奨の理由**: fix の基準をすべて満たすので、直すことを勧める。
- 3 件とも代表の重大度は medium で、主に誤 clear の向き。
- どれも Python の言語仕様・pathlib の仕様から正解が決まり（D61 の基準 1・2）、v2 / v3 への合わせ込みではない。
- 凍結した語彙（sink / 入口 / weak 理由）の追加ではない（TRANSFER 表は凍結の一覧の外。ただし O25 への答えを決定として書く）。
- 設計の観点では反証されていない。
- 検証役 3 人とも、条件つきで一般に正しい直し方を示し、試作で確かめている（Path の形の守り、str の上書きの守り、リテラルの fold）。

条件:
- 探索役の fix_sketch をそのまま入れると、3 件ともそれぞれ新しい誤 clear を作る（ce5_namedmethod、str_shadow、rstrip_then_endpoint）。fix_outline の守りを必ず付ける。
- (C) の rstrip 系は、R3-r2-1 の fold（リテラルに対して結果を計算する直し方）を入れることが前提になる。学生が fold を採らないなら、(C) のうち定数の側は限界として記録し、(ii) の非定数の受け手の側だけを直す（実質 fix_partially）。
- **所見**:
  - R4-r1-5: 代表の 1 つ（D1 / D2、medium×3）。Path を返す pathlib のメソッドで Path の形が消え、後続の write_text / unlink の効果行が丸ごと消える。D43 と同じ機構の残り。直すときは「受け手の形が既に Path のときだけ」適用し、canonicalised は引き継がない（ce5_namedmethod の反例）。（Path を返す pathlib のメソッド（expanduser / joinpath / with_suffix / absolute / Path.home() / Path.cwd()）が TRANSFER に無く、受け手が Unk）
  - R4-r2-3: 代表の 1 つ（D1 / D2、medium×3）。str() / os.fspath / as_posix の恒等変換で MODEL/resolved が opaque になり、3-a の矛が不に落ちる（R3-r2-2 はこの重複）。直すときは組込み str の上書きと木内 Obj の守りが要る（str_shadow の反例）。（`str(p)` / `os.fspath(p)` / `p.as_posix()` / `str(cmd)` の恒等変換が TRANSFER に無く（`str` は組込み名の解決にも無い）、MODEL/resolved のパス・コマンドが）
  - R1d-r6-3: 同じ原因の別の表れ（D3 が主、D1 / D2 にも効く。medium/medium/low → medium）。rstrip 系で定数の宛先が読めなくなる。strip と同じ行を足すと新しい誤 clear / 誤警報になるので、R3-r2-1 のリテラル fold と組にして直す。既存の strip の行にも同じ穴がある（範囲外）。（`str.rstrip` / `lstrip` / `removesuffix` / `removeprefix` が TRANSFER に無い（`strip` はある）ため、`BASE_URL.rstrip("/") + "/items/）

### U08 リテラルの純関数の畳み込み（定数どうしの文字列演算の結果が「定数」として読めない）（段階 C・重大度 中・推奨 直す）

"delete".upper() や " ".join(["DELETE","FROM","t"])、"VACUUM".strip() は、Python では実行前に値が 1 つに決まる定数です。ところが解析器は計算した結果を持たず、「中身の見えない連結」として扱います。そのため SQL は途中までしか読めない文、HTTP メソッドは読めないものになり、readOnly なツールの DELETE・VACUUM は「矛（宣言と食い違う）」ではなく「不（判定できない）」に落ちます（矛の取りこぼし）。GET・COMMIT・SELECT は「内（問題なし）」でなく「不」に上がります（不の水増し）。さらに urljoin(ローカルの BASE, "https://外部/x") は宛先の host を BASE 側と読むので、openWorldHint=False と食い違う外部への通信が、黙って「内」になります（誤 clear）。

- **宣言**: D1 / D2 / D3　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_apply_transfer` は実引数と受け手が全部リテラルでも純関数の結果を計算せず、`Str((subject,))`（`Value.const` が None）や受け手の定数をそのまま返す（定数 + 定数の Str も const を持たない）。そのため `"delete".upper()` / `" ".join(["DELETE", ...])` / `"VACUUM".strip()` が SQL は「接頭辞」・HTTP メソッドは「読めない」扱いになり、`urljoin(BASE, 絶対 URL)` の宛先は BASE の host と読まれる。
- **コードの場所**: authgap/val/engine.py:915-925 _apply_transfer（全リテラルで Str((subject,)) を保つ）, authgap/catalog/transfers.py:64 urljoin 行, authgap/ir.py:364-372 Value.const, authgap/effects.py:286-293, 333-369 _http_method / _mode_const / sql_text, authgap/dparse.py:364-374
- **重大度の根拠**: 代表の R3-r2-1 は 3 意見（探索・設計・一般性）とも medium。DB と NET の両方の効果に効きます。REST を橋渡しする MCP サーバの wrapper（request(method=method.upper(), …)）は標準的な書き方で、readOnly の DELETE が 矛→不、GET が 内→不 の両向きに出ます。この書き方の件数は、探索役の数えで corpus/ に 62 行、一般性の検証役の数えで 15 件です（数え方が違い、どちらも未照合）。一方、v2 run20 で影響を受けた行は 0（一般性の検証役が確認: db_sql_unreadable の Str 形 2 行は先頭が Unknown の連結、net_method_unknown 289+11 行はすべて urlopen）なので high にはしません。R1d-r6-6 は 3 意見とも low で、理由は「定数の絶対 URL を urljoin に渡す書き方はまれ」だからです（D3 だけに効くことは理由にしていません）。D4 も dparse._d4 が sql_text と fs_mode を読むので、コードを読む限り同じ機構が効きますが、未測定です。
- **直し方（一般に正しいか: 条件つきである）**: 【直し方】定数の畳み込み（検証役の fix (i) を細かくしたもの）。受け手と実引数（kwargs を含む）が全部確度 resolved のリテラル（`Value.const is not None`。`is_literal()` と同じ）のときだけ、実際に計算した値を `Atom(const=結果)` にします。主体・確度・root・attrs（'joined' など）は今のまま残します。
(1) `_apply_transfer`（engine.py:915-917 の全リテラルの分岐）: str を返す変換（strip / lstrip / rstrip / upper / lower / replace / format）と `urllib.parse.urljoin` は、ライブラリの関数そのもので計算します。urljoin は RFC 3986 §5.2.2 のとおり、絶対 URL や `//host/x` の参照なら参照側の host になります。
(2) `_str_join` / `_make_str`: 区切りと全要素が str の定数で、かつ列にも結果にも tail が無い（K=16 を超えて畳まれていない）ときだけ連結します。所見の題名にある「定数 + 定数」（'DELETE' + ' FROM t' → 今は 不 db_sql_unreadable）も、`_make_str` の同じ条件で畳みます。
(3) 計算は try/except で包み、例外が出たら今の形に戻します。
【素朴な直し方で壊れる反例（検証役）】
(a) encode / decode まで畳むと、'DELETE FROM t'.encode() の const が bytes になり、sql_text が読めずに 今の 矛 db_modify が 不 db_sql_unreadable に退行します。→ str を返す変換だけを畳みます。
(b) 読む側で変換前の定数 part を連結する直し方（fix (ii)）は一般に正しくありません。'SELECT * FROM t'.replace('SELECT *','DELETE') は実行時 DELETE なのに 内（今ある誤 clear）のまま残り、逆向きの誤警報も残ります。→ fix (ii) は採りません。畳み込みならどちらも直ります。
(c) 20 要素の join（K 超え）は value_join が同じ定数を保つので、畳むと要素が欠けます。→ tail があれば畳みません（今のまま 不）。
(d) 'DELETE FROM {} {}'.format('t') は実行時に IndexError です。→ 例外なら今の挙動（矛）に戻します。
(e) urljoin を直すとき「全部リテラルなら形を捨てて Atom()」にすると、今は正しい urljoin(BASE,"items")（内）と urljoin("https://api.example.com/v1/","items")（矛 net_external_host）が 不 に落ちます。→ 形を捨てず、計算して定数にします。
【避ける条件】
・`Value.const`（resolved）で鍵をかけます。形（Str / Atom）では鍵をかけません（D61 G2 取り消しの教訓）。opaque の定数、再束縛されるモジュール名、MODEL の仮引数の既定値（method: str = "GET"。const を持たないことを検証役が ce3b で確認）では畳み込みが発火しません。
・subject が定数でない場合は今の `Str((subject,))` のままにします（BASE が定数の連結のとき、今は 不 net_host_unknown で、誤 clear は作らない）。
【任意の追加（一般性の検証役の提案。不が増える向き）】畳めない場合でも、内容を変える変換を別に扱う案です。対象は replace と、参照がリテラルの絶対 URL か `//` で始まる urljoin です。今は `Str((subject,))` で subject の host を保ちますが、これを Atom()（不）にします。例外として、urljoin の参照がリテラルで scheme も netloc も無いなら、subject の host を保ちます。これは今の BASE が MODEL で参照が絶対 URL の形（誤警報）と、host が変わる replace（誤 clear）を直しますが、replace の一般的な使い方で 内→不 の数え落としを増やします。採るかは学生が決めます。
【同時に確かめること】"http://localhost/x".replace("localhost","api.example.com") も同じ機構の誤 clear です（一般性の検証役が確認）。urljoin だけでなく replace も畳み込みの対象に入れます。
【本記録者の追加の注意（検証役の指摘ではない）】`'{:>1000000000}'.format('x')` のような巨大な結果を避けるため、結果の長さに上限を付けます。超えたら今の形に戻します。
【テストと手順】反例テストに次を入れます: encode / replace の両向き / join の K 超え / format の例外 / MODEL の既定値 / wrapper の仮引数に届くリテラル（_api("delete") → 矛 net_modify）/ urljoin の絶対 URL・`//`・名前つき定数・相対参照・外部の BASE。既存の tests/test_f0a_defects.py:705-736（urljoin_second_arg）の隣に置きます。scripts/diff_effects.py で較正対の効果行を突き合わせ、run を取り直したら compare_scans.py で消えた行を 1 件ずつ確かめます。解決を上げる変更なので、CLAUDE.md / D19 の敵対的レビューを通します。ゲート側（付録）の Str の part を読む箇所への影響は check_gates で確かめます。
- **記録済みの限界・決定との重なり**: 設計の観点では 2 件とも反証されていません（refuted=false）。
・D17 改訂 3（decisions.md:1701）: 非リテラルの実引数が混ざったら形を捨てる規則です。全部リテラルの場合に `Str((subject,))` を保つのは近似にすぎず、決定として書かれたものではありません。
・D17 改訂 5（:1740）: `Value.const` を resolved に限る制限です。確度のためのもので、形のためではありません。
・D57 §9.3 の「"UPD" + x を決めない」空白の防御: 本物の接頭辞のためのもので、全部定数の Str は対象外です。
・D61 G2 の取り消し（:3468）: 未知の受け手のメソッド解決の話です。const で鍵をかければ反しません。
・contradiction_principles.md §9.2 は、urljoin 型のクライアントで「//」に誤 clear を作らないことを意図しています。これは所見の側に立つ記述です。
・K1〜K7・O1〜O41・preregistration の逸脱のどれにも該当しません。
・姉妹の所見 R1d-r6-3（rstrip / lstrip / removesuffix / removeprefix が TRANSFER に無い）は別の単位です。直すなら、畳み込みの対象の一覧に同じ変換を入れると整合します。
・O25（open_questions.md:618-620）の「TRANSFER 表は月 3 凍結の対象か要確認」は未回答です。この単位は TRANSFER の行を足さないので影響しません（R1d-r6-3 側の論点です）。
・§7 の前置き（:149）が「定数 = resolved の Value.const」と括弧書きしている点は、字義どおりに読めば今の実装が仕様どおりになります。しかし設計の検証役は、この読みでは §9.4-1 と §7.6 の「定数」がこれらの形で空になるので採らない、と判定しています。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R3-r2-1 は D1+D2 の所見で、3 意見とも medium です。R1d-r6-6 は D62 の後の D3 / D4 の回（§7.6）で検証されており、設計の検証役は「D62 で D3 が主指標になったので §7.5 により対象」と明記しています。low の理由は書き方のまれさで、旧文言ではありません。
- **推奨の理由**: 代表の重大度は medium です。直し方は、Python とライブラリの意味から値が一意に決まる定数の畳み込みで、v2 / v3 に合わせたものではありません（D61 の基準 1・2 を満たす）。str を返す変換に限る・tail があれば畳まない・例外なら戻す・const で鍵をかける、という条件つきで一般に正しいです。凍結した語彙（sink / 入口 / weak 理由）の追加は要らず、設計の観点の反証もありません。ただし解決を上げる向きの変更なので、直すなら敵対的レビューと diff_effects / compare_scans による突き合わせを必須にします。R1d-r6-6（low）は同じ分岐の同じ直し方で直るので、分けて記録する理由はありません。任意の追加（畳めない replace / urljoin を 不 にする）は、数え落としとの交換になるので、採るかは別に決めてください。
- **所見**:
  - R3-r2-1: 代表（medium、D1+D2）。upper / strip / join / 定数 + 定数 の結果が const を持たず、SQL は接頭辞、HTTP メソッドは読めない扱いになる。矛→不（DELETE / VACUUM）と 内→不（GET / COMMIT / SELECT）の両向きに出る。設計の検証役は rule_mismatch、一般性の検証役は false_clean と判定。encode の退行・fix (ii) の replace の反例・K 超え・format の例外の条件は一般性の検証役によるもの。v2 run20 への影響は 0 行。（定数どうしの Str（str.upper/strip/replace/format() の結果、定数の join、定数 + 定数）は Value.const が None なので、SQL は「接頭辞」・HTTP メソッドは「読めない」扱いに）
  - R1d-r6-6: 同じ原因（全リテラルの分岐が Str((subject,)) を返す）の別の表れ（low、D3、false_clean）。urljoin(ローカルの BASE, 絶対 URL または //host) の宛先を BASE の host と読み、内 になる。一般性の検証役が str.replace で host が変わる誤 clear も同じ機構だと確認した。「形を捨てる」直し方では今は正しい 2 例が 不 に落ちるので、計算して定数にする。（`urljoin(BASE, ref)` の TRANSFER が「実引数が全部リテラルなら結果 = 受け手（BASE）の定数」とするため、`ref` が絶対 URL や `//host/x` の定数（`urljoin("http://lo）

### U10 G3 の import による pin（読む側の束縛を 1 件に決め打つ）（段階 C・重大度 中・推奨 一部直す）

ツールが import した関数を呼んだとき、解析器は「読む側のファイルの import 表」を見て呼び先を決めます（pin）。ところがこの表は同じ名前を 1 件しか覚えません。(1) `try: from .fast import run / except: from .slow import run` や if/else の platform 分岐では、後に書いた import 先 1 件にしか降りません。先に書いた側にある危険な効果（例: os.remove）は、書く順を入れ替えるだけで出たり消えたりします。(2) 関数の中で `from .impl import f as g` の後に `except: g = None` と書くと、import を丸ごと見なくなり効果行が消えます。(3) 同じファイルの別の関数に、同じ名前の仮引数や局所変数があるだけで、呼び先を「決まらない」扱いにします。その結果、矛（食い違いあり）が不（不明）に落ちます。(1)(2) は効果行が黙って消える向き（readOnly 宣言のツールでは誤 clear）で、(3) は矛から不明へ移る向きです。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 呼び出し先を読む側の import 表で固定する `_pinned_candidates`（G3 / D17 改訂 3）が読む側の束縛を 1 件に決め打つ: 条件つき import（try/except・if/else で同じ名前を 2 回 import）は import 表の最後の 1 件しか候補にせず（ソース順に依存）、関数内の `try: from .m import f as g / except: g = None` は `g` が `local_bindings` にあるので import の写像を捨て、書き換えの判定に流用した `_scan_module_writes`（D17 改訂 2）は別の関数の仮引数・局所変数まで「書き換え」に数えて pin を ambiguous（→ `_opaque_deep`）にする。
- **コードの場所**: authgap/val/engine.py:1641-1720 _pinned_candidates, authgap/val/engine.py:2077-2102 _scan_module_writes, authgap/srcindex.py:368-388, 446-457 import 表 / resolve_call_name
- **重大度の根拠**: 代表は R1-r1-6 で、3 意見（探索 medium / 設計 medium / 一般性 low）の中央値は medium。一般性の観点が low としたのは、v2 で「木内どうしの条件つき import で呼ばれる関数」が 0 件だったという頻度が理由で、旧文言（D3 / D4 だけなら low）とは関係がない。3 件とも影響は D1+D2 で、D62 による重大度の戻しは要らない。R1-r1-10 と R1-r4-5 は 3 意見とも low。検証役が数えた数: R1-r1-6 の構文上の上限は 760 件 / 35 木（413 木中。TYPE_CHECKING 形を含む過大な上限）。v2 の AST 計数では、2 回以上 import で束縛され少なくとも 1 件が相対 import の名前が 289、同じモジュールで呼ばれる関数名が 99 だった。99 はすべて abyss-stack `_modern_runtime.py`（12 複製）の 1 パターンで、except 側が外部 import の別経路にあたり、今回の穴そのものは v2 で 0 件観測。R1-r4-5 は v2 で 3/99 木（構文上の上限）。R1-r1-10 は未測定。書き方としては Python の常套形（任意依存の予備、platform 分岐）で、最終評価のデータでの頻度は未測定。
- **直し方（一般に正しいか: 条件つきである）**: 【R1-r1-6（直す）】`_pinned_candidates`（engine.py:1641-1720）で、読む側の呼ぶ名前の束縛（`_module_bindings(rtree, reader_name)`）が 2 件以上のときは、import 表（srcindex.py:368-388 の `_collect_imports` は同名を後勝ちで上書きする）を使わない。各 Import / ImportFrom を `_follow_reexport` と同じく `level` で解いて（モジュール, 元の名前）にし、`_visible_defs` の和集合を候補にする。`ambiguous=True` のまま全候補へ降り、opaque にする（D61 改訂 G3-3 の「全候補へ降りて opaque」と D17 改訂 5 に合わせる）。
検証役が付けた条件は次の 3 つ。(a) 表の最後の import が外部だと `module=None` で早期 return し、今は末尾名検索で救われている（ce_r6_external_first）。この経路に依らないよう、「読む側の全 import 束縛のうち木内に解けるものすべて」を候補にする。(b) 各 import 先にも `_follow_reexport` を当て、(module, qualname) で重複を除く。同じ def を 2 経路で import した形（`from pkg import run` と `from pkg.core import run`）で行が二重に出ないようにするため。(c) `if TYPE_CHECKING:` の本体は実行時の束縛ではないので、束縛の数にも候補にも入れない。
検証役は patched_r6 で動かし、reader_cond_import / reader_if_import が reader_if_import_rev と同じ FS_WRITE 行（opaque、contradiction:D1:fs_write）を出すこと、つまり結果が順序に依らなくなることを確かめた。今の正しい結果が壊れる形は見つからなかった（試した形: 先が木内・後が外部、両方外部、同じ def を 2 経路、TYPE_CHECKING）。増える行はすべて opaque。使われない分岐の行が誤警報になりうる点は、D17 改訂 5 で受け入れ済みの限界。
【R1-r1-10（任意。直すなら条件つき）】所見の素朴な直し方「head が local_bindings にあっても local_imports に写像があれば pin して ambiguous」には、検証役の反例がある。`from .impl import do_write as writer; writer = print; writer(p)`（c10 の aliased_overridden）は今は効果なしで正しいのに、素朴な直し方では impl.do_write に opaque で降り、D1 fs_write の誤警報を新しく作る。避ける条件: 関数本体の import は env に `_import_placeholder`（engine.py:381-390, 1870）を書くので、呼び出し位置の env の値に import 由来の束縛が合流で届いている（全経路で上書きされていない）ときだけ local_imports で pin し、ambiguous=True にする。`resolve_call_name`（srcindex.py:446）も同じ条件で扱う。
【R1-r4-5（記録）】所見の直し方は `_scan_module_writes` を (i) 真の再束縛（global / nonlocal、"*"、モジュール直下の再代入）と (ii) 関数ローカルの束縛（関数ごとの行範囲つき）に分けるもの。G3 の reader 判定、`_module_value` の `reader_rebinds`（engine.py:1231）、定義側の rebound、`_follow_reexport` の `name in writes` には、(i) と「呼び出し位置 / 読み出し位置を囲む関数（入れ子の外側すべて）の局所」だけを使う。検証役の反例: 素朴な直し方（global / nonlocal / * だけを見る）では、入れ子関数が外側の局所 `ROOT = root` / `render = ident` を掴む形（cx5 / cx5b）が誤って OP/resolved の定数になる（判定は不のまま、resolved の主張が誤り）。「囲む関数の局所」の節がこれを防ぐ。直すなら cx5 / cx5b を反例テストにする。これは opaque → resolved の向きなので、CLAUDE.md の敵対的レビューが要る。
共通: どれも authgap/ の変更なので再凍結（指紋の更新）と `docs/preregistration.md` への逸脱の記録が要る。直したら diff_effects.py と compare_scans.py で消えた行を 1 件ずつ確かめる。
- **記録済みの限界・決定との重なり**: R1-r4-5 は設計の観点で反証済み（refuted、confidence 0.7）。D61 改訂 G3 の条件 3（decisions.md:3479-3481）は判定に `_scan_module_writes` を名指しで使うと決めており、その docstring は仮引数・代入先を含むと明記している。D17 改訂 2 の「精度の代償」（decisions.md:1682-1683、「同名の局所変数がどこかの関数にあるだけで読まなくなる … clean を作らない」）も同じ過剰近似を記録している。さらに contradiction_principles.md §9.3（:310）は、MODEL/opaque が不へ移ることを「誤 clear ではなく『不明』への移動（規則 4 どおり）」と明示している。このため、所見の「O33 の後は誤 clear」という主張は規則からは導けない。実装は書いた規則どおりで、直すには規則の改訂（逸脱）が要る。R1-r1-6 はどの記録済みの限界とも重ならない。D61 改訂 G3-3 の「全候補へ降りて opaque」と実装の食い違いで、D17 改訂 5 が受け入れた限界は逆向き（全候補へ降りる側の誤警報）。tests/test_fix_d61.py:453-466 は `g = danger` 形しか試していない。CLAUDE.md の落とし穴「条件つき import を落とさない」とも同じ形。R1-r1-10 に近い記録は decisions.md:1759-1760（局所 def と同名の呼び出しは末尾名検索に回る）と K5（decisions.md:1538）があるが、どちらも帰結が違い、重ならない。review_plan §5 の O41・K1〜K7・O36 にもこの根本原因は無い。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも影響は D1+D2 で、D3 / D4 の旧文言は関係しない。R1-r1-6 の一般性の観点が low としたのは、v2 での頻度（木内どうしの条件つき import で呼ばれる関数 0 件）が理由。
- **推奨の理由**: R1-r1-6 は fix の基準をすべて満たす。代表の重大度は medium、設計の観点は反証せず「書いた規則 G3-3 と実装の食い違い」と判定し、一般に正しい直し方があり（検証役が patched_r6 で確認、壊れる反例なし）、語彙の追加も要らない。直すと効果行が増える向きなので、敵対的レビューを通す。R1-r1-10 は low でまれな書き方（関数内・別名つき・except で None の 3 つがそろう形）。素朴な直し方には誤警報の反例があり、流れに沿った条件が要るため、基準上は記録に回すのが妥当。R1-r1-6 と同じ関数を直すので、条件つきで一緒に直す選択もある。R1-r4-5 は、設計の観点が「書いた規則（G3 条件 3・D17 改訂 2）どおりで、§9.3 により誤 clear ではなく不明への移動」と反証した。low で v2 でも 3/99 木とまれで、直すと opaque → resolved の向きの規則改訂になるので、限界として記録する。
- **所見**:
  - R1-r1-6: 代表（medium、推奨 fix）。読む側の条件つき import（try/except・if/else）で import 表の最後の 1 件にしか降りず、結果がソースの順序で変わる。設計は反証せず（G3-3 との食い違い）、一般性の観点は patched_r6 で直し方を確認済み。（読む側モジュールの条件つき import（try/except・if/else で同じ名前を 2 回 import）は `ambiguous` にはなるが候補が import 表の最後の 1 件だけで、先に書かれた import 先の効果が）
  - R1-r1-10: 同じ原因の別の表れ（low、推奨 record_as_limitation、条件つきで一緒に直してもよい）。関数内の別名つき import に except の `g = None` が重なると、local_bindings を理由に import の写像を捨てて効果行が消える。素朴な直し方には aliased_overridden の誤警報の反例があり、env の import placeholder が生きているときだけ pin する条件が要る。（関数内の `try: from .m import f as g` / `except ImportError: g = None` の後の `g(p)` が、`g` が `local_bindings` にあるため import 表の写像）
  - R1-r4-5: 設計の観点で反証済み（low、推奨 record_as_limitation）。`_scan_module_writes` を流用したため、別の関数の仮引数や局所変数でも pin が ambiguous になる。G3 条件 3 と D17 改訂 2 の書いた規則どおりで、§9.3 により矛から不への移動は誤 clear ではない。直すなら規則の改訂と、cx5 / cx5b の反例テストが要る。（G3 改訂 3 の「読む側で呼ぶ名前が関数の中で書き換えられるなら ambiguous」の実装が `_scan_module_writes`（D17 改訂 2）をそのまま使うため、**別の関数の仮引数 / 局所変数**が import した）

### U11 木内 / 外部の区別を名前の一致で決める（段階 C・重大度 中・推奨 一部直す）

解析器は、呼び出した関数や型がこのリポジトリ（木）の中で定義されたものか外部ライブラリのものかを、import の意味どおりに解かず、名前の末尾が一致するかどうかで決めている箇所が 4 つある。そのため、`subprocess.run` や `requests.Session().get` のような外部の呼び出しが木の中の同名メソッド（`Agent.run` など）に結ばれたり、木の中の `app/requests.py` の関数がライブラリの `requests.delete` として扱われたりして、readOnly のツールに無い矛盾が出る（誤警報）。逆に、`from . import utils` の `utils.resolve(p)` は文字列や Path のメソッドと取り違えられ、木の中の関数に降りないので、その中の `os.remove` などが丸ごと消える（誤 clear）。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 呼び出し・型の名前が木内の定義か外部ライブラリかを、読む側の import 表による解決でなく名前の一致で決める: `_is_external_class` は `resolve_module_strict` の末尾成分一致に頼る（木に `app/requests.py` があると `requests.Session()` が木内クラスに resolved で結ばれる）、`_resolve_in_tree` は import 表で木外に解決した `subprocess.run` / 外部型の受け手のメソッドでも末尾名で木内の同名メソッドへ降りる、`_suffix_match` の末尾 2 要素一致は木内の同名モジュールの関数呼び出しを sink 行にする、`_apply_transfer` のメソッド名の TRANSFER 照合は木内解決より先に走りモジュール別名 `utils.resolve(p)` を `Path.resolve` にする。
- **コードの場所**: authgap/val/engine.py:1551-1555 _is_external_class, authgap/srcindex.py:234-247 resolve_module_strict, authgap/val/engine.py:939-1020 _resolve_in_tree（末尾名の木全体検索）, authgap/effects.py:161-170 _suffix_match / 603 _direct, authgap/val/engine.py:887-897 _apply_transfer のメソッド名照合
- **重大度の根拠**: 代表の重大度は medium。R1-r2-1（誤警報）と R1-r3-3（誤 clear）はどちらも 3 観点とも medium で、ほかの 2 件（R1-r1-12、R4-r3-2）は 3 観点とも low。4 件とも影響は D1+D2 で、4 件とも実行の観点で再現した。頻度は次のとおり。R1-r2-1: 探索役の AST 走査では、同名メソッドが木に 1 つだけある外部の呼び出しを持つ木が 31/87（検証役は explorer の estimate_tail から 38/87 木・2485 箇所を引いている）。どちらも到達性と sink の有無を見ていない上限。run20 の CONTRADICTION で実例は 0。ただし野外の 34 木を突き合わせたところ、偽の経路 2 本（neo4j の session.run → 評価スクリプトの run、httpx の client.post → click コマンドの post）を確認した。これらは宣言が無いか判定に効かない位置で、矛にはなっていない。R1-r3-3: v2 で 4 木 16 箇所（探索役の数え。到達性は未確認で、検証役は未検証と明記）。R4-r3-2: 同名のファイルは 20 個あるが、sink と同名の関数を持つものは確認できなかった（見積もりのみ）。R1-r1-12: 頻度は未測定（稀）。第 1〜5 回の旧文言「D3 / D4 だけなら low」で重大度を下げた形跡は無い（4 件とも D1+D2 に効く）。
- **直し方（一般に正しいか: 条件つきである）**: 共通の原理: 「外部」または「木内」と言い切れるのは、Python の import の意味でそう証明できるときだけにする。証明できないときは、今までどおり D17 の末尾名で降りて opaque(unresolved) を合流する。どの所見も探索役の fix_sketch をそのまま入れると壊れる形があるので、検証役の条件を必ず写す。

(1) R1-r2-1（_resolve_in_tree、engine.py:939-1020）。_pinned_candidates が「import 先が木外」で None を返したときに、末尾名で木全体を検索する経路に回さない。ただし「外部と断定」してよいのは次の (i)〜(v) を全部満たすときだけ（試作 patched/r1c）。
(i) 読む側のモジュールで、その名前の束縛が 1 つ（D61 G3 の条件 3 と同じ）。
(ii) `*` import・`exec`・`globals()` が無い（_scan_module_writes が '*' を返さない）。
(iii) 厳密な解決だけでなく、緩い末尾一致の resolve_module_path も木内モジュールを見つけない。
(iv) 木のどこにも `<alias>.<name> = …` / `setattr(<alias>, "<name>", …)` / `builtins.<name> = …` が無い。
(v) 受け手が外部型なら、その外部型を基底に持つ木内の派生クラスの同名メソッドにだけ by_name（opaque）で降りる。
組込み（builtins）の補足: 同じモジュールに def open があると resolve_call_name が builtins.open を返すので、_visible_defs(scope.module, name) が空のときだけ外部とみなす。
fix_sketch を字義どおり実装した版（r1）が壊す反例 5 形（すべて誤 clear）:
- try/except の予備 import（木内の fastrun.run を先に import し、subprocess.run を予備にする）
- リポジトリの根がパッケージそのもので、絶対 import する形（from mcp_foo.tools import run）
- 外部型を継承した木内クラス（class RetrySession(requests.Session)）で、受け手の型が注釈 `s: requests.Session` でしか分からない形
- from fsutil import * が組込みの open を隠す形
- モジュール直下で束縛し直す形（run = Agent().run）
r1c の結果: 10 木ですべて意図どおり。野外 34 木では、消えた効果行は偽の経路 2 本だけで、contradiction 注記は 23→23 で不変。r1c の pytest は報告の時点で実行中で、結果は未確認。残る限界: package_dir で葉のモジュール名を変える配置は、外部と誤判定しうる。ce1_exec_variant（モジュールが exec を呼ぶ形）は、(ii) により保守側で矛が残る。これは意図どおり。

(2) R1-r1-12（_is_external_class、engine.py:1551-1555）。案 2 を採る: dotted 型のモジュール部分が木内モジュールに解決できても、get_class(末尾名, そのモジュール, strict=True) が無ければ外部とみなす。木内とみなすときも、typed_classes をそのモジュールのクラスに限る（末尾名で木全体に広げない）。案 1（カタログ由来の dotted 型を無条件に外部とする）は反例 c12e で壊れるので採らない。c12e は、木の根に git.py の Repo.cleanup があり、根から実行すると import git が木内を読む形で、案 1 だと矛が消える（誤 clear）。注意: 所見の期待は、D17 の降下を残す現行の設計では誤り。所見の木でも opaque(unresolved) で矛は残り、D1 が変わるのは同名メソッドが 2 つ以上あるとき（c12c）だけ。(1) の条件 (v) と一緒に入れると、所見の木でも降りなくなる。(v) は _is_external_class が正しいことを前提にしているので、(1) を採るなら (2) も一緒に入れる。

(3) R1-r3-3（_apply_transfer、engine.py:887-897）。メソッド名で TRANSFER を照合する前に木内の解決を試す。条件は受け手の値に置き、_is_import_placeholder(receiver, head) が真で、かつ _pinned_candidates が候補を返すときだけ TRANSFER を飛ばす。fix_sketch の「scope.lookup(head) がモジュールに解ける」だけでは壊れる。Scope.lookup は local_bindings を見ないので、局所で束縛し直した `utils = Path(p)`・仮引数 `utils`・ループ変数 `utils` まで木内に降り、実行されない os.remove の矛や、存在しない SPAWN 行を作る（試作 3n で確認）。試作 3 の結果: 所見の 6 形が素の名前の import と同じ行になり、影の 3 形と posixpath.join は変わらず、関数本体の import・`import pkg.utils as u`・__init__ の再公開も降りた。較正 14 木で lost 0 / gained 0、pytest 685 passed / 14 xfail。候補が複数あるときは D17 改訂 5 の規則（全候補へ降りて opaque）に乗せる。行が増える向きの変更なので、敵対的レビューが要る。

(4) R4-r3-2（_suffix_match、effects.py:161-170 / 603 _direct）。fix_sketch の「呼び先が木内の関数定義に解決したら sink 表を当てない（行を落とす）」は、ライブラリを木に複製した形（app/_vendor/requests。urllib3 は語彙外）で、本物の HTTP DELETE を黙って消す（誤 clear）。複製と偶然の同名を言語の意味で見分ける規則は見つからなかった。一般に正しいのは、行を残して opaque(unresolved) を合流する形（effects.py:231-236 の _resolution_of(..., by_name=True)）。判定は「モジュールが木内」ではなく「関数定義が木内に解決した」で行う（app/compat.py でライブラリを再公開する形を壊さないため）。結果として、所見の例は矛から不になる（「矛盾なし」にはならない）。§7.1 で FS_WRITE / EXEC は確度を問わず矛なので、この直し方ではその kind の誤警報は残る（推論。未測定）。

手順: 規則を書く → 上の反例をテストにする → 実装する → scripts/diff_effects.py と compare_scans.py で消えた行を 1 件ずつ確かめる。(1)(2)(4) は効果行や確度を落とす向き、(3) は行が増える向き。
- **記録済みの限界・決定との重なり**: 4 件とも設計の観点で反証されていない（refuted=false）。関係する記録:
- D61 改訂の G4（decisions.md:3481-3484「外部の型のオブジェクトが木の中の同名クラスのインスタンスであることはない」）: R1-r1-12 はこの規則の実装の抜けで、R1-r2-1 はこの原理を関数呼び出しへ広げる話。
- D17 改訂 2 の resolve_module_strict（decisions.md:1678）: 末尾一致は意図した近似。ただし R1-r1-12 の帰結は、どちらの読み方でも G4 に反する。
- D17 改訂の「末尾名で降りて opaque にする」と、review_plan §5 の「opaque(unresolved) への合流は設計上の決定」: 受け手の型が分からない呼び出しのための規則で、import 表で外部と分かる呼び先（R1-r2-1）は対象外と設計の観点が判定した。ただし R1-r2-1 の直し方を条件なしで入れると「降りるのをやめて真の経路が消える」という D17 の落とし穴にそのまま落ちる（反例 5 形）。R1-r1-12 について一般性の観点は、所見の期待（矛が出ない）は D17 と食い違うと判定した（review_rows で expected_ok=false）。
- O41 の「組込み型の末尾名解決」（記録済みの限界）: 根本原因が別（値の形は型の証明ではない）で、重ならないと判定された。
- D35 (e)（decisions.md:302-308「TRANSFER は木内メソッドを横取りしない」）: 受け手が Obj の形だけを直した記録。R1-r3-3 はその残り（モジュール別名の受け手）で、限界として記録したものではない。
- R4-r3-2: decisions.md:1729 の相対 import の限界は別の根本原因。D61 改訂の追記（decisions.md:3488、`from . import httpx` を注釈側で直した）は同じ種類の誤りを別の経路で直した記録。
- explore_d3d4 の checked_but_ok は、R1-r2-1 / R4-r3-2 について「D3 / D4 の判定は変わらない」と記録している。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも影響は D1+D2 で、検証役の重大度（R1-r1-12 low / R1-r2-1 medium / R1-r3-3 medium / R4-r3-2 low）の理由は、発生条件の狭さ（外部と同名の木内モジュール、同名メソッドが 1 つ、など）。「D3 / D4 だけなら low」を理由にした記述は無い。
- **推奨の理由**: R1-r2-1（誤警報）と R1-r3-3（誤 clear）は、fix の推奨の基準を満たす。3 観点とも medium で、import の意味から導ける条件つきの一般の直し方があり、試作でも確かめられている（r1c: 野外 34 木で偽の経路 2 本だけが消えた / 試作 3: 較正 14 木で差 0、pytest 685 passed）。語彙の追加は要らず、設計の観点も反証していない。R1-r1-12 は low だが、R1-r2-1 の条件 (v) は _is_external_class が正しいことを前提にするので、同じ修正に含めるのが整合的（S の変更で、案 2 に限る）。R4-r3-2 は low でまれ（コーパスに sink と同名の関数を持つ同名モジュールは確認されていない）。一般に正しい直し方（opaque の合流）でも、結果は矛から不に変わるだけで、FS_WRITE / EXEC の誤警報は残る。落とす版はライブラリを木に複製した形で誤 clear を作るので、限界として記録することを推奨する（直すなら opaque の合流の形だけ）。R1-r3-3 は解決率を上げる向きなので、CLAUDE.md の敵対的レビューが要る。
- **所見**:
  - R1-r2-1: 代表（medium、誤警報）。import 表で木外と分かる呼び先（subprocess.run / builtins.open / 外部型の受け手の post や get）が、末尾名で木内の同名メソッドへ降りる。素の名前の形では resolved で降りる。直す（条件 (i)〜(v)、試作 r1c）。（外部ライブラリの呼び出し（import 表で木外のモジュールに解決する `subprocess.run` / `requests.get` / `builtins.open`、または受け手型が外部クラスの `httpx.AsyncClien）
  - R1-r3-3: 同じ原因の逆向きの表れ（medium、誤 clear）。モジュール別名の utils.resolve(p) が、名前だけの TRANSFER の照合で Path / str のメソッドとして扱われ、木内関数へ降りない。直す（受け手の値が import placeholder であることを条件にする。敵対的レビューが要る）。（`_apply_transfer` のメソッド名だけの TRANSFER 照合（`resolve` / `format` / `encode` / `decode` / `split` / `rsplit` / `strip` / `low）
  - R1-r1-12: 同じ原因の別の表れ（low、誤警報）。_is_external_class が resolve_module_strict の末尾一致に頼るので、木に app/requests.py があると requests.Session が木内扱いになる。R1-r2-1 の条件 (v) の前提なので、一緒に直す（案 2 に限る。所見の期待は D17 の下では誤りで、検証役が修正済み）。（G4 の外部型判定 `_is_external_class` が `resolve_module_strict` の末尾成分一致に依存するため、木に外部パッケージと同名のモジュール（`app/requests.py`）があると `reque）
  - R4-r3-2: 同じ原因の別の表れ（low、誤警報、まれ）。_suffix_match の末尾 2 要素の一致で、木内の同名モジュールの関数が sink 行になる。落とす版はライブラリを木に複製した形で誤 clear になるので、限界として記録を推奨（直すなら opaque の合流だけ）。（`_suffix_match` の末尾 2 要素一致が、木の中のモジュールがライブラリと同名（`app/requests.py` / `app/subprocess.py` / `pkg/os.py`、相対 import `from . i）

### U14 構築するクラスの特定（別名・再公開・cls）（段階 C・重大度 中・推奨 直す）

解析器は、ツールの中で `Runner(cmd)` のようにクラスからオブジェクトを作る箇所を見つけると、`__init__` を実際に走らせて「このオブジェクトの `self.cmd` にはモデルの入力が入っている」と覚えます。ところが、どのクラスを作るのかは「呼び出しに書かれた名前を同じファイルで探す」だけで決めています。そのため次の書き方ではオブジェクトを作れません。別名で import したクラス（`from .impl import Runner as R; R(cmd)`）、`pkg/__init__.py` が公開し直したクラス（`from pkg import Runner`）、公開し直した基底クラスの `__init__`、`@classmethod` の中の `cls(...)`。作れないと、後で `self.cmd` を使う危険な呼び出しは「値が分からない」扱いになり、矛盾が「不明」に落ちます（数え落とし）。効果の行そのものが消えることもあります（誤 clear）。どちらも見落とす側への誤りで、誤警報を出す向きではありません。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_construct_in_tree` が構築するクラスを、呼び出し式に書かれた名前を同じモジュールで引くだけで決める: `from .impl import Runner as R` の別名・`pkg/__init__.py` の再公開・再公開された基底の `__init__` は G3 の `_follow_reexport` を通さず（関数にしか適用していない）、`@classmethod` の中の `cls(...)` は `cls` が局所束縛なので構築にならない。どちらも Obj が作られず、受け手型と `self.<field>` の MODEL が消える。
- **コードの場所**: authgap/val/engine.py:1274-1300 _construct_in_tree（クラスの引き方）, authgap/val/engine.py:1616-1632 _base_classes, authgap/val/engine.py:1717-1754 _follow_reexport
- **重大度の根拠**: 3 観点の重大度の中央値は、2 件とも medium（R1-r2-5 は探索 medium / 設計 medium / 一般性 high、R4-r2-9 は 3 観点とも medium）。向きはどちらも見落とす側。R1-r2-5 は矛が不に移る数え落としで、関数の中で別名 import した形と v2 bbwatch では効果行ごと消える。R4-r2-9 は誤 clear。構文だけで数えた候補の上限は次のとおり（到達するかは見ていない）。R1-r2-5 は v2 の 99 木で、別名でのクラス構築が 10 木・292 箇所、再公開されたクラスの構築が 19 木・2,125 箇所（うち xagent 1,589）、どちらかがある木は 25（一般性観点の count_forms）。R4-r2-9 は、探索役の数え方（vendored を含む）で `@classmethod … return cls(` が 944 箇所・22 木。検証役の数え方（venv / vendored を除く）では、cls(...) を呼ぶ classmethod を含むファイルが 256・42 木、同じファイルの中の `Class.method(` の呼び出しが 178 箇所・25 木。実際に結果が変わる件数は、R1-r2-5 の試作（proto2）で v2 bbwatch を走らせた分しか測っていない。8/8 ユニットに DB 行が増え、readOnly の 4 ツールに新しく D1 矛が立った（原ソースで本物と確認）。postgres-mcp は変化 0 だった。v2 全体と R4-r2-9 の実際の影響は未測定（run20 の db_unresolved から抜き取った 8 サイトには R4-r2-9 の形は無かった）。一般性観点が high とした理由は、bbwatch で D1 の主指標が実際に動いたこと。ただ K7 の前例（候補 32 木に対して、実際に変わったのは 6 木）もあるので、代表値は medium のままにした。D3 / D4 は効果行が消えれば原理上は影響を受けうるが、測っていない。
- **直し方（一般に正しいか: 条件つきである）**: 【A. 別名・再公開・基底（R1-r2-5）】一般性観点の試作 proto2 = patch_proto.py + patch_proto2.py が、次の 4 条件をすべて入れた形。
(i) `_construct_in_tree` は、`dotted` があれば `dotted.rpartition('.')[2]`（import 先の元の名前）でクラスを引く。
(ii) `get_class(strict=True)` が None のときだけ、G3 改訂の条件 1・2 で `_follow_reexport` を辿る。条件 1 は、再公開するモジュールでその名前の束縛がちょうど 1 つで、それがモジュール直下の from-import であり、`_module_writes` に無いこと。条件 2 は、辿る先を `ImportFrom.level` で解くこと。`_follow_reexport` の最後の確認（`_visible_defs`）は、クラス定義も可に広げる。
(iii)【fix_sketch に無い。必須】読む側の条件（G3 改訂の条件 3）をクラスの構築にも掛ける。構築に使う名前（別名なら別名）が読む側のモジュールで 2 回以上束縛されるか、`_module_writes` にあるなら構築しない。既存の `func.id in scope.local_bindings` は関数内の束縛しか見ないので足りない。
(iv)【fix_sketch に無い。必須】`_base_classes` も import 先の名前で引いて再公開を追い、基底名にも (iii) と同じ条件を掛ける（Guard A）。

素朴な直し方で壊れる反例（テストに入れる。一般性観点の木 scratchpad/verify/R1_hm_4/ce5_*）:
・ce5_alias_rebind: `from .impl import Runner as R; from .impl import Safe; R = Safe`。Python では Safe が作られ、正解は 不。別名を import 先の名前で引くだけの直し方だと Runner を構築して 矛（誤警報）になる。
・ce5_alias_global: `global R; R = Safe` の形で、上と同じ。
・ce5_shadow_base: `from pkg import Base`（`__init__.py` で再公開）のあと、読む側で `class Base` を定義し直す。後の束縛が勝つので、正解は 不。fix_sketch に (iii) だけを足した試作（proto）は 矛（誤警報）を出した。(iv) を足した proto2 は 不 のまま。
・(iii)(iv) で既存の誤警報も直る。ce5_plain_rebind（`from .impl import Runner; Runner = Safe` が今は 矛）と ce5_shadow_base_plain。

proto2 の確認結果は次のとおり。所見の 5 形と別名つき基底（ce5_alias_base）は、すべて contradiction:D1 になった。較正対 A9/A18 の 4 木は変化ユニット 0、pytest は exit=0。

直したあとも残る限界（壊れるのではなく届かない）: `from .x import *`、try/except による二重の再公開（ce5_reexport_multi。G5 の数に残るのは設計どおり）、クラス属性の付け替え `Runner.go = f`。Guard A は、`_module_writes` にある同名があると基底を保守的に落としうる。直したら compare_scans で消えた行を 1 件ずつ見る。

【B. classmethod の cls(...)（R4-r2-9）】
fix_sketch の第 1 案（`_class_stack[-1]` = 定義した側のクラスを構築する）は使わない。反例は r9_subclass（scratchpad/verify/R4_hm_5）。`class ReadOnlyStore(Store)` が delete を raise だけに上書きしているとき、`ReadOnlyStore.open()` から Store を構築すると、Store.delete の DB 行が resolved で出る（新しい誤警報）。`class Audited(Store)` が delete を 2 文にしているときは 1 行しか出ず、受け手が resolved なので取りこぼしが db_unresolved にも残らない（誤 clear を隠す）。所見が第 1 案を「上界」と書いたのは誤り。

一般に正しい形は、cls を受け手の式から決めること。`_ev_Call` で、メソッド呼び出しの受け手の式（ast.Name / ast.Attribute）を `_construct_in_tree` と同じ strict な解決で木の中のクラス C に解けるときだけ、C の家族のメソッドに型で解決する。被呼び出しが classmethod なら、第 1 仮引数に「C のクラスオブジェクト」を種付けする。インスタンスが受け手のとき（`Obj.classes` が 1 つで木の中）は type(obj) を使う。`cls(...)` を構築にするのは、名前が実行中の classmethod の第 1 仮引数で、種付けがあるときだけ。そのときは `get_class(strict=True)` を使う。
受け手が Unknown・外部の型・複数の型なら構築しない（今までどおり unresolved）。本体で cls を再束縛する形は、env の上書きで自然に外れる（D58 2(c) と同じ保守的な検査）。
クラスオブジェクトの印は `VALUE_ATTRS`（語彙）に足さず、エンジン側のスタック（`_class_stack` と並べて受け手クラスを積む）で持つ。
`type(self)(...)` と `self.__class__(...)` は範囲外。

【共通】どちらも opaque → resolved の向きなので、CLAUDE.md の敵対的レビューを通す。崩しに行く点は次のとおり。同じ名前のクラスが木に 2 つある場合。cls の上書きや super() への受け渡し。`Sub.open()` が Sub の `__init__` と上書きメソッドに結ばれるか。外部の基底の classmethod を木の中のクラスと取り違えないか。
直したら diff_effects（A9/A18）と compare_scans を回す。v2 は回帰の確認だけに使い、bbwatch の増分を改善として報告しない（D61）。
凍結（D61 最終凍結）後の変更なので、preregistration に逸脱として記録し、指紋を取り直す。
- **記録済みの限界・決定との重なり**: 設計の観点による反証は 2 件とも無い（refuted=false、expected も正しいと判定）。関連する記録は次のとおり。
・D19 K7（呼び出し式の局所の別名で定義を探す）は同じ形の関数版で、D61 G3 で直した扱い（review_plan §5）。G3 の規則本文（「import の意味そのもの」「別名は元の名前で引く」）は名前一般について書かれているが、実装は `_visible_defs` のせいで関数にしか効いていない。クラス側を限界として記録した所は無い（scan_known_defect_forms.py も FunctionDef しか数えない）。
・D17 改訂 2 の厳密化（外部の同名モジュールや基底を取り違えない）は、この直し方でも保たれる。D17 改訂 3 は、import 越しの基底 `__init__` を解くのが意図された挙動だと示している。
・R4-r2-9 に当たる記録は O1〜O41 / D35 の残る限界 / D51 / K1〜K6 のどれにも無い。f0a_checks.md:1262 の `cls(...)` は別の原因。
・どちらの消失も G5 の列（unresolved_in_tree_calls）には数えられず、黙って起きる（規則 4 の趣旨に反する）。
・同じ系統の R1-r4-11（値の再公開。`_module_value` の穴）は直す場所が別で、この単位には入れていない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し（2 件とも D1+D2 に効く所見で、検証役の notes に「D3 / D4 だけなら low」を理由にした格下げは見当たらない）
- **推奨の理由**: 2 件とも代表の重大度が medium で、見落とす側（数え落とし / 誤 clear）に働く。正解は Python の意味から決まり、v2/v3 に合わせた直しではない（D61 の基準 1・2）。一般に正しい直し方があり、条件つきで使える。語彙の追加は要らない。設計の観点でも反証されていない。R1-r2-5 は、条件 (i)〜(iv) を入れた試作で反例が 不 のまま保たれ、較正対も変化 0 だった。R4-r2-9 は、受け手の式でクラスを決める形なら反例を避けられる。ただし解析器（authgap/val/engine.py）の変更で、凍結後の逸脱の記録・再凍結・敵対的レビューが要る。まず試作済みの A（別名・再公開・基底）を入れ、B（classmethod）は受け手の式から決める形だけを入れる、と段階を分ければ危険が小さい。B の敵対的レビューで崩れたら、B だけを限界として記録に回す選択もある。
- **所見**:
  - R1-r2-5: 代表。別名 import・`__init__.py` の再公開・再公開された基底の `__init__` のどれでも、クラスの構築（Obj）ができない。G3 を関数にしか適用していないため。試作 proto2 では、fix_sketch に読む側の条件 (iii) と基底名の条件 (iv) を足さないと誤警報の反例（ce5_alias_rebind / ce5_shadow_base）が出る。重大度は探索・設計が medium、一般性が high。（クラスの構築 `C(...)` が import の意味（別名・`__init__.py` の再公開）を解かない: `from .impl import Runner as R; R(cmd)`、`from pkg import Runne）
  - R4-r2-9: 同じ根本（構築するクラスを呼び出しの名前だけで決める）の別の表れ。`@classmethod` の `cls(...)` が局所束縛として捨てられる。直し方は別の仕組みで、cls を受け手の式のクラスから種付けする。定義した側のクラスで構築する第 1 案は r9_subclass で誤警報・誤 clear になるので使わない。重大度は 3 観点とも medium、誤 clear。（`@classmethod` ファクトリの `cls(...)` が木内クラスの構築にならない（`cls` が局所束縛なので `_construct_in_tree` が None を返し unresolved）ため、`Store.open）

### U15 dataclass 形の構築（`__init__` を書かないクラス）（段階 C・重大度 中・推奨 一部直す）

`@dataclass` のように `__init__` を自分で書かないクラスでは、Python が `__init__` を自動で作ります。この自動の `__init__` は、基底クラスのフィールドを先に受け取り、最後に `__post_init__` を呼びます。解析器はこの 2 つを真似ていません。自クラスのフィールドだけを並べて実引数を割り当て、`__post_init__` は実行しません。その結果、`Job(cmd)` で渡したモデル由来の値が `self.cmd` に入らず、「持ち主不明（OP/opaque）」として読まれます。本当は矛（readOnly なのに `os.system` にモデルの値が届く）なのに、不（判定できない）に落ちます。さらに、`__post_init__` の中にある `os.makedirs` などの効果は 1 行も出ず、数え落としになります。どちらも誤 clear の向きです。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `__init__` の無いクラスの構築（`_construct_in_tree` の `init is None` の枝）が、自クラスの annotated field だけを自クラスの順で実引数に割り当て（基底の field を無視）、生成された `__init__` が呼ぶ `__post_init__` を実行せず、作る Obj の主体を OP にするので、記録されないフィールドの読み出しが OP/opaque になり MODEL が落ち、`__post_init__` の中の sink も出ない。
- **コードの場所**: authgap/val/engine.py:1308-1336 _construct_in_tree（init is None の枝）, authgap/val/engine.py:1338-1351 _find_init, authgap/val/engine.py:533-551 _ev_Attribute（fields に無いフィールド）
- **重大度の根拠**: 代表は R1-r1-8 で、3 つの意見は探索 medium / 設計 medium / 一般性 low、中央値は medium。一般性の検証役が low とした理由は「v2 ではツール経路上にほぼ 0」という件数の見積もりで、旧文言の「D3 / D4 だけなら low」ではない（この単位は D1+D2 に効く）。数えた件数は 2 つあり、定義が違う。設計の検証役は構文上の上限として、同じファイルの基底から注釈つきフィールドを継承し `__init__` を持たないクラスを 1,812 件 / 89 木（413 木中）と数えた。一般性の検証役は v2 の AST で数え、木の中の基底に注釈フィールドを持つ dataclass / BaseModel 派生が 369（13 木）、位置引数か基底フィールドのキーワードで構築する箇所が 61（3 木）だった。61 箇所はどれもツール経路の外。R1-r4-6 は探索 low / 設計 low / 一般性 medium で中央値は low。設計の検証役が low とした根拠は「`__post_init__` に sink を持つ MCP ツールはまれ」という判断で、件数は未測定。R1-r4-6 の半分は効果行が丸ごと消える数え落としで、向きとしてはこの単位でいちばん重い。最終評価のデータで pydantic / dataclass の継承とキーワード構築が多ければ重大度は上がりうる（一般性の検証役の notes）。
- **直し方（一般に正しいか: 条件つきである）**: 場所: authgap/val/engine.py の `_construct_in_tree` の `init is None` の枝（1308-1320）、`_find_init`（1338-1351）。
(a) 基底のフィールドを先に集める（R1-r1-8）: 集め方は `_class_body_defaults` と同じ基底 3 段の鎖（`_base_classes`、import 表で厳密に引く）にする。基底を先に、自クラスを後に並べ、キーワードは全体の名前で束縛する。
  【素朴な直し方で壊れる反例（一般性の検証役が確かめた）】fix_sketch の「鎖の AnnAssign を全部フィールドとみなす」をそのまま入れると、今は正しく矛になっている 3 つの形が不に後退する。(1) 基底の `kind: ClassVar[str] = "job"`、(2) 基底の `created: float = field(init=False, default=0.0)`、(3) dataclass でない基底の素の注釈 `timeout: int`。どれも arg0 が `kind` / `created` / `timeout` に入り、`cmd` が記録されなくなる。
  【避ける条件】基底のフィールドを集めるのは、基底自身が dataclass のときだけ（`@dataclass` / `dataclasses.dataclass`、pydantic なら BaseModel 派生、attrs なら `@define` / `@attr.s`。いずれも import 表で厳密に引く）。`ClassVar[...]` と `field(init=False)` はフィールドから外す。`KW_ONLY` より後のフィールドと `kw_only=True` のフィールドには位置引数を割り当てない。`InitVar` はフィールドだが属性にはならない。自クラスにも同じ規則を当てると、今の自クラスの扱いも正確になる。残る近似（`@dataclass(init=False)`、明示の `__init__` を持つ非 dataclass の基底を `_find_init` が拾う形）は今もある近似で、悪化はしない。補足（本記録者の観察。検証役は触れていない）: pydantic の BaseModel は `__init__(**data)` でキーワードしか受けないので、BaseModel に位置引数を割り当てる今の動きはライブラリの仕様と合わない。
(b) 構築した Obj の主体を実引数から取る（D44 と同じ理屈）: 設計の検証役によれば、(b) だけでは値が MODEL/opaque になるだけで §9.3 により不のままであり、D1 / D2 は変わらない。変わるのは付録の GAP_INJECT / UNKNOWN の座標だけなので、記録止まりとする。
  【素朴な直し方で壊れる反例】主体と root を `_prin_all(args+kwargs)` にして確度を resolved のまま残すと、`__str__` が定数を返す dataclass をオブジェクトごと f 文字列に入れる形（`os.system(f"echo {job}")`）で、resolved の誤警報が出る。
  【避ける条件】オブジェクト全体を使う経路（f 文字列 / `str()` / sink の実引数）は `__str__` / `__repr__` / `__fspath__` を追っていないので、確度を opaque(unresolved) にする。フィールドの読み出しはフィールドの値をそのまま返すので影響を受けない。(a) が正しく入れば、所見の期待（positional / keyword の矛）は (b) なしで満たされる。
(c) `__post_init__` を実行する（R1-r4-6）: `init is None` の枝で、フィールドを入れた後に自クラス → 基底の順で最初に見つかった `__post_init__` を `_descend_env` で実行する。`self.<f>` への書き込みを fields に合流し、効果行も出す（`__init__` の枝と同じ扱い）。
  【素朴な直し方で壊れる反例（一般性の検証役が cx6 で確かめた）】dataclass かどうかを確かめずに実行すると、次の 2 つで実行されない `os.makedirs` が FS_WRITE の行として出て、readOnly との誤警報になる。(1) pydantic `BaseModel` の派生に `__post_init__` という名前のメソッドがある（BaseModel が呼ぶのは `model_post_init`）。(2) `__init__` の無い普通のクラスに `__post_init__` がある（誰も呼ばない）。今はどちらも正しく行が出ていない。
  【避ける条件】(1) 自クラスか基底が dataclass で修飾され（`dataclasses.dataclass` / `pydantic.dataclasses.dataclass`、import 表で厳密に引く）、`init=False` でないときだけ実行する。(2) 自クラス → 基底の順で最初の 1 つだけを実行する。(3) 外部の `__init__` を持つ基底を dataclass が継承する形でも、生成された `__init__` が優先されるので同じ扱いにする。attrs の `__attrs_post_init__` と pydantic の `model_post_init` は、それぞれのライブラリの仕様で条件を付けてから扱う。`InitVar` と `field(init=False)` も同じ枝で扱う。
共通: (a) と (c) は「このクラスは dataclass か」という同じ判定の上に載るので、判定を 1 か所にまとめる。opaque → resolved の向きで、効果行も増えるので、CLAUDE.md の敵対的レビューを通す。反証役の反例木（ce_r8_base_nonfields、ce_r8_obj_in_fstring、cx6）は回帰テストにする。直した後は `diff_effects.py` と `compare_scans.py` で消えた行が無いことを確かめる。ここで直すのは最終凍結の後の変更なので、`docs/preregistration.md` に逸脱として記録し、指紋を取り直す。
- **記録済みの限界・決定との重なり**: 記録済みの限界との重なりは無い（両所見とも設計の観点で反証されていない）。設計の検証役の確認では、D35 の残る限界 3「継承メソッドは分割降下の対象外」（decisions.md:317）と O17 の「継承」（open_questions.md:378）は 2 型の受け手の分割降下の話で、根本原因が違う。D35 のレビュー b の `super().__init__` は `__init__` がある形なので、これも別。O41 と K1〜K7 に dataclass は無い。decisions / open_questions / principles / BRIEF / preregistration を post_init で grep しても、無関係な 1 件（decisions.md:3382）しか当たらない。関連: 構築した Obj の主体が OP なのは `_build_obj`（engine.py:2620-2641）と同じ慣行で、記録された決定でも決定でないとも言い切れない。ただし `_build_obj` は root を運び、`_construct_in_tree` は root を空にしていて、ここは不整合。(b) は D44（未解決の呼び出しの戻り値は入力の主体と root を引き継ぐ）の理屈がオブジェクトの構築に当てられていない形。`opaque(unresolved)` への合流そのもの（D17）は review_plan §5 の設計上の決定だが、主体 OP・root 空はそれとは別。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。この単位は D1+D2 に効き、D3 / D4 だけの所見ではない。R1-r1-8 の一般性 low は「v2 のツール経路上にほぼ 0」という件数の見積もりが理由。R1-r4-6 の探索 low と設計 low は「`__post_init__` に sink を持つツールはまれ」という判断が理由。
- **推奨の理由**: 代表の R1-r1-8 は medium で、条件つきの一般に正しい直し方がある（dataclass のフィールド規則はライブラリの仕様から決まり、v2 / v3 の件数と無関係なので D61 の方針に合う）。語彙の追加は要らず（os.system / os.makedirs は sink 表にある）、設計の観点でも反証されていない。そこで (a) の「基底のフィールドを dataclass の規則で集める」を直す。R1-r4-6（`__post_init__` の実行）は代表値 low だが、次の 3 点から (a) と一緒に直すことを推奨する。(1) 同じ枝の同じ「dataclass か」の判定に載る。(2) 一般性の検証役は medium とした。(3) 効果行が丸ごと消える数え落としの向き。学生が「low でまれ」を重く見るなら、R1-r4-6 は限界として記録に回してよい。(b) の「構築した Obj の主体を実引数から取る」は、設計の検証役の判定どおり付録の座標（GAP_INJECT / UNKNOWN）にしか効かず D1 / D2 を変えない。素朴に入れると f 文字列で誤警報が出るので、記録止まりにする。どれも凍結後の `authgap/` の変更で opaque → resolved の向きなので、敵対的レビューと逸脱の記録が要る。
- **所見**:
  - R1-r1-8: 代表（medium）。前半の (a)「基底の annotated field を無視し、自クラスの順で位置引数を割り当てる」は直す。反例 3 形（ClassVar / field(init=False) / dataclass でない基底の注釈）を避ける条件つき。後半の (b)「構築した Obj の主体が OP・root が空」は、設計の検証役が付録にしか効かないと判定したので記録に回す。f 文字列の誤警報の反例あり。（dataclass 形（`__init__` 無し）の構築で基底クラスの annotated field を無視し自クラスの field 順で実引数を割り当てる。さらに `_construct_in_tree` の Obj は主体 OP な）
  - R1-r4-6: 同じ `init is None` の枝の別の欠落（`__post_init__` を実行しない）。代表値 low（一般性の検証役は medium）。導いたフィールドの矛 → 不と、`__post_init__` の中の sink の数え落とし。dataclass 修飾（import 表で厳密に引く）かつ init=False でないときだけ実行する条件で直すことを推奨する。条件が無いと BaseModel と普通のクラスで誤警報が出る（cx6）。（dataclass 形（`__init__` 無し）の構築で `__post_init__` を一度も実行しない: `__post_init__` で導いたフィールド（`self.cmd = "echo " + self.raw`）は `O）

### U16 暗黙に呼ばれる木内コード（__call__ / with の __enter__・__exit__ / @property の getter / 木内デコレータの wrapper）（段階 C・重大度 中・推奨 一部直す）

Python では、書いた文に呼び出しが見えなくても、言語の側がこちらのコードを呼ぶことがあります。インスタンスを関数のように呼ぶ `r()` は `__call__` を、`with X() as y` は `__enter__` と `__exit__` を、`obj.conn` は `@property` の本体を呼び、`@audited` で飾った関数を呼ぶと wrapper が動きます。解析器は明示の呼び出しにしか降りないので、これらの中の sink（ファイル削除・DB 更新・コマンド実行・ログ追記）や、`__enter__` や property が返す接続の型が消えます。効果行が 1 本も出ないまま「宣言と矛盾なし」に見えるので、誤りは誤 clear の向き（見逃し）に出て、誤警報の向きには出ません。未解決の呼び出しとしても数えられないので、消えたことが表に出ません。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 値エンジンは明示の呼び出しの被呼び出しにしか降りず、Python が暗黙に呼ぶ木内のコードを実行しない: インスタンスの呼び出し `r()` の `__call__`、`with` / `async with` の `__enter__` / `__exit__`（`as` はインスタンスに束縛され、後始末の sink と `__enter__` が返す接続の受け手型が消える）、`@property` / `@cached_property` の getter（`_ev_Attribute` はフィールドと型遷移表しか引かない）、木内デコレータが返す wrapper（`_descend_env` は元の def の本体だけを実行する）。
- **コードの場所**: authgap/val/engine.py:962, 1477, 1661 呼び出し先の解決（__call__）, authgap/val/engine.py:351-356 _exec_stmt With / AsyncWith, authgap/val/engine.py:509-553 _ev_Attribute（property）, authgap/val/engine.py:1055-1082 _descend_env（デコレータ）, authgap/val/engine.py:1557-1572 _class_family
- **重大度の根拠**: 代表値は medium。所見ごとの 3 意見（探索役 / 設計 / 一般性）の中央値は、R1-r3-1（with）が medium/medium/medium、R4-r2-4（property）が medium/medium/medium、R1-r2-8（__call__）が low/low/low、R1-r4-12（デコレータ）が low/medium/low。medium の 2 件は、readOnly と宣言したツールで FS_WRITE / DB の矛が効果行ごと消える誤 clear で、G5（未解決の木内呼び出しの数）にも載らない。探索役の件数はどれも未検証の構文上の上限: with のクラス形は v2 で 17 木 168 箇所（到達性・sink の有無は見ていない）、接続を返す property は 105 箇所 / 17 木（見積もり）。D51 には dejavu の 94 件があり、property と注釈つき代入の 2 つの原因が重なっている。デコレータは設計の検証役が数えた「corpus で functools.wraps を使うファイル 1,869」だけがあり、sink を持つ wrapper の数は未測定。__call__ が low なのは、MCP ツールでまれな書き方だから（全員一致）。どの所見も影響は D1+D2 の自己申告で、D3 / D4 への効きは誰も確かめていない。ただし property の先の NET proxy が消えれば D3 にも効く見込みがある（未測定）。
- **直し方（一般に正しいか: 条件つきである）**: 共通: 受け手の値が木内クラスの Obj で、型で裏付けられるときだけ、Python が暗黙に呼ぶメソッドに降りる。外部型（`_is_external_class`、D61 G4 の条件）は除く。`_class_name_unique` が偽なら、今と同じく降りずに opaque / 未解決として数える。見つからなければ今の挙動のまま。各 dunder / getter は Def 4 どおり深さを 1 消費し、SUMMARY_CAP も使う。解決率と行を増やす向きなので、CLAUDE.md の敵対的レビュー、diff_effects（較正対）、compare_scans（消えた行 0 の確認）を通す。D61 どおり v2 / v3 に合わせた例外は入れない。authgap/ を変えるので、再凍結（fingerprint）と preregistration の逸脱記録が要る。

(1) with / async with（R1-r3-1）: `_exec_stmt` の With / AsyncWith で、文脈式の値が木内 Obj なら `__enter__` / `__aenter__` を受け手つきで降り、その戻り値を `as` に束縛する。本体の後に `__exit__` / `__aexit__` を同じ受け手で降りる。検証役の試作（AG_PATCH=1）で確かめた条件は次のとおり。
(a) `__exit__` の 3 実引数は値として None を渡す。AST の `Constant(None)` を実引数に持つ Call を合成してはいけない。合成すると `_static_params`（engine.py:1944）が exc_type を静的にし、`_static_truth` が `if exc_type is not None: os.remove(...)` の後始末を刈るので、新しい誤 clear になる。試作は `_fake_call(item.context_expr)`（実引数なし）で避けた。
(b) `__enter__` が書いた `self.<f>` を `_construct_in_tree` と同じく受け手の fields に畳んでから `__exit__` に渡す。文脈式にアクセスパスがあれば `_write_back_self` も行う。
(c) `return self` のときは、畳んだ受け手を `as` に束縛する。
(d) 外部基底の CM（`class MyTmp(tempfile.TemporaryDirectory)`）、`open()` / `httpx.Client()`、モジュール水準の `with LOCK:`、`@contextmanager` 関数は変えない（試作で不変を確認した）。
(e) 分岐の合流で 2 型の Obj になったら、各型の dunder に降りる（試作は先頭の型だけ）。
(f) `__exit__` の後始末は経路に非感応で出る（D35 の限界 5 の false-dirty 側）。自作の一時ディレクトリの削除は O41 の「D2 矛」がそのまま表に出るが、§7.1 どおりで却下の理由にはならない。
試作の結果: 較正 14 木で lost 0 / gained 0、pytest 685 passed / 14 xfail（両側比較の 2 ファイルは未完）。

(2) @property / @cached_property（R4-r2-4）: `_ev_Attribute` で base が木内 Obj のとき、自クラス → 基底の順に `lookup_function(f"{cls}.{attr}")` を引く（基底は `_base_classes` で厳密に 3 段）。最初に見つかった定義が property / functools.cached_property で飾られていれば、その getter を `_descend_env` で受け手つきに実行し、`<return>` を値にする。by_name は付けない。素朴な直し方で壊れる反例は prop_mro: 基底が property を定義し、派生が同名の property で上書きして None を返す形。`_class_family` の集合から同名 property を拾うと基底の getter を採り、purge_child に DB 矛の誤警報が出る。避ける条件は MRO 順で最初の定義を採ることで、同名の普通のメソッドやフィールドが先にあれば property として扱わない。ほかの条件は、同名クラスが 2 つある prop_dup では降りない（一意性の守り）、getter が `self._conn` を遅延生成する形は `_write_back_self` で受け手に戻す（prop_side）、の 2 つ。setter つき property ではデータディスクリプタが instance dict より優先されるので、正しくは getter を fields より先に見る。ただし fields を先に見ても今と同じ結果になるだけで、退行ではない。`property(fget)` の呼び出し形と `@ft.cached_property` の別名は試作では拾わないが、拾わなくても opaque のままなので安全側。試作 proto4 の結果: B3a 8/8、B3b 15/15、tests 通過（corpus 走査を除く）、較正 14 木 + prev5 4 木の差分 0。

(3) インスタンスの呼び出し `r()` / `Runner(cmd)()`（R1-r2-8）: 所見の案のように `lookup_function(f"{cls}.__call__")` で直接降りるのではなく、`r.__call__()` と同じ既存の `_resolve_in_tree` の経路に落とす。この経路は型による絞り込み・`_class_name_unique`・by_name の opaque 合流という guard をすでに持っている。反例の確認: c8b（同名 Runner が 2 モジュール）は未解決として数えられ、c8c（`k = Runner; k(cmd)` のクラス参照）は Obj にならないので、構築子の呼び出しと取り違えない。

(4) 木内デコレータ（R1-r4-12）: 一般に正しいのは (a) だけ。デコレータを実行し、返る wrapper の本体を同じ受け手 / 実引数で実行し、中継の形 `fn(*args, **kwargs)` を元の本体への同じ実引数での降下に写す。守りは 3 つ。`**kwargs` を今の `_ev_Call` の扱いで流すと `_run(cmd=cmd)` の cmd が捨てられ、新しい誤 clear になる。wrapper の分で深さを消費すると、MAX_DEPTH=4 の境界で元の本体の効果が新たに落ちるので消費しない。外部デコレータ（lru_cache 等）と登録用デコレータ（mcp.tool）は変えない。所見の案 (b)「木内デコレータがあれば opaque(unresolved) を効果の確度に合流」は誤り。中継だけの `handle_errors`（try/except で `return fn(*a, **kw)`）や恒等の `register` の下にある、今は正しい resolved の spawn_model 矛 3 件が不に落ちる（verdict.py:151-156）。解けないデコレータは G5 と同じく manifest に数えるだけにし、判定には使わない。Def 4 は関数値を持たないので、(a) は設計を伴う変更（L）になる。
- **記録済みの限界・決定との重なり**: 設計の観点で反証された所見は無い（4 件とも refuted=false、expected_is_correct=true）。
- property（R4-r2-4）は既知の先送りと重なる。D51（decisions.md:2758-2767）が dejavu で同じ欠落を見つけ、「DB の受け手を超えた一般的な変更（プロパティへの降下）なのでここでは手を付けない」と書いた。O29（open_questions.md:866-868）にも「深さと無関係に残る形: @property … 未着手」とある。ただし凍結時の限界（D59 / D61 / O41）にも review_plan §5 の既知の問題にも持ち越されていないので、「記録済みの限界」ではなく「観測して先送りした一般的な修正」に当たる。学生が既知として O42 で限界に格上げする選択肢もある。その場合、DB は manifest の db_unresolved に痕跡が残るが NET には site 水準の痕跡が無い、と併記する。
- with（R1-r3-1）: D51 は @contextmanager の関数形だけを扱った。クラス形を扱わない決定も限界の記録も無い。F8 の「async with のコンストラクタ型付け」は外部型の話で、この修正では変わらない。O17(e) は機構を事実として書いただけ。直すと O41（自作の一時ファイルの削除 = D2 矛）と D35 の限界 5（経路非感応）が表に出る。
- __call__（R1-r2-8）とデコレータ（R1-r4-12）: decisions / open_questions / 仕様書のどこにも記録が無い。decorator_list を読むのは `_is_context_manager` だけ。
- review_plan §5 の設計上の決定（MAX_DEPTH=4、opaque(unresolved) への合流など）の言い換えではない。
- 4 件とも G5 の未解決数に載らない黙った消失で、規則 4 に反する。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも影響の自己申告は D1+D2 で、どの検証役も「D3 / D4 だけなら low」を理由にしていない。__call__ の low は MCP ツールでまれな書き方だから（3 意見一致）。デコレータの low（探索役・一般性）と medium（設計）の分かれも、sink を持つ wrapper の頻度の見立ての違いで、旧文言とは無関係。
- **推奨の理由**: with のクラス形（R1-r3-1）と property（R4-r2-4）は、fix の基準をすべて満たす。3 意見とも medium の誤 clear で、Python の言語仕様から正解が決まる一般に正しい直し方があり、語彙の追加は要らず、設計の反証も無い。どちらも検証役の試作で、反例を避ける条件つきで較正の木の差分 0 を確かめてある。__call__（R1-r2-8）は low でまれな書き方なので、基準では限界の記録になる。ただし直し方は既存の `r.__call__()` の経路に落とすだけ（S）で、with と同じ「暗黙の dunder に降りる」補助を共有できる。with / property を直すなら同じコミットに含める選択もある（学生の判断）。デコレータ（R1-r4-12）は中央値が low で、正しい直し方 (a) は関数値を持たない Def 4 を超える設計の変更（L）。kwargs の中継と深さの扱いに新しい誤 clear の罠があるので、今回は限界として記録を推奨する。その場合も規則 4 に従い、黙った消失のままにしないこと。解けない木内デコレータを G5 と同じく manifest の列として数える（判定には使わない）かどうかを学生が決める。確度への opaque 合流にするのは誤り。
- **所見**:
  - R1-r3-1: 代表（medium、3 意見一致、false_clean）。with / async with の木内クラスで __enter__ / __exit__ を実行しない。直す側。条件は、__exit__ に AST の None 実引数を合成しないこと、__enter__ の書き込みを受け手に畳むこと、外部基底は今のまま、の 3 つ。（`with` / `async with` の文脈式が木内クラスのインスタンスのとき `__enter__` / `__exit__`（`__aenter__` / `__aexit__`）を一度も実行・解決しない: `as` の名前は `）
  - R4-r2-4: 同じ原因の別の表れ（medium、3 意見一致、false_clean）。@property / @cached_property の getter を評価しない。直す側。MRO 順で最初の定義を採る（家族集合から拾うと prop_mro で誤警報）、一意性と外部型の守りも付ける。D51 / O29 で先送りの記録があるが、凍結時の限界ではない。（`@property` / `@cached_property` で返す受け手（`store.conn` → `return self._conn`）を `_ev_Attribute` がフィールドと型遷移表でしか引かず、プロパティ本体を評）
  - R1-r2-8: 同じ原因の別の表れ（low、3 意見一致、MCP ではまれ）。r() / Runner(cmd)() が __call__ に解決されない。基準では記録の側。直すなら r.__call__() と同じ _resolve_in_tree の経路に落とす（S）。with と一緒に直す選択もある。（インスタンスの呼び出し `r()` / `Runner(cmd)()` が `__call__` に解決されず、効果行が 1 本も出ない（数え落とし））
  - R1-r4-12: 同じ原因の別の表れ（low / medium / low、count_loss）。木内デコレータの wrapper を実行しない。記録の側を推奨（設計を伴う L）。案 (b) の確度への opaque 合流は、中継デコレータの下の正しい矛 3 件を不に落とすので誤り。記録する場合は manifest に数えるだけにする。（木内で定義したデコレータ（`@audited` = 閉包 `wrapper` を返す関数）で包んだ関数 / ツールを呼ぶとき、`_descend_env` はデコレータを無視して元の def の本体だけを実行するので、wrapper の中の）

### U17 入れ子のスコープ（閉包・内包）（段階 C・重大度 中・推奨 直す）

解析器の値エンジンは、変数の表（env）を関数ごとに 1 枚の平らな表で持っていて、Python の「入れ子のスコープ」を扱えない。そのため 2 つの形で値を取り違える。(1) ツール関数の中で補助関数を def して呼ぶと、補助関数は空の表から始まるので、外側の仮引数 `cmd`（モデルが決める値 = MODEL）を「分からない値」（OP/opaque）として読む。`nonlocal` での書き戻しや `def f(c=cmd)` の既定値も反映されない。(2) `[cmd for cmd in NAMES]` のような内包表記は、ループ変数を外側の表に書き込むので、同じ名前の外側の変数が上書きされる（Python 3 では内包の中だけの変数）。主な向きは誤 clear で、本当は宣言と矛盾する `os.system(cmd)` が「矛盾なし（不）」に落ちる。内包の形では逆向きもあり、外側の定数が MODEL に化けて誤警報になる。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 値エンジンが関数ごとに平らな env しか持たず、Python の入れ子のスコープを実装しない: 入れ子の def（閉包）は新しい空の env で実行するので囲む関数の仮引数・局所変数（MODEL）が opaque(unresolved) の OP になり、`nonlocal` の書き込みは戻らず、`def f(c=cmd)` の既定値の捕捉も評価しない; 内包（list / set / dict / generator）は独自スコープを作らず、ループ変数を囲む関数の env に束縛して同名の外側の変数を上書きする。
- **コードの場所**: authgap/val/engine.py:1030-1107 _descend_env（seed が空）, authgap/val/engine.py:375-376 入れ子の def 文（降りない）, authgap/val/engine.py:1836-1845 非リテラルの既定値を評価しない, authgap/val/engine.py:700-717 _ev_ListComp / 内包
- **重大度の根拠**: 代表値は探索役・設計・一般性の 3 意見の中央値。R1-r2-4 は medium / medium / medium。R1-r2-3 は medium / medium / low で、中央値は medium。R1-r2-3 の一般性の観点が low としたのは、「内包の後でその名前を読む形は珍しい」という頻度の判断による。影響は D1+D2 なので、旧文言「D3 / D4 だけなら low」とは関係ない。頻度は検証役が数えた構文上の上限で、効果に届くかは数えていない。閉包は「囲む関数の局所変数を読む入れ子 def」で、直接呼ぶもの 2361 箇所、executor / Thread 経由 161 箇所（87 木中 55 木、verify/R1_hm_3/incidence.out）。内包は「外側の束縛を隠し、内包の後で再代入より前に読む」厳密版で 50 箇所（87 木中 9 木、incidence_comp_strict.out）、緩い上限は 6551 箇所 / 65 木。何件の判定が実際に変わるかは未測定で、野外 8 木の標本では変化 0。閉包の形（to_thread / run_in_executor / 再試行の包み / コールバック）は MCP サーバでよく見るので、単位としては medium とした。
- **直し方（一般に正しいか: 条件つきである）**: 【内包 R1-r2-3】所見の案（inner = env.copy() で評価し、walrus だけ書き戻す）を字義どおりに入れてはいけない。反例: 副作用のために内包を使う形で、今は正しい矛が不に落ちる（新しい誤 clear、5 ユニットで確認）。
- `parts = []; [parts.append(n) for n in names]; subprocess.run(parts)`
- `argv = ["echo"]; [argv.append(n) for n in names]; os.system(" ".join(argv))`
- `any(parts.append(a) for a in args)`
Python では内包の中の自由変数は外側の同じオブジェクトを指すので、中での変更は外に残る。一般に正しい直し方: 内包が新しく束縛するのは target の名前だけなので、表は複製しない。評価の前に target 名の束縛を退避し、評価の後に戻す（元が無ければ消す）。walrus（:=）には触らず、PEP 572 どおり外側の表に残す。属性・添字を target にする内包（`[0 for a.b in xs]`）は退避の対象外でよい。この形を試した版（patched/r3b）での結果は次のとおり。
- 再現 4 ユニットが期待どおり（MODEL が隠された 3 件は矛、定数が隠された 1 件は不）
- 副作用の反例 5 ユニットは矛のまま
- 入れ子の内包、内包の中の walrus も正しい
- 野外 8 木で効果行 40→40、注記 4→4
- 既存テスト（pytest）の完走は未確認

【閉包 R1-r2-4】所見の案（呼び出し元の表の素の名前を seed に足す／nonlocal を書き戻す／非リテラルの既定値を呼び出し元の表で評価する）を字義どおりに入れると、4 つの形を壊す。
- (1) 既定値を呼び出し時に評価してしまう。`cmd="ls"; def _go(c=cmd); cmd=p; _go()` で誤警報、逆の順序では誤 clear になる。
- (2) 入れ子 def が `global cmd` と宣言しているのに外側の MODEL を注入し、誤警報になる。
- (3) 素の名前だけを渡し `self.cmd` を渡さないので、`__init__` の既定値 "ls" を resolved で読む。今の opaque より悪い、黙った誤 clear になる。
- (4) `threading.Thread(target=_go)` の後で名前を束縛し直してから `start()` する形で、登録時の値を resolved で注入し、誤警報または黙った誤 clear になる。

避ける条件は (a)〜(f)。
- (a) 囲む関数が「いま実行中の関数」のときだけ（関数スタックで判定）自由変数を seed する。返された閉包を別の関数から呼ぶ形では seed しない。
- (b) `global` と宣言された名前は除く。
- (c) `self.x` のような dotted の鍵も、先頭が自由変数なら渡す。
- (d) 非リテラルの既定値は def 文の実行時に囲む表で評価して保存し、呼び出し時はそれを使う（言語リファレンス 8.7）。今の engine.py:375 は def 文で何もしないので、ここに手が入る。
- (e) INDIRECT（Thread / to_thread など遅延実行）経由では、入れ子 def より後で束縛し直される名前を `_opaque_deep` で渡す。O33 により MODEL/opaque は不のままなので、新しい矛は作らない。
- (f) `nonlocal` は sub の値を書き戻す（env_join は片側だけの束縛も残す）。

この形を試した版（patched/r4c）では、再現 7/7 が矛になり、反例 7 ユニットはすべて現行と同じか正しい側。野外 8 木で差は 0。既存テストの完走は未確認。

【共通】解決率を上げる向き（opaque → resolved）の変更なので、CLAUDE.md の落とし穴に従う。
- 実装の後で敵対的レビューを通す。
- diff_effects.py（較正対）と compare_scans.py（v2 の run 前後）を通し、消えた行・増えた行を 1 件ずつ確かめる。
- tests/test_f0a_defects.py:1036-1041（D17 改訂 2 の固定テスト。入れ子関数が外側の局所変数 COMMAND を読む）の期待が、新しい挙動（MODEL）と両立するかを確かめる。
- authgap/ を変えるので、凍結の指紋は変わる（再凍結が要る）。
- **記録済みの限界・決定との重なり**: 設計の観点は、2 件とも反証しなかった（refuted=false）。

【閉包】部分的に重なる記録が 3 つある。
- (i) analyze.py の `_closure_seed` の docstring に「外側の関数の本体で代入された自由変数は扱わない」とある。ただしこれは、ユニットの入口（register(mcp, store) の中のツール）では外側の本体が実行されず表が無い、という別の根拠による限界。今回の形は、ツール本体の中の入れ子 def をツールから呼ぶもので、呼び出し元の表があるのに捨てている。
- (ii) D17 改訂 2（decisions.md:1674）は、入れ子関数が掴む同名の外側局所変数を定数の OP にしていた誤りを opaque に直した。決めたのは「定数を読まない」ことで、opaque を最終の答えとしたわけではない。D57 §9.3 以降は opaque も不に落ちるので、今は誤 clear になる。
- (iii) K4 / K5 は入れ子 def の解決先を決め打つ別の欠陥で、今回は解決先が正しく決まった後の表の問題。D17 の「直す」表（decisions.md:1616）は、クロージャ変数を直す対象に挙げている。engine.py:375 の「入れ子定義は別ユニット。ここでは降りない」は、定義時に本体を実行しないという Python どおりの扱いで、決定ではない。R1-r1-4（lambda の本体を評価しない）とも別。
学生がこれらを既知の限界と読む余地はあるが、根拠が違うと検証役は判定した。

【内包】val 側に決定の記録は無い。仕様書 413 行とゲート側 cfgbuild.py:18 / 521-525 は、内包を別スコープ（合成した無名関数）として扱っており、所見と同じ立場。D58 改訂 2(c) が内包の対象を「束縛し直し」と数えるのは、静的な仮引数を狭める保守側の規則で、直しと矛盾しない。

K1〜K7・O1〜O41 に同じ根本原因は無い。

副次的な観察（この単位の外）: 同名の入れ子 def が木に 2 つ以上あると `_pinned_candidates` が降りず、効果が全部消える（数え落とし、K4 / K5 の家族）。別の所見として扱う価値があると検証役が書いている。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R1-r2-3 の一般性の観点が low としたのは「同じ名前を外側でもループ変数でも使い、内包の後で読む形は珍しい」という頻度の判断で、影響は D1+D2。旧文言「D3 / D4 だけなら low」は使われていない。R1-r2-4 は 3 意見とも medium。
- **推奨の理由**: 「直す」の基準を満たしている。
- 代表の重大度は medium（D1+D2、主な向きは誤 clear）。
- 正解は Python のスコープ規則（LEGB、nonlocal、既定値は def の実行時に評価、内包は独自スコープ、PEP 572）だけで決まり、検証データに依らない（D61 の基準 1・2）。
- 凍結した語彙の追加は要らない。
- 設計の観点は反証していない（記録済みの限界とは根拠が違う）。

ただし「一般に正しい」のは条件つき。所見の案をそのまま入れると新しい誤 clear と誤警報を作ることを、検証役が反例で示している。内包は target の退避と復元、閉包は (a)〜(f) の形で入れること。さらに、解決率を上げる変更なので、敵対的レビュー、diff_effects.py、compare_scans.py を通すことが前提になる。検証役の試作版（r3b / r4c）では再現も反例も正しい側になったが、既存テストの完走は未確認。2 件は同じ根本原因（平らな表）なので、まとめて直して一度に再凍結するのが効率がよい。
- **所見**:
  - R1-r2-4: 代表。閉包（入れ子 def）を空の表で実行するので、外側の MODEL が opaque の OP になり、nonlocal と既定値の捕捉も落ちる（誤 clear、7 ユニットで再現）。3 観点とも medium。所見の案は 4 つの反例で壊れるので (a)〜(f) の条件つきで直す（入れ子の関数（閉包）を新しい空の env で実行するので、囲む関数の仮引数・局所変数（MODEL）が `opaque(unresolved)` の OP になり、`nonlocal` の書き込みは戻らず、`def f(c=cmd)` の既定）
  - R1-r2-3: 同じ根本原因の別の表れ（内包が独自スコープを作らない）。誤 clear が主で、誤警報の側もある（4 ユニットで再現）。medium / medium / low。env.copy() の案は副作用のための内包で誤 clear を作るので、target 名の退避と復元で直す（内包表記（list / set / dict / generator）のループ変数を囲む関数の env に束縛するので、同名の外側の変数が上書きされる: MODEL の変数が定数に落ちる（誤 clear）／定数が MODEL になる（誤警報）

### U18 ジェネレータの yield が呼び出し元に届かない（段階 C・重大度 中・推奨 直す）

ジェネレータは yield を使って値を 1 つずつ返す関数です。これを for / async for / join / 内包表記で読むと、yield した値が呼び出し元に届きません。解析器はその値を「中身の分からない定数」(OP/resolved の Unknown) として扱います。そのため、ツールの引数 (MODEL) から作ったコマンドやパスを os.system や open('w') に渡していても出所が消え、本来「矛」(宣言と実際の動作の矛盾) と出るべきものが「不」(判定できない) になります。見落とし (誤 clear) の向きの誤りで、しかも opaque (不明) ではなく resolved (解決済み) に見えるので、どこにも気づく手がかりが残りません。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_descend_env` の戻り値は `<return>` だけで、`yield` / `yield from` を持つ関数の `<yield>` を列（`Seq((), tail=y)`）として返さないので、`for` / `list()` / `join` / 内包で消費すると yield した MODEL の値が OP/resolved の Unknown になる。
- **コードの場所**: authgap/val/engine.py:1091-1107 _descend_env の戻り値, authgap/val/engine.py:661-678 yield / yield from
- **重大度の根拠**: 3 観点 (実行 / 設計 / 一般性) の意見はすべて medium で、誤 clear の向きも一致している。D1 (spawn: shell_string) と D2 (fs_writeout: path) の主指標で、矛が不に落ちる。値が opaque ではなく OP/resolved になるので黙って消える。これは D17 改訂 2 が最も重い向きとした「MODEL → 定数の OP/resolved」と同じ向き。構文上の上限は、母集団 v2 で「定数でない値を yield するジェネレータ定義」が 46 木に 1094 個 (一般性の検証役が incidence.out で数えた。ツールから到達するかは見ていない)。実際に矛が不に落ちている件数は未測定。影響は D1+D2 なので、旧文言「D3 / D4 だけなら low」の影響は受けていない。
- **直し方（一般に正しいか: 条件つきである）**: 【直す場所】authgap/val/engine.py の _descend_env で戻り値を決める所 (1091-1097)。被呼び出し関数の本体に yield / yield from がある (入れ子の def / lambda / class の中は除く) なら、その関数をジェネレータとみなす。@contextmanager / asynccontextmanager の場合 (D51) は今のまま <yield> を返す。それ以外のジェネレータでは <return> を使わず、sub.get("<yield>") から作った列 (Seq) を返す。<yield> が無ければ空の Seq にする。<return> より先にジェネレータかどうかを判定すること。今は `return v` を持つジェネレータで、呼び出しの値が v になってしまう (StopIteration.value が呼び出しの値にすり替わる)。

【素朴な直し方で壊れる反例 (一般性の検証役。必ず避ける)】探索役の sketch どおり全部の yield を 1 つに join して `Seq((), tail=<yield>)` を返すと (patched/r2)、次の書き方で新しい誤警報 (不 → 矛) が出る。
- ce2_direct_gen: `def _argv(t): yield "ping"; yield "-c"; yield "1"; yield t` を `subprocess.run(_argv(target))` にそのまま渡す。POSIX の Popen は list(args) するので正しいコードで、argv0 は定数 "ping"。ところが全 yield の join で argv0 が MODEL になり、contradiction:D1:spawn_model になる。同じ argv をリストで書いた対照 (ce2_list_baseline) は argv0 'ping' で不なので、リストで書くかジェネレータで書くかだけで結果が変わってしまう。
- ce2_prefix_gen: `yield "ping"; yield "-c"; for n in names: yield n` をそのまま渡す。先頭だけ全か無かで扱う直し方 (patched/r2b) でも誤警報が出る。

【避ける条件 = 一般に正しい直し方】リスト表示や append の連なりに既に使っている D17 改訂の規則 (共通の先頭は要素ごとに join し、はみ出しを tail に畳む) をジェネレータ本体にも当てる (patched/r2c 相当)。本体の先頭に続けて並ぶ `yield <式>` 文 (docstring は飛ばす) は、それぞれ 1 回ずつ順に実行されるので、位置つきの要素にする。それ以外の yield (ループや分岐の中、yield from、先頭の連なりより後のもの) は tail に join する。検証役の scratch 版 r2c では、反例 2 木はどちらも argv0 'ping' で不のまま、再現の矛はすべて保たれ、@contextmanager と .send() は変わらなかった。

【守ること (こちらで足した条件。検証役の実測ではない)】
(a) 位置つきにするのは、本体直下の ast.Expr(Yield) が途切れずに並ぶところまでに限る。if / try / with / 代入の yield (`x = yield v`) が 1 つでも挟まれば、そこから後はすべて tail にする。
(b) yield 式そのものの結果 (.send() の値) は今どおり dynamic のまま変えない。`x = yield from g()` の結果 (サブジェネレータの return 値) も dynamic のまま変えない。
(c) MAX_DEPTH (D54) などで本体に降りなかった呼び出しは今どおりにし、この規則で resolved を作らない。
(d) 戻り値の注釈で型を与える処理 (1099-1105) が、ジェネレータの Seq を Obj で上書きしないことを確かめる。今は `not (isinstance(ret.shape, Obj) ...)` という条件なので、Seq でも注釈の型に置き換わりうる。`-> Iterator[str]` などが ANNOTATION_TYPED_RECEIVERS に当たる場合を点検する。

【直しても届かないもの】`list(gen)` の形 (list_of_gen) は、別の限界 (list() / tuple() に非リテラルの引数を渡したときの TRANSFER が無く、opaque(unresolved) になる) があるため、この直し方だけでは MODEL/opaque の不のまま残る。期待値 5/5 のうち届くのは 4/5 (for / async for / join / 内包 / yield from の連鎖と write_gen_paths は届く。検証役の実測)。

【手順】CLAUDE.md に従う。反例 2 木と再現 2 木をテストで先に固定し、実装してから scripts/diff_effects.py と compare_scans.py で前の run と突き合わせる。行が増える向きの変更なので、敵対的レビューで「MODEL にしてよい根拠」を 1 件ずつ崩しに行く。r2c での tests/ の実行は、残っているログ (verify/R1_hm_3/pytest_r2c.out) が途中で切れていて、合否は未確認。野外の突き合わせは run20 の速い順 8 木で、消えた 0 / 増えた 0 (検証役の実測)。
- **記録済みの限界・決定との重なり**: 設計の観点は反証していない (refuted=false)。D51 は、@contextmanager の yield を戻り値にすることと、yield 式の結果 (.send() の値) を dynamic にすることだけを決めた。普通のジェネレータを反復して得る値の扱いは、decisions / open_questions / preregistration のどこにも決めていない。O41 と K1〜K7 にもジェネレータは無く、review_plan §5 の既知の問題とも重ならない。tests/test_receiver_resolution_more.py:65 の gen_plain は定義されているだけで、どのツールからも使われていない (正例としても反例としても固定されていない)。仕様書 AUTHGAP_BRIEF_v3.md:278 の「generator 越しは opaque」は config atom の文脈だが、ジェネレータを越えた値を resolved にしない立場で、今の実装 (OP/resolved) はそれより弱い。隣の限界として、list() / set() などの構築子が未解決になる問題が R1-r5-3 (別の単位) にある。list(gen) が届かないのはそちらの原因。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。影響は D1+D2 で、3 観点とも medium。旧文言で下げた形跡は無い。
- **推奨の理由**: 代表の重大度は medium (3 観点一致) で、見落とし (誤 clear) の向き、しかも resolved なので黙って消える。正解は Python のジェネレータの意味から v2 / v3 と無関係に決まり (D61 の基準 1)、どの木にも現れうる書き方 (基準 2) で、凍結した語彙の追加も要らない。設計の観点も反証していない。ただし探索役の sketch そのままでは反例 2 木で新しい誤警報が出るので、検証役が示した接頭辞規則 (patched/r2c 相当) で入れることを条件にする。list(gen) の取りこぼしはこの単位では直らないため、R1-r5-3 の採否と合わせて扱う。authgap/ を変えるので指紋は変わり、再凍結の前にまとめる必要がある。
- **所見**:
  - R1-r2-2: 代表 (この単位の唯一の所見)。for / async for / join / 内包 / yield from の連鎖と、パス列の書き出しで MODEL が OP/resolved の Unknown に落ちる。3 観点で生存し、重大度はすべて medium。一般性の検証役が sketch の反例 2 木と、それを避ける接頭辞規則を示した。list(gen) の形は R1-r5-3 側の限界で、この単位では直らない。（ジェネレータ関数（`yield`）を `for` / `async for` / `list()` / `join` / 内包で消費すると、yield された値が呼び出し元に流れず、MODEL 由来の値が OP/resolved の Unk）

### U22 G4 / D50 の注釈による受け手型付け（経路の欠け・Optional の書き方・None リテラル）（段階 C・重大度 中・推奨 一部直す）

解析器は `conn: sqlite3.Connection` のような型注釈を読んで、「`conn.execute(...)` は DB への書き込みだ」と判断する（D50 / G4）。ところがこの読み取りは「補助関数に降りるとき」にしか働かない。クラスの `__init__` で受け取った接続（`self.conn`）や、`register(mcp, conn)` のように外側の関数から閉包へ渡した接続・HTTP クライアントには型が付かない。そのため DB や HTTP の効果が 1 行も出ず、readOnly なのに書き込むツールが「問題なし」に見える（誤 clear）。同じ仕組みの穴がほかに 2 種類ある。1 つは `t.Optional[...]`、`Union[X, None]`、`Optional["X"]` といった書き方で型を読み落とすこと（数え落とし）。もう 1 つは既定値のリテラル `None` にまで型を付けるため、`if conn is None: return` の先にある到達しない呼び出しが行として出てしまうこと（誤警報）。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 注釈から受け手型を付ける G4 / D50 の実装が狭く、経路も欠ける: `_annotation_receiver_type` / `_annotation_head` は Optional の包みを字面の `Optional` / `typing.Optional` でしか外さず（`import typing as t` / 別名 / `Union[X, None]` を解かない）、包みの中の文字列の前方参照 `Optional["sqlite3.Connection"]` を読まない; `_seed_params` はリテラルの None（既定値・明示の実引数）まで型付きの Obj に置き換えて O31 の `if conn is None: return` を刈れなくする; 型付けは降下の `_seed_params` にしか無く、入口の種付け（`_self_fields` の `__init__` 仮引数、`_closure_seed`）では適用されない。
- **コードの場所**: authgap/val/engine.py:2351-2396 _annotation_receiver_type / _annotation_head, authgap/val/engine.py:1519-1549 _annotation_type, authgap/val/engine.py:1781-1810, 1852-1858 _seed_params, authgap/analyze.py:369-376 _self_fields（__init__ 仮引数）, authgap/analyze.py:280-288 _closure_seed
- **重大度の根拠**: 代表は R1-r3-8。探索役・設計・一般性の 3 意見がすべて medium で、依存性注入（DI。`__init__` の仮引数や閉包を囲む関数の仮引数で接続を渡す形）という特定の書き方でだけ起きるが、MCP サーバではよく使う形。効果行そのものが消える本物の誤 clear で、NET は db_unresolved にも痕跡が残らないため compare_scans でも見えない。件数は未測定（D50 の集計の Session 注釈 696 件は降下の仮引数だけを数えたもの）。他の 3 件は 3 意見とも low。R1-r5-5 は探索役が v2 の 99 木を数えた上限で、Union[X, None] が 1 木に 2 箇所、別名の Optional は 0 箇所。R1-r4-14 は件数未測定で、設計の観点の意見は「頻出ではない」。R1-r4-8 は件数未測定。4 件とも影響は D1+D2 なので、D62 の前の旧文言（D3 / D4 だけなら low）とは関係しない。
- **直し方（一般に正しいか: 条件つきである）**: 【R1-r3-8（直す）】
- `_self_fields`（analyze.py:367-372）では、`init_env.set(p.name, ...)` の前に、その ast.arg の注釈で `engine._annotation_type(annotation, init_scope)` を引く。型が返れば `Value(OP, RESOLVED, Obj((cls,), ()))` で種付けする。
- `_closure_seed`（analyze.py:285-288）では、`_annotated_class` が None のときに `_annotation_type(a.annotation, mscope)` を試し、それでも付かなければ `_seed_from_annotation` に進む。
- 守る条件（検証役）:
  (1) 既知の型を上書きしない。例: `self.conn = Store()` の Svc2.method_wrapped は今も修正後も同じ行になる。
  (2) `_annotation_type` の D61 追記の健全性条件（2 回束縛・相対 import・木の中のモジュールの import なら付けない）をそのまま使う。
  (3) 外部の型を木の中のクラスへの絞り込みに使わない（D61 G4 の穴の条件）。
  (4) `_self_fields` は init_res を捨てているので、`annotation_typed` の記録をユニットの報告に届ける配線を足す（D50 の「注釈は宣言であって証明ではない」を切り分けるため）。結果はクラス単位でキャッシュされ、そのクラスの全ツールに効く。
- 反例探し（ce8a_intree_execute）の結果: 末尾名で木の中の同名メソッド（Store.execute の os.system）へ降りる SPAWN 行は残り、DB 行が加わるだけで、消える行は無かった。`X | None = None` の閉包変数も Optional をほどいて型が付く。
- 副次点（PIPE の受け手型 subprocess.Popen / asyncio.subprocess.Process を `_ANNOTATION_TYPES` に足す案）は G4 の文言「proxy の受け手の型」の外で、別の決定になる。足す場合の期待は EXEC ではない。argv0 / shell が注釈から決まらないので、上界の FS_WRITE(content) 行になる（D61 改訂の G1 取り消し）。今回は入れない。
- 解決率を上げる向きなので、実装より先に tests に固定する。正例は 4 ユニット（method_net / method_db / closure_net / closure_db）、反例は木の中の同名クラス・2 回束縛・`self.conn = Store()`・`X | None`。取り直しの後、diff_effects と compare_scans で「消えた行 0」を確かめ、敵対的レビューを通す。

【R1-r4-14（low。直すなら R1-r5-5 と同時）】
- Optional や `|` をほどいた後の node が文字列の ast.Constant なら、`ast.parse(value, mode="eval").body` で読み直してから先に進む。
- この処理は `_annotation_receiver_type` と `_annotation_head` の両方に同じ順序で入れる。1 つの補助関数にまとめるのが安全。
- 素朴な直し方で壊れる反例（検証役）: `from sqlite3 import Connection` の後に木の中で `class Connection` を定義し、`Optional["Connection"]` と書く形。`_annotation_receiver_type` だけを直すと head が None のままになり、`_annotation_type` が束縛の検査を飛ばす。その結果 sqlite3.Connection が付いて誤警報になる。
- 補足: `"X" | None` は `from __future__ import annotations` の外では実行時に TypeError になる書き方で、大事なのは `Optional["X"]` の側。

【R1-r5-5（low・第 5 回で事前登録の手続きの外。直すなら R1-r4-14 と同じ補助関数で）】
- 所見の sketch（包みの判定を `resolve_call_name(...) == "typing.Optional"` に置き換える）はそのままでは誤り。検証役が見つけた反例は 2 つ。
  (1) `from typing import *` の `Optional[...]`: resolve_call_name が None を返し、今は正しく出ている矛の行が消える。
  (2) `from typing_extensions import Optional`: `typing_extensions.Optional` と一致せず、行が消える。
- 避ける直し方:
  - 今の字面一致は残す。そのうえで、import 表で解いた名前が {typing, typing_extensions}.Optional のときも包みとして外す。
  - Union も同じ集合で扱う。要素がちょうど 2 つで片方が None リテラルのときだけ、`X | None` の分岐に合流させる。
  - `_annotation_head` と `_annotation_type` の束縛の検査を、包みの名前（木の中で自前に束縛した Optional / Union / t）にも掛ける。

【R1-r4-8（限界として記録を推奨。直すなら D58 規則 1 の改訂として逸脱に記録）】
- 直し方: `_seed_params` で、値の形が `Atom(none=True)`（リテラル None の既定値か、明示の None 実引数）のときは注釈による型付けを飛ばす。
- 一般性の観点の反例探し（patched8）では、次の形で行は残り、壊れる形は見つからなかった。
  - `if conn is None: conn = sqlite3.connect(...)` と束縛し直す形
  - 実物の接続を渡す形（passes_real_conn）
  - `conn = conn or _get_conn()` の形（今も行なし）
- 別案（型を保ったまま、元が None であることを `_static_value` に読ませる）も一般に正しいが、変更の範囲が大きい。
- 入口の種付けの経路（R1-r3-8 の修正）の仮引数は Atom(formal) で、リテラル None ではない。したがって、この飛ばしの条件とは干渉しない。
- **記録済みの限界・決定との重なり**: - D50（decisions.md:2633-2636）は注釈の型付けを `_seed_params` の機構として書いているが、どの種付け経路に当てるかは限定していない。
- D61 G4 は対象の型を PROXY_SINKS の受け手型へ機械的に広げたもので、G4 の穴（外部型を木の中の同名クラスに結ぶ誤警報）と改訂の追記（2 回束縛・相対 import・木の中のモジュールの import なら付けない）は、この単位の直し方がそのまま守る条件になる。
- D17 の表（decisions.md:1616）は「__init__ の self フィールドやクロージャ変数に受け手型が付かず sink を落とす」を、直す対象の false-clean にしている。R1-r3-8 はこの方向と一致する。
- 近いが別のもの:
  - D51（注釈付き代入と木の中のクラスの注釈は手を付けない）。
  - `_closure_seed` の docstring が限界として書く「外側の関数の本体で代入された自由変数」。
  - 仕様書 517 行目の「入口仮引数は注釈の文字列だけ・型環境は作らない」は D50 より前の記述で、D50 / G4 で既に改められている。
- R1-r4-8 は設計の観点で反証された（confidence 0.6）。D58 規則 1（decisions.md:3140-3142）が「注釈による受け手の型付け（D50）は既定値 None の後にかかるので、`db: Session = None` の型は失われない」と明記しており、D58 改訂の規則 4 で `_static_value` は Atom しか読まない。今の出力は書かれた規則どおりになる。ただし設計の観点も「guard-return 形の刈り込みが効かなくなることまで検討した記録は無い」「直し方は一般に正しい、採るなら逸脱として記録」と書いている。一般性の観点は反証していない。
- R1-r5-5 は第 5 回の所見で、review_plan §7.3 により事前登録の手続きの外。表では分けて示す。
- review_plan §5 の既知の問題（O35 / O38 / O39 / O41、K1〜K6、MAX_DEPTH など）とは重ならない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも影響は D1+D2 で、検証役の reason / notes に「D3 / D4 だけなら low」を理由にした記述は無い。low の 3 件（R1-r4-14 / R1-r5-5 / R1-r4-8）は、稀さ（R1-r5-5 は v2 の上限で 2 箇所 / 1 木）と誤警報の向きを理由にしている。
- **推奨の理由**: - 代表の R1-r3-8 は次の条件をすべて満たすので、推奨の基準で fix に当たる: 3 観点とも medium・false_clean、設計・一般性の両方で反証されず、fix_is_general も両方 true、語彙の追加が要らず、既存の D50 / G4 の規則を種付けの残り 2 経路に同じ健全性の条件で当てるだけ、反例探しで消える行が無い。
- R1-r4-14 と R1-r5-5 は同じ関数の low の穴で、一般に正しい直し方はある（条件つき）。ただし R1-r5-5 は母集団で稀（v2 の上限で 2 箇所 / 1 木）で、しかも事前登録の手続きの外の所見。R1-r4-14 も件数未測定で、設計の観点は「頻出ではない」としている。基準の「low でまれな書き方」に当たるので、限界として記録を推奨する。直すなら 2 件を 1 つの補助関数で同時に直し、fix_outline の反例（typing の星 import、typing_extensions、木の中の同名クラスで head が None になる形）を先にテストに固定する。
- R1-r4-8 は設計の観点が D58 規則 1 の明記どおりと判定したので、限界として記録を推奨する。直し方自体は一般に正しく、反例も無い。学生が採るなら D58 規則 1 の改訂として `docs/preregistration.md` に逸脱を書く。
- どの部分を直すにしても解決率を上げる向きなので、CLAUDE.md の敵対的レビューと、diff_effects / compare_scans による「消えた行 0」の確認が要る。
- **所見**:
  - R1-r3-8: 代表（medium・false_clean）。`_self_fields` の `__init__` 仮引数と `_closure_seed` の外側関数の仮引数に注釈の型付けが無く、DI で渡した DB / NET の proxy 行が消える。3 観点とも生き延び、直し方も一般に正しい → 直す（D50 / G4 の注釈型付け（`sqlite3.Connection` / `httpx.Client` などの受け手型）が `_seed_params`（降下のとき）にしか無く、`_self_fields`（メソッド形ツールのクラスの ）
  - R1-r4-14: 同じ原因の別の表れ（low・count_loss）。Optional / `|` の中の文字列の前方参照を読まない。直すなら `_annotation_head` にも同じ処理を入れる条件つき。稀なので限界として記録を推奨（直すなら R1-r5-5 と同時）（G4 / D50 の注釈型付けが、`Optional[...]` / `X | None` の**中**に書いた前方参照の文字列（`conn: Optional["sqlite3.Connection"]`、`conn: "sqlite3.）
  - R1-r5-5: 同じ原因の別の表れ（low・count_loss、第 5 回で事前登録の手続きの外）。`t.Optional`、`Opt`、`Union[X, None]` を外さない。sketch そのままでは星 import や typing_extensions の行が消えるので、字面一致との合併が条件。v2 の上限は 2 箇所 / 1 木と稀 → 限界として記録を推奨（G4 / D50 の注釈型付けが `Optional` の包みを import 表で解かず字面 `"Optional"` / `"typing.Optional"` でしか外さない（`_annotation_receiver_type` :）
  - R1-r4-8: 同じ仕組みの逆向きの表れ（low・false_alarm）。リテラル None に型を付けて `is None` の guard を刈れない。設計の観点で D58 規則 1 の明記どおりと反証済み（一般性の観点は反証せず、直し方は一般に正しい）→ 限界として記録を推奨。採るなら D58 の改訂として逸脱に記録（G4 / D50 の注釈型付け（`_seed_params`）がリテラルの `None`（`conn: Optional[sqlite3.Connection] = None` の既定値、または明示の `None` 実引数）を `Obj(s）

### U24 _self_fields の作り方（メソッド形ツール / 閉包の self の種）（段階 C・重大度 中・推奨 一部直す）

メソッドの形で書いたツール（`self.conn.execute(...)`）では、解析器が「self にどんなフィールドがあるか」を `_self_fields` という専用の関数で推測する。この関数は、モジュール水準でインスタンスを作ったときに使う仕組み（基底クラスまでたどる）を使わず、自分で走査している。そのため (1) 基底クラスの `__init__`・`super().__init__()`・基底のクラス属性で作った接続が見えず、SQL の実行などの効果が消える（誤 clear）。(2) クラス体の走査の条件が逆で、`base_sql` から `sql` のような存在しないフィールドを作って本物より先に入れ、DELETE を SELECT と読むなどの誤りも起きる（どちらの向きの誤りにもなる）。(3) `__init__` で None にしておき `connect()` で接続する遅延初期化は見えないが、これは設計どおり「不明」として記録されている（直さない側）。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: メソッド形ツール / 閉包の注釈つき引数の `self` を種付けする `_self_fields` が、構築の機構（`_find_init` / `_class_body_defaults` / `__init__` の実行）を使わず独自に走査する: クラス体の走査は条件が逆（`if not name.startswith("self.")` の後で `name[len("self."):]`）で `base_sql` → `sql` のような捏造フィールドを本物より先に入れ、自クラスの `__init__` とクラス体しか見ないので基底の `__init__`・`super().__init__()`・基底のクラス体既定値のフィールドが無く、`__init__` で None にして別メソッド（`connect()` / `start()` / lifespan）で束縛する遅延初期化の受け手型も無い。
- **コードの場所**: authgap/analyze.py:316-378 _self_fields, authgap/analyze.py:345-360 クラス体の走査, authgap/val/engine.py:1338-1399 _find_init / _class_body_defaults
- **重大度の根拠**: 代表は R4-r2-5: 探索役・設計・一般性の 3 意見とも medium（メソッド形・閉包形のユニットで、フィールドを木の中の基底クラスで束縛する書き方に限る）。R4-r4-4 は 3 意見とも low（4 文字 + '_' の接頭辞での名前の衝突か遅延束縛に依存するまれな形。件数は見積もっていない）。R4-r2-6 は medium / low / medium で、設計の観点は「記録済みの設計の帰結」として low・反証（旧文言が理由ではない）。3 件とも D1+D2 に効くもので、旧文言「D3 / D4 だけなら low」による格下げは無い。件数: R4-r2-5 は未測定（較正対 14 木 + prev5 4 木では試作前後の差 0、つまりこの 18 木には形が無い）。R4-r2-6 は探索役の構文上の見積もり `self.<conn|client|...> = None` 858 箇所 / 34 木（vendored を含む・未検証）。
- **直し方（一般に正しいか: 条件つきである）**: 【直すもの: R4-r2-5 + R4-r4-4。どちらも `_self_fields`（analyze.py:316-378）を構築の規則にそろえることで直る】
(1) クラス体: 第 1 ループ（analyze.py:350-352 の `if not name.startswith("self.")` → `name[len("self."):]`）を削除する（クラス体では `self.*` は束縛されないので、このループが出すのは捏造名と '' だけ。条件を反転しても実質は削除と同じ）。そのうえで基底（3 段まで、import 表で厳密に引く）を先に、自クラスを後に入れて上書きする。
 守り A（U24 で確認した反例）: 現行の `engine._class_body_defaults` をそのまま呼んではいけない。これはクラスごとに新しい `Env()` で右辺を評価して env に書き戻さないので、`head = "DELETE FROM items"; sql = head` の `sql` が opaque(unresolved) になる。現行の `_self_fields` の第 2 ループでは Chain.purge が `contradiction:D1 db_modify`（正しい）だが、置き換えると `contradiction_unknown:D1:db_sql_unreadable` に落ちる（同じクラスをモジュール水準で構築した purge_module は現行で既にそうなっている。木は scratchpad/triage/U24/chain）。避け方: クラスごとに、そのクラスのモジュール scope と「そのクラス体の中だけで積み上がる env」で評価する（今の `_exec_body` の使い方を基底ごとに繰り返す）。基底のクラス体の名前を派生のクラス体の env に持ち込まない（Python でも NameError）。`_class_body_defaults` 側を直す場合は `_construct_in_tree` の結果も opaque→resolved の向きに変わるので、別に敵対的レビューを通す。クラス体の評価中は `on_call = None`（import 時の構築の効果行をツールに付けない。レビュー b4）。
(2) `__init__`: `engine._find_init(cd)`（自クラス → 基底 3 段）で見つけ、`__init__` を定義するモジュールの scope（`index.function_scope(index.resolve_module_path(init.module), init.node)`）で仮引数を形式値 Atom(formal) に種付けして `_exec_body` する。
 守り B（一般性の検証役）: `_class_stack` に積むのは `(init.classname, init.module)`＝`__init__` を定義するクラスで、ユニットのクラスではない。派生クラスを積むと、継承した `__init__` の `super()` が同じクラスを指す（所見の fix_sketch「(classname, module) を積む」は曖昧）。深さは 1 から始め、`super()` 連鎖は MAX_DEPTH 4 の中で 2〜3 段を使う。
 守り C（設計の検証役）: D35 (b) と同じく、`__init__` が深さ / 再帰の打ち切りで走らなかったときは既定値の確度に理由を合流する（黙って resolved のままにしない）。
(3) 残る近似（現行と同じ。限界として書く）: 引数を要する基底 `__init__` は形式値のまま型が付かない / `_find_init` の BFS は C3 MRO の近似（菱形では一致を確認）/ `_super_callees` は多重継承で定義クラスの基底を見る / `a, b = ...` のクラス属性は拾わない。
(4) 反例テスト（実装より先に）: 再現の Inherited / ViaSuper / ClassBodyChild / register.purge_closure が DB 矛（Direct / purge_module_instance と同じ）、init_mro（菱形 C(A, B) で B.__init__ の None → 行なし、ChildNeedsArg 行なし、super() を呼ばない Overrider 行なし）、init_chain（3 段 super() 連鎖は矛、上書きは無し）、init_pkg（相対 import の基底）、R4-r4-4 の Store（DELETE 矛）/ Store2 / Store.show（'/tmp/other'）/ Plain / Override / Chain（不変）/ Annot（SELECT 内 → DELETE 矛）/ Late（捏造 SELECT の内 → opaque の不）、U24 の chain（Chain.purge は矛のまま）。試作 proto5（一般性の検証役）で B3a 8/8・B3b 15/15・tests 通過・較正対 14 木 + prev5 4 木の差分 0。opaque → resolved の向きを含むので CLAUDE.md の敵対的レビュー、`diff_effects.py`・`compare_scans.py` を通す。
【直さないもの: R4-r2-6（遅延初期化）】
 素朴な直し方（クラスの全メソッドの `self.<f> = ...` を形式値で評価し opaque を合流して join、`_self_fields` と `_construct_in_tree` の両方）は退行を作る（試作 proto6, lazy_regress）: `__init__` で `self.root = Path("/data")`、別メソッドで `self.root = Path(r)` のとき `_shape_join` が異なる Path を潰して opaque が MODEL slot に合流し、現行で正しい `contradiction:D2 fs_writeout_model_path` が `contradiction_unknown:..._opaque` に落ちる。`self.prefix + arg` → os.system の `spawn_model` も `spawn_model_opaque` に落ち、CmdConst は argv0 の定数 'ls' を失う。避ける条件（試作 AG_LAZY_NONE_ONLY=1 で退行なし）: 適用先を未知インスタンスの種 `_self_fields` だけにし `_construct_in_tree` には当てない / `__init__`・クラス体の値が None リテラルか未定義のフィールドに限る / 再帰の切断と `on_call = None`。ただしこれは spec §2.6 の経路ベースの heap を「解析していないメソッドが走ったかもしれない」へ広げる設計の拡張で、仮定した状態から resolved の矛が出る（受け手の確度が `_resolution_of` にも `_choice` にも入らない）。所見が根拠にした `_module_value` の先例は逆（関数内の再束縛は右辺を評価せず確度を落とすだけ。lazy_global で確認）。入れるなら学生が規則を決め、反例テスト → 実装 → 敵対的レビューの順。規則 4 だけを満たす最小の改善は判定を変えない列（`db_unresolved` を全 proxy kind に広げる `receiver_unresolved`）だが、これも authgap/ を変える。
- **記録済みの限界・決定との重なり**: R4-r2-5 / R4-r4-4: 記録済みの限界・設計の決定との重なりは無い（review_plan §5・D19 の K1〜K7・O1〜O41 のどれにも無い）。むしろ逆の記録がある: D17 改訂 2 / 3（decisions.md:1700）は「基底の `__init__` の `self.conn` 経由の効果が消えた」を false-clean として直しており、D35 は `super().__init__()` を `_descend_env` で解決した。`_class_body_defaults` の docstring は「`analyze._self_fields` の (1) と同じ規則」と書くのに実装が食い違っている（取りこぼし）。D35 の限界 3「継承メソッドは分割降下の対象外」は 2 型受け手の分割の話で別。D35 (b) / spec AUTHGAP_BRIEF_v3.md:1198 は「クラス体の既定値を入れ `__init__` で上書き」で、R4-r4-4 の期待を支持する。R4-r2-6: 設計の観点で反証済み。spec §2.6（AUTHGAP_BRIEF_v3.md:514-515）の経路ベースの heap、Def 4 の下向きの降下、D35 (a)(c)・O17 (c) の「経路上で束縛する形だけ追う」、D51（decisions.md:2760-2766、`self._conn = None` しか見ないことを記録し一般の変更として先送り）の帰結。AUTHGAP_BRIEF_v3.md:1118 により解決できない `.execute()` は `db_unresolved` として記録し危険効果に数えないので、DB では規則 4 を満たしている（NET / pipe には site 水準の痕跡が無く、ユニットの `opaque_reasons=[unresolved]` だけ）。O42 の候補。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも D1+D2 に効く所見で、旧文言「D3 / D4 だけなら low」は理由に使われていない。R4-r2-6 の設計の観点の low は「記録済みの設計の帰結」という理由で、旧文言によるものではない。
- **推奨の理由**: R4-r2-5（medium、3 観点とも生存、Python のクラスの意味から正解が決まり、解析器が構築の形で既に使っている規則にそろえるだけ）と R4-r4-4（low だが写し間違いで、直し方は同じ関数の第 1 ループの削除。R4-r2-5 の直しに含まれ、解決率を下げる向き）は、語彙の追加なしの一般に正しい直し方がある（守り A〜C つき）ので直す。どちらも D61 の基準（v3 と無関係に正解が決まる・どの木にも現れうる）を満たす。R4-r2-6 は設計の観点が記録済みの設計（spec §2.6 の経路ベースの heap、brief:1118 の db_unresolved）の帰結と判定し、一般性の観点も素朴な直しは正しい矛を不に落とすと示した。避ける形は heap モデルの拡張で学生の設計判断が要るので、限界として記録する（O42 候補）。authgap/analyze.py を変えるので凍結の指紋が変わり、再凍結と preregistration への逸脱の記録が要る。
- **所見**:
  - R4-r2-5: 代表（medium × 3）。`_self_fields` が自クラスの `__init__` とクラス体しか見ず、基底の `__init__`・`super().__init__()`・基底のクラス属性のフィールドが消える（誤 clear）。一般に正しい直し方あり（試作 proto5、較正対 18 木の差 0）。守り A〜C つきで直す。（メソッド形ツール / 閉包の注釈つき引数の `self` の種を作る `_self_fields` が自クラスの `__init__` とクラス体しか見ず、基底の `__init__`・`super().__init__()`・基底のクラス）
  - R4-r4-4: 同じ関数の別の表れ（low × 3）。クラス体の走査の条件が逆で捏造フィールド（base_sql → sql、data_path → path、''）が本物より先に入る。誤 clear / 誤警報の両方と、遅延束縛の隠蔽を作る。第 1 ループの削除で直り、R4-r2-5 の直しに含まれる。直す。（`_self_fields` (1) のクラス体の走査が条件を逆に書いていて（`if not name.startswith("self.")` の後で `name[len("self."):]`）、クラス体の名前 N と `self` か）
  - R4-r2-6: 設計の観点で反証済み（spec §2.6 の経路ベースの heap と brief:1118 の db_unresolved による記録済みの扱い）。一般性の観点でも、素朴な直しは lazy_regress で正しい矛を不に落とす。None 限定版は heap モデルの拡張で学生の設計判断が要る。限界として記録する（O42 候補）。（`__init__` で `self.conn = None` とし別のメソッド（`connect()` / `start()` / lifespan）で束縛する遅延初期化では、`_self_fields` / `_construct_in）

### U28 pipe 形の EXEC 判定（argv0 の字面とクラス名の部分一致に頼る）（段階 C・重大度 中・推奨 一部直す）

子プロセスを起動して標準入力にデータを流し込む書き方（Popen(..., stdin=PIPE) の後で communicate(input=...) や stdin.write(...) を呼ぶ）について、解析器は「起動したのが Python などのインタプリタなら、流し込んだものはコードとして実行される（EXEC）」と判定します。インタプリタかどうかは、起動するプログラム名の文字列と、受け手のクラス名だけで決めています。その結果、次の 3 つの書き方で判定を誤ります。(1) 起動するプログラムを sys.executable（今動いている Python 自身のパス）で指定すると、解析器はその値を知らないのでインタプリタと見なさず、「ファイル書き込みかもしれない」という参考の行に落とします。D2（destructiveHint）では「矛盾」が「不明」に変わり、矛盾を見逃します。(2) Windows のパス C:\Python311\python.exe は「\」で区切られていてファイル名を取り出せず、同じように見逃します。(3) 逆に、名前に Popen を含むだけの自作クラス（PopenRecorder など）を本物の子プロセスと取り違え、readOnly のツールで誤った矛盾（誤警報）を出します。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: pipe 形（Popen + stdin への書き込み）の効果を EXEC にするかを、argv0 の定数文字列の字面と受け手のクラス名の部分文字列で決める: `is_interpreter` は basename を `/` でしか切らない（Windows の `C:\\Python311\\python.exe` が外れる）、`sys.executable` は値エンジンで定数を持たない（Unknown/opaque）ので interpreter に当たらず、受け手判定 `"Popen" in c` は `PopenRecorder` のような木内クラスにも当たる。外れると EXEC が FS_WRITE の情報行になり（D2 矛 → 不）、当たり過ぎると readOnly の D1 矛になる。
- **コードの場所**: authgap/catalog/sinks.py:623-635 is_interpreter, authgap/effects.py:787-831 _pipe / 受け手判定, authgap/val/engine.py:509-553 _ev_Attribute（sys.executable）, authgap/catalog/transfers.py:175-192 Popen の型
- **重大度の根拠**: 単位の代表は R4-r2-8。探索役・設計の観点・一般性の観点の 3 意見がそろって medium。D2 の pipe 行で矛 → 不になり（D1 は矛のままで、理由が exec から fs_write に変わるだけ）、shell 文字列の形では D1 / D2 とも不 → 矛の誤り（一般性の検証役が見つけた）。影響の見積もりは探索役の構文上の数え上げだけ: v2 で `sys.executable … stdin=PIPE` が 13 箇所 / 7 木、`Popen([sys.executable` が 45 箇所 / 14 木（上限。判定が実際に変わる件数は未測定）。shell 文字列連結の形は未集計。R4-r3-5 と R4-r3-6 は 3 意見とも low で、コーパスでは該当する書き方がテストにしか無い（R4-r3-5 は Windows パスのリテラル 5 行。R4-r3-6 はテストの Fake / Recording 系と本物の派生 WindowsPatchedPopen だけ）。3 件とも D1+D2 に効くので、旧文言「D3 / D4 だけなら low」は関係せず、それで下げた重大度は無い。
- **直し方（一般に正しいか: 条件つきである）**: 【R4-r3-5 Windows の区切り。大きさ S】sinks.py `is_interpreter` で、ファイル名を `argv0.replace("\\", "/").rsplit("/", 1)[-1]` で取り出す。`.exe` を落とす処理は害が無く、`bash.exe` / `node.exe` には要る（`python.exe` は今でも前方一致で当たる）。守ること: カタログの語（INTERPRETER_ARGV0）に `cmd` / `powershell` / `pwsh` を足さない（sink 語彙は月 3 に凍結）。検証役が直し方をシミュレートした結果: `C:\Program Files\Git\bin\git.exe` と POSIX の `./tools\\formatter` は FS_WRITE のまま、`/` 区切りと POSIX の対照は EXEC のまま、run_code_win だけが EXEC（contradiction:D2 exec）に変わった。今正しい結果が壊れる反例は見つからなかった。`is_interpreter` を呼ぶのは effects.py:828 の 1 か所だけ。
【R4-r3-6 クラス名の部分一致。大きさ M】所見が挙げた素朴な直し方（正確な型名の集合 `subprocess.Popen` / `subprocess.Popen.stdin` / `asyncio.subprocess.Process` / `….stdin` との一致だけにする）は壊れる。反例: 木内の本物の派生 `class ManagedPopen(subprocess.Popen)` の `p.communicate(input=code)`。今は部分一致で FS_WRITE 行が出て D1 矛になり、これは正しい。SPAWN 行は出ないので、この pipe 行が唯一の跡になる。素朴版ではこの行が効果ゼロになり、黙って誤 clear になる。避ける条件: 正確な型名の一致に加えて継承を見る。木内クラスは `_class_family` と import 表で基底を厳密にたどり、基底に `subprocess.Popen` か `asyncio.subprocess.Process` があればハンドルとして扱う（isinstance の意味。名前に Popen を含まない派生も新しく拾える）。基底が解決できないときは今の保守的な行を残す（D61 G1 の教訓）。D61 G4 の条件（外部の dotted 型を木内の同名クラスに結ばない）も守る。検証役の確認では、中で `self._p.communicate` に委ねる木内ラッパ `PopenWrapper` の本体の EXEC 行は残った。
【R4-r2-8 sys.executable。入れるなら逸脱として】所見の直し方（`_ev_Attribute` で `sys.executable` に `Atom(const="python")` を resolved で与える）には副作用がある。SPAWN 行の sub_kind が SPAWN_MODEL_ARGV → SPAWN_CONST_ARGV に変わり、argv0 が opaque から resolved になって、opaque 率・解決率の指標も動く。設計の検証役は、値に「インタプリタである」印を付けて `_pipe` だけがそれを読む形を勧めている。守ること:
(1) 木のどこかで `sys.executable = …` や `setattr(sys, "executable", …)` と書き換えていれば、今までどおり opaque にする（反例の木 r8_rebound: `sys.executable = "/usr/bin/node"`）。`_tree_attr_writes` は外部モジュールを集めないので、`_writes_environ` と同じような走査を別に足す。別名 import は `resolve_call_name` で解く。局所変数の `sys` は local_bindings で除く。
(2) 合成した定数を使う場合は、代役の文字列であることをコメントに書く。`os.path.dirname(sys.executable)` のような連結から偽の定数パスが resolved になり、それが付録のゲート等級（strong-path など）に使われないかを確かめる。
(3) frozen アプリ（PyInstaller）や埋め込みインタプリタでは、sys.executable が別の実行ファイルや空になる。警報の向きの誤りなので、限界として記録する。
(4) `[sys.executable, "-m", "pip", "install", pkg]` に標準入力で `"y\n"` を流す形は EXEC 矛になり、誤警報が増える。定数 `python3` でも今すでにそうなっていて、Def 3(c) / O35 の粗さによるものなので直しの責任ではない。ただし件数が増えるので、compare_scans で増えた矛を 1 件ずつ見る。
範囲: `subprocess.run(sys.executable + " " + script, shell=True)`（D1 は spawn_model_opaque の不 → 矛）と `asyncio.create_subprocess_exec(sys.executable, "-", stdin=PIPE)` も同じ原因。`subprocess.run([...], input=code)` で EXEC 行が出ないのは別件なので、この単位には含めない。月 3 に凍結した INTERPRETER_ARGV0 には触らない。
【共通】authgap/ を変えるので、指紋が変わり再凍結が要る（D62 の docstring 修正と同じ再凍結にまとめる）。直す前後で `scripts/diff_effects.py` を較正対に、`scripts/compare_scans.py` を v2 の run に対して走らせる。不 → 矛の向きの変更と行が増える変更（R4-r3-6 の継承、R4-r2-8）があるので、CLAUDE.md の敵対的レビューにかける。
- **記録済みの限界・決定との重なり**: R4-r2-8 は設計の観点で反証された（refuted=true、確信度 0.7）。理由: (a) argv0 が定数に読めないとき `_pipe` が FS_WRITE 側だけを出す機構は、D19 の既知の欠陥 K1（decisions.md:1533。tests/test_f0a_defects.py:1807-1816 の xfail strict）そのもの。review_plan.md §5 は K1〜K6 を「再発見しても所見にしない」と定めている。(b) D61 G1 の取り消し（decisions.md:3463-3467）と O41（open_questions.md:1064）は、argv0 が決まらないときの FS_WRITE 情報行を「子プロセスがデータで何をしうるかの保守的な上界」として残すと決めた。(c) f0a_checks.md:517 で以前の点検者が、`sys.executable` の opaque(unresolved) を「木外で、config atom の 4 源にも TRANSFER にも無いので Def 4 の字義どおり妥当」と判定し、D17 でも直す対象に入れなかった。設計の観点の結論: 現行の規則のもとで実装は規則どおりで、直しは Def 4 の解決源を増やす新しい規則なので、凍結後の逸脱として学生が判断する。一般性の観点は反証せず、「決まらないものではなく、Python の仕様で決められるものを決める話で、os.environ の config atom や D35(e) / D43 / D50 と同種のライブラリ知識の追加」と読んだ。3 観点の突き合わせでは expected_ok=false（設計の観点だけが ✗）。R4-r3-5 と R4-r3-6 には意図した決定の記録が無い（設計の観点も反証せず）。関連する記録済みの限界: O35（argv0 だけで EXEC を決める粗さ。pip に `-m` と標準入力を渡す形が EXEC 矛になる）、decisions.md:314-316（Obj.classes が木内クラスを末尾名で持つ限界。R4-r3-6 とは別件）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも D1+D2 に効き、どの検証役も D3 / D4 を理由に重大度を下げていない。R4-r3-5 / R4-r3-6 が low なのは、書き方がまれ（コーパスではテストにしか無い）という理由による。
- **推奨の理由**: 単位の中で扱いが分かれる。R4-r3-5 は直すことを勧める。仕様のカタログの語が当たるはずの形を、区切り文字の処理の不備で外しているだけで、1 関数の 1 行で直り、検証役のシミュレーションで壊れる反例が無く、語彙も増えない。low だが、学生の最終評価は新しいデータで行うので、Windows 向けのサーバが入れば起きる。D62 で再凍結はどのみち必要になるので、追加の手間はほとんど無い。
R4-r2-8 は代表で medium だが、設計の観点が「K1 / D61 G1 取り消し / f0a_checks:517 で記録済みで、現行の Def 4 のもとでは仕様どおり」と反証した。推奨の基準に従い、限界として記録することを勧める。学生が「Python の仕様で正解が決まる」（D61 の基準 1）として入れる場合は、preregistration に逸脱として書き、fix_outline の条件 (1)〜(4) と「印の形」を守って敵対的レビューにかける。
R4-r3-6 は low でまれで、向きは誤警報。素朴な直し方は本物の派生の唯一の跡を消して誤 clear を作る。正しい直し方（継承を見る）は M の規模で、行を増やす変更なので敵対的レビューも要る。凍結直前に入れる利点は小さいので、限界として記録することを勧める。
- **所見**:
  - R4-r2-8: 代表（medium、3 意見とも medium、false_clean）。sys.executable が値エンジンで opaque になり、インタプリタとして扱われない。設計の観点で反証済み（K1 / D61 G1 取り消し / f0a_checks:517 で記録済み、Def 4 どおり）、一般性の観点は条件つきで一般に正しいとした。推奨は限界として記録。入れるなら逸脱として条件 (1)〜(4) を守る。（`Popen([sys.executable, ...], stdin=PIPE)` + `communicate(input=code)` / `stdin.write` で、`sys.executable` が interpreter ）
  - R4-r3-5: 同じ原因（argv0 の字面での照合）の別の表れ（low、false_clean）。Windows の `\` 区切りで basename が取れない。3 観点とも反証なし。区切りの正規化だけで反例が無いので、直すことを勧める（S）。（`is_interpreter` が `/` でしか basename を切らないので、Windows のパス（`C:\\Python311\\python.exe`）を argv0 にした Popen + stdin パイプが EXEC ）
  - R4-r3-6: 同じ判定の、逆向きの表れ（low、false_alarm）。受け手のクラス名の部分一致 `"Popen" in c` で自作クラスを子プロセスと取り違える。3 観点とも反証なし。素朴な直し方（正確な型名だけ）は本物の派生を黙って消す反例がある。推奨は限界として記録。直すなら継承を見て、基底が解決できないときは今の行を残す。（`_pipe` の受け手判定 `"Popen" in c` が部分文字列一致なので、名前に Popen を含む木内クラス（`PopenRecorder` など）の `communicate(input=…)` / `stdin.write`）

### U30 sink に届く名前・構築子の表の穴（受け手型を作る表と再公開別名の表が欠ける）（段階 C・重大度 中・推奨 一部直す）

sink（危険な操作）の表には、pandas の df.query、jinja2 の env.from_string、neo4j の非同期ドライバ、arango の AQL、asyncio.subprocess の子プロセス起動、sympy.parse_expr が載っています。ところが実際のコードの書き方からは一度も当たりません。原因は 2 つです。(1) df = pd.DataFrame(...)、env = jinja2.Environment()、driver = AsyncGraphDatabase.driver(...)、s = requests.session() のように「この変数は何の型か」を決める表（構築子の表、型遷移の表）に、これらの行がありません。(2) from asyncio.subprocess import create_subprocess_exec や from sympy import parse_expr のように公式の別の import 経路を使うと、名前の照合（完全一致か末尾 2 要素の一致）で表の正式名に当たりません。どちらの場合も効果の行がゼロになり、readOnlyHint: true なのにコードを実行する・DB に書くツールが「矛盾なし」と出ます。誤りは見逃し（誤 clear）の向きです。

- **宣言**: D1 / D2 / D3 / D4　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 要　**scripts/ だけで直る**: いいえ
- **根本原因**: 語彙にある sink に実コードの API の書き方から届くための表が欠ける: 受け手型の要る直接 sink（`pandas.DataFrame.query` / `jinja2.Environment.from_string`）と proxy 受け手型（neo4j の AsyncDriver / AsyncSession、arango、`requests.session()`）を作る CtorRow / 型遷移が無く、再公開された別名（`asyncio.subprocess.create_subprocess_exec` / `from asyncio.subprocess import …`、`sympy.parse_expr`）を正規名に写す表も無いので `_suffix_match` の完全一致・末尾 2 要素一致に当たらず、語彙の sink が一度も当たらない。
- **コードの場所**: authgap/catalog/transfers.py:165-203 CtorRow / CALL_TYPE_TRANSITIONS, authgap/catalog/sinks.py:150, 199, 227, 294, 571-586 対象の sink / proxy 行, authgap/effects.py:161 _suffix_match, authgap/effects.py:423 受け手型の照合
- **重大度の根拠**: 代表の R4-r1-4 は 3 意見（探索役・設計・一般性）がそろって medium です。当たるはずの EXEC / DB / SPAWN / NET の sink が丸ごと消える誤 clear で、run20 の contradictions.json では site に neo4j / pandas / jinja2 / arango が 0 件でした（一般性の検証役が確認）。v2 の実例は、一般性の検証役が per-tree JSON で該当効果 0 を確認した deploylabs429（AsyncGraphDatabase.driver）と synalinks（env.from_string）です。探索役と設計の検証役が挙げた hughmkiii は、一般性の検証役によると corpus の木に該当の出現がありません（rg で 0 件）。R4-r1-11 は low / medium / low で中央値は low です。設計の検証役は v2 の実例（cnseniorious000 の ipython-mcp.py:99 `from asyncio.subprocess import PIPE, create_subprocess_shell`）を理由に medium としました。一般性の検証役は頻度が低いことを理由に low としました。旧文言「D3 / D4 だけなら low」を理由に下げた形跡はありません。どちらの所見も D1+D2 に効くと申告されており、D3 / D4 の話を根拠にした下げは見当たりません。なお §7.3 / §7.4 の表から導くと、消えた EXEC / SPAWN / NET / DB の効果は D3（EXEC・SPAWN の MODEL 由来は矛、NET は宛先しだい）と D4（EXEC / SPAWN は不、DB の書き込みは不）の判定にも効きます。この効きは表からの導出で、件数は未測定です。
- **直し方（一般に正しいか: 条件つきである）**: 【A. 受け手型を作る表（R4-r1-4）】authgap/catalog/transfers.py の CTORS / CALL_TYPE_TRANSITIONS に、ライブラリの API の型で決まる行を足します。
- CtorRow("jinja2.Environment" → cls "jinja2.Environment")
- CtorRow("neo4j.AsyncGraphDatabase.driver" → "neo4j.AsyncDriver", {uri: arg0}) と CALL_TYPE_TRANSITIONS[("neo4j.AsyncDriver","session")] → ("neo4j.AsyncSession", {uri: uri})。同期版の行（transfers.py:203 / CALL 表）の鏡です。
- CtorRow("requests.session" → "requests.Session")
- pandas.DataFrame / pandas.read_csv・read_json・read_parquet・read_sql・read_excel → cls "pandas.DataFrame"

【守り 1: pandas で MODEL が OP に洗われる（一般性の検証役の反例 t4_launder）】_build_obj（val/engine.py:2620-2641）は常に Prin.OP を返し、roots も fields からしか取りません。そのため、データを運ぶ構築子（pd.DataFrame(rows)、read_csv）にフィールド無しの行を足すと、次の形で MODEL の主体と根が消えます。
- `df = pd.DataFrame(rows); open(df.iloc[0]["path"], "w")` は .path MODEL/opaque から OP へ。
- `subprocess.run(df["cmd"][0], shell=True)` は MODEL/opaque から OP/resolved へ。
D1 / D2 の verdict は不のまま変わりませんが、*_opaque の注記（D56 の感度分析の帯）と INJECT の座標が失われます。避け方は次のどちらかです。
- (i) _build_obj で主体を下げない。CALL 遷移が engine.py:787 ですでにしている「持ち上げはしても下げない」を構築子にも当て、args / kwargs の主体と根を join する。
- (ii) pandas の行に data: arg0 のフィールドを持たせる。
jinja2.Environment / neo4j async / requests.session / arango は設定の引数しか取らず、既存の同期版の行の鏡なので、この洗いは起きません。

【守り 2: 注釈経路は直らない】`def f(df: pd.DataFrame, expr)` の df.query は、この直し方では当たりません。_ANNOTATION_TYPES（engine.py:1865）が ANNOTATION_TYPED_RECEIVERS ∪ PROXY_SINKS の受け手型だけから作られ、DIRECT_SINKS のクラス修飾キーを含まないためです。含めるかは G4 と同じ理由づけの拡張で、別の判断になります。

【守り 3】df.head() など DataFrame を返すメソッドは追えないので、直しても部分的です。誤 clear が残るだけで、新しい誤警報は出ません。D61 改訂の「外部の型は木の中のクラスの絞り込みに使わない」がすでにあるので、新しい誤った降下も作りません。

【B. arango（R4-r1-4 の一部。語彙の行の書き換え）】sinks.py:585-590 の method="aql" は python-arango の実 API と食い違います。実 API では db.aql が属性で、実行は db.aql.execute(q) です。直すには次の 3 つが要り、凍結した sink 行の文言を動かします。
- CtorRow("arango.ArangoClient") と CALL 遷移 (ArangoClient, "db") → arango.database.StandardDatabase
- ATTR 遷移 (StandardDatabase, "aql") → arango.aql.AQL
- proxy 行の受け手を arango.aql.AQL、method を execute に付け替え
【守り 4】受け手を付け替えると、DB_RECEIVER_TYPES と _ANNOTATION_TYPES（どちらも PROXY_SINKS から導出）から StandardDatabase が消え、`db: StandardDatabase` の注釈経路が死にます。StandardDatabase を注釈型として残す必要があります（検証役の実験では旧行を残したので aql_annot が当たった）。

【C. 再公開された別名の表（R4-r1-11）】_suffix_match（effects.py:161）の前に「完全一致の dotted → 表の正式名」の別名表を引きます。PIPE_HANDLE_SOURCES（sinks.py:657）と CTOR_BY_NAME も同じ正式名で引きます。
【守り 5】手で選んだ 3 件（asyncio.subprocess.create_subprocess_exec / _shell、sympy.parse_expr）にしません。DIRECT_SINKS / PIPE_HANDLE_SOURCES / CTOR_BY_NAME の各項目について、ライブラリの公開モジュールが同じオブジェクト（`is` で同一）として再公開している dotted 名を機械的に列挙して作ります（G4 の「一覧は表から機械的に作る」と同じ方針）。これで requests.api.get、sympy.core.sympify.sympify、sqlalchemy.sql.text、jinja2.environment.Template も同じ理屈で拾えます。照合は完全一致に限り、ルートと末尾だけの一般化（xml.*.parse など）はしません。
【守り 6: 反例 ce1】木の中に sympy.py / asyncio.py があって import を影で覆うと、今でも sympy.sympify が EXEC の矛として誤警報になります。別名表を足すと、この既存の誤警報が parse_expr にも広がります。避け方は、ルートのモジュールが木の中にあるときは sink 表を引かない条件を、既存の表と別名表の両方に付けることです（ce1 の既存の誤警報も直ります）。正式名・`as` 別名・sympy.sympify の正しい矛（ce2）は壊れません。

【手順】行が増える変更です（A は opaque → resolved を含む）。CLAUDE.md の敵対的レビューと、diff_effects / compare_scans での消えた行の確認を通します。ctor カタログは月 3 凍結ですが、D50（psycopg、逸脱 #15）に同じ理由で拡張した前例があります。preregistration の逸脱（#24）に記録します。一般性の検証役が scratchpad の複製に A と B を当てたところ、所見の全形が規則どおりの矛になり、凍結テストは 830 passed / 0 failed でした。
- **記録済みの限界・決定との重なり**: 設計の観点ではどちらの所見も反証されていません。記録済みの近い項目と、この単位との違いは次のとおりです。
- O41「語彙に無いライブラリ（zvec / arcpy）」: 語彙に無いライブラリの話。この単位は語彙に「ある」sink です。
- O39: HTTP メソッドが語彙に無い話で、別物です。
- D35 限界 4（remote カタログ）と D35 の値の別名（b = a）: 別物です。
- D17 の opaque(unresolved) への合流: この単位はその言い直しではありません。
- D61 G3: 木の中の __init__ の再公開を追う決定で、外部ライブラリの再公開を除外した決定ではありません。むしろ G3 と同じ考え方を sink 側でしていない食い違いです。
- 同じ根本原因の前例: O29 → D50 / D51（DB の受け手型を作る規則が無かった。preregistration 逸脱 #15 として ctor を拡張）。D61 G4 も、受け手型が sink に届くべきという意図を示します。
- review_plan §2: 「語彙にある sink が当たらない」を明示的に対象にしています。
凍結との関係は次の 2 点です。
- ctor カタログは月 3 凍結（transfers.py:145、BRIEF 514 / 841 行）ですが、D50 の拡張の前例があります。
- arango の proxy 行の書き換えは、凍結した sink 行の文言の変更に当たります。設計の検証役は「§2 の語彙変更に当たるので学生の逸脱判断。直さないなら O 番号で記録」としています。
付け加えると、A14（arango）と S2（neo4j）は cve_triage.csv で UNSCORED / unchecked で、corpus_spec の 14 targets にもありません。これらの行を動かす較正対は一度も走っていません。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R4-r1-4 は 3 意見とも medium です。R4-r1-11 は low / medium / low で、low とした理由（探索役の自己申告と一般性の検証役）は「v2 に 1 件しか無い、頻度が低い」で、D3 / D4 に言及していません。両所見とも D1+D2 に効くと申告されているので、旧文言が適用される余地もありませんでした。
- **推奨の理由**: 代表は medium です。構築子と型遷移の行（jinja2.Environment、neo4j async、requests.session、条件つきの pandas）と別名表（R4-r1-11）は、ライブラリの API と import の意味から正解が決まります。v2 / v3 に合わせた直し方ではなく（D61）、凍結した sink の語彙も増やしません。D50 の前例にならって直す基準を満たします。ただし pandas は、主体を下げない条件（守り 1）が無いと MODEL が OP に洗われます。別名表は、木の中のモジュールが影で覆うときの条件（守り 6）と、機械的に列挙すること（守り 5）が要ります。

一方、arango の部分は凍結した sink 行の文言（受け手型 / メソッド）を書き換えるので、基準の「語彙の追加・変更が要らない」を満たしません。注釈だけの `df: pd.DataFrame` の経路（守り 2）も、G4 の拡張という別の設計判断になります。この 2 つは、学生が逸脱として直すと決めない限り限界として記録する（O42 以降）のが基準どおりです。R4-r1-11 は単独では low ですが、同じ「表から sink に届かない」原因で、守りつきの一般的な直し方があり、壊れる正しいケースも作れなかったので、A と一緒に直すことを推奨します。
- **所見**:
  - R4-r1-4: 代表（medium、3 観点とも生存、fix_is_general=true）。ここを分けて扱う。(1) jinja2.Environment / neo4j.AsyncGraphDatabase.driver + AsyncDriver.session / requests.session の構築子・型遷移の行 → 直す。(2) pandas の構築子 → 守り 1（_build_obj で主体を下げない、または data: arg0 のフィールド）をつけて直す。(3) arango の proxy 行の付け替え → 凍結した sink 行の文言を変えるので学生の逸脱判断。直さないなら限界として記録。(4) 注釈だけの `df: pd.DataFrame` の経路 → G4 の拡張という別判断。記録に回す。（受け手型が要る直接 sink（pandas.DataFrame.query / jinja2.Environment.from_string）と proxy 受け手型（neo4j.AsyncDriver/AsyncSession、arang）
  - R4-r1-11: 同じ原因の別の表れ（表の正式名に届かない、ここでは import の別名で）。重大度 low（中央値。設計の検証役は medium）、3 観点とも生存、fix_is_general=true。完全一致の別名表を機械的に列挙し、木の中のモジュールで影になるときの条件をつけて直すことを推奨。v2 の実例は ipython-mcp.py:99 の 1 木。（語彙にある sink の再公開別名（asyncio.subprocess.create_subprocess_exec / from asyncio.subprocess import …、sympy.parse_expr）が _suffi）

### U33 SQL の先頭語の読み方（段階 A・重大度 中・推奨 一部直す）

解析器は SQL 文字列の種類（読み取り / 変更 / 設定など）を、文字列の最初の単語だけで決めています。そのため 4 つの書き方で読み違えます。1 つ目は先頭に説明のコメント（`-- …` や `/* … */`）がある場合で、コメント記号を単語として読んでしまいます。2 つ目は `CREATE …; DELETE …` のように 1 つの文字列に文を 2 つ以上並べた場合で、2 文目以降の DELETE / DROP を見ません。3 つ目は `"%s FROM t" % ("DELETE", x)` のように書式の穴を先頭に置いた場合で、`%s` を単語として読みます。4 つ目は SQLite の `PRAGMA journal_mode(WAL)` のように括弧で値を渡す設定で、読み取りと見なします。誤りはどれも「矛盾あり」を取りこぼす向きです。D1 / D2 では「矛（矛盾）」が「不（不明）」か「内（矛盾なし）」に落ちます。D4（idempotentHint）では、コメント付き・複文・書式の穴の形の INSERT が何の注記も無く「内」になることを、この単位の作業で確かめました。

- **宣言**: D1 / D2 / D4　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: SQL を分類する `sql_head_of_text` / `sql_class` / `_sub_kind` が文字列の先頭の空白区切りの語だけを読む: 先頭のコメント（`--` / `/* */`）を剥がさず先頭語が `--` になる、定数の複文（executescript / psycopg execute / exec_driver_sql）を引用符の外の `;` で分けず 2 文目以降の DELETE / DROP を見ない、書式テンプレートの先頭のプレースホルダ（`"%s FROM t …" % ("DELETE", x)` / `"{} …".format(...)`。`_ev_BinOp` の `%` は置換でなく連結）を語として読む、PRAGMA の括弧形 `PRAGMA journal_mode(WAL)` を「= の無い PRAGMA = 読み取り」にする。
- **コードの場所**: authgap/effects.py:342-369 sql_text / sql_head_of_text, authgap/effects.py:372 _sub_kind, authgap/catalog/statements.py:53-95 sql_class / PRAGMA, authgap/val/engine.py:564-593 _ev_BinOp（%）, authgap/dparse.py:360-384 _db
- **重大度の根拠**: 代表は R3-r1-1（複文）で、3 観点すべてが medium。矛が注記なしで内に落ちる、最も見えにくい誤 clear で、`CREATE TABLE IF NOT EXISTS …; DELETE …`、`BEGIN; DELETE …; COMMIT;`、`PRAGMA foreign_keys = ON; DROP …` のような executescript の常套句に当たります。R3-r1-2（先頭コメント）は設計の観点が medium、一般性の観点が low でした。low の理由は「v2 で 0 件、しかも D1 / D2 では不として見える」ことです。ただしこれは D1 / D2 だけを見た判断です。この単位の作業で repro_scan を走らせたところ、D4 では `-- c\nINSERT …` と `executescript("SELECT 1; INSERT …")` が注記なしの内でした（対照の `INSERT …` は `contradiction_unknown:D4:db_nonidempotent_statement`）。つまり D4 では黙った誤 clear になります（_d4 も同じ sql_head_of_text を使うため）。D62 で D4 も主指標になったので、この点は medium を支えます。R3-r1-3 と R3-r4-3 は 3 観点とも low で、まれな書き方です。件数は検証役が数えたものだけを書きます。v2 run20 では、複文の定数 SQL の効果行が 24（すべて宣言なしの claude-replay call_tool）で、判定が変わる行は 0。先頭コメントは 0、括弧形の設定 PRAGMA は 0（括弧形は table_info の 12 件だけ）です。corpus 全体（vendored 含む）では、先頭語より厳しい文が後ろに隠れている定数が executescript 32 + execute 29 + exec_driver_sql 0、先頭コメント付きの定数が executescript 8 + execute 2 でした。R3-r4-3 の件数と D4 への影響の件数は未測定です。
- **直し方（一般に正しいか: 条件つきである）**: 共通: 規則 → 反例テスト → 実装の順にします。§7.5 の文言を先に直してコミットします（R3-r1-1 と R3-r1-3 は §7.5 の字面どおりに動いており、規則のほうに抜けがある）。正規化と分割は 1 つの関数にまとめ、sql_head_of_text / sql_class（`_PRAGMA` の正規表現も正規化後の文字列に当てる）/ _sql_head_of / _sub_kind / _db / _d4 のすべてで使います。

(1) 先頭コメント（R3-r1-2）: 先頭の空白・`--` 行コメント・`/* */` ブロックコメントを剥がしてから先頭語を取ります。避ける条件は次のとおりです。
(i) `/*!` で始まる MySQL の実行されるコメントは剥がさない。素朴な正規表現 `\A(?:\s+|--[^\n]*(?:\n|\Z)|/\*.*?\*/)+` だと `/*!50000 DROP TABLE t */ SELECT 1` の中身が消えて SELECT が残り、不 → 内 の誤 clear になる。一般性の検証役が作れた唯一の反例。
(ii) 剥がした後が空なら今と同じ不にする。
(iii) PostgreSQL の入れ子コメントや閉じないコメントは剥がし切れず不のまま。退行ではない。
(iv) 接頭辞（complete=False）では、剥がした後に既存の「最初の語の後に空白」の条件を当てる。
(v) どの方言の字句で読むか（MySQL の `#`、`--` の後に空白が要るか）を §7.5 に書く。

(2) 定数の複文（R3-r1-1）: complete=True の定数だけを文に分け、各文を §7.5 で分類して最も厳しい結果（矛 > 不 > 内）を採ります。D4 でも、どれかの文が NONIDEMPOTENT なら不にします。接頭辞（complete=False）は §9.4 のままです。素朴な直し方で壊れる反例は 2 段あります。
(a) 引用符を見ない `split(';')` は、`INSERT … VALUES ('a;b')` を不に落とす。
(b) 引用符とコメントを見る分割でもまだ足りない。SQLite の `CREATE TRIGGER … BEGIN UPDATE …; DELETE …; END;` は 1 文で、D2 では CREATE なので内が正しいのに、DELETE を独立した文と読んで矛にしてしまう（誤警報）。PostgreSQL の `CREATE FUNCTION … AS $$ BEGIN DELETE FROM t; END $$` も同じく矛か不になる。本体は作成時には実行されない。corpus の alembic 移行に実在する。
避ける条件は次のとおりです。
- SQLite の分割は sqlite3.complete_statement（トリガ本体を 1 文として扱う。検証役が確認済み）で行う。
- `$tag$…$tag$` のドル引用は文字列として扱う。
- 分割器が扱えない構文（BEGIN…END の複合文、閉じない引用、$ 引用の対応の不一致）に出会ったら、矛にせず不にする（規則 4）。
- sqlite3 の execute は複文を ProgrammingError で拒むが、解析器は sqlite3 の execute も psycopg.Cursor.execute の site に写すので区別できない。複文から出た矛には独自の理由（例: db_multi_statement。凍結語彙ではない）を付け、手判定で見分けられるようにする。
- 反例テストに CREATE TRIGGER / `$$` / `'a;b'` / `'-- ;'` / `'BEGIN; DELETE; COMMIT;'` を入れる。
- 矛が増える向きの変更なので、増えた矛を 1 件ずつ原典で確かめる敵対的レビューを通す。

(3) 書式の穴（R3-r4-3）は 2 段で直せます。
(a) 読む側: 接頭辞の最初の語が `%` / `{` / `}` を含むとき（URL の `_has_placeholder` と同じ判定）は先頭語を決めない。D1 / D2 は不のままで理由が db_sql_unreadable に正されるだけ。D4 では、今は `%S` が非 None なので内（誤 clear）になっているのが不に直る。安全で小さい変更。
(b) engine 側: `_ev_BinOp` の Mod と str.format で、リテラルの実引数だけを本当に置換する。一般性の検証役が挙げた条件は次のとおり。
- 右辺が構文上の ast.Tuple か単一のリテラルのときだけ置換する。Seq はリストとタプルを区別しない。`% ["DELETE", x]` は実行時に `"['DELETE', …]"` になるので置換してはならない。
- `%%`・`%(name)s`・幅や精度（`*` を含む）を正しく解析し、数の不一致・スター付き引数・dict では置換せずに降りる。
- リテラルの置換は Python 自身の `%` で行う。
- 最初の非リテラルの実引数の位置で切り、その Value を part として残す（主体と確度を保つ）。
- .format は string.Formatter().parse を使い、`{{ }}` を扱い、`{0.attr}` / `{x[0]}` では降りる。
既存規則と整合する変化として、`"%s * FROM t; %s" % ("SELECT", env)` は不 → 内 になる（同じ連結 `"SELECT * FROM t; " + env` は今も内）。(b) は R1（engine）の範囲で、% を使うすべての値（URL・パス）に効きます。設計の観点は「解決率を上げる変更」と見ています。

(4) PRAGMA の括弧形（R3-r1-3）: `op in ("=", "(")` のとき、PRAGMA_PERSISTENT_SET の名前は persistent、PRAGMA_CONNECTION の名前は connection にします。PRAGMA_PERSISTENT_ACTION は今のままです。`table_info(users)` / `index_info(i)` / 引数なしの `PRAGMA journal_mode` / `page_size` は read のまま、`wal_checkpoint(TRUNCATE)` は persistent のままで、検証役は反例を作れませんでした。§7.5 の文言を「`= …` または `(…)`」に直すのが先です（§7.1 は読み取りを「値を設定しない PRAGMA」と定義しており、§7.5 と食い違っている）。
- **記録済みの限界・決定との重なり**: 4 つとも設計の観点で反証されていません（refuted=false）。

記録と似ているが別のものは次のとおりです。
- O24 は「SQL を字句解析するのは役割を超える」「本文の語を探すと誤警報」という立場で、`WITH` を読み取りとしている。これは単一の文の後ろの句の話で、`;` で区切った別の文や先頭のコメントは扱っていない。設計の検証役は、R3-r1-1 を O24 の再発見と読む余地がある（迷い）と書いた。学生が R3-r1-1 を直さない場合は、D55 の既知の限界（`INSERT … ON CONFLICT DO UPDATE`、`WITH … INSERT`）の隣に「定数の複文（executescript / パラメータ無しの psycopg execute / exec_driver_sql）」を O42 以降として明記すべきとしています。今は内で注記も出ません。
- D41 / D42 の B1 は、改行で始まる SQL のために `split(None, 1)` を選んだ決定。コメントは検討していない。
- D17 改訂 2〜4 の `_has_placeholder` は URL の host だけの防御で、SQL の接頭辞読みには同じ防御が無い。R3-r4-3 はこれを SQL にも当てる話。
- §9.4 は「psycopg などは 1 回の execute で複数の文を実行する」を注入（db_model_sql）にだけ当て、項目 1（全体が定数）では複文を検討していない。

仕様との関係は次のとおりです。R3-r1-1 と R3-r1-3 は、実装が §7.5 の字面どおりに動いています。R3-r1-1 は設計の観点が expected_is_correct=false としました。§7 の字義では内で、矛は §6 3-a（M は上界）から導かれる期待だからです。R3-r1-3 は §7.1（値を設定しない PRAGMA = 読み取り）と §7.5（`=` の無い PRAGMA = 読み取り）が食い違っていて、§9.3 はすでに `(` を想定しています。どちらも「表の導出漏れ」で、直すなら §7.5 の改訂が先です。R3-r1-2 は規則と実装の食い違い（review_plan §1 の (b)）そのものです。R3-r4-3 は、別の単位の R3-r2-1（定数どうしの Str に const が無い）と R3-r3-1（f 文字列 / 仮引数で動詞が 1 語の part になる）と関係しますが、機構は別です。review_plan §5 の既知の問題にはどれも入っていません。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも探索役の自己申告は D1+D2 で、旧文言「D3 / D4 だけなら low」を理由に下げた形跡はありません。ただし、第 1〜5 回は D3 / D4 を探さない範囲で行われたため、D4 への効き（先頭コメント・複文・書式の穴の INSERT が D4 で注記なしの内になる）はどの検証役も評価していません。R3-r1-2 の一般性の観点の low は「不として見える」を根拠にしていますが、これは D1 / D2 でしか成り立ちません。この単位の作業で D4 の黙った誤 clear を repro_scan で確かめたので、代表の重大度 medium を保つ根拠に加えました。
- **推奨の理由**: 直すことを推奨するのは R3-r1-2（先頭コメント）と R3-r1-1（複文）です。どちらも medium の判定を持ち、正しい答えが SQL の字句規則やライブラリの仕様から v2 / v3 と無関係に決まり（D61 の基準 1・2）、一般性の検証役が条件つきで正しい直し方を示し、凍結した語彙の追加も要りません。R3-r1-2 は剥がし方が SQL 文法から一意に決まり、値の確度を変えず、`/*!` を除けば反例がありません（S）。R3-r1-1 は分割器に sqlite3.complete_statement・ドル引用・不への退避の条件が要り、§7.5 の改訂も先に要ります（M）。どちらも矛が増える向きなので、CLAUDE.md の敵対的レビューを通してください。

限界として記録すること（O42 以降）を推奨するのは R3-r1-3 と R3-r4-3 の (b) です。3 観点とも low で、まれな書き方です。R3-r1-3 は v2 で 0 件です。R3-r4-3 (b) は engine の値の表現を変え、% を使うすべての値に効くので危険が大きい変更です。ただし R3-r1-3 は `op in ("=", "(")` の 1 行と §7.5 の文言だけで、反例も作れなかったので、同じ関数を触るついでに直す費用は小さいです。R3-r4-3 の (a)（先頭語に % / { / } があれば決めない）も判定を変えず、D4 の黙った内を不に直すだけの安全な変更です。この 2 つを同梱するかは学生の判断です。
- **所見**:
  - R3-r1-1: 代表。定数の複文の 2 文目以降を見ず、D1 / D2 の矛が注記なしの内になる（3 観点とも medium・false_clean）。設計の観点は「§7.5 の字面どおりで、規則の抜け」とした。直す。条件は、トリガ本体とドル引用を文の内側として扱うこと、分割できなければ不にすること、複文の矛には別の理由を付けること。（定数の複文 SQL（executescript / psycopg execute / exec_driver_sql）を先頭語だけで判定し、2 文目以降の DELETE / DROP が黙って「内」になる）
  - R3-r1-2: 同じ原因の別の表れ（先頭コメントを単語として読む）。D1 / D2 では矛 → 不（rule_mismatch。設計 medium / 一般性 low）。D4 では注記なしの内（この単位の作業で確認）。直す。条件は `/*!` を剥がさないこと、剥がして空なら不にすること。（SQL の先頭にコメント（`--` / `/* */`）があると先頭語が `--` になり、DELETE / UPDATE が「矛」でなく「不」になる）
  - R3-r1-3: 同じ関数の表の穴（PRAGMA の括弧形を読み取りにする）。3 観点とも low、v2 で 0 件、反例なし。基準では限界として記録。ただし §7.5 の文言と 1 行の変更で直せるので、同梱するかは学生の判断。（SQLite の括弧形の設定 `PRAGMA journal_mode(WAL)` / `PRAGMA user_version(3)` を「= の無い PRAGMA = 読み取り」として内に落とす（永続する設定なのに D1 矛 / D2 ）
  - R3-r4-3: 同じ原因の別の表れ（書式の穴 `%s` / `{}` を先頭語と読む。`_ev_BinOp` の % を連結として扱う）。3 観点とも low。(a)（先頭語を決めない）は安全で、D4 の黙った内を不に直す。(b)（engine での置換）は限界として記録を推奨。（`%` / `str.format` の書式テンプレートの先頭がプレースホルダで実引数に非リテラルが混ざる形（`"%s FROM t WHERE id = %s" % ("DELETE", os.environ["ID"])` / `"{}）

### U36 URL の分解（権威部・相対参照・列）（段階 A・重大度 中・推奨 一部直す）

openWorldHint（D3）の判定では、通信先の URL が「手元のマシン（localhost など）か、外部のホストか」を読みます。ところが URL を切り分ける処理が URL の正式な文法（RFC 3986）どおりになっていません。そのため (1) `http://user:pass@localhost/x`・`http://[::1]:8080/x`・`http://localhost./x` のような手元宛ての URL を外部ホスト宛てと読み、「宣言と矛盾」と誤って報告します（誤警報）。(2) base_url つきのクライアントに渡す `"items"`・`""`・`"?q=" + x` のような相対パスを、パスではなくホスト名として読み、誤警報や取りこぼしを出します。(3) `arun_many([...])` に定数の外部 URL を並べて渡すと宛先を「読めない」扱いにし、本来の矛盾を「不明」に落とします。

- **宣言**: D3　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: D3 の宛先を読む `_split_url` / `_host_class` が URL を RFC 3986 と値の形どおりに分解しない: `_split_url` は scheme 無しの権威部をそのまま `url.host` に置き、`_host_class` がそれを手書きの split で分解するので userinfo（`user:pass@localhost`）・角括弧 IPv6 + ポート（`[::1]:8080`）・末尾ドット（`localhost.`）の loopback を外部ホストにする; 相対参照を「`/` 始まり」しか認めず `"items"` / `""` / `"?q=" + x` を host に入れる（base_url の補完は host が無いときだけ）; `url.host` が列（`arun_many([...])` の Seq）のときは `Value.const`（Atom）しか読まないので定数の外部 URL の列も unknown にする。
- **コードの場所**: authgap/effects.py:460-509 _split_url, authgap/effects.py:518-533 _split_url_slots, authgap/dparse.py:260-282 _host_class, authgap/catalog/sinks.py:600-606 arun_many の proxy 行
- **重大度の根拠**: 単位の代表は R3d-r6-1 で、3 意見は探索 medium / 設計 medium / 一般性 low、中央値は medium。R3d-r6-2 は medium / low / low で中央値 low、R1d-r6-7 は 3 意見とも low。low の理由はどれも頻度か範囲の狭さで、「D3 だけに効くから」を理由にしたものは無い。R3d-r6-1 と R3d-r6-2 は、v2 run20（NET 効果 4,292〜4,298、定数の url.host 644、D3 net_external_host 49）と v3 に該当が 0 件。R1d-r6-7 は、url.host に列が入る語彙行が arun_many だけ。R3d-r6-1 の設計観点は、D62 のもとで D3 が主指標であることを明記したうえで medium と判定した。系統的な誤りで、同じ書き方なら常に同じ向きに外れ、規則 §7.3 と実装が食い違っている。なお頻度を v2/v3 の件数で見積もることは、最終評価データでの頻度を保証しない。探索役は corpus/ の文字列リテラル（テスト・vendored を含む）から、角括弧 IPv6 + ポートを約 60 行、userinfo つきの localhost / loopback を数十行数えた。R3d-r6-2 の形は `.get("/")` 494 / `.get("")` 269 / `.post("")` 95 行で、これは字面の数なので dict.get を含む。
- **直し方（一般に正しいか: 条件つきである）**: 共通: 規則 → 反例テスト → 実装の順で直す。直したら diff_effects と compare_scans で消えた行を 1 件ずつ確かめる。解決率を上げる向き（external→local、host→path）なので、敵対的レビューを通す。

[R3d-r6-1 権威部の分解]
直す場所は `_host_class`（dparse.py）だけ。`_split_url` は変えない。SSRF の座標（url.host の INJECT）は権威部全体のままでよく、§2.6 と整合する。候補の手順は次のとおり。
(1) 先に `ipaddress.ip_address(c.strip("[]"))` を試し、IP リテラルならそれで判定する。
(2) だめなら `urlparse(c if "://" in c else "//"+c).hostname` で host を取る。
(3) urlparse の ValueError は unknown にする。
(4) 権威部に `\` があれば unknown にする。
(5) 末尾ドットの `rstrip(".")` は名前の比較（localhost / .localhost / .local）だけに使い、IP の解釈には使わない。

素朴な直し方で壊れる反例（fix_sketch を字義どおり `urlparse("//"+c).hostname` + rstrip で入れた場合）:
(a) 角括弧無しの裸 IPv6 が退行する。`http://fe80::1/x` は hostname が 'fe80' になり 内→矛、`http://::1/x` は 内→不。守りは (1)。
(b) `http://[::1/x` では urlparse が ValueError を投げ、木全体が analysis_failed になる。runner.py:139 は RecursionError しか捕まえない。守りは (3)。
(c) `requests.get("http://evil.example\\@localhost/x")` は今 矛 で正しい（urllib3 は evil.example に接続する）。ところが urlparse / httpx は localhost と読むので 内 に落ち、新しい誤 clear になる。守りは (4) で、結果は 不 になる。クライアント間で読みが割れるので規則 4 に従う。
(d) `127.0.0.1.` は getaddrinfo が失敗するので、IP 側では rstrip しない。

守りつき候補を scratch で確かめた結果:
- テスト表 68 件で不一致 0、他の宣言の沈黙に違反 0、tests/ は exit 0。
- 所見の 6 件は 矛→内、対照 3 件は変わらない。
- 今の手書き分解が作っている誤 clear も直る。`http://localhost:pw@evil.example/x` と `http://10.0.0.5:80@evil.example/x` は今 内 だが、候補では 矛。
- `user:pass@api.example.com` と `user@evil.example:80` は external のまま。
- IPv4 写像 `[::ffff:8.8.8.8]` は ipaddress（3.10 / 3.12）が写像先で分類するので、external のまま。

テスト表に足す行: userinfo / 角括弧 IPv6 + ポート / 末尾ドット / 裸 IPv6 / 不正な角括弧 / バックスラッシュ / userinfo の中の `:` で localhost を装う形。
別件: `"://"` 側の分岐にも ValueError の穴がある。`httpx.get("http://[::1")` で今でも木全体が落ちる（数え落とし）。同時に捕まえるか、別に記録する。

[R3d-r6-2 相対参照]
fix_sketch の「先頭 part が英数字始まり・空文字なら url.path」は、字義どおり入れると健全でない。反例は次の形で、どれも今は 矛 net_model_host で正しいが、base が localhost なら 内、base が無ければ 不 に落ち（誤 clear）、GAP_INJECT も消える。
- `f"http{'s' if tls else ''}://{host}/x"`
- `"http" + ("s" if tls else "") + "://" + host + "/x"`
- `proto='https'; f"{proto}://{host}/x"`
- `"" + url`
- `_has_placeholder` の守りが無い場合の `"%s/items" % url`

一般に正しい条件（RFC 3986 では scheme は最初の `/?#` より前にしか書けない）。相対参照とみなすのは次の場合だけ:
(i) 値全体が 1 つの定数（後続の part が無い）で、`://` を含まず `//` で始まらない。`""` と `"/"` 単独を含む。
(ii) 定数の先頭 part に `/` `?` `#` のどれかがあり、最初のその位置より前に `:` が無く、先頭が `/` ではなく、`_has_placeholder` が偽。

`"/" + x` と `"//"` 始まりは §9.2 のまま分割しない。`"/"` 単独を相対にするのは §9.2 / D57 の字義（`"/"` だけは分割しない）を変える規則の改訂なので、逸脱として記録する。候補を scratch で確かめた結果、所見の 9 ユニットはすべて期待どおり、反例 7 件は 矛 のまま、tests/ は exit 0。base_url を構築子以外（`c.base_url = model`）で決める形は、矛 から 不 に移る。これは O32 と同じ限界で、誤 clear ではない。

[R1d-r6-7 列]
url.host が Seq / Argv のときは要素ごとに `_split_url` して分類する。判定は正の向きだけにする。
- 定数の外部ホストが 1 つでもあれば external。
- そうでなく、MODEL が選ぶ要素があるか、Seq 全体の `_choice` が chosen なら model。influenced なら model_opaque。
- それ以外は unknown。

Seq から local（内）は決して出さない。反例は alias_append（`other = urls; other.append(u)`）/ callee_append（`fill(urls, u)`）/ opaque_mutate（`some_unknown_lib.add(urls, u)`）/ dict_holder（`cfg['urls'].append(u)`）。どれも Seq は OP/resolved のまま 'http://localhost/a' だけを持ち、今は正しく 不 だが、「全部 local なら local」の枝を入れると 内（誤 clear）になる。この 4 形を 不 に固定する回帰テストを足す。callee が列を空にして localhost で詰め直す形では、まれに誤警報が出る。これは argv0 の要素に今すでに与えている信頼と同じなので受け入れる。
- **記録済みの限界・決定との重なり**: R3d-r6-1: O1〜O41・K1〜K7・逸脱 #19〜#24・review_plan §5 のどこにも、userinfo / 角括弧 IPv6 / 末尾ドットの記録は無い。D56 の手検証（net_external_host 37 件「規則どおり」）は本物の FQDN だけを見ており、権威部の書き方は点検していない。仕様書 539 行目の「`@` を含めば MODEL」は主体の規則で、宛先の類の話ではない。

R3d-r6-2: 一部が設計で反証されている。§9.2（contradiction_principles.md:283-294）と D57 / O32 が決めたのは、「`/` で始まり次が `/` でない」相対 URL だけ。定数 `"/"` 単独（local_base_root / ext_base_root）は §9.2・D57 の字義「`"/"` だけは分割しない」どおりで、今の 不 は仕様どおり（設計観点の corrected_expected）。変えるなら規則の改訂になる。ほかの形（`items` / `""` / `?q=` / `items/`+x）は決めた記録が無く、決定ではない（effects.py の docstring は D57 で更新されなかった既定の挙動にすぎない）。base_url を構築子からしか読まない限界は O32 で受け入れ済み。

R1d-r6-7: 記録は無い（decisions.md:327 は F8 の MODEL の urls のみ）。直し方の守りは、既知の限界 decisions.md:312-313（容器・引数・戻り値を通る別名は追わない）と関わる。contradiction_principles.md:310 は、矛→不 を誤 clear ではなく不明への移動としている（設計観点は向きを count_loss とした）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも D3 / D4 の追加回（第 6 回、§7.6〜7.7）の所見で、R3d-r6-2 と R1d-r6-7、R3d-r6-1 の一般性観点の検証役には D62 後の文言が渡っている。R3d-r6-1 の設計観点は最初の実行（Fable）だが、D62 / §7.5 で D3 は主指標だと明記したうえで medium とした。low にした意見の理由は、どれも v2/v3 に該当が 0 件か、語彙行が arun_many だけという頻度・範囲で、「D3 だけに効くから」ではない。
- **推奨の理由**: R3d-r6-1 は直す基準をすべて満たす（代表の重大度 medium、守りつきで一般に正しい直し方があり scratch で回帰 0、語彙の追加が要らない、設計観点でも反証されていない）。直す場所は `_host_class` 1 関数で、今の手書き分解が作っている誤 clear（`localhost:pw@evil.example`）も同時に直る。R3d-r6-2 と R1d-r6-7 はどちらも中央値が low で、まれな書き方（v2/v3 に 0 件、語彙行が arun_many の 1 行だけ）なので、基準に従い限界として記録することを勧める。R3d-r6-2 は素朴な直し方で誤 clear が出る条件が多く（scheme の分割、テンプレート）、`"/"` 単独は §9.2 の規則の改訂を要する。学生が直すことを選ぶなら、fix_outline の条件 (i)(ii) と「Seq から local を出さない」を必ず守ること。
- **所見**:
  - R3d-r6-1: 代表。権威部を scheme 無しで手書き分解するので、userinfo・角括弧 IPv6 + ポート・末尾ドットの手元宛てを外部と読んで誤警報になる（同じ原因で `localhost:pw@evil.example` は誤 clear）。3 観点とも生存、medium。守り (1)〜(5) つきで直すことを推奨（`_host_class` が `_split_url` の切り出した権威部（scheme 無し）を手書きで分解するため、ユーザ情報つき（`user:pass@localhost`）・角括弧 IPv6 + ポート（`[::1]:8080`））
  - R3d-r6-2: 同じ原因（URL を RFC 3986 どおりに分解しない）の別の表れで、相対参照を「/ 始まり」しか認めない。`"/"` 単独の 2 件は §9.2 / D57 の字義どおりで、設計観点で仕様どおりと反証済み。残りは生存だが中央値 low でまれなので、記録を推奨（直すなら条件 (i)(ii) つき）（`_split_url` が相対 URL を「先頭が `/` で次が `/` でない」形にしか認めないため、`base_url` つきクライアントへの `"items"`（先頭スラッシュ無し）・`""`・`"?q=" + x`・`"item）
  - R1d-r6-7: 同じ原因の別の表れで、url.host が列（arun_many）だと定数しか読まず、定数の外部 URL の列を 不 に落とす（矛の取りこぼし）。low で語彙行 1 つだけなので記録を推奨（直すなら正の向きだけにし、Seq から local を出さない）（`_host_class` が `url.host` の `Value.const`（Atom）しか読まないため、`crawl4ai.AsyncWebCrawler.arun_many([...])` の `urls`（`A(0, kw="）

### U39 デコレータ構文の照合（束縛したデコレータ・式の受け手・2 段重ね）（段階 C・重大度 中・推奨 一部直す）

解析器は `@mcp.tool(...)` のように「名前.tool」をそのまま書いたデコレータしかツールの入口と認めません。次の 3 つの書き方では、ツールが丸ごと消えるか、宣言（readOnlyHint など）が読まれません。(1) `ro_tool = mcp.tool(annotations=...)` と変数に入れてから `@ro_tool` と書く、(2) `@get_mcp().tool(...)` や `@SERVERS["fs"].tool(...)` のように受け手が関数呼び出しや添字になっている、(3) 登録のデコレータを 2 段重ね、外側に宣言なし・内側に宣言ありと書く。向きはどれも誤 clear（矛盾があるのに「矛盾なし」と出る）で、(1)(2) はツールそのものが数えから消えます。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `find_units` のデコレータ照合（`_decorator_calls` → `_match_decorator`）が `@<dotted 名>.tool(...)` を直接書いた形だけを規則 1 に当てる: デコレータを変数に束縛した `ro_tool = mcp.tool(...)` の `@ro_tool` は末尾名が tool でないので外れ、受け手が Call / Subscript（`@get_mcp().tool(...)` / `@SERVERS["fs"].tool(...)`）は `dotted_of` が None で捨てられ、カタログのデコレータが 2 段重なると最初の 1 つで `break` して内側の登録の宣言を捨てる。
- **コードの場所**: authgap/entries.py:235-259 _decorator_calls / _match_decorator, authgap/entries.py:376-441 find_units のデコレータの走査
- **重大度の根拠**: 代表の R2-r2-1 は 3 意見とも medium（探索役・設計・一般性）。共通の annotations を変数にまとめる書き方は一般的な Python で、この書き方を使う木では宣言つきのツールに偏って消える。v2 では 1 木（corpus/v2-8dionysus__abyss-stack）で、一般性の検証役が ast で数えて 12 ファイル 159 回の適用（設計の検証役の grep では 133 行。数え方の違い）。run20 ではこの木のユニットは 21 しかない。R2-r4-2 / R2-r4-3 は 3 意見とも low で、根拠は v2/v3 での出現が 0（探索役の grep。R2-r4-3 は 72,586 ファイル中の登録デコレータの 2 段重ね 2 件で、どちらも typer の app.command で MCP ではない）。どれも D1+D2 に効くと申告されており、low は「D3/D4 だけ」の理由ではない。修正後に増えるユニットと CONTRADICTION の件数は未測定（abyss-stack の注釈は snake_case なので、D が立つかは R2-r1-1 の扱いしだい）。
- **直し方（一般に正しいか: 条件つきである）**: [R2-r2-1 束縛したデコレータ] `find_units` で、デコレータが素の名前（Name / dotted 名）のとき、その名前が何に束縛されているかを調べる。束縛先の右辺が規則に当たる `<srv>.tool(...)`（Call）か `<srv>.tool`（Attribute）なら、その Call を `call` として今と同じ経路（_kwarg_str(name) / _kwarg_node(annotations) / _read_annotations）で読む。守ること:
(a) 束縛の解決には D61 改訂 G3 の条件 1 をそのまま使う。条件は「束縛がちょうど 1 つ」「モジュール直下（入れ子定義なら囲む関数本体）」「関数の中で書き換えられない（_scan_module_writes に無い）」の 3 つ。反例 cx_r2_1_global では、モジュール直下で `ro_tool = mcp.tool(annotations=RO)` とした後、import 時に呼ばれる configure() が `global ro_tool; ro_tool = mcp.tool()` と束縛し直す。モジュール直下の Assign だけを引く素朴な直し方だと readOnly のユニットができ、os.remove に D1 の誤警報を出す（今は 0 ユニットで誤警報なし）。この木では _scan_module_writes = {ro_tool, path} なので、条件を付ければ除外される。
(b) 束縛が 1 つに決まらない場合（cx_r2_1_conditional: if/else でモジュール直下に 2 回束縛する）。探索役の案は「ユニットにして annotations を unreadable（D_unknown）」だが、一般性の検証役は「一致する束縛がちょうど 1 つでなければユニットにせず、件数だけ manifest に出す」方が厳密だとした。束縛の片方が登録でないと偽のユニットになりうるからである（規則 4 に従い、黙って落とさず数える）。
(c) 変数名が偶然 `tool` の場合（`tool = mcp.tool(); @tool`）。今は末尾名の規則が先に当たり、call=None なので束縛先の annotations を読まない（form=None で ⊥ になる、誤 clear の変形）。素の Name のデコレータでは、末尾名の規則より先に束縛を引く。
(d) 別モジュールから import した束縛（`from .reg import ro_tool`）は、G3 の import 追跡を使わない限り数え落としのまま残る（誤警報にはならない）。記録しておく。
(e) 末尾名 `tool` の照合を広げるわけではないので、新しい種類の過剰収集は無い。右辺が規則外（自作レジストリ）なら今までどおり入口にしない。
[R2-r4-2 式の受け手] `_decorator_calls` で dotted_of が None のときは、Attribute の連鎖を上からたどり、底が Call / Subscript でも末尾の属性名を返す補助関数を使う（擬似名 `<expr>.tool`）。`_match_decorator` には末尾成分を渡し、受け手が式だったことを Unit / manifest に残す。規則 1 はもともと受け手の型を見ていない（ce_r4_2 の `box.tool(...)` は今も decorator/mcp のユニットになる）ので、過剰収集の性質は変わらない。変わるのは、同じ関数に重なった登録のうち最初に当たる相手だけで、正しい方向に変わる。
[R2-r4-3 2 段重ね] 規則に当たる登録デコレータを全部集め、annotations= を持つ登録ごとに D を作り、D1 / D2 は登録ごとに判定して OR する（どれかの登録に矛があれば矛）。上界の交わりで近似してもよいが、フィールドをまたいで混ぜない。annotations= を持つ登録が 1 つも無いときだけ、従来どおり form=None で join に任せる。反例 ce_r4_3: `@public.tool(annotations=RO)` と `@admin.tool(annotations=readOnlyHint=False, destructiveHint=True)` が重なる形。探索役の案「値が食い違えば unreadable（D_unknown）」を使うと、今正しく出ている public 側の contradiction:D1 が dparse.py:178 の DKind(unknown=True) に落ちて消える。この案は使わない。2 つの登録の宣言を 1 ユニットでどう合成するかは Def 6 に無い（設計の検証役）ので、学生の決定が要る。決めないなら open_questions に不明として記録する。
[共通] 行が増える向き（ユニットの追加）なので、CLAUDE.md の敵対的レビューを通す。規則 → 反例テスト（上の cx / ce をそのまま使う）→ 実装の順で進める。run21 を取り、diff_effects / compare_scans で増えたユニットを 1 件ずつ見る。preregistration に逸脱として記録し、fingerprint を作り直す。
- **記録済みの限界・決定との重なり**: 3 件とも、設計の観点で反証されていない（refuted=false）。検証役が decisions / open_questions / f0a_checks / K1〜K7 を grep しても、意図した決定・記録済みの限界は無かった。ENTRY_RULES の規則 1（decorator / mcp.tool）は語彙の中にあり、欠けているのは束縛・受け手の式を読む部分だけなので、review_plan §2 の「入口の規則の追加」ではなく「語彙にある規則が当たらない」側（§1 (a)）に入る。関連: D17 改訂 4（同じ関数を 2 ユニットにしない）は設計だが、宣言を最初のデコレータだけから取る決定ではない（R2-r4-3 の設計の検証役）。R2-r1-2（デコレータ構文でない呼び出し形 `mcp.tool(...)(fn)` の登録。high）とは根本原因が別で、f0a_checks.md:1185 の `study_assistant = tool(...)(fn)` はそちら側。R2-r1-1（snake_case の ToolAnnotations を版を見ずに D_malformed にする。high）と連動し、abyss-stack で増えるユニットの D が立つかはその扱いしだい。D61 G3（別名つき import・再公開の解決）は「束縛の解決は解析器の欠陥として直す」先例で、その健全性の条件 1 をここでも使う。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも影響は D1+D2 と申告され、low の 2 件（R2-r4-2 / R2-r4-3）の理由は v2/v3 での出現 0 件で、「D3/D4 だけなら low」の文言によるものではない。
- **推奨の理由**: 代表の R2-r2-1 は medium で、条件（D61 G3 の条件 1 と、束縛が 1 つでなければユニットにしない）を付ければ一般に正しい直し方がある。語彙の追加も要らず、設計の反証も無いので fix の基準を満たす。R2-r4-2 は low で v2/v3 に 0 件と、基準では「low でまれな書き方」にあたり記録になる。ただし同じ関数（_decorator_calls）に補助関数を 1 つ足すだけで、新しい過剰収集も無いので、R2-r2-1 と一緒に入れる選択肢もある（学生の判断）。R2-r4-3 は low・0 件で、2 つの登録の宣言の合成規則が Def 6 に無く学生の決定が要るので、限界として記録（O42 以降）を推奨する。直す場合は「食い違い → unreadable」を使わず、登録ごとに判定して OR する。
- **所見**:
  - R2-r2-1: 代表（medium ×3）。`ro_tool = mcp.tool(annotations=...)` のあと `@ro_tool` と書くとツールが丸ごと消える。直す。条件は G3 の条件 1（反例 cx_r2_1_global）、束縛が 1 つでなければユニットにしない（cx_r2_1_conditional）、名前が偶然 `tool` のときも束縛を先に引く。野外 1 木で 159 回（ast。grep では 133 行）。（デコレータを変数に束縛した登録（ro_tool = mcp.tool(annotations=...); @ro_tool def f）は末尾名が tool でないので入口にならず、ツールが宣言ごと丸ごと消える（数え落とし・誤 clear。）
  - R2-r4-2: 同じ原因の別の表れ（low ×3）。受け手が Call / Subscript（`@get_mcp().tool` / `@SERVERS["fs"].tool`）だと dotted_of が None になり、デコレータごと捨てられる。v2/v3 では 0 件。基準では記録だが、直し方は一般に正しく小さい（末尾の属性名で照合する）ので、R2-r2-1 と一緒に入れてもよい。（R2-r4-2 [R2] デコレータの受け手が Call / Subscript のとき（`@get_mcp().tool(annotations=...)` / `@SERVERS["fs"].tool(annotations={...}）
  - R2-r4-3: 同じ走査の別の表れ（low ×3。誤 clear）。登録デコレータの 2 段重ねで、最初の 1 つで break して内側の宣言を捨てる。v2/v3 では MCP の該当 0 件。合成規則が Def 6 に無く学生の決定が要るので、限界として記録を推奨。直すなら登録ごとに判定して OR する（「食い違い → unreadable」は反例 ce_r4_3 で正しい矛を消す）。（R2-r4-3 [R2] 同じ関数にカタログのデコレータが 2 段重なる（`@mcp.tool()` の下に `@admin.tool(annotations=ToolAnnotations(readOnlyHint=True))`、`@t）

### U42 低レベルの name 判定の認識（段階 C・重大度 中・推奨 一部直す）

低レベル MCP のサーバは、ツールを 1 つのハンドラ（call_tool）にまとめ、`if name == "delete_note":` のように name で分岐します。解析器はこの分岐を読んで「どのツール宣言（readOnlyHint など）をどの効果に当てるか」を決めますが、読める書き方が狭すぎます。分岐を別関数に任せる形（`return await dispatch(name, arguments)`）、Enum との比較（`name == ToolName.DELETE`）、否定形（`if name != "x": raise`）、定数を左に書いた比較（`"x" == name`）からはツール名を取れません。すると宣言が 1 つも結び付かず、書き込みがあっても矛盾が出ません（誤 clear）。逆に、比べている左側が name かどうかを見ないので、`arguments["action"] == "write"` のような引数の比較も、同じ名前のツールの判定として数えます。その結果、別のツールの宣言で矛盾が出ます（誤警報）。

- **宣言**: D1 / D2 / D3 / D4　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 低レベルハンドラの name 分岐を読む `dispatch_name_candidates`（Tool リテラルを join する候補名）と `_dispatch_test_names`（効果の帰属）が name 判定の形を狭く、かつ緩く読む: `if name == "x"` / `in (...)` しか読まず、Enum 比較（`== ToolName.DELETE`。match では Enum 表を引くのに Compare では引かない）・否定形（`!=` / `not in` で raise）・定数が左の比較・別関数への委譲（`dispatch(name, arguments)`）からは候補を取らない一方、比較の左が name 変数であることを要求しないので `arguments["action"] == "write"` までツール名の判定に数える。
- **コードの場所**: authgap/entries.py:748-764 dispatch_name_candidates, authgap/entries.py:674, 899, 927-940 find_lowlevel_units の join, authgap/analyze.py:553-563 _dispatch_test_names
- **重大度の根拠**: 代表は R2-r1-3（委譲）で、探索役・設計・一般性の 3 意見とも medium。委譲という特定の書き方でだけ起きますが、起きた木では宣言が丸ごと消えます。v2 の実例は低レベルユニット 10 件中 1 件（claude-replay）で、Tool 10 件（readOnlyHint / destructiveHint 付き）に対し、FS_WRITE・SPAWN・DB の効果があっても矛盾の注記が 0 でした（探索役と設計の検証役が run20 で確認）。残り 3 件は 3 意見とも low です。v2/v3 で数えた件数は次のとおりです。Enum 比較は 0。否定形の guard は 89 ファイル中 6 件で、6 件とも == の分岐も持つため、純粋な guard 形は 0。左定数形は 0。引数の値がツール名と重なる比較は 0。宣言の読み取りへの効き方: join が落ちると 4 つの宣言（readOnly / destructive / openWorld / idempotent）がまとめて ⊥ になります。誤った帰属では、meet が explicit と idempotent を和で取るので、D3 / D4 にも同じ仕組みで効きます。ただしこれはコードから導いたもので、検証役は D3 / D4 の件数を測っていません（未測定）。4 件とも影響は D1+D2 と自己申告されており、旧文言「D3 / D4 だけなら low」で重大度が下がった形跡はありません。
- **直し方（一般に正しいか: 条件つきである）**: 4 つを別々に直さず、「比較の左が name（ハンドラの name 仮引数 / params.name）に由来するか」を先に決めてから候補と帰属を広げる順にします。広げる向き（候補を増やす）と絞る向き（帰属を正確にする）を 1 つの変更で片方だけ入れると、誤 clear が誤警報に入れ替わるだけです。

(1) R2-r2-4（左が name でない比較）: 絞るのは帰属側（analyze._dispatch_test_names）だけにし、候補側（dispatch_name_candidates）は緩いままにします。左の式の値の出自が name 仮引数 / params.name であることは、val エンジンの roots で判定します。【避ける条件】「name 仮引数か単純代入の別名」という構文の一覧で限ると、`tool = name.strip().lower(); if tool == "write_note"` を追えません（反例 ce24）。この場合は全ツール帰属に落ち、readOnly の read_note の宣言で D1 の誤警報に退行します（誤 clear にはなりません）。候補側を絞ると、別名を追えないときに join が減って誤 clear に振れます。帰属を絞った結果、認識できない比較は全ツール帰属（より厳しい meet）に落ちるだけなので、誤 clear は生まれません。R3-r4-1（入れ子の判定の和を積にする、別の単位）を直すなら、その前提として必須です。左を見ないまま積にすると `arguments["mode"] == "rm"` で peek の readOnly を失い、誤 clear になります。

(2) R2-r2-2（否定形・左定数）: 候補側には NotEq / NotIn と、左が定数の Eq / NotEq を足してよいです（join が増える向き）。帰属側は否定形の極性を反転し、「真側から効果に届かない」ときだけ帰属します。反転しないなら帰属に使わず、全ツール帰属に落とします。【反例 ce22b】`!=` を `==` と同じ極性で gates に渡すと、`if name != "append_log": os.remove(...)`（readOnly の reader から届く）が {append_log} だけに帰属し、今は出ている正しい D1 が消えます（新しい誤 clear）。(1) と同時に入れます。

(3) R2-r1-7（Enum 比較）: dispatch_name_candidates と _dispatch_test_names の両方で Enum を解決します。【条件】`Class.MEMBER` のキーだけを引きます（裸名 `READ` は複数クラスで衝突します）。末尾の `.value` は落とします。裸のメンバとの比較は str 混在の Enum か StrEnum に限ります（`name == PlainEnum.X` は実行時に真になりません）。【反例 c7_enum_mixed】候補にだけ足して帰属を変えないと全ツール帰属になり、read_note の readOnly が meet で入って、destructive の delete_note の os.remove に D1 の誤警報が出ます。match 版（c7_match_mixed）は今すでにこの誤警報を出しています（§2.9 (g) の保守側の選択）。

(4) R2-r1-3（委譲）: 候補名の収集を「ハンドラの name 仮引数をそのまま渡す木内の呼び出しで、index.lookup_function で一意に解決できる先」に広げます。【反例 cx_r1_3_mixed】所見の素案どおり候補だけ集めて帰属をハンドラの CFG のままにすると、ハンドラには name の判定が無いので全ツール帰属になります。宣言が混ざる木（delete_note は無宣言で os.remove、read_note は readOnly で読むだけ）では、os.remove に D1 の誤警報が出ます。claude-replay（RO と非 RO が混在する 10 ツール）では、委譲先の書き込み・SPAWN・DB がすべて D1 矛になり、核の件数を水増しします。一般に正しい形は、効果の証人鎖の各フレームの CFG で、呼び出し先の対応する仮引数に対する name 判定の支配を見ることです（インライン展開の意味を帰属にも使います）。`dispatch(name.removeprefix(...))` のように変換して渡す場合は、候補が Tool 名に一致しないので join されず、誤警報になりません。最小案は verdict を変えずに、「委譲先で候補名が見つかったが未 join」の件数だけを出すことです（規則 4）。§2.9 (a) の「ハンドラ本体の」を広げるので、preregistration §5 の逸脱として記録が要ります。直したら claude-replay の全効果行を compare_scans で 1 件ずつ見ます。

(5) 評価の道具（scripts/ だけ）: 設計の検証役の記録事項です。§2.9 (d) の「未 join の件数を出す」は report.summary() の annotations_join にはありますが、scan_v2 / repro_scan が書く manifest_json（evidence/scan_v2_run20/*.json）には無いため、学生が使う経路では「Tool リテラルがあるのに 1 件も join されない」が見えません。scripts/scan_v2.py で res.tree.n_tool_literals / n_annotation_joined / n_annotation_unjoined（runner.py:106-110 で既に計算済み）を木ごとの行と summary に書き出せば、指紋に触れずに黙った ⊥ を見えるようにできます。authgap/report.py の manifest_json を変える形にすると指紋が変わるので避けます。

候補を増やす変更（(2)(3)(4) の候補側）は、⊥ から宣言つきになり矛の行が増える向きなので、CLAUDE.md の敵対的レビューにかけます。
- **記録済みの限界・決定との重なり**: 設計の観点で反証された所見が 2 件あります。R2-r1-3（委譲）は、prereg §2.9 (a) が候補名を「ハンドラ本体の name == "<literal>" 分岐」から取ると明記しているため、「規則どおり」と判定されました（dispatch_name_candidates の docstring の「読めない形は候補にしない」、tests/test_dispatch_join.py、O5 の暫定 (a)、D28 (4) による優先度の引き下げも根拠）。ただし、委譲の形を検討して除外した記録はどの文書にも無く、効果側は深さ 4 まで降りるのに宣言側は深さ 0 という非対称にも議論がありません。R2-r1-7（Enum 比較）は、docstring の「4 形だけを読む」と §2.9 (a) の文言どおりとして反証されました。ただし match では同じ Enum 表を引く拡張が D 番号なしで入っており、Compare との不揃いは検証役自身も「迷いあり」としています。R2-r2-2 と R2-r2-4 は設計の観点も生き延びました。否定形・左定数・左辺を見ないことを決めた記録は D28 / D29 / O5 / §2.9 (g) に無く、R2-r2-4 は §2.9 (b)「name == "<t>" 判定」との食い違い（review_plan §1 の (b) 型）です。関連: §2.9 (g) は match 文の全ツール帰属を保守側の選択として記録済みです（本単位の Enum の反例 c7_match_mixed はこの既知の挙動）。R3-r4-1（入れ子の判定の和。別単位）は、R2-r2-4 の直し方を前提に持ちます。review_plan §5 の既知の問題（MAX_DEPTH、O33、D17 など）とは重なりません。訂正: R2-r2-2 の「未 join の件数にも現れない」は不正確です（設計の検証役の指摘）。木単位の n_annotation_unjoined には数えられます。ただし scan_v2 の manifest には出ません。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも自己申告の影響は D1+D2 で、検証役の重大度意見（R2-r1-3 は 3 意見とも medium、他 3 件は 3 意見とも low）の理由は、書き方のまれさ（v2/v3 の測定で 0 件など）でした。「D3 / D4 だけなら low」を理由にした形跡はありません。
- **推奨の理由**: 推奨の基準をそのまま当てると、解析器の側はどれも fix に届きません。代表の R2-r1-3 は medium で一般に正しい直し方もありますが、設計の観点が §2.9 (a) の文言どおりとして反証しています。R2-r1-7 も設計で反証済みで、low、v2 は 0 件です。R2-r2-2 と R2-r2-4 は設計を生き延びましたが、low で、v2/v3 の測定では誤りになる形が 0 件のまれな書き方です。さらに、正しく直すには (1)→(2)(3)→(4) の順で帰属側（val の roots による左辺の出自、否定形の極性、委譲先の CFG での支配）まで入れる必要があります。候補だけ広げると、ce22b / c7_enum_mixed / cx_r1_3_mixed のように誤 clear が誤警報に入れ替わるか、新しい誤 clear が出ます。規模は L で、§2.9 (a)(b) の文言変更（逸脱の記録）と、行が増える向きの敵対的レビューを伴います。そこで解析器の 4 件は限界として記録し（O42 以降。上の反例と避ける条件も併記）、評価の道具の欠落だけを直す、という推奨にします。欠落とは、scan_v2 の出力に §2.9 (d) の未 join の件数（Tool リテラル数 / join 数 / 未 join 数）が無いことです。これは scripts/scan_v2.py だけで直り、解析器の指紋に触れません。最終評価の手判定で「宣言つきの Tool があるのに黙って ⊥」のサーバ（委譲・Enum・否定形のどれでも）を見つける手がかりになります。学生が R2-r1-3 を直すと決める場合は、帰属も委譲先の CFG で行う形に限り、素案の「全ツール帰属のまま」は採らないこと。また R3-r4-1 を直すなら、R2-r2-4 の帰属側の絞り込みを同時に入れることが条件です。
- **所見**:
  - R2-r1-3: 代表（medium、誤 clear）。name の分岐を別関数に委譲すると join 候補が 0 になり、宣言が黙って ⊥ になる。v2 の実例は claude-replay の 1 件。設計の観点は §2.9 (a)「ハンドラ本体の」どおりとして反証、一般性の観点は条件つきで生存（帰属も委譲先の CFG で行うこと。素案のままだと cx_r1_3_mixed で誤警報）。推奨: 解析器は限界として記録し、scan_v2 に未 join の件数を出す道具の修正で見えるようにする。（低レベルハンドラが name 分岐を別関数（dispatch(name, arguments)）に委譲すると、効果はその関数から拾うのに join は手前のハンドラ本体しか見ず、全ツールの宣言が黙って未 join（⊥）になる（誤 clear）
  - R2-r1-7: 同じ原因の別の表れ（low、誤 clear）。Compare では Enum 表を引かない（match では引く）。設計の観点は docstring「4 形だけ」と §2.9 (a) どおりとして反証（迷いあり）。一般性の観点は条件つきで生存（両側で解決する、Class.MEMBER だけ、.value を落とす、str 混在 Enum に限る）。v2 は 0 件。推奨: 限界として記録（match との不揃いも明記）。（`if name == ToolName.DELETE:` / `== ToolName.READ.value`（Enum 比較）から候補名を取らず、文字列名の Tool リテラルが 1 つも join されない（match 文では同じ E）
  - R2-r2-2: 同じ原因の別の表れ（low、誤 clear）。否定形の guard と左定数の比較から候補が取れない。設計・一般性とも生存。条件は、帰属側で否定形の極性を反転するか全ツール帰属に落とすこと（素朴な同極性では ce22b が誤 clear）。v2/v3 の純粋な guard 形は 0。推奨: 限界として記録（直すなら R2-r2-4 と同時に）。（低レベルハンドラの name 分岐が否定形（`if name != "x": raise` / `if name not in ("x",): raise`）や定数が左の比較（`"x" == name`）だと候補名が 1 つも取れず、Too）
  - R2-r2-4: 同じ原因の逆向きの表れ（low、誤警報）。比較の左が name かを見ないので、引数値の比較がツール判定に数えられる。§2.9 (b) との食い違い（(b) 型）。設計・一般性とも生存。条件は、帰属側だけ絞り、val の roots で出自を見ること（構文の別名一覧だと ce24 が誤警報に退行）。v2/v3 は 0 件。推奨: 限界として記録。ただし R3-r4-1（和を積に）を直すなら、その前提として同時に直す。（引数値の比較の定数（`arguments["action"] == "write"`）が join 済みツール名と一致すると、その分岐の効果がそのツールにも帰属し、別ツールの厳しい宣言（destructiveHint:false）で矛にする）

### U43 低レベルの効果のツール帰属（段階 C・重大度 中・推奨 一部直す）

低レベル MCP では 1 つのハンドラ `call_tool(name, arguments)` が `if name == "..."` で分岐して複数のツールを受け持ちます。解析器は、分岐の中の効果（ファイルの削除やコマンドの実行）がどのツールのものかを決め、そのツールの宣言（readOnlyHint など）と照らします。ところが次の書き方では、効果が関係のないツールにも付けられ、別のツールの「読み取りだけ」の宣言で矛盾と判定されます（誤警報）。(1) 呼び出しが複数行の文の 2 行目以降から始まる（black 整形の `return [TextContent(..., text=f(...))]`）。(2) name の判定が入れ子になっている。(3) `name == "a" or name == "b"` と書いている。(4) 判定しているツール名が list_tools と結び付いていない。もう 1 つ、複数のツールに付いた共通処理の効果は readOnly が 1 つでもあると D1 でしか判定されず、D2 / D4 の宣言ごとの件数から落ちます（数え落とし。今の事前登録 §2.9 (c) の文言どおりの動作です）。

- **宣言**: D1 / D2 / D4　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_attribute_effects_to_tools` が効果を支配する name 判定からツールを決める合成が誤る: 支配する判定の候補名を和（`attributed |= names`）で集めるので入れ子の判定では外側の全ツールに帰属し（積であるべき）、`name == "a" or name == "b"` は短絡 CFG の 2 つの test がどちらも単独では支配しないので全ツール帰属に落ち、支配する名前が join されていないと「共通処理」として join 済み全ツールに帰属する; 効果の呼び出し式が文の先頭行より後の行から始まると CFG ノードが無く全ツール帰属（FastMCP では cfg.exit）に落ち; 複数ツールに帰属した効果は `meet_d_kind` で explicit を和にした 1 つの宣言で判定するので D2 が評価されない。
- **コードの場所**: authgap/analyze.py:565-591 _attribute_effects_to_tools, authgap/cfgbuild.py:93 by_line / 584-598 短絡の CFG, authgap/dparse.py:128-161, 443-471 meet_d_kind / 複数ツールの判定, authgap/val/engine.py:751, 1067 entry_site の行, authgap/effects.py:673 entry_lineno
- **重大度の根拠**: 単位の重大度は、所見のうち最も重い代表値に合わせて medium にした。代表値は探索役・設計・一般性の 3 意見の中央値。R4-r1-7 は medium（medium / medium / low）。black 整形の `return [TextContent(type="text", text=...(...))]` はよく出る書き方で、条件はありふれている。ただし run20 の実測では、低レベル dispatch_join のユニット 4 件のうち全ツール帰属になった効果は napjon の 1 件だけで、そのハンドラのツールは 1 つなので誤警報は 0。FastMCP（2,231 ユニット中 2,205）では D1/D2 に効かず、付録の req_occ / req_val に効くだけ。R3-r4-1 は中央値が low（medium / low / low）。検証役が数えると、handler 候補 953 ファイルで該当する本物の call_tool は 1 か所で、内側の分岐に効果が無い。v2/v3 で真部分集合への複数帰属は 0 件。R2-r1-6 は low（v2 の低レベルユニット 10 件中 0）。R2-r2-5 は low（89 ハンドラファイル中 0 件）。R3-r1-4 は low（run20 で readOnly と destructiveHint:false が混ざるハンドラは 0 件）。すべての向きが誤警報か数え落としで、今の動作による誤 clear は無い。R3-r1-4 の検証役は「主指標（D1+D2 の矛の組）と verdict は変わらないので low」と書いた。これは D62 より前の枠組みで、D62 では宣言ごとの件数（D2・D4 の列）そのものが主指標なので、この理由は弱くなる。それでも low のままにしたのは、出現 0 件という測定が根拠として残るため。
- **直し方（一般に正しいか: 条件つきである）**: 【R4-r1-7 複数行の文（直す推奨）】探索役の主案「engine が実行中の文の行を entry_site にする（複合文ならヘッダの行）」は一般に正しくない。CFG の test ノードは葉の式の行に作られる（cfgbuild.py:565-575）。そのため、複数行の `if (` の test の中の効果（ce7_multiline_test）が、今は run だけに正しく帰属しているのに、If の行に寄せられて全ツール帰属になり、新しい D1 誤警報になる（patchC_stmtline で確認）。正しい形は patchD_spanfallback。`cfg.nodes_for_line` に「その行にノードが無いときだけ、その行を lineno..end_lineno に含む**単純文**（Assign / AnnAssign / AugAssign / Expr / Return / Raise / Assert）のノードを返す。候補が複数なら最も狭い範囲」を足す。行にノードがある場合の挙動も entry_lineno の値も変えないので、two_sided / diff_effects の鍵は動かない。h8 は直り、ce7 は今のまま、check_gates は B3a 8/8・B3b 15/15 で変わらない（検証役が写しで確認）。避ける条件: by_line を構築時に広げる eager 版は使わない。内包表記のノードと単純文のノードが同じ行に並ぶので、付録 G の g07 を動かしうる（未確認）。複合文には広げない。残る形（未測定。直すなら反例テストで確かめる）: `for x in (\n f(...))` のように for のヘッダの反復式が複数行にまたがる形。`with a(\n b(...)) as c:` のように enter_cm ノードの式の途中の行から呼び出しが始まる形。nodes_for_line は FastMCP の req_occ / req_val（analyze.py:468、`or [cfg.exit]`）でも使うので、付録の座標が変わる。取り直しの後に diff_effects / compare_scans で消えた行を 1 件ずつ確かめる。

【R3-r4-1 入れ子の判定（記録を推奨。直すなら次の条件つき）】探索役の素朴な案「支配する判定の候補名の積、any(gates) のまま」は、今は正しい readOnly の D1 矛を 4 つの形で消す（誤 clear）。CE1: 内側の判定が別の変数で、リテラルがツール名と偶然一致する（`arguments.get("mode") == "rm"`）。CE2: `name = arguments.get("op", name)` で名前を束縛し直す。CE3: 外側のタプルに非リテラルの要素が混ざる（`("rm", PEEK, "mk")`）。CE4: finally の後片付けで、return の複製だけが内側の判定にゲートされる。積を取ってよいのは次の P0〜P4 をすべて満たすときだけ。1 つでも外れたら今の和に戻す。P0: 主語は dispatch 仮引数（unit.params[0]）。P1: 各判定の左辺がその名前の ast.Name そのもの（`name.lower()` や `arguments.get(...)` は不可。R2-r2-4 の直し方と同じ）。P2: その名前がユニット内で束縛し直されない（Store/Del、global/nonlocal、except as、import as、match の as/star、for/with/walrus の対象。入れ子スコープも保守的に含める）。P3: 比較の相手が str 定数か、全要素が str 定数のタプル・リスト・集合。P4: finally の複製ごとに積を取り、複製の間は和にする。積が空なら全ツール。手順: §2.9 (b)（複数の支配判定の合成を決めていない）の文面を先に改める。結果が緩む向きなので §2.9 (f) に従って逸脱として記録する。反例テストには所見の 3 木と CE1〜CE4 を入れる。

【R2-r2-5 `or` 形（記録を推奨）】直すなら、短絡で分解した test 列に元の BoolOp(Or) を持たせる。次の 3 つをすべて満たすときだけ、全項の名前の和に帰属する。(i) 全項が name 判定である。(ii) 列の偽の出口から効果に届かない。(iii) 列の先頭の test が効果を支配する。1 つでも省くと `or` の外の共通処理まで名前に帰属し、誤 clear になる。Not を一緒に扱えば `if not (name == a or name == b): raise` の否定形の誤警報も直る。

【R2-r1-6 未 join の名前（記録を推奨）】探索役の案「`_dispatch_test_names & set(unit.dispatch_names)`」は誤 clear を作る（反例 c6_shared_mode）。dispatch_names は handler の中の `x == "str"` をすべて集める（`"w"`、`"http"`、`"ok"` など。run20 の xagent と napjon で実在）。そのため共通処理の `arguments.get("mode") == "w"` が未 join のゲートと見なされて ⊥ になり、今は正しい D1 矛が消える。条件: 左辺がハンドラの name 仮引数である判定だけをゲートにする（R3-r4-1 の P1 と同じ）。もう 1 点。`name in ("a","b")` で片方だけ join 済みのとき、未 join 側の ⊥ を meet に入れると upper が ⊥ になり、GAP 側の扱いが変わる。どちらに倒すかは実装の前にテストで決める。

【R3-r1-4 共通効果の D2/D4（記録を推奨）】直すなら、帰属先ツールごとの DKind（d_kind_by_tool）で contradiction_findings を呼び、(宣言, 結果, 理由) の和を取る。upper の積（SELECT / INVENTORY 用）には触らない。検証役は、所見が消える反例を作れなかった（ツールごとの和は meet の所見の上位集合）。ただしこれは §2.9 (c)「readOnly が 1 つでもあればそれで判定」の改訂になるので、decisions に解釈を書いてから逸脱として入れる。
- **記録済みの限界・決定との重なり**: R3-r1-4 は、設計の観点で反証済み（refuted=true）。事前登録 §2.9 (c)（preregistration.md:442-446）は、複数ツールに帰属する効果を「readOnly を宣言するツールが 1 つでもあればそれで判定する」と定めており、今の出力はその文言どおり。(g) の「各ツールで判定した結果の和集合と同じ」は verdict の有無の話で、宣言ごとの件数（D56 で後から入った）には触れていない。一般性の観点は反証せず、「(c) と (g) のどちらを読むか」を設計側に委ねた。ほか 4 件（R4-r1-7、R3-r4-1、R2-r2-5、R2-r1-6）は、設計の観点でも記録済みの限界・仕様どおりに当たらない。§2.9 (g) と docstring が全ツール帰属を保守的と明記しているのは `match` 文と「どの判定にも支配されない共通処理」だけで、複数行の文、入れ子、`or`、未 join の名前は、decisions / open_questions / K1〜K7 / 逸脱 #1〜#23 のどこにも無い。ただし R3-r4-1 については、一般性の観点が「§2.9 (b) は複数の支配判定の合成を決めておらず、字義どおりなら和とも読める。『書いた規則との食い違い (b)』は言い過ぎで、(a) 解析器の一般的な誤り＋規則の未定義」と注記した。R2-r2-5 と R3-r4-1 は、設計の観点が「§2.9 (c)/(g) の保守側の延長として O42 以降に限界記録する選択もありうる」と書いている。R2-r2-4（判定の左辺が name かどうか）と R2-r2-2（否定形）は別の単位だが、R3-r4-1 と R2-r1-6 の直し方の前提（P1）に当たる。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 検証役 10 意見の本文（verify_r1_r2_R2/R3/R4.json、verify_r4r5_R2R3R4R5.json）に「D3 / D4 だけなら low」の文言を使った形跡は無い（grep で "D3 / D4" は 0 件）。low の根拠は、どれも v2/v3 の出現数の測定か、verdict が変わらないこと。ただし R3-r1-4 の 2 つの観点は「主指標（D1+D2 の矛の組）と verdict は変わらず、D2 の宣言別件数だけが減る」を low の理由の一部にしている。これは D62 より前の枠組みで、D62 では宣言ごとの件数（D2 列。explore_d3d4 によると同じ原因で D4 列も）が主指標になった。旧文言そのものではないが同じ系統の理由なので、D62 の下ではこの部分を根拠にしない。出現 0 件の測定が残るので重大度は low のまま。
- **推奨の理由**: 直す推奨は R4-r1-7 だけ。代表の重大度が medium で、black 整形のありふれた書き方で起き、一般に正しい直し方（patchD：行にノードが無いときだけ単純文の範囲に落とす）がある。この直し方は既存の行の挙動も entry_lineno の値も変えないことを検証役が写しで確かめており、語彙の追加も要らない。R3-r4-1・R2-r2-5・R2-r1-6 は設計で反証されていないが、代表値が low で、v2/v3 の実測でも 0 件か、効果の無い 1 か所だけ。しかも素朴な直し方は誤 clear を作る（R3-r4-1 で 4 形、R2-r1-6 で 1 形）。安全な形（P0〜P4、(i)〜(iii)、左辺が name 仮引数）は §2.9 (b) の文面の改訂と逸脱の記録が要るので、限界として O42 以降に記録することを推奨する。3 件とも同じ関数 `_attribute_effects_to_tools` の中の話なので、直すならまとめて、敵対的レビューを通して入れるのがよい。R3-r1-4 は設計の観点で §2.9 (c) どおりと反証されたので、「低レベルハンドラの共通効果では D2 / D4 の宣言別件数が数えられない」を限界として記録する。D62 で宣言ごとの件数が主指標になったので、この限界は論文の結果の節で明示するのがよい。
- **所見**:
  - R4-r1-7: 代表。呼び出し式が文の先頭行より後から始まると、その行に CFG ノードが無く全ツール帰属に落ちる（FastMCP では cfg.exit）。medium・誤警報。直す推奨（patchD の形に限る。主案の「ヘッダ行に寄せる」は ce7 で新しい誤警報を作る）。（呼び出し式が文の先頭行より後の行から始まると entry_lineno に CFG ノードが無く、低レベル MCP ハンドラでは効果が join した全ツールに帰属して他ツールの宣言（readOnly）で矛になる（FastMCP では支配判）
  - R3-r4-1: 同じ関数の別の表れ。入れ子の name 判定を和で合成するので、内側の効果が外側の全ツールに帰属し、D1 誤警報と D2→D1 の列移動が起きる。代表値 low（medium/low/low）。素朴な積は誤 clear 4 形を作るので、直すなら P0〜P4 つき。記録を推奨。（低レベル MCP ハンドラで name 判定が入れ子（外側 `name in ("peek", "rm", "mk")` の中に内側 `if name == "rm"` / `elif name == "mk"`）のとき、`_attribu）
  - R2-r2-5: 同じ関数の別の表れ。`name == a or name == b` を短絡 CFG に分解すると単独で支配する test が無く、全ツール帰属になる（同値の `in` 形は正しい）。low・出現 0 件。直すなら (i)〜(iii) つき。記録を推奨。（`if name == "a" or name == "b":` の分岐は短絡 CFG で 2 つの test に分かれ、どちらも単独では効果を支配しないので join 済み全ツールに帰属し、readOnly の別ツールの D1 で矛にする）
  - R2-r1-6: 同じ関数の別の表れ。支配する名前が join されていないと「共通処理」扱いで全ツール帰属になる。low・v2 で 0 件。探索役の案は c6_shared_mode で誤 clear になるので、左辺が name 仮引数の条件が要る。記録を推奨。（支配する name 判定のツール名が join されていない（リテラル名が非リテラル・またはリテラル無し）と、その効果を「共通処理」として join 済み全ツールに帰属し、他ツールの readOnly で矛にする（§2.9 (b) と不一致）
  - R3-r1-4: 帰属の後段（meet_d_kind の explicit の和）で D2 / D4 の宣言別件数が落ちる数え落とし。設計の観点で §2.9 (c) どおりと反証済み（一般性は反証せず）。low・run20 で 0 件。限界として記録を推奨（直すなら §2.9 (c) の改訂と逸脱の記録が要る）。（低レベルハンドラの複数ツール帰属で `meet_d_kind` が explicit を和にするため、readOnly のツールが 1 つでも混ざると destructiveHint:false のツールの D2 が一度も評価されない（D2）

### U44 Tool リテラルの検出と join（別名の見落としと、木全体からの名前だけの join）（段階 C・重大度 中・推奨 一部直す）

ツールの宣言（Tool(...) の書き方の中にある readOnlyHint など）を探すとき、解析器は呼び出しの名前の最後が「Tool」かどうかだけを見ています。そのため `from mcp.types import Tool as MCPTool` のように別名で書かれた宣言は、まったく見つかりません。宣言が「無い」（⊥）ことになり、readOnlyHint=True なのにファイルを消すツールでも矛盾が出ない誤 clear になります。見つかった宣言は、どのサーバやモジュールのものかを見ずに、ツール名だけで木全体から結びつけます。このため、別のサーバやテストにある同じ名前の宣言がくっつく誤警報が起きます。同じ名前の宣言が 2 つあると、ファイル名の順で先に来た方を黙って採るので、自分の宣言を失う誤 clear も起きます。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `find_tool_literals` が Tool リテラルを書かれた名前の末尾成分 `Tool` で見つけ（import 表は `MCPTool` を `mcp.types.Tool` に解けるのに使わない）、ツール名だけで木全体から join する（リテラルがどのサーバ / モジュール / テストに属するかを見ない）ので、別名で作った宣言は見えず ⊥ になり、別サーバ・テストのリテラルは誤って付くか先勝ちで自分の宣言を奪う。
- **コードの場所**: authgap/entries.py:820-847 find_tool_literals, authgap/entries.py:874-877, 899-919 join, authgap/srcindex.py:300-312, 431-459 import 表
- **重大度の根拠**: 代表は R2-r3-4 です。探索役・設計・一般性の 3 意見がそろって medium でした。起きた木では宣言が丸ごと ⊥ になり、D_unknown にも「未 join」の件数にも出ません。そのため、その木の D1 / D2 は黙って 0 になります。D1 / D2 の判定に直接効くもので、D3 / D4 だけに効く話ではありません。

件数（件数だけに使う）: 探索役の見積もりでは、corpus（非 site-packages）に `as MCPTool` が 56 行、`as McpTool` が 3 行ありました。検証役の数えでは `as MCPTool` 59 行、`as McpTool` 3 行、その他 2 行の計 18 木です。多くは MCP クライアント側の構築です。run20 の D に効いていないことは探索役の自己申告で、検証役もそれに同意していますが、独自には測っていません。

R2-r1-5 は 3 意見とも low でした。理由は「v2 での該当 0（探索役の見積もりスクリプトによる。検証役は run20 の低レベルユニットが 5+1 であることを確かめた）」と「t21 は仕様どおり」の 2 つです。旧文言による格下げではありません。
- **直し方（一般に正しいか: 条件つきである）**: A. 別名の宣言の検出（R2-r3-4。直す）
find_tool_literals（entries.py:836-838）で、今の末尾名の一致に加えて、`resolve_call_name(node.func, index.module_scope(path))` が `mcp.types.Tool` / `mcp.Tool` に解ける名前も採ります。_read_annotations の `ToolAnnotations` も同じ手順で扱います。`_read_annotations` は SourceIndex を受け取らないので、呼び出し側から scope を渡す小さな署名変更が要ります。

検証役（一般性）の条件（必ず守る）:
(1) 直し方は additive（今の検出に足すだけ）に限ります。末尾名が Tool のものは今までどおり採ります。「import 表で木の中に解ける名前は捨てる」という strict 版にしてはいけません。反例 B6: pkg/models.py の `class Tool(mcp.types.Tool)` を `from .models import Tool` で使う木の中のラッパーでは、今出ている正しい D1 矛が消えて新しい誤 clear になります。所見の fix_sketch 後段の「木内の自前 Tool クラスを別名で使う形は採らない」は、B2（`from .models import Tool as MCPTool` は、直す前も後も ⊥）の意味に限って読みます。裸の Tool を落とす意味に読んではいけません。
(2) D61 の追記と同じ束縛回数の条件を付けます。その名前がモジュール直下で 2 回以上束縛されるなら、import 表で解きません。反例 B3: 別名を import した後に `class MCPTool(MCPTool)` で annotations を readOnlyHint=False に強制するラッパーでは、書かれた True が join されて誤警報になります。代償として B4（`try: from mcp.types import Tool as MCPTool / except ImportError: MCPTool = None`）は ⊥ のまま残りますが、件数の損失だけで、誤った主張は作りません。
(3) 別名の修正だけを入れると、B5 型の既存の誤警報が別名の分だけ広がります。B5 は、client.py にクライアント側の目録として `MCPTool(name="cl_search", readOnlyHint=True)` があり、server.py の宣言の無いツールに先勝ちで付くものです。そこで B の「食い違う同名の宣言は D_unknown」と同じ変更で入れます。
(4) `ToolAnnotations as TA` は unreadable（D_unknown）から読める形に変わるので、unknown → explicit の向きで新しい矛が出えます。取り直した run で増えた行を 1 件ずつ確かめます。
(5) 受け入れテストは srv_alias 型（低レベル）を使います。t83（デコレータ + モジュール水準のリテラル）は C の決定しだいで期待が変わるので避けます。回帰テストは t80 の srv_ctl / srv_modalias（今と変わらないこと）です。

B. 同じ名前の宣言が食い違うとき（R2-r1-5 の t26。直す）
`by_name.setdefault` の先勝ち（entries.py:907-911）をやめます。同じ名前のリテラルが複数あって annotations が一致しないときは、D_unknown（未 join として件数を出す）にします。設計・一般性の両観点が一般に正しいと認めています。仕様（Def 6）は候補が複数あるときを決めていないので、CLAUDE.md 規則 4 から導けます。

C. 学生の決定が要るもの（decisions.md に記録。仕様書本体は書き換えない）
- テストパスのリテラルを外すこと（t20）: 一般性の観点は §9.1 と同じ理由で一般に正しいとしています。設計の観点は、§9.1 / O30 が関数解決の規則であって Def 6 に無いので決定が要る、としています。
- 「同じモジュール → 同じパッケージ → 木全体」の優先順位: 設計の観点は新しい規則だとしています。一般性の観点は「同じモジュールを優先し、無ければ D_unknown」なら一般に正しいとしています。

避ける条件: デコレータユニットを同じモジュールのリテラルだけに制限してはいけません。反例 c5_registry: definitions.py の Tool リテラル、server.py の list_tools、handlers.py の自前 `@app.tool()` に分かれた構成で、今の正しい D1 矛が誤 clear になります。受け手が FastMCP(...) のインスタンスと確かめられるときに限れば安全です。

D. 限界として記録（t21）
別サーバの同名リテラルがデコレータユニットに付く問題です。サーバへの所属を推論しない限り c5 と区別できません。Def 6（AUTHGAP_BRIEF_v3.md:322「パッケージ内の全リテラル・名前の完全一致」）の字義どおりの挙動でもあります。

同根の別件（この単位の外）: t95a の `Server as LowLevelServer`（find_lowlevel_units、entries.py:689-690）にも同じ正規化が効きます。

手順: authgap/entries.py を変えるので implementation_sha256 が変わり、再凍結が要ります。直す前後の run を scripts/compare_scans.py と diff_effects.py で突き合わせます。A で増えた CONTRADICTION は敵対的レビューにかけます。
- **記録済みの限界・決定との重なり**: 仕様との重なり: t21（別サーバのリテラルがデコレータユニットに付く）は、Def 6 の join 規則（AUTHGAP_BRIEF_v3.md:322「パッケージ内の全 Tool(...) リテラル…ツール名文字列の完全一致」）を字義どおり読むと現状どおりです。設計の観点がそう判定しており、⊥ にするのは設計の変更です。

テストパスの除外と近さの優先順位は Def 6 に無い規則です。§9.1 / O30（contradiction_principles.md:269）は関数解決からテストを外す規則で、Tool リテラルは対象外です。O13（open_questions.md:258）は unit id の重複の話で、根本原因が違います。

別名の見落とし（R2-r3-4）については、末尾名に限ると決めた記録はありません。f0a_checks.md:1212 / :1218 は機構を記述しただけで、別名は検討していません。D28 の「Tool(...) リテラル 676」も同じ機構での測定です。この repo はむしろ別名の綴りで引くことを欠陥として扱ってきました。K7 を D61 G3 で直しています。

第 2 回の checked_but_ok（ToolAnnotations の別名 → D_unknown の件数損失）は annotations 側の話で、本件の Tool 側は ⊥ に混ざる点が違います。

review_plan §5 の既知の問題には該当しません。設計の観点で反証された所見はありません（両所見とも refuted=false）。ただし R2-r1-5 は設計の観点で expected_is_correct=false です（t21 の期待は仕様と食い違う、t26 の「srv_b だけ D1」は規則から導けない）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。両所見とも影響は D1+D2 です。R2-r1-5 の low は「v2 での該当 0」と「t21 は仕様どおり」によるもので、「D3 / D4 だけなら low」の旧文言を理由にしたものではありません。
- **推奨の理由**: 代表の R2-r3-4 は medium です。一般に正しい直し方（import の意味そのもので、additive に足し、束縛回数の条件を付ける）があり、凍結した語彙にも触れません（find_tool_literals は fingerprint の凍結ブロックの外）。設計の観点の反証も無いので、直す基準を満たします。

R2-r1-5 のうち、t26 の先勝ちを D_unknown にする部分は一般に正しいと両観点が認めています。別名の修正で B5 型の誤警報が広がるのを防ぐためにも、一緒に入れるべきです。

一方で、t20 のテストパス除外と近さの優先順位は Def 6 に無い規則なので、学生の決定が要ります。t21 は仕様の字義どおりで、c5 と区別できないため限界として記録するのが妥当です。単位の中に直すものと記録に回すものが混ざるので fix_partially を推奨します。
- **所見**:
  - R2-r3-4: 代表（直す）。別名 `Tool as MCPTool` の宣言が検出されずに ⊥ になる誤 clear。3 意見とも medium、fix_is_general=true。条件: additive に限る（strict は B6 を壊す）、モジュール直下で 2 回以上束縛される名前は解かない（B3）、R2-r1-5 の食い違い → D_unknown と一緒に入れる（B5）。（`Tool(...)` リテラルの検出が書かれた名前の末尾成分 `Tool` にしか当たらないため、`from mcp.types import Tool as MCPTool`（corpus に 45+ 行、自前の `Tool` クラスと）
  - R2-r1-5: 同じ原因（名前だけの木全体 join）の別の表れ。3 意見とも low。t26 の先勝ちは直す（食い違えば D_unknown）。t20 のテストパス除外と近さの優先順位は学生の決定。t21 は仕様どおりで、c5 反例のため限界として記録。デコレータユニットの同一モジュール限定は c5 反例で不可。（Tool(...) リテラルをツール名だけで木全体から join し、リテラルがどのサーバ / モジュール（テストを含む）に属するかを見ない: 別サーバ・テストの宣言が付く（誤警報）、同名の別サーバのリテラルに先勝ちで負けて自分の宣言を失う）

### U45 tools_list の要素の解決（import 表を使わない裸名引きと、裸名の already による遮蔽）（段階 C・重大度 中・推奨 直す）

`Agent(tools=[delete_file])` のようにツールの一覧に並べた関数を入口（ユニット）にするとき、解析器は Python の import のつながりを見ていません。関数の名前だけで木全体を探しています。そのため、別のファイルから import した関数は、tests/ や examples/ に同じ名前の関数が 1 つあるだけで「どれか決められない」として黙って落ちます（数え落とし）。逆に、木の外のライブラリから import した名前が、木の中にある無関係な同じ名前の関数に結び付けられて、偽の入口になることもあります（誤警報）。さらに、同じ名前の MCP ツールが木のどこかにあると、別のファイルにある同じ名前の関数まで一緒に除外されます（数え落とし）。向きは主にユニット数と危険な効果を持つユニット数（分母）の数え落としで、偽ユニットによる水増しも少しあります。

- **宣言**: tooling　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `find_tools_list_units` が要素の関数を import 表を使わず裸の末尾名で木全体から引く（別モジュールから import した関数は木のどこかに同名があると「一意でない」で落ち、外部から import した名前は木内の無関係な同名関数を入口にする）うえ、二重登録の除外 `already` を裸の関数名の集合にしているので別モジュールの同名関数までユニットにしない（同じ関数の二重登録は `registered` が既に防いでいる）。
- **コードの場所**: authgap/entries.py:484-549 find_tools_list_units, authgap/srcindex.py:249-264, 300-312 module_scope / resolve_import_module
- **重大度の根拠**: 代表は R2-r5-2 の medium（探索役・設計・一般性の 3 意見が中 / 中 / 低で、その中央値）。R2-r2-6 は低 / 低 / 低。設計の検証役が medium とした理由は 3 つ。(a) 「import した関数と、tests/ や examples/ にある同名の関数」という書き方は珍しくない（探索役の計数では 315 箇所 / 10 木 / 83 (木, 名前) で、上界）。(b) 数え落としと偽ユニットの両方の向きで、prereg §2.2 の分母 all_units / dangerous を系統的に動かす。(c) join_annotations（entries.py:899-925）は tool_name の完全一致で Tool リテラルの宣言を付けるので、偽ユニットが宣言 D を得て偽の矛になる可能性を構造的には排除できない。一般性の検証役が low とした根拠は評価の経路での実測。run20 の tools-list ユニットは 17/2,231 で、すべて D_kind が ⊥、矛盾行は 0。v2+v3 で救える落としは 1 件でこれも ⊥。R2-r2-6 の実測は v2 で差 0、v3 で 1 木 2 ユニット。最終評価の新しいデータで D1〜D4 の数字が動くかは未測定。旧文言「D3 / D4 だけなら low」で下がった重大度は無い。
- **直し方（一般に正しいか: 条件つきである）**: 一般に正しい直し方は「ツールの一覧に並べた名前を、参照している側のモジュールで見えている束縛（Python の名前解決）で解く。解けないとき、または曖昧なときだけ今の裸名ヒューリスティックに落とす」。2 つの所見は一緒に直す。

手順:
(1) `names` には末尾名だけでなく、(参照しているファイル, 要素の dotted 名, 囲む関数) を持たせる。
(2) 参照側モジュールで、先頭名の束縛（def / 代入 / import）を数える。2 つ以上ある、または関数の中で書き換えられる（`_scan_module_writes`）なら ambiguous として今のヒューリスティックに落とす。同じモジュールの def が import の後にあれば def が勝つ。
(3) 束縛が in-tree の import なら、解決先のモジュールで `lookup_function(last, module)` を引く。dotted 形（`fs_tools.delete_file`）は、`resolve_call_name` と同じく先頭を import 表で解いてから残りを結ぶ。
(4) `already` は裸名の集合をやめ、重複の除去は (module, qualname) の `registered` に任せる。

検証役が見つけた「素朴な直し方で壊れる反例」と、それを避ける条件（D61 G3 の条件を entries に持ち込む）:
- CE-a（R2-r2-6 の一般性の検証役）: `already` を消すだけだと壊れる。b.py が `from a import delete_file`（a.delete_file は @mcp.tool）を tools に並べ、同じファイルに無関係な入れ子関数 `make_cleanup.delete_file` があると、入れ子関数が偽ユニットになる。今は `already` のおかげで正しく 0 ユニット。対策は、`already` をやめるのは束縛による解決を入れた後にし、除外は `registered` だけで行うこと。
- CE1 `pkg/tools/__init__.py` の再公開（`from .fs import delete_file`）: 解決先のモジュールだけを厳密に引くと [] になり、今は正しい 1 ユニットが消える。対策は G3 規則 1 に従うこと。再公開するモジュールでその名前の束縛がちょうど 1 つで、それがモジュール直下の `from ... import` のときだけたどる。`import *` や遅延 `__getattr__` の表はたどらない。
- CE5 外部 import の後に同じモジュールの `def delete_file` で束縛し直す形: 「外部なので採らない」とすると誤って落とす。対策は (2) の束縛の数え上げと、def が勝つ規則。
- CE6 `from ..tools import delete_file`: import 表は相対の点を捨てるので、走査順で先にある根の `tools.py` に解いて [] になる。対策は、相対 import を `ImportFrom.level` で解くこと（import 表は使わない）。
- 実データ（v3-aslamkhan-github__lab の `from tools.send_email import send_email`。同名の def が 96 個ある）: `resolve_module_strict` の最初の接尾一致が別プロジェクトの複製に結ぶ。対策は、接尾一致する木内モジュールを全部集め、参照側と同じパッケージを優先し、それでも複数なら ambiguous として落とすこと。
- A9 の `from praisonaiagents.tools import write_file`: `resolve_import_module` がハイフン付きディレクトリを解けずに None を返す。これは「解決できない」であって「木外」ではない。対策は、「採らない（外部）」を、先頭のパッケージ名が木の中に無いと分かるときだけにすること。resolver の失敗（None）を「木外」と読まない。
- tools=[...] が関数の中にあり、import が関数ローカルのときは function_scope を使う。使わなくても今の挙動に落ちるだけで、退行にはならない。
- 文字列形 `tools=["f"]` は今のヒューリスティックのまま変えない。

残る限界: 遅延 `__getattr__` の表と束縛メソッド（A9 の `write_file = _file_tools.write_file`）は追わないので、今の偽ユニットが残る。これは限界として記録する（O41 か O42 以降）。

手順は review_plan §4.4 どおり。規則 → 反例テスト（t111 / t111b / t111c / t56、CE-a / CE1 / CE5 / CE6）→ 実装、の順にコミットする。解決率を上げる向きなので敵対的レビューを通す。run21 を取り、diff_effects（A9）/ two_sided / compare_scans で消えた行を確かめる。preregistration に逸脱として記録する。
- **記録済みの限界・決定との重なり**: 設計の観点では 2 件とも反証されていない（refuted=false）。
- D12 の限界（decisions.md:1386-1391）は、`tools=` キーワードを広く手がかりにするので登録でない呼び出しも拾う、という引き金の広さの話で、要素の解決とは根本原因が別。
- D17 改訂 4（decisions.md:1720）が防ぎたいのは同じ関数の 2 ユニットで、それは `registered` が担う。裸名の `already` は最初の実装（b3aa2c8）からある粗い除外で、意図された決定ではない。
- D17 の 186d406（「参照しているファイルの定義に絞る」）は、同じファイルの中の入れ子関数だけを想定していた。
- 同じ根本原因（末尾名で木全体を引く）は、val エンジン側では D17 改訂 3〜5・K7・D61 G3 で「欠陥」として import 表で直されており、tools_list だけを例外にした記録は無い。
- review_plan §5（O35〜O41、K1〜K7、設計上の決定）には無い。O41 の「組込み型の末尾名解決」は別の話。
- R2-r3-3（lowlevel_v2 の handler を裸名で引く）は別の関数・別の規則で、この単位の直し方では直らない（別の単位）。
- R2-r5-2 は第 5 回の所見（†）で、review_plan §7.3 のとおり事前登録の手続き（上限 4 回）の外にある。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R2-r2-6 の low（3 意見とも）は「D1/D2 に効かず、分母だけ。名前の衝突はまれ」が根拠。R2-r5-2 の一般性の検証役の low は「最終評価の経路（宣言あり MCP）で run20 の tools-list ユニットがすべて ⊥」という実測が根拠。どちらも「D3 / D4 だけなら low」という旧文言によるものではない。tools-list ユニットは D を持たないので、D3 / D4 にも同じく効かない。
- **推奨の理由**: 推奨の基準に当てはめると fix になる。代表の重大度が medium で、一般に正しい直し方があり（D61 G3 の条件つき）、語彙の追加が要らず、設計の観点でも反証されていない。直し方は D61 G3 で既に決めて敵対的レビューを通した条件を entries に持ち込むもので、新しい設計は要らない。R2-r2-6 は `already` を消すだけでは偽ユニットを作るので、同じ修正の中で一緒に直す。

ただし学生が判断するための注意が 2 つある。
1. 評価に近い実データでの効きは小さい。run20 の tools-list ユニットは 17 件ですべて ⊥、矛盾行は 0。v2+v3 で救える落としは 1 件と、v3 で 2 ユニット。
2. 解決率を上げる変更で、しかも `authgap/` を変える（指紋が変わる）。fix_sketch をそのまま当てると 3 つの反例と 1 つの実例で退行する。

凍結の危険を重く見るなら、限界として記録する（分母の数え落とし・偽ユニットとして O42 以降に書く）ことにも根拠はある。
- **所見**:
  - R2-r5-2: 代表（中 / 中 / 低 → medium）。要素を import 表を使わずに裸の末尾名で引くので、import した関数の落とし（t111 / t111c）と、木外の名前による偽ユニット（t111b）が起きる。第 5 回の所見（†）で、事前登録の手続きの外。fix_sketch はそのままでは CE1 / CE5 / CE6 と v3 の send_email の実例で退行するので、D61 G3 の条件が要る。（`tools_list` 規則の要素解決が import 表を使わず裸の末尾名で木全体を引く: 別モジュールから import した関数は、木のどこか（tests/ の stub、examples/ の同名関数）に同名の関数があるだけで「一）
  - R2-r2-6: 同じ原因の別の表れ（低 / 低 / 低）。裸名の `already` が、別モジュールの同名関数まで除外する（v3 の sidekick_loop で 2 ユニットを実測）。単独で `already` を消すと、CE-a（import した MCP ツールと、同名の入れ子関数）で偽ユニットができる。R2-r5-2 の束縛による解決と一緒に直す。（`find_tools_list_units` の `already`（裸の関数名の集合）が、別モジュールの同名関数まで除外する: `@mcp.tool() def delete_file` が木にあると `Agent(tools=[del）

### U47 _index_body の走査（ループ本体の定義の取りこぼしと、深い入れ子での木全体の落ち）（段階 C・重大度 中・推奨 直す）

解析器はまず木の中の関数定義を一覧（索引）にし、その一覧からツールを探します。この一覧作り（SourceIndex._index_body）には 2 つの欠陥があります。1 つ目: if / try / with の中の定義は拾うのに、for / while / match の中の定義は拾いません。そのためループの中で @mcp.tool を付けて定義したツールは、ツールとして数えられず、どこにも記録が残りません（数え落とし）。2 つ目: 入れ子を 1 段ずつ自分を呼び直して辿るので、約 1,000 段の入れ子（1,200 分岐の elif の連鎖など）を持つファイルが 1 つでもあると Python の再帰の上限で落ちます。この処理はユニット単位の打ち切り（D17 改訂 4）の外にあるので、その木は丸ごと analysis_failed になり、関係のない別ファイルのツールの D1 の矛も一緒に消えます（木の失敗そのものは summary に残ります）。

- **宣言**: D1 / D2 / D3 / D4　**向き**: 数え落とし　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `SourceIndex._index_body` が入れ子の定義を If / Try / With にだけ降りて For / While / Match の本体を索引せず（ループの中で定義したツールが消える）、その降下を入れ子 1 段ごとの再帰で行うので約 1,000 段の入れ子（長い elif 連鎖）を含むファイルが 1 つあると RecursionError で `index.build()` が落ち、ユニット単位の打ち切り（D17 改訂 4）の外なので木全体が analysis_failed になる。
- **コードの場所**: authgap/srcindex.py:182-216 _index_body, authgap/srcindex.py:174 _index_defs, authgap/runner.py:70-72 build の呼び出し
- **重大度の根拠**: 代表は R2-r1-9 で、設計の観点が medium としている。ユニットが丸ごと消え、parse 失敗や TRUNCATED のような印もどこにも出ない、黙った数え落とし（CLAUDE.md 規則 4、落とし穴「入れ子定義を落とさない」に直接反する）なので medium とする。実行と一般性の観点は low だが、理由は「まれ」（v2 では for 直下のデコレータ付きツール定義は 1 木 1 件 = v2-rahmanef63__cowork-kit-setup、探索役の実測）である。R5-r2-5 は 3 観点とも low（木の失敗は summary / progress に analysis_failed として記録され、population_v3.md の V1 で列挙されるので黙った消失ではなく、引き金は生成コードの巨大な分岐表くらいでまれ）。scan_v2_run20 と v3 の出力を grep して RecursionError の木は 0（本記述の作成時に確認）。v2 で実際にループ内ツールが矛を落としているか（件数）は未測定。どちらの所見も affects は D1+D2 で判定の種類によらず（ユニットごと消えるので D3 / D4 も同じく消える）、「D3 / D4 だけなら low」の旧文言で下がった重大度は無い。
- **直し方（一般に正しいか: 条件つきである）**: (1) ループ / match の本体に降りる: _index_body の降下先に ast.For / ast.AsyncFor / ast.While の body と orelse、ast.Match の各 case.body を、If / Try / With と同じ扱いで足す（R2-r1-9 の fix_sketch、一般性の観点も同意）。
【素朴な直し方で壊れる反例（本記述で確かめた、scratchpad/triage/U47/ce_shadow と drv.py）】_funcs は鍵 module:qualname の setdefault で「最初の定義が勝つ」ので、ループ本体を足しただけだと、実行されないループの中の同名定義（例: `for _ in (): def remove(...): return "never"`）がその後にあるモジュール直下の `@mcp.tool(annotations={"readOnlyHint": True}) def remove(path): os.remove(path)` を押しのける。今は mcp:remove のユニットが出て D1 の矛になるが、素朴に直すと _funcs は 7 行目のループ内の定義になり、ユニットが 0 件になった（新しい誤 clear）。【避ける条件】新たに索引するループ / match 本体の定義で、既に出るユニット（デコレータ付きの定義）が消えないこと。一般に正しい形は、同じ鍵の定義を 1 件に潰さず全部持ち、find_units がデコレータ付きの定義をすべてユニットにすること（登録はその def が実行されるたびに起きるので）。unit_id の衝突を避ける工夫が要るので M。最低限の形は、ループ / match 本体の定義は既にある鍵を上書きしない（直線の本体を先に索引し、ループ本体はその後に足す）こと。一般性の観点が見た呼び出し解決（_funcs_by_qual に候補が増えて曖昧 → 全候補に降りて opaque を合流）は効果を消さないが、経路依存の D2 の一部が矛 → 不に動きうる（実在する曖昧さの反映で誤 clear ではない）。
(2) 再帰の上限: _index_body を明示スタックの反復に書き換えるか、_index_defs をファイル単位で try/except RecursionError で包み、cap_hits に (rel, "recursion", 0) を残してそのファイルだけ除く（D17 改訂の _iter_nodes、改訂 4 と同じ方針）。【素朴な直し方で壊れる反例（一般性の観点、verify/R5_low_1/ce_order3）】順序を保たない LIFO のスタックにすると、`if sys.platform != "win32": @mcp.tool(...) def clean(): os.remove(...)  else: @mcp.tool(...) def clean(): return "unsupported"` で後の stub が setdefault で勝ち、正しい D1 の矛が消える。【避ける条件】今の前順（preorder）と同じ順で索引すること（body + orelse + finalbody と handlers を逆順に積む）。try/except 版は cap_hits への記録を必ず残すこと（部分的に索引した定義が残る点は扱いを決めて記録する）。探索役が挙げた find_units / find_tool_literals / build_trig_index の保護は、それらが ast.walk（反復）で辿るので要るかは未確認。
(3) 直した後: diff_effects.py で較正対の効果行、compare_scans.py で run20 との消えたユニット / 消えた CONTRADICTION を 1 件ずつ確かめる。ユニットと行が増える向きなので CLAUDE.md の敵対的レビューを通す。
範囲外（別の単位で扱う）: 一般性の観点が見つけた「if / else の両側で同名のツールを定義すると先の方しかユニットにならない（stub が先なら os.remove が解析されない誤 clear、verify/R5_low_1/ce_order2）」は同じ setdefault の first-wins が原因で、(1) の「全部持つ」形で一緒に解けるが、この単位の所見ではない。
- **記録済みの限界・決定との重なり**: 記録済みの限界・既知の問題（review_plan §5、K1〜K7、O 番号）とは重ならない。R5-r2-5 は D17 の改訂（再帰の NodeVisitor を明示スタックの _iter_nodes に直した）と改訂 4（ユニット単位で RecursionError を捕まえ TRUNCATED(recursion) を残す）と同じ方針の「直し漏れ」で、設計の観点は「決定は直す側で、限界として残す決定ではない」とした。R2-r1-9 はループ本体を除外する決定がどこにも無く、docstring と CLAUDE.md の「入れ子定義を落とさない」に反する。設計の観点で反証された所見は無し（2 件とも 3 観点を生き延びた）。関連するが別の所見: R5-r3-2（TRUNCATED(recursion) のユニットに D_kind が付かない。別の箇所で、この単位を直しても残る）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。2 件とも affects は D1+D2 で、重大度の理由は「まれ」と「木の失敗は記録される」であり、旧文言「D3 / D4 だけなら low」は使われていない。
- **推奨の理由**: 代表（R2-r1-9）は黙ってユニットが消える数え落としで medium。直し方は Python の言語の意味（ループ / match の中の def も実行時に登録される、再帰の上限）から決まり、v2 / v3 の個別の形に合わせたものではない（D61 の基準を満たす）。凍結した語彙の追加は要らない。設計の観点はどちらも「記録済みの限界・仕様どおり」とはしていない。ただし条件つき: (1) では同名の既存ユニットを押しのけないこと（本記述で素朴な版がユニットを 0 件にする誤 clear を作ることを確かめた）、(2) では索引の順序を保つこと。authgap/ を変えるので再凍結の前にまとめ、ユニットと行が増える向きなので敵対的レビューと compare_scans の突き合わせを通す。R5-r2-5 は単独なら low だが、同じ関数の同じ書き換えで直り、D17 の既存の方針の直し漏れなので一緒に直すのが自然。
- **所見**:
  - R2-r1-9: 代表。for / while / match の本体の定義を索引しないので、ループの中で定義したデコレータ付きツールが印もなく消える（重大度: 実行 low / 設計 medium / 一般性 low。v2 では 1 木 1 件）。直すときは、ループ内の同名定義が既存のツールを押しのけない条件が要る。（for / while ブロックの直下で定義したデコレータ付きツールを索引しない（入れ子定義の落とし。数え落とし））
  - R5-r2-5: 同じ関数（1 段ごとの再帰）の別の表れ。約 1,000 段の入れ子で index.build() が RecursionError になり、木全体が analysis_failed になる（3 観点とも low。木の失敗は summary に残る）。D17 の方針の直し漏れで、順序を保つ反復への書き換えで直る。（SourceIndex._index_body の再帰が If / Try / With の入れ子 1 段ごとに 1 フレーム使うため、約 1,000 段の入れ子（例: 1,200 分岐の elif 連鎖）を含むファイルが 1 つあると i）

### U48 SourceIndex の衝突と symlink（段階 C・重大度 中・推奨 一部直す）

解析器はまず木の中の .py ファイルを列挙し、「どのモジュールのどの関数か」の表を作ります。その表が、名前がぶつかったり、辿れない場所があったりしたときに、黙って 1 つに決めるか、黙って捨てています。3 つの書き方で起きます。(1) 同じファイルで if/else や try/except の両側に同じ名前のツールを定義すると、字面で先の方しか残りません。(2) 起動用の server.py の隣に同じ名前のパッケージ server/ があると、server/__init__.py のツールを server.py の import 表で読んでしまい、sp.run などが解決できずに効果が消えます。(3) シンボリックリンクのディレクトリの中は読まず、読まなかったことも記録しません。どれも痕跡を残さずツールや効果が消える向き（誤 clear / 数え落とし）の誤りで、矛盾を見逃します。

- **宣言**: D1 / D2 / D3 / D4 / tooling　**向き**: 誤 clear　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: SourceIndex の表とファイルの列挙が、衝突・除外を記録せずに 1 つに決める: 定義表 `_funcs` は (module, qualname) の鍵に `setdefault` するので同じモジュールの同名の 2 つ目の定義（if/else・try/except で分けたツール）を捨て、モジュール表 `_modname_to_path` は `X.py` とパッケージ `X/` が同じ名前になると先勝ちで X.py に固定して `X/__init__.py` のツールを X.py の import 表で解析し、`os.walk`（followlinks=False）は symlink のディレクトリを辿らず parse_failures / truncations にも残さない。
- **コードの場所**: authgap/srcindex.py:96-104 py_files（os.walk）, authgap/srcindex.py:148-160 build / _modname_to_path, authgap/srcindex.py:196, 218 _funcs.setdefault, authgap/analyze.py:199-203 ユニットの import 表
- **重大度の根拠**: 代表は R5-r1-2（探索役・設計・一般性の 3 意見とも medium）と R5-r1-5（medium / medium / low で中央値 medium）。起きるとツール 1 個が丸ごと消えるか（R5-r1-2。@overload のスタブが先にある形では 0 ユニットになる）、ツールの効果行が 1 本も出ず（R5-r1-5）、notes / parse_failures / truncations のどこにも痕跡が残らない。規則 4 の「黙って安全側に倒さない」にも反する。一方で頻度は低い。数えたものは次のとおり。R5-r1-2: v2 の 87 木で同一モジュール内の同名ツール定義が 14 件（2 木）あったが、どれも先の定義が本物。一般性の検証役が直した版を run20 の 87 木に当てても増えるユニットは 0。R5-r1-5: X.py と X/ が並ぶ配置は corpus 413 木中 10 木にあり、影で読まれる側に関数があるのは 3 木・13 関数、そのうちツールは 0。R5-r1-10: 413 木にディレクトリのリンクは 0（ファイルのリンクが 7）。R5-r1-5 の一般性の検証役は頻度を理由に low としたが、「起きたときの形を重く見るなら medium も妥当」と書いている。decls に D3 / D4 を入れたのは推論による。ユニットや効果が丸ごと消えれば 4 つの宣言すべての判定が消えるからで、再現で確かめたのは D1 だけ。向きは主に false_clean で、R5-r1-10 は count_loss（その中のツールの矛盾も見逃す）。旧文言「D3 / D4 だけなら low」による格下げは無い。
- **直し方（一般に正しいか: 条件つきである）**: 【R5-r1-2 同名定義】一般に正しい直し方: `_funcs` の鍵（module:qualname）と `lookup_function` は変えない。`SourceIndex.functions()`（srcindex.py:218）が `_funcs_by_qual` の全定義を返すようにする（id で重複を除き、(key, lineno) の順に並べる）。低レベル経路の `seen`（entries.py:655-660）の鍵にも lineno を入れる。同名定義があるユニットには `duplicate_definition:<lineno>` の注記を付ける。素朴な直し方で壊れる反例: 所見の fix_sketch を字面どおりに当て、`_funcs` の鍵に lineno を入れる。すると `lookup_function(qual, module)` の完全一致（srcindex.py:293）が必ず外れ、`_self_fields`（analyze.py:362-371。モジュールで絞らず先頭 1 件で break する）が別モジュールの同名クラスの `__init__` を採る。two_stores（a.Store は httpx、b.Store は sqlite3）で b.Store.query の DB 効果と contradiction:D1 が消え、新しい誤 clear になる。避ける条件: `_self_fields`、engine.py:1347 / 1471、`_closure_seed` は module つきの完全一致に依存しているので、鍵を変えない。`_closure_seed`（analyze.py:272-273 の `len(parents) != 1`）が opaque 側に倒れることも確かめる。検証役が測った結果（general 変種）: dup_ifelse は 1→2 ユニットになり、17 行目に FS_WRITE + D1 が出る。overload_stub は 0→1、redef_first_wins は 1→2。two_stores と helper_two_modules は今と同じ。run20 の 87 木で増えるユニットは 0。誤警報側の注意: 逐次の再定義でどちらが効くかは枠組みで変わる（mcp 1.x の add_tool は最初、jlowin/fastmcp 2.x は後）ので、静的には選べない。両方を注記つきで出す。スタブ側は効果の無いユニットとして分母に足される（判定行は増えない）。**R5-r1-3（評価道具の unit_id = framework:qualname:schema_hash にモジュール / relpath が無い）と対で直す。** そうしないと、増えたユニットが contradictions.json・runner.enforcement・prev.join で潰れて数に出ない。同一モジュール内で `__init__` が重複するとき先頭 1 件を返す点は残る（まれで、この所見の範囲の外）。
【R5-r1-5 X.py と X/ の衝突】一般に正しい直し方: ユニットと FuncDef の import 表は、dotted 名の表を経由せず、自分の relpath から作る（`join(src_root, x.relpath)`）。対象は analyze.py:199-203、val/engine.py:1051-1055、entries.py:948-951（と find_units の entries.py:376-379）、gate.py:636-639 の `resolve_module_path(x.module)`。import 文からの解決（resolve_import_module → `_modname_to_path`）は、Python の意味どおりパッケージを優先してよい。衝突は parse_failures 相当の行として残す。素朴な直し方で壊れる反例: 所見の案 (a)「`_modname_to_path` で `__init__.py` を優先する」だけを当てる。すると modclash_script（ツールが server.py 側にあり、隣にヘルパのパッケージ server/ がある）で、今は正しく出ている SPAWN + contradiction:D1 が消える。誤 clear が反対側のファイルに移るだけ。避ける条件: 表の優先順位ではなく、自分のファイルの relpath で引く。検証役が 413 木で測った結果、案 (b) は衝突の無いところで挙動が変わらない（違いは 3 木 13 関数で、ユニットは 0）。残る穴: 両ファイルが同名の関数を持つと、`_funcs` の鍵 module:qualname がやはり先勝ちで衝突する。鍵に relpath を含めるか、衝突を記録する。R5-r1-2 の条件（鍵を変えると `_self_fields` が壊れる）とぶつからないよう、鍵を変えずに衝突を記録するのが安全。
【R5-r1-10 symlink のディレクトリ】辿らない。walk の中で `os.path.islink(join(dirpath, d))` のディレクトリを `cap_hits` に `(rel, 'symlink_dir', 0)` として出すだけにする（truncations に出る）。素朴な直し方で壊れる反例は「辿る」変種（followlinks=True）。木の中を指すリンク（alias -> src/pkg）だと、同じ定義を src.pkg.tools と alias.tools の 2 つの名前で索引し、ユニットと矛盾を二重に数える。木の外を指すリンクだと、解析対象の外のコードが入る。ループ対策も要る。別件の非対称: ファイルのリンクは今も辿っていて、木の中を指すリンクで二重索引が起きている（corpus に 7 本。wealth のものはツールを含まないので実害 0）。これは直さず記録する。
【共通】行が増える向き（ユニットの追加、効果が解決される）なので、CLAUDE.md の敵対的レビューを通す。diff_effects.py で較正対を突き合わせ、compare_scans.py で run20 と比べ、消えた行が 0 であることを確かめる。notes の文字列と cap 名は凍結した語彙ではない。authgap/ を変えるので指紋が変わり、再凍結の前にまとめる必要がある。
- **記録済みの限界・決定との重なり**: 設計の観点では 3 件とも反証されていない（refuted=false）。記録済みの限界にも review_plan §5 にも無い。近い記録は次のとおり。D17 改訂 4（decisions.md:1715）は同じ `_funcs.setdefault` の「最初の 1 件に決め打ち」を false-clean として直したが、直したのは呼び出し先の解決（`_visible_defs` / `_pinned_function`）だけで、ユニット発見の側は同じ原因のまま残っている（R5-r1-2 はその取り残し）。D17 改訂 5（:1743, :1757）は「複数候補は決めずに全部出して opaque」で、直し方の原理と一致する。O13（open_questions.md:258-265）の「同名ツールの再定義」は unit id の重複の話で、原因が別。R5-r1-3（評価道具の unit_id にモジュール / relpath が無い）は別の単位だが、R5-r1-2 を直すなら対で直す必要がある。R5-r1-5 に近いものとして、decisions.md:1729-1730（相対 import の点を捨てることによる兄弟モジュールの衝突の限界）、:1704（末尾名検索での同名関数の衝突）、D19 K4 / K5（モジュール内の同名 def の決め打ち。K1〜K6 は未修正）があるが、どれも根本原因が違う。モジュール表は AUTHGAP_BRIEF_v3.md:1196 が前身の `_build_module_map` を「そのまま流用」と書くだけで、同名衝突を検討した跡は無い。symlink は docs のどこにも記録が無く、preregistration §2.3 の all_paths は「木の中の全 .py」と定めている。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 件とも影響は D1+D2 か評価の道具で、D3 / D4 を理由に下げた意見は無い。R5-r1-5 の一般性の検証役が low としたのは頻度（413 木中 3 木・ツール 0）が理由。R5-r1-10 の low も頻度（ディレクトリのリンク 0）が理由。
- **推奨の理由**: R5-r1-2 と R5-r1-5 は fix の基準をすべて満たす。代表の重大度が medium で、一般に正しい直し方がある（検証役の条件つき）。直し方は Python の意味（if/else の束縛、パッケージ優先の import）から導けて、v2 / v3 に合わせた閾値ではない（D61）。語彙の追加も要らず、設計の観点でも反証されていない。R5-r1-10 は low で、413 木にディレクトリのリンクが 0 件のまれな書き方なので、基準どおりなら限界として記録する側になる。ただしこの件の直し方は「辿らずに cap_hits に 1 行出す」だけで、壊すものが無い。同じ srcindex.py を触るので、学生の判断で同じコミットに入れてもよい。ファイルのリンクとディレクトリのリンクを違う扱いにしている点は、別件の限界として open_questions に記録する。R5-r1-2 は R5-r1-3（unit_id の衝突）と対で直さないと、増えたユニットが評価の道具で潰れる。行が増える向きなので、敵対的レビューを通すこと。
- **所見**:
  - R5-r1-2: 代表（直す）。同じモジュールの if/else・try/except・@overload で同名のツールを定義すると、_funcs.setdefault で 2 つ目以降が消える。3 観点とも medium・false_clean。直し方は functions() が全定義を返すことで、鍵は変えない（鍵に lineno を入れると two_stores で新しい誤 clear が出る）。R5-r1-3 と対で直す。（同じモジュールに同名の関数定義が 2 つあると（if/else・try/except の分岐で別々に定義するツール）、2 つ目の定義が SourceIndex._funcs.setdefault で黙って捨てられ、ユニットにも記録にも残らな）
  - R5-r1-5: 同じ原因（名前の衝突を 1 つに決める）の別の表れ（直す）。X.py と X/__init__.py が同じ dotted 名になり、パッケージ側のツールを X.py の import 表で読む。medium / medium / low。直し方は自分の relpath から import 表を作ることで、パッケージ優先だけの直しは modclash_script で誤 clear を移すだけになる。（起動スクリプト X.py とパッケージ X/ が同じディレクトリにあると、SourceIndex のモジュール表が X → X.py に固定され、X/__init__.py のツールが X.py の import 表で解析されて sink ）
  - R5-r1-10: 同じ原因（列挙が除外したものを記録しない）の別の表れ。low で、corpus に 0 件。基準では限界として記録する側だが、直し方は辿らずに cap_hits に symlink_dir 行を出すだけで、安全かつ安価。辿る変種は二重索引になるので採らない。ファイルのリンクとの非対称は別件として記録する。（シンボリックリンクのディレクトリは os.walk（followlinks=False）で辿られず、その中のツールはユニットにも parse_failures / truncations にも残らない）

### U49 打ち切り・落としたファイルの痕跡がユニット水準に残らない（段階 A・重大度 中・推奨 直す）

解析器が途中でやめたものや読めなかったものは、木全体・ファイル単位でしか記録されず、ユニット（ツール 1 つ）の manifest には残りません。このため 3 つのことが起きます。(1) 時間切れで解析しなかったツールは、manifest の打ち切り欄に何も書かれません。(2) 深い式で再帰の上限に当たったツールは、宣言（readOnlyHint など）まで無いものとして扱われます。(3) 構文エラーのファイルや大きすぎるファイル（2 万ノードを超えて切られたもの）にある関数を呼ぶツールは、効果が 1 つも出ず、外部ライブラリを呼んだときと同じ「unresolved」の印しか付きません。いちばん重い (3) は、本当は矛盾する宣言が矛盾なし（宣言の範囲内）に見える向き（誤 clear）です。(1)(2) は評価の道具がツールを黙って数え落とす向きです。

- **宣言**: D1 / D2 / tooling　**向き**: 混在　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 打ち切りや取りこぼしの記録がファイル水準・run 水準にしか無く、manifest のユニット水準に残らない: 木の時間上限（max_tree_seconds）で解析しなかったユニットは truncations に入らず（probe では cap 名も wall_clock と誤記）、RecursionError で打ち切ったユニットの代替 UnitReport には D_kind が無いので宣言が ⊥ に見え、parse 失敗 / AST_NODE_CAP で落とした木内モジュールを呼ぶツールは外部呼び出しと同じ `opaque_reasons: unresolved` だけで宣言 D1/D2 に対して黙って「内」に見える。
- **コードの場所**: authgap/runner.py:116-151 時間上限 / RecursionError の代替 report, authgap/report.py:206, 234, 269 manifest の truncations / D_kind, authgap/analyze.py:198-221 analyze_unit_f0a, authgap/val/engine.py:1227, 1288-1294 AST の無い木内モジュールへの解決
- **重大度の根拠**: 代表は R5-r2-2 で、探索役・設計・一般性の 3 意見がそろって medium、向きは誤 clear。起きるのは依存先のファイルが parse 失敗か AST_NODE_CAP で落ちたときに限るが、そういう木では系統的に起きる。run20 の実測は次のとおり。探索役: 落としたファイルを import するファイルにあるユニット 794（6 木）、そのうち効果 0 が 116、D1/D2 を明示するもの 39。一般性の検証役（dropped_deps.py）: 落としたファイルを持つ木 18（parse 失敗 86 ファイル・cap 136）、落とした木内モジュールを import するユニット 133、そのうち効果 0 が 88、D1/D2 明示 39（37 が sheetforge-mcp。78 ツールすべてが効果 0・行 0）。ツール本体が落としたモジュールを直接呼ぶユニットは 395（効果 0 が 90、D1/D2 明示 15。深さ 1 以上を経る分は含まないので下限）。sheetforge の 37 件が本当に矛盾になるかは確かめていない。R5-r1-6 と R5-r3-2 は 3 意見とも low で、影響は評価の道具に限る。run20 では、ユニットの走査の途中で時間切れになった木は 0、TRUNCATED(recursion) のユニットは 2,231 中 0。ただし道具は最終評価の経路にある（V3 の見落とし抜き取りの枠、probe の n_units_with_D_kind、木ごとの manifest）。D3/D4 への効きは未測定。落としたファイルにある NET 効果は openWorldHint にも同じ形で効くはずだが、数えていない。
- **直し方（一般に正しいか: 条件つきである）**: どれも「印・記録を足すだけ」で、判定（rows / verdict）と effects は変えない。3 件とも一般性の検証役は、正しい判定が壊れる反例を作れなかった。
(A) R5-r2-2（代表）: engine の木内解決（val/engine.py:1227 付近、1288-1294 付近）で、import 表が木内モジュールに解決したのに、そのファイルの AST が None（index.parse_failures か cap_hits にある）とき、ユニットに印を残す。形は unresolved_in_tree_calls に理由（parse_failure / ast_node_cap）と relpath を付けた項を足すか、unit notes に `depends_on_dropped:<relpath>` を付ける。scan_v2.py の summary にも、落としたファイルに依存するユニット数と、木ごとの parse_failures / truncations の件数を出す。V3 の見落とし抜き取りでは、この印を持つユニットを別の列に分ける。
守ること:
- 凍結語彙 VAL_OPAQUE_REASONS は動かさない。既存の `cap`（§5.2 の summary_cap 用）を流用しない。
- 効果の無い行を作って「不」に数えるのは別の決定で、この単位には入れない。§7 は効果の無い行を作らない。
- unresolved_in_tree_calls の形を変えるなら、docs/manifest.schema.json の版を上げる。
- cap（2 万ノード）は指紋の一部なので変えない。
反例（印が余計に付く向き。保守的）: 木の中の落としたファイル（例 tests/big.py）と同じ名前の外部パッケージを `import big` すると、resolve_import_module の厳密解決（D17 改訂 2）が木内側に解いて印が付く。判定は変わらず、V3 の抜き取りから外しすぎる側に働く。既存の規則を引き継ぐ形として受け入れ、限界として記す。
(B) R5-r3-2: RecursionError を捕まえた後の代替 report（runner.py:139-143）に `d_kind=parse_d_kind(unit)` と `d_kind_by_tool=parse_d_kind_by_tool(unit)` を入れる。
守ること:
- except の中のこの 2 つの呼び出しは、自分の try/except RecursionError で包む。失敗したら ⊥ に戻し、notes に印を残す。ハンドラの中で 2 度目の例外が出ると、木全体が落ちるため。
- analyze_unit_f0a で設定を engine.analyze より前に動かすだけでは足りない。例外で report が返らないため。
- 設定を関数の冒頭に動かすと、'module unresolved' の早期 return（analyze.py:201）で ⊥ になる同じ原因も直る。
- v3_miss_sample.py の出力に notes（TRUNCATED）を載せ、判定者が「不明（打ち切り）」に分けられるようにする。
(C) R5-r1-6: manifest_json（report.py:269）の truncations に、ユニットの走査の途中で時間切れになった分を足す。cap は tree_budget、count は tree_budget_skipped で、前処理側の tree_budget_prep（D52）と同じ形にする。probe_json（report.py:234）の cap の名前は、`TRUNCATED(<cap>)` の接頭から決める。
守ること: runner.py:146 は WALL_CLOCK_CAP 超えのユニットを接頭無しの unit_id のまま入れている。接頭が無いものは wall_clock に戻す。
検証役の確認: compare_scans / intersection_rows / contradiction_by_decl は truncations を読まない。時間切れに当たる木はもともとユニット集合が非決定的なので、記録を足しても新しい非決定性は生まれない。
共通:
- authgap/ を変えるので指紋が変わる。§4.4 の再凍結の前にまとめて入れる。
- diff_effects / compare_scans で、消えた効果行と CONTRADICTION が 0 であることを確かめる。
- **記録済みの限界・決定との重なり**: 3 件とも設計の観点で反証されていない（refuted=false）。近い記録と、それとの違いは次のとおり。
- D61 G5（decisions.md。改訂で「G5 は変えない」）: 解決できなかった木内の呼び出しを、判定を変えずに数える列を作った。ただし対象は索引にある定義に限る。落としたファイルの定義は索引されない（srcindex.py:174-177）ので取りこぼしていた。R5-r2-2 はこの穴を塞ぐもので、G5 と同じ形（印だけ）。
- population_v3.md:95-98 の「未解決の呼び出しは一律に不明にはできない」は、未解決一般の話。落としたファイルへの依存はそれより狭い部分集合で、実行時には確実に動くコードなので、別扱いにできる（設計の検証役）。
- O21（open_questions.md:425-446）: cap で切られたファイルの中にあるツールを分母でどう扱うかの話で、原因が違う。
- 仕様（AUTHGAP_BRIEF_v3.md:476, 640）はファイル水準の parse_failure / TRUNCATED 行を要求していて、それは満たしている。ユニット水準の記録は CLAUDE.md 規則 4 の趣旨と G5 の形から導かれる。
- D17 改訂 4: RecursionError を TRUNCATED(recursion) として数えると決めただけで、宣言を落とすことは決めていない。
- D52: 前処理で打ち切った場合は truncations に記録すると決めている。途中で打ち切った場合との扱いの違いは、意図したものではない。
- D34: run ごとに報告するという約束は、summary.json の budget_skipped で満たされている。
review_plan §5 の既知の問題には入っていない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 形跡なし。3 件とも影響は D1+D2 か評価の道具で、D3/D4 だけに効く所見ではない。検証役の理由も「D3/D4 だけ」を根拠にしていない。R5-r1-6 と R5-r3-2 の low は、「run 全体の件数は summary.json に残る」「run20 で 0 件」「まれな書き方」を根拠にしている。
- **推奨の理由**: 代表の R5-r2-2 は、3 意見とも medium の誤 clear です。直し方は一般に正しく（印だけで判定を変えない。条件は上のとおり）、凍結語彙の追加も要らず、設計の観点で反証されていません。R5-r1-6 と R5-r3-2 は low ですが、同じ根本原因（ユニット水準に記録が残らない）で、どちらも記録を足すだけです。最終評価の経路（V3 の見落とし抜き取りの枠、probe の分子、木ごとの manifest）で黙った数え落としを防ぎます。どれも authgap/ に触れますが、§4.4 の再凍結の前にまとめれば追加の費用は小さいので、単位ごと直すことを勧めます。学生が範囲を絞るなら、R5-r1-6 は run 全体の件数が summary.json に残るので、限界として記録に回す第 1 候補です。
- **所見**:
  - R5-r2-2: 代表（medium、誤 clear、D1/D2）。落としたファイル（parse 失敗 / AST_NODE_CAP）にある定義を呼ぶツールが「unresolved」だけになり、宣言の範囲内と区別できない。G5 の穴を塞ぐ印を足す。印が余計に付く反例（同名の外部パッケージ）は保守的な向きなので受け入れる。（parse に失敗した / AST_NODE_CAP で落とした木内モジュールの関数を呼ぶツールは効果も行も出ず、unit 水準の印は外部呼び出しと同じ `opaque_reasons: unresolved` だけなので、宣言 D1/D2）
  - R5-r3-2: 同じ原因の別の表れ（low、数え落とし、道具）。RecursionError の代替 report と 'module unresolved' の早期 return で D_kind が ⊥ になり、V3 の抜き取り枠と n_units_with_D_kind から消える。ハンドラの中の parse_d_kind を try/except で包むのが条件。run20 では 0 件。（RecursionError で打ち切ったユニットは runner の代替 UnitReport に D_kind が無く（analyze_unit_f0a も parse_d_kind を engine.analyze の後に呼ぶ）、宣言）
  - R5-r1-6: 同じ原因の別の表れ（low、数え落とし、道具）。走査の途中の時間切れが manifest の truncations に出ず、probe では cap の名前が wall_clock に誤記される。run 全体の件数は summary.json に残る。run20 では途中の時間切れは 0 件。範囲を絞るなら記録に回す第 1 候補。（木の時間上限（max_tree_seconds）に途中で当たって解析しなかったユニットは manifest に痕跡が無く（truncations: []）、evidence の manifest だけを読む道具（intersection_r）

### U50 評価スクリプトの鍵の作り方（同一性の鍵に区別に要る成分が無い / 処理系に依存する）（段階 A・重大度 中・推奨 一部直す）

評価スクリプトは「同じツールの同じ矛盾か」を鍵で見分けます。その鍵に、区別に要る情報が入っていません。(1) ファイル（モジュール）の場所が無いので、別ファイルにある同じ名前のツールの矛盾が 1 件に潰れます。(2) compare_scans の「消えた矛盾」の鍵にどの宣言（D1〜D4）への矛盾かが入っていないので、同じ場所に別の宣言の矛盾が残っていると、消えた矛盾が見えません。(3) two_sided の経路の鍵に入口のツール名が無いので、同じヘルパを呼ぶ兄弟ツールが 1 本の経路に潰れます。どれも件数を少なく数える向き（数え落とし）で、回帰検査が「消えた 0」と黙って通ってしまいます。(4) これとは別に、unit_id は既定値の書き方を文字列にした値から作るので、Python 3.10 と 3.12 で値が変わることがあります（非決定性）。

- **宣言**: tooling / D1 / D2 / D3 / D4　**向き**: 混在　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: 評価の道具が使う同一性の鍵が、区別に要る成分を含まないか処理系に依存する: ユニットの鍵にモジュール / relpath が無い（scan_v2 の unit_id = framework:qualname:schema_hash、contradiction_by_decl / compare_scans / intersection_rows の (木, qualname, site, kind)）ので別モジュールの同名ツールの矛が 1 件に潰れ、compare_scans の「消えた CONTRADICTION」の鍵に宣言が無いので同じ位置に D3/D4 の矛が残れば消えた D1/D2 の矛が見えず、two_sided.py の経路の鍵に入口ツール名が無いので同じヘルパを通る兄弟ツールが 1 経路に潰れ、unit_id の schema_hash は既定値を `ast.unparse` した文字列なので Python 3.10 と 3.12 で変わる。
- **コードの場所**: scripts/scan_v2.py:44 _contradiction_rows の鍵, scripts/contradiction_by_decl.py:46 load_reasons, scripts/compare_scans.py:68-69, 109-116, scripts/intersection_rows.py:80, scripts/two_sided.py:134, 188, 439 collect の経路の鍵, authgap/entries.py:96-108, 213-229 schema_hash / unit_id, scripts/lost_units.py:40
- **重大度の根拠**: 代表は R5-r1-3 で、探索役・設計・一般性の 3 意見とも medium。scan_v2 の contradictions.json（手検証の候補表）、contradiction_by_decl（宣言ごとの矛の件数 = 主指標）、compare_scans（§4.4 の run21 の回帰検査）は、どれも最終評価と再凍結の経路にある。run20 で実際に潰れた組は 0 件（検証役が数えた。CONTRADICTION の鍵は (木,qualname,site,kind) でも (木,unit_id,site,kind) でも relpath+lineno 込みでも 191。D1 109 / D2 44 / D3 39、§3 の交差行 1 はどの鍵でも同じ）なので、公表値は動かない。一方、同じ (木, qualname) が複数の relpath に現れる組は 12（3 木。mcparmory の servers/<x>/server.py はそれぞれ別のツール）、unit_id の衝突は 3（2 木）あり、登録簿型の repo では普通に起きる形なので、新しいデータで数が静かに変わりうる（review_plan §1 (c) の形）。他の所見: R5-r3-3 は low（3 意見とも。run20 で宣言が 2 つ以上ある鍵は 191 中 1 件、contradiction_by_decl を前後で見比べれば件数の差は見える）。R5-r2-1 は low が代表（medium / low / low。D36 で two_sided は主軸から外れ、D60 の最終評価にも使わない）。R5-r3-4 は low（3 意見とも。最終評価の run は 1 つの処理系で閉じる）。D62 の後では、R5-r3-3 の隠れは D1/D2 だけでなく、どの宣言の消失も別の宣言の残りで隠れる向きに広がる。重大度は上げていない。
- **直し方（一般に正しいか: 条件つきである）**: すべて scripts/ の中で直せる（R5-r3-4 は (a) の道をとる場合）。
【R5-r1-3】scan_v2._contradiction_rows の鍵を (unit_id, relpath, lineno, site, kind) に、contradiction_by_decl.load_reasons・compare_scans.load の contradictions・intersection_rows:80 の鍵を (木, relpath, lineno, qualname, site, kind[/slot]) に揃える。compare_scans はユニットの鍵にはすでに relpath:lineno を混ぜているので、それに合わせる。守ること:
- 1 つのユニットの中で (site, kind) / (site, slot) を畳む設計（O18 対策）は変えない。
- corpus は SHA で pin しているので、同じ corpus の run どうしなら lineno を入れても鍵はずれない。ただしリリースをまたぐ突き合わせ（r_prev / prev.join）では lineno の無い鍵が要る。runner.enforcement[unit_id] と prev.join は O13 の範囲なので、ここでは触らない。
- 検証役が探した「直すと壊れる」候補は同梱コピーだった（run20 の prebid の examples/ 2 ファイル、synalinks の guide と template。後者は unit_id も衝突）。直すとこれが 2 件に数えられる。ただし n_units・verdict_rows・compare_scans のユニットの鍵はすでに 2 件で数えている。いまは名前が衝突して偶然 1 件に潰れているだけなので、壊れたとは言えない。コピーを 1 件に数えたいなら、名前の衝突に頼らず明示の規則（内容ハッシュ、examples/ の除外など）にする。
- 単位の定義が変わるので、preregistration に逸脱として書く。run20 で再生成し、191 / 109 / 44 / 39 / 交差行 1 が変わらないことを確かめる。
- R5-r1-2（同じモジュールの同名定義）を直すなら、この直しが先に要る。
【R5-r3-3】compare_scans の contradictions の集合の要素に宣言を足し、(木, relpath, lineno, qualname, site, kind, 宣言) にする。宣言は行の注記 contradiction:<宣言> から取る。「消えた」「増えた」は宣言ごと（D62 で D1〜D4 は 4 つとも主指標）に分けて出す。守ること:
- contradiction:<宣言> の注記が無い CONTRADICTION 行には仮の宣言 '?' を付け、集合から落とさない（run20 では 0 件だが、将来に備える）。
- 宣言を足した鍵はいまの鍵を細かくしただけなので、いま見えている消失はすべてそのまま見える。検証役も反例を作れなかった。D1→D2 の移動は「消えた + 増えた」として出るが、これは正しい情報。
- 影響をいちばん小さくしたいなら、いまの鍵は残し、宣言ごとの集合差の表を別に足す形でもよい。
【R5-r2-1】探索役の案「collect の chain を常に (qualname,)+witness_chain にする」は一般には正しくない。検証役の反例（scratchpad/verify/R5_hm_2/rename_pair）: 修正でツール名も変わる対（vuln の save → fixed の save_note。検証はツール側に入り、ヘルパ write_note は共通）では、いまの鍵なら pass_any_change=True だが、案を当てると only_vuln=['save->write_note'] / only_fixed=['save_note->write_note'] で pass_any_change=False になる（新しい数え落とし）。避ける直し方は 2 つ:
- 2 段で照合する。まず入口つきの鍵で両側を合わせ、片側にしか無い経路は入口を外した鍵（いまの鍵）で合わせ直してから、only_vuln / only_fixed に落とす。
- 入口の同一性に manifest の tool_name を使う（name= があれば関数名の変更に耐える）。
expected_tuples.json の path 条件は部分文字列一致なので、接頭辞を付けても当たる。直したら 8 対で 3 列 7/8 ｜ 7/8 ｜ 8/8、verdict-clearing 厳密 0/8 / INJECT 1/8 が変わらないことを確かめる。
【R5-r3-4】探索役の案はどちらも一般には正しくない（一般性の検証役の反例）:
- ast.dump(annotate_fields=False) は 3.13 で出力が変わる（lambda: 0 が 'Lambda(arguments(), Constant(0))' になる）。
- 定数でない既定値を '<expr>' に潰すと、別モジュールの同名ツールの unit_id が同じになり、scan_v2._contradiction_rows が正しい 2 行を 1 行に畳む（新しい数え落とし。R5-r1-3 を直せば contradictions.json 側は防げるが、unit_id を鍵にする lost_units / r_prev は防げない）。
一般に正しい道は 2 つ:
- (a) unit_id は変えない。scan_v2 の summary に処理系の版を記録する（いまは freeze_analyzer の fingerprint にしか無い）。unit_id で突き合わせる道具（compare_scans:52 のユニットの鍵、lost_units:40、r_prev）は、版が違えば止めるか警告する。「処理系をまたいで unit_id を突き合わせない」を docs に書く。scripts/ だけで直り、凍結の中身は変わらない。
- (b) ast.dump / ast.unparse を使わず、ノードの型と固定したフィールドの一覧をたどる自前の直列化器で hash を作る。authgap/entries.py が変わるので指紋も全 unit_id も変わる。やるなら凍結前に 1 回だけ。
1 つの処理系で閉じる最終評価には (a) で足りる。なお探索役の「compare_scans は影響なし」は誤りで、ユニットの鍵に unit_id を含むので、処理系を変えるとユニットが「消えた」ように出る。
- **記録済みの限界・決定との重なり**: O13（unit id が木の中で一意でない）は同じ根本原因を r_prev / drift（付録）についてだけ記録している。主指標の件数（contradictions.json、contradiction_by_decl）と回帰検査（compare_scans の「消えた CONTRADICTION」）への影響はその影響欄に無い、と設計・一般性の両検証役が判定した。D19 の記録（decisions.md:1577-1582）は「unit_id 単独で突き合わせる新しいスクリプトでは relpath と行を鍵に含める」と書いており、R5-r1-3 は記録した意図と実装の食い違いにあたる。D17「直さない 2」（複製サーバが同じ id になるのは定義どおり）は unit id の定義の決定で、集計の鍵の決定ではない。R5-r2-1 の道具は D36 #4 で主軸から降ろした判別実験（付録）の道具だが、所見は降ろした決定ではなく道具の docstring（two_sided.py:32-47「入口からの経路」）と実装の食い違いを指している。R5-r3-4 は D16（3.12 への切り替え）が unit_id の処理系依存を記録していない所に当たる。4 件とも設計の観点で反証されていない（refuted=false）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R5-r3-3 の設計の検証役は「D3/D4 だけに効く所見ではなく、D1/D2 の回帰を D3/D4 が覆い隠す向き」と書いており、low の理由は contradiction_by_decl で件数の差が見えることと、run20 の該当が 1 件であること。R5-r2-1 の low の理由は D36 で降ろした道具であること。R5-r3-4 の設計の検証役の「記録のみでよい水準（D1/D2 には効かない）」は D62 前の枠組みの言い方だが、所見は処理系をまたぐ非決定性で、D3/D4 だけに効くものではない。low の理由は最終評価の run が 1 つの処理系で閉じることなので、旧文言で下がったとは見なさない。D62 の後は R5-r3-3 の隠れが D1〜D4 のどの宣言にも及ぶので、影響の範囲は広がる。ただし件数（run20 で 1 件）は変わらないので、重大度は動かしていない。
- **推奨の理由**: R5-r1-3（medium）と R5-r3-3（low）は、最終評価と再凍結（§4.4 の run21 の突き合わせ）の経路にある道具の数え落としである。直し方は scripts/ だけで済み、凍結の指紋に触れず、一般に正しい（鍵を細かくするだけで、いま見えているものは消えない）。だから直すことを推奨する。R5-r3-4 は unit_id そのものを変える直し（authgap/entries.py）は勧めない。scripts/ だけで済む (a)（summary に処理系の版を記録し、unit_id で突き合わせる道具で版の違いを止めるか警告し、docs に限界として書く）を入れ、処理系への依存は限界として記録することを推奨する。R5-r2-1 は D36 で降ろした付録の道具で、D60 の最終評価には使わない。探索役の素朴な直し方には反例がある（ツール名が変わる対で新しい数え落としが出る）。そのため限界として記録するのを基本とし、学生が望むなら 2 段照合の形で入れる（scripts/ だけ、8 対の値が不変であることを確かめる）。
- **所見**:
  - R5-r1-3: 代表（medium、3 意見とも medium）。scan_v2 / contradiction_by_decl / compare_scans / intersection_rows の鍵に relpath が無く、別モジュールの同名ツールの矛が 1 件に潰れる。直す: 鍵に relpath+lineno を足す。run20 の数は不変（191 / 109 / 44）を確かめる（評価道具のユニット同一性の鍵にモジュール / relpath が無いため、別モジュールの同名ツール（同じ関数名）の D1/D2 の矛が 1 件に潰れる: contradictions.json の n（scan_v2 は unit_id =）
  - R5-r3-3: 同じ原因の別の表れ（鍵に宣言が無い）。compare_scans の「消えた CONTRADICTION」が、同じ鍵に別の宣言の矛が残ると消失を隠す。low だが §4.4 の回帰検査の経路にある。直す: 鍵に宣言を足し、注記の無い行は '?' にする（compare_scans.py の「消えた CONTRADICTION」は宣言を区別しない集合差なので、同じ (木, ユニット, site, kind) に D3/D4 の矛が残っていれば D1/D2 の矛が消えても（主指標 153 が減）
  - R5-r2-1: 同じ原因の別の表れ（two_sided の経路の鍵に入口ツール名が無い）。low、D36 で降ろした付録の道具で最終評価の経路に無い。素朴な接頭辞はツール名が変わる対で反例あり。限界として記録。入れるなら 2 段照合（two_sided.py の経路の鍵に入口ツール名が無い（witness_chain は被呼び出しの列だけ）ため、同じヘルパを通る兄弟ツールが 1 経路に潰れて最弱が残り、片方のツールにだけ入った修正（等級 / req_val の変化）が両）
  - R5-r3-4: 同じ単位の別の原因（鍵が処理系に依存する。unit_id の schema_hash が ast.unparse の出力に依存）。low、非決定性。探索役の 2 案はどちらも反例あり。scripts/ だけの (a)（版の記録と、版が違うときの停止・警告）を入れ、限界として記録。unit_id の定義は変えない（unit_id（schema_hash）は仮引数の既定値を ast.unparse した文字列から作るため、既定値が lambda や入れ子引用符の f-string のツールでは Python 3.10 と 3.12 で unit_id ）

### U51 contradictions.json（手検証の候補表）の行の位置と destructive が、同じ組の別の行・別の効果から取られる（段階 A・重大度 中・推奨 直す）

scripts/scan_v2.py は、矛（宣言に反する効果）の行を「ユニット × (site, kind)」ごとに 1 行へまとめて、手検証の候補表 contradictions.json に書き出します。このまとめ方には欠陥が 2 つあります。1 つ目は位置です。ファイル名は最初の行から取るのに、行番号は別ファイルの行も含めた最小値を取ります。そのためファイル名と行番号の組み合わせが、実在しない位置（import 文や docstring など）を指すことがあります。2 つ目は destructive 列です。この列はその行の効果ではなく、同じ (site, kind) で最初に見つかった効果から取られます。そのため、追記 open('a') の後に上書き open(path,'w') がある書き方では、上書きの行に destructive=False が付きます。解析器の判定や件数は変わりません。ただし、判定者がこの表の位置や destructive 列を頼りに手で判定すると、正しい矛を「誤」や declared_ok と判定してしまい、精度が実際より低く測られます。

- **宣言**: tooling / D1 / D2　**向き**: 誤警報　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: `scan_v2._contradiction_rows` が同じ (unit, site, kind) の矛の行を畳むとき、表示の属性をそれぞれ別の出所から取る: relpath は最初の行、lineno は別ファイルの行も含めた min（存在しない位置を指す）、destructive は行の効果でなく同じ (site, kind) の最初の効果から取る（追記 open('a') の後の上書き open('w') に destructive=False が付く）。
- **コードの場所**: scripts/scan_v2.py:34-64 _contradiction_rows
- **重大度の根拠**: 代表は R5-r3-1 で、探索役・設計・一般性の 3 人とも medium。検証役が run20 の manifest から数え直した結果、候補表 191 行のうち同じ組が 2 ファイル以上に跨るのは 16 組、位置が誤る行は 6（すべて teamplay-talk の D1。storage.py:36 を指すが、実際は kakao_store.py:36 と storage.py:1153）。run18 でも同じ 6 行、scan_v2_v3_run1 でも 87 行中 1 行（tekla print_drawings）が誤る。件数と主指標（153）は動かない。v3 の判定対象（v2_judge_targets.json）は位置を持たないので、今の v3 判定には効いていない。このため high にはしない。一方、docstring と verification_guide（「effect_relpath:effect_lineno を開く」「destructive 列が True なら contradiction」）がこの表を手検証の入口にしており、D60 の最終評価で真の D1/D2 矛を誤に倒しうる。このため low にもしない。R5-r1-8 は 3 人とも low で、run20 で destructive が誤る行は 0 だった。
- **直し方（一般に正しいか: 条件つきである）**: scripts/scan_v2.py の _contradiction_rows だけを直す。畳み込みの鍵 ユニット × (site, kind)（D31 の設計）と、判定・件数は変えない。
(1) 位置: relpath と lineno を別々に更新しない。(relpath, lineno) を対で持ち、組の中の CONTRADICTION 行の対の辞書順の最小を採る。一般性の検証役の推奨はこの形で、理由は 2 つ。列挙順に依らない。全行が同一ファイルなら現行と完全に一致するので、過去の run の表とも対比できる。「最初の行の対」を採る案も誤りではないが、同一ファイル内の行番号まで変える（cx_single で 10 → 16）ので対比が崩れる。加えて locations: [(relpath, lineno, declarations, destructive), ...] を行に足し、組の全位置を判定者が見られるようにする。
(2) destructive: eff_by を (site, kind) の setdefault で作るのをやめる。**素朴な直し方で壊れる反例（一般性の検証役・R5-r1-8）**: 所見の fix_sketch の鍵 (site, kind, lineno) では足りない。(a) readOnlyHint のもとで L8 の open(p,'a') と L10 の open(q,'w') が両方とも矛になると、畳んだ行は最小の lineno=8 を採り、destructive は False のまま残る。(b) 別ファイルの同じ行番号の効果（降りた呼び出し先）と取り違える。**避ける条件**: 効果の照合は (relpath, lineno, site, kind) の 4 つで行う。1 行に同じ (site, kind) の効果が複数あるときは any(destructive) を採る（設計の検証役）。組全体の destructive は、代表位置の値ではなく組の CONTRADICTION 行に一致する効果の any、または locations に位置ごとの値を並べる形にする。
(3) declarations の和も別位置の行から取る機構は同じ。検証役の数え直しでは run20 で組内の宣言集合が異なる組は 0（探索役の「1 件」は誤り）。locations に位置ごとの declarations を持たせれば一般に解ける。
守り: contradictions.json を読む script は無い（intersection_rows / contradiction_by_decl / compare_scans / catalog_map ほかは読み飛ばす）ので、列を足しても評価の経路は壊れない。検証役が scratchpad で両案を run20 の全 manifest にかけた結果、n=191 は不変、誤位置 6 → 0、変わった行はちょうど誤っていた 6 行、declarations と destructive は全行が現行と同一。直したら run20 の manifest から contradictions.json を作り直し、変わった行が上の 6 行だけであることを確かめる。authgap/ に触れないので、凍結の指紋と解決率は変わらない。
- **記録済みの限界・決定との重なり**: 無し。review_plan §5 の既知の問題、O1〜O41、D19 の K1〜K7 のどれも候補表の位置と destructive 列に触れていない。min を採る根拠も、導入時のコミット 38531e7 には無い。畳み込み ユニット × (site, kind) 自体は D31 の設計だが、どちらの所見もそれを変えない。設計の観点での反証は 2 件とも無し（refuted=false）。隣の所見 R5-r1-3（ユニット同一性の鍵に relpath が無く、別モジュールの同名ツールの矛が 1 件に潰れる）は同じ表の別の根本原因で、この単位には含めない。ただし同じ関数を触るので、同時に直すときは鍵の変更と混ぜないこと。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 形跡なし。R5-r3-1 は 3 人とも medium で、設計の検証役は「D3 / D4 だけではない（誤る行は全部 D1）」と明記している。R5-r1-8 の low の理由は「道具の表示の属性だけ」「追記が先に来る形だけ」「run20 で誤る行 0」の 3 点で、D3 / D4 の旧文言には依っていない（再現例も D2 の矛）。
- **推奨の理由**: 代表の重大度は medium です。一般に正しい直し方があり、条件は (relpath, lineno, site, kind) で照合することと、対の最小と locations を持たせることです。凍結した語彙は要らず、設計の観点での反証もありません。scripts/scan_v2.py の 1 関数だけの変更なので、解析器の凍結の指紋に触れません。表は最終評価（D60）の手検証の入口で、verification_guide の手順が位置と destructive 列を判定の根拠に使っています。道具の欠陥ですが、最終評価の経路で起きるので直すことを推奨します。R5-r1-8 単独なら low ですが、同じ関数の同じ畳み込みで一緒に直せます。
- **所見**:
  - R5-r3-1: 代表（medium ×3）。relpath は最初の行から、lineno は別ファイルの行も含めた最小から取るので、存在しない位置を指す。run20 で 6/191 行、v3_run1 で 1/87 行が実際に誤る。直す。（scan_v2.py の contradictions.json（手検証の候補表）が、同じ (unit, site, kind) の矛の行を畳むとき relpath は最初の行、lineno は別ファイルの行の min から取るため、存在し）
  - R5-r1-8: 同じ関数の同じ畳み込みの別の表れ（low ×3）。destructive を行の効果でなく (site, kind) の最初の効果から取るので、追記の後の上書きに False が付く。run20 で誤る行は 0。鍵 (site, kind, lineno) では足りない反例があるので、(relpath, lineno, site, kind) で照合し any を採る形で一緒に直す。（contradictions.json（手検証の候補表）の destructive は行の効果ではなく同じ (site, kind) の最初の効果から取られるため、追記 open('a') の後に書き出し open(path,'w') があ）

### U52 run ディレクトリの manifest の集合が summary.json と結びついていない（書く側・読む側の両方）（段階 A・重大度 中・推奨 直す）

走査の結果は、木ごとの結果ファイル（manifest）と、その回に走らせた木の一覧（summary.json）に分けて保存されます。ただし、集計の道具（contradiction_by_decl / intersection_rows / compare_scans）は一覧を見ずに、フォルダにある .json を名前で拾います。このため次の 3 つが起きます。(1) contradiction_by_decl は名前に「-」が無いファイルを黙って読み飛ばします。木の名前が A9__vuln や eval_01 の形だと、宣言ごとの矛の表が D1〜D4 とも 0 になります。(2) 同じ label で走らせ直すと、標本から外れた木や解析に失敗した木の古い manifest が残り、今の回の結果として数えられます。(3) 文字列定数に単独のサロゲート（"\ud800"）があると manifest を UTF-8 で書くところで例外が出ます。すると run 全体が止まり、書きかけのファイルが残ります。誤りの向きは主に数え落としです。(2) は件数を上乗せしますが、比較では消えた矛が見えなくなります。

- **宣言**: tooling / D1 / D2 / D3 / D4　**向き**: 数え落とし　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: run ディレクトリの manifest の集合が summary.json と結びついていない: scan_v2.py は同じ label の再走査で古い木の manifest を消さず（analysis_failed の木は新しい manifest を書かない）、manifest の書き出しが try の外なので孤立サロゲートの文字列定数（ir.py の utf-8 化）で UnicodeEncodeError が出ると run 全体が止まり書きかけの manifest が残る; 読む側（contradiction_by_decl / intersection_rows / compare_scans）は summary.json の木の一覧でなくディレクトリのファイル名で列挙し、contradiction_by_decl は `"-" not in fn` の manifest を黙って読み飛ばす。
- **コードの場所**: scripts/scan_v2.py:92-148 再走査・書き出し, authgap/ir.py:410 str 定数の表現, scripts/contradiction_by_decl.py:38-43, scripts/intersection_rows.py:57-62, scripts/compare_scans.py:39-44
- **重大度の根拠**: 重大度は代表の所見 R5-r1-4 に合わせた。3 意見（探索 medium / 設計 medium / 一般性 low）の中央値が medium。contradiction_by_decl は D62 で主指標にした D1〜D4 を宣言ごとに報告する道具そのもので（review_plan §1 (c)）、「-」の無い名前では 4 宣言とも黙って 0 になる。同じ種類の失敗は一度実際に起きている（コミット 9c8eb81。`startswith("v2-")` のせいで v3 の表が全部 0 になった）。一般性の観点が low としたのは「sample_population_v2.py の `--prefix` で作れば名前に必ず「-」が入り（v2 87 木・v3 91 木とも「-」の無い名前は 0）、今の手順では起きない」ためで、D3/D4 の旧文言によるものではない。R5-r2-7 と R5-r2-6 は 3 観点とも low。R5-r2-7 は、既存の evidence/scan_v2_* 28 ディレクトリのうち 27 で manifest の集合が ok の木の集合と一致し、同じ label を使い直したときにしか起きない。R5-r2-6 は corpus の 425,237 項目に非 UTF-8 の名前が 0 件、サロゲートのエスケープは vendored の .venv にしか無く、起きても例外が出るので気づける。3 件とも評価の道具（scripts/）の問題で、最終評価（D60）の経路に入る。凍結の指紋に触れずに直せるので、low の 2 件も同じ単位で直す価値がある。
- **直し方（一般に正しいか: 条件つきである）**: 【読む側 3 本（contradiction_by_decl / intersection_rows / compare_scans）と v3_miss_sample.py:40】
- 木の一覧は summary.json の `trees` のうち status == "ok" のものから作り、manifest 名 = `<tree>.json` とする。ファイル名の形（「-」の有無など）には頼らない。
- ディレクトリにあるのに一覧に無い（余分）、一覧にあるのにファイルが無い（不足）ときは、警告を出して件数を表に出す。scan_v2_run8 は summary が ok 87 なのに manifest が 0 件で、今は黙って 0 と数えている。
- summary.json が無い書きかけの run は、今までどおり listdir に戻って警告する。こうすれば壊れる run は無い（一般性の観点の条件）。
- 【素朴な直し方で壊れる反例（一般性の観点）】`or "-" not in fn` を消すだけだと、run ディレクトリに manifest 以外の .json（手書きの notes.json など）があるとき、contradiction_by_decl の `json.load(...)["units"]` が KeyError で落ちる。黙った数え落としではないが、「壊れるケースは無い」という探索役の見立ては言い過ぎ。【避ける条件】summary.json の trees から名前を決める。そうでなければ `units` 鍵の無いファイルを飛ばす。
- 安全網として、contradiction_by_decl の宣言ごとの合計を summary.json の verdict_rows / contradictions.json の n と照合し、合わなければ警告する。数える単位（ユニット × site × kind）は先に揃えておく。
- 同じ仮定は o23_cells.py:103 と o39_count.py:83（`startswith("v2-")`）にもある。これらは評価の経路ではなく未決問題の集計用だが、一緒に直すか限界として書く。

【書く側 scan_v2.py】
- --resume なしで始めたとき、out_dir にすでに manifest があれば止める。【避ける条件（一般性の観点）】標本に無い manifest を自動で消す案より安全で、label を取り違えてもデータを消さない。
- 解析が analysis_failed になった木について、古い `<name>.json` が残っていれば消す（または一覧から外れていることを読む側が警告する）。
- 【サロゲート（R5-r2-6）の最良の直し方（一般性の観点）】scan_v2.py で書き出すすべてのファイル（manifest / summary.json / contradictions.json / progress.jsonl）を `open(..., encoding="utf-8", errors="backslashreplace")` で開く。UTF-8 で書けない文字はサロゲートだけで、JSON 文字列の中に `\ud800` のエスケープとして書かれ、json.load で元の str に戻る。本物のバックスラッシュは json.dumps がすでに `\\` にしているので混ざらない（検証役が 4 つの入力で往復の一致を確かめた）。判定も解決率も変えず、scripts/ だけで直る。
- 【素朴な直し方で壊れる反例（一般性の観点）】探索役の案 (a)「ir.py:410 で str 定数を repr にする」は定数しか覆わない。非 UTF-8 のファイル名（os.listdir の surrogateescape で `\udcff` になる。t-fname で再現）が同じ行で漏れる。そのうえ authgap/ を変えるので指紋も変わる。案 (b)「manifest_json と書き出しを try に入れて analysis_failed にする」は、解析が済んで見つかっているその木の矛（D1 fs_write）を捨てる。数え落としに記録が付くだけになる。どちらも backslashreplace に劣る。
- ほかの書き出し失敗（ディスクが満杯など）への備えとして、manifest は一時ファイルに書いてから os.replace で置き換え、書きかけ（0 バイト）の `<name>.json` を残さない。書けなかった木は error つきで summary に残す。0 バイトのファイルが残ると、R5-r2-7 と組み合わさって読む側の json.load が落ちる二次被害がある。
- テストで確かめる入力: 「-」の無い名前 / 手書きの notes.json / 同じ label で標本を変えた再走査 / analysis_failed に変わった木 / `"\ud800"` の定数 / 非 UTF-8 のファイル名 / summary.json の無い run。既存の 28 run ディレクトリで結果が変わらないこと（27 は同一、run8 は警告だけ）も確かめる。
- **記録済みの限界・決定との重なり**: 無し。review_plan §5 の既知の問題（O35/O38/O39/O40/O41、K1〜K6、MAX_DEPTH など）にも、decisions.md・open_questions.md（O1〜O41）・D19 の K1〜K7 にも、同じ label を走らせ直したときの manifest の扱い、ファイル名のフィルタ、サロゲートや書き出しの失敗の扱いを決めた記録は無い（3 件とも設計の観点で refuted=false）。関係する記録は 3 つある。(1) コミット 9c8eb81 は「木ごとの manifest を名前の接頭辞によらず読む」ことを意図していたが、「-」への依存が残った。(2) scan_v2.py のコメント「1 本の失敗で全体を落とさない。件数として残す」と verification_guide.md:297 は設計の意図で、R5-r2-6 はそれとの食い違い。(3) D62 は contradiction_by_decl を D1〜D4 の主指標の報告に使うと決めている。D61 には触れない（v2/v3 の件数に合わせた変更ではなく、名前・言語・codec の仕様から導ける直し方）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R5-r1-4 を一般性の観点が low にした理由は「sample_population_v2.py の命名なら起きない（tooling の規則）」で、R5-r2-6 / R5-r2-7 を low にした理由は「まれ・大きな音で落ちる」と「label ごとに新しい dir を使う限り起きない」。どれも「D3 / D4 だけなら low」を理由にしていない。
- **推奨の理由**: 代表の重大度は medium。一般に正しい直し方があり（検証役の条件つき）、語彙の追加は要らず、設計の観点で反証された所見も無い。scripts/ だけで直る（サロゲートは ir.py の repr ではなく、書き出しの errors="backslashreplace" で直す）ので、解析器の凍結の指紋（authgap/）に触れない。最終評価（D60）は新しいデータで行い、木の名前や label の使い方は決まっていない。そのため 3 件とも評価の経路で起きうるので、low の 2 件も含めてまとめて直すことを推奨する。既存の run で結果が変わるのは scan_v2_run8（manifest が 0 件）に警告が出ることだけで、過去の数字は変わらない。
- **所見**:
  - R5-r1-4: 代表（medium）。contradiction_by_decl.py:40 の `"-" not in fn` が、「-」の無い名前の manifest を黙って読み飛ばす。姉妹の 2 本とは数え方が食い違う。直すなら summary.json の trees を使う。notes.json で KeyError になる反例を避けること。v3_miss_sample.py:40 も同じ。（contradiction_by_decl.py はファイル名に '-' を含まない manifest を黙って読み飛ばす（`"-" not in fn`）ため、木の名前に '-' が無い run では矛 / 不がすべて 0 になる。int）
  - R5-r2-7: 同じ原因（読む側が summary.json でなくディレクトリを数える）の書く側の表れ（low）。同じ label で走らせ直すと古い manifest が残って数えられる。直すなら読む側は summary の ok の木を使い、余分・不足を警告する。書く側は削除ではなく、dir が空でなければ止める。（scan_v2.py は同じ label の再走査で古い木の manifest を消さず（progress.jsonl だけ消す / --resume は標本に無い木を見ない / analysis_failed の木は新しい manifes）
  - R5-r2-6: 同じ単位の書き出しの穴（low）。孤立サロゲートの定数や非 UTF-8 のファイル名で UTF-8 の書き出しが落ち、run 全体が止まって書きかけの manifest が残る。直すなら ir.py の repr や analysis_failed 化ではなく、書き出しを errors="backslashreplace" にし、一時ファイル + os.replace で書く。（孤立サロゲートを含む文字列定数（"\ud800"）が slot の定数として manifest に入ると、scan_v2.py の utf-8 の書き出しが UnicodeEncodeError で落ち、try の外なので木が analys）

### U19 match 文の capture の束縛（段階 C・重大度 低・推奨 限界として記録）

Python 3.10 の `match` 文で `case {"cmd": c}:` や `case [exe, *rest]:` や `case c:` と書くと、実行時には c や exe に入力の値（またはその一部）が入ります。解析器（authgap/val/engine.py の Match の処理）は各 case の中身を実行するだけで、case の形（パターン）を読まないので、c が何なのかを知りません。そのため c は「出所不明（OP/opaque(unresolved)）」になり、ツールの引数がそのままシェルに渡る危険な書き方でも、宣言との矛盾（矛）が出ずに「判定できない（不）」に落ちます。つまり、本当はある矛盾を数え落とす向きの誤りです（「矛盾なし」と誤って言うわけではありません）。

- **宣言**: D1 / D2　**向き**: 数え落とし　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_exec_stmt` の Match が各 case の本体を実行するだけで pattern（MatchAs / MatchMapping / MatchSequence / MatchStar / MatchClass）を歩かないので、`case {"cmd": c}` などで取り出した名前が束縛されず `OP/opaque(unresolved)` の `Atom(formal)` になる（主体まで OP に落ちる）。
- **コードの場所**: authgap/val/engine.py:395-403 _exec_stmt Match
- **重大度の根拠**: 探索役・設計・一般性の 3 意見がそろって low（review_rows.json の severities = [low, low, low]）。根拠は、探索役が AST を走査して v2 の 87 木で capture つきの match が 0 箇所だったこと（v3 と最終評価のデータでの出現数は未測定）。効くのは D1 / D2（SPAWN）なので、旧文言「D3 / D4 だけなら low」で下がったものではない。向きについて: 探索役は false_clean と書いたが、一般性の検証役は「矛 → 不であって内（矛盾なし）にはならないので、厳密な誤 clear ではなく矛の数え落とし」としている。ここではその見方を採った。ただし主体まで OP に落ちるので、D44 が想定する保守側の MODEL/opaque にも届かない。
- **直し方（一般に正しいか: 条件つきである）**: 直す場所は authgap/val/engine.py:395-403 の `_exec_stmt` の Match の分岐。各 case で、本体を `ce` の上で実行する前に `case.pattern` を歩いて名前を束縛し、guard を評価する。case 同士の合流（`env_join`）は今のまま変えない。PEP 634 に沿った束縛の決め方は次のとおり。
- MatchAs（`case c` や `... as c`）: subject そのものを束縛する（MODEL は流れ込む、という D57 §9.3 の設計と合う）。
- MatchMapping の key: `subject[key]` を読むのと同じ経路（`_refine_roots(_element_of(subject), subject.roots, key)`）。`**rest` は subject。
- MatchClass の kwd（`Runner(cmd=c)`）: 属性の読み（`subject.cmd` と同じ経路）にする。位置引数は `__match_args__` が解決できなければ opaque のまま。
- MatchOr: 選択肢ごとの束縛を join する。
- MatchValue / MatchSingleton: 何も束縛しない。
- MatchSequence / MatchStar: PEP 634 / 3132 に従う（`*` より前は左から、後ろは右から数える。`*` には中間のスライスが入る）。ただし engine の Seq は insert や添字代入のせいで位置が正確でないので、保守側で束縛する（`*` の対象と `*` より後ろの対象には、位置を持たない join か tail を入れる）。

【検証役が見つけた、素朴な直し方で壊れる反例（fix_sketch をそのまま入れてはいけない）】
(1) MatchSequence を「位置が決まれば elems[i]」、MatchStar を「subject の列全体」で束縛すると、R1-r3-6（拡張アンパック）と同じ誤りを match に持ち込む。反例 ce5 の seq_star_last は `match ["x", "ls", cmd]: case [*_, last]: os.system(last)` で、実行時には last == cmd（MODEL）。今は opaque で正直に「不」になっているが、素朴に直すと last が 'ls' の OP/resolved になる。根拠の無い resolved への引き上げで、しかも矛が消える。
(2) MatchClass の kwd を `_element_of(subject)` で束縛すると、Obj の field が失われる。反例 ce5 の class_kw（`r = Runner(cmd); match r: case Runner(cmd=c): os.system(c)`）で、c が field の MODEL ではなく、subject の主体の Unknown（resolved）になる。
【避ける条件】位置の束縛は右端から数え、`*` 以降は位置を持たない保守側の値にする。MatchClass は属性の読みの経路を使う。解決できないものは opaque のまま残す（黙って resolved にしない）。
【手順の条件】opaque → resolved を増やす変更なので、CLAUDE.md の敵対的レビュー（resolved にしてよい根拠を 1 件ずつ崩しに行く）を通す。反例テストには ce5 の seq_star_last / class_kw / eq_check_flows と、探索役の match_capture の 4 ユニット（mapping / sequence / class / as）を入れる。直した後は scripts/diff_effects.py と scripts/compare_scans.py で回帰を確かめる。v2 での出現は 0 なので、v2 の件数は変わらないはず。変わったら、それ自体が回帰の兆候として調べる。
- **記録済みの限界・決定との重なり**: なし（設計の検証役が確認した）。D35 の限界、K1〜K7、O35〜O41 のどれにも match の記録は無い。仕様書 AUTHGAP_BRIEF_v3.md:413 の「match は if 連鎖へ脱糖」はゲート側の CFG の話で、val 側で束縛を省く決定ではない。D58 改訂の規則 2(c)（decisions.md:3229）は match の capture を「名前を束縛し直す文」として数えており、設計は束縛されることを前提にしている。束縛されない名前が opaque(unresolved) になるのは D17 の設計だが、ここでの原因は「実行時に束縛される名前を env に書かない」ことで、D59 が関数本体の import について直したのと同じ種類の欠陥（decisions.md:3313-3318）。隣の所見 R1-r3-6（拡張アンパックの `*` を列全体で束縛し、`*` より後ろを左から数える）は、直し方を誤ったときに同じ誤りが入り込む関係にある（別の単位）。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。効くのは D1 / D2（SPAWN）で、3 意見とも low の理由は「v2 の 87 木で出現 0、まれ」であり、「D3 / D4 だけなら low」という旧文言は使われていない。
- **推奨の理由**: 推奨の基準の「low でまれな書き方」に当たる。3 意見とも low で、v2 の 87 木では出現 0（v3 と最終評価のデータでは未測定）。一般に正しい直し方はあり、語彙の追加も要らず、設計の反証も無いので、直すこと自体の筋は通る。ただし次の理由から、凍結の直前には記録に回すのが妥当と考える。
- 解決率を上げる変更で、敵対的レビューが要る。
- 素朴な直し方では、検証役の反例 ce5 のとおり根拠の無い resolved を作る。これは矛を消す、より悪い誤り。
- 列の位置を正しく扱うには R1-r3-6 と同じ保守側の設計が要り、規模が M になる。
記録には次を書く: 「match の capture は束縛しない。capture した名前を通る SPAWN は矛にならず不に落ちる（数え落とし）。v2 では出現 0」。
もし学生が直すほうを選ぶなら、fix_outline の条件で直す。安全側の途中までの直し方としては、MatchAs / 裸の capture / MatchMapping の key / MatchClass の kwd（属性の読み）だけを束縛し、MatchSequence / MatchStar / MatchClass の位置引数は opaque のまま残す方法がある。これなら反例 (1) を避けられる。
- **所見**:
  - R1-r3-5: 代表で、この単位の唯一の所見。3 観点とも生き残った（実行 25/25 行が再現、設計・一般性とも反証なし、fix_is_general = true）。一般性の検証役が fix_sketch の Sequence / Star / Class の束縛の誤りを反例 ce5 で示した（fix_outline に写した）。（`match` 文の capture パターン（`case {"cmd": c}` / `case [exe, *rest]` / `case str(c)` / `case … as c` / `case c`）を一度も束縛しないので、M）

### U20 O31 の静的判定が条件式・短絡に効かない（段階 C・重大度 低・推奨 限界として記録）

呼び出し元が定数を渡していて片方の枝が実行されないと分かるとき、解析器はその枝を刈る（O31、D58）。ただしこの刈り込みは `if` 文にしか効かない。1 行の条件式 `"a" if append else "w"` や、短絡 `really and shutil.rmtree(path)` / `dry or os.remove(path)` では、実行されない側も評価してしまう。その結果、`append=True` を渡しても開くモードが「a か w か不明」になって D2 の矛盾が出る。`really=False` で削除が起きない場合でも FS_WRITE の効果と D1 の矛盾が出る。誤りの向きは誤警報（実際には無い矛盾を出す）だけで、誤 clear（実際の矛盾を見逃す）にはならない。

- **宣言**: D1 / D2　**向き**: 誤警報　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: O31（D58 改訂）の静的な仮引数による枝刈り `_static_truth` を `_exec_stmt` の `ast.If` にしか当てず、`_ev_IfExp`（`x if c else y`）と `_ev_BoolOp`（`c and f()` / `c or f()`）は静的に決まる条件でも両側を評価するので、到達しない側の mode / sink が効果になる。
- **コードの場所**: authgap/val/engine.py:622-640 _ev_IfExp / _ev_BoolOp, authgap/val/engine.py:328-338 _exec_stmt If の静的判定, authgap/val/engine.py:2004 _static_truth
- **重大度の根拠**: 探索役・設計・一般性の 3 意見がすべて low で、代表値も low（review_rows.json）。向きは誤警報だけで、静的でない条件ではこれまでどおり両方の枝を評価するので、誤 clear は起きない。同じ内容を if 文で書けば正しく刈られる。`"a" if append else "w"` の mode の書き方を探索役は「常套」と書いているが、v2 / v3 での出現数は未測定。D1+D2 の所見なので、旧文言「D3 / D4 だけなら low」は当たらない。重大度を戻す必要は無い。
- **直し方（一般に正しいか: 条件つきである）**: 直し方（探索役の案と一般性の観点による補足）: `_ev_IfExp`（engine.py:622）では、まず今までどおり test を評価する。次に `_static_truth(node.test, env, self._static_stack[-1] if self._static_stack else frozenset())` を取り、None でなければ取られる側だけを評価する。`_ev_BoolOp`（:628）では要素を左から順に評価し、`and` は静的に False と決まる要素で、`or` は静的に True と決まる要素で止め、戻り値はその要素の値にする。静的に決まらない要素から後は今までどおり join する。こうすると if 文の test に書いた短絡（`if really and shutil.rmtree(p):`）も同時に直る。

守ること（素朴な直し方で壊れる形）:
(1) 式全体に `_static_truth` を当てて全部を捨てない。`_static_truth` は `and` の要素のどこかが False なら位置によらず False を返す（engine.py:2016-2020）。そのため `f() and flag` を丸ごと刈ると、実際に実行される `f()` の効果が消える（誤 clear）。止める位置より前の要素は必ず評価する。
(2) 静的な名前の集合は `if` と同じもの（D58 改訂の規則 1〜2 = 直接呼び出しの仮引数のうち、リテラルか静的な名前から来て、本体で束縛し直されないもの）だけを使う。局所変数や大域の名前を静的にすると、run15 で誤 clear 23 行を出した (B)(C)(D) の値の欠陥（O36）が戻る。
(3) test の中の呼び出しなどの副作用は今までどおり評価する（`_static_truth` は呼び出しを含む条件を None にする）。

一般性の観点が確かめた「壊れない」形: 内包の対象で名前を隠す形（comp_shadow）は `_rebound_names`（engine.py:1922-1941）が Store として拾うので静的にならない。`_ev_Lambda` は本体を評価しないので、lambda の仮引数で隠す形は起きない。MODEL の仮引数を渡す形（model_flag）は静的でないので、今までどおり矛盾が出る。反例は作れなかった。

手順: 刈り込みの範囲が広がるので、D58 と同じく「規則 → 刈ってはいけない形の敵対的テスト → 実装」の順で進める。その後 `diff_effects.py` と `compare_scans.py` で消えた効果行を 1 件ずつ確かめる。
- **記録済みの限界・決定との重なり**: 設計の観点が「規則どおり」として反証している（confidence 0.6）。理由: D58 O31 の規則 2 と改訂の規則 4（decisions.md:3143-3145, 3234）は、刈る対象を `if` 文の枝に限っている。所見が根拠に挙げた「規則 3 が除外したのは try / with / ループだけ」は、終わる枝の規則を読み違えたもの。「D51 の原則」は観察で、判定の規則ではない。したがって直すことは凍結した O31 の範囲を広げる規則の変更にあたる。設計の観点の迷い: 規則は条件式や短絡を明示的に除外したのではなく、書いていないだけ。一般性の観点は逆に「`if` しか挙げていないのは書き方の問題で、除外の決定ではない」とし、反証していない。review_plan §5 の既知の問題と O41 には無い。open_questions にも記録されていない（記録するなら O42 以降の候補）。O36（値の欠陥 (B)(C)(D)）は、静的な名前を仮引数に限る理由として関係する。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し（D1+D2 の所見で、3 意見とも low。検証役の理由に D3 / D4 への言及は無い）
- **推奨の理由**: 重大度は low で、向きは誤警報だけ。設計の観点は、凍結した O31 の規則（`if` 文だけを刈る）どおりの動きと判定している。直すことは、刈る範囲を広げる規則の変更（解決を上げる向き）になり、D58 と同じ敵対的レビューと v2 の取り直しが要る。これは凍結前の添削の範囲を超える。直し方そのものは Python の意味で一般に正しく、語彙の追加も要らない。したがって学生が直すと決めた場合は、fix_outline の条件 (1)〜(3) を守れば安全に入れられる。記録するときは「条件式・短絡では O31 の刈り込みが効かず、if 文と結果が変わる（誤警報の向き）」と書き、出現数は未測定と明記する。
- **所見**:
  - R1-r2-7: 代表（この単位の唯一の所見）。実行は 18/18 行が再現。設計の観点は「規則どおり」として反証。一般性の観点は生存（反例なし）。3 意見とも low、誤警報、D1+D2。（O31 の静的判定が `ast.If` にしか掛からず、条件式 `x if c else y` と短絡 `c and f()` / `c or f()` は静的な仮引数でも両側を評価する: `open(path, "a" if append）

### U21 try の else の到達性（段階 C・重大度 低・推奨 限界として記録）

Python の try 文の else 節は「try の本体が例外も return も無く最後まで進んだとき」だけ走ります。解析器（engine.py の _exec_stmt の Try）は、本体が必ず return / raise で抜ける場合でも else 節をいつも実行したものとして扱うので、実際には絶対に走らない else の中の書き込み（例: os.remove）が効果行として出て、readOnly と宣言したツールが「矛盾あり」と判定されます。向きは誤警報（本当は矛盾でないのに矛盾と出す）です。`try: return ... except: return ... else: <書き込み>` というまれな書き方でだけ起き、件数は未測定です。

- **宣言**: D1 / D2　**向き**: 誤警報　**規模**: S　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_exec_stmt` の Try が本体の終わり（return / raise）を記録せず `orelse` を常に実行するので、到達しない else 節の sink が効果行になる（D58 規則 3 は try が関数を終えるかの話で、else の到達性は扱っていない）。
- **コードの場所**: authgap/val/engine.py:357-374 _exec_stmt Try
- **重大度の根拠**: 重大度は探索役・設計の観点・一般性の観点の 3 意見とも low（中央値 low）。影響は D1+D2 で、D3 / D4 だけに効く話ではない。検証役が旧文言「D3 / D4 だけなら low」を理由に重大度を下げた形跡は無いので、戻す必要も無い。low とした理由は、誤警報の向きであること（誤 clear ではない）、そして本体と except の両方が必ず return / raise で終わり、else に sink があるという形がまれであること。件数は未測定。実行の観点では 7/7 行が再現した（exec_lens_r3plus.json）。
- **直し方（一般に正しいか: 条件つきである）**: 直し方（authgap/val/engine.py:357-374 の _exec_stmt Try）: 本体を回すループで、_exec_stmt が True を返した（その文で本体が終わった）ら body_ended = True を立てる。orelse は not body_ended のときだけ実行する。finalbody は今までどおり常に実行する。try 文そのものの戻り値は今までどおり False のまま（D58 規則 3「try は終わるとみなさない」は変えない）。同じ原因の R1-r4-9 もまとめて直すなら、else の入口の env を merged（本体の後の env に handler の env を合流したもの）ではなく「本体が正常に終わった時点の env」にする。else は handler と合流する前のその env で実行し、結果を handler 側の env と合流する。finalbody はその合流の後に実行する。
守るべき条件（検証役の notes から）: (1) body_ended は、最上位の Return / Raise と、両枝が終わる If だけで True になる。with / try / ループの中の return では True にならない。だから保守側は崩れない。検証役が反例ファイル ce12 で確認した形は次のとおり。cond_return_else（片側だけ return する if）は直した後も else を実行して矛のまま（正しい）。with_return_else も D58 規則 3 で with を終わるとみなさないので、else を実行したまま保守側に残る。via_helper（静的な dry=True の既定値で必ず return する helper）は今の矛が消えるが、Python の意味でも到達しないので消えるのが正しい。break / continue では _exec_stmt が False を返すので、else は実行されたままになる（保守側に残り、誤 clear は生まない）。(2) 危険が 1 つある。_static_truth による枝刈りが誤っていると、else を誤って捨てうる。ただしこれは「return の後の文を捨てる」既存の経路と同じ信頼の上にあり、新しい危険ではない。(3) 到達しない効果行を消す変更（R1-r4-9 の分では定数が読めるようになる変更）なので、CLAUDE.md と D58 に従い、敵対的な反例テストを実装より先に書く。直した後は diff_effects.py と compare_scans.py で消えた行を 1 件ずつ確かめる。(4) 採るときは decisions.md に書き添える。D58 規則 3 の「try は終わるとみなさない」は try 文の後ろの文についての決定で、else の到達性は別だと明記すると、設計の観点の迷いが消える。素朴な直し方で壊れる反例は、一般性の検証役には作れなかった。
- **記録済みの限界・決定との重なり**: 部分的に重なる。D58 規則 3（decisions.md:3146-3148）は「try / with / ループは終わるとみなさない（保守側）」と決めている。D35 の限界 5（decisions.md:320-321）は、経路を区別しないせいで dead な経路に行が出ること（false-dirty 側）を受け入れている。設計の観点の判断は refuted=false（確信度 0.55、迷いあり）。その理由は 2 つ。規則 3 は try 文の後ろについての決定で、else 節の到達性は扱っていない。D35 の限界 5 は値で決まる dead 経路で、構文上の到達不能とは根本原因が違う。一方、規則 3 の「保守側」の精神で、今の動きを意図どおりと読む余地もある、と検証役は書いている。checked #105（with / try の return が外へ伝播しないのは D58 規則 3 の設計）とは別の点。review_plan §5 の既知の決定の一覧には載っていない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 意見とも最初から low で、影響は D1+D2。旧文言「D3 / D4 だけなら low」を理由にした形跡は無い。
- **推奨の理由**: 推奨の基準では、fix には medium 以上が要る。この単位は 3 意見とも low で、まれな書き方の誤警報（誤 clear ではない）なので、限界として記録するのを推奨する。記録先は D35 の限界 5 の隣で、「try 本体が必ず終わるときも else を実行する（構文上の到達不能。誤警報側）。R1-r4-9 の、handler の束縛が else に流れ込む問題も同じ原因」と書く。ただし学生が直すと決めても差し支えは小さい。一般に正しい直し方があり（言語リファレンス 8.4 の意味から導け、検証データに合わせる話ではないので D61 の基準も満たす）、1 関数の局所変更（S）で、語彙の追加も要らず、一般性の検証役は反例を作れなかった。直す場合は解析器の凍結の指紋に触れるので、D58 と同じ順（規則 → 反例テスト → 実装 → diff_effects / compare_scans）を踏むこと。
- **所見**:
  - R1-r3-12: 代表。try 本体と except が必ず return / raise で終わるのに else の os.remove を実行し、readOnly × FS_WRITE で contradiction:D1:fs_write になる（誤警報）。3 観点とも生き残り（実行 7/7 再現、設計は refuted=false で迷いあり、一般性は refuted=false で反例なし）。重大度 low / low / low。（`try` 本体が必ず終わる（`return` / `raise`）ときも `else` 節を実行するので、到達しない `else` の sink が効果行になり readOnly の矛になる（誤警報。D58 規則 3 は try が関数を）
  - R1-r4-9: 同じ原因の別の表れ（探索の重複除去で R1-r3-12 に統合済み。単位の所属一覧には載っていない）。else を、handler の env と合流した後の merged で実行しているので、handler の束縛が else に流れ込む。本体で選んだ定数（mode="a" / m="DELETE"）が読めなくなり、D2 の誤警報と D1 の誤 clear（net_method_unknown の不）の両方の向きに誤る。重大度 low。else の入口を「本体が正常に終わった時点の env」にすれば両方とも直る。（）

### U27 文字列の args の argv0 の射影（段階 C・重大度 低・推奨 限界として記録）

subprocess.run や pty.spawn に、リストではなく文字列を 1 本だけ渡し、shell=True を付けない場合（例: `subprocess.run("/usr/bin/" + tool)`、`Popen(f"{BIN}/{tool}")`）を扱う誤りです。POSIX ではこの文字列全体が実行するプログラムのパスになるので、モデルが渡す値でどのプログラムを動かすかを選べます。ところが解析器は、つなげた文字列の最初の部品（定数の "/usr/bin/"）だけを「実行するプログラム」とみなします。そのため readOnlyHint / destructiveHint の宣言との矛盾（矛 spawn_model）を見逃して「不（判定できない）」を出します。これは誤 clear の向きです。同じ読み方を使う pipe 形（`Popen(PY_DIR + "/python3", stdin=PIPE)` の後に `communicate(input=code)`）でも、実行されるのがインタプリタだと分からず、D2 が 矛 exec ではなく 不 fs_unknown になります。

- **宣言**: D1 / D2　**向き**: 誤 clear　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_first_element` が Str（連結した文字列）に対して語の境界を見ずに `parts[0]` を返すので、shell=False で文字列を渡す `subprocess.run("/usr/bin/" + tool)` / `Popen(f"{BIN}/{tool}")` の argv0 が定数の接頭辞（OP/resolved）になり、モデルがプログラムを選べるのに 不 になる（同じ射影を使う pipe 形のインタプリタ判定も外れる）。
- **コードの場所**: authgap/effects.py:206-220 _first_element, authgap/catalog/sinks.py:248, 282, 304 argv0 の elem0 指定, authgap/effects.py:774-777, 806-813 _register_handle / pipe
- **重大度の根拠**: 探索役・設計の検証役・一般性の検証役の 3 者とも low。理由は影響する宣言ではなく、書き方がまれなこと。探索役の AST 走査では、corpus 8,648 ファイルのうち shell=True 無しで文字列の連結や f 文字列を subprocess.* / pty.spawn の第 1 引数に直接渡す形は 0 件だった（リストで渡すのが普通の書き方）。ただし、変数を経由する形（`cmd = BIN + "/" + tool; subprocess.run(cmd)`）は走査が終わっておらず未測定なので、「まれ」と言えるのは直接渡す形だけ。影響するのは D1 / D2 なので、D62 の「D3 / D4 だけ」の文言とは関係しない。実行の観点では 45 行の出力がすべて再現した（exec_lens_r4r5.json）。
- **直し方（一般に正しいか: 条件つきである）**: 直す場所は authgap/effects.py の `_first_element` の Str 分岐（今は `parts[0]` を返す）。採る規則（一般性の検証役が monkeypatch で実装して確かめたもの）: Str の parts を先頭から見て、確度 resolved の str 定数が続くあいだはつなげていく。つないだ文字列（lstrip の後）に空白があれば、定数のプログラムの語（最初の語）を argv0 として返し、今までどおり OP → 不 spawn_command にする。空白が出る前に定数でない part に当たったら、Str 全体を返す（主体と確度はそのまま）。この規則で `"/usr/bin/" + tool`、`f"{BIN}/{tool}"`、`BIN + "/" + tool`、`pty.spawn("/usr/bin/" + tool)` が 矛 spawn_model になる。
【素朴な直し方で壊れる反例（一般性の検証役）】探索役の fix_sketch どおりに「parts[0] に空白があるときだけ最初の語」とすると、次の 3 つがどれも 矛 spawn_model になり、新しい誤警報を生む。(a) `f"{BIN} --version {tool}"`（空白が 2 番目の part にある）、(b) `"/usr/bin/" + "git " + tool`（定数の part が 3 つ続く）、(c) `" ".join(["git", tool])`（join の区切りが独立した part になる）。これを避ける条件は「先頭から続く resolved の定数 part をつないでから空白を探す」こと。そうすれば a / b / c は 不 のままになる。
【変わってはならない対照】os.path.join（Path 形）、リスト連結、os.execv、create_subprocess_exec、list + list、tuple +、`cmd +=`、Popen に列を渡す pipe 形の EXEC、spawn_shell_list の木。改訂した規則で、どれも変わらないことを検証役が確かめている。Seq / Argv の分岐が先に評価されるので、列の要素の扱いは変わらない。
【規則として明記すべき点】POSIX では `"git " + args` も文字列全体がプログラム名になる。空白のある定数の最初の語をプログラムとみなすのは Windows 流の読み方で、それを 不 のまま残すのは規則の選択になる。直すなら、この選択を規則文に書いておく。
【直らない部分】pipe 形（`Popen(PY_DIR + "/python3", stdin=PIPE)`）は直らない。`_register_handle` / `_pipe` は `first.const` を読むが、Str 全体が返ると定数が取れず、argv0 は None になる。その結果は今と同じ FS_WRITE 情報行で、情報行は落ちない（D61 G1 の教訓に反しない）。EXEC まで直すには R3-r2-1（定数どうしの Str の畳み込み）が要る。
【手順】直すなら、反例のテスト（repro の 2 つの木と、検証役の ce1 の木 a / b / c と対照）を先に置く。直した後は scripts/diff_effects.py と compare_scans.py で突き合わせる。
- **記録済みの限界・決定との重なり**: 設計の観点では反証できなかった（refuted=false）。elem0 射影を Str の parts[0] にするという決定は、D 番号・O 項目・K1〜K7 のどこにも無い。近いが根本原因が違うものは次のとおり。K1（argv0 がモジュール水準のリストのときに pipe の EXEC が消える。`_pipe` 側の話）、O35（列の中の要素をオプション名と値に分けるかどうか）、O41（`shlex.quote` した固定コマンド、標準入力の情報行）。pipe 形の残りは、O41 / D61 G1 の「標準入力は FS_WRITE の情報行で上界をとる」という扱いと同じ帰結になる。pipe 形をインタプリタとして判定できるようにするのは R3-r2-1（別の単位。定数 Str の畳み込み）の範囲。R4-r1-1 / R4-r1-9 / R4-r3-3 / R1-r1-9 / R1-r3-6 は列の要素や tail の問題で、この分岐には触れない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。影響するのは D1 / D2 で、3 者とも low にした理由は書き方のまれさ（corpus で直接渡す形が 0 件）。「D3 / D4 だけなら low」を理由にはしていない。
- **推奨の理由**: 推奨の基準では、fix には重大度 high か medium が要る。この単位は 3 者とも low で、直接渡す形は corpus で 0 件の、まれな書き方にあたる。そのため「low でまれな書き方」として限界に記録することを推奨する。記録には、変数を経由する形のまれさが未測定であることと、pipe 形は R3-r2-1 に依存することを書き添える。一方で、直し方は一般に正しいもの（先頭から続く定数 part をつないでから空白を見る規則）が見つかっており、検証役が実装して対照が壊れないことを確かめている。変更も 1 関数（サイズ S）で済み、語彙の追加は要らず、解決率も上げない（射影を変えるだけで、矛が増える向きにしか動かない）。D62 の帰結 2 のとおり、再凍結の前に authgap/ をどのみち触るので、他の fix とまとめて入れる判断も学生は取れる。その場合は、上の反例 a / b / c のテストと Windows 流の読み方の明記を必ず入れる。
- **所見**:
  - R3-r4-2: 代表で、唯一の所見。文字列の args の argv0 が定数の接頭辞になり、D1 / D2 が 矛 spawn_model から 不 spawn_command に落ちる（subprocess.run / check_output / Popen / call、pty.spawn）。3 観点とも生き延び、実行では 45 行が再現した。同じ所見に含まれる pipe 形（D2 が 矛 exec から 不 fs_unknown になる）は、この単位の直し方では直らず R3-r2-1 に依存するので、直す場合も記録に回る部分として扱う。（`_first_element` が `Str`（連結した文字列）に対して `parts[0]` を返すので、shell=False で**文字列**（列ではない）を args に渡す `subprocess.run("/usr/bin/"）

### U29 git.cmd.Git の proxy 行（method *）が全メソッドに当たる（段階 C・重大度 低・推奨 限界として記録）

GitPython の `repo.git.<名前>(...)` は、どんな名前で呼んでも「git コマンドを 1 回起動する」と読む表の行（method `*`、起動するプログラムの名前 argv0 は定数 'git'）が 1 本だけあり、全メソッドに当たる。このため 2 つの向きで誤る。(1) `repo.git.execute(cmd)` や `execute("git log " + args, shell=True)` は、モデルが決めたコマンドをそのまま実行する。それでも argv0 を 'git' とみなすので、本来の「矛」（宣言と実際の動きの食い違い）が「不」（判定できない）になり、見逃す向き（誤 clear）に倒れる。(2) `custom_environment` / `update_environment` / `clear_cache` などは子プロセスを起こさない。それでも「git を起動する」行を作るので、環境変数を設定するだけの readOnly ツールが「内」でなく「不」になる（誤警報の向き。矛は増えない）。

- **宣言**: D1 / D2　**向き**: 混在　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 要　**scripts/ だけで直る**: いいえ
- **根本原因**: `git.cmd.Git` の proxy 行が method `*` で全メソッドに当たり argv0 に 'git' 定数を注入するので、実際の argv と `shell=` を持つ `Git.execute(command, shell=…)` ではモデルが決めたコマンドを捨てて 不 にし、子プロセスを起こさない `custom_environment` / `update_environment` / `clear_cache` などには SPAWN 行を捏造する（execute 専用の行と除外メソッドが無い）。
- **コードの場所**: authgap/catalog/sinks.py:455-463 git.cmd.Git の ProxyRow, authgap/effects.py:703-728 _proxy / _from_proxy_row（argv0 の注入）
- **重大度の根拠**: 両方の所見で、探索役・設計・一般性の 3 意見がどれも low（review_rows.json の severities = [low, low, low]）。理由は頻度と向き。R4-r3-4 は、コーパスの木の中に `.git.execute(` が 0 件（site-packages の GitPython 自身を除く。探索役と一般性の検証役が数えた）。R4-r4-5 は「内 → 不」の向きで矛の数を変えない。単位ごとの判定が変わるのは、git コマンドを 1 つも起動せず環境だけを触るツールに限られる（その件数は未測定）。影響は D1+D2 で、旧文言「D3 / D4 だけなら low」とは関係なく決まった重大度なので、戻すものは無い。
- **直し方（一般に正しいか: 条件つきである）**: 直すなら 2 つに分ける（どちらも authgap/catalog/sinks.py の git.cmd.Git の ProxyRow と、authgap/effects.py の _proxy / _from_proxy_row）。
(A) R4-r3-4（execute）: `execute` 専用の行を `*` 行より先に当てる。束縛は argv0 ← A(0,"elem0")、argv[*] ← A(0)。`shell=` キーワードは subprocess の行の exec_mode_kw と同じ扱いにし、True のときは shell_string ← A(0)。effects.py:725-728 の 'git' 定数の注入は `*` 行（`__getattr__` 形のサブコマンド）だけに限り、execute では行わない。
守るもの（一般性の検証役が擬似的に直して確かめた）: `execute(["git"] + args)` と `execute(["git", "log", branch])` は argv0 = 'git' 定数のまま SPAWN_CONST_ARGV（不）に留まる。`repo.git.log(branch)` など `__getattr__` 形も今までどおり 'git' 定数になる。この確認では、今正しい結果が壊れる反例は見つからなかった。
(B) R4-r4-5（起動しないメソッド）: ProxyRow に exclude_methods を足し、git.cmd.Git の行から、名前を挙げた公開の非起動メソッドだけを除く。除く名前は custom_environment / update_environment / clear_cache / set_persistent_git_options / transform_kwargs / transform_kwarg / environment / polish_url / check_unsafe_protocols / check_unsafe_options。
**素朴な直し方で壊れる反例（一般性の検証役）**: 探索役の fix_sketch にある「`_` で始まる名前を一括で除外」は入れない。`_call_process` と `_get_persistent_cmd` はクラスに明示されたメソッドで、子プロセスを起こす。`repo.git._call_process("rm", path)` は今、argv[*] = MODEL の SPAWN 行を正しく出しており、`_` の規則を入れるとこの行が消えて誤 clear になる。`__getattr__` が `_` の名前を除くのは「定義されていない `_` の名前をコマンドにしない」という意味で、「`_` のメソッドは起動しない」という意味ではない。
**避ける条件**: 除外は明示的に名前を挙げたものだけにする。refresh / execute / stream_object_data / get_object_header / get_object_data は起動するので残す。GitPython は venv に入っていないので、メソッドの一覧は検証役の API の知識によるもの。直すなら、インストールした版で dir(git.cmd.Git) と照合する。custom_environment(GIT_SSH_COMMAND=MODEL) は、今の行でも env slot を持たないので、除外しても失う情報は無い（with の中の git コマンドの行は残る）。
手順: (B) は効果の行を消す向きなので、scripts/diff_effects.py と scripts/compare_scans.py で消えた行を 1 件ずつ確かめる。凍結済みの Def 3(b) の行を変えることになるので、CLAUDE.md 規則 6 に従い、仕様書の値（argv0 ← "git", shell ← False）とライブラリの仕様を decisions.md に並べて書く。preregistration.md には逸脱として記録し、解析器の指紋（fingerprint.json）を取り直す。
- **記録済みの限界・決定との重なり**: 設計の観点は 2 件とも「仕様どおり」として反証した（R4-r3-4 は確信度 0.65、R4-r4-5 は 0.6）。仕様書 Def 3(b)（AUTHGAP_BRIEF_v3.md:228）は `git.Repo(p).git.*` / `git.cmd.Git.*` → SPAWN { argv0 ← "git", argv[*] ← *args, cwd ← p, shell ← False } と、method を `*` にして argv0 を定数と明記している。proxy 行の slot 束縛は月 3 の sink 語彙の凍結に含まれる（同 841 行）。したがって、今の出力は凍結した規則どおりになる。設計の検証役は、O39（凍結した語彙が実際の API より粗いことによる限界）と同じ扱いで、既知の限界（O42 以降）に 2 件並べて書くことを勧めている。ただし 2 件とも迷いを書いている。仕様の `*` は `__getattr__` 形（A1 の `repo.git.checkout`）を想定して書かれたと読めるので、「語彙の追加」ではなく「語彙にある行の当てすぎ」とも読める。一般性の観点（反証せず）は後者の立場で、「sink 語彙の追加ではなく既存の行の束縛の訂正」とした。review_plan §2 は「sink 語彙の追加」を対象外とする一方、「語彙にある sink が当たらない」は対象としている。今回の「当たりすぎ」はそのどちらとも言える境界にある。§5 の既知の問題（O35 argv の分解、O39、O41）とは重ならない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。2 件とも影響は D1+D2 で、重大度 low の理由は頻度（木の中の `.git.execute(` 0 件）と向き（内 → 不で矛は動かない）。D3 / D4 だけだから下げた形跡は無い。
- **推奨の理由**: 3 つの意見がどれも low で、頻度も低い（木の中の `.git.execute(` 0 件）。設計の観点は 2 件とも「凍結した仕様 Def 3(b) どおり」と判定しており、直すには月 3 凍結の proxy 行（sink 語彙）の束縛を変える必要がある。つまり execute 行を足し、`*` から除外名を切り出すことになる。推奨の基準の「記録済みの限界・仕様どおり」「語彙の変更が要る」「low でまれ」にそろって当たるので、O39 と並べて限界として記録する。記録の中身: 誤 clear の向き（execute / shell=True のモデルのコマンドを見逃す）と、誤警報の向き（起動しないメソッドで不が増える）を分けて書く。仕様書の値とライブラリの仕様を併記する。直し方は一般に存在する（条件つき）ことも添える。学生が仕様の `*` を「`__getattr__` 形の意図」と読んで直すと決めた場合は、fix_outline の条件（`_` の一括除外をしない、名前は dir(git.cmd.Git) で照合、["git"]+args は定数のまま）を守る。そのうえで逸脱として preregistration に記録し、変更の小ささ（M）で直せる。
- **所見**:
  - R4-r3-4: 代表。誤 clear の向き。`Git.execute(command, shell=…)` で、モデルが決めた argv0 / shell_string が捨てられ、矛が不になる。実行の観点で再現した（21/21 行）。一般性の観点は反証せず、execute だけを直す擬似修正で反例なしを確かめた。設計の観点は仕様どおりとして反証（確信度 0.65）。3 意見とも low。（`git.cmd.Git` の proxy 行（method `*`、argv0 ← 'git' 定数）が GitPython の `Git.execute(command, ..., shell=)` にも当たり、実際の argv（com）
  - R4-r4-5: 同じ原因（method `*`）の別の表れで、向きは逆（誤警報、内 → 不。矛は動かない）。子プロセスを起こさない custom_environment / update_environment / clear_cache などに SPAWN 行を作る。実行の観点で再現した（19/19 行）。一般性の観点は反証しなかったが、fix_sketch の『`_` で始まる名前を除外』は `_call_process` を消して誤 clear になるという反例を出した。設計の観点は R4-r3-4 と同じ理由で反証（確信度 0.6）。3 意見とも low。（`git.cmd.Git` の proxy 行（method `*`）が GitPython の**子プロセスを起こさない**明示メソッド（`custom_environment` の with 文 / `update_environmen）

### U31 sqlalchemy.text と execute の 2 組（段階 C・重大度 低・推奨 限界として記録）

`stmt = text("DELETE …")` のように SQL の文を先に作り、あとで `conn.execute(stmt)` で実行する書き方（`conn.execute(text("DELETE …"))` のように 1 行で書いても同じ）では、解析器が 1 つの SQL を「文を作った所（text）」と「実行した所（execute）」の 2 つの効果として数えます。text 側は文が読めるので矛盾 / 宣言内と判定されますが、execute 側は text() が返すものの中身を解析器が追えないので「SQL が読めない → 不明（db_sql_unreadable）」になります。その結果、読めている文に余計な「不明」が 1 組付き、本文で必ず併記する不明の件数が多めに出ます（矛盾の件数は増えないので、主指標が誤って増える向きではありません）。

- **宣言**: D1 / D2 / tooling　**向き**: 誤警報　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: `sqlalchemy.text(s)` の戻り値が文（SQL）を運ばない（TextClause の値が無い）ので、別の文で作った `stmt` を `execute(stmt)` すると `text` 行は文を読んで 矛 / 内 になり、`execute` 行は sql が読めず 不（`db_sql_unreadable`）になる。同じ文が構築点と実行点の 2 組の判定になり、不の件数が水増しされる。
- **コードの場所**: authgap/catalog/sinks.py:410 sqlalchemy.text 行, authgap/dparse.py:376-377 _db の unreadable, scripts/contradiction_by_decl.py:46 不の集計
- **重大度の根拠**: 3 観点とも low（探索役 low、設計の観点 low、一般性の観点 low）。実行の観点で再現済み（主張した 7 行を 7 行とも再現）。影響は「不」の件数だけで、矛（D1 + D2 の主指標）は動かない。一般性の観点の再計測（scan_v2_run20、contradiction_by_decl.load_reasons の組で数えた値）: db_sql_unreadable を理由に持つ組は D1 25 / D2 6 = 31 組、そのうち同じユニットに sqlalchemy.text の組があるのは 2 組（redhat-ai-americas/memory-hub の memory / search_memory）だけで、その 2 つの text 組自体も不（db_unknown_statement）。「読めている文に余分な不が 1 組立つ」形は run20 で 0 件。探索役の件数（132 組のうち 34 組）は再計測で一致せず過大。旧文言「D3 / D4 だけなら low」による格下げではない（効くのは D1 / D2 の不の列で、low の理由は影響が不の件数だけであることと実測の少なさ）ので、重大度を戻す必要は無い。最終評価の新しいデータでの件数は未測定。
- **直し方（一般に正しいか: 無い）**: 素朴な直し方はどちらも一般に正しくない（一般性の観点）。
(a) val エンジンで `sqlalchemy.text(s)` の戻り値を `Obj(classes={"sqlalchemy.TextClause"}, fields={"sql": s})` にし、DB proxy 行（execute）の sql slot が Obj なら fields["sql"] を読む — 反例: インラインの `conn.execute(text("DELETE …"))` で text 行と execute 行の両方が矛になり、同じ文が主指標（矛）に 2 組入る。`conn.exec_driver_sql("DELETE …")` なら 1 組なので数が揃わず、水増しが「不」から主指標の「矛」に移る（設計の観点も同じ欠点を指摘）。
(b) 集計側（scripts/contradiction_by_decl.py）で、同じユニットに sqlalchemy.text の効果があるときの execute 行の db_sql_unreadable を不に数えない — 反例: 同じユニット内にある、本当に読めない別の execute まで隠す（探索役自身が認める）。manifest の行には text 行と execute 行の対応（どの text がどの execute に渡ったか）が無いので、scripts/ だけでは正しく直せない。
一般に正しいと考えられる形: (a) で execute 行に SQL を渡し、かつ「DB proxy 行に消費された text() の行」を独立に判定しない（text 行を execute 行に寄せる、または逆）。避ける条件: (1) 受け手が解けない `session.execute(text(query))`（較正対 A18 の langroid、corpus/A18__vuln/langroid/agent/special/sql/sql_chat_agent.py:474）では text 行が唯一の行なので、消費されたと確かめられないときは text 行を消さない（A18 の効果行に触れるので diff_effects.py で確かめる）。(2) モジュール水準の `PURGE = text("DELETE …")` を execute する形は今は text 行がユニットに入らず execute の不だけなので、(a) で不 → 矛になる（改善だが解決率を上げる向き）。(3) opaque → resolved の変更なので CLAUDE.md の敵対的レビューが要る。どれも authgap/（sinks.py の text 行、val エンジン、dparse.py の _db）の変更で、凍結の指紋に触れる。
- **記録済みの限界・決定との重なり**: text() を別の sink（「生 SQL の構築点。実行は proxy 側」、authgap/catalog/sinks.py:410-414、required_by A18）にしたのは意図した設計で、効果ごとの判定（§7.1「SQL が読めない → 不」、docs/contradiction_principles.md:172）も規則どおり。ただし 1 つの文が 2 組になり不が水増しされることを意図・記録したものは decisions.md / open_questions.md / contradiction_principles.md に無い（設計の観点は反証せず、refuted = false）。review_plan.md §5 の既知の問題とも重ならない。集計単位 (木, ユニット, site, kind)（contradiction_by_decl.py:11）は compare_scans.py と共通の設計。所見が提案する (b) の範囲は R5（集計）と重なる。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。検証役 2 者の low の理由は「影響が不の件数だけで主指標の矛は動かない」「run20 で高々 2 組、読めている文への余分な不は 0 件」で、D3 / D4 の旧文言は使われていない（この単位は D1 / D2 に効く）。
- **推奨の理由**: 重大度は low で、run20 では実害の形（読めている文への余分な不）が 0 件。所見の 2 つの直し方はどちらも一般に正しくない（(a) は水増しを主指標の矛に移し、(b) は本当に読めない execute を隠す）。一般に正しい形（execute に SQL を渡し、消費された text 行を寄せる）は authgap/ の変更で凍結の指紋に触れ、sink 行を消すので較正対 A18 に触れ、解決率を上げる向きなので敵対的レビューも要る。scripts/ だけでは行の対応が取れず正しく直せない。凍結直前に入れる根拠は弱いので、「text() を経由する SQL は構築点と実行点の 2 組になり、実行点が不（db_sql_unreadable）として数えられる。不の件数はその分多めに出うる（矛は増えない）」を限界として docs/open_questions.md などに記録することを推す（一般性の観点の推奨と同じ）。決めるのは学生。
- **所見**:
  - R3-r1-8: 代表（この単位の唯一の所見）。3 観点を生き延び、実行の観点で 7/7 行再現。設計の観点は反証せず（fix_is_general = true、ただし (a) は矛を水増しすると注記）、一般性の観点は反証せず fix_is_general = false・限界として記録を推奨。件数は再計測で 31 組中 2 組、余分な不 0 件（探索役の 132 / 34 は過大）。（`sqlalchemy.text("DELETE …")` を別の文で作って `execute(stmt)` すると、1 つの文が `text` 行の矛と `execute` 行の不（`db_sql_unreadable`）の 2 組になり）

### U32 効果行の重複（ループ 2 周と中間関数の複数呼び出しで、中身がまったく同じ行が manifest に何本も出る）（段階 A・重大度 低・推奨 限界として記録）

解析器はループの本体を 2 回なぞって値を落ち着かせる（2 周の固定点）。そのたびに危険な呼び出し（sink）を効果行として記録し、既に同じ行があるかを確かめないので、for の中の os.remove は 2 行、二重ループなら 4 行と、中身がバイト単位で同じ行が出る。同じ関数を 2 回呼ぶ中間の関数（_rm_twice が _rm を 2 回呼ぶ形）を経由した場合も同じことが起きる。判定の鍵（木, ユニット, site, kind）と CONTRADICTION の数（run20 で 191）は変わらないが、行を数える集計（compare_scans の「効果」、summary の rows / verdict 行、catalog_map の深さ分布）は大きくなる方向にずれる。run20 では効果 8,337 行のうち 3,876 行（46%）が完全な重複だった。

- **宣言**: tooling　**向き**: 数え落とし　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: ループ本体の 2 周の固定点と、中間の被呼び出しを複数の呼び出し箇所から降りるたびに `on_call` が同じ効果を積むので、バイト同一の効果行が manifest に重複して出る。行単位の件数（compare_scans の「効果」、summary の rows / verdict 集計、run20 の 8,337 行のうち 3,876 行）が膨らむ（判定の鍵 (木, ユニット, site, kind) には効かない）。
- **コードの場所**: authgap/val/engine.py:408-427 _exec_loop（2 周）, authgap/effects.py:562 EffectExtractor.on_call, authgap/analyze.py:209 report.effects, scripts/compare_scans.py:56 / scripts/scan_v2.py:75 行の集計
- **重大度の根拠**: 3 観点の意見は探索 medium / 設計 low / 一般性 medium。この単位では low とする。理由: (1) 主指標 D1〜D4 の判定はユニット × site × kind で数えるので、重複を除いても CONTRADICTION は 191 → 191 で変わらない（一般性の検証役が run20 で実測）。contradiction_by_decl.py:46 の鍵も intersection_rows.py:80 の集合も影響を受けない。(2) 最終評価の単位（population_v3.md §35 の V2 = (木, ユニット, site, kind, 宣言)、V3 = ユニット）と two_sided の経路集合も影響を受けない。(3) 行が膨らむのは行単位の件数だけで、D15 は行単位の値を「併記」と決め、O18 (c) は行単位の指標を本文で使わない選択肢を挙げている。一方で medium の意見の根拠は、docs/catalog_map.md:36 の深さ分布（4 段 784 → 重複を除くと 182 で 4.3 倍）、行単位の resolved 率 12.3% → 16.2%、verdict 行 16,268 → 一意 6,952、review_plan §6 の基準点「効果 8,337」が生の行数であることで、これらは説明の数字を誤らせうる（review_plan §1 (c)）。そのため low でも「行単位の数値には重複が入っている」という注記は要る。旧文言「D3 / D4 だけなら low」による引き下げは無い（設計観点の low は、D1 / D2 の判定に効かないことと既に記録されていることが理由）。
- **直し方（一般に正しいか: 条件つきである）**: 一般に正しい直し方は「完全に同じ行だけを 1 本に畳む」こと。効果を正規化した JSON（to_json の全項目: kind / site / form / lineno / relpath / entry_lineno / slots / chain / resolution …。json.dumps(sort_keys=True)）が既に出ていれば追加しない。決定論的な順序で最初の行を残す。置き場所の候補は 2 つある。(A) 集計側（scripts/ だけ。凍結の指紋に触れない。O18 (b) に近い）: compare_scans.py:56 の n_effects、scan_v2.py:75 の _tally の rows / verdicts、catalog_map.py:167-185 の exercised_sinks / 深さ分布で、生の行数と一意の行数を両方出す。(B) 解析器側: analyze.py:209 で report.effects を作るとき（または EffectExtractor.on_call）に既出の行を除く。db_unresolved も同じ仕組みで膨らむので一緒に畳む。

守ること（検証役が見つけた条件と反例）:
1. 畳む鍵は完全な正規化 JSON にする。(site, kind) や (site, slot) のような粗い鍵にしない。粗い鍵だと、経路（entry_lineno / chain）や slot の確度が違う行（opaque の行と resolved の行）が 1 本になり、D15 の合流（opaque > remote > resolved）で opaque が消えて false-clean になりうる。凍結済み fixture の件数の期待（fixtures/val/expected.json:85 F3 = shell が不明な argv / shell の 2 行、:149 F6 = SPAWN + EXEC@pipe、:171 F7 = 経路ごとの複製。tests/test_val_fixtures.py:62-72 で KNOWN_UNMET）は、どれも slot か経路の鍵が違う行なので、完全一致で畳めば動かない。粗い鍵だと動く。
2. 「ループの 1 周目だけ on_call を止める」案は採らない。1 周目と 2 周目で値が違うとき（widening の前後）の扱いや、spawn_handles / db_unresolved の副作用と絡むので、報告の段で畳む方が安全（探索役・一般性の検証役とも同じ意見）。
3. 境界の例 ce8_sameline（同じ文の中で `_rm(path); _rm(path)`、または `_rm(path) or _rm(path)`）は entry_lineno も chain も同じなので 1 本になる。Def 3 では効果は (kind, site, slots) の集合なので、これは同じ効果であり反証にはならない。ただし「呼び出しの回数」を数えたい人には見えなくなることを記録する。
4. 解析器側 (B) で直すと、解析器の出力と基準点「効果 8,337」がおよそ 46% 減る。その場合は preregistration に逸脱として記録し、compare_scans で「消えたユニット 0 / 消えた CONTRADICTION 0」を確かめてから再凍結する。D15 は結果を見る前に固定した決定なので、行単位とサイト単位のどちらを主に使うかは選び直さない（行単位は併記のまま）。
5. 直さない場合も、docs/catalog_map.md:36 の深さ分布と D15 の併記値（行単位の解決率）に「バイト同一の複製を含む」と注記する。O18 には run20 の定量（完全重複 3,876 / 8,337、重複を含むユニット 1,057、うち少なくとも 2,094 行は entry 行か sink 行がループの中）を追記する。
- **記録済みの限界・決定との重なり**: 設計の観点は「記録済みの限界の再発見」として反証した（refuted = true、信頼度 0.8）。根拠: 仕様書 §2.6（AUTHGAP_BRIEF_v3.md:520「指数項は出力側に現れる — 効果行は呼び出し点ごとに複製される」）、D15（decisions.md:1449-1464。関門をサイト単位 (木, relpath, lineno, kind) で数え、行単位は併記）、O18（open_questions.md:391-407。複製で行数の指標が膨らむ。案 (b)「行を (site, slot, chain) で畳む」が学生の決定待ち）。O18 は review_plan.md §5「既知の問題（再発見しても所見にしない）」に付録側として載っている。さらに第 1 の機構（ループ 2 周で on_call が 2 回発火し、重複を除かない）は f0a_checks.md:179,232,253,591 で仕組みまで特定したうえで「D15 のサイト単位では無害、行単位では過大計上」と判定済みで、D17 の「直す」表にも入っていない。一般性の観点はこれに反対し、§2.6 / O18 が言う複製は「経路（entry_lineno / chain）が違う行」の話で、バイト同一の複製（2 周目の出力と、中間関数の同じ呼び出しの重複）は別の仕組みであり記録されていない、とした。本記録者の判断: 行数が膨らむという帰結は O18 / D15 / f0a_checks の範囲に入っている。新しいのは run20 での定量と、基準点 8,337・catalog_map.md:36 の深さ分布が生の行数だという指摘で、これは O18 への追記に当たる。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。設計の観点が low とした理由は「D1 / D2 の判定（ユニット × site × kind）にも two_sided の経路集合にも効かず、行単位の件数の膨張は D15 / O18 に明記済み」であり、影響先は tooling。「D3 / D4 だけなら low」の旧文言は理由に使われていない。
- **推奨の理由**: 設計の観点が、記録済みの限界（§2.6 / D15 / O18。O18 は review_plan §5 の既知の問題）の再発見と判定した。最終評価の単位（V2 / V3、two_sided の経路集合、CONTRADICTION 191）は重複を除いても変わらない（実測）。そのため最終評価の経路で数字を壊すものではなく、解析器（authgap/）を変えて基準点を 46% 動かす理由は弱い。推奨は次のとおり。(1) O18 に run20 の定量（3,876 / 8,337、重複を含むユニット 1,057、少なくとも 2,094 行がループ起因）とバイト同一の 2 つの仕組みを追記する。(2) docs/catalog_map.md:36 の深さ分布と D15 の行単位の併記値に「複製を含む」と注記する。学生が行単位の数字も本文で使うと決めるなら、scripts/ だけで一意の件数を併記する直し方（完全一致の正規化 JSON で畳む。凍結の指紋に触れない、大きさ S）は安全なので、そのときは fix に切り替えてよい。
- **所見**:
  - R4-r1-8: 代表（唯一の所見）。ループ 2 周の固定点と中間関数の複数呼び出しで、バイト同一の効果行が出る。run20 で 3,876 / 8,337 行が重複（探索役と一般性の検証役が独立に数えて一致）。設計の観点は O18 / D15 / §2.6 の再発見として反証（low）、一般性の観点は別の仕組みとして生存（medium、反例は作れず、境界例 ce8_sameline のみ）。（ループ本体（2 周固定点）と中間の被呼び出しの複数呼び出し箇所で、バイト同一の効果行が重複して出力され、行単位の件数（compare_scans の「効果」、summary の rows / verdict 集計、review_plan §）

### U34 DB の分類から判定・理由への写像（段階 A・重大度 低・推奨 直す）

この単位は、SQL 文の種類からツールの宣言との判定（矛盾・不明・宣言内）とその理由を決める部分の誤り 2 つです。(1) idempotentHint: true（D4）の規則表 §7.4 は、分類に無い先頭語（NOTIFY / CALL / COPY / UPSERT / ATTACH）を「宣言内」にしています。一方、同じ文書の §7.5、原理 2-a、D1 / D2 の表はどれもこれを「不明」としており、§7.4 だけが食い違っています。そのため D4 だけで不明が数え落とされ、呼ぶたびに効果が増える NOTIFY や COPY まで問題なしと扱われます（誤 clear 寄り）。(2) `"DELETE FROM t WHERE a = " + x` のように、モデルが中身を選べる値を変更の文につないだ SQL では、判定（矛盾）は正しいのに、理由が「モデル由来」の `db_model_sql` になります。感度分析 3-b は理由の文字列に model を含む矛盾を不明に倒すので、定数の DELETE だけで矛盾と決まるこの形も不明に落ち、3-b の行が少なく数えられます。

- **宣言**: D4 / D1 / D2 / tooling　**向き**: 混在　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: dparse の DB 分岐が SQL の分類から（判定, 理由）を作るときに規則と食い違う: `_db` は選べる（MODEL かつ resolved）連結 SQL の接頭辞が変更の文（`"DELETE … " + x`）でも理由を `db_model_sql` にするので感度分析 3-b が「model を含む理由」として 矛 → 不に倒し、`_d4` は §7.4 の「DB: それ以外の先頭語 → 内」を文言どおり実装して、§7.5 / 原理 2-a では 不 になる分類に無い先頭語（NOTIFY / CALL / COPY / UPSERT / ATTACH）を 内 にする（§7.4 の行自体が §7.5 と矛盾）。
- **コードの場所**: authgap/dparse.py:360-384 _db（chosen 分岐の理由）, authgap/dparse.py:408-430 _d4 の DB 分岐, authgap/catalog/statements.py:22 SQL_NONIDEMPOTENT_HEADS, docs/contradiction_principles.md:223 §7.4 / :245 §7.5, scripts/contradiction_by_decl.py:66 感度分析 3-b
- **重大度の根拠**: 2 件とも、探索役と検証役 2 観点のすべてが low と判定した（review_findings.md の「低（低 / 低 / 低）」）。
R1d-r6-5 は D62 の後の文言で検証された（設計の観点が「D62 で D4 は主指標」と明記している）。low にした理由は「MCP ツールで CALL / COPY / NOTIFY はまれ」だけで、D4 だけに効くことは理由になっていない。
R3-r1-7 の影響は評価の道具（3-b の行）だけで、採った原理での件数は変わらない。run20 には `db_model_sql` の行が 0 件なので、v2 の数字も動かない（検証役が manifest で確認）。
新しいデータで何件に効くかは未測定。run20 で D4 が付いた DB の行のうち分類に無い先頭語を持つものの件数も未測定。
向きは、R1d-r6-5 が 不 → 内 の数え落としで、NOTIFY / COPY では誤 clear になる。R3-r1-7 は感度分析の過小計上。
- **直し方（一般に正しいか: 条件つきである）**: 共通: どちらも規則の文書（docs/contradiction_principles.md）を先に直してコミットし、その後に実装を直す（§9 / D57 と同じ順序）。§7 は実装より前に固定したものなので、docs/preregistration.md に逸脱として書く。authgap/ を変えるので指紋が変わる。D62 の帰結 2 で予定している再凍結の前に、1 つのコミットにまとめる。v2 / v3 の件数を見て規則を決めない（D61）。

■ R1d-r6-5（D4 で分類に無い先頭語）
1. §7.4 の DB の行を次のように直す: 「先頭語が分類（§7.5 の読み取り / 接続単位 / SQL_MODIFY_HEADS / SQL_PERSISTENT）に無い → 不 `db_unknown_statement`」。DELETE / DROP / CREATE / ALTER / TRUNCATE、永続・接続単位・読み取りの文は 内 のまま。
2. `_d4` の DB 分岐で、`head in SQL_NONIDEMPOTENT_HEADS` を見た直後に `if sql_class(text, complete) == SQL_CLASS_UNKNOWN: return CONTRA_UNKNOWN, "db_unknown_statement"` を足す。`_db` と同じ分類器を使う。`complete` は必ず渡す（接頭辞だけの文を全文として分類しないため）。
- 素朴な直し方で壊れるもの: 「SQL_NONIDEMPOTENT_HEADS にも SQL_DESTRUCTIVE_HEADS にも無ければ 不」とすると、SELECT / SET / BEGIN などが誤って 不 になる。必ず `sql_class` が UNKNOWN かどうかで判定する。
- 検証役が確かめた副作用: 分類に無い PRAGMA の代入（`PRAGMA wal_autocheckpoint = 1000`）と GRANT は、実際には冪等なのに 内 → 不 に移る。これは不明の側への移動で、誤った 矛 は生まない。§7.5 の「分類に無い PRAGMA → 不」と D2 の扱いとも合う。
- より狭い案: 「PRAGMA の代入は同じ値を入れ直すだけなので冪等」という D4 の規則を導いて PRAGMA は 内 に残し、PRAGMA 以外（NOTIFY / CALL / COPY / ATTACH / UPSERT / GRANT …）だけを 不 にする。この案を採るなら、その理由を §7.4 に書く。
- テスト: d4heads の 5 件は 不 `db_unknown_statement`。対照の DELETE / `CREATE TABLE IF NOT EXISTS` / VACUUM / `PRAGMA foreign_keys = ON` / SELECT は 内 のまま。
- 別の問題（この単位ではない）: 再現の中で d4_attach は sqlite の `db()` を呼んでいるのに、`psycopg.Cursor.execute` の site に解決されている。受け手の解決の問題なので、別に扱う。

■ R3-r1-7（chosen の変更文接頭辞の理由）
1. §9.4 の 2 の「確度 resolved → 矛 `db_model_sql`」に次の但し書きを足す: 「接頭辞の先頭語が変更の文（その宣言の modify_heads）なら理由は `db_modify`（注入の有無によらず変更する）」。
2. `_db` の chosen 分岐を `return (CONTRA, "db_modify") if head in modify_heads else (CONTRA, "db_model_sql")` にする。verdict は変わらず、変わるのは理由の文字列だけ。
- 検証役が探した反例（どれも今の正しい結果を壊さない）:
  - SELECT 接頭辞 + chosen は `db_model_sql` のまま（3-b で 不。influenced の SELECT の `db_sql_model_opaque` = 不 と揃う）。
  - D2 の INSERT 接頭辞 + chosen は、INSERT が D2 の modify_heads（SQL_DESTRUCTIVE_HEADS）に無いので `db_model_sql` のまま。
  - `"DELETE" + x` のように最初の語の後に空白が無い形は先頭語が決まらないので、今のまま。
  - `db_model_sql` を読むのは contradiction_by_decl.py の 3-b だけで、既存テスト（tests/test_fix_o30_o32_o33.py の SELECT / 不完全 / PRAGMA の接頭辞 4 件）は影響を受けない。
- 別案として新しい理由コード（例: `db_model_sql_modify`）を作る場合、名前に `model` を含めてはいけない。apply_flip が部分文字列で 3-b に倒すため。
- scripts/ だけでは直せない。注記に接頭辞の先頭語が残っていないため（検証役の指摘）。
- 未確認: 接頭辞が永続の類（`"VACUUM " + x` など）の chosen 形も、3-b では同じ理屈で `db_persistent` が期待になりうる。探索役の案はこれを扱っておらず、検証もしていない。
- **記録済みの限界・決定との重なり**: review_plan.md §5 の既知の問題にも、decisions.md（D56 / D57 / D61〜D63）にも、open_questions.md にも、この 2 つは意図・限界として記録されていない（2 件とも設計の観点が grep で確認）。
- R1d-r6-5 は §7.4 の行を文言どおり実装した結果だが、§7.4 の行自体が同じ文書の §7.5「それ以外（ATTACH / NOTIFY / 分類に無い PRAGMA など）→ 不」、§7.1 / §7.2「先頭語が分類に無い → 不」、原理 2-a、statements.py の docstring「ここに無いものは不明」と矛盾している。導出のときの書き落としであって、設計の決定ではない（設計の観点は反証せず）。§2 の「D3 / D4 は直さない」は §7.5（D62）で取り下げ済み。
- R3-r1-7 の verdict は §9.4 の 2 どおりで正しい。食い違っているのは、contradiction_by_decl.py の docstring「原理を反対側にしたときの結果は注記から正確に決まる」と、原理 3-b の定義（§3 :80）との間。§9.4 は理由コードを決めたときに 3-b での復元を考えていなかった（設計の観点は反証せず）。
設計の観点で反証された所見は無い。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。R1d-r6-5 は D62 の後の文言で検証された（verify_d3d4.json の設計の観点が「D62 で D4 は主指標、範囲外ではない」と明記している）。low の理由は頻度の低さだけ。R3-r1-7 は第 1 回（旧文言）で検証されたが、影響は tooling（D1 / D2 の 3-b の行）で D3 / D4 ではない。low の理由は「採った原理の件数が変わらない」と「run20 に db_model_sql が 0 件」で、旧文言は使われていない。
- **推奨の理由**: 基準を文字どおり当てると、2 件とも low でまれな書き方なので record_as_limitation になる。それでも fix を推す理由は次の 5 つ。
(1) D62 の帰結 2 で authgap/ の変更と再凍結がもともと予定されており、指紋が変わる追加の費用はほぼ無い。
(2) どちらも 1 分岐の局所変更（S）で、語彙を足さずに済む。`db_unknown_statement` と `db_modify` はどちらも既にある理由コード。検証役 2 観点とも fix_is_general = true で、誤った 矛 を生む反例は見つかっていない。
(3) R1d-r6-5 を限界として残すと、主指標になった D4 の規則表が同じ文書の §7.5 と矛盾したままになる。しかも向きは誤 clear 寄り（NOTIFY / COPY）。
(4) R3-r1-7 は論文に載せる感度分析 3-b の復元の主張（「注記から正確に決まる」）を崩している。証拠の強い chosen 形のほうが弱く数えられるという単調性の破れでもある。
(5) どちらも規則の文書を先に直すという既存の手順に乗る。
学生が再凍結の範囲を広げたくない場合、限界として記録するならそれぞれ 1 文で足りる。「§7.4 の DB 行は分類に無い先頭語を D4 で内とし、§7.5 と食い違う（不が欠ける）」と「3-b の行は chosen の変更文接頭辞を不に数える（過小）」。
- **所見**:
  - R1d-r6-5: 代表（D4 の判定の誤り）。§7.4 の「DB: それ以外の先頭語 → 内」が §7.5 と原理 2-a に反していて、`_d4` はその表を文言どおり実装している。NOTIFY / CALL / COPY / UPSERT / ATTACH が D4 で注記なしの 内 になる（D1 / D2 では 不）。3 観点とも生存、low。直し方は §7.4 を先に直し、`_d4` に sql_class が UNKNOWN なら 不 を足す。分類に無い PRAGMA の代入と GRANT が 不 に移る副作用あり。（§7.4 の「DB: それ以外の先頭語 → 内」が §7.5「それ以外（ATTACH / NOTIFY / 分類に無い PRAGMA など）→ 不」と原理 2-a に反し、`_d4` は表どおり `NOTIFY` / `CALL proc(）
  - R3-r1-7: 同じ `_db` / `_d4` の「分類 → (判定, 理由)」の写像の、別の表れ（D1 / D2 の理由コード → 感度分析の道具）。chosen の連結 SQL の接頭辞が変更の文でも理由が db_model_sql になり、3-b で 矛 → 不 に落ちる。verdict は正しく、影響は評価の道具だけ（run20 は 0 件）。3 観点とも生存、low。直し方は chosen 分岐で head が modify_heads にあれば db_modify にする。scripts/ だけでは直せない。（MODEL が選べる（resolved）連結 SQL の接頭辞が変更の文（`"DELETE … " + x`）でも理由を `db_model_sql` にするため、感度分析 3-b が「model を含む理由」として矛 → 不に倒し、3-b）

### U35 open の mode（a+ / x+）の破壊性（段階 C・重大度 低・推奨 限界として記録）

解析器は、ファイルを開くときのモード文字列に「+」（読み書き両用）が入っていると、それだけで「既存の内容を消す書き込み」とみなします（D32 の規則の文言どおりです）。そのため「destructiveHint: false」と宣言したツールが open(path, "a+") や "x+" を使うと、D2（destructiveHint）で矛盾（パスをモデルが選ぶ場合）や判定不能（パスが定数の場合）が出ます。所見は、これを誤警報とみなして「内（矛盾なし）」にすべきだと主張しています。ただし検証では、a+ でも truncate() による全体の書き直しに使える（よくある書き方）ことが実際に確かめられました。したがって誤警報と言えるのは x+ だけで、a+ は一部の書き方に限られます。

- **宣言**: D2　**向き**: 誤警報　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 要　**scripts/ だけで直る**: いいえ
- **根本原因**: `_mode_destructive`（D32）が `+` を含む mode を一律に上書き（destructive=True）とし、Python の `open` で既存の内容を消さない `a+`（追記）/ `x+`（新規作成）を区別しない（§7.2 の `open('w' / '+')` の文言も同じ）。規則（D32 / §7.2）の改訂が先に要る。
- **コードの場所**: authgap/effects.py:297-312 _mode_destructive, authgap/dparse.py:285 D2 の書き出し, docs/contradiction_principles.md:190 §7.2, docs/decisions.md:470 D32
- **重大度の根拠**: 3 観点とも low（探索役・設計・一般性）で、影響は D2 だけです。D3 / D4 だけに効くことを理由に下げた形跡はありません（そもそも D4 の fs_append の判定は正しく、影響しません）。件数は、一般性の観点が run20 で「+ を含む mode は a+b の 1 件だけで、x+ は 0 件」と数えています。a+b のその 1 件が truncate を伴うかどうかは未測定です。a+ は「追記しつつ読み返す」書き方と「読んで書き直す」書き方の両方に使われます。後者では今の矛盾（D2 矛）が正しい判定で、誤警報になるのは truncate しない単純な追記の a+ と x+ に限られます。
- **直し方（一般に正しいか: 条件つきである）**: 所見の直し方（fix_sketch）はこうです。_mode_destructive を「w を含む → True。そうでなく a か x を含む → False。そうでなく + を含む（r+）→ True」の順にし、D32 の規則本文と §7.2 の open('w' / '+') の文言を先に改訂します（規則 → テスト → 実装の順）。
【素朴な直し方で壊れる反例（一般性の観点、scratchpad/verify/R3_low_1/ce5）】次のような @mcp.tool(annotations={"destructiveHint": False}) のツールを考えます。open(os.path.join(ROOT, name), "a+") で開いて f.seek(0); json.load(f); f.seek(0); f.truncate(); json.dump(data, f) とする「無ければ作り、読んで、全体を書き直す」定型です。r+ だと無いときに失敗し、w+ だと読む前に消えるので、この定型には a+ が使われます。今は D2 矛（fs_writeout_model_path）で正しく判定されます。fix_sketch を当てると a+ → destructive=False → append → 内となり、新しい誤 clear が生まれます。truncate は O_APPEND と無関係に効きます。本記述者も Python で、既存の {"keep":"old"} が a+ 経由で {"n":2} に置き換わることを確かめました。解析器は truncate を sink に持たない（authgap/catalog/sinks.py）ので、この破壊性を捉えているのは mode の分類だけです。
【避ける条件】a+ を追記型にしてよいのは truncate や読み書きの流れを sink として見分けられるときだけです。それには sink 語彙の追加が要り、これは月 3 凍結の対象で添削の範囲外です。a と a+ の線引き（a は読めないので書き直しの定型にならない）は、言語の意味に根拠があります。
【一般に正しい部分】x+ だけを追記型にする直し方（「x を含み w を含まない → False」）は、Python の意味から一般に正しいです。x+ で既存のファイルを開くと FileExistsError になるので、上書きはできません（本記述者も確認済み）。ただし run20 では 0 件で影響はほぼ無く、D32 / §7.2 の規則の改訂と、凍結済み解析器（fingerprint）の変更が要ります。
【記録案】「a+ は書き直しの定型に使われるので書き出しとして扱う。truncate しない追記の a+ と x+ では D2 で過大（誤警報側）」を docs/open_questions.md の既知の限界に置きます。
- **記録済みの限界・決定との重なり**: 規則の文言どおりの実装です。D32（docs/decisions.md:470「mode に w または + を含めば True」）と §7.2（contradiction_principles.md:187「open('w' / '+')」= 書き出し）に一致しています。a+ / x+ をあえて上書き型にすると決めた記録は、設計の観点が探しても見つかりませんでした。D32 自身の分類原理（削除・上書き型か追記型か）から見ると導出の誤りとも読めますが、「意図された決定」とも読める余地があるので、設計の観点は refuted=false としています（expected_is_correct=false。今の規則では今の出力が規則どおり）。一般性の観点は、a+ について所見の前提（上書きできない）が Python の意味として誤りだとして refuted=true としました。review_plan §5 の既知の問題とは重なりません。D61 の「直さないもの」にある flock のための "a"（D4 の誤 1）は別の話です。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。影響は D2 だけで、3 観点とも low の根拠は「書き方がまれ」「規則どおり」「a+ の多くは書き直しの定型で正しく矛」です。旧文言「D3 / D4 だけなら low」は使われていません。
- **推奨の理由**: 理由は次の 3 つです。(1) a+ の部分は、一般性の観点が実行できる反例で反証しています。素朴に直すと、読んで書き直す定型で新しい誤 clear が生まれます。正しく区別するには truncate などの sink 語彙の追加が要り、これは凍結済みです。(2) 一般に正しい x+ の部分は low で、run20 では 0 件です。それでも規則（D32 / §7.2）の改訂と凍結済み解析器の変更が要り、fix の基準（high か medium）を満たしません。(3) 今の扱いは誤警報側（安全側）の過大であり、誤 clear ではありません。学生が x+ だけを規則の一般的な訂正として直すことを選ぶ余地はあります。その場合でも a+ は変えないことを条件にしてください。
- **所見**:
  - R3-r1-5: 代表で、唯一の所見です。実行では再現しました（8/8 行）。設計の観点は非反証（規則の文言どおりで、改訂の判断が要る）。一般性の観点は a+ について反証（truncate による書き直しの反例あり）で、x+ だけが主張どおりです（run20 で 0 件）。（`open(path, "a+")` / `"x+"` を「書き出し（上書き）」に分類する — Python の open では `a+` / `x+` は既存の内容を消せない追記型なので D2 で誤警報（path MODEL → 矛、pa）

### U37 §7.3 の private な名前の定義（段階 C・重大度 低・推奨 限界として記録）

D3（openWorldHint: false、「外の世界には出ない」という宣言）の規則 §7.3 は「宛先が localhost / private / loopback なら 内（宣言どおり）」としていますが、ホスト名について何を private とみなすかは書かれていません。実装の `_host_class` は `localhost`、`*.localhost`、`*.local` の 3 つの形だけを内側とし、それ以外の名前はすべて「外部ホスト」として扱います。そのため、標準で私用と決まっている名前（`host.docker.internal` や `api.internal`、`nas.home.arpa`）や、公開 DNS では引けない 1 語だけの名前（`http://ollama:11434`）を定数で呼ぶツールも 矛（宣言と食い違う）になります。誤りの向きは誤警報です。IP で書けば 内 になる宛先が、名前で書くと 矛 になるという食い違いもあります（`169.254.169.254` は 内、`metadata.google.internal` は 矛）。

- **宣言**: D3　**向き**: 誤警報　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: §7.3「宛先が localhost / private / loopback → 内」の private が名前について未定義のまま、`_host_class` が `localhost` / `*.localhost` / `*.local` の 3 形だけを local とし、それ以外の名前を無条件に external にするので、標準で私用と定まる名前（`*.internal` / `host.docker.internal`、`*.home.arpa`（RFC 8375）、公開 DNS で解決できない単一ラベル名 `ollama`）の定数の宛先が 矛 になる。規則の定義（学生の判断）が先に要る。
- **コードの場所**: authgap/dparse.py:274-280 _host_class の名前の判定, docs/contradiction_principles.md §7.3
- **重大度の根拠**: 探索役と、設計・一般性の 2 観点の検証役は、3 者とも low としました。理由は影響の小ささで、旧文言によるものではありません。設計の検証役によれば、v2 run13 の D3 net_external_host 37 件はすべて公開ホスト（kakao / feishu / pushover / dartmouth、decisions.md:3035）です。一般性の検証役も、run20 の該当行は 4 木にしか無く、主に公開サービスだと確かめています。どちらも「v2 の件数はたぶん変わらない」という判断です。corpus/ 全体の文字列リテラルの数（`http://gw:` 375、`http://host.docker.internal` 44 など）はテストや vendored のコードを含む上限で、どの検証役も確かめていません（ツール宛先としての実数は未測定）。D62 で D3 は主指標になったので、D3 の精度の問題として数えます。
- **直し方（一般に正しいか: 条件つきである）**: 【順序の条件（必須）】名前についての「private」の定義は学生が決めます。まずそれを §7.3 に書いてコミットし、その後で実装を変えます（CLAUDE.md 規則 6、review_plan §4.3）。件数を見て決めないこと（D61）。
【一般に正しい直し方（一般性の検証役の案）】
(a) 内とする名前は標準から取る。`localhost` / `*.localhost`（RFC 6761）、`*.local`（RFC 6762）、`*.home.arpa`（RFC 8375）、`*.internal`（ICANN が 2024 に予約。`host.docker.internal` と `metadata.google.internal` を含む）。比較は小文字にし、先頭の点を付けた接尾辞で行う（`x.internal.example.com` は endswith('.internal') が偽なので 矛 のまま。確認済み）。
(b) まず IP として解析し、IP でなく、かつ '.' を含まない名前だけを原理 2-a で 不 にする。理由の名前は探索役の案では新しい `net_host_dotless`。既存の `net_host_unknown` を流用してもよい。
(c) それ以外の名前は今までどおり external（矛）。
【素朴な直し方で壊れる反例】「'.' を含まないホストは 不」を IP の解析より前に置くと、`http://[::1]/x`（IPv6 のループバック。今は正しく 内）が 不 に落ちます。(b) の「IP でない名前に限る」を必ず守ってください。
【避けたと確かめた反例】文字列の連結や f-string のホストは、途中で切れた「点の無い定数」にはなりません。`'https://api' + p` は MODEL、`BASE + '.example.com'` は net_host_unknown です（検証役の r6_3 の木）。したがって (b) が正しい 矛 を誤りに変えることはありません。
【単一ラベル名を「常に 内」にしない】ccTLD の apex に A レコードがある例（`ai` / `dk` など）があるので、1 語の名前は 内 ではなく 不 が規則と整合します。
【注意】(a) は 矛 → 内 に変わる向き（見逃しの危険がある向き）なので、接尾辞の一致の境界を反例テストで固めます。
【範囲外で見つかったもの（別の所見として扱う）】`[::1]:8080`（ポート付きの IPv6）が 矛 net_external_host に誤判定されます。コロンが 1 つ以下のときしかポートを切り離さず、'[::1]:8080' 全体を IP として解析しようとして失敗するためです。同じ関数の誤警報ですが、この単位には含めません。
直す場合の手順は review_plan §4.4 どおりです（規則 → 反例テスト → 実装、run21 と compare_scans、逸脱の記録）。
- **記録済みの限界・決定との重なり**: 部分的に重なりますが、どちらも反証にはなりません。(1) O23 #4 は「openWorldHint:false の外部ホストの定義（private range / localhost / 環境変数由来）」を決める項目に挙げていました。しかし解決 (a) は「定数の外部ホストだけを矛盾にする」と決めただけで、名前の扱いは決めていません。(2) `.local` を内に入れたのは D56（c3a8c0c）で `_host_class` を入れたときの実装上の選択で、記録がありません。(3) evidence/review/explore_r3plus.json:3168 に「host.docker.internal → 外部で 矛、規則の穴、D3 だけ」という記録があります。これは旧 §2（D3 / D4 だけに効く誤りは記録するだけ）の下での記録で、D62 と review_plan §7.5 でその範囲は取り下げられたので、意図した設計判断ではありません。review_plan §5 の既知の問題・設計上の決定にも入っていません。設計の検証役の判定は refuted=false です。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。この所見は D3 / D4 の追加の回（第 6 回）のもので、2 観点の検証役はどちらも D62 で D3 が主指標になったことを踏まえています（設計: 「D62 and review_plan §7.5 withdrew that scope」、一般性: 「Since D62 made D3 a primary metric, it counts as a precision issue on D3」）。low とした根拠は v2 の件数への影響がたぶん無いことで、「D3 / D4 だけなら low」という旧文言ではありません。
- **推奨の理由**: 推奨の基準で fix にするには high か medium が要りますが、3 者の重大度はすべて low です。v2 の D3 net_external_host は公開ホストだけなので、今の件数への影響は無いと見込まれます。そのうえ、まず学生が「名前の private」を定義しなければならず、実装だけでは決まりません。そこで、§7.3 の「private」は名前については `localhost` / `*.localhost` / `*.local` の 3 形だけだと明記し、`*.internal` / `*.home.arpa` / 単一ラベル名が 矛 になることを限界（O42 以降）として記録することを推奨します。ただし、直し方は一般に正しく（条件つき）、凍結した語彙も要らず、変更も小さい（S）です。新しいデータでは Docker や社内の宛先を持つサーバで誤警報を出しうるので（corpus の件数は未測定の上限）、学生が §7.3 に定義を書くと決めるなら、fix_outline の順序と反例を守って直すのも妥当な選択です。
- **所見**:
  - R3d-r6-3: 代表で唯一の所見。実行は 24/24 行が再現。設計・一般性の両観点を生き延び（refuted=false）、重大度は 3 者とも low、fix_is_general=true（規則を先に定義し、IP の解析より後で点の無い名前を判定するという条件つき）。一般性の検証役が見つけた `[::1]:8080` の誤判定は同じ関数の別の問題で、この単位には含めない。（D3 の「private」の判定が名前について `localhost` / `*.localhost` / `*.local` の 3 形だけで、標準で私用と定まる名前（`*.internal`（ICANN 2024 予約、`host.do）

### U41 宣言（デコレータ引数・annotations）の読み取りが SDK の署名と pydantic の変換どおりでない（段階 C・重大度 低・推奨 限界として記録）

ツールの宣言（readOnlyHint など）を読む部分が、SDK の署名や pydantic が実行時に値を変換する規則のとおりに読んでいません。そのため、次の書き方で宣言の読み方を誤ります。(1) `@mcp.tool("名前")` のように名前を位置引数で渡す形。(2) annotations を位置引数や `**RO` で渡す形。(3) `readOnlyHint=IS_RO` のように値が変数になっている形。(4) `readOnlyHint=1` や `"true"` のように、実行時に真偽値へ変換される値。こうした宣言は「宣言なし」（⊥）として扱われ、仕様にある「読めないものは D_unknown（不明）」にもなりません。誤りの向きは主に、あるはずの矛盾を見落とす誤 clear と、D_unknown の数え落としです。名前を読み違えたせいで、別のツールの宣言を当てはめて誤警報を出す場合もあります。5 件とも 3 観点がそろって low で、v2 ではほぼ出てこない書き方です。

- **宣言**: D1 / D2 / D3 / D4 / tooling　**向き**: 混在　**規模**: M　**解決率を上げる向き**: はい　**語彙の追加**: 不要　**scripts/ だけで直る**: いいえ
- **根本原因**: 宣言の読み取り（`find_units` のデコレータ引数 → `_read_annotations` / `take()` → `d_kind_from`）が SDK の署名と pydantic の変換どおりに読まず、読めない形を D_unknown にしない: 第 1 位置引数のツール名 `@mcp.tool("x")` と公式 SDK の位置引数の annotations を読まない、`@mcp.tool(**RO)` の展開を黙って ⊥ にする、annotations の非定数の項（`readOnlyHint=IS_RO` / `{**COMMON}`）を黙って落として ⊥ にし、`ToolAnnotations(readOnlyHint=True, **EXTRA)` では読めた明示の項まで捨てて全体を D_unknown にし、lax 変換で真偽値になる値（`1` / `"true"` / `0`）を「真偽値でない」として ⊥ にする。
- **コードの場所**: authgap/entries.py:393-413 find_units（name / annotations の読み）, authgap/entries.py:850-891 _read_annotations / take(), authgap/dparse.py:164-197 d_kind_from, authgap/entries.py:915-918
- **重大度の根拠**: 5 件とも、探索役・設計・一般性の 3 観点すべてが low（review_rows.json の severities）。low の理由はどれも「まれ」であることで、D3 / D4 だけに効くからではない。

v2 での件数（検証役・探索役が数えたものだけ）:
- R2-r1-11 / R2-r1-4（デコレータ位置）/ R2-r2-3: 0 件。
- R2-r1-12: 非 dict の `**` を持つ ToolAnnotations はコーパス全体で 54 件。そのうち、上界を動かすキーワードも明示で持つものは 0 件。
- R2-r1-13: 探索役は「0 件」と書いたが、一般性の観点がこれを訂正した。v2-jag-k__google-docs-mcp に `@mcp.tool("docs.read", ...)` が 7 件ある（run20 では tool_name が関数名になっている）。ただしこの 7 件は annotations= をキーワードで持つので、D1 / D2 の判定は変わらない。

影響の範囲:
- R2-r1-12 は探索役が「tooling / count_loss」としていたが、両観点が、D1 の CONTRADICTION 1 件が UNKNOWN に落ちる（一般性の観点は D1 の誤 clear とみなす）ことを指摘した。これで影響の範囲は広がるが、出現が 0 件なので重大度は low のまま。
- D62 で D3 / D4 も主指標になった。R2-r1-11 の lax 変換は、`openWorldHint=0` の closed_world（D3）と `idempotentHint="true"` の idempotent（D4）も落とす。本記録者が d_kind_from を直接呼んで確かめた（ツリー全体での件数は未測定）。これは効く宣言が増える話で、D3 / D4 に効くことで重大度を上げも下げもしない。
- **直し方（一般に正しいか: 条件つきである）**: 入口は `find_units` / `_read_annotations` / `d_kind_from` の 3 か所。所見ごとに、直し方・避ける条件・反例を書く。

(a) 名前を位置引数で渡す形（R2-r1-13）
- 直し方: mcp 規則のデコレータで `call.args[0]` が文字列定数なら、それを tool_name にする。
- 根拠: 公式 SDK 1.9.4 / 1.10 / 1.30 / 2.2 の `name`、jlowin fastmcp の `name_or_fn`、それに規則 mcp が拾う claude_agent_sdk・crewai・langchain の `tool("Name")` のどれでも、第 1 位置の文字列は名前だった（一般性の観点がコーパスで分類し、例外は無かった）。
- 条件: 文字列定数のときだけ採る。
- 反例（ce13）: `@mcp.tool("safe_read") def delete_file` に別の `Tool(name="delete_file", readOnlyHint=True)` がある形。今は関数名で誤って join して誤警報を出しており、直すと誤警報が消える。直したことで正しい矛が消える反例は作れなかった。
- 手順上の注意: tool_name は unit のキーと D_op の照合に入る。直した後の run では、jag-k の 7 ユニットが compare_scans の「消えたユニット」に出る見込みなので、1 件ずつ理由を確かめる。

(b) annotations を位置引数で渡す形（R2-r2-3）
- 避ける条件: `call.args[3]` に決め打ちしない。mcp 1.9.x の署名は (name, description, annotations) で annotations は args[2]、1.10 以降は (name, title, description, annotations) で args[3]。反例 ce23 の `@mcp.tool("remove_19", "desc", ToolAnnotations(readOnlyHint=True))` は args[3] 固定では直らない。
- 直し方: args[2] と args[3] のうち、ToolAnnotations(...) の Call（か dict 表示）であるものを読む。それぞれの配置は片方の署名でしか実行できないので、一意に決まる。
- 位置で決め打ちせず形で見分ける理由: 規則 mcp は他の枠組みも拾うので、形で見分ける方が安全。

(c) `@mcp.tool(**RO)` の形（R2-r2-3）
- 直し方: デコレータ呼び出しに `kw.arg is None` のキーワードがあり、`annotations=` が見つからないときは、ann_form を unreadable（D_unknown）にする。
- 副作用（反例 spread_no_ann）: `**` の中に annotations が無いときも ⊥ が unknown に変わる。unknown は矛を立ても消しもしないので verdict は変わらない。変わるのは r_D の分母と、Tool リテラルとの join。Def 6 の規則どおり。
- 入れないもの: モジュール定数の dict を解いて中身を読むことは、解決率を上げる向き。global の再束縛などの敵対的レビューが要る（D17 改訂 2）ので入れない。

(d) フィールドの値が定数でない形（R2-r1-4）
- 素朴な直し方は壊れる: form='unreadable' にする案（fix_sketch の第 1 案）。`ToolAnnotations(title=TITLE, readOnlyHint=True)` は今、正しく contradiction:D1 になっている（c4_title_var）が、この案では explicit が消えて誤 clear になる。
- 直し方: literal_eval に失敗したフィールドのうち、判定に使うものだけで DKind.unknown=True を立てる。読めた値は values / explicit に残す。
- 対象のフィールド: 検証役は readOnlyHint / destructiveHint / openWorldHint を挙げた。D62 で D4 も主指標になったので、idempotentHint も含めるのが整合的（本記録者の補足。検証役は見ていない）。
- 含めないフィールド: 非リテラルの title には unknown を立てない。立てると D_unknown を過大に数える。
- 入れないもの: `readOnlyHint=IS_RO` の定数を解くことは解決率を上げる向きなので入れず、既知の限界として記録する。

(e) 明示キーワードと `**` が混ざる形（R2-r1-12）
- 直し方: `ToolAnnotations(readOnlyHint=True, **EXTRA)` で非 dict の `**` を見たら、return せず unknown=True を立てて続ける。明示のキーワードは explicit に残す。
- 根拠: Call のキーワードが明示と `**` の両方にあると TypeError になるので、登録に成功した以上、明示の値は必ず有効。
- 条件: Call のキーワード（kw.arg が非 None）にだけ当てる。dict 表示の中の `**` には当てない。
- 反例（ce12）: `{"readOnlyHint": True, **EXTRA}` や `ToolAnnotations(**{"readOnlyHint": True, **EXTRA})` では、後の `**` が前の項を上書きする。

(f) 範囲外の副産物（R2-r1-4 / R2-r1-12 の検証役が指摘）
- 今のコードは dict 表示の中の `**`（key が None）を黙って飛ばし、その前に書かれた項を明示として読んでいる。OVR={readOnlyHint: False} のときに誤警報になる（spread_after / dict_then_spread）。
- 直すなら、dict 表示では「`**` より後に書かれた項だけ explicit に残し、前の項は unknown」とする。
- これは別の所見として扱う（この単位の所見 ID には無い）。

(g) lax 変換される値（R2-r1-11）
- 直し方: d_kind_from の前に、pydantic v2 の bool の lax 規則をそのまま写した正規化を掛ける。
- 避ける条件: fix_sketch の 8 語の一覧は不完全。`'t'/'f'/'y'/'n'`（大小無視）、1.0 / 0.0 も True / False になる（mcp 1.30 / 2.2 で実測）。
- 変換できない値: 2 などは登録時に ValidationError になる。「明示」にはせず、present_no_bound のままにする。
- 反例: `readOnlyHint=0` / `"false"` は正規化しても False のままで、正しい ⊥ は壊れない。
- 対象: readOnlyHint / destructiveHint だけでなく、openWorldHint / idempotentHint にも同じ正規化を掛ける（D3 / D4）。
- 小さな注意: find_tool_literals は、pydantic でない自作の Tool クラスの値も拾う。ただ、意図は同じなので実害はほぼ無い。

回帰の確かめ方: (a)(b)(e)(g) は CONTRADICTION が増える向きなので、直した後の run で compare_scans と diff_effects を回し、増えた行と消えた行を 1 件ずつ確かめる。
- **記録済みの限界・決定との重なり**: 設計の観点は 5 件とも反証していない（refuted=false）。3 観点がそろい、5 件とも生き残った。どの挙動についても、それを決めた D 番号・O 番号・K1〜K7 は見つからなかった（検証役が decisions / open_questions / preregistration を grep した）。

仕様との関係:
- 仕様 Def 6（AUTHGAP_BRIEF_v3.md:322）の「読めない形は D_unknown とし ⊥ と混ぜない」と、「ツール名文字列の完全一致で join」に実装が反している。
- D17（decisions.md:1622）は「読めない形だけが D_unknown」を仕様どおりと確認しているだけで、今の挙動を決めたものではない。
- R2-r1-12 の「部分的に読めた形の扱い」は仕様の文言に書かれていない。規則の解釈を足すことになるので、設計の観点の confidence は 0.65。ただし meet_d_kind はすでに unknown と explicit を併せ持つ DKind を作っているので、既存の意味論から導ける。

既知の問題（review_plan §5）とは重ならない。

限界として残すもの（検証役の指示）:
- 直し方のうち、モジュール定数（`IS_RO` / `RO` / `COMMON`）を解くことは解決率を上げる向きなので、この修正に入れず既知の限界として記録する。
- dict 表示の中の `**` で前の項を明示として読む誤警報（spread_after / dict_then_spread）は、別の所見として扱う。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。5 件とも、探索役の自己申告の影響は D1+D2 か tooling です。検証役の重大度の理由はどれも「v2 での出現が 0 件（R2-r1-13 は 7 件あるが判定は変わらない）でまれ」で、「D3 / D4 だけなら low」を理由に下げた記述はありません。R2-r1-11 の D3 / D4 への効きは、D62 の後に本記録者が d_kind_from を直接呼んで確かめたもので、重大度は変えていません。
- **推奨の理由**: 推奨の基準では、fix には重大度 high か medium が要ります。5 件とも 3 観点がそろって low で、v2 ではほぼ出てこない書き方です。R2-r1-13 は v2 に 7 件ありますが、D1 / D2 の判定は変わりません。直すには authgap/ を変える必要があり、凍結の指紋に触れます。scripts/ だけで直る例外にも当たりません。以上から、基準どおりなら「low でまれな書き方」として限界に記録するのが推奨です。

一方で、直し方はどれも SDK の署名、Python の呼び出しの意味、pydantic の変換規則から一般に導けます。語彙の追加も要りません。学生が直すことを選ぶ場合は、費用に対して利点が大きい順に次の 3 つです。
- R2-r1-11: d_kind_from の 1 か所に正規化を入れる。D1〜D4 の誤 clear を正す。
- R2-r1-13: 第 1 位置の文字列を名前にする。誤 clear と誤警報の両方を正す。
- R2-r1-12: Call のキーワードだけを対象にする。

ただし、どれも CONTRADICTION が増える向きなので、CLAUDE.md の敵対的レビューと run の突き合わせが要ります。R2-r1-4 と R2-r2-3 の `**` の部分は D_unknown を正直に数える変更で、verdict は変わりません。どれを選んでも、fix_outline の条件（位置で決め打ちしない、form を unreadable にしない、dict 表示の `**` には当てない、pydantic の規則を全部写す）を守ること。
- **所見**:
  - R2-r2-3: 代表。宣言を渡す呼び出しの形（`**RO` と位置引数の annotations）を読まず、⊥ に落としている。3 観点とも low で false_clean。位置引数は D1 / D2 の誤 clear、`**` は ⊥ と D_unknown の混同。直し方は args[3] に決め打ちせず、ToolAnnotations の形で見分けるという条件つき。（デコレータ呼び出しの annotations が素のキーワードでない（`@mcp.tool(**RO)` / `@mcp.tool(name=..., **COMMON)` / 公式 SDK の位置引数 `@mcp.tool("n", No）
  - R2-r1-13: 同じ原因（SDK の署名どおりに読まない）の別の表れで、位置引数のツール名を読まない。3 観点とも low。一般性の観点が「v2 では 0 件」を訂正し、jag-k に 7 件あるとした（判定は変わらない）。誤 clear と誤警報の両方を作る。直すと compare_scans のキーが変わる。（デコレータの第 1 位置引数で与えたツール名（@mcp.tool("delete_file")）を読まず関数名を tool_name にするので、同名の Tool リテラル / D_op の名前と join できない（まれ））
  - R2-r1-4: 同じ原因の別の表れ（annotations の中身）。値が定数でない項を黙って捨てて ⊥ にし、D_unknown にしない。3 観点とも low で rule_mismatch。影響は D_unknown と r_D の報告だけ。form を unreadable にする素朴な直し方は c4_title_var を壊すので不可。定数を解くことは限界として記録する。（annotations のフィールド値が定数でない（readOnlyHint=IS_RO / Cfg.ro / not False、{**COMMON}）とき、その項を黙って落として ⊥ にし D_unknown にしない（仕様「読めない形）
  - R2-r1-12: R2-r1-4 の裏返し。明示のキーワードと読めない `**` が混ざると、確定している明示まで捨てて全体を unknown にする。3 観点とも low。両観点が「tooling」でなく D1 の矛が落ちると指摘した。直し方は Call のキーワードだけに当て、dict 表示の `**` には当てない（ce12）。（ToolAnnotations(readOnlyHint=True, **EXTRA) のように明示キーワードと読めない展開が混ざると、確定している明示宣言まで捨てて全体を D_unknown にする（宣言の数え落とし。まれ））
  - R2-r1-11: 同じ原因の別の表れ（pydantic の変換）。1 / "true" / 0 を真偽値として読まず ⊥ にする。3 観点とも low で false_clean。D1 / D2 に加えて D3 / D4 の closed_world と idempotent も落ちる（本記録者が確認）。pydantic の lax 規則を全部写すという条件つきで、1 か所の変更で直る。（pydantic の lax 変換で True になる値（readOnlyHint=1 / "true"、destructiveHint=0）を『真偽値でない = 上界を動かさない』として ⊥ にする（誤 clear。まれ））

### U46 クラス形の入口（method 規則・langroid）がクラスの構造を Python の意味で解かない（段階 C・重大度 低・推奨 限界として記録）

LangChain の BaseTool・agno の Toolkit・langroid の ToolMessage のように「クラスを継承して書くツール」を見つけるとき、解析器はクラスの継承関係を Python と同じ規則でたどらず、ソースに書かれた基底クラスの名前と、関数に付いた「所属クラス名」だけで判定しています。このため、(1) mixin から継承した `_run`、3 段以上の継承、別名 import した基底（`BaseTool as LCBaseTool`）、中間クラスを挟んだ ToolMessage を使うと、ツールが黙って 0 件になります（数え落とし）。逆に (2) メソッドの中の局所関数、別ファイルにある同名の無関係なクラス `Base` の子、Agent ではないクラスの同名メソッドは、ツールでないのにツールとして数えられます（偽ユニット）。どちらの場合もクラス形のツールには宣言 D がないので、D1〜D4 の判定は動きません。変わるのはユニットの数（分母）と、危険な効果を持つユニットの数、それに較正対 A18 の効果行です。

- **宣言**: tooling　**向き**: 混在　**規模**: L　**解決率を上げる向き**: はい　**語彙の追加**: 要　**scripts/ だけで直る**: いいえ
- **根本原因**: クラス形の入口がクラスの構造を Python の意味で解かず、書かれた名前と `FuncDef.classname` だけで照合する: `_class_bases` は書かれた基底名（別名 import を解かない）と裸名の `get_class` で 2 段までしか辿らず MRO を追わない（mixin から継承した `_run`、3 段の鎖、ToolMessage の間接派生が消え、別モジュールの同名 `Base` で偽ユニット）; method 規則は `fd.classname` しか見ないので `_index_body` が classname を引き継いだ入れ子の局所関数までユニットにする; langroid の handler は request 値と同名のメソッドをどのクラスからでも拾い、`_handler = "..."` の経路指定を読まない。
- **コードの場所**: authgap/entries.py:363-373 _class_bases, authgap/entries.py:443-470 method 規則, authgap/entries.py:574-620 langroid ToolMessage / handler, authgap/srcindex.py:192-207 _index_body の classname
- **重大度の根拠**: 4 件とも 3 観点（実行・設計・一般性）で low の判定が一致しています。実行の観点では 4/4 が再現しました。
low とする根拠は次の 3 点です。
- クラス形のユニット（method / toolmessage_handler）は自分では宣言を持たず、D=⊥ です。D が付く道は join_annotations（entries.py:899-925）で tool_name が同じ木の MCP `Tool(name=...)` リテラルと一致する場合だけで、検証役は「理論上はあるがまれ」と判定しました。
- 評価の経路 scan_v2_run20 での件数はクラス形 3 / 2,231（method/langchain 3、agno 0、toolmessage_handler 0）です。動くのは n_units と n_dangerous_units の分母だけです。
- 母集団での書き方の件数:
  - R2-r4-4: agno Toolkit の入れ子 def は v2/v3 で 0。BaseTool 派生のメソッドの中の入れ子 def は 30 件あるが、`_run` という名前のものは 0。
  - R2-r4-5: v2/v3 で `BaseTool as` / `Toolkit as` は 0。同名の中間基底の衝突は未測定。
  - R2-r5-1: (a) mixin・代入束縛は 0（413 木の AST 走査）。(b) カタログ基底まで 3 段の継承は corpus 全体で 3（OpenManus `VisualizationPrepare`、autogen `AgentTool` / `TeamTool`）。(c) ToolMessage の間接派生は 26（A18 = langroid 本体）。
  - R2-r5-4: A18__vuln の toolmessage ユニット 118 のうち 24 が Agent 基底の無いクラス。

例外は較正対 A18 です。A18 の効果行には効きます（24 件の偽ユニットと、26 件の間接派生）。ただし A18 の two_sided（T1）の結果が動くかどうかは未測定です。

旧文言「D3 / D4 だけなら low」は重大度の理由になっていません。low の理由は、D=⊥ であることと、書き方がまれなことです。D62 の下でも、D1〜D4 のどれにも同じように効かない点は変わらないので、重大度は戻しません。
- **直し方（一般に正しいか: 条件つきである）**: 共通の機構として、基底鎖の解決を 1 つにまとめ、R2-r4-5・R2-r5-1・R2-r5-4 (a) の 3 件で共有する。

【1. 基底鎖の解決】（R2-r4-5 / R2-r5-1。entries.py `_class_bases`）
- 基底名を次の順で解く。
  1. 同じモジュールを `get_class(name, module=cd.module, strict=True)` で引く。
  2. 無ければ `module_scope(path).lookup(head)` で import 先の dotted 名に解く。
  3. 解いた先が木内モジュールなら strict に get_class する。外部なら dotted 名の末尾で規則の bases と比べる。
- 鎖は有界（例 4 段）にたどる。上限は preregistration に書く。docstring（1 段）と実装（2 段）の食い違いも合わせて直す。
- 守りの条件（一般性の観点の反例より）:
  - (i) 裸名での引きを全廃しない。『木の中でその名前のクラスがちょうど 1 つ』のときだけ裸名で引く。2 つ以上あるときは、候補をすべてたどるか、たどらずに記録する。ソート順では選ばない。
  - (ii) 鎖の途中で到達した木内クラスについて、そのクラス自身の名前（と dotted の完全名）も規則の bases と比べる。これを怠ると、カタログ基底を木内に持つ木で、今は正しいユニットが消える。反例は ce_vendored（langchain_core/tools.py を vendoring した木）と、較正対 A18（langroid 本体で、ToolMessage が木内クラス）。
  - (iii) `from m import *` は m の `__all__` と直下の定義から解く。反例は ce_star（`from pkg.base import *` で FsBase を持ち込む形。今は正しくユニットになる）。
  - 解けない基底（動的な基底など）は、今までどおり末尾名で比べる。過剰収集の向きは変えない。

【2. メソッドの解決を MRO 順にする】（R2-r5-1）
- カタログ基底に届くクラス C について、`_run` / `_arun`（agno は `*`）を C から MRO 順に木内クラスをたどって解く。探す順は、まず `def`、次にクラス本体の `Assign` で木内関数に束縛したもの（`_run = shared_fn`）。
- self の種は C にする。
- 守り: mixin の `_RemoveImpl._run` を 2 つのツールクラスが共有すると、(module, qualname) のキーが衝突する（CLAUDE.md『同一キーの衝突』）。ユニットのキーに具象クラス C を含める。

【3. langroid の ToolMessage を推移的に集める】（R2-r5-1 (c)）
- ToolMessage の派生を推移的に集め、`request` と AnnAssign フィールドを基底鎖から合成する。どちらもサブクラスを優先する。

【4. 入れ子 def】（R2-r4-4。srcindex `_index_body` / method 規則）
- 素朴な直し方で壊れる反例: 『クラス本体の直下の def（is_method）だけをユニットにする』を当てると、メソッドの中で定義して `self.register(delete_under_root)` で登録した閉包（本当のツール。反例 ce_r4_4）が消える。
- 避ける条件: 入れ子 def（qualname の段が 2 以上）は、囲むメソッドの本体で `register(<名>)` または `tools=[<名>]` に渡されるときだけユニットにする。
- classname の伝播と self の種付けは変えない（K4 と関係する）。直接のメソッドに対する『*』規則は既存の設計なので触らない。t89 の `Srv._register.read`（デコレータ形）を壊さないこと。

【5. langroid の handler】（R2-r5-4 (a)）
- 候補は『Agent 派生クラス C の MRO 上にある木内クラスのメソッド』とし、C から MRO 順に解く。
- 素朴な直し方で壊れる反例: 『そのクラス自身が Agent 派生か、msg の注釈が当該 ToolMessage か』で絞ると、注釈の無い handler を mixin に置く形が消える（反例 ce_mixin_handler: `class FsAgent(FsHandlers, ChatAgent)`。今は正しくユニット）。
- 条件: 注釈が ToolMessage 派生に解ける経路も残す。A18 のテスト関数の中で入れ子に定義された Agent は基底が引けないので、この経路で拾う。テスト関数の中で同名クラスが衝突する場合（get_class の setdefault）は別に確かめる。

【6. `_handler` の経路指定】（R2-r5-4 (b)）
- 設計の観点で『入口規則の追加（§2、月 3 凍結）』と判定された。直さず、限界として記録する。
- 将来やるなら、Assign と AnnAssign の両方を読む（A18 の examples/basic/tool-custom-handler.py は `_handler: str = ...` の形）。1 つの handler に複数の message class が対応する場合も扱う。

【検証】
- t92、t93、t126、t126b、t110、t114、t112、t116 と、反例 ce_r4_4、ce_star、ce_vendored、ce_mixin_handler をテストにする。
- `diff_effects.py` で A9 / A18 を突き合わせる。A18 の偽ユニット 24 の行が消えるのは意図どおりだが、1 件ずつ確かめる。
- `compare_scans.py` で run20 と比べる。
- ユニットと行が増える向きの変更なので、CLAUDE.md の敵対的レビューを通す。
- **記録済みの限界・決定との重なり**: §5 の既知の決定・限界とは重ならない（4 件とも設計の観点が確認済み）。近い記録との関係は次のとおり。
- MAX_DEPTH=4 は呼び出しの深さで、継承の深さではない。
- D35 の限界 2 は val 側の `_class_family` の末尾名、限界 3 は val の分割降下の継承メソッドで、いずれも場所と機構が別。
- K4（decisions.md:1536）は同じ classname 伝播が原因だが、症状は呼び出し解決の誤 clear で、直す場所も違う。
- D17 は `_construct_in_tree` で『名前だけで引く』形を禁じた。入口側の裸名フォールバックはこの方針に反して残ったもの。
- D12 の限界（tools-list の呼び出し先を Agent / Crew に限る案を採らない）は別の規則の話。
- R2-r4-5 (a) は R2-r3-4（`Tool` の別名）と同型の兄弟だが、箇所が違う。
- `_class_bases` の docstring『1 段だけ』は設計意図とも読めるが、文書化された決定ではない。実装は 2 段で、docstring と食い違う（R2-r5-1 の設計の観点の迷い）。

設計の観点で反証された部分: R2-r5-4 (b)（`_handler` の経路指定）だけ。書いた規則（request 値と同名のエージェントメソッド）の外にあり、入口規則の追加（§2、月 3 凍結、O39 と同じ扱い）に当たる。所見の expected（MyAgent.do_rm もユニット）は規則から導けない（expected_is_correct=false）。
所見の事実に誤りが 1 つある: R2-r5-4 の『`_handler =` の使用は corpus 内 0』は誤り。一般性の観点が、A18 の examples に AnnAssign 形で 3 件あることを確認した。
R2-r5-1 と R2-r5-4 は第 5 回（事前登録の手続きの外、review_plan §7.3）の所見なので、表では分けて示す。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。4 件とも low の理由は「D=⊥ で D1〜D4 のどれにも効かず、分母だけが動く」と「書き方がまれ（run20 でクラス形 3 / 2,231、書き方ごとに 0〜3 件）」で、旧文言は使われていない。R2-r4-4 の設計の観点はむしろ「D3 / D4 だけに効く件ではないので記録止まりにはならない」と明記したうえで、agno が 0 件なので low としている。
- **推奨の理由**: 代表の重大度は 4 件とも low で、3 観点が一致しています。どれも D=⊥ で D1〜D4 の判定を動かさず、評価の経路（run20）でのクラス形ユニットは 3 / 2,231 です。書き方もまれです（mixin 0、別名基底 0、3 段継承 3、agno の入れ子 0）。
直し方は一般にありますが、条件つきです（裸名は一意なときだけ、到達した木内クラスの名前も比べる、star import、MRO と具象クラスのキー、register された閉包、mixin の handler）。基底鎖と MRO の解決を新しく設計することになり（L）、`authgap/` を変えるので凍結の指紋が変わります。さらに、較正対 A18 の units と効果行が動きます。ユニットが増える向きなので敵対的レビューも要ります。凍結の直前に low の件へ払う費用としては大きいです。
R2-r5-4 (b) は入口規則の追加（凍結語彙）に当たるので、どのみち限界として記録するしかありません。
学生が一部だけ直すなら、候補は次の 2 つです。
- R2-r4-4: 局所の変更で直せます。ただし「register / tools= に渡される閉包は残す」という条件が必須です。
- R2-r5-4 (a): 書いた規則「エージェントメソッド」と実装の食い違いで、review_plan §1 の (b) に当たります。
どちらも数は小さく、A18 を diff_effects で突き合わせることが前提です。
- **所見**:
  - R2-r5-1: 代表。クラス形の入口が継承（MRO）を追わない。(a) mixin・代入束縛の `_run`、(b) 3 段の継承、(c) ToolMessage の間接派生が、ユニット 0 のまま黙って消える（数え落とし）。3 観点とも low で生存。件数は (a) 0、(b) 3、(c) 26（A18）。第 5 回（手続きの外）の所見。（クラス形の入口（method 規則 / langroid ToolMessage）の認識が「書かれたクラス本体と直接の基底」だけを見て継承（MRO）を追わない: (a) `_run` を BaseTool 派生でない mixin から継承す）
  - R2-r4-5: 同じ原因の別の表れ。`_class_bases` が書かれた基底名で比べるので別名 import（`BaseTool as LCBaseTool`）を解かず、裸名の get_class でファイルのソート順によって偽ユニット（Helper._run）か数え落とし（RealTool._run）が起きる。3 観点とも low で生存。直すときは、裸名を一意なときだけに限る、到達した木内クラス名も比べる、star import を解く、の 3 条件が要る。（R2-r4-5 [R2] method 規則の基底照合 `_class_bases` が書かれた基底名しか見ない: (a) `from langchain_core.tools import BaseTool as LCBaseTool` ）
  - R2-r4-4: 同じ原因の別の表れ（classname だけを見ているため）。agno の method 規則が、メソッドの中の入れ子の局所関数までユニットにする（過大計上。同じ効果が 2 ユニットに数えられる）。3 観点とも low で生存。単独でも局所の変更で直せるが、register / tools= に渡した閉包は残す条件が必須（反例 ce_r4_4）。（R2-r4-4 [R2] agno の method 規則（bases=Toolkit, names="*"）が、メソッドの**中に入れ子で定義した局所関数**（`FileTools.__init__._log` / `FileTools.）
  - R2-r5-4: 同じ原因の langroid 側の表れ。(a) Agent でないクラスの同名メソッドを handler にする偽ユニットは、書いた規則との食い違いとして生存（A18 で 24/118）。(b) `_handler` の経路指定は、設計の観点が『入口規則の追加（月 3 凍結）』と判定したので、期待から外して限界として記録する。所見の『corpus で使用 0』は誤りで、A18 の examples に 3 件ある。第 5 回（手続きの外）の所見。（langroid の handler 解決が (a) `request` 値と同名のメソッドを**どのクラスからでも**拾う（Agent でない helper クラスの `search` / `update` / `add` が toolm）

### U53 diff_effects の比較の値（段階 A・重大度 低・推奨 直す）

解析器を直したときの確認用の道具 scripts/diff_effects.py は、較正対の木で効果の行を新旧 2 つの版で比べます。ただ、行の中身として比べているのは「誰が値を決めるか（主体）」と「確度」と「解決できたか」の 3 つだけです。矛盾の判定に効くほかの属性（SQL の先頭語、ファイルを開くモード、削除や上書きかどうか、HTTP メソッド、shell の指定、定数の値）が変わっても、また判定が「矛盾」から「不明」に変わっても、「消えた 0 / slot 変化 0」、終了コード 0 と表示されます。つまり解析器の回帰を見落とす向き（数え落とし）の誤りで、解析器の出力そのものではなく確認用の道具の盲点です。

- **宣言**: tooling　**向き**: 数え落とし　**規模**: S　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: `diff_effects.py` の DUMP が効果行の値を slot の主体 / 確度と resolution だけで比べ、§7 の判定に効く属性（sql_head / fs_mode / destructive / http_method / exec_mode / 定数）と 矛 ↔ 不 の注記を比べないので、解析器の変更による判定の反転が「消えた 0 / slot 変化 0」（終了コード 0）で通る。
- **コードの場所**: scripts/diff_effects.py:35-49 DUMP, scripts/diff_effects.py:112, 131-134
- **重大度の根拠**: 代表の重大度は 3 意見の中央値で low（探索役 medium / 設計 low / 一般性 low）。low とした理由は、最終評価の数字を作る道具ではなく、開発時に回帰を見つけるための道具だから（設計の観点）。見落としが起きるのは「凍結前に解析器を直す」「属性が退行する」「v2 で宣言つきのユニットがその site に届かない（compare_scans でも拾えない）」の 3 条件が重なるときだけ。一般性の観点も、凍結後は解析器を変えない（D59 / D60）ので評価では起きないとした。旧文言「D3 / D4 だけなら low」を使って下げた形跡は無い（下げた理由は D1〜D4 のどれにも直接効かない道具だからで、D62 で変わる理由ではない）。ただし review_plan §4.4 手順 2 では、この添削で直す所見（run21 と再凍結）の確認にこの道具を使う。R3 系の SQL / open モード / destructive の分類を直す所見が採られると、その修正の較正対での確認が正にこの盲点に当たるので、重大度は low のままでも今回の再凍結の手順の中で効く。
- **直し方（一般に正しいか: 条件つきである）**: 直し方: scripts/diff_effects.py の DUMP（35〜49 行）で、行の値の文字列（val）に §7 の判定に効く効果の属性を足す。足すのは destructive / fs_mode / sql_head / http_method / http_method_model / exec_mode / sub_kind / db_rule と、各 slot の shape の種類と定数（stable_repr）。値が違えば今の 112 行の比較でそのまま「slot 変化」（~）として表示される。できれば「属性変化」として slot 変化と分けて数えると読みやすい。任意で、その効果に対応する行の contradiction:* / contradiction_unknown:* 注記も値に足す。

守る条件（検証役が挙げたもの）:
1. 行の鍵（44 行の unit_id | witness_chain | kind@site relpath:lineno）は変えない。鍵に属性を入れると、属性の変化が「消えた行 + 増えた行」に化けて、終了コード 1 の意味（本当に消えた経路）が壊れる。
2. 終了コードの規則（131〜134 行。消えた行があるときだけ 1）は変えない。直した結果は「不変と出ていたものが変化と出る」方向にしか動かず、消えた行を隠すことは無い（一般性の観点: 壊れる正しいケースは無い）。
3. DUMP は --before に指定した古い版の authgap の上でも走る（56〜63 行）。destructive（ef15c4b、09-20）、fs_mode / http_method（c3a8c0c、09-24）はあとから足された属性なので、それより前の commit を --before にすると属性が無くて AttributeError で落ちる。getattr(e, "fs_mode", None) のように既定値つきで読む（落ちても「解析に失敗」と出るので黙った回帰にはならないが、道具として使えなくなる）。片方の版にだけある属性は全行が「変化」と出るので、その場合は注意書きを出すとよい。
4. 行の注記を効果に対応させるとき、(kind, site) だけで結ぶと 1 ユニットの中に同じ sink の呼び出しが複数あるときに多対一になる。lineno（と relpath）まで使って結ぶ。
5. 定数の repr を値に入れると、表現だけの版間差（例: bytes の repr）が「変化」として並ぶ雑音が出る。表示が増えるだけで消えた行の検出には影響しない。

役割の分担（設計の観点）: 判定の反転（矛 → 不）は、母集団 run の compare_scans.py の「消えた CONTRADICTION」が本来の見張り役で、D57 でも run13 → run14 の 29 件として実際に見えて 1 件ずつ確かめられている。注記を diff_effects に入れるのは compare_scans と重なり、較正対は宣言をほとんど持たない（A4 が 1 ファイル、A9 が 10 ファイル）ので効果は小さい。優先するのは効果の属性のほう。変更は scripts/ だけで、authgap/ は変えないので凍結の指紋（docs/fingerprint.json は authgap/ の sha256）に触れない。
- **記録済みの限界・決定との重なり**: 記録済みの限界（review_plan §5）とは重ならない。docstring（9〜10 行）が約束しているのは「slot の主体 / 確度の変化」までで、属性を比べないという決定を書いた D 番号は無い。diff_effects は 6be7930（09-14）で書かれ、destructive / fs_mode / http_method はそのあとで効果に足された属性なので、意図した除外ではなく見直されていないだけ（設計の観点）。設計の観点は所見の「期待」の一部を読み違いとした: 探索役の再現（c3a8c0c → HEAD、D57 の db_model_sql → db_sql_model_opaque）は効果行も slot も同じで変わったのは判定規則だけなので、今の規則どおりなら「行 1 → 1、消えた 0 / slot 変化 0」が正しく、判定の反転は compare_scans の担当（CLAUDE.md の落とし穴の分担、scripts/compare_scans.py:107-123）。ただし設計の観点も refuted = false で、効果の属性を比べない点は所見として残した。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。設計の観点の「記録のみ（D1/D2 に効かない）」は、道具が D1〜D4 のどの判定にも直接効かないという意味で、「D3 / D4 だけなら low」の旧文言を理由にしたものではない。一般性の観点も low の理由は「凍結後は解析器を変えないので評価では起きない」。戻す必要は無い。
- **推奨の理由**: 重大度は low だが、scripts/diff_effects.py の DUMP の 1 か所を変えるだけで authgap/ に触れず（凍結の指紋が変わらない）、語彙の追加も要らず、直し方は一般に正しい（壊れる正しいケースは無い。条件は getattr の既定値、鍵と終了コードを変えない、注記は lineno まで使って結ぶ）。基準の「評価の道具は low でも fix してよい」に当たる。さらに review_plan §4.4 手順 2 で、この添削の修正（run21・再凍結）の確認にこの道具を使う。SQL の先頭語や open モード、destructive の分類を直す所見を採るなら、その較正対での確認がこの盲点に当たるので、ほかの修正より先に直すのがよい。判定の反転を diff_effects に出すこと（注記の比較）は compare_scans と重なるので、入れるかどうかは任意。
- **所見**:
  - R5-r2-3: 代表で唯一のメンバー。実行の観点で再現した（5/5 行、rc=0）。設計の観点は refuted=false だが、期待の一部（矛 → 不 の反転を diff_effects に出すべき）は役割分担の読み違いとした（反転は compare_scans の担当）。生き残る核は「効果の属性の変化が見えない」点。一般性の観点は refuted=false、直し方は一般に正しい。重大度は medium / low / low で代表は low。（diff_effects.py は効果行の値を slot の主体 / 確度と resolution だけで比べるので、§7 の判定に効く属性（sql_head / fs_mode / destructive / http_method / ）

### U54 run と解析器の実装の指紋（段階 A・重大度 低・推奨 直す）

走査の記録（summary.json）には「その時の git の HEAD」しか残らず、HEAD が docs だけの commit でも、authgap/ に未コミットの変更があっても、記録からは区別できない。凍結の記録を書く freeze_analyzer.py は、根拠として渡された run が今の解析器で取ったものかを確かめないため、別の解析器で取った run18 を渡しても終了コード 0 で凍結の記録を書いてしまった。判定そのものが誤るわけではない。誤るのは「どの解析器の結果か」の来歴で、凍結後に解析器へ手を入れたまま最終評価を走らせても、記録からは分からない。

- **宣言**: tooling　**向き**: 規則との食い違い　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: run の記録と解析器の実装を結ぶものが無い: scan_v2.py は git HEAD しか残さず（docs だけの commit・未コミットの変更を区別しない）、manifest の fingerprint.sha256 はカタログだけなので D1 の判定が違う実装（672f0f0 と 94c40b4）でも同一になり、freeze_analyzer.py は --run の analyzer_commit を照合せずに別の解析器の run を凍結の根拠として書く。
- **コードの場所**: scripts/scan_v2.py:168, 190-197 summary, authgap/report.py:50-131 fingerprint, scripts/freeze_analyzer.py:44-65
- **重大度の根拠**: 探索役・設計・一般性の 3 観点がそろって low と判定した。実行の観点でも再現した（rc 0、主張 7 行のうち 5 行が自動で一致し、残りは手で確認）。D1〜D4 の判定そのものは変えない。今の記録には食い違いが無い（fingerprint.json の scan_run = scan_v2_run20、analyzer_commit = 94c40b4 で、run20 の analyzer_commit と一致）。run18 で凍結するのは操作の誤りを想定した筋書きである。一方で、review_plan §1 の目的「誤った解析器のまま最終評価を始めない」に直接かかわり、population_v3.md:30-31 と D59 の末尾（decisions.md:3390）に書いた「凍結後の実行は指紋と照合し、一致しなければ走らせない」に対応する実装が無い。これは文書と道具の食い違いである（設計の観点の判定）。旧文言「D3 / D4 だけなら low」とは関係が無く、重大度を戻す必要は無い。
- **直し方（一般に正しいか: 条件つきである）**: 直すのは scripts/ だけで、authgap/ には触れない。
(1) scripts/scan_v2.py の summary に次の 4 つを足す。scripts/freeze_f0a.implementation_hashes() を再利用した implementation_sha256_combined、authgap_dirty（`git status --porcelain -- authgap` の出力が空でないか）、走らせた Python の版、authgap_last_commit（`git log -1 --format=%H -- authgap`）。analyzer_commit（HEAD）は、過去の run と比べられるように残す。
(2) scan_v2.py に `--require-fingerprint docs/fingerprint.json` の選択肢を付ける。結合 sha256 が一致しないとき、または authgap_dirty のときは走らせずに rc 2 を返す。これで population_v3.md:30-31 の手順が道具で強制される。
(3) scripts/freeze_analyzer.py は evidence/<run>/summary.json を読み、run の実装と今の実装が違えば書かずに rc 2 で止まる。python の版は、今の処理系ではなく run の値を記録する。

守り（一般性の観点の反例と、避ける条件）:
- 素朴な直し方「run の analyzer_commit（HEAD の文字列）と今の commit を比べ、違えば rc 2」は壊れる。過去の 21 run のうち 12 run（run11〜14、16、17、4、5、v3_run1 など）は、authgap/ を最後に変えた commit とは別の、docs だけの HEAD を記録している（例: run11 は HEAD ff04043、authgap の最終 commit 95ade18）。文字列で比べると、正しい run を誤って拒む。
- 避ける条件: 比べるのは「実装の結合 sha256」か「`git log -1 --format=%H <run の commit> -- authgap`（run 時点で authgap/ を最後に変えた commit）」にする。HEAD の文字列では比べない。
- 既存の run（run20 を含む全部）には実装 hash の欄が無い。欄が無い run は authgap の最終 commit で比べる。ただしその場合は、run 時点の未コミット変更は検出できない。この限界を出力に明記する。
- `--require-fingerprint` は既定にせず、選択肢にする。review_plan §4.4 の手順では、fingerprint.json を作り直す前に run21 を取る。既定で照合すると、古い fingerprint.json と一致せずに run21 が拒まれる。
- 順序: この修正は run21 を取る前に入れる。そうすれば run21 の summary が実装 hash を持ち、手順 5 の再凍結がそれと照合できる。
- 根拠から外すもの: manifest の fingerprint()（report.py:50-131）が val エンジン・effects.py を区別しないことは、freeze_analyzer.py:6-8 の docstring に書かれた既知の設計である。そのために implementation_sha256 を別に持っている。fingerprint() は変えない（変えると authgap/ の指紋が動く）。
- **記録済みの限界・決定との重なり**: 部分的に重なる。manifest の fingerprint.sha256 がカタログしか hash せず、D1 の判定が違う 2 版（672f0f0 と 94c40b4）でも同じ値になる点は、freeze_analyzer.py:6-8 の docstring に既知の設計として書かれている。このため設計・一般性の両観点が、この部分を所見の根拠から外した。所見の本体（run の要約に実装 hash・dirty・処理系が無いこと、freeze_analyzer が run を照合しないこと、population_v3.md:30-31 と decisions.md:3390 の手続きに実装が無いこと）は既知ではない。review_plan §5 の既知の問題・O 番号・K1〜K7 とは重ならない。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。3 観点とも low としたが、理由は「評価の道具の来歴の問題で判定を変えない」「今の記録は整合している（run18 で凍結するのは操作の誤りの筋書き）」であり、D3 / D4 の旧文言によるものではない。
- **推奨の理由**: 重大度は low だが、scripts/ だけで直る評価の道具であり、解析器の凍結の指紋に触れない。凍結と最終評価の経路（review_plan §4.4 の run21 から再凍結まで、学生が新しいデータで走らせる最終評価）で起きるため、基準の但し書きにより fix を推奨する。一般に正しい直し方がある（条件つき: HEAD の文字列ではなく、実装 hash か authgap の最終 commit で比べる）。語彙の追加は要らず、設計の観点も本体は記録済みの限界ではないと判定した。run21 より前に入れれば、再凍結の記録が照合つきで作れる。
- **所見**:
  - R5-r2-4: 代表で、唯一の所見。3 観点とも生き残った（実行: 再現、設計: 本体は反証されず、一般性: 直し方は一般に正しいが、HEAD の文字列で比べると 12 run を誤って拒むので条件つき）。ただし「manifest の fingerprint がカタログだけ」の部分は、docstring に書かれた既知の設計として設計の観点が根拠から外した。（run と解析器の実装を結ぶ記録が無い: scan_v2.py は git HEAD しか残さず（docs だけの commit / 未コミットの変更を区別しない）、manifest の fingerprint.sha256 はカタログだけ）

### U55 two_sided の片側だけのサイト（「サイトが無い」を「等級なし（null）」と取り違える）（段階 A・重大度 低・推奨 限界として記録）

両側比較の採点器（scripts/two_sided.py）は、脆弱版と修正版の片方にしか無い効果サイトについて、無い側の値を座標に関係なく None で返します。修正で書き込み関数を置き換えた場合（open を Path.write_text にする）や、同じツールに呼び出し点を足した場合がこれに当たります。期待表では null は「サイトはあるが等級が無い」という意味で、「サイトが無い」は presence 座標でだけ表す決まりです。そのため、サイトが無いことが「等級なし → weak」という事前登録どおりの変化として数えられます。また req_val のように両側とも MODEL で何も動いていない座標でも「値が違う」と数えられ、座標一致を通ります。どちらも通過を多めに数える向きの誤りです。現行の較正 8 対では件数は変わりません（7/8・7/8・8/8）。

- **宣言**: tooling　**向き**: 規則との食い違い　**規模**: M　**解決率を上げる向き**: いいえ　**語彙の追加**: 不要　**scripts/ だけで直る**: はい
- **根本原因**: two_sided.py の事前登録照合 / 座標一致で、`SiteRecord.value()` が片側にしか無いサイトの欠けた側を None で返すため、「等級なし（null）」と「サイトが無い（absent。presence 座標でだけ表す）」が混ざり、sink の置換・呼び出し点の追加で片側にだけ現れたサイトが `from: null` の等級変化や任意の座標の変化として主指標（pass_preregistered）と座標一致（pass_coord_match）を通る。
- **コードの場所**: scripts/two_sided.py:327-346 SiteRecord.value, scripts/two_sided.py:360-409 match_expected, docs/expected_tuples.json:_semantics
- **重大度の根拠**: 探索役・設計・一般性の 3 観点とも low。探索役が 8 対を instrument.py で走らせ、一般性の検証役も走らせ直した。どちらも「presence 以外の座標で片側だけの record が strict / coord に当たった件数 0」（当たるのは presence の期待の A3 1 件・A5 2+2 件だけ）で、報告値 7/8 ｜ 7/8 ｜ 8/8 は変わらない。一般性の観点によれば、two_sided.py は凍結した較正 8 対（T1 の主指標）にしか使われない。scan_v2 系の集計と D60 の最終評価（新しいデータの手判定）の経路には入らないので、将来の対を足したときにだけ効く潜在的な欠陥にとどまる。D3 / D4 とは関係が無く（道具の所見）、旧文言による格下げは無い。
- **直し方（一般に正しいか: 条件つきである）**: 【直す場所】scripts/two_sided.py の SiteRecord.value（:342-346）と match_expected（:360-409）。docs/expected_tuples.json（事前登録済み・凍結）は変えず、採点器だけを直す。authgap/ に触れないので指紋は変わらない。
【一般に正しい直し方（一般性の検証役の notes）】(1) presence 以外の座標では「サイトが無い」を null と同一視しない。欠けている側は None ではなく「absent」という区別できる印で返し、strict・coord のどちらでも from/to/値との一致に使わない。(2) 同じ経路・同じ slot で、片側だけの record が脆弱側と修正側に 1 つずつあるとき、BRIEF:703 は sink の置き換え（sink-substitution）を「同じ効果サイト」として扱う。そこで両者を対にして値を比べる。片側に複数あるときは、既存の規則「同じサイトキーが複数残る場合は最弱を採る」で 1 つ選ぶ。(3) 対にならない片側だけの record は presence の期待にだけ使う。(4) kind は records のキー (kind, site, slot) に入っているので、両側にある record では kind の変化を表せない。今の実装では kind の strict が構造上通らない。kind の変化もこの対の作り方で拾うのが BRIEF:690（A3 のために kind を座標に入れた趣旨）と合う。
【素朴な直し方で壊れる反例（必ず避ける）】探索役の fix_sketch は「coord != presence では両側に tuple_view がある record だけを候補にする」。これだと、sink の置き換えと検証子の追加を同じ修正で入れた対が壊れる。反例は、脆弱側 open(path,'w')、修正側が commonpath 検査のうえで Path(real).write_text の対。この対の grade null→weak の strict 通過は BRIEF:703 に照らして正しいが、それが消えて n_strict 0 になる（数え落とし）。座標一致の誤った通過（req_val・principal が MODEL→MODEL なのに n_coord 2）は消えるが、正しい通過まで巻き込む。避ける条件は、片側だけの record を捨てずに、同じ経路・同じ slot で対にすること。
【守り】直したら 8 対で 3 列（事前登録照合 7/8・座標一致 7/8・any-change 8/8）と、tests/test_two_sided_preregistered.py の逆向き 4 対・open→read_text の対が不通過のままであることを確かめる。A3 / A5 の presence 期待が通ることも確かめる。検証役によれば、今の 8 対では値が変わらないはず。変わったら 1 件ずつ理由を確かめる。SiteRecord.value の docstring に「absent は presence でだけ表す」と書く。
- **記録済みの限界・決定との重なり**: 記録済みの限界・決定との重なりは無い。設計の検証役は decisions.md・preregistration.md・open_questions.md（O1〜O41）・D19 の K1〜K7・review_plan §5 を grep したが、該当する記録は見つからなかった。A2 の 7/8（D58 / O35）と A18 の転記（prereg 逸脱 #5）は別の原因。設計の観点では反証されなかった（BRIEF:688・:1178 の「両版に同一の効果サイトが存在し」、expected_tuples.json:8-9 の _semantics と食い違う）。ただし一般性の検証役は、所見の expected の一部を仕様と合わないと判定した（expected_is_correct=false）。BRIEF:703 は sink の置き換えを同じ効果サイトとみなすので、repro の grade null→weak の strict 通過は仕様上は正しい通過になる。誤りと確定したのは、req_val・principal の座標一致の誤通過と、「欠けている側」と「null」を区別しない実装の不整合の 2 点。
- **旧文言（D3 / D4 だけなら low）による格下げ**: 無し。この所見は評価の道具（tooling）の所見で、D3 / D4 とは関係が無い。3 観点とも low としたのは「8 対で件数が変わらない」「最終評価の経路に入らない」を理由にしており、旧文言「D3 / D4 だけなら low」は使われていない。
- **推奨の理由**: 重大度は 3 観点とも low。two_sided.py は凍結した較正 8 対にしか使わず、D60 の最終評価（scan_v2 系・新しいデータ）の経路には入らない。そのため「最終評価の経路で起きる道具の誤りなら low でも fix」の条件に当たらない。8 対で presence 以外の座標に片側だけの当たりは 0 件で、報告値も変わらない。探索役の素朴な直し方は、仕様上正しい通過（sink の置き換えと検証子の追加が重なる対）を消す。正しい直し方には同じ経路・同じ slot で片側だけの record を対にする設計が要り（size M）、較正の数値が変わらないのに採点器の規則を事後に増やすことになる。そこで「片側だけのサイトは presence 以外の座標で null と同一視される。今の 8 対では当たり 0 件」と限界として記録し、較正の対を将来足すときは採点の前に fix_outline の対にする直し方を入れることを勧める。直す場合も authgap/ に触れず（指紋は不変）、期待表を変えずに採点器だけを直す。
- **所見**:
  - R5-r4-1: 代表で唯一の所見。実行 3/3 行が再現、設計・一般性とも反証されず（どちらも low・rule_mismatch・fix_is_general=true）。一般性の検証役は、fix_sketch（両側にある record だけに絞る）は sink の置き換えと検証子の追加が重なる対の正しい strict 通過を消すので不可とし、同じ経路・同じ slot で対にする直し方を示した。（two_sided.py の事前登録照合 / 座標一致が、片側にしか無いサイト（sink の置換・呼び出し点の追加で修正側にだけ現れた site）を `from: null` の等級変化や任意の座標の「変化」として数える: `SiteRec）
