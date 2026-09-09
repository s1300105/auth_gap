"""CFG の構造的な性質（付録 G の 3 つ組では観測されないもの）。

**このテストは §2.5.6 の実装変異の生存数には数えない。** 生存数は付録 G と
支配 mutant の fixture テストだけで計算するのが仕様書の定義であり、
fixture 外のテストを足して見かけの生存数を下げてはならない。
ここで守るのは「fixture が判別しない性質を、それでも壊さない」ことである。
"""

import ast
import textwrap

from authgap.cfgbuild import EXIT_KINDS, build_cfg


def _fn(src: str):
    """関数 AST と「そのソース内の文字列 → 行番号」を返す。

    行番号を直書きすると `textwrap.dedent` の前置改行 1 つでずれる。
    **目印の文字列から引く。**
    """
    text = textwrap.dedent(src).strip("\n")
    fn = ast.parse(text).body[0]

    def line_of(needle: str) -> int:
        for i, line in enumerate(text.splitlines(), 1):
            if needle in line:
                return i
        raise AssertionError(f"見つからない: {needle!r}")

    return fn, line_of


def test_finally_is_duplicated_per_exit_kind():
    """`finally` は脱出種別ごとに複製する（§2.5.1 の唯一の例外）。

    付録 G の G12 は複製の有無で 3 つ組が変わらないので、この性質は
    fixture では判別されない（`docs/decisions.md` D2）。**構造で固定する。**
    """
    fn, line_of = _fn(
        """
        def f(name):
            try:
                approve(name)
            finally:
                run(name)
        """
    )
    cfg = build_cfg(fn)
    copies = [cfg.nodes[n] for n in cfg.nodes_for_line(line_of("run(name)"))]
    assert len(copies) >= 2, "finalbody が複製されていない"
    kinds = {c.copy_kind for c in copies}
    assert kinds <= set(EXIT_KINDS)
    assert {"normal", "exc"} <= kinds, f"正常複製と例外複製の両方が要る: {kinds}"
    for c in copies:
        assert c.copy_kind in c.witness(), "witness に脱出種別が入っていない"


def test_return_inside_try_gets_its_own_finally_copy():
    """`return` の脱出経路にも複製が要る。"""
    fn, line_of = _fn(
        """
        def f(name):
            try:
                if bad(name):
                    return ""
                ok(name)
            finally:
                run(name)
        """
    )
    cfg = build_cfg(fn)
    kinds = {cfg.nodes[n].copy_kind for n in cfg.nodes_for_line(line_of("run(name)"))}
    assert "return" in kinds, f"return 用の複製が無い: {kinds}"


def test_for_loop_has_zero_iteration_exit():
    """`for` は 0 回実行があるので、本体内のゲートは後続をゲートしない。"""
    fn, _line_of = _fn(
        """
        def f(names):
            for n in names:
                if allow(n):
                    run(n)
            after()
        """
    )
    cfg = build_cfg(fn)
    headers = [n for n, nd in cfg.nodes.items() if nd.label == "for-header"]
    assert headers
    assert cfg.successors(headers[0], ("loop_exit",)), "0 回実行の脱出辺が無い"


def test_process_exit_does_not_fall_through():
    """`sys.exit` は後続へ落ちない（A-b のゲート要約が判定できなくなる）。"""
    fn, line_of = _fn(
        """
        def f(name):
            if not allow(name):
                sys.exit(1)
            run(name)
        """
    )
    cfg = build_cfg(fn)
    target = line_of("sys.exit(1)")
    exits = [n for n, nd in cfg.nodes.items() if nd.lineno == target and nd.kind == "stmt"]
    assert exits
    assert not cfg.successors(exits[0], ("seq",)), "sys.exit から後続へ辺が出ている"
