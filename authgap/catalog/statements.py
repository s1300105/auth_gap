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


def sql_class(text: Optional[str]) -> Optional[str]:
    """定数 SQL の類。`None` は SQL が読めない（定数でない / 空白だけ）。"""
    if not isinstance(text, str):
        return None
    parts = text.split(None, 1)
    if not parts:
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
        m = _PRAGMA.match(text)
        if not m:
            return SQL_CLASS_UNKNOWN
        name, op = m.group(1).lower(), m.group(2)
        if name in PRAGMA_PERSISTENT_ACTION:
            return SQL_CLASS_PERSISTENT
        if op == "=":
            if name in PRAGMA_PERSISTENT_SET:
                return SQL_CLASS_PERSISTENT
            if name in PRAGMA_CONNECTION:
                return SQL_CLASS_CONNECTION
            return SQL_CLASS_UNKNOWN
        # `=` が無い: 値の読み出し（`PRAGMA table_info(t)` / `PRAGMA journal_mode`）
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
