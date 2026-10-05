"""scripts/path_view.py: 道筋の関数だけを並べる読む補助。"""
import json
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_path_view_marks_calls_effects_and_conditions(tmp_path):
    tree = tmp_path / "t"
    tree.mkdir()
    (tree / "s.py").write_text(textwrap.dedent('''\
        def tool(x):
            if x:
                return helper(x)
            return None


        class Store:
            def save(self, p):
                open(p, "w").write("1")


        def helper(x):
            Store().save(x)
        '''), encoding="utf-8")
    man = {"units": [{"unit": {"relpath": "s.py", "lineno": 1, "qualname": "tool", "tool_name": "tool",
                               "annotations": {"readOnlyHint": True}},
                      "effects": [{"site": "builtins.open", "relpath": "s.py", "lineno": 9, "entry_lineno": 3,
                                   "witness_chain": ["helper", "Store.save"]}],
                      "rows": [{"site": "builtins.open", "relpath": "s.py", "lineno": 9,
                                "notes": ["contradiction:D1", "contradiction_reason:D1:fs_write"]}]}]}
    mp = tmp_path / "m.json"
    mp.write_text(json.dumps(man), encoding="utf-8")
    r = subprocess.run([sys.executable, str(ROOT / "scripts" / "path_view.py"), str(mp), str(tree), "s.py", "1",
                        "builtins.open", "--decl", "D1"], capture_output=True, text=True, check=True)
    out = r.stdout
    assert "本体の 3 行 → helper → Store.save" in out
    assert "▶     3          return helper(x)" in out          # 入口の呼び出し行
    assert "?     2      if x:" in out                         # 条件の行
    assert "▶    13      Store().save(x)" in out               # 次の段を呼ぶ行
    assert "★     9          open(p, \"w\").write(\"1\")" in out  # 効果の行
    assert out.count("■ helper") == 1                          # 関数は 1 回だけ出す
