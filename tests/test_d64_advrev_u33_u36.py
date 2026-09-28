"""D64: 段階 A の修正（7440a2a）の敵対的レビューで見つけた抜け（`docs/contradiction_principles.md` §9.6 の改訂）。

**期待値はこのテストで、`authgap/` を直す前に書いた（§9.6 の改訂 1' / 2' / 7'）。** 所見は
`evidence/review/advrev_u33_u36.md` の N1〜N8。判定関数（`dparse._d1` / `_d2` / `_d4` / `_host_class`）に定数の
効果を直接渡す（レビュー役の `advrev_u33_u36/h.py` と同じ形。`runner.run` を通しても同じ結果になることは
レビュー役が確かめた）。今の解析器で落ちる側は `test_fix_*`、通る側（直した後も通らなければならない）は
`test_keep_*`。
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from authgap import dparse
from authgap.ir import lit


def _db(text: str):
    return SimpleNamespace(kind="DB", site="sqlite3.Cursor.execute", slots={"sql": lit(text)})


def _st(r) -> str:
    if r is None:
        return "内"
    return "矛" if r[0] == dparse.CONTRA else "不"


def _judge(decl: str, text: str):
    return {"D1": dparse._d1, "D2": dparse._d2, "D4": dparse._d4}[decl](_db(text))


# (宣言, SQL, 期待, 期待の理由（None = 見ない）, 根拠)
FIX_DB = [
    # 改訂 1'(a) / 2'(c): 入れ子にする方言ではコメントが `*/ DELETE` まで続かず、DELETE が実行されうる
    ("D1", "/* old /* x */ SELECT */ DELETE FROM t", "不", None, "N1 入れ子のブロックコメントは剥がさない"),
    ("D4", "/* old /* x */ SELECT */ DELETE FROM t", "不", None, "N1（D4）"),
    ("D1", "SELECT 1; /* a /* b */ SELECT */ DELETE FROM t", "不", None, "N1 複文の中の入れ子コメント"),
    # 改訂 1'(b): MariaDB の実行されるコメント
    ("D1", "/*M!100100 INSERT INTO t */ SELECT * FROM u", "不", None, "N2 /*M! は剥がさない"),
    ("D2", "/*M!100100 REPLACE INTO t VALUES (1) */ SELECT * FROM u", "不", None, "N2（D2）"),
    # 改訂 1'(c) / 2'(c): PostgreSQL は `\r` でも行コメントを終える
    ("D1", "-- c\rDELETE FROM t;\nSELECT 1", "不", None, "N3 `\\r` を含む行コメント"),
    ("D1", "SELECT 1; -- c\rDELETE FROM t\n", "不", None, "N3 複文の中の `\\r`"),
    # 改訂 2'(a): 分割できなくても先頭の文は読める（退行 N4）
    ("D1", "DELETE FROM t WHERE name = 'O\\'Brien';", "矛", "db_modify", "N4 MySQL のエスケープ"),
    ("D2", "DELETE FROM t WHERE name = 'O\\'Brien';", "矛", "db_modify", "N4（D2）"),
    ("D1", "DELETE FROM t WHERE x = 1; # user's rows", "矛", "db_modify", "N4 `#` コメントの中の引用符"),
    ("D1", "UPDATE t SET s = 'a;b' WHERE n = 'it\\'s'", "矛", "db_modify", "N4 引用の中の `;` と `\\'`"),
    # 改訂 2'(b): complete_statement が拒む `;` をつないでよいのは SQLite の CREATE TRIGGER だけ
    ("D1", "SELECT $$it's$$; DELETE FROM t;", "不", "db_sql_unsplittable", "N5 分割器と complete_statement の食い違い"),
    ("D1", "SELECT $$[$$; DELETE FROM t;", "不", "db_sql_unsplittable", "N5 `[` の識別子"),
    ("D2", "CREATE TRIGGER trg AFTER INSERT ON a FOR EACH ROW EXECUTE FUNCTION f(); DROP TABLE b;", "不",
     "db_sql_unsplittable", "N6 PostgreSQL のトリガ（END で閉じない）"),
    ("D4", "CREATE TRIGGER trg AFTER INSERT ON a FOR EACH ROW EXECUTE FUNCTION f(); DROP TABLE b;", "不",
     "db_sql_unsplittable", "N6（D4）"),
    ("D4", "CREATE TRIGGER trg BEFORE INSERT ON t FOR EACH ROW SET NEW.x = 1; INSERT INTO log VALUES (1);", "不",
     "db_sql_unsplittable", "N6 MySQL のトリガ"),
    # 改訂 2'(c): 方言で字句が変わる印
    ("D1", "SELECT 'a\\'b'; DELETE FROM t; -- '", "不", "db_sql_unsplittable", "N7 MySQL の `\\'`"),
    ("D1", "SELECT E'a\\'b'; DELETE FROM t; -- '", "不", "db_sql_unsplittable", "N7 PostgreSQL の E''"),
    ("D1", "SELECT 1 # don't\n; DELETE FROM t; -- '", "不", "db_sql_unsplittable", "N7 MySQL の `#` コメント"),
    ("D1", "SELECT 1 /*! ; DELETE FROM t */;", "不", "db_sql_unsplittable", "N7 途中の実行されるコメント"),
    # 改訂 2'(d): 識別子の直後の `$` はドル引用の始まりではない
    ("D1", "SELECT 1 AS x$$; DELETE FROM t; SELECT 1 AS y$$", "矛", "db_multi_statement", "N7 `x$$` は識別子"),
    # 改訂 2'(e): 1 文に分かれたらその文を読む
    ("D1", "/* c */;DELETE FROM t", "矛", "db_modify", "D1 / D2 と D4 の読み方を揃える"),
]


@pytest.mark.parametrize("decl, text, want, reason, why", FIX_DB, ids=[f"{i}-{c[4]}" for i, c in enumerate(FIX_DB)])
def test_fix_db(decl, text, want, reason, why):
    r = _judge(decl, text)
    assert _st(r) == want, f"{why}: {decl} {text!r} -> {r}（期待 {want}）"
    if reason is not None:
        assert r[1] == reason, f"{why}: 理由 {r[1]}（期待 {reason}）"


KEEP_DB = [
    ("D1", "/*!50000 DROP TABLE t */ SELECT 1", "不", "/*! は剥がさない（§9.6-1）"),
    ("D1", "/* c */ DELETE FROM t", "矛", "閉じたコメントは剥がす"),
    ("D1", "-- c\nDELETE FROM t", "矛", "`\\n` で終わる行コメントは剥がす"),
    ("D1", "/*+ INDEX(t i) */ SELECT * FROM t", "内", "文頭の `/*+` は普通のコメント"),
    ("D1", "SELECT 'a;b'; SELECT 2", "内", "引用の中の `;`"),
    ("D1", "SELECT 'it''s'; DELETE FROM t", "矛", "引用符の重ね"),
    ("D1", "SELECT $tag$ ; DELETE $tag$; SELECT 1", "内", "ドル引用の中は文字列"),
    ("D1", "SELECT $1; SELECT 2", "内", "`$1` は引数"),
    ("D2", "CREATE TRIGGER t AFTER INSERT ON a BEGIN INSERT INTO b VALUES (1); END; DELETE FROM c;", "矛",
     "SQLite のトリガの本体の `;` は文の終端ではない（後ろの DELETE は別の文）"),
    ("D2", "CREATE TRIGGER t AFTER INSERT ON a BEGIN INSERT INTO b VALUES (1); END", "内",
     "`;` で終わらない SQLite のトリガ"),
    ("D1", "SELECT * FROM t WHERE name LIKE 'a\\_b'", "内", "`;` の無い 1 文は分けない"),
    ("D1", "SELECT 1;", "内", "末尾の `;` だけ"),
    ("D1", "BEGIN; DELETE FROM t; COMMIT;", "矛", "複文の中の DELETE"),
    ("D1", "/* unclosed DELETE FROM t", "不", "閉じないコメント"),
]


@pytest.mark.parametrize("decl, text, want, why", KEEP_DB, ids=[f"{i}-{c[3]}" for i, c in enumerate(KEEP_DB)])
def test_keep_db(decl, text, want, why):
    r = _judge(decl, text)
    assert _st(r) == want, f"{why}: {decl} {text!r} -> {r}（期待 {want}）"


def _host(h: str) -> str:
    e = SimpleNamespace(kind="NET", site="requests.get", http_method="GET", slots={"url.host": lit(h)})
    return dparse._host_class(e)


# 改訂 7': IP の local は明示の網で、IPv4 を埋め込んだ IPv6 は中の IPv4 で、それ以外のグローバルでない IP は不
FIX_HOST = [
    ("[2002:808:808::1]:80", "external", "N8 6to4 の中は 8.8.8.8"),
    ("user@[2002:808:808::1]", "external", "N8 userinfo つきの 6to4"),
    ("2002:808:808::1", "external", "N8 角括弧の無い 6to4"),
    ("[2001:0:4136:e378:8000:63bf:f7f7:f7f7]:443", "external", "N8 Teredo のクライアントは 8.8.8.8"),
    ("192.0.2.1", "unknown", "文書用の網は local とも external とも言えない"),
    ("100.64.0.1", "unknown", "CGNAT は local とも external とも言えない（A2）"),
    ("240.0.0.1", "unknown", "予約の網"),
    ("::1%x@evil.example", "external", "`@` があるときは IP を先に試さない（scope ID の形）"),
]


@pytest.mark.parametrize("h, want, why", FIX_HOST, ids=[c[2] for c in FIX_HOST])
def test_fix_host(h, want, why):
    assert _host(h) == want, f"{why}: {h!r} -> {_host(h)}（期待 {want}）"


KEEP_HOST = [
    ("127.0.0.1:8080", "local", "loopback"),
    ("[::1]:8080", "local", "IPv6 loopback"),
    ("10.1.2.3", "local", "RFC 1918"),
    ("172.16.0.5", "local", "RFC 1918"),
    ("192.168.1.10:5432", "local", "RFC 1918"),
    ("[fd00::1]:80", "local", "ULA"),
    ("fe80::1", "local", "link-local（角括弧なし）"),
    ("169.254.169.254", "local", "link-local"),
    ("0.0.0.0:8000", "local", "unspecified"),
    ("[::ffff:127.0.0.1]:80", "local", "IPv4-mapped の loopback"),
    ("[::ffff:8.8.8.8]:80", "external", "IPv4-mapped のグローバル"),
    ("[2002:c0a8:101::1]:80", "local", "6to4 の中が 192.168.1.1"),
    ("[64:ff9b::808:808]:80", "external", "NAT64 の中が 8.8.8.8"),
    ("8.8.8.8", "external", "グローバル"),
    ("localhost:3000", "local", "名前 localhost"),
    ("api.example.com", "external", "名前"),
    ("user:pw@localhost:5000", "local", "userinfo つき"),
    ("localhost:pw@evil.example", "external", "userinfo の中の localhost"),
    ("evil\\@localhost", "unknown", "`\\` はクライアントで読みが割れる"),
]


@pytest.mark.parametrize("h, want, why", KEEP_HOST, ids=[c[2] + ":" + c[0] for c in KEEP_HOST])
def test_keep_host(h, want, why):
    assert _host(h) == want, f"{why}: {h!r} -> {_host(h)}（期待 {want}）"
