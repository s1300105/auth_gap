# F0a の §10 関門の率と木単位ブートストラップ区間（D18）

再現: `python scripts/f0a_ci.py`

抽出単位は木（`trees.jsonl` の analyzed）。seed 20260914、反復 2000、パーセンタイル法 95% 区間。**関門の判定は点推定のまま**（§10）。区間が閾値を
跨ぐものは「境界」と書き、点推定だけで合格 / 不合格を主張しない。

| run | 母集団 | 木 | 率 | 点推定 | 95% 区間 | 閾値 | 点推定の判定 | 区間 |
|---|---|---|---|---|---|---|---|---|
| run1 | app | 8 | `in_tree_resolution_ratio_sites` | 20.0% | [0.0%, 20.5%] | >= 50% | × | 区間も同じ側 |
| run1 | app | 8 | `opaque_ratio_primary_slots_sites` | 64.4% | [62.8%, 100.0%] | <= 40% | × | 区間も同じ側 |
| run1 | app | 8 | `validator_holding_ratio` | 4.3% | [0.0%, 7.7%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | mcp_server | 60 | `in_tree_resolution_ratio_sites` | 31.4% | [14.2%, 52.2%] | >= 50% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | mcp_server | 60 | `opaque_ratio_primary_slots_sites` | 56.9% | [36.6%, 79.2%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | mcp_server | 60 | `validator_holding_ratio` | 4.4% | [2.4%, 7.4%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | tool_package | 30 | `in_tree_resolution_ratio_sites` | 40.2% | [13.3%, 55.0%] | >= 50% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | tool_package | 30 | `opaque_ratio_primary_slots_sites` | 46.2% | [35.6%, 64.9%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run1 | tool_package | 30 | `validator_holding_ratio` | 3.4% | [1.5%, 7.5%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | app | 8 | `in_tree_resolution_ratio_sites` | 20.0% | [0.0%, 20.5%] | >= 50% | × | 区間も同じ側 |
| run1py312 | app | 8 | `opaque_ratio_primary_slots_sites` | 64.4% | [62.8%, 100.0%] | <= 40% | × | 区間も同じ側 |
| run1py312 | app | 8 | `validator_holding_ratio` | 4.3% | [0.0%, 7.7%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | mcp_server | 60 | `in_tree_resolution_ratio_sites` | 31.4% | [14.2%, 52.2%] | >= 50% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | mcp_server | 60 | `opaque_ratio_primary_slots_sites` | 56.9% | [36.6%, 79.2%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | mcp_server | 60 | `validator_holding_ratio` | 4.4% | [2.4%, 7.4%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | tool_package | 30 | `in_tree_resolution_ratio_sites` | 40.2% | [13.3%, 55.0%] | >= 50% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | tool_package | 30 | `opaque_ratio_primary_slots_sites` | 46.2% | [35.6%, 64.9%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run1py312 | tool_package | 30 | `validator_holding_ratio` | 3.4% | [1.5%, 7.5%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run2 | app | 8 | `in_tree_resolution_ratio_sites` | 27.3% | [0.0%, 30.8%] | >= 50% | × | 区間も同じ側 |
| run2 | app | 8 | `opaque_ratio_primary_slots_sites` | 41.9% | [16.7%, 100.0%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run2 | app | 8 | `validator_holding_ratio` | 6.3% | [0.0%, 16.0%] | >= 5% | ○ | **境界**（区間が閾値を跨ぐ） |
| run2 | mcp_server | 60 | `in_tree_resolution_ratio_sites` | 51.0% | [37.3%, 65.1%] | >= 50% | ○ | **境界**（区間が閾値を跨ぐ） |
| run2 | mcp_server | 60 | `opaque_ratio_primary_slots_sites` | 27.1% | [15.8%, 45.1%] | <= 40% | ○ | **境界**（区間が閾値を跨ぐ） |
| run2 | mcp_server | 60 | `validator_holding_ratio` | 4.4% | [2.3%, 7.3%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run2 | tool_package | 30 | `in_tree_resolution_ratio_sites` | 49.5% | [27.6%, 70.2%] | >= 50% | × | **境界**（区間が閾値を跨ぐ） |
| run2 | tool_package | 30 | `opaque_ratio_primary_slots_sites` | 25.0% | [7.0%, 46.7%] | <= 40% | ○ | **境界**（区間が閾値を跨ぐ） |
| run2 | tool_package | 30 | `validator_holding_ratio` | 3.3% | [1.4%, 7.1%] | >= 5% | × | **境界**（区間が閾値を跨ぐ） |
| run2app | app | 8 | `in_tree_resolution_ratio_sites` | 27.3% | [0.0%, 30.8%] | >= 50% | × | 区間も同じ側 |
| run2app | app | 8 | `opaque_ratio_primary_slots_sites` | 41.9% | [14.9%, 100.0%] | <= 40% | × | **境界**（区間が閾値を跨ぐ） |
| run2app | app | 8 | `validator_holding_ratio` | 6.3% | [0.0%, 16.0%] | >= 5% | ○ | **境界**（区間が閾値を跨ぐ） |
