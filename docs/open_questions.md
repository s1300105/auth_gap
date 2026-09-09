# 未解決事項（黙って安全側に倒さないための記録）

規則: **解決できなかったものは「不明」として記録する。** 本ファイルは
仕様書 `AUTHGAP_BRIEF_v3.md` を読んで実装した際に、仕様書の記述だけでは
決まらなかった点と、実装で暫定的に決めた内容を残す。各項目に
「いつ誰が決めるか」を書く。

最終更新 2026-09-09。

---

## Q1. weak 理由語彙の食い違い（`absolute_only` / `existence_only`）

- **状況**: Def 5 の凍結語彙は **19 語**で、`absolute_only` と `existence_only` を
  含まない。一方 §2.6 の fixture F7（OpenManus `StrReplaceEditor`）は
  「weak 理由 `absolute_only` / `existence_only` / `no_containment` を追加する根拠」
  と書いている。
- **実装がしたこと**: 19 語を採用し、2 語は**追加していない**
  （`authgap/catalog/validators.py` の `WEAK_REASONS`）。
- **効果**: F7 の期待行を書くときに、この 2 つの weak 理由が使えない。
  現状は `no_containment` に寄せることになる。
- **決める時点**: 月 6 のゲート語彙凍結の**前**。学生が決める。
  語彙を 21 語にするなら `WITNESS_TEMPLATES` にも witness を足すこと
  （`tests/test_vocabulary.py::test_every_weak_reason_has_witness` が要求する）。

## Q2. 付録 G の G12 の reason が仕様書に無い

- **状況**: 付録 G の表は G12 の期待を `NODOM` とだけ書き、reason クラスを
  書いていない。しかし §2.5.6 B3b は `(verdict, reason クラス, witness 行)` の
  3 つ組一致を要求するので、reason を空のままには置けない。
- **実装がしたこと**: `deny_reaches_effect` を pin した
  （`fixtures/gates/expected.json` の `reason_note` に導出を書いた）。
  導出: 承認の拒否辺は finally(exc) 複製へ入り、その複製が効果そのものなので
  `d ∈ Reach(s)` が成り立つ。
- **決める時点**: 学生が追認する。追認するまで「実装者の導出」であって
  仕様書の記述ではない。

## Q3. `finally` 複製を判別する fixture が無い（実装変異の既知の生存）

- **状況**: 実装変異 `no_finally_copies`（finalbody を脱出種別ごとに複製せず
  1 ノードで表す）が**生存する**。生存 1/15 なので受け入れ条件（≤ 2）は満たすが、
  これは fixture 集合の被覆の穴である。
- **測定**: G12 について、複製ありで効果行 L19 に対応する CFG ノードは 2 個
  （`normal` / `exc`）、複製なしで 1 個。しかし verdict / reason / witness は
  **どちらも `NODOM(deny_reaches_effect)` / `L17`** で一致する。
- **なぜ一致するか**: `(G-i)∧(G-ii)` が先に同じ誤りを捕まえるから。承認の
  拒否辺が finally ノードへ入る以上、複製の有無に関わらず「拒否側から効果へ
  到達できる」が成り立つ。
- **したがって**: 複製が効くのは (a) 効果行に対応するノードの個数、
  (b) witness の脱出種別表記（`finally-copy(exc) @ L19`）、(c) 一部の複製だけが
  ゲートされる形での ⊓ の計算、の 3 つであり、付録 G の 15 件はどれも見ていない。
- **決める時点**: 学生が (i) 生存 1 件として報告するか、(ii) 付録 G の外に
  構造的な単体テストを足すか（その場合も**生存数は fixture テストだけで数える**
  — §2.5.6 の定義を動かさない）を決める。

## Q4. セレクタの運用定義（`req_occ` の主語）

- **状況**: Def 5 は「ディスパッチキー（セレクタ）そのものを主語とする allowlist」
  が `req_occ` を引き上げると書くが、「セレクタ」の機械的な決め方を書いていない。
  G11（主語不一致 → `non_binding_gate`）と G15（`dispatch(name, argstr)` から
  `git_log(argstr)` を直接呼ぶ形で `name` が主語）の両方を満たす定義が要る。
- **実装がしたこと**（`authgap/gateharness.py: selector_names`）:
  1. 被呼び出しが `Subscript`（`TOOLS[name](args)`）なら、その添字がセレクタ。
  2. そうでなければ、ユニット入口の仮引数のうち効果の実引数に現れないもの。
- **置き換える予定**: val エンジンが入ったら「MODEL ラベルを持ち、どの slot にも
  入らない入口引数」に置き換える。規則 2 は暫定である。
- **決める時点**: B2（val）完了時。

## Q5. `origin_closure` は `Value.roots` の暫定版

