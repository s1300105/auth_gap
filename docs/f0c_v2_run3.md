# F0c（前身の 4 条件を新規に測る）

**F0c-1（A5 の run で測る）**

| 条件 | 測定量 | 値 |
|---|---|---|
| (iii) ツール本体が別プロセス / HTTP の向こうにある率 | `resolution.remote` [mcp_server] | 0.0% |
| (iv) 無ガードのシェル実行が仕様である率 | `rubric1c` [mcp_server] | 0/0 = — |

**(ii) framework 境界で型が消える率は AuthGap では測定不能**（型環境を構築しないため）。**別の量を (ii) の名前で報告してはならない。**

**(i) dispatch キーが in-tree で解決する率**（`traced_ratio` と
`registry_resolution_ratio`）は **B1 完了後の別 run**で測る。
F0c の完成は B1 完了時点である。

§1 が F0c に負わせている callee 側反転の正当化は (i)+(iii) と §1.5 で行う。

