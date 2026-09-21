# 母集団 v2（宣言あり）と旧枠（import 文の code search）の比較

**本文の主表の下書き。** 値はすべて `evidence/` の run から転記し、出典を列に書く。
仕様書からの転記値は含まない。分母の定義は `docs/preregistration.md` §2.2 / §2.7 / §2.8。
母集団の変更は旧枠の結果を見た後の決定（D29、post-hoc）。

| 指標 | 母集団 v2（宣言あり、87 木） | 旧枠 mcp_server（60 木） | 出典 |
|---|---|---|---|
| 母集団の定義 | `annotations=ToolAnnotations(` / dict 形の宣言を自前コードに持ち、宣言ファイルが `mcp` / `fastmcp` を import する公開 Python repo（3,827） | `from mcp.server` 等の import 文で code search に掛かった repo（2,299、上限つき） | `docs/population_v2.md`、`docs/population.md` |
| ユニット / 危険ユニット | 2,231 / 1,027 | 1,669 / 431 | `evidence/f0a_v2_run1`、`evidence/f0a_run6` |
| annotation 保有ユニット | 1,603（71.8%） | 1（同梱 SDK のテスト） | 同上、D28 |
| **r_D**（上界を動かす明示 / 危険ユニット） | **53.3%**（547/1,027） | 0.0% | D30、O15 |
| 明示フィールド 1 つ以上（openWorldHint 単独を含む、併記） | 80.0%（822/1,027） | 0.0% | D30 |
| §10 の分岐 | 1（主張を維持） | 3（P0 と D_prev へ） | D30、D27 |
| validator 保有（主分母 dangerous_fp_excluded × all_paths） | 3.51%（36/1,027）× | 12.06%（52/431）○ | `scripts/denominators.py` |
| validator 保有（all_units × all_paths） | 3.77% × | 4.43% × | 同上 |
| validator 保有の関門（6 分母） | 6/6 で × | 4/6 で ○ | 同上、O7 |
| NET 以外の危険効果を持つユニット（§2.10） | **186 / 1,027**（NET のみ 841） | 214 / 431（NET のみ 217） | `scripts/denominators.py`（`dangerous_non_net`） |
| validator 保有（dangerous_non_net × all_paths、§2.10 併記） | **18.3%**（34/186）○ | 14.0%（30/214）○ | 同上 |
| in_tree_resolution_ratio（サイト） | 21.7% × | 19.3% × | `docs/f0a_v2_run1.md`、`docs/f0a_run6.md` |
| opaque 率（主 slot、サイト） | 54.7% × | 45.3% × | 同上 |
| tree budget（180 s）で飛ばしたユニット | 716 | （run6 の値は `trees.jsonl` の `units_skipped_by_tree_budget`） | `evidence/f0a_v2_run1/f0a.json` |
| **tree budget 900 s の再走（感度、D34）**: ユニット / 危険ユニット | 2,947 / 1,193（飛ばし 0。増分 716 / 166 は**すべて 1 木** `david-li0406/meta-skill-evloving`） | — | `evidence/f0a_v2_run2_budget900` |
| 同、validator 保有（主分母） | **8.38%**（100/1,193）○。木単位 95% 区間 [1.5%, 26.7%]（境界）。当該 1 木を除くと 3.51%（36/1,027、run1 と同値） | — | D34 |
| 同、validator 保有（all_units） | 6.11%（180/2,947）○。区間 [2.2%, 10.3%]（境界） | — | `scripts/f0a_ci.py` |
| 同、validator 保有（dangerous_non_net） | 30.3%（86/284）○ | — | `scripts/denominators.py` |
| **解析器 38531e7（D35、受け手型の修正）での取り直し**: ユニット / 危険ユニット | 2,231 / 1,169（+142、外れた 0） | — | `evidence/f0a_v2_run3`、`scan_v2_run4`、D35 |
| 同、validator 保有（主分母 / all_units / non_net） | 4.11% × / 3.77% × / 17.4% ○（分子は同じ、分母が増えた） | — | `scripts/denominators.py` |
| 同、r_D | 51.1%（分岐 1） | — | `docs/f0a_v2_run3.md` |
| 同、CONTRADICTION（ユニット × site） | 79（16 木。+7、すべて cohort の `Path.write_text`） | — | `evidence/scan_v2_run4/contradictions.json` |
| 決定論（`scan --determinism 3`、87 木） | 85 木で 3 回一致。1 木 OOM（未測定）、1 木は壁時計 cap の印 `TRUNCATED(wall_clock)` の有無だけが違う（解析結果は同じ） | run6: `docs/f0a_run6.md` | `evidence/determinism_v2/README.md` |
| 直前リリースを持つ木 | 34/87 = 39.1% | 8/60 = 13.3% | `docs/prev_releases_v2.json`、D23 |
| r_prev（適用木の危険ユニット） | 93.9%（169/180） | 87.7%（71/81） | D31、D27 |
| r_prev（5 リリース前、感度） | 65.6% | 86.4% | 同上 |
| r_prev（無条件、全木の危険ユニット） | 16.5% | 23.1%（98 木、3 母集団） | 同上 |
| §10 の「方向を疑う 3 連言」 | 不発火（r_D 偽、r_prev 偽、validator 真） | 不発火（事前登録の分母）/ 併記分母で 2 母集団発火 | D31、D27 |
| full scan の行 | 4,804（UNKNOWN 2,549 / GAP_INJECT 197 / GAP_SELECT 232 / CONTRADICTION 142） | 未実施（旧枠は F0a のみ） | `evidence/scan_v2_run3/summary.json` |
| CONTRADICTION（ユニット × site） | **72（16 木）**: readOnly に反する 48（8 木）、destructiveHint=false に反する削除・上書き 24（12 木） | 0（宣言が無い） | D32 |
| INVENTORY / GAP_SELECT の木 | 0 / 5（デコレータ形は trig が assumed） | — | D31 |
| 低レベルハンドラの join（O5） | 4 ユニット、55 ツール、明示 0 | — | D30 |
| ユニット 0 件の木（枠の雑音） | 7/87 | run6 の値は `docs/f0a_run6.md` | |

