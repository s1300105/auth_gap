# 母集団 v2: 宣言（MCP ToolAnnotations）を持つ公開 Python MCP サーバ

**列挙する前に書く**（2026-09-20）。列挙後に定義・除外規則・seed を変えない。
変えるなら `docs/preregistration.md` §5 に逸脱として記録する。

学生の決定（`docs/decisions.md` D29）: 母集団は宣言のあるものだけにする。
宣言を持つプロジェクトの比率は論文に明記するが、今回の主目的ではない。
**旧枠（`docs/population.md`、import 文の code search）は捨てず、「long tail には
宣言が無い」という対照として残す。** 母集団の変更は旧枠の r_D = 0.0% を見た後の
決定であり post-hoc（`docs/preregistration.md` §0）。

## 定義

公開 GitHub リポジトリで、次をすべて満たすもの:

1. **宣言の存在**: `.py` ファイルに MCP ツール宣言の呼び出し形が少なくとも 1 つある。
   - 形 A: `annotations=ToolAnnotations(`（SDK の `ToolAnnotations` モデル）
   - 形 B: `annotations={` と `readOnlyHint` を同じファイルに含む（dict 形。
     FastMCP 2 系が受け付ける）
   形 A / B 以外（変数経由 `annotations=spec.annotations`、レジストリのデータ構造、
   OpenHands の `ToolDefinition`）は**列挙の手段では拾えない**ので母集団に入らない。
   これは母集団の定義の一部であり、欠陥として後から足さない。
2. **Python の MCP サーバであること**: 宣言を含むファイルが `mcp`（公式 SDK）または
   `fastmcp` から import している。取得後に確認し、満たさないものは
   「宣言はあるが MCP サーバでない」として件数を出して除く。
3. **除外**（取得後、規則を先に固定）:
   - `modelcontextprotocol/python-sdk` 自身、およびそのミラー / 同梱コピー
     （宣言を含むファイルのパスが `site-packages` / `node_modules` / `.venv` /
     `vendor` 配下、または `mcp/types.py` `mcp/server/` の複製）
   - 宣言を含むファイルが `tests` / `test` / `examples` / `docs` 配下**にしか**無い
     もの（`scripts/denominators.py: NON_SRC_DIRS` の path_class = non_src のみ）。
     **自前のサーバ本体に宣言があることを要求する。**
   - fork（code search の既定で除外される）、アーカイブ済み（取得時の metadata で判定）
   - 旧枠の標本と重複する repo は**残す**（対照との重なりは注記する）

## 列挙の手段

GitHub code search（REST、`docs/population.md` と同じ手段）。1 クエリ 1000 件の
上限があるので **`size:` の範囲で分割**し、各分割の `total_count` が 1000 未満に
なるまで細分する。分割境界と各分割の件数を `evidence/population_v2/enumeration.json`
に記録する。取得日時（UTC）を記録する。

- クエリ A: `"annotations=ToolAnnotations(" language:Python size:<lo>..<hi>`
- クエリ B: `"annotations={" "readOnlyHint" language:Python size:<lo>..<hi>`
- 結果はファイル単位。**repo の full_name で重複を除く**（大文字小文字を無視）。
- `total_count` は参考値（fork / 複製を含む）。母集団の数は重複除去後の repo 数。

## pin と抽出

- 列挙で得た repo の default branch の HEAD を、**取得時**に `git ls-remote` で
  SHA に固定し `docs/corpus_sample_v2.json` に書く（旧枠の O9 = 全件 `HEAD` の
  問題を最初から避ける）。
- 抽出: 母集団（除外前の列挙結果）が 100 を超えるなら **seed = 20260920** で
  100 件を無作為抽出し、取得・除外の順に処理する。除外で減った分は補充しない
  （分母の記録を優先する）。100 以下なら全数。
- 抽出前に母集団の規模を仕様書の関門（≥ 300、§9-6）と照らす。届かない場合も
  列挙結果はそのまま使い、届かなかった事実を書く。

## 測るもの

旧枠と同じ F0a（`scripts/f0a.py`）、`r_D`（新しい join 規則 §2.9 を含む）、
validator 保有（§2.2 の 6 分母）、`r_prev`（§2.7）、full scan。**すべて旧枠の
値と並べて報告する**（母集団の差が値をどれだけ動かすかが、この変更の主な所見）。

## 書けること / 書けないこと

- 書ける: 「宣言を持つ公開 Python MCP サーバについて」の値。
- 書けない: 生態系全体への一般化。「宣言を持つ」で選ぶと検証子も丁寧な repo に
  偏りうる（選択効果）。旧枠の値がその対照になる。
