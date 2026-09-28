CASES = [
    # --- controls
    "SELECT 1",
    "-- note\nSELECT 1",
    "/* c */ DELETE FROM t",
    "/*!50000 DROP TABLE t */ SELECT 1",
    # --- 1. comment stripping vs dialects
    # PostgreSQL nested block comment: PG executes DELETE, stripper stops at first */
    "/* old /* x */ SELECT */ DELETE FROM t",
    "/* disabled /* inner */ SELECT 1; */ DELETE FROM t",
    # MariaDB executable comment /*M! (MariaDB runs INSERT ... SELECT)
    "/*M!100100 INSERT INTO t */ SELECT * FROM u",
    "/*M! DELETE FROM t WHERE id IN */ (SELECT id FROM u)",
    # MySQL optimizer hint at start (MySQL treats as plain comment there)
    "/*+ BKA(t) */ SELECT * FROM t",
    # MySQL # comment
    "# note\nDELETE FROM t",
    # PostgreSQL: -- comment ends at \r as well
    "-- c\rDELETE FROM t;\nSELECT 1",
    "-- c\rDELETE FROM t\nSELECT 1",
    # MySQL: -- without trailing space is not a comment
    "--x\nSELECT 1",
    # comment only / unclosed
    "-- only",
    "/* only */",
    "/* unclosed SELECT 1",
    # comment containing quotes
    "-- it's\nSELECT 1",
    "/* it's */ SELECT 1; DELETE FROM t",
    # unicode whitespace
    " DELETE FROM t",
    "　SELECT 1",
    # --- 2. split
    # MySQL backslash escape (mysqlclient runs multi statements by default)
    "SELECT 'a\\'b'; DELETE FROM t; -- '",
    "SELECT 'it\\'s'; DELETE FROM t",
    # PostgreSQL E'' string
    "SELECT E'a\\'b'; DELETE FROM t; -- '",
    # MySQL # comment with apostrophe
    "SELECT 1 # don't\n; DELETE FROM t; -- '",
    # $ inside identifiers (PG allows $ in identifiers, not at start)
    "SELECT 1 AS x$$; DELETE FROM t; SELECT 1 AS y$$",
    # dollar-quoted body
    "DO $$ BEGIN DELETE FROM x; END $$; SELECT 1",
    "SELECT $$a;b$$; DELETE FROM t",
    "SELECT $tag$ ; $tag$; DELETE FROM t",
    # $1 parameters
    "SELECT $1; DELETE FROM t WHERE id = $2",
    # SQLite trigger body
    "CREATE TRIGGER tr AFTER INSERT ON a BEGIN DELETE FROM b; END; SELECT 1",
    # PG / MySQL trigger without BEGIN..END -> complete_statement never closes
    "CREATE TRIGGER tr AFTER INSERT ON a FOR EACH ROW EXECUTE FUNCTION f(); DROP TABLE b;",
    "CREATE TRIGGER tr BEFORE INSERT ON a FOR EACH ROW SET NEW.x = 1; DELETE FROM b;",
    "CREATE TRIGGER tr BEFORE INSERT ON a FOR EACH ROW SET NEW.x = 1; INSERT INTO log VALUES (1);",
    # PG SQL-standard function body
    "CREATE FUNCTION f() RETURNS int LANGUAGE sql BEGIN ATOMIC SELECT 1; END; DROP TABLE b",
    # brackets
    "SELECT [a;b] FROM t; DELETE FROM t",
    "SELECT [a FROM t; DELETE FROM t",
    # trailing / empty
    "SELECT 1; DELETE FROM t",
    "SELECT 1;;",
    "SELECT 1; -- done",
    ";DELETE FROM t",
    "/* c */;DELETE FROM t",
    # connection statements around a write
    "BEGIN; DELETE FROM t; COMMIT;",
    "SET x = 1; UPDATE t SET a = 1",
    # WITH ... DELETE (O24)
    "WITH x AS (SELECT 1) DELETE FROM t",
    # --- 3. PRAGMA paren form
    "PRAGMA journal_mode(WAL)",
    "PRAGMA main.user_version(5)",
    "PRAGMA table_info(t)",
    "PRAGMA writable_schema(1)",
    "PRAGMA writable_schema = 1",
    "PRAGMA foreign_keys(0)",
    "/* x */ PRAGMA user_version = 3",
    "PRAGMA  /* c */ user_version = 3",
    "PRAGMA user_version /* c */ = 3",
    # --- 6. placeholders
    "%s FROM t",
    "{op} FROM t",
    "{CALL delete_all()}",
    "DELETE%s FROM t",
]
