# §3 の交差行（統一の唯一の証拠）と trig の内訳

再現: `python scripts/intersection_rows.py evidence/scan_v2_run4`

**この表は 3 腕アブレーションの値ではない。** §3 が与えた特徴づけ
（同一行が SELECT 系と INJECT 系の verdict を同時に持つ）で数えた**候補**である。
数える単位は (ユニット, site, slot)。効果行は呼び出し経路ごとに複製されるため
（`docs/open_questions.md` O18）、行をそのまま数えない。

| 項目 | 実測 | §3 の条件 | 判定 |
|---|---|---|---|
| 交差行の候補 | 5 | 3 以上 | ○ |
| 由来プロジェクト数 | 2 | 3 以上 | × |
| `trig = traced` のユニット | 14 / 2231 = 0.6% | 20% 以上 | × |

**§3 の格下げ条項が発火している。** 仕様書の文言: 「traced 率が 20% 未満なら
SELECT の野外評価は成立しないので、その時点で SELECT は fixture + ケーススタディのみの
構造的主張に格下げする。**この条項は撤回しない。**」

## 由来

- `v2-ariffazil__wealth`（1 行）
  - `wealth_fx_rate` / `httpx.AsyncClient.get` / slot `url.query`
- `v2-fanfan-de__anybox`（4 行）
  - `KeynoteMCPServer._register_handlers.call_tool` / `glob.glob` / slot `path`
  - `KeynoteMCPServer._register_handlers.call_tool` / `shutil.move` / slot `path`
  - `KeynoteMCPServer._register_handlers.call_tool` / `shutil.rmtree` / slot `path`
  - `KeynoteMCPServer._register_handlers.call_tool` / `subprocess.run` / slot `argv[*]`

## 決定

`docs/decisions.md` D36: 統一主張と等級づけによる判別は主張から降ろし、
「宣言 D と実効 M の照合」1 本を主軸にする。D10 の二択は格下げ分岐を採る。
