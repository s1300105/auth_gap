"""§2.6 の val 受け入れ fixture F1–F10 の採点器。

**期待値 `fixtures/val/expected.json` は仕様の表から書き、この採点器より先にコミットした**
（コミット 5944a0b、CLAUDE.md 規則 5）。期待値ファイルを出力に合わせて書き換えない。
実装が満たさない項目は `KNOWN_UNMET` に xfail(strict) として残し、誤りの向きを
`docs/open_questions.md` に記録する。XPASS になったら印を外す。

採点の単位は「fixture × 項目」で、1 項目 = 1 テスト。項目の id は
`F1/effect[git.Git.checkout]/slot[cwd].attrs_absent[canonicalised]` のような文字列で、
`KNOWN_UNMET` のキーはこの id である。

木の取り方:
* F1–F4（A1 / A5 の較正対）は `authgap.runner.run`（probe 経路）で普通に入口を拾う。
* F5–F8（OpenManus 3309bf4e）は R2 カタログに `BaseTool.execute` が無いので
  `Unit` を手で組んで `analyze_unit_f0a` に通す（`expected.json` の `forced_entry`）。
  入口認識の是非はここでは試験しない（D17「直さない 3」）。
* F9 / F10 は木が未取得なので skip（xfail ではない: 未測定であって未達ではない）。
"""

from __future__ import annotations

import ast
import json
import os
from collections.abc import Callable
from typing import Any

import pytest

from authgap.analyze import analyze_unit_f0a
from authgap.entries import Unit, params_of
from authgap.runner import RunConfig, run
from authgap.srcindex import SourceIndex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXPECTED_PATH = os.path.join(ROOT, "fixtures", "val", "expected.json")
EXPECTED = json.load(open(EXPECTED_PATH, encoding="utf-8"))
FIXTURES: dict[str, dict] = EXPECTED["fixtures"]
TREES: dict[str, dict] = EXPECTED["trees"]

#: 正規化子の transform（Def 5 (i) の canonical alias を作るもの）。
CANONICALISING = frozenset({"realpath", "Path.resolve", "normpath+abspath", "normpath", "abspath"})

#: 実装が満たさない項目（id → 理由）。**向きを書く。** XPASS で strict が落ちたら外す。
#: 初回の採点（2026-09-21、fixture 期待値 5944a0b）: 74 項目中 26 項目が未達。
#: 内訳と診断は docs/open_questions.md O17。
_F6_SPAWN = "F6/effect[asyncio.create_subprocess_shell]"
_F6_PIPE = "F6/effect[pipe:write]"
_F7_WT = "F7/effect[pathlib.Path.write_text]"
_F8_ARUN = "F8/effect[crawl4ai.AsyncWebCrawler.arun]"
_R_F2 = (
    "仕様内の食い違い（F2『alias_facts が空』と F7『Path() の alias fact を含める』）。"
    "実装は F7 側（`Path()` を非正規化の alias fact として出す）。正規化子が無いことは"
    " `alias_facts_canonical_absent_for_root` で別に通っている。向き: 中立（O17 (a)）"
)
_R_DEPTH = "manifest に `depth_used` の欄が無い（未出力。仕様 §2.6 の期待行の属性）。向き: 中立（O17 (b)）"
_R_F6 = (
    "`self._session` が `Optional[_BashSession]`（None との合流で Obj が Unknown に落ちる）ため"
    "受け手型が消え、`_BashSession.start` は末尾名解決 + opaque(unresolved)、`self.command` は"
    "読めず、`run` の `self._process.stdin.write` は出ない。向き: **false-clean**（MODEL の"
    " `command` が bash の stdin に届く EXEC 行が無い。ユニットは opaque(receiver/unresolved) で"
    " clean ではない）。O17 (c)"
)
_R_F7 = (
    "`operator = self._get_operator()`（IfExp で `LocalFileOperator` / `SandboxFileOperator` の"
    " 2 型 Obj）を `str_replace` / `insert` 経由で `operator.write_file` に渡す経路が深さ 3 で"
    " cap（`cap_hits = depth`）に当たり FS_WRITE 行が出ない。向き: **false-clean**（MODEL の"
    " `path` への書き込み行が無い。ユニットは opaque(depth) で clean ではない）。O17 (d)"
)
_R_F8 = (
    "`async with AsyncWebCrawler(config=...) as crawler` の ctor は CTOR カタログにあるが、"
    "`crawler.arun(url=url, ...)` の proxy sink が当たらない（受け手 opaque(receiver)）。"
    "向き: **false-clean**（MODEL の `urls` が NET の url.host に届く行が無い。ユニットは"
    " opaque で clean ではない）。O17 (e)"
)
KNOWN_UNMET: dict[str, str] = {
    "F2/alias_facts_empty_literal": _R_F2,
    "F5/effect[builtins.exec]/depth_used": _R_DEPTH,
    f"{_F6_SPAWN}/present": _R_F6,
    f"{_F6_SPAWN}/slot[argv0].prin": _R_F6,
    f"{_F6_SPAWN}/slot[argv0].const": _R_F6,
    f"{_F6_SPAWN}/exec_mode.shell.prin": _R_F6,
    f"{_F6_SPAWN}/exec_mode.shell.const": _R_F6,
    f"{_F6_PIPE}/present": _R_F6,
    f"{_F6_PIPE}/slot[code_text].prin": _R_F6,
    f"{_F6_PIPE}/slot[code_text].roots": _R_F6,
    f"{_F6_PIPE}/depth_used": _R_F6 + "；さらに " + _R_DEPTH,
    f"{_F7_WT}/present": _R_F7,
    f"{_F7_WT}/slot[path].prin": _R_F7,
    f"{_F7_WT}/slot[path].roots": _R_F7,
    f"{_F7_WT}/resolution": _R_F7,
    f"{_F7_WT}/witness_chain_includes": _R_F7,
    "F7/effects_count[pathlib.Path.write_text]=2": _R_F7,
    f"{_F8_ARUN}/present": _R_F8,
    f"{_F8_ARUN}/slot[url.host].prin": _R_F8,
    f"{_F8_ARUN}/slot[url.host].roots": _R_F8,
    f"{_F8_ARUN}/slot[url.host].shape_k": _R_F8,
    f"{_F8_ARUN}/slot[url.host].shape_tail": _R_F8,
}


