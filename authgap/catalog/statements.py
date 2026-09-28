"""SQL 文・HTTP メソッド・ファイル書き込みの分類（矛盾の判定原理 §7 の語彙、D56）。

**判定の規則はここに無い**（`authgap/dparse.py: contradiction_findings`）。ここは「どの先頭語 /
メソッド / sink がどの類か」だけを持つ。出所は `docs/contradiction_principles.md` §7.5 / §7.6 /
§7.2 で、**原理を選んでコミットした後に、原理から機械的に導いた**（件数を見て足し引きしない）。

ここに無いものは「不明」になる（原理 2-a）。足すときは §7 を先に直してコミットする。
"""

from __future__ import annotations

import re
from typing import Optional

#: データ・スキーマを変える文（D55）。
SQL_MODIFY_HEADS: frozenset[str] = frozenset(
    {"INSERT", "UPDATE", "DELETE", "REPLACE", "MERGE", "TRUNCATE", "DROP", "CREATE", "ALTER"}
)
#: そのうち追記でないもの（D55。`INSERT` / `CREATE` を除く）。
SQL_DESTRUCTIVE_HEADS: frozenset[str] = SQL_MODIFY_HEADS - {"INSERT", "CREATE"}
#: 冪等とは限らない変更（§7.4。一意制約や `x = x + 1` で決まる）。
SQL_NONIDEMPOTENT_HEADS: frozenset[str] = frozenset({"INSERT", "UPDATE", "REPLACE", "MERGE"})
#: 読み取りの文。`WITH` は O24 のまま読み取り扱い。
SQL_READ_HEADS: frozenset[str] = frozenset({"SELECT", "SHOW", "EXPLAIN", "DESCRIBE", "WITH"})
#: 接続・トランザクション単位（接続が閉じれば残らない）。
SQL_CONNECTION_HEADS: frozenset[str] = frozenset(
    {"BEGIN", "COMMIT", "ROLLBACK", "SAVEPOINT", "RELEASE", "END", "SET", "RESET", "DETACH",
     "LISTEN", "UNLISTEN"}
)
#: DB ファイルに残る保守の文（1-i-b）。
SQL_PERSISTENT_HEADS: frozenset[str] = frozenset({"VACUUM", "ANALYZE", "REINDEX"})
#: 値を設定しても接続単位で消える PRAGMA。
PRAGMA_CONNECTION: frozenset[str] = frozenset(
    {"foreign_keys", "busy_timeout", "synchronous", "cache_size", "temp_store", "locking_mode",
     "recursive_triggers", "query_only", "case_sensitive_like", "cache_spill", "mmap_size",
     "threads", "defer_foreign_keys", "trusted_schema", "automatic_index", "secure_delete"}
)
#: 値を設定すると DB ファイルに残る PRAGMA（1-i-b）。
PRAGMA_PERSISTENT_SET: frozenset[str] = frozenset(
    {"journal_mode", "user_version", "application_id", "auto_vacuum", "page_size", "encoding",
     "schema_version"}
)
#: 値を取らなくても書き込む PRAGMA。
PRAGMA_PERSISTENT_ACTION: frozenset[str] = frozenset({"wal_checkpoint", "optimize", "incremental_vacuum"})

#: SQL 文の類。
SQL_CLASS_MODIFY = "modify"
SQL_CLASS_PERSISTENT = "persistent"
SQL_CLASS_CONNECTION = "connection"
SQL_CLASS_READ = "read"
SQL_CLASS_UNKNOWN = "unknown"

_PRAGMA = re.compile(r"^\s*PRAGMA\s+(?:\w+\.)?(\w+)\s*(=|\()?", re.IGNORECASE)
#: PostgreSQL のドル引用の開き（`$$` / `$tag$`）。`$1` のような位置パラメータは当たらない。
_DOLLAR = re.compile(r"\$([A-Za-z_][A-Za-z0-9_]*)?\$")


def strip_leading_sql_comments(text: str) -> Optional[str]:
    """先頭の空白・`--` 行コメント・`/* */` ブロックコメントを剥がした残り（§9.6 の 1、D64 / U33）。

    **`/*!` で始まる MySQL の実行されるコメントは剥がさない**（中身が実行されるので、剥がすと
    `/*!50000 DROP TABLE t */ SELECT 1` が読み取りになる誤 clear。検証役の反例）。閉じないコメントと、
    剥がした後に何も残らないときは `None`（読めない）。
    """
    i, n = 0, len(text)
    while True:
        while i < n and text[i].isspace():
            i += 1
        if text.startswith("--", i):
            j = text.find("\n", i)
            if j < 0:
                return None
            i = j + 1
            continue
        if text.startswith("/*", i) and not text.startswith("/*!", i):
            j = text.find("*/", i + 2)
            if j < 0:
                return None
            i = j + 2
            continue
        break
    rest = text[i:]
    return rest if rest.strip() else None


