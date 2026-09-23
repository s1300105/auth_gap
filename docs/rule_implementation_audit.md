# 事前登録した規則が実装されているかの点検（2026-09-23、D47）

**きっかけ**: D46 で、`scripts/intersection_rows.py` の docstring に
「`OPAQUE` 行は数えない」と書いてありながら**実装していない**ことが分かった。
しかも食い違いの向きが主張に有利で、あやうく事前登録した判断（D36）を
巻き戻すところだった。**同じ食い違いが他にもないかを点検した。**

## 点検の手続き（再現できる形で書く）

1. `AUTHGAP_BRIEF_v3.md` を「数えない / 含めない / 除く / に限る / 算入しない」で検索し、
   **除外・限定の規則を 14 件**抽出した。
2. そのうち**実装があり機械的に照合できるもの**を選び、実装を読んで規則と突き合わせた。
3. 食い違ったものは母集団 v2（`evidence/scan_v2_run5`）で**影響の大きさを測った**。

**網羅的な点検ではない。** 手作業の項目（κ、ラベリング、較正対の選定）と
実装が無い項目（D_dom のパーサ）は対象外である。

## 結果

| # | 仕様の行 | 規則 | 実装 | 判定 |
|---|---|---|---|---|
| 1 | 553 | 交差行から `OPAQUE` 行を除く | `scripts/intersection_rows.py` | **不一致だった → D46 で修正** |
| 2 | 320 | `r_kind` の分子は上界を動かすフィールドだけ | `authgap/dparse.py: d_kind_from` | **一致**（10 例で確認） |
| 3 | 322 | snake_case は `D_malformed` として別行で報告 | `authgap/entries.py` / `dparse.py` | **不一致だった → D48 で修正（130 ユニット / 2,231）** |
| 4 | 1118 | 解決できない `.execute()` は `db_unresolved` として**記録**し危険効果に数えない | `authgap/effects.py` | **不一致だった → D49 で修正。記録した結果 2,078 件あり、75% が本物の SQL（O29）** |
| 5 | 322 | 未 join 行は D にも CONTRADICTION にも寄与させない | `authgap/entries.py: join_annotations` | **一致**（`(joined, unjoined)` を返す） |
| 6 | 7-8 | D_dom のパーサは書かず `r_dom = 0` と報告 | `scripts/f0a.py:262` | **一致** |
| 7 | 632 | `self_granted` は weak 理由語彙ではなく `downgrade` | `authgap/catalog/validators.py` | **一致**（`WEAK_REASONS` に無く `DOWNGRADES` にある） |
| 8 | 282 | `dash_rejected` のような制御述語由来の事実は val の出力に含めない | `authgap/ir.py: VALUE_ATTRS` | **一致**（8 語に無い） |
| 9 | 344 | D_dom の被覆判定は Def 3 の制御位置に限る | — | **対象外**（パーサを書いていない） |

**9 件を照合し、2 件の不一致（#3 / #4）が新たに見つかった。**

---

## O27（#3）— snake_case の注釈が記録されない

**仕様 322 行目:**

> snake_case 表記（`read_only_hint` 等、前測で 21 エントリ）は `ToolAnnotations` に
> deserialize されず protocol に届かないので **`D_malformed` として別行で報告する**。

**実装:**

* `authgap/entries.py: _read_annotations` は snake_case を集めて 3 つ目の戻り値で返す。
* しかし**デコレータ経路（`entries.py:403`）は `_malformed` を捨てている**
  （`ann, ann_form, _malformed = _read_annotations(ann_node)`）。
* `ToolLiteral.malformed_fields` は定義されているが**どこからも読まれていない**。
* `DKind.malformed` を設定する箇所が無い（`meet_d_kind` が他の `DKind` から
  和を取るだけ）。**したがって構造的に常に空である。**

**母集団 v2 での実数:**

| キー | 箇所 |
|---|---|
| `read_only_hint` | 195 |
| `destructive_hint` | 174 |
| `idempotent_hint` | 159 |
| `open_world_hint` | 46 |
| **合計** | **574 箇所 / 11 木（87 木中）** |

manifest に `malformed` が出ているユニット: **0**。

**仕様の前測は「21 エントリ」だったが、母集団 v2 では 574 箇所ある。**

**誤りの向き**: 誤 clear ではない（snake_case は正しく上界を動かさない）。
**失われているのは測定である。** `read_only_hint: True` と書いたツールは
「読み取り専用のつもりで宣言したが protocol に届いていない」という**具体的な失敗形**
であり、「宣言はどれだけ当てにならないか」という本研究の問いに直接効く。
**それが注釈なしのツールと区別できていない。**

---

## O28（#4）— `db_unresolved` が記録されずに消える

**仕様 1118 行目:**

> 受け手が Def 3 の proxy カタログの DB 受け手型に局所代入で解決できる場合のみ DB 効果とする。
> 解決できない `.execute()` は **`db_unresolved` として記録し**、危険効果に数えない
> （`effect_fp_audit.db_only_non_db_execute` の分子）。

**実装（`authgap/effects.py:558-562`）:**

```python
db_rule = None
if kind == "DB" and method in ("execute", "executemany"):
    db_rule = db_execute_rule(frozenset(getattr(ev.receiver.shape, "classes", ())))
    if db_rule != "db":
        return None          # ← 効果ごと捨てる
```

**「危険効果に数えない」は満たしている。** しかし `return None` で `Effect` を作らないので、
`db_rule == "db_unresolved"` の効果は**存在しない**。

`authgap/report.py:169` の

```python
elif e.db_rule == "db_unresolved":
    db_only_non_db += 1
```

は**到達不能**であり、`effect_fp_audit.db_only_non_db_execute` は**構造的に常に 0**。
母集団 v2 の manifest でも `db_unresolved` の効果行は **0 件**。

**誤りの向き**: 仕様が要求した FP 監査の分子が常に 0 になるので、
**「DB の判定に曖昧さは無かった」と読める出力を出している。** 実際には
受け手型が解決できない `.execute()` は黙って消えており、**その中に本物の DB 書き込みが
あっても分からない。** CLAUDE.md 規則 4（解決できなかったものは不明として記録する。
黙って安全側に倒さない）に反する。

---

## 教訓

**「規則を docstring / 仕様書に書いた」ことと「規則を実装した」ことは別である。**
3 件の食い違い（D46 の交差行、O27、O28）はいずれも

* 規則の文言は正しく書かれていて、
* 実装が一部だけ、または逆向きで、
* **出力を見ても食い違いが分からない**（0 が出ているのが「該当なし」なのか
  「数えていない」のか区別できない）

という形だった。**対策は「除外したもの・落としたものの件数も出力する」こと。**
D46 で `intersection_rows.py` に `n_excluded_opaque` を足したのはこのためである。
O27 / O28 を直すときも同じ形にする。