- **状況**: 主語一致は「前向き def-use でその値から導かれる値」を許すが、
  val エンジンが無い段階では代入連鎖の閉包で近似している。
- **実装がしたこと**: `authgap/gateharness.py: origin_closure`。
- **置き換える予定**: `Value.roots`（§2.6 の canonical-alias 表と同じ出所集合）。
- **決める時点**: B2（val）完了時。

## Q6. §8 項目 7（D_op に in-tree の露出宣言を含めるか）が未凍結

- **状況**: 仕様書 §8-7 は「D_op に in-tree の露出宣言（FastMCP `enabled=` ほか）を
  含めるかを第 0 週に凍結する」と書く。前測の実使用は 0 件なので数値影響は
  無い見込みだが、**含める / 含めないを先に決める**ことが要求されている。
- **実装がしたこと**: まだ D パーサを書いていないので未決のまま。
- **推奨**: Def 6 の D_op 節の記述どおり「含める。ただし `enabled=` の式が
  真偽 config atom に解決でき、かつ atom の既定が閉のときのみ」。
- **決める時点**: B5（D パーサ）着手前。学生が決める。

## Q7. §8 項目 1 の (d)（SELECT 格下げ分岐）の扱い

- **状況**: 利用者の上書きにより §8-1 の (a)(b) と F0 の論文性は承認済み、
  (c) 拒否分岐は不要とされた。(d)「SELECT が野外で発火しない場合の格下げ分岐」に
  ついては言及が無い。
- **実装がしたこと**: §3 と §10 が「この条項は撤回しない」と書いているので、
  承認を要さない**仕様内規則**として扱っている。拒否分岐は作っていない。
- **決める時点**: 学生が追認する。

## Q8. 較正対 A1 / A2 の脆弱側の期待タプルが仕様書と食い違う（一次確認済み）

- **状況**: 2026-09-09 に `modelcontextprotocol/servers` を pin して diff を
  目視した結果、A1 と A2 の**脆弱側に検証子が 1 つも存在しない**ことを確認した。
  仕様書 §6 T1.2 は A1 の脆弱側を `weak(prefix_no_canon)`、A2 の脆弱側を
  `weak(no_dash_reject)` と書いている。
- **一次確認の内容**:
  - A1 脆弱側 `9e5d5b8e`: `repo_path = Path(arguments["repo_path"])` の直後に
    `git.Repo(repo_path)` があり、包含検査も正規化子も無い
    （`grep -n 'repo_path' server.py` で全 2 箇所）。
  - A2 脆弱側 `d9c45477`: `git_diff` は `return repo.git.diff(f"--unified={n}", target)`、
    `git_checkout` は `repo.git.checkout(branch_name)` のみ。dash 拒否も
    `rev_parse` も無い。
  - なお `9e5d5b8e`（A1 脆弱側 = A2 修正側）には dash 拒否 + `rev_parse` が
    **既に入っている**。仕様書の A1/A2 の ref 関係と整合する。
- **影響**: 消滅理由は A1 が `normalisation-add` 単独ではなく `validator-add`
  （`validate_repo_path` の新設）。**両側判別可能性は変わらず成立する**ので
  §6 T1.5 の算入数は動かない。
- **もう 1 点**: 仕様書の A2 は `git_checkout` しか挙げていないが、
  同じ修正コミットが `git_diff` にも同じ検証を入れている。両側で変化する
  効果サイトは 1 つではなく 2 つである。
- **実装がしたこと**: `docs/cve_triage.csv` に `expected_tuple_change`（訂正後）と
  `spec_expected_tuple_change`（仕様書の値）を**両方**置いた。
  **仕様書の値を黙って書き換えていない。**
- **決める時点**: 学生が追認し、`AUTHGAP_BRIEF_v3.md` §6 T1.2 を訂正するか、
  triage 表の訂正だけに留めるかを決める。**採点前に決めること**（§6 T1.1 が
  期待タプルの事前凍結を要求している）。

## Q9. 較正対のうち一次確認できているのは 2 対だけ

- **状況**: `docs/cve_triage.csv` の 25 行のうち、ref・diff・両側実行まで
  自分で確認したのは **A1 と A2 の 2 対のみ**（`verified_by_me = sha+diff+two_sided`）。
  残りは仕様書からの転記で `verified_by_me = none`、すなわち**未検証**。
- **したがって**: 「両側通過 11 対」「算入可能 11 対 / 5 プロジェクト」といった
  数を**現時点で論文に書いてはならない**。書けるのは「2 対で両側通過を確認した」
  だけである。
- **決める時点**: §7.6 の D9–D12 に相当する作業。各対について
  `docs/verification_guide.md` の 2.1〜2.3 を実行し、`verified_by_me` を埋める。

## Q10. Def 5 に「正規化後の allowlist」の等級が無い（A18 で実際に当たった）