## 読み（本文の候補）

1. 宣言を持つ母集団では「宣言 D と実効 M の差」に主語があり、危険ユニットの半分以上が
   上界を明示する。旧枠（分岐 3）との対比が母集団変更の主な所見。
2. 差の現れ方は SELECT 座標ではなく **CONTRADICTION**（明示宣言に反する書き込み /
   削除 / 実行）と INJECT 行の `D_layer_present`。FastMCP デコレータ形は木内に
   モデル側の dispatch が無いため trig が assumed になる（設計どおり）。
3. 宣言はあるが値検証は少ない（validator 保有 3.5%）。「宣言する成熟したサーバは検証子も
   丁寧」という選択効果はこの標本では逆。**ただし分母の 8 割（841/1,027）は NET だけを
   持つユニット（API のラッパ）で、NET を除いた危険ユニットに限ると 18.3% になり関門を
   通る**（§2.10 の併記分母。主分母は変えない）。宣言する母集団は「外部 API を叩く
   サーバ」に偏っており、ファイル / コマンド系のサーバは 186 ユニット。
4. 解析器の解決限界（opaque 率、in-tree 解決率）は母集団で変わらない。
5. **validator 保有の関門は 1 木で決まる。** 180 s の budget で飛ばした 716 ユニットは
   すべて `david-li0406/meta-skill-evloving`（36,900 の .py を持つスキル集）のもので、
   900 s で解析すると主分母の validator 保有が 3.5% → 8.4% に動き関門を通る。
   この 1 木を除くと run1 と同値（3.5%）。木単位のブートストラップ区間は両 run とも
   閾値を跨ぐ（境界）。**点推定の合否を主張しない**（D18 の規則）。

## まだ無いもの

- 人間が再現した数値（`docs/verification_log.csv` 無し）。CONTRADICTION 72 件の手検証が最初。
- tree budget 900 s の再走と決定論チェックは済んだ（上の表、D34）。
- 第二ラベラー、κ。
