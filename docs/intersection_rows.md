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
| `corpus/A9__vuln` | MervinPraison/PraisonAI | 49 | 0 |
| `corpus/A9__fixed` | MervinPraison/PraisonAI | 49 | 0 |
| `corpus/A18__vuln` | langroid/langroid | 14 | 0 |
| `corpus/A18__fixed` | langroid/langroid | 14 | 0 |

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

## 単一座標のゲート寄与（**交差行ではない。別表**）

§3 が明記するとおり、(i) callee の `confirm()` が SELECT を clear する / 
(ii) caller の承認 hook が `req_val` を引き上げる、はそれぞれ腕 B のみ・
腕 A のみとしか差が出ないので**定義上 0 行**であり交差行に数えない。
ここには「腕 A とだけ差が出た行 / 腕 B とだけ差が出た行」の件数を出す。

| プロジェクト | 腕 A とだけ差 | 腕 B とだけ差 |
|---|---|---|
| MervinPraison/PraisonAI | 13 | 3 |
| langroid/langroid | 9 | 0 |
| modelcontextprotocol/servers | 0 | 18 |
