"""D64 / U34: DB の分類から（判定, 理由）への写像（R1d-r6-5, R3-r1-7）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U34）。** 規則は
`docs/contradiction_principles.md` §7.4 / §7.5 / §9.4 と、それを直した §9.6 の 4・5（実装より先にコミット済み）。
v2 / v3 の件数には合わせていない。所見・反例は `evidence/review/triage.json` の U34、
`evidence/review/explore_*.json` / `verify_*.json` の R1d-r6-5 / R3-r1-7。

* R1d-r6-5（§9.6 の 4）: D4 で先頭語が §7.5 の分類（読み取り / 接続単位 / `SQL_MODIFY_HEADS` /
  `SQL_PERSISTENT`）に無い文は **不** `db_unknown_statement`。判定は `sql_class(text, complete)` が
  UNKNOWN かどうかで決める。**素朴な直し方**「`SQL_NONIDEMPOTENT_HEADS` にも `SQL_DESTRUCTIVE_HEADS` にも
  無ければ不」は SELECT / SET / BEGIN などを誤って不にする（検証役の反例）。`complete` を渡さないと、
  接頭辞だけの文（`"PRAGMA foreign_keys" + 設定値`）を全文として読み取りに分類してしまう。
* R3-r1-7（§9.6 の 5）: MODEL が選べる（resolved）連結 SQL でも、接頭辞の先頭語がその宣言の変更の文
  （D1 は `SQL_MODIFY_HEADS`、D2 は `SQL_DESTRUCTIVE_HEADS`）なら理由は `db_modify`。判定は矛のまま。
  感度分析 3-b（`scripts/contradiction_by_decl.py: apply_flip`、理由に `model` を含む矛 → 不）で矛のまま残る
  こと。SELECT 接頭辞・D2 の INSERT 接頭辞・空白の無い `"DELETE" + x` は `db_model_sql` のまま（検証役の反例）。

記号: `"矛"` = 注記 `contradiction:<宣言>`、`"不"` = `contradiction_unknown:<宣言>:<理由>`、`"内"` = どちらも無い。
全ツールは sqlite3 の接続で書く（再現の d4_attach が psycopg の site に解決された件は受け手の解決の別問題で、
この単位ではない）。
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


def _finding(u, decl, kind="DB"):
    """(結果, 理由の列)。矛なら `contradiction_reason:` の理由、不なら `contradiction_unknown:` の理由。"""
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（前提が崩れている）"
    notes = [n for r in rows for n in r.get("notes", [])]
    reasons = sorted({n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_reason:{decl}:")})
    unk = sorted({n.split(":", 2)[2] for n in notes if n.startswith(f"contradiction_unknown:{decl}:")})
    if f"contradiction:{decl}" in notes:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        assert not unk, f"{decl} が矛と不の両方"
        return "矛", reasons
    return ("不", unk) if unk else ("内", [])


def _findings_set(u, decl, kind="DB"):
    """`apply_flip` に渡す形 `{(status, reason)}`（contradiction_by_decl.load_reasons と同じ読み方）。"""
    out = set()
    for r in u["rows"]:
        if r["kind"] != kind:
            continue
        for n in r.get("notes", []):
            if n.startswith(f"contradiction_reason:{decl}:"):
                out.add(("contradiction", n.split(":", 2)[2]))
            elif n.startswith(f"contradiction_unknown:{decl}:"):
                out.add(("unknown", n.split(":", 2)[2]))
    return out


# ---------------------------------------------------------------------------
# R1d-r6-5: D4（idempotentHint: true）の DB 行で、分類に無い先頭語は不（§9.6 の 4）
# ---------------------------------------------------------------------------

D4_SRC = r'''
import sqlite3

import somelib
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def db():
    return sqlite3.connect("x.db")


# ---- 分類に無い先頭語（再現 d4heads の 5 件）: 不 db_unknown_statement -------------
@mcp.tool(annotations={"idempotentHint": True})
async def d4_notify(p: str) -> str:
    db().execute("NOTIFY events, 'x'"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_call(p: str) -> str:
    db().execute("CALL enqueue_job(?)", (p,)); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_copy(p: str) -> str:
    db().execute("COPY t FROM '/tmp/data.csv'"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_upsert(p: str) -> str:
    db().execute("UPSERT INTO t (a) VALUES (?)", (p,)); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_attach(p: str) -> str:
    db().execute("ATTACH DATABASE 'y.db' AS y"); return "x"


# ---- 検証役が確かめた副作用（§9.6 の 4 が明記）: 分類に無い PRAGMA の代入と GRANT も不 --------
@mcp.tool(annotations={"idempotentHint": True})
async def d4_pragma_unknown_set(p: str) -> str:
    db().execute("PRAGMA wal_autocheckpoint = 1000"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_grant(p: str) -> str:
    db().execute("GRANT SELECT ON t TO bob"); return "x"


# ---- 接頭辞（主体が MODEL でない連結、§9.4 の 3）: 類が接頭辞で決まらなければ不 ---------------
@mcp.tool(annotations={"idempotentHint": True})
async def d4_op_prefix_notify(p: str) -> str:
    db().execute("NOTIFY " + somelib.CHANNEL); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_op_prefix_pragma_name(p: str) -> str:
    db().execute("PRAGMA foreign_keys" + somelib.SUFFIX); return "x"


# ---- 対照（今 内 で、直した後も 内）: 分類にある先頭語 ---------------------------------------
@mcp.tool(annotations={"idempotentHint": True})
async def d4_delete(p: str) -> str:
    db().execute("DELETE FROM t WHERE a = ?", (p,)); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_drop(p: str) -> str:
    db().execute("DROP TABLE IF EXISTS t"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_create(p: str) -> str:
    db().execute("CREATE TABLE IF NOT EXISTS t (a)"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_alter(p: str) -> str:
    db().execute("ALTER TABLE t ADD COLUMN b"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_truncate(p: str) -> str:
    db().execute("TRUNCATE TABLE t"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_vacuum(p: str) -> str:
    db().execute("VACUUM"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_pragma_persistent_set(p: str) -> str:
    db().execute("PRAGMA journal_mode = WAL"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_pragma_conn(p: str) -> str:
    db().execute("PRAGMA foreign_keys = ON"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_pragma_read(p: str) -> str:
    db().execute("PRAGMA journal_mode"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_select(p: str) -> str:
    db().execute("SELECT * FROM t WHERE a = ?", (p,)); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_with(p: str) -> str:
    db().execute("WITH q AS (SELECT 1) SELECT * FROM q"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_set(p: str) -> str:
    db().execute("SET search_path TO app"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_begin(p: str) -> str:
    db().execute("BEGIN"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_listen(p: str) -> str:
    db().execute("LISTEN events"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_op_prefix_select(p: str) -> str:
    db().execute("SELECT * FROM " + somelib.TABLE); return "x"


# ---- 対照（今 不 で、直した後も同じ理由）: 冪等とは限らない変更・読めない・モデルの文 -------------
@mcp.tool(annotations={"idempotentHint": True})
async def d4_insert(p: str) -> str:
    db().execute("INSERT INTO t (a) VALUES (?)", (p,)); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_executemany_insert(rows: list) -> str:
    db().executemany("INSERT INTO t (a) VALUES (?)", rows); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_update_prefix_op(p: str) -> str:
    db().execute("UPDATE " + somelib.TABLE + " SET a = 1"); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_model_sql(sql: str) -> str:
    db().execute(sql); return "x"


@mcp.tool(annotations={"idempotentHint": True})
async def d4_delete_prefix_chosen(x: str) -> str:
    db().execute("DELETE FROM t WHERE a = " + x); return "x"


# ---- D1 / D2 の同じ文（直す前から不。D4 をこれに揃える） ------------------------------------
@mcp.tool(annotations={"readOnlyHint": True})
async def d1_notify(p: str) -> str:
    db().execute("NOTIFY events, 'x'"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_call(p: str) -> str:
    db().execute("CALL enqueue_job(?)", (p,)); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_pragma_unknown_set(p: str) -> str:
    db().execute("PRAGMA wal_autocheckpoint = 1000"); return "x"
'''


@pytest.fixture(scope="module")
def d4(tmp_path_factory):
    return _units(tmp_path_factory, "u34_d4", {"server.py": D4_SRC})


def test_d4_premise_declarations(d4):
    """前提: 宣言が読めている（読めなければ全部 内 になって対照が素通りする）。"""
    for name, u in d4.items():
        dk = u["D_kind"]
        assert not dk.get("unknown"), name
        if name.startswith("d4_"):
            assert dk.get("idempotent") is True, (name, dk)


@pytest.mark.parametrize("tool", ["d4_notify", "d4_call", "d4_copy", "d4_upsert", "d4_attach"])
def test_d4_unclassified_head_is_unknown(d4, tool):
    """R1d-r6-5 の再現 d4heads: §9.6 の 4（§7.5「それ以外 → 不」・原理 2-a）で不 db_unknown_statement。今は注記なしの内。"""
    assert _finding(d4[tool], "D4") == ("不", ["db_unknown_statement"])


@pytest.mark.parametrize("tool", ["d4_pragma_unknown_set", "d4_grant"])
def test_d4_unclassified_pragma_and_grant_move_to_unknown(d4, tool):
    """R1d-r6-5 の検証役の副作用: §9.6 の 4 が明記する（分類に無い PRAGMA の代入と GRANT も不）。内 → 不 は矛を生まない。"""
    assert _finding(d4[tool], "D4") == ("不", ["db_unknown_statement"])


def test_d4_op_prefix_unclassified_head_is_unknown(d4):
    """R1d-r6-5 × §9.4 の 3: 主体が OP の連結で接頭辞の先頭語が分類に無い（NOTIFY）→ 不。"""
    assert _finding(d4["d4_op_prefix_notify"], "D4") == ("不", ["db_unknown_statement"])


def test_d4_op_prefix_pragma_name_uses_complete(d4):
    """U34 fix_outline「complete は必ず渡す」: `"PRAGMA foreign_keys" + 設定値` は接頭辞で類が決まらない → 不。

    `sql_class(text)`（complete=True の既定）で分類すると「`=` の無い PRAGMA = 読み取り」で内に落ちる。
    理由は類が決まらないことを表すもの（`db_unknown_statement` か `db_sql_unreadable`）。
    """
    got, reasons = _finding(d4["d4_op_prefix_pragma_name"], "D4")
    assert got == "不", (got, reasons)
    assert set(reasons) <= {"db_unknown_statement", "db_sql_unreadable"}, reasons


@pytest.mark.parametrize(
    "tool",
    [
        # 検証役の対照（verify/d3d4/r6_5）: DELETE / CREATE IF NOT EXISTS / VACUUM / PRAGMA foreign_keys = ON / SELECT
        "d4_delete", "d4_create", "d4_vacuum", "d4_pragma_conn", "d4_select",
        # §7.4 で内のまま: 残りの変更（DROP / ALTER / TRUNCATE）、永続、読み取り
        "d4_drop", "d4_alter", "d4_truncate", "d4_pragma_persistent_set", "d4_pragma_read", "d4_with",
        # 素朴な直し方（NONIDEMPOTENT にも DESTRUCTIVE にも無ければ不）で壊れる形: SET / BEGIN / LISTEN（接続単位）
        "d4_set", "d4_begin", "d4_listen",
        # 主体が OP の連結で、接頭辞の類が読み取りに決まる（§9.4 の 3）
        "d4_op_prefix_select",
    ],
)
def test_d4_classified_heads_stay_inside(d4, tool):
    """U34 の対照・反例: 先頭語が §7.5 の分類にある文は D4 で内のまま（`sql_class` が UNKNOWN でない）。"""
    assert _finding(d4[tool], "D4") == ("内", [])


@pytest.mark.parametrize(
    "tool,reason",
    [
        ("d4_insert", "db_nonidempotent_statement"),
        ("d4_executemany_insert", "db_nonidempotent_statement"),
        # 主体が OP の連結でも接頭辞の先頭語で決まる（§9.4 の 3）。UNKNOWN の検査より先に当たる
        ("d4_update_prefix_op", "db_nonidempotent_statement"),
        # D4 には原理 3 を当てない（§7.0 の 1）: モデルの文は db_sql_model のまま
        ("d4_model_sql", "db_sql_model"),
        ("d4_delete_prefix_chosen", "db_sql_model"),
    ],
)
def test_d4_existing_unknown_reasons_unchanged(d4, tool, reason):
    """U34 の対照: 今 不 の D4 の行は、`db_unknown_statement` の分岐を足しても理由が変わらない。"""
    assert _finding(d4[tool], "D4") == ("不", [reason])


@pytest.mark.parametrize("tool,decl", [("d1_notify", "D1"), ("d2_call", "D2"), ("d2_pragma_unknown_set", "D2")])
def test_d1_d2_unclassified_head_already_unknown(d4, tool, decl):
    """R1d-r6-5 の比較対象: D1 / D2 は直す前から §7.1 / §7.2「先頭語が分類に無い → 不」。D4 をこれに揃える。"""
    assert _finding(d4[tool], decl) == ("不", ["db_unknown_statement"])


# ---------------------------------------------------------------------------
# R3-r1-7: chosen の連結 SQL で接頭辞が変更の文なら理由は db_modify（§9.6 の 5）
# ---------------------------------------------------------------------------

CHOSEN_SRC = r'''
import sqlite3

import unknownlib
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def db():
    return sqlite3.connect("x.db")


# ---- 所見の形（再現 f7_model_sql_reason と generality の 4 形）: 矛 db_modify -------------
@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_prefix_chosen(x: str) -> str:
    sqlite3.connect("x.db").execute("DELETE FROM t WHERE a = " + x)
    return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_fstring_chosen(x: str) -> str:
    db().execute(f"DELETE FROM t WHERE a = {x}"); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_format_chosen(x: str) -> str:
    db().execute("DELETE FROM t WHERE a = {}".format(x)); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_update_prefix_chosen(x: str) -> str:
    db().execute("UPDATE t SET a = 1 WHERE b = " + x); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_update_prefix_chosen(x: str) -> str:
    db().execute("UPDATE t SET a = 1 WHERE b = " + x); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_insert_prefix_chosen(x: str) -> str:
    db().execute("INSERT INTO t VALUES (" + x + ")"); return "x"


# ---- 検証役の反例（ce7）と対照: 直した後も今のまま -----------------------------------------
@mcp.tool(annotations={"destructiveHint": False})
async def d2_select_prefix_chosen(x: str) -> str:
    sqlite3.connect("x.db").execute("SELECT * FROM t WHERE a = " + x)
    return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_select_prefix_chosen(x: str) -> str:
    db().execute("SELECT * FROM t WHERE a = " + x); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_prefix_influenced(x: str) -> str:
    sqlite3.connect("x.db").execute("DELETE FROM t WHERE a = " + unknownlib.q(x))
    return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_insert_prefix_chosen(x: str) -> str:
    sqlite3.connect("x.db").execute("INSERT INTO t VALUES (" + x + ")")
    return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_create_prefix_chosen(x: str) -> str:
    db().execute("CREATE TABLE " + x); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_delete_nospace_chosen(x: str) -> str:
    db().execute("DELETE" + x); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_pragma_prefix_chosen(mode: str) -> str:
    db().execute("PRAGMA journal_mode=" + mode); return "x"


@mcp.tool(annotations={"readOnlyHint": True})
async def d1_sql_param(sql: str) -> str:
    db().execute(sql); return "x"


@mcp.tool(annotations={"destructiveHint": False})
async def d2_vacuum_prefix_chosen(x: str) -> str:
    db().execute("VACUUM " + x); return "x"
'''


@pytest.fixture(scope="module")
def chosen(tmp_path_factory):
    return _units(tmp_path_factory, "u34_chosen", {"server.py": CHOSEN_SRC})


def _apply_flip():
    from scripts.contradiction_by_decl import apply_flip

    return apply_flip


def test_chosen_premise_model_resolved(chosen):
    """前提: 所見の形の SQL は MODEL/resolved（chosen）で届いている（opaque なら db_modify は今も出る）。"""
    for tool in ("d2_delete_prefix_chosen", "d2_delete_fstring_chosen", "d2_delete_format_chosen",
                 "d2_update_prefix_chosen", "d1_update_prefix_chosen", "d1_insert_prefix_chosen"):
        eff = [e for e in chosen[tool]["effects"] if e["kind"] == "DB"]
        assert eff, tool
        # sql の slot が MODEL かつ resolved（= _db の chosen 分岐を通る形）
        sql = [e["slots"]["sql"] for e in eff if "sql" in (e.get("slots") or {})]
        assert sql and all(s["prin"] == "MODEL" and s["prov"] == "resolved" for s in sql), (tool, sql)
        decl = "D1" if tool.startswith("d1_") else "D2"
        got, reasons = _finding(chosen[tool], decl)
        assert got == "矛", (tool, got, reasons)


@pytest.mark.parametrize(
    "tool,decl",
    [
        ("d2_delete_prefix_chosen", "D2"),   # 再現 f7_model_sql_reason
        ("d2_delete_fstring_chosen", "D2"),  # generality: d2_fstring_model
        ("d2_delete_format_chosen", "D2"),   # generality: d2_format_model
        ("d2_update_prefix_chosen", "D2"),
        ("d1_update_prefix_chosen", "D1"),   # D1 の modify_heads = SQL_MODIFY_HEADS
        ("d1_insert_prefix_chosen", "D1"),   # INSERT は D1 の変更の文（D2 とは違う）
    ],
)
def test_chosen_modify_prefix_reason_is_db_modify(chosen, tool, decl):
    """R3-r1-7 / §9.6 の 5: chosen でも接頭辞の先頭語が宣言の変更の文なら 矛 `db_modify`（判定は変えない）。"""
    got, reasons = _finding(chosen[tool], decl)
    assert got == "矛", (tool, got, reasons)
    assert reasons == ["db_modify"], (tool, reasons)


@pytest.mark.parametrize(
    "tool,decl",
    [("d2_delete_prefix_chosen", "D2"), ("d1_update_prefix_chosen", "D1"), ("d1_insert_prefix_chosen", "D1")],
)
def test_chosen_modify_prefix_survives_sensitivity_3b(chosen, tool, decl):
    """R3-r1-7: 3-b（理由に model を含む矛 → 不）でも矛のまま。新しい理由コードに `model` を含めると壊れる（fix_outline）。"""
    apply_flip = _apply_flip()
    fs = _findings_set(chosen[tool], decl)
    assert apply_flip(fs, decl, None) == "矛"
    assert apply_flip(fs, decl, "3-b") == "矛", fs


def test_chosen_vs_influenced_monotone_under_3b(chosen):
    """R3-r1-7 の単調性（検証役）: 証拠の強い chosen の DELETE が、弱い influenced の DELETE より弱く数えられない。"""
    apply_flip = _apply_flip()
    strong = apply_flip(_findings_set(chosen["d2_delete_prefix_chosen"], "D2"), "D2", "3-b")
    weak = apply_flip(_findings_set(chosen["d2_delete_prefix_influenced"], "D2"), "D2", "3-b")
    assert weak == "矛"
    assert strong == weak


@pytest.mark.parametrize(
    "tool,decl,reason",
    [
        # 検証役の反例 ce7: SELECT 接頭辞 + chosen は db_model_sql のまま（3-b で不。influenced の SELECT と揃う）
        ("d2_select_prefix_chosen", "D2", "db_model_sql"),
        ("d1_select_prefix_chosen", "D1", "db_model_sql"),
        # 検証役の反例 ce7: D2 の INSERT 接頭辞 + chosen は modify_heads（SQL_DESTRUCTIVE_HEADS）に無いので db_model_sql
        ("d2_insert_prefix_chosen", "D2", "db_model_sql"),
        # 同じ理由で D2 の CREATE 接頭辞も db_model_sql
        ("d2_create_prefix_chosen", "D2", "db_model_sql"),
        # 検証役の反例: 最初の語の後に空白が無い `"DELETE" + x` は先頭語が決まらないので今のまま
        ("d2_delete_nospace_chosen", "D2", "db_model_sql"),
        # 既存（test_fix_o30_o32_o33）: PRAGMA の接頭辞（変更の文ではない）と、SQL 全体がモデルの値
        ("d1_pragma_prefix_chosen", "D1", "db_model_sql"),
        ("d1_sql_param", "D1", "db_model_sql"),
        # 検証役の反例 ce7: influenced の DELETE は今も db_modify
        ("d2_delete_prefix_influenced", "D2", "db_modify"),
    ],
)
def test_chosen_non_modify_prefix_unchanged(chosen, tool, decl, reason):
    """R3-r1-7 の反例・対照: 接頭辞がその宣言の変更の文でない chosen の形は理由を変えない（判定は矛）。"""
    assert _finding(chosen[tool], decl) == ("矛", [reason])


def test_chosen_select_prefix_still_unknown_under_3b(chosen):
    """R3-r1-7 の反例: SELECT 接頭辞 + chosen は 3-b で不（注入が無ければ読み取り）。db_modify にすると矛に残ってしまう。"""
    apply_flip = _apply_flip()
    assert apply_flip(_findings_set(chosen["d2_select_prefix_chosen"], "D2"), "D2", "3-b") == "不"


def test_chosen_persistent_prefix_verdict_only(chosen):
    """U34 fix_outline の「未確認」: `"VACUUM " + x`（永続の類）の chosen 形の理由は §9.6 の 5 が決めていない。判定（矛）だけ固定する。"""
    got, reasons = _finding(chosen["d2_vacuum_prefix_chosen"], "D2")
    assert got == "矛", (got, reasons)
