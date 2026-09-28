CASES = [
    "/*M! REPLACE INTO t */ SELECT * FROM u",
    "/*M!100100 DELETE FROM t WHERE id IN */ (SELECT id FROM u)",
    "/* a /* b */ SELECT */ UPDATE t SET a = 1",
    "SELECT 1; /* a /* b */ SELECT */ DELETE FROM t",
    "SELECT 1; -- c\rDELETE FROM t\n",
    "-- c\rDROP TABLE t;\nSELECT 1",
]
