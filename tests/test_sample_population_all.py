"""`scripts/sample_population_v2.py` の選び方（D73 の 5: 最終評価は --all で全部を取り、種を使わない）。"""

import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))

from sample_population_v2 import choose  # noqa: E402

POP = [f"o/r{i:03d}" for i in range(50)]


def test_all_returns_everything_sorted_without_seed():
    assert choose(list(reversed(POP)), None, None, True) == sorted(POP)


def test_sample_is_seeded_and_sized():
    a = choose(POP, 10, 20260920, False)
    assert len(a) == 10 and a == choose(POP, 10, 20260920, False) and a == sorted(a)
    assert a != choose(POP, 10, 1, False)


def test_sample_larger_than_population_returns_all():
    assert choose(POP, 1000, 5, False) == sorted(POP)


def test_all_rejects_n_and_seed():
    script = os.path.join(ROOT, "scripts", "sample_population_v2.py")
    for extra in (["--n", "5"], ["--seed", "3"]):
        p = subprocess.run([sys.executable, script, "--all", *extra], capture_output=True, text=True)
        assert p.returncode != 0 and "--all" in p.stderr
