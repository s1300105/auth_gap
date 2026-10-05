# 練習の答え合わせ（v4 の判定）

> **練習を全部終えてから開く。** ここにあるのは v4 のときに**本記録者（AI）が判定した結果**で、正解ではない。
> しかも D76 より前の規則での判定なので、D76 の規則では答えが変わるものがありうる（例: 条件の種類、ラベル）。
> 食い違ったら、どちらが**今の手引き**に合っているかを考える。手引きが曖昧で食い違ったなら、それを教えてほしい（封の前に直せる）。

| 練習の id | v4 の id | 種類 | 宣言 | v4 の判定 | v4 の誤の原因・見落としの原因 |
|---|---|---|---|---|---|
| P-C01 | M05 | 矛 | D1 | 誤 | 解析器の読み違い: 組み込みの set() を末尾名で CacheManager.set に解決した |
| P-C02 | M07 | 矛 | D1 | 誤 | 到達しない: 効果は server._init の中の起動時処理だけにある。_ensure_global_playbook / _ensure_playbook は大域変数が None のときだけ _init() を呼ぶが、唯一の起動口 main() が mcp.run の前に _init(args.project) を済ませるので、ツール呼び出しの時点では None にならない |
| P-C03 | M08 | 矛 | D2 | 誤 | 到達しない: server._init 内の起動時処理。_get_project_memory(None)→_ensure_memory は _memory が None のときだけ _init を呼ぶが、main() が起動時に _init を済ませる |
| P-C04 | M12 | 矛 | D2 | 誤 | 宣言に反しない: ツール自身が同じ呼び出しで作ったロックファイル（path + '.lock'）の後始末の unlink。既にあったデータを消す・変える動作ではない（v3 の誤『同じ呼び出しで作った一時ファイルの削除を破壊的とみなす』と同じ類） |
| P-C05 | M13 | 矛 | D1 | 正 |  |
| P-C06 | M16 | 矛 | D1 | 正 |  |
| P-C07 | M48 | 矛 | D1 | 正 |  |
| P-C08 | M49 | 矛 | D2 | 正 |  |
| P-M01 | R09 | 見落とし | D1 | 解析器が不として出している |  |
| P-M02 | R16 | 見落とし | D1 | 見落とし | その他 |
| P-M03 | R20 | 見落とし | D1 | 反する動作は無い |  |

## v4 の根拠（evidence）

- **P-C01**（v4 の M05）: src/rails_lens/tools/migration_context.py:260-380: the migration_context body does not call cache.set; cache is unpacked at L263 and never used. The call that the witness_chain ['CacheManager.set'] points at is seen: set[str] = set() at L332. The write it leads to, cache/manager.py:90 open(path,'w'), is not reachable from this tool. grep.search, bridge.execute, _parse_schema_for_table and _parse_migration_file contain no writes either (the only other writes are in analyzers/reverse_index_builder.py, which only screen_map uses).
- **P-C02**（v4 の M07）: ccr/mcp/server.py:210-215 の os.remove(session_marker) は _init の中（138 行〜）にしかない。ace_tools.py:84-85 は _srv._ensure_global_playbook() / _ensure_playbook() を呼び、server.py:541-583 は `if _global_playbook is None: _init()` の形。main()（server.py:659-700）が 678 行で _init(args.project) を呼んでから 700 行で mcp.run。サーバの起動口は pyproject.toml:68 / ccr/mcp_server.py の main だけ（mcp.run は他に無い）
- **P-C03**（v4 の M08）: 唯一の証人連鎖は _get_project_memory→_ensure_memory→_init→server.py:212（os.remove(session_marker)）。_ensure_memory は server.py:549-554 で `if _memory is None: _init()`。main() は server.py:678 で _init を呼んでから 700 行で mcp.run。_memory は _init の 153 行目付近で先に代入される
- **P-C04**（v4 の M12）: ccr/core/memory_pkg/memory_file_io.py:88-113 の _file_lock: 102 行で open(lock_path, 'w') で作り、flock を外したあと 111 行で os.unlink(lock_path)。連鎖は add_discussion→get_active_branch→_read_file→_file_lock で、読み取りのためのロックでも毎回作って消す
- **P-C05**（v4 の M13）: gcc_search_tools.py:94-110: gcc_recall は毎回 RecallEngine(mem).recall(...) の後に append_audit(mem.ccr_root, 'memory_read', ...) を呼ぶ。governance.py:206 で <project>/.ccr/governance_audit.jsonl を 'a' で開いて追記（ccr_root は memory_init.py:49 で <root>/.ccr なので basename の検査を通る）。recall.py:186 は毎回 RecallTraceStore.append_trace を呼び、replay.py:103 で recall_traces.jsonl に追記
- **P-C06**（v4 の M16）: gcc_tools.py:463-467: level >= 2（既定値は 2）で scratchpad にエントリがあれば scratchpad.format_for_context() を呼ぶ。scratchpad.py:229-234→list_entries（140-162）は期限切れのエントリを消し、_save() で .ccr/scratchpad.json を tmp に書いてから os.replace で上書き（scratchpad.py:84）
- **P-C07**（v4 の M48）: reaper_mcp_server.py:598-602 get_master_track は ToolAnnotations(readOnlyHint=True)。本体は reaper_call('GetTrackInfo', -1) だけ。reaper_call_file の :329-343 は claims_ok が False（初期値 :475）のとき request_N.json を write_bytes する。版照会（:507）が成功するまでは、各プロセスの初回呼び出しと、ブリッジが応答しないときに到達する。
- **P-C08**（v4 の M49）: reaper_mcp_server.py:604-628 insert_track は ToolAnnotations(destructiveHint=False) で、readOnlyHint は無い。本体は reaper_call（index が None のとき）と reaper_batch(:557-569) を呼ぶ。reaper_batch -> ensure_bridge_current -> dispatch -> reaper_call_file、または reaper_batch -> reaper_call_file の経路で、:340 / :368 / :416-417 / :429 の unlink に毎回到達する。
- **P-M01**（v4 の R09）: github/tools/issues.py:18-55 gh_issue_list → gh_request('GET', ...) (github/client.py:58-110) → get_installation_token (client.py:19-46). On a cache miss it POSTs to /app/installations/{id}/access_tokens (L35). The rows carry contradiction_unknown:D1:net_post (client.py:35).
- **P-M02**（v4 の R16）: src/texas_grocery_mcp/tools/coupon.py:330 @ensure_session → auth/session.py:741-765 wrapper → :760 auto_refresh_session_if_needed（:633-735）→ :703 refresh_session_with_browser（auth/browser_refresh.py:259）→ :314 _cleanup_old_screenshots（:206-226 で /tmp/heb-login-*.png を os.remove）、:377 auth_path.parent.mkdir、:378 context.storage_state(path=auth_path)（認証状態ファイルの上書き）、:382 ensure_secure_permissions（utils/secure_file.py:89- で chmod）。
- **P-M03**（v4 の R20）: src/aws-pricing-mcp-server/awslabs/aws_pricing_mcp_server/server.py:387-560 get_pricing: create_pricing_client() → :464 pricing_client.get_products(...)（AWS Price List の読み取り API）→ transform_pricing_data で整形するだけ。ロガーは :59-60 で stderr だけ。

出典: `evidence/population_v4/v4_judgments.json`（id で引ける）。
