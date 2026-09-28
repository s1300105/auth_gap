CASES = [
    # splitter treats $$...$$ as a string, but sqlite3.complete_statement re-scans the segment with
    # SQLite's lexer (no dollar quotes) and sees an unterminated ' -> never "complete" -> no split
    "SELECT $$it's$$; DELETE FROM t;",
    "SELECT $$it's$$; DELETE FROM t",
    "SELECT $q$don't$q$ AS note; UPDATE t SET a = 1;",
    "SET app.note = $$it's$$; DELETE FROM t;",
    # same with a '[' inside a dollar-quoted string (SQLite reads [ as identifier quote)
    "SELECT $$[$$; DELETE FROM t;",
    # PG CREATE TRIGGER without BEGIN..END, D2 / D4
    "CREATE TRIGGER trg AFTER INSERT ON a FOR EACH ROW EXECUTE FUNCTION f(); DELETE FROM b;",
    # INSERT then hidden DELETE after PG trigger (D2: INSERT additive, CREATE additive)
    "INSERT INTO a VALUES (1); CREATE TRIGGER trg AFTER INSERT ON a FOR EACH ROW EXECUTE FUNCTION f(); DELETE FROM b;",
    # EXPLAIN ANALYZE executes in PostgreSQL
    "EXPLAIN ANALYZE DELETE FROM t",
    # MySQL SET that persists
    "SET PERSIST max_connections = 10",
    "SET PASSWORD FOR 'u'@'%' = 'x'",
]
