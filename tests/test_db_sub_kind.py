"""`_sub_kind` の DB 分類（D42 の B1 / B2 / B3）。

**期待値はこの表で、`authgap/effects.py` を直す前に書いた**（CLAUDE.md 規則 5）。

3 件の問題のうち直したのは **B1 だけ**である。B2 と B3 は「**直さないと決めた**」ことを
テストで固定する。**期待どおりに間違っている**ことを書き残すのは、後から黙って
挙動が変わるのを防ぐためで、正しさの主張ではない（根拠は `docs/decisions.md` D42）。
"""

from __future__ import annotations

import pytest

from authgap.effects import _sub_kind
from authgap.ir import RESOLVED, Atom, Prin, Value


def sql(text):
    return {"sql": Value(Prin.OP, RESOLVED, Atom(const=text))}


# --- B1: 直した。改行で始まる複数行 SQL を読み取りとして扱う -------------------
# **旧実装は `split(" ", 1)` で切っていたので `head == "SELECT\n"` になり `DB_WRITE` に
# 落ちていた**（母集団 v2 で 2 件。向きは誤警報）。
@pytest.mark.parametrize(
    "text",
    [
        "SELECT * FROM t",
        "\n        SELECT\n            id::text,\n            act_name\n        FROM acts",
        "\tSELECT\t1",
        "  select 1",  # 大文字小文字を問わない
        "SELECT",
        "\n  WITH a AS (SELECT 1)\n  SELECT * FROM a",
        "\nSHOW TABLES",
        "\nEXPLAIN SELECT 1",
        "\nDESCRIBE t",
    ],
)
def test_b1_multiline_read_verbs_are_db_read(text):
    assert _sub_kind("DB", sql(text)) == "DB_READ"


@pytest.mark.parametrize("text", ["INSERT INTO t VALUES (1)", "\n  INSERT INTO t\n  VALUES (1)",
                                  "UPDATE t SET x=1", "DELETE FROM t", "DROP TABLE t"])
def test_b1_write_verbs_stay_db_write(text):
    assert _sub_kind("DB", sql(text)) == "DB_WRITE"


# --- B1 の併せ直し: 空白だけの SQL は「不明」。`DB_WRITE` に倒さない（規則 4） ----
@pytest.mark.parametrize("text", ["", "   ", "\n\t "])
def test_blank_sql_is_unknown_not_write(text):
    assert _sub_kind("DB", sql(text)) is None


def test_unreadable_sql_is_unknown():
    """SQL の値が無い（解決できなかった）ときも「不明」。"""
    assert _sub_kind("DB", {}) is None


# --- B2: 直さないと決めた。`DB_WRITE` は「読み取り語で始まらない」の意味 --------
# **`SUB_KINDS`（月 3 凍結）を広げないため、接続設定とトランザクション制御は
# `DB_WRITE` のまま。**`readOnlyHint` の矛盾判定にそのまま使うと母集団 v2 で
# 105 件の誤警報になる（`docs/contradiction_matrix.md` §5、O23 #1）。
@pytest.mark.parametrize("text", ["PRAGMA journal_mode=WAL", "PRAGMA busy_timeout=5000",
                                  "BEGIN", "COMMIT", "ROLLBACK"])
def test_b2_control_statements_are_db_write_by_design(text):
    assert _sub_kind("DB", sql(text)) == "DB_WRITE"


# --- B3: 直さないと決めた。既知の誤 clear（母集団 v2 に 0 件、O24） -------------
def test_b3_with_writing_cte_is_wrongly_db_read():
    """`WITH x AS (...) INSERT INTO ...` は書き込みだが `DB_READ` になる。

    **これは既知の誤り（誤 clear 方向）であって、期待する挙動ではない。**
    憶測で直すと文字列リテラルの語で誤警報を作るので、O24 で決めるまで固定する。
    """
    assert _sub_kind("DB", sql("WITH x AS (SELECT 1) INSERT INTO t SELECT * FROM x")) == "DB_READ"