# --------------------------------------------------------------------------
# 木の準備
# --------------------------------------------------------------------------


def _tree_path(tree: str) -> str:
    return os.path.join(ROOT, "corpus", tree)


def _tree_ready(tree: str) -> bool:
    return os.path.isdir(_tree_path(tree))


def _tree_sha(tree: str) -> str | None:
    import subprocess

    try:
        return subprocess.run(
            ["git", "-C", _tree_path(tree), "rev-parse", "HEAD"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
    except Exception:  # noqa: BLE001
        return None


class _UnitView:
    """採点器が見る 1 ユニットの出力（manifest と同じ JSON 形）。"""

    def __init__(self, report, index: SourceIndex) -> None:
        self.report = report
        self.index = index
        self.effects: list[dict] = [e.to_json() for e in report.effects]
        self.alias_facts: list[dict] = (
            [a.to_json() for a in report.val.alias_facts] if report.val is not None else []
        )
        self.opaque_reasons: list[str] = (
            sorted(set(report.val.opaque_reasons)) if report.val is not None else []
        )
        self.config_atoms: dict = dict(report.config_atoms or {})


_CACHE: dict[tuple, Any] = {}


def _index_for(tree: str) -> SourceIndex:
    key = ("index", tree)
    if key not in _CACHE:
        idx = SourceIndex(_tree_path(tree))
        idx.build()
        _CACHE[key] = idx
    return _CACHE[key]


def _scanned_units(tree: str) -> dict[str, _UnitView]:
    key = ("scan", tree)
    if key not in _CACHE:
        pop = TREES[tree]["population"]
        res = run(RunConfig(src_root=_tree_path(tree), population=pop, full=False))
        idx = _index_for(tree)
        _CACHE[key] = {u.unit.qualname: _UnitView(u, idx) for u in res.tree.units}
    return _CACHE[key]


def _forced_unit(tree: str, qualname: str, relpath: str) -> Unit:
    idx = _index_for(tree)
    path = os.path.join(idx.src_root, relpath)
    module = idx.module_name(path)
    cands = [f for f in idx.lookup_function(qualname, module) if f.relpath == relpath]
    assert len(cands) == 1, (qualname, relpath, [f.relpath for f in cands])
    fd = cands[0]
    return Unit(
        framework="fixture-forced",
        entry_kind="method",
        module=fd.module,
        qualname=fd.qualname,
        relpath=fd.relpath,
        node=fd.node,
        params=params_of(fd.node),
        tool_name=qualname.split(".")[-1],
        is_async=fd.is_async,
    )


def _forced_view(tree: str, qualname: str, relpath: str) -> _UnitView:
    key = ("forced", tree, qualname, relpath)
    if key not in _CACHE:
        idx = _index_for(tree)
        unit = _forced_unit(tree, qualname, relpath)
        _CACHE[key] = _UnitView(analyze_unit_f0a(idx, unit), idx)
    return _CACHE[key]


def _view(fid: str) -> _UnitView:
    fx = FIXTURES[fid]
    tree = fx["tree"]
    unit = fx["unit"]
    if unit.get("forced_entry"):
        return _forced_view(tree, unit["qualname"], unit["relpath"])
    units = _scanned_units(tree)
    assert unit["qualname"] in units, sorted(units)
    v = units[unit["qualname"]]
    assert v.report.unit.relpath == unit["relpath"]
    return v


def _function_line_range(index: SourceIndex, relpath: str, funcname: str) -> tuple[int, int] | None:
    """`relpath` の中で末尾名が `funcname` の関数の行範囲（1 つに定まるときだけ）。"""
    path = os.path.join(index.src_root, relpath)
    tree = index.parse(path)
    if tree is None:
        return None
    found = [
        n for n in ast.walk(tree)
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == funcname
    ]
    if len(found) != 1:
        return None
    n = found[0]
    return n.lineno, getattr(n, "end_lineno", n.lineno)


def _site_line(site: str) -> tuple[str, int]:
    rel, _, line = site.rpartition(":L")
    return rel, int(line)


# --------------------------------------------------------------------------
# 項目の生成（1 fixture → 複数の (id, check) 対）
# --------------------------------------------------------------------------


def _rows_matching(view: _UnitView, exp: dict) -> list[dict]:
    rows = [
        r for r in view.effects
        if r["site"] == exp["site"] and r["kind"] == exp["kind"] and r["form"] == exp["form"]
    ]
    # slot の名前で絞る（同じ site に slot 束縛違いの 2 行が出る F3 のため）。
    want = set(exp.get("slots", {}))
    if want:
        rows = [r for r in rows if want <= set(r["slots"])]
    return rows


def _check_slot(view: _UnitView, exp: dict, slot: str, cond: dict, item: str) -> Callable[[], None]:
    def check() -> None:
        rows = _rows_matching(view, exp)
        assert rows, f"行が無い: {exp['site']} {exp['kind']}@{exp['form']} slots={sorted(exp.get('slots', {}))}"
        errors = []
        for r in rows:
            v = r["slots"][slot]
            if item == "prin":
                if v["prin"] != cond["prin"]:
                    errors.append(f"prin={v['prin']}")
            elif item == "const":
                if v["shape"].get("const") != cond["const"]:
                    errors.append(f"const={v['shape'].get('const')!r}")
            elif item == "roots":
                if set(v.get("roots", [])) != set(cond["roots"]):
                    errors.append(f"roots={v.get('roots')}")
            elif item.startswith("attrs_absent["):
                a = item[len("attrs_absent["):-1]
                if a in v.get("attrs", []):
                    errors.append(f"attrs={v.get('attrs')}")
            elif item == "shape_k":
                if v["shape"].get("k") != cond["shape_k"]:
                    errors.append(f"shape.k={v['shape'].get('k')}")
            elif item == "shape_tail":
                if "tail" not in v["shape"]:
                    errors.append("shape に tail が無い")
            elif item == "config_atom":
                # 仕様の `cwd = config-atom(base_dir, default=None)/default-open` の欄は
                # manifest に無い。値が config atom 由来であることを `prov`/`roots` からは
                # 読めないので、この項目は未出力として扱う。
                errors.append("manifest に config-atom の欄が無い")
            else:  # pragma: no cover
                raise AssertionError(item)
        # **1 行でも満たせば良い**のではなく、同じ site/slot の行はすべて満たすことを要求する。
        assert not errors, errors

    return check


def _check_row_field(view: _UnitView, exp: dict, field: str) -> Callable[[], None]:
    def check() -> None:
        rows = _rows_matching(view, exp)
        assert rows, f"行が無い: {exp['site']} {exp['kind']}@{exp['form']}"
        errors = []
        for r in rows:
            if field == "resolution":
                if r.get("resolution") != exp["resolution"]:
                    errors.append(f"resolution={r.get('resolution')}")
            elif field == "depth_used":
                if "depth_used" not in r:
                    errors.append("manifest に depth_used の欄が無い")
                elif r["depth_used"] != exp["depth_used"]:
                    errors.append(f"depth_used={r['depth_used']}")
            elif field == "witness_chain_includes":
                chain = " ".join(r.get("witness_chain", []))
                missing = [w for w in exp["witness_chain_includes"] if w not in chain]
                if missing:
                    errors.append(f"witness_chain={r.get('witness_chain')} に {missing} が無い")
            elif field.startswith("exec_mode.shell."):
                k = field[len("exec_mode.shell."):]
                shell = (r.get("exec_mode") or {}).get("shell") or {}
                want = exp["exec_mode"]["shell"][k]
                if shell.get(k) != want:
                    errors.append(f"exec_mode.shell.{k}={shell.get(k)!r} (want {want!r})")
            else:  # pragma: no cover
                raise AssertionError(field)
        assert not errors, errors

    return check


def _items_for(fid: str) -> list[tuple[str, Callable[[], None]]]:
    fx = FIXTURES[fid]
    items: list[tuple[str, Callable[[], None]]] = []
    if fx.get("tree") is None:
        return items
    view = _view(fid)

    for exp in fx.get("effects", []):
        tag = f"{fid}/effect[{exp['site']}]"

        def present(exp=exp) -> None:
            rows = _rows_matching(view, exp)
            assert rows, (
                f"行が無い: {exp['site']} {exp['kind']}@{exp['form']} "
                f"slots={sorted(exp.get('slots', {}))}; あるのは "
                f"{[(r['site'], r['kind'], r['form'], sorted(r['slots'])) for r in view.effects]}"
            )

        items.append((f"{tag}/present", present))
        for slot, cond in exp.get("slots", {}).items():
            for key in cond:
                if key == "attrs_absent":
                    for a in cond[key]:
                        items.append((f"{tag}/slot[{slot}].attrs_absent[{a}]",
                                      _check_slot(view, exp, slot, cond, f"attrs_absent[{a}]")))
                else:
                    items.append((f"{tag}/slot[{slot}].{key}", _check_slot(view, exp, slot, cond, key)))
        for field in ("resolution", "depth_used", "witness_chain_includes"):
            if field in exp:
                items.append((f"{tag}/{field}", _check_row_field(view, exp, field)))
        for k in (exp.get("exec_mode") or {}).get("shell", {}):
            items.append((f"{tag}/exec_mode.shell.{k}", _check_row_field(view, exp, f"exec_mode.shell.{k}")))

    if "effects_count" in fx:
        c = fx["effects_count"]

        def count() -> None:
            rows = [r for r in view.effects if r["site"] == c["site"] and r["kind"] == c["kind"] and r["form"] == c["form"]]
            assert len(rows) == c["n"], [(r["site"], sorted(r["slots"])) for r in rows]

        items.append((f"{fid}/effects_count[{c['site']}]={c['n']}", count))

    if "effects_count_total" in fx:
        n = fx["effects_count_total"]

        def total() -> None:
            assert len(view.effects) == n, [(r["site"], r["kind"], r["form"]) for r in view.effects]

        items.append((f"{fid}/effects_count_total={n}", total))

    for af in fx.get("alias_facts_include", []):
        def alias(af=af) -> None:
            hits = [a for a in view.alias_facts if a["root"] == af["root"] and a["transform"] == af["transform"]]
            assert hits, f"alias_facts={view.alias_facts}"
            if "in_function" in af:
                rng = _function_line_range(view.index, fx["unit"]["relpath"], af["in_function"])
                assert rng is not None, f"関数 {af['in_function']} が 1 つに定まらない"
                inside = [a for a in hits if rng[0] <= _site_line(a["site"])[1] <= rng[1]]
                assert inside, f"{af['in_function']} の行範囲 {rng} に無い: {hits}"

        items.append((f"{fid}/alias_facts_include[{af['root']},{af['transform']}]", alias))

    if "alias_facts_canonical_absent_for_root" in fx:
        root = fx["alias_facts_canonical_absent_for_root"]

        def no_canon() -> None:
            bad = [a for a in view.alias_facts if a["root"] == root and a["transform"] in CANONICALISING]
            assert not bad, bad

        items.append((f"{fid}/alias_facts_canonical_absent_for_root[{root}]", no_canon))

    if fx.get("alias_facts_empty_literal"):
        def empty() -> None:
            assert view.alias_facts == [], view.alias_facts

        items.append((f"{fid}/alias_facts_empty_literal", empty))

    for atom in fx.get("config_atoms_include", []):
        def has_atom(atom=atom) -> None:
            assert atom in view.config_atoms, view.config_atoms

        items.append((f"{fid}/config_atoms_include[{atom}]", has_atom))

    return items


def _all_items() -> list:
    out = []
    for fid in FIXTURES:
        fx = FIXTURES[fid]
        if fx.get("tree") is None or not _tree_ready(fx["tree"]):
            out.append(pytest.param(fid, None, id=f"{fid}/tree_missing",
                                    marks=pytest.mark.skip(reason=f"{fid}: 木が未取得（{fx.get('tree_needed') or fx['tree']}）")))
            continue
        for item_id, check in _items_for(fid):
            marks = []
            if item_id in KNOWN_UNMET:
                marks.append(pytest.mark.xfail(strict=True, reason=KNOWN_UNMET[item_id]))
            out.append(pytest.param(fid, check, id=item_id, marks=marks))
    return out


# --------------------------------------------------------------------------
# 前提（印なし）
# --------------------------------------------------------------------------


@pytest.mark.parametrize("tree", sorted(TREES))
def test_precondition_tree_sha(tree):
    if not _tree_ready(tree):
        pytest.skip(f"{tree} が未取得")
    assert _tree_sha(tree) == TREES[tree]["sha"], "corpus の pin が expected.json と違う（SHA 一致を検証する）"


def test_precondition_known_unmet_keys_exist():
    ids = {item_id for fid in FIXTURES if FIXTURES[fid].get("tree") and _tree_ready(FIXTURES[fid]["tree"])
           for item_id, _ in _items_for(fid)}
    stale = sorted(set(KNOWN_UNMET) - ids)
    assert not stale, f"KNOWN_UNMET に無い項目の id: {stale}"


# --------------------------------------------------------------------------
# 本体
# --------------------------------------------------------------------------


@pytest.mark.parametrize("fid,check", _all_items())
def test_val_fixture_item(fid, check):
    check()


# --------------------------------------------------------------------------
# F5 の負のアサート: INDIRECT 表から multiprocessing.Process を外しても clean にならない
# --------------------------------------------------------------------------


def test_f5_negative_indirect_removed(monkeypatch):
    fx = FIXTURES["F5"]
    if not _tree_ready(fx["tree"]):
        pytest.skip("OpenManus が未取得")
    from authgap.val import engine as val_engine

    table = dict(val_engine.INDIRECT_BY_NAME)
    removed = fx["negative_assert"]["remove_indirect"]
    assert removed in table
    del table[removed]
    monkeypatch.setattr(val_engine, "INDIRECT_BY_NAME", table)
    _CACHE.pop(("forced", fx["tree"], fx["unit"]["qualname"], fx["unit"]["relpath"]), None)
    try:
        view = _forced_view(fx["tree"], fx["unit"]["qualname"], fx["unit"]["relpath"])
    finally:
        _CACHE.pop(("forced", fx["tree"], fx["unit"]["qualname"], fx["unit"]["relpath"]), None)
    exec_rows = [r for r in view.effects if r["kind"] == "EXEC"]
    opaque_in_rows = any(
        r["slots"].get("code_text", {}).get("prov", "").startswith("opaque") for r in exec_rows
    )
    opaque_in_unit = "unresolved" in view.opaque_reasons
    # **clean（EXEC 行が無く opaque も無い）は不健全。** どちらかで opaque が残ること。
    assert opaque_in_rows or opaque_in_unit, {
        "exec_rows": exec_rows, "opaque_reasons": view.opaque_reasons,
    }
