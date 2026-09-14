# 母集団（§9-6 / §10 の最初の関門）

関門: **重複除去後の Python MCP サーバが 300 件以上**。
**この関門だけは A5 まで待てない**（待つと 98 木を取り直すことになる）。

**重複除去の単位は GitHub リポジトリ**（`owner/name` を小文字化）。
1 リポジトリが複数の PyPI プロジェクト / 複数サーバを出荷していても 1 件。
リポジトリ URL が取れない配布物は別カウントで報告し 300 の判定に含めない。

再現: `python scripts/fetch_frame.py`

## 試行した手段（優先順。**失敗も記録する**）

| 順 | 手段 | 件数 | 成否 | 取得日時 | 備考 |
|---|---|---|---|---|---|
| 1 | libraries.io dependents | 0 | × | 2026-09-14T13:07:43+09:00 | LIBRARIES_IO_API_KEY が無いので試行不能。**「試さなかった」ではなく「鍵が無くて試せなかった」と記録する。** |
| 2 | PyPI BigQuery distribution_metadata.requires_dist | 0 | × | 2026-09-14T13:07:43+09:00 | `bq` CLI が無いので試行不能（GCP の課金プロジェクトも要る）。**「試さなかった」ではなく「環境が無くて試せなかった」と記録する。** |
| 3 | GitHub code search | 2299 | ○ | 2026-09-14T13:07:43+09:00 |  |

## クエリ

**GitHub code search**

- `"from mcp.server" language:Python`
- `"@mcp.tool" language:Python`
- `"from mcp.server.fastmcp" language:Python`
- `"server.call_tool" language:Python`

## 判定

**採用: GitHub code search（2299 件 ≥ 300）。関門を通過。**

**採用手段は PyPI 逆依存ではない。** したがって母集団の定義は
「PyPI 上の `mcp` / `fastmcp` 依存者」ではなく**「公開 Python MCP サーバ」**である。
この差を本文に明記すること（§9-6 の要求）。

GitHub code search は 1 クエリあたり最大 1000 件しか返さないので、
**得られた件数は母集団の下限である**（`total_count` は信用しない）。
関門は「≥ 300」なので下限で判定できるが、**母集団規模そのものを
論文に数として書くときはこの上限を併記する。**

