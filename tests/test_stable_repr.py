"""集合定数の表示がプロセスをまたいで同じになる（manifest のバイト一致）。

**期待値はこのテストで、`authgap/` を直す前に書いた。**

`ConfigAtom` / `Atom` の `default` は、集合なら `repr(set)` をそのまま manifest に書いていた。
文字列のハッシュはプロセスごとに変わる（PYTHONHASHSEED）ので、**同じ木を 2 回走らせると
要素の並びが変わり、manifest が一致しない**。同じ解析器で取り直した深さ 3 の run 2 本で
6 木・14 ユニットの `gate` がこれだけで食い違った。判定には効かない（表示だけ）が、
run の突き合わせで本物の差と区別できなくなる。
"""

from __future__ import annotations

import os
import subprocess
import sys

from authgap.atoms import Atom
from authgap.gate import ConfigAtom
from authgap.ir import stable_repr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_set_is_sorted():
    assert stable_repr({"b", "a", "c"}) == "{'a', 'b', 'c'}"
    assert stable_repr(frozenset({"b", "a"})) == "frozenset({'a', 'b'})"
    assert stable_repr(set()) == "set()"


def test_nested_and_non_set_unchanged():
    assert stable_repr(("x", {"b", "a"})) == "('x', {'a', 'b'})"
    assert stable_repr(["x", 1]) == "['x', 1]"
    assert stable_repr({"k": {"b", "a"}}) == "{'k': {'a', 'b'}}"
    assert stable_repr(3.5) == "3.5"


def test_to_json_uses_stable_repr():
    assert ConfigAtom("N", "module_const", {"z", "y", "x"}).to_json()["default"] == "{'x', 'y', 'z'}"
    assert Atom("N", "module_const", {"z", "y", "x"}).to_json()["default"] == "{'x', 'y', 'z'}"


def test_across_hash_seeds():
    code = ("from authgap.gate import ConfigAtom;"
            "print(ConfigAtom('N','module_const',{'sp500','nasdaq100','russell2000','dow','ftse'}).to_json()['default'])")
    outs = set()
    for seed in ("1", "2", "3", "4"):
        env = dict(os.environ, PYTHONHASHSEED=seed)
        outs.add(subprocess.run([sys.executable, "-c", code], cwd=ROOT, env=env,
                                capture_output=True, text=True, check=True).stdout)
    assert len(outs) == 1