- **状況**: A18（langroid `SQLChatAgent`）の修正は
  `sqlglot.parse(query)` で正規化してから `type(stmt).__name__.upper() in allowed`
  で文型 allowlist を掛ける。Def 5 の等級語彙は
  `strong-path`（パス）/ `strong-token`（シェルトークン）/
  `strong-enum`（Def 6 の執行表で執行される値域）/ `strong-eval`（任意）/
  `weak(19 語)` / `unknown` で、**この形に当たる語が無い**。
  weak の 19 語も `denylist_enum` / `regex_denylist` は拒否リスト側で、
  allowlist 側の語ではない。
- **仕様書自身も未決**: A13 の行に「`sqlglot` を Def 5 の正規化子カタログに
  載せた場合に限り算入する」とあり、sqlglot の扱いは決まっていない。
- **実装がしたこと**: 等級は `unknown`（判定不能）とし、**語彙外の等級を作らない**。
  会員判定が束縛したことは manifest の `gate.candidates[]` に
  `value_grade: "allowlist"` と config atom 情報つきで残る。
  A18 の両側判別は `grade: None -> unknown` の変化で成立する。
- **決める時点**: 月 6 のゲート語彙凍結の前。選択肢は 3 つ —
  (a) `sqlglot` を正規化子カタログに載せ SQL 版の `strong-*` を新設する、
  (b) weak の 19 語に allowlist 側の語を足す、
  (c) `unknown` のままにして「SQL 文型 allowlist は等級づけの対象外」と限界節に書く。
  **(a) と (b) は語彙の拡張なので、凍結前でなければできない。**

## Q11. config atom の 4 源のうち「コンストラクタ kwarg」がまだ読めない

- **状況**: Def 5 の config atom の源は 4 種（コンストラクタ kwarg / モジュール定数 /
  `os.environ` / CLI 既定値）だが、実装が解決できるのは**モジュール定数と
  `os.environ` の 2 源**だけである（`authgap/gate.py: resolve_atom`）。
- **実際に当たった例**: A18 の `SQLChatAgentConfig.allowed_statement_types`
  （pydantic のクラス既定値）と `allow_dangerous_operations`。読めないので
  `req_val` が MODEL のままになり、A18 の両側差は grade だけになった。
- **影響**: `config-conditional(atom, default)` による `req` の引き上げが
  過小評価される。**方向は保守側**（GAP を多めに出す）なので false-clean は
  起きないが、A14 のような「既定閉 config atom の実例」は等級が出ない。
- **決める時点**: B3b の完了前。`_self_fields` が既に `__init__` を解析して
  いるので、同じ機構でコンストラクタ kwarg と CLI 既定値を足せる。

## Q12. 低レベル MCP サーバの `trig` は `assumed` ではなく `traced`（測定で判明）

- **仕様書の想定**（§3 / §10）: 「MCP サーバでは dispatch が framework 内に
  あるので trig は常に `assumed` になり、SELECT は原理的に発火しない。
  したがって野外母集団を MCP サーバだけにすると交差行は fixture と自作
  ケーススタディからしか出ない」。
- **測定した結果**: **低レベル経路（`@server.call_tool()` / `Server(on_call_tool=)`）
  では `traced` になる。** ハンドラが解析対象の木の中にあり、`match name:` /
  `if name == ...` の分岐が木内で読めるので、セレクタ → ディスパッチ → callee の
  連結経路が見える。`corpus/A1__vuln`（mcp-server-git）では 3 ユニットすべてが
  `traced` で、交差行が 5 行出た。
- **`assumed` になるのは**: 高レベル `@mcp.tool`、langroid の `ToolMessage` 形、
  `tools=[f, g]` の裸の関数。いずれもディスパッチが SDK の中にある。
  `corpus/A18__fixed` では 138 ユニットすべてが `assumed` で交差行 0。
- **したがって仕様書の 2 か所に影響がある**:
  1. §3 の「MCP サーバだけにすると交差行は fixture からしか出ない」は
     **高レベル経路についてのみ正しい**。
  2. §10 の B1 関門「T3-app の traced 率 ≥ 20%」— 低レベル MCP サーバ自体が
     traced ユニットを供給するので、T3-app（第二母集団）に頼らずに
     traced 率を満たせる可能性がある。**SELECT の格下げ分岐が発火しないかも
     しれない。**
- **決める時点**: B1 完了時に `traced_ratio` を母集団別（高レベル / 低レベル /
  ツールパッケージ）に出して確かめる。**母集団を分けずに 1 つの traced 率を
  出すと、この構造差が平均で消える。**
- **現時点の交差行**: 12 行 / **1 プロジェクト**。§3 は「3 行が異なる
  プロジェクト由来」を要求するので**不合格**。低レベル MCP サーバをもう
  2 プロジェクト足して測り直すこと。
