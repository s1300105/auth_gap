"""manifest が `docs/manifest.schema.json` に validate すること（§5.1 / B5）。

schema は **manifest の採点前に書く**（§5.1）。gate 欄が真偽ではなく
`(3 値 verdict, grade, reason, witness 行)` であることを schema が強制する。
"""

import json
import os

import pytest

from authgap.report import manifest_json, probe_json
from authgap.runner import RunConfig, run

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(ROOT, "docs", "manifest.schema.json")
FIXTURE = os.path.join(ROOT, "fixtures", "entries")


@pytest.fixture(scope="module")
def result():
    return run(RunConfig(src_root=FIXTURE, population="mcp_server", full=True))


def test_manifest_validates(result):
    jsonschema = pytest.importorskip("jsonschema")
    with open(SCHEMA, encoding="utf-8") as fh:
        schema = json.load(fh)
    man = manifest_json(result, run_id="test")
    jsonschema.validate(man, schema)


def test_volatile_is_confined_to_run_meta(result):
    """**volatile はトップレベルの `run_meta` に閉じ込める**（§5.2）。"""
    man = manifest_json(result, run_id="test")
    assert "run_meta" in man
    blob = json.dumps({k: v for k, v in man.items() if k != "run_meta"}, ensure_ascii=False)
    assert ROOT not in blob, "絶対パスが run_meta の外に漏れている"
    assert "elapsed" not in blob


def test_probe_has_all_required_keys(result):
    """§5.1 が列挙する probe.json の全キーがあること。"""
    p = probe_json(result, corpus_id="test")
    required = [
        "corpus_id", "n_units", "n_units_with_dangerous_effect", "n_effects_by_kind",
        "resolution", "resolution_by_cause", "rubric1c", "registry_resolution_ratio",
        "n_units_with_validator", "validator_shapes", "n_units_with_D_kind",
        "n_units_with_D_dom_covering", "n_units_with_D_op", "n_units_with_D_prev_join",
        "d_layer_unknown", "enforcement_path_counts", "dep_pin_resolvable",
        "effect_fp_audit", "traced_ratio", "parse_failures", "truncations",
    ]
    missing = [k for k in required if k not in p]
    assert not missing, f"probe.json に無いキー: {missing}"
    assert p["traced_ratio"] is None, "A5 の run では traced_ratio は null（§5.1）"
    assert p["n_units_with_D_dom_covering"] == 0, "D_dom パーサは書かない（Def 6）"
