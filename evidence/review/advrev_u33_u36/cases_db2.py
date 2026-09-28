CASES = [
    # contradiction lost to 不 when split fails although the leading statement is a definite modify
    "DELETE FROM t WHERE name = 'O\\'Brien';",
    "UPDATE t SET s = 'a;b' WHERE n = 'it\\'s'",
    "DELETE FROM t WHERE x = 1; # user's rows",
    "DELETE FROM sys$log$ WHERE id = 1;",
    "DROP TABLE t; SELECT 'unterminated",
    # D2 destructive with unsplittable tail
    "UPDATE t SET a = 1; SELECT \"x",
    # len(stmts)==1 but not first segment
    "/* c */;DELETE FROM t",
    # multi statement where first is PRAGMA paren
    "PRAGMA user_version(3); SELECT 1",
    # PRAGMA with spaces around dot
    "PRAGMA main . user_version = 3",
    "PRAGMA user_version /* c */ = 3",
    "PRAGMA user_version -- c\n = 3",
    # -- inside strip then quote
    "-- c\n'x'",
    # comment then ; then read
    "-- x\n; SELECT 1",
    # BOM / zero-width
    "﻿DELETE FROM t",
    "​DELETE FROM t",
]
