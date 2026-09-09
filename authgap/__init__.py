"""AuthGap: Python の LLM エージェントにおけるモデル実効権限の静的推論。

解析中核は標準ライブラリ `ast` のみ。venv も型環境も構築しない。
LLM を判定入力に使わず決定的に判定する。仕様の正本は `AUTHGAP_BRIEF_v3.md`。
"""

__version__ = "0.1.0"
