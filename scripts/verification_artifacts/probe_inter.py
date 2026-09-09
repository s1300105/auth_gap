import ast, os, sys
sys.path.insert(0, "/home/yudai/Project/research/Master_Project/dispatch-taint-system/dispatch-taint/taintp2x_extension")
import selection_guard as sg
S = os.path.dirname(os.path.abspath(__file__))
for t, sinkline_needle in (("t13","subprocess.run"),("t14","subprocess.run"),("t15","subprocess.run")):
    root = os.path.join(S, t)
    idx = sg.SourceIndex(root)
    path = os.path.join(root, "tools.py")
    src = open(path).read()
    mod = ast.parse(src)
    line = next(i for i,l in enumerate(src.splitlines(),1) if sinkline_needle in l and "import" not in l)
    fn = sg.enclosing_function(mod, line)
    r = sg.interproc_guard(fn, None, "tools.py", mod, line, idx)
    print(f"{t}: guarded={r.guarded}  reason={r.reason}")
    print(f"    witness={r.dominating_witness!r}  notes={r.notes}")
