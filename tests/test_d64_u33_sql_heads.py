"""D64 / U33: SQL の先頭語の読み方（`docs/contradiction_principles.md` §9.6 の 1・2・3・6）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U33）。** 期待値は §7（7.1 / 7.2 / 7.4 / 7.5）と
§9.4 / §9.6 の規則から導いた。v2 / v3 の件数には合わせていない。

所見は `evidence/review/explore_*.json` の R3-r1-2（先頭コメント）、R3-r1-1（定数の複文）、R3-r1-3（PRAGMA の
括弧形）、R3-r4-3 の (a)（書式の穴を先頭語と読まない）。検証役の反例と `evidence/review/triage.json` の U33
の fix_outline の「避ける条件」は、今の解析器で**通る**側（`*_KEEP`）に入れた。直した後もこれが通らなければ
ならない。今の解析器で**落ちる**側は `*_FIX`。

R3-r4-3 の (b)（engine での `%` / `.format` の置換）は D64 で直さず限界として記録するので、書式の穴の形の
期待は「矛」ではなく §9.6 の 6 の「読めない（不、`db_sql_unreadable`）」にしている。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _units(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _db_notes(u: dict) -> list[str]:
    rows = [r for r in u["rows"] if r["kind"] == "DB"]
    assert rows, f"{u['unit']['qualname']}: DB の行が無い（前提が崩れている）"
    return [n for r in rows for n in r.get("notes", [])]


def _status(u: dict, decl: str) -> str:
    """DB の行の宣言 `decl` の判定: 矛 / 不 / 内（tests/test_contradiction_principles.py と同じ読み方）。"""
    rows = [r for r in u["rows"] if r["kind"] == "DB"]
    notes = _db_notes(u)
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方"
    if hit:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, decl: str) -> set[str]:
    out = set()
    for n in _db_notes(u):
        for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
            if n.startswith(pre):
                out.add(n[len(pre):])
    return out


def _check(units, tool, decl, want, reason):
    u = units[tool]
    got = _status(u, decl)
    assert got == want, f"{tool} {decl}: {got}（期待 {want}）notes={_db_notes(u)}"
    if reason is not None:
        assert reason in _reasons(u, decl), f"{tool} {decl}: 理由 {_reasons(u, decl)}（期待 {reason}）"


HEAD = '''
import os
import sqlite3

import psycopg
import sqlalchemy
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
engine = sqlalchemy.create_engine("postgresql://x")


def db():
    return sqlite3.connect("x.db")

'''


# ---------------------------------------------------------------------------
# §9.6 の 1: 先頭のコメントを剥がしてから先頭語を取る（R3-r1-2）
# ---------------------------------------------------------------------------

COMMENT_SRC = HEAD + r'''
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_line_comment_delete(p: str) -> str:
    db().execute("-- remove stale rows\nDELETE FROM t WHERE a = ?", (p,)); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_block_comment_update(p: str) -> str:
    db().execute("/* touch */ UPDATE t SET a = ? WHERE id = 1", (p,)); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_triple_quoted_comment_delete(p: str) -> str:
    db().execute("""
        -- purge
        /* all rows */
        DELETE FROM t
    """); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_then_select(p: str) -> str:
    db().execute("-- list rows\nSELECT * FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_then_pragma_set(p: str) -> str:
    db().execute("-- wal\nPRAGMA journal_mode = WAL"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_comment_then_insert(p: str) -> str:
    db().execute("-- c\nINSERT INTO t VALUES (1)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_op_prefix_delete(p: str) -> str:
    db().execute("-- audit\nDELETE FROM t WHERE a = " + os.environ["A"]); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_block_comment_op_prefix_update(p: str) -> str:
    db().execute("/* c */ UPDATE t SET a = " + os.environ["A"]); return "x"


# ---- 壊してはいけない形 ----------------------------------------------------
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_mysql_executable_comment(p: str) -> str:
    db().execute("/*!50000 DROP TABLE t */ SELECT 1"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_only(p: str) -> str:
    db().execute("-- DELETE FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_unterminated_block_comment(p: str) -> str:
    db().execute("/* DELETE FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_nested_block_comment(p: str) -> str:
    db().execute("/* outer /* inner */ still comment */ DELETE FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_hash_comment_delete(p: str) -> str:
    db().execute("# mysql comment\nDELETE FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_in_middle(p: str) -> str:
    db().execute("DELETE /* x */ FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_dashes_in_string(p: str) -> str:
    db().execute("SELECT '-- not a comment' FROM t"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_comment_op_prefix_partial_word(p: str) -> str:
    db().execute("-- x\nUPD" + os.environ["A"]); return "x"
'''


@pytest.fixture(scope="module")
def comment_units(tmp_path_factory):
    return _units(tmp_path_factory, "u33_comment", {"server.py": COMMENT_SRC})


COMMENT_FIX = [
    # R3-r1-2 の再現。§9.6 の 1 → 先頭語 DELETE ∈ SQL_MODIFY_HEADS → §7.1 矛
    ("d1_line_comment_delete", "D1", "矛", "db_modify"),
    # R3-r1-2 の再現。§9.6 の 1 → UPDATE ∈ SQL_DESTRUCTIVE_HEADS → §7.2 矛
    ("d2_block_comment_update", "D2", "矛", "db_modify"),
    # R3-r1-2 の「三重引用符の複数行」形。空白・行コメント・ブロックコメントが続いても剥がす
    ("d2_triple_quoted_comment_delete", "D2", "矛", "db_modify"),
    # R3-r1-2 の generality（SELECT なら 内 → 不 の水増し）。§9.6 の 1 → SELECT は読み取り → 内
    ("d1_comment_then_select", "D1", "内", None),
    # fix_outline (1): _PRAGMA の正規表現も剥がした後に当てる。journal_mode = → §7.5 永続 → §7.1 矛
    ("d1_comment_then_pragma_set", "D1", "矛", "db_persistent"),
    # triage の D4 の黙った誤 clear。§9.6 の 1 → INSERT → §7.4 不（冪等とは限らない）
    ("d4_comment_then_insert", "D4", "不", "db_nonidempotent_statement"),
    # 接頭辞（§9.4 の 3）でも剥がしてから最初の語の後の空白を見る（fix_outline (1)(iv)）→ DELETE → 矛
    ("d1_comment_op_prefix_delete", "D1", "矛", "db_modify"),
    # 検証役 sim_r1_2 の「接頭辞 '/* c */ UPDATE ' + x: 不 → 矛」。§9.3 の接頭辞規則と整合
    ("d1_block_comment_op_prefix_update", "D1", "矛", "db_modify"),
]

COMMENT_KEEP = [
    # 検証役の唯一の反例: `/*!` は MySQL で実行されるので剥がさない（§9.6 の 1）。剥がすと SELECT → 内 の誤 clear
    ("d1_mysql_executable_comment", "D1", "不", None),
    # fix_outline (1)(ii): 剥がした後が空なら今と同じく読めない（不）
    ("d1_comment_only", "D1", "不", None),
    # §9.6 の 1: 閉じないコメントは剥がし切れず読めないまま（不）
    ("d1_unterminated_block_comment", "D1", "不", None),
    # 今正しく判定できている形: 途中のコメントは先頭語に関係しない
    ("d1_comment_in_middle", "D1", "矛", "db_modify"),
    # 今正しく判定できている形: 引用符の中の `--` はコメントではない
    ("d1_dashes_in_string", "D1", "内", None),
    # fix_outline (1)(iv): 剥がした後の接頭辞 "UPD" は最初の語の後に空白が無いので決めない（不）
    ("d1_comment_op_prefix_partial_word", "D1", "不", None),
]


@pytest.mark.parametrize("tool,decl,want,reason", COMMENT_FIX, ids=[c[0] for c in COMMENT_FIX])
def test_comment_fix(comment_units, tool, decl, want, reason):
    _check(comment_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool,decl,want,reason", COMMENT_KEEP, ids=[c[0] for c in COMMENT_KEEP])
def test_comment_keep(comment_units, tool, decl, want, reason):
    _check(comment_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool", ["d1_nested_block_comment", "d1_hash_comment_delete"])
def test_comment_dialect_not_clean(comment_units, tool):
    """方言で読みが割れる形は「内」にしない（規則 4）。

    PostgreSQL の入れ子コメント（fix_outline (1)(iii)）は剥がし切れず不のままでよく、入れ子を正しく剥がして
    DELETE → 矛 にしてもよい。MySQL の `#` 行コメント（fix_outline (1)(v)、§9.6 は方言を決めていない）も
    不か矛のどちらか。どちらでも中の DELETE を落として「内」にはならない。
    """
    assert _status(comment_units[tool], "D1") != "内"


# ---------------------------------------------------------------------------
# §9.6 の 2: 定数の複文は文ごとに分類し、最も厳しい結果を採る（R3-r1-1）
# ---------------------------------------------------------------------------

MULTI_SRC = HEAD + r'''
@mcp.tool(annotations={"destructiveHint": False})
async def d2_script_create_then_delete(p: str) -> str:
    db().executescript("CREATE TABLE IF NOT EXISTS t (a); DELETE FROM t;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_psycopg_select_then_drop(p: str) -> str:
    cur = psycopg.connect("dbname=x").cursor()
    cur.execute("SELECT 1; DROP TABLE t;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_sqlite_execute_multi(p: str) -> str:
    db().execute("SELECT 1; DROP TABLE t;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_begin_delete_commit(p: str) -> str:
    db().executescript("BEGIN; DELETE FROM t; COMMIT;"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pragma_then_drop(p: str) -> str:
    db().executescript("PRAGMA foreign_keys = ON; DROP TABLE IF EXISTS t;"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_psycopg_insert_then_truncate(p: str) -> str:
    with psycopg.connect("dbname=x") as conn:
        conn.execute("INSERT INTO t VALUES (1); TRUNCATE t;"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_sqlalchemy_create_then_drop(p: str) -> str:
    with engine.connect() as conn:
        conn.exec_driver_sql("CREATE TABLE t (a); DROP TABLE u;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_select_then_pragma_persistent(p: str) -> str:
    db().executescript("SELECT 1; PRAGMA journal_mode = WAL;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_select_then_unknown(p: str) -> str:
    cur = psycopg.connect("dbname=x").cursor()
    cur.execute("SELECT 1; NOTIFY ch;"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_select_then_insert(p: str) -> str:
    db().executescript("SELECT 1; INSERT INTO t VALUES (1);"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_unclosed_quote(p: str) -> str:
    db().executescript("SELECT 'abc; DELETE FROM t"); return "x"


# ---- 壊してはいけない形 ----------------------------------------------------
@mcp.tool(annotations={"destructiveHint": False})
async def d2_trigger_body(p: str) -> str:
    db().executescript(
        "CREATE TRIGGER IF NOT EXISTS trg AFTER INSERT ON t BEGIN "
        "UPDATE t SET seen = 1 WHERE id = NEW.id; DELETE FROM log WHERE id = NEW.id; END;"
    ); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_trigger_body(p: str) -> str:
    db().executescript(
        "CREATE TRIGGER trg AFTER INSERT ON t BEGIN UPDATE s SET n = n + 1; DELETE FROM log; END;"
    ); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pg_dollar_function(p: str) -> str:
    cur = psycopg.connect("dbname=x").cursor()
    cur.execute(
        "CREATE OR REPLACE FUNCTION purge() RETURNS void AS $$ BEGIN DELETE FROM t; DELETE FROM u; END $$ LANGUAGE plpgsql;"
    ); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pg_tagged_dollar_function(p: str) -> str:
    cur = psycopg.connect("dbname=x").cursor()
    cur.execute(
        "CREATE FUNCTION purge() RETURNS void AS $body$ DELETE FROM t; $body$ LANGUAGE sql;"
    ); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_semicolon_in_literal(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES ('a;b')"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_in_literal(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES ('x; DELETE FROM t')"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_script_semicolon_in_literal(p: str) -> str:
    db().executescript("INSERT INTO t (a) VALUES ('a;b'); INSERT INTO t (a) VALUES ('c')"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_semicolon_in_line_comment(p: str) -> str:
    db().executescript("INSERT INTO t (a) VALUES (1) -- ; DROP TABLE t\n"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_semicolon_in_block_comment(p: str) -> str:
    db().executescript("INSERT INTO t (a) VALUES (1) /* ; DROP TABLE t; */"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_semicolon_in_quoted_ident(p: str) -> str:
    db().execute('SELECT "a;DROP TABLE t" FROM t'); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_begin_insert_commit(p: str) -> str:
    db().executescript("BEGIN; INSERT INTO t VALUES (1); COMMIT;"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_create_then_index(p: str) -> str:
    db().executescript("CREATE TABLE a (x); CREATE INDEX i ON a (x);"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_single_trailing_semicolon(p: str) -> str:
    db().execute("DELETE FROM t;"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_select_trailing_semicolon_ws(p: str) -> str:
    db().execute("SELECT 1;\n  "); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_op_prefix_stacked(p: str) -> str:
    db().execute("SELECT * FROM t; " + os.environ["X"]); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_model_sql(q: str) -> str:
    db().execute("SELECT * FROM t WHERE a = " + q); return "x"
'''


@pytest.fixture(scope="module")
def multi_units(tmp_path_factory):
    return _units(tmp_path_factory, "u33_multi", {"server.py": MULTI_SRC})


MULTI_FIX = [
    # R3-r1-1 の再現（executescript）。2 文目 DELETE ∈ SQL_DESTRUCTIVE_HEADS → §9.6 の 2 で矛、理由 db_multi_statement
    ("d2_script_create_then_delete", "D2", "矛", "db_multi_statement"),
    # R3-r1-1 の再現（psycopg の execute）。2 文目 DROP ∈ SQL_MODIFY_HEADS → 矛
    ("d1_psycopg_select_then_drop", "D1", "矛", "db_multi_statement"),
    # 検証役 ce1: sqlite3 の execute は複文を実行時に拒むが、解析器は site を区別しない（§9.6 の 2）→ 矛。
    # 理由を db_multi_statement にして手判定で見分ける
    ("d1_sqlite_execute_multi", "D1", "矛", "db_multi_statement"),
    # 検証役 ce1: executescript の常套句。接続単位の間の DELETE → 矛
    ("d1_begin_delete_commit", "D1", "矛", "db_multi_statement"),
    # 検証役 ce1: 接続単位の PRAGMA の後の DROP → 矛
    ("d2_pragma_then_drop", "D2", "矛", "db_multi_statement"),
    # R3-r1-1 の sql_multi/: psycopg.Connection.execute の TRUNCATE → 矛
    ("d2_psycopg_insert_then_truncate", "D2", "矛", "db_multi_statement"),
    # R3-r1-1 の sql_multi/: SQLAlchemy exec_driver_sql の DROP → 矛
    ("d2_sqlalchemy_create_then_drop", "D2", "矛", "db_multi_statement"),
    # §9.6 の 2 × §7.5: 2 文目が SQL_PERSISTENT → §7.1 で矛（複文から出た矛なので理由は db_multi_statement）
    ("d1_select_then_pragma_persistent", "D1", "矛", "db_multi_statement"),
    # §9.6 の 2「矛 > 不 > 内」: 2 文目が分類に無い（NOTIFY）→ 不
    ("d1_select_then_unknown", "D1", "不", None),
    # §9.6 の 2（D4）: どれかの文が冪等とは限らない類（INSERT）なら不（triage の D4 の黙った誤 clear）
    ("d4_select_then_insert", "D4", "不", None),
    # §9.6 の 2「閉じない引用 → 分割できない → 矛にせず不」。今は先頭語 SELECT だけ見て 内
    ("d1_unclosed_quote", "D1", "不", None),
]

MULTI_KEEP = [
    # 検証役の反例 (b): トリガ本体の `;` は文の終端ではない（sqlite3.complete_statement）。1 文の CREATE → §7.2 内
    # （§9.6 の 2 は分割できない形を不にしてもよいとするので、ここは test_multi_not_contra で「矛でない」を見る）
    # D1 ではトリガ作成そのものが CREATE ∈ SQL_MODIFY_HEADS → 矛。1 文なので理由は db_modify のまま
    ("d1_trigger_body", "D1", "矛", None),
    # 反例 (a): 引用符を見ない split(';') は 'a;b' の後ろを不明の文にする。1 文の INSERT → §7.2 内
    ("d2_semicolon_in_literal", "D2", "内", None),
    # 反例 (a) の強い形: 引用符の中の DELETE を文と読むと矛の誤警報
    ("d2_delete_in_literal", "D2", "内", None),
    # 反例 (a) を複文の中で: 'a;b' を含む INSERT 2 文 → どちらも追記 → 内
    ("d2_script_semicolon_in_literal", "D2", "内", None),
    # fix_outline (2) の '-- ;': 行コメントの中の `;` と DROP は文ではない → 内
    ("d2_semicolon_in_line_comment", "D2", "内", None),
    # 同じくブロックコメントの中の `;` と DROP
    ("d2_semicolon_in_block_comment", "D2", "内", None),
    # 二重引用符（識別子）の中の `;` も文の区切りではない → SELECT → 内
    ("d1_semicolon_in_quoted_ident", "D1", "内", None),
    # 'BEGIN; … COMMIT;' で中が追記だけなら 接続単位・追記・接続単位 → §7.2 内
    ("d2_begin_insert_commit", "D2", "内", None),
    # 典型の `CREATE TABLE …; CREATE INDEX …` は全部追記（検証役: 無害な常套句）→ 内
    ("d2_create_then_index", "D2", "内", None),
    # 末尾の `;` だけの単文は複文ではない → 理由は db_modify のまま
    ("d1_single_trailing_semicolon", "D1", "矛", "db_modify"),
    # 末尾の `;` の後が空白だけ → 空の文を「読めない」にしない → SELECT → 内
    ("d1_select_trailing_semicolon_ws", "D1", "内", None),
    # §9.6 の 2「接頭辞（§9.4 の 2・3）は今までどおり」: OP の連結の接頭辞 SELECT → 内（検証役 R3-r4-3 の対照）
    ("d1_op_prefix_stacked", "D1", "内", None),
    # §9.4 の 2 は今までどおり: MODEL/resolved の連結 → 矛 db_model_sql
    ("d1_model_sql", "D1", "矛", "db_model_sql"),
]


@pytest.mark.parametrize("tool,decl,want,reason", MULTI_FIX, ids=[c[0] for c in MULTI_FIX])
def test_multi_fix(multi_units, tool, decl, want, reason):
    _check(multi_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool,decl,want,reason", MULTI_KEEP, ids=[c[0] for c in MULTI_KEEP])
def test_multi_keep(multi_units, tool, decl, want, reason):
    _check(multi_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool", ["d2_trigger_body", "d2_pg_dollar_function", "d2_pg_tagged_dollar_function"])
def test_multi_not_contra(multi_units, tool):
    """検証役の反例 (b): 本体の `;` で分けて DELETE を独立の文と読むと D2 で矛の誤警報になる。

    SQLite の `CREATE TRIGGER … BEGIN … END`（本体は作成時に実行されない）と PostgreSQL の `$$` / `$tag$`
    （ドル引用。中身は文字列）。§9.6 の 2 は「分割できない形は矛にせず不にする」、fix_outline は「1 文として
    扱う（→ CREATE で内）」なので、内か不のどちらでもよい。**矛にだけはしない。** 今は 内。
    """
    assert _status(multi_units[tool], "D2") != "矛"


# ---------------------------------------------------------------------------
# §9.6 の 3: PRAGMA の括弧形は `=` と同じに扱う（R3-r1-3）
# ---------------------------------------------------------------------------

PRAGMA_SRC = HEAD + r'''
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_paren_journal(p: str) -> str:
    db().execute("PRAGMA journal_mode(WAL)"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pragma_paren_user_version(p: str) -> str:
    db().execute("PRAGMA user_version(3)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_paren_schema_qualified(p: str) -> str:
    db().execute("PRAGMA main.user_version(7)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_paren_op_prefix(p: str) -> str:
    db().execute("PRAGMA user_version(" + os.environ["N"] + ")"); return "x"


# ---- 壊してはいけない形 ----------------------------------------------------
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_table_info(p: str) -> str:
    db().execute("PRAGMA table_info(users)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_index_info(p: str) -> str:
    db().execute("PRAGMA index_info(i)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_journal_read(p: str) -> str:
    db().execute("PRAGMA journal_mode"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_page_size_read(p: str) -> str:
    db().execute("PRAGMA page_size"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_paren_connection(p: str) -> str:
    db().execute("PRAGMA foreign_keys(1)"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pragma_paren_connection(p: str) -> str:
    db().execute("PRAGMA busy_timeout(5000)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_wal_checkpoint(p: str) -> str:
    db().execute("PRAGMA wal_checkpoint(TRUNCATE)"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_eq_journal(p: str) -> str:
    db().execute("PRAGMA journal_mode = WAL"); return "x"
'''


@pytest.fixture(scope="module")
def pragma_units(tmp_path_factory):
    return _units(tmp_path_factory, "u33_pragma", {"server.py": PRAGMA_SRC})


PRAGMA_FIX = [
    # R3-r1-3 の再現。§9.6 の 3 → journal_mode ∈ PRAGMA_PERSISTENT_SET → §7.1 矛
    ("d1_pragma_paren_journal", "D1", "矛", "db_persistent"),
    # R3-r1-3 の再現。user_version ∈ PRAGMA_PERSISTENT_SET → §7.2 不（永続する設定）
    ("d2_pragma_paren_user_version", "D2", "不", "db_persistent"),
    # 検証役の模擬: `main.` 付きの括弧形も同じ
    ("d1_pragma_paren_schema_qualified", "D1", "矛", "db_persistent"),
    # 検証役 notes: 接頭辞でも名前と `(` が揃えば決める（§9.3）→ persistent → 矛
    ("d1_pragma_paren_op_prefix", "D1", "矛", "db_persistent"),
]

PRAGMA_KEEP = [
    # §9.6 の 3「§7.5 の名前の一覧に無いものは今までどおり」→ 読み取り → 内
    ("d1_pragma_table_info", "D1", "内", None),
    ("d1_pragma_index_info", "D1", "内", None),
    # 引数なしは値の読み出し → 内（検証役: 反例なし）
    ("d1_pragma_journal_read", "D1", "内", None),
    ("d1_pragma_page_size_read", "D1", "内", None),
    # PRAGMA_CONNECTION の括弧形 → 接続単位 → 内（直す前も後も内）
    ("d1_pragma_paren_connection", "D1", "内", None),
    ("d2_pragma_paren_connection", "D2", "内", None),
    # PRAGMA_PERSISTENT_ACTION は今のまま → 矛
    ("d1_pragma_wal_checkpoint", "D1", "矛", "db_persistent"),
    # `=` の形（R3-r1-3 の対照）→ 矛
    ("d1_pragma_eq_journal", "D1", "矛", "db_persistent"),
]


@pytest.mark.parametrize("tool,decl,want,reason", PRAGMA_FIX, ids=[c[0] for c in PRAGMA_FIX])
def test_pragma_fix(pragma_units, tool, decl, want, reason):
    _check(pragma_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool,decl,want,reason", PRAGMA_KEEP, ids=[c[0] for c in PRAGMA_KEEP])
def test_pragma_keep(pragma_units, tool, decl, want, reason):
    _check(pragma_units, tool, decl, want, reason)


# ---------------------------------------------------------------------------
# §9.6 の 6: 書式の穴を先頭語と読まない（R3-r4-3 の (a)）
# ---------------------------------------------------------------------------

PLACEHOLDER_SRC = HEAD + r'''
VERB_PURGE = "DELETE"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_percent_verb_literal_tail_op(p: str) -> str:
    db().execute("%s FROM t WHERE id = %s" % ("DELETE", os.environ["ID"])); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_percent_verb_const_tail_op(p: str) -> str:
    db().execute("%s FROM t WHERE id = %s" % (VERB_PURGE, os.environ["ID"])); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_percent_verb_literal_tail_op(p: str) -> str:
    db().execute("%s FROM t WHERE id = %s" % ("DELETE", os.environ["ID"])); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_percent_verb_select_tail_op(p: str) -> str:
    db().execute("%s * FROM t WHERE id = %s" % ("SELECT", os.environ["ID"])); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_percent_verb_insert_tail_op(p: str) -> str:
    db().execute("%s INTO t VALUES (%s)" % ("INSERT", os.environ["V"])); return "x"


# ---- 壊してはいけない形 ----------------------------------------------------
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_format_verb_literal_tail_op(p: str) -> str:
    db().execute("{} FROM t WHERE id = {}".format("DELETE", os.environ["ID"])); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def ctl_d1_percent_head_literal(p: str) -> str:
    db().execute("DELETE FROM %s WHERE id = %s" % ("t", os.environ["ID"])); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def ctl_d1_percent_verb_tail_model(x: str) -> str:
    db().execute("%s FROM t WHERE id = %s" % ("DELETE", x)); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def ctl_d1_like_escape(p: str) -> str:
    db().execute("DELETE FROM t WHERE name LIKE '%%%s%%'" % os.environ["X"]); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def ctl_d1_percent_after_first_word(p: str) -> str:
    db().execute("SELECT * FROM t WHERE name LIKE '%" + os.environ["X"] + "%'"); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def ctl_d1_paramstyle_const(p: str) -> str:
    db().execute("DELETE FROM t WHERE id = %s", (p,)); return "x"
'''


@pytest.fixture(scope="module")
def placeholder_units(tmp_path_factory):
    return _units(tmp_path_factory, "u33_placeholder", {"server.py": PLACEHOLDER_SRC})


PLACEHOLDER_FIX = [
    # R3-r4-3 の再現。§9.6 の 6: 接頭辞の最初の語 `%s` に `%` → 先頭語を決めない → 読めない（不）。
    # (b) は直さないので矛ではなく不。今は理由が db_unknown_statement（`%S` を先頭語と読んでいる）
    ("d1_percent_verb_literal_tail_op", "D1", "不", "db_sql_unreadable"),
    ("d1_percent_verb_const_tail_op", "D1", "不", "db_sql_unreadable"),
    ("d2_percent_verb_literal_tail_op", "D2", "不", "db_sql_unreadable"),
    # R3-r4-3 の SELECT の形（不の水増し側）。(a) だけでは不のまま、理由が正しくなる
    ("d1_percent_verb_select_tail_op", "D1", "不", "db_sql_unreadable"),
    # triage (3)(a): D4 は今 `%S` が非 None なので黙った内（誤 clear）→ 読めない（不）
    ("d4_percent_verb_insert_tail_op", "D4", "不", "db_sql_unreadable"),
]

PLACEHOLDER_KEEP = [
    # R3-r4-3 の .format の形は今も読めない（不 db_sql_unreadable）
    ("d1_format_verb_literal_tail_op", "D1", "不", "db_sql_unreadable"),
    # R3-r4-3 の対照: テンプレートの先頭がリテラル → 矛 db_modify（今も正しい）
    ("ctl_d1_percent_head_literal", "D1", "矛", "db_modify"),
    # R3-r4-3 の対照: 尾が MODEL/resolved → §9.4 の 2 で矛 db_model_sql
    ("ctl_d1_percent_verb_tail_model", "D1", "矛", "db_model_sql"),
    # 検証役 (b) の反例の一つ: `%%` を含む LIKE でも先頭語 DELETE → 矛
    ("ctl_d1_like_escape", "D1", "矛", "db_modify"),
    # `%` が最初の語より後ろにあるだけなら先頭語は決まる（§9.6 の 6 は「最初の語」だけ）→ SELECT → 内
    ("ctl_d1_percent_after_first_word", "D1", "内", None),
    # DB-API の paramstyle `%s` を含む定数（全体）→ 先頭語 DELETE → 矛
    ("ctl_d1_paramstyle_const", "D1", "矛", "db_modify"),
]


@pytest.mark.parametrize("tool,decl,want,reason", PLACEHOLDER_FIX, ids=[c[0] for c in PLACEHOLDER_FIX])
def test_placeholder_fix(placeholder_units, tool, decl, want, reason):
    _check(placeholder_units, tool, decl, want, reason)


@pytest.mark.parametrize("tool,decl,want,reason", PLACEHOLDER_KEEP, ids=[c[0] for c in PLACEHOLDER_KEEP])
def test_placeholder_keep(placeholder_units, tool, decl, want, reason):
    _check(placeholder_units, tool, decl, want, reason)


# ---------------------------------------------------------------------------
# 前提: 宣言が読めている（読めなければ全部「内」になり、KEEP の「内」が素通りする）
# ---------------------------------------------------------------------------

_EXPECT_DECL = {"d1": "readOnlyHint", "d2": "destructiveHint", "ctl_d1": "readOnlyHint"}


@pytest.mark.parametrize("fx", ["comment_units", "multi_units", "pragma_units", "placeholder_units"])
def test_premise_declarations(request, fx):
    units = request.getfixturevalue(fx)
    assert units, fx
    for name, u in units.items():
        dk = u.get("D_kind") or u.get("d_kind") or {}
        prefix = name.split("_", 2)
        key = "ctl_d1" if name.startswith("ctl_d1") else prefix[0]
        if key in _EXPECT_DECL:
            assert _EXPECT_DECL[key] in dk.get("explicit", []), f"{name}: {dk}"
        elif key == "d4":
            assert dk.get("idempotent") is True, f"{name}: {dk}"