def split_sql_statements(text: str) -> Optional[list[str]]:
    """定数 SQL を、引用符・コメント・ドル引用の外の `;` で文に分ける（§9.6 の 2、D64 / U33）。

    SQLite の `CREATE TRIGGER … BEGIN … END` の本体の `;` は文の終端ではないので、`;` で切るのは
    `sqlite3.complete_statement` がそこまでを 1 文と認めるときだけにする。`$tag$ … $tag$` の中は文字列。
    閉じない引用・ブロックコメント・ドル引用があれば **`None`（分けられない）**。空の文（末尾の `;` だけ）は
    数えない。
    """
    import sqlite3

    out: list[str] = []
    start = i = 0
    n = len(text)
    while i < n:
        c = text[i]
        if c in "'\"`":
            j = i + 1
            while True:
                j = text.find(c, j)
                if j < 0:
                    return None
                if text.startswith(c * 2, j):  # 引用符を 2 つ重ねたエスケープ
                    j += 2
                    continue
                break
            i = j + 1
            continue
        if text.startswith("--", i):
            j = text.find("\n", i)
            i = n if j < 0 else j + 1
            continue
        if text.startswith("/*", i):
            j = text.find("*/", i + 2)
            if j < 0:
                return None
            i = j + 2
            continue
        if c == "$":
            m = _DOLLAR.match(text, i)
            if m:
                j = text.find(m.group(0), m.end())
                if j < 0:
                    return None
                i = j + len(m.group(0))
                continue
        if c == ";" and sqlite3.complete_statement(text[start:i + 1]):
            out.append(text[start:i])
            start = i + 1
        i += 1
    out.append(text[start:])
    return [st for st in out if strip_leading_sql_comments(st) is not None]


def sql_class(text: Optional[str], complete: bool = True) -> Optional[str]:
    """定数 SQL の類。`None` は SQL が読めない（定数でない / 空白だけ / コメントだけ）。

    `complete=False` は `text` が連結の接頭辞であること（D57、§9.4）。先頭語は最初の語の後に空白が
    あるときだけ決め、`PRAGMA` は接頭辞の中に名前と `=` / `(` が揃うときだけ決める。
    先頭のコメントは剥がしてから読む（§9.6 の 1）。**1 文として読む**（複文は呼び出し側が
    `split_sql_statements` で分ける）。
    """
    if not isinstance(text, str):
        return None
    stripped = strip_leading_sql_comments(text)
    if stripped is None:
        return None
    parts = stripped.split(None, 1)
    if not parts:
        return None
    if not complete and not stripped[len(parts[0]):][:1].isspace():
        return None
    head = parts[0].upper().rstrip(";")
    if head in SQL_MODIFY_HEADS:
        return SQL_CLASS_MODIFY
    if head in SQL_READ_HEADS:
        return SQL_CLASS_READ
    if head in SQL_CONNECTION_HEADS:
        return SQL_CLASS_CONNECTION
    if head in SQL_PERSISTENT_HEADS:
        return SQL_CLASS_PERSISTENT
    if head == "PRAGMA":
        m = _PRAGMA.match(stripped)
        if not m:
            return SQL_CLASS_UNKNOWN
        name, op = m.group(1).lower(), m.group(2)
        if not complete and op is None:
            return SQL_CLASS_UNKNOWN  # 接頭辞の中で名前が終わっているか分からない
        if name in PRAGMA_PERSISTENT_ACTION:
            return SQL_CLASS_PERSISTENT
        if op == "=":
            if name in PRAGMA_PERSISTENT_SET:
                return SQL_CLASS_PERSISTENT
            if name in PRAGMA_CONNECTION:
                return SQL_CLASS_CONNECTION
            return SQL_CLASS_UNKNOWN
        if op == "(":
            # **括弧で値を渡す形は `=` と同じ**（§9.6 の 3、D64 / U33）。一覧にある設定の名前だけ。
            # `table_info(t)` / `index_info(i)` など一覧に無い名前は今までどおり読み取り。
            if name in PRAGMA_PERSISTENT_SET:
                return SQL_CLASS_PERSISTENT
            if name in PRAGMA_CONNECTION:
                return SQL_CLASS_CONNECTION
        # 値を設定しない: 値の読み出し（`PRAGMA table_info(t)` / `PRAGMA journal_mode`）
        return SQL_CLASS_READ
    return SQL_CLASS_UNKNOWN


#: HTTP の意味論（RFC 9110）で安全なメソッド。
HTTP_SAFE: frozenset[str] = frozenset({"GET", "HEAD", "OPTIONS"})
#: 相手を変えるメソッド（1-ii-b）。
HTTP_MODIFY: frozenset[str] = frozenset({"PUT", "PATCH", "DELETE"})
#: 冪等なメソッド（RFC 9110 §9.2.2）。
HTTP_IDEMPOTENT: frozenset[str] = frozenset({"GET", "HEAD", "OPTIONS", "PUT", "DELETE"})
#: sink 名の末尾がこれなら、そのままメソッドとして読む。
HTTP_METHOD_SUFFIXES: frozenset[str] = frozenset({"get", "post", "put", "patch", "delete", "head", "options"})
#: sink 名の末尾がこれなら、第 1 引数をメソッドとして読む。
HTTP_METHOD_ARG_SUFFIXES: frozenset[str] = frozenset({"request"})

#: FS_WRITE のうち「書き出し」（新規作成か上書きかが書き先の有無で決まる。§7.2、#7）。
FS_WRITEOUT_SITES: frozenset[str] = frozenset(
    {"pathlib.Path.write_text", "pathlib.Path.write_bytes", "builtins.open", "io.open",
     "pathlib.Path.open", "shutil.copy", "shutil.copy2", "shutil.copyfile",
     "shutil.unpack_archive", "urllib.request.urlretrieve"}
)
#: `open` 系（mode を持つ sink。§7.4 の追記の判定）。
FS_OPEN_SITES: frozenset[str] = frozenset({"builtins.open", "io.open", "pathlib.Path.open"})
