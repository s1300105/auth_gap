# 交差行（§3 の 3 腕アブレーション）

**統一の唯一の証拠。** trig / val / gate は伝播機構を共有しないので、
3 座標のうち 2 つを同時に必要とする行が実在しなければ「一つの解析」とは
書けない。3 腕は `authgap/analyze.py` の `arm` 引数によるフラグ違いであり、
**別実装ではない**（§3 の要求）。

再現: `python scripts/ablation.py <木> [<木> ...]`

- 交差行 **12** 行 / **1** プロジェクト
- 事前登録した閾値 **3**（**経験的根拠は無い。事前に固定することだけが根拠である**）
- 判定: **不合格**

数えない行: `UNKNOWN` を含む行（OPAQUE 行）、`Leak` だけで説明できる行、
D だけで説明できる行（INVENTORY / CONTRADICTION / GAP_DRIFT のみ）、
fixture 由来と自作ケーススタディ由来。

## 木ごとの内訳

| 木 | プロジェクト | 行数 | 交差行 |
|---|---|---|---|
| `corpus/A1__vuln` | modelcontextprotocol/servers | 19 | 5 |
| `corpus/A2__vuln` | modelcontextprotocol/servers | 19 | 6 |
| `corpus/A3__vuln` | modelcontextprotocol/servers | 19 | 1 |
| `corpus/A5__vuln` | Significant-Gravitas/AutoGPT | 21 | 0 |
| `corpus/A5__fixed` | Significant-Gravitas/AutoGPT | 25 | 0 |
| `corpus/A9__vuln` | MervinPraison/PraisonAI | 49 | 0 |
| `corpus/A18__vuln` | langroid/langroid | 14 | 0 |

## 交差行

| 行 | プロジェクト | V_A | V_B | V_C |
|---|---|---|---|---|
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|FS_WRITE@git.IndexFile.add|path` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.add|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.checkout|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.log|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.status|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|FS_WRITE@git.IndexFile.add|path` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.add|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.checkout|argv[*]` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.checkout|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.log|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|SPAWN@git.Git.status|cwd` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |
| `mcp-lowlevel-v1:serve.call_tool:965af40077db|FS_WRITE@git.IndexFile.add|path` | modelcontextprotocol/servers | GAP_SELECT | GAP_INJECT | GAP_INJECT,GAP_SELECT |

## 交差行がどこから出るか（測定で分かったこと）

交差行が出るのは **`trig` が `traced` のユニット**に限る。SELECT 座標が
発火しなければ「同一行が SELECT 系と INJECT 系を同時に持つ」形が作れない。

測定した範囲では `traced` になるのは**低レベル MCP の
`@server.call_tool()` 形だけ**である。ハンドラが解析対象の木の中にあり、
`match name:` / `if name == ...` の分岐が木内で読めるので、
セレクタ → ディスパッチ → callee の連結経路が見える。

一方で次はすべて `assumed` になり、交差行に寄与しない:

- 高レベル `@mcp.tool`（ディスパッチが SDK の中）
- langroid の `ToolMessage` 派生 + 同名ハンドラ（同上）
- `tools=[f, g]` に渡す裸の関数（同上）

**これは仕様書 §3 の想定と食い違う。** §3 は「MCP サーバでは dispatch が
framework 内にあるので trig は常に `assumed` になり、SELECT は原理的に
発火しない」と書くが、**低レベル経路では発火する**。仕様書の主要較正
プロジェクト（mcp-server-git）自身が低レベル経路である。
詳細は `docs/open_questions.md` Q12。

## 単一座標のゲート寄与（**交差行ではない。別表**）

§3 が明記するとおり、(i) callee の `confirm()` が SELECT を clear する / 
(ii) caller の承認 hook が `req_val` を引き上げる、はそれぞれ腕 B のみ・
腕 A のみとしか差が出ないので**定義上 0 行**であり交差行に数えない。
ここには「腕 A とだけ差が出た行 / 腕 B とだけ差が出た行」の件数を出す。

| プロジェクト | 腕 A とだけ差 | 腕 B とだけ差 |
|---|---|---|
| MervinPraison/PraisonAI | 13 | 0 |
| Significant-Gravitas/AutoGPT | 7 | 0 |
| langroid/langroid | 9 | 0 |
| modelcontextprotocol/servers | 0 | 18 |
