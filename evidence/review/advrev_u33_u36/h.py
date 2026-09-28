"""Harness: python h.py <tree> <mode> ; reads cases from cases_<mode>.py (list CASES)."""
import sys, json, runpy
from types import SimpleNamespace

tree = sys.argv[1]
mode = sys.argv[2]
sys.path.insert(0, tree)
from authgap import dparse
from authgap.ir import lit, Value, Prin, RESOLVED, Atom, Str, opaque

cases = runpy.run_path(sys.argv[3])["CASES"]


def eff_db(text):
    return SimpleNamespace(kind="DB", site="sqlite3.Cursor.execute", slots={"sql": lit(text)})


def eff_net(host):
    return SimpleNamespace(kind="NET", site="requests.get", http_method="GET", slots={"url.host": lit(host)})


for c in cases:
    if mode == "db":
        e = eff_db(c)
        r1 = dparse._d1(e)
        r2 = dparse._d2(e)
        r4 = dparse._d4(e)
        def f(r):
            return "内" if r is None else ("矛" if r[0] == dparse.CONTRA else "不") + ":" + r[1]
        print(json.dumps(c, ensure_ascii=False), "| D1", f(r1), "| D2", f(r2), "| D4", f(r4))
    elif mode == "host":
        e = eff_net(c)
        try:
            hc = dparse._host_class(e)
        except Exception as ex:  # noqa
            hc = f"EXC {type(ex).__name__}: {ex}"
        print(json.dumps(c, ensure_ascii=False), "->", hc)
