"""§2.5.1: CFG の構成（標準ライブラリ `ast` のみ）。

規則（仕様書が名指しで固定しているもの）:

* 関数ごとに ``ENTRY`` / ``EXIT`` / ``EXC_EXIT`` と、原則「文 1 個 = ノード 1 個」。
  **基本ブロック併合は行わない。**
* ``if`` は test ノードから True/False 辺。**「body が全部 exit 文か」という
  構文条件は使わない**（前身の `_is_exit_body` が G1 を落とした原因）。
* ``while`` / ``for`` は進入辺・脱出辺・後退辺。``for`` は 0 回実行があるので
  ループ本体内のゲートはループ外の後続をゲートしない。
* ``try`` は body の各文から handler へ例外辺（保守側: `Constant` のみの代入以外は
  すべて送出しうる）。
* ``with`` は ``ENTER(cm)`` / ``EXIT(cm)`` の仮想ノード。``contextlib.suppress(E)``
  は body から出た例外辺を後続へ吸収する。
* ``A and B`` / ``A or B`` / ``IfExp`` / ``NamedExpr`` は式ノードの分岐へ脱糖する
  （これで ``or`` の極性と walrus が構文特例なしに出る）。
* ``match`` は ``if`` 連鎖へ脱糖。
* 内包表記 / genexp は合成した無名関数として別 CFG。
* **唯一の例外は ``finally``。** finalbody は脱出種別ごとに複製する。
* 1 関数 :data:`authgap.ir.CFG_NODE_CAP` ノード超で ``OPAQUE(cfg_cap)``。

**辺のラベルは真偽の極性を保つ。** `deny(g)` は「肯定センスなら false 辺の後継」
で定義されるので、合流のときにラベルを ``seq`` へ落とすと極性が消える。
したがって部分グラフの出口は `(ノード, 辺ラベル)` の対で持ち回す。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Optional

from .ir import CFG_NODE_CAP

#: ノード種別。
NODE_KINDS = ("entry", "exit", "exc_exit", "stmt", "test", "enter_cm", "exit_cm", "loop_header", "handler")

#: 辺種別。
EDGE_KINDS = ("seq", "true", "false", "exc", "back", "loop_exit")

#: `finally` 複製の脱出種別。
EXIT_KINDS = ("normal", "exc", "return", "break", "continue")

#: 部分グラフの出口: `(ノード id, その出口が使う辺ラベル)`。
Exit = tuple[int, str]


@dataclass
class Node:
    id: int
    kind: str
    lineno: Optional[int] = None
    col: Optional[int] = None
    ast_node: Optional[ast.AST] = None
    label: str = ""
    #: `finally` 複製のときの脱出種別。
    copy_kind: Optional[str] = None
    #: この test ノードが評価する式（脱糖後の 1 オペランド）。
    test_expr: Optional[ast.AST] = None
    #: 内包表記の別 CFG（あれば）。
    subgraph: Optional["CFG"] = None

    def witness(self) -> str:
        """witness 行の表記。`finally` 複製は脱出種別を併記する（§2.5.1）。"""
        if self.lineno is None:
            return self.label or self.kind
        if self.copy_kind:
            return f"finally-copy({self.copy_kind}) @ L{self.lineno}"
        return f"L{self.lineno}"


@dataclass
class CFG:
    """1 関数分の制御フローグラフ。"""

    func: ast.AST
    nodes: dict[int, Node] = field(default_factory=dict)
    succ: dict[int, list[tuple[int, str]]] = field(default_factory=dict)
    pred: dict[int, list[tuple[int, str]]] = field(default_factory=dict)
    entry: int = 0
    exit: int = 1
    exc_exit: int = 2
    #: 構築中に立った OPAQUE 理由（ゲート側語彙）。
    opaque: list[str] = field(default_factory=list)
    #: 元ソース行 → その行を持つノード id の列（`finally` 複製で 1 対多になる）。
    by_line: dict[int, list[int]] = field(default_factory=dict)

    def add_node(self, node: Node) -> int:
        self.nodes[node.id] = node
        self.succ.setdefault(node.id, [])
        self.pred.setdefault(node.id, [])
        if node.lineno is not None:
            self.by_line.setdefault(node.lineno, []).append(node.id)
        return node.id

    def add_edge(self, a: int, b: int, kind: str = "seq") -> None:
        if kind not in EDGE_KINDS:
            raise ValueError(f"未知の辺種別: {kind}")
        if (b, kind) not in self.succ.setdefault(a, []):
            self.succ[a].append((b, kind))
            self.pred.setdefault(b, []).append((a, kind))

    def successors(self, n: int, kinds: Optional[tuple[str, ...]] = None) -> list[int]:
        return [b for b, k in self.succ.get(n, ()) if kinds is None or k in kinds]

    def nodes_for_line(self, lineno: int) -> list[int]:
        """その行に対応する CFG ノード（`finally` 複製で複数になりうる）。"""
        return list(self.by_line.get(lineno, ()))

    def size(self) -> int:
        return len(self.nodes)

    def reachable_from(self, start: int, blocked: frozenset[int] = frozenset()) -> set[int]:
        """`blocked` の節点を除いたグラフでの到達集合（`CFG∖{g}` の実装）。"""
        seen: set[int] = set()
        stack = [start]
        while stack:
            n = stack.pop()
            if n in seen or n in blocked:
                continue
            seen.add(n)
            for b, _k in self.succ.get(n, ()):
                if b not in seen and b not in blocked:
                    stack.append(b)
        return seen


@dataclass
class _Frag:
    """部分グラフ。`entry` は入口、`exits` は次文へ落ちる出口の列。"""

    entry: Optional[int]
    exits: list[Exit] = field(default_factory=list)


@dataclass
class _Ctx:
    """構築文脈。例外辺の宛先とループ / finally のスタック。"""

    exc_targets: list[int] = field(default_factory=list)
    suppress_targets: list[int] = field(default_factory=list)
    #: ループの `(continue の宛先, break の宛先)`。
    loops: list[tuple[int, int]] = field(default_factory=list)
    #: `finally` 節の AST 本体（内側から順）。複製に使う。
    finallys: list[list] = field(default_factory=list)

    def child(self, **kw) -> "_Ctx":
        return _Ctx(
            kw.get("exc_targets", list(self.exc_targets)),
            kw.get("suppress_targets", list(self.suppress_targets)),
            kw.get("loops", list(self.loops)),
            kw.get("finallys", list(self.finallys)),
        )


class CFGBuilder:
    """1 関数から CFG を組む。"""

    def __init__(self, func: ast.AST) -> None:
        self.func = func
        self.cfg = CFG(func=func)
        self._next_id = 0
        self._capped = False
        self.entry = self._new("entry", label="ENTRY")
        self.exit = self._new("exit", label="EXIT")
        self.exc_exit = self._new("exc_exit", label="EXC_EXIT")
        self.cfg.entry, self.cfg.exit, self.cfg.exc_exit = self.entry, self.exit, self.exc_exit

    # -- 基本操作 ---------------------------------------------------------

    def _new(
        self,
        kind: str,
        node: Optional[ast.AST] = None,
        label: str = "",
        copy_kind: Optional[str] = None,
        test_expr: Optional[ast.AST] = None,
    ) -> int:
        if self.cfg.size() >= CFG_NODE_CAP and not self._capped:
            self._capped = True
            if "cfg_cap" not in self.cfg.opaque:
                self.cfg.opaque.append("cfg_cap")
        nid = self._next_id
        self._next_id += 1
        self.cfg.add_node(
            Node(
                id=nid,
                kind=kind,
                lineno=getattr(node, "lineno", None),
                col=getattr(node, "col_offset", None),
                ast_node=node,
                label=label or (type(node).__name__ if node is not None else kind),
                copy_kind=copy_kind,
                test_expr=test_expr,
            )
        )
        return nid

    def _exc_target(self, ctx: _Ctx) -> int:
        if ctx.suppress_targets:
            return ctx.suppress_targets[-1]
        if ctx.exc_targets:
            return ctx.exc_targets[-1]
        return self.exc_exit

    def _link_exc(self, nid: int, ctx: _Ctx, node: Optional[ast.AST]) -> None:
        """保守側の例外辺: `Constant` のみの代入以外はすべて送出しうる（§2.5.1）。"""
        if node is not None and _cannot_raise(node):
            return
        self.cfg.add_edge(nid, self._exc_target(ctx), "exc")

    def _connect(self, exits: list[Exit], target: int) -> None:
        for nid, kind in exits:
            self.cfg.add_edge(nid, target, kind)

    # -- 入口 -------------------------------------------------------------

    def build(self) -> CFG:
        ctx = _Ctx()
        frag = self._stmts(list(getattr(self.func, "body", [])), ctx)
        if frag.entry is None:
            self.cfg.add_edge(self.entry, self.exit)
        else:
            self.cfg.add_edge(self.entry, frag.entry)
            self._connect(frag.exits, self.exit)
        return self.cfg

    # -- 文の列 -----------------------------------------------------------

    def _stmts(self, stmts: list, ctx: _Ctx) -> _Frag:
        entry: Optional[int] = None
        prev: list[Exit] = []
        for st in stmts:
            frag = self._stmt(st, ctx)
            if frag.entry is None:
                continue
            if entry is None:
                entry = frag.entry
            self._connect(prev, frag.entry)
            prev = frag.exits
        return _Frag(entry, prev)

    def _stmt(self, st, ctx: _Ctx) -> _Frag:
        m = getattr(self, "_st_" + type(st).__name__, None)
        if m is None:
            # §2.5.1: 出現率 1% 未満の構文は実装せず OPAQUE(unsupported_syntax) に落とす。
            if "unsupported_syntax" not in self.cfg.opaque:
                self.cfg.opaque.append("unsupported_syntax")
            nid = self._new("stmt", st, label=f"unsupported:{type(st).__name__}")
            self._link_exc(nid, ctx, st)
            return _Frag(nid, [(nid, "seq")])
        return m(st, ctx)

    # -- 単純文 -----------------------------------------------------------

    def _simple(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        self._attach_comprehensions(nid, st)
        self._link_exc(nid, ctx, st)
        return _Frag(nid, [(nid, "seq")])

    _st_Expr = _simple
    _st_Assign = _simple
    _st_AugAssign = _simple
    _st_AnnAssign = _simple
    _st_Delete = _simple
    _st_Assert = _simple
    _st_Import = _simple
    _st_ImportFrom = _simple
    _st_Global = _simple
    _st_Nonlocal = _simple
    _st_FunctionDef = _simple
    _st_AsyncFunctionDef = _simple
    _st_ClassDef = _simple

    def _st_Pass(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        return _Frag(nid, [(nid, "seq")])

    # -- 脱出文 -----------------------------------------------------------

    def _st_Return(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        self._attach_comprehensions(nid, st)
        self._link_exc(nid, ctx, st)
        self.cfg.add_edge(nid, self._finally_chain(ctx, "return", self.exit))
        return _Frag(nid, [])

    def _st_Raise(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        self.cfg.add_edge(nid, self._finally_chain(ctx, "exc", self._exc_target(ctx)), "exc")
        return _Frag(nid, [])

    def _st_Break(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        if ctx.loops:
            self.cfg.add_edge(nid, self._finally_chain(ctx, "break", ctx.loops[-1][1]))
        return _Frag(nid, [])

    def _st_Continue(self, st, ctx: _Ctx) -> _Frag:
        nid = self._new("stmt", st)
        if ctx.loops:
            self.cfg.add_edge(nid, self._finally_chain(ctx, "continue", ctx.loops[-1][0]), "back")
        return _Frag(nid, [])

    def _finally_chain(self, ctx: _Ctx, exit_kind: str, final_target: int) -> int:
        """脱出経路上の `finally` を脱出種別つきで複製し、その入口を返す。"""
        target = final_target
        for body in reversed(ctx.finallys):
            frag = self._copy_finally(body, exit_kind, ctx)
            if frag.entry is None:
                continue
            self._connect(frag.exits, target)
            target = frag.entry
        return target

    def _copy_finally(self, body: list, exit_kind: str, ctx: _Ctx) -> _Frag:
        """finalbody を 1 つの脱出種別ぶん複製する。

        複製の中では同じ `finally` を再帰的に複製しない（無限展開を避ける）。
        """
        sub = ctx.child(finallys=[])
        entry: Optional[int] = None
        prev: list[Exit] = []
        for st in body:
            nid = self._new("stmt", st, copy_kind=exit_kind)
            self._attach_comprehensions(nid, st)
            self._link_exc(nid, sub, st)
            if entry is None:
                entry = nid
            self._connect(prev, nid)
            prev = [(nid, "seq")]
        return _Frag(entry, prev)

    # -- 分岐 -------------------------------------------------------------

    def _st_If(self, st, ctx: _Ctx) -> _Frag:
        body_frag = self._stmts(st.body, ctx)
        else_frag = self._stmts(st.orelse, ctx) if st.orelse else _Frag(None, [])
        tf = _TestBuilder(self, ctx).build(st.test, body_frag.entry, else_frag.entry)
        exits: list[Exit] = list(body_frag.exits) + list(else_frag.exits)
        if body_frag.entry is None:
            exits += tf.true_pending
        if else_frag.entry is None:
            exits += tf.false_pending
        return _Frag(tf.entry, exits)

    # -- ループ -----------------------------------------------------------

    def _st_While(self, st, ctx: _Ctx) -> _Frag:
        header = self._new("loop_header", st, label="while-header")
        after = self._new("stmt", None, label="loop-exit")
        sub = ctx.child(loops=ctx.loops + [(header, after)])
        body_frag = self._stmts(st.body, sub)
        tf = _TestBuilder(self, ctx).build(st.test, body_frag.entry, after)
        self.cfg.add_edge(header, tf.entry)
        if body_frag.entry is None:
            for nid, _k in tf.true_pending:
                self.cfg.add_edge(nid, header, "back")
        for nid, _k in body_frag.exits:
            self.cfg.add_edge(nid, header, "back")
        return self._loop_orelse(st, ctx, header, after)

    def _loop_for(self, st, ctx: _Ctx) -> _Frag:
        """`for` は 0 回実行があるので、ループ本体内のゲートは後続をゲートしない。

        header から後続への ``loop_exit`` 辺を必ず引くことでそれを表現する。
        """
        header = self._new("loop_header", st, label="for-header")
        self._link_exc(header, ctx, st)
        after = self._new("stmt", None, label="loop-exit")
        sub = ctx.child(loops=ctx.loops + [(header, after)])
        body_frag = self._stmts(st.body, sub)
        if body_frag.entry is not None:
            self.cfg.add_edge(header, body_frag.entry, "true")
        for nid, _k in body_frag.exits:
            self.cfg.add_edge(nid, header, "back")
        self.cfg.add_edge(header, after, "loop_exit")
        return self._loop_orelse(st, ctx, header, after)

    _st_For = _loop_for
    _st_AsyncFor = _loop_for

    def _loop_orelse(self, st, ctx: _Ctx, header: int, after: int) -> _Frag:
        if getattr(st, "orelse", None):
            ofrag = self._stmts(st.orelse, ctx)
            if ofrag.entry is not None:
                self.cfg.add_edge(after, ofrag.entry)
                return _Frag(header, ofrag.exits)
        return _Frag(header, [(after, "seq")])

    # -- try / except / finally -------------------------------------------

    def _st_Try(self, st, ctx: _Ctx) -> _Frag:
        """例外経路は 3 つに分かれる。

        1. handler がある → body の各文から最初の handler へ ``exc`` 辺。
        2. handler が無く `finally` がある → body の各文から **finally(exc) 複製**へ。
           複製の出口は外側の例外宛先へ抜ける（`finally` は例外を飲まない）。
        3. どちらも無い → 外側の例外宛先。

        return / break / continue 側の複製は :meth:`_finally_chain` が作る。
        """
        has_final = bool(getattr(st, "finalbody", None))

        fin_exc_entry: Optional[int] = None
        if has_final and not st.handlers:
            fin_exc = self._copy_finally(st.finalbody, "exc", ctx)
            if fin_exc.entry is not None:
                fin_exc_entry = fin_exc.entry
                for nid, _k in fin_exc.exits:
                    self.cfg.add_edge(nid, self._exc_target(ctx), "exc")

        handler_entries: list[int] = []
        handler_exits: list[Exit] = []
        handler_ctx = ctx.child(finallys=ctx.finallys + ([st.finalbody] if has_final else []))
        for h in st.handlers:
            hid = self._new("handler", h, label="except")
            handler_entries.append(hid)
            hfrag = self._stmts(h.body, handler_ctx)
            if hfrag.entry is not None:
                self.cfg.add_edge(hid, hfrag.entry)
                handler_exits += hfrag.exits
            else:
                handler_exits.append((hid, "seq"))
        first_handler = handler_entries[0] if handler_entries else None

        if first_handler is not None:
            body_exc = first_handler
        elif fin_exc_entry is not None:
            body_exc = fin_exc_entry
        else:
            body_exc = self._exc_target(ctx)

        body_ctx = ctx.child(
            exc_targets=ctx.exc_targets + [body_exc],
            finallys=ctx.finallys + ([st.finalbody] if has_final else []),
        )
        body_frag = self._stmts(st.body, body_ctx)

        normal_exits = list(body_frag.exits)
        if st.orelse:
            ofrag = self._stmts(st.orelse, body_ctx)
            if ofrag.entry is not None:
                self._connect(normal_exits, ofrag.entry)
                normal_exits = ofrag.exits

        all_exits = normal_exits + handler_exits

        if has_final:
            fin_norm = self._copy_finally(st.finalbody, "normal", ctx)
            if fin_norm.entry is not None:
                self._connect(all_exits, fin_norm.entry)
                all_exits = fin_norm.exits

        entry = body_frag.entry if body_frag.entry is not None else first_handler
        return _Frag(entry, all_exits)

    _st_TryStar = _st_Try

    # -- with -------------------------------------------------------------

    def _st_With(self, st, ctx: _Ctx) -> _Frag:
        enter_ids: list[int] = []
        suppressing = False
        for item in st.items:
            eid = self._new("enter_cm", item.context_expr, label="ENTER(cm)")
            enter_ids.append(eid)
            self._link_exc(eid, ctx, item.context_expr)
            if _is_suppress(item.context_expr):
                suppressing = True
        after = self._new("exit_cm", None, label="EXIT(cm)")
        sub = ctx.child(suppress_targets=ctx.suppress_targets + ([after] if suppressing else []))
        body_frag = self._stmts(st.body, sub)
        prev = enter_ids[0]
        for nid in enter_ids[1:]:
            self.cfg.add_edge(prev, nid)
            prev = nid
        if body_frag.entry is not None:
            self.cfg.add_edge(prev, body_frag.entry)
            self._connect(body_frag.exits, after)
        else:
            self.cfg.add_edge(prev, after)
        return _Frag(enter_ids[0], [(after, "seq")])

    _st_AsyncWith = _st_With

    # -- match ------------------------------------------------------------

    def _st_Match(self, st, ctx: _Ctx) -> _Frag:
        """`match` は `if` 連鎖へ脱糖する。"""
        subject = self._new("stmt", st, label="match-subject")
        self._link_exc(subject, ctx, st)
        exits: list[Exit] = []
        prev_false: Optional[int] = None
        for case in st.cases:
            tid = self._new("test", case.pattern, label="case", test_expr=case.pattern)
            if prev_false is None:
                self.cfg.add_edge(subject, tid)
            else:
                self.cfg.add_edge(prev_false, tid, "false")
            frag = self._stmts(case.body, ctx)
            if frag.entry is not None:
                self.cfg.add_edge(tid, frag.entry, "true")
                exits += frag.exits
            else:
                exits.append((tid, "true"))
            prev_false = tid
        if prev_false is not None:
            exits.append((prev_false, "false"))
        else:
            exits.append((subject, "seq"))
        return _Frag(subject, exits)

    # -- 内包表記 ----------------------------------------------------------

    def _attach_comprehensions(self, nid: int, st: ast.AST) -> None:
        """内包表記 / genexp を合成した無名関数として別 CFG にする。

        `GeneratorExp` は即時消費される場合のみ合流し、変数束縛されて関数外へ
        渡る場合は ``OPAQUE(lazy_genexp)``。
        """
        for node in ast.walk(st):
            if isinstance(node, (ast.ListComp, ast.SetComp, ast.DictComp)):
                self.cfg.nodes[nid].subgraph = build_comprehension_cfg(node)
            elif isinstance(node, ast.GeneratorExp):
                if isinstance(st, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
                    if "lazy_genexp" not in self.cfg.opaque:
                        self.cfg.opaque.append("lazy_genexp")
                else:
                    self.cfg.nodes[nid].subgraph = build_comprehension_cfg(node)


# --------------------------------------------------------------------------
# test 式の脱糖
# --------------------------------------------------------------------------


@dataclass
class _TestFrag:
    entry: int
    #: 真辺 / 偽辺の宛先が未定のときの保留出口。**`and` / `or` の連鎖では
    #: 片側に複数のノードが保留されるので列で持つ。**
    true_pending: list[Exit] = field(default_factory=list)
    false_pending: list[Exit] = field(default_factory=list)


class _TestBuilder:
    """`A and B` / `A or B` / `IfExp` / `NamedExpr` を分岐へ開く。

    **極性はここで一度だけ扱う。** `not` は真偽の宛先を入れ替えるだけで、
    ノード自身の辺ラベルは常にそのノードの式から見た真偽である。
    """

    def __init__(self, b: CFGBuilder, ctx: _Ctx) -> None:
        self.b = b
        self.ctx = ctx

    def build(self, test, t: Optional[int], f: Optional[int]) -> _TestFrag:
        pt: list[Exit] = []
        pf: list[Exit] = []
        entry = self._emit(test, t, f, pt, pf)
        return _TestFrag(entry, pt, pf)

    def _leaf(self, e, t: Optional[int], f: Optional[int], pt: list, pf: list) -> int:
        nid = self.b._new("test", e, test_expr=e)
        self.b._attach_comprehensions(nid, e)
        self.b._link_exc(nid, self.ctx, e)
        if t is not None:
            self.b.cfg.add_edge(nid, t, "true")
        else:
            pt.append((nid, "true"))
        if f is not None:
            self.b.cfg.add_edge(nid, f, "false")
        else:
            pf.append((nid, "false"))
        return nid

    def _emit(self, e, t: Optional[int], f: Optional[int], pt: list, pf: list) -> int:
        if isinstance(e, ast.BoolOp) and isinstance(e.op, ast.And):
            # A and B: A が偽なら短絡して偽側へ。A が真なら B を評価する。
            target_true = t
            entry: Optional[int] = None
            for expr in reversed(list(e.values)):
                entry = self._emit(expr, target_true, f, pt, pf)
                target_true = entry
            assert entry is not None
            return entry
        if isinstance(e, ast.BoolOp) and isinstance(e.op, ast.Or):
            # A or B: A が真なら短絡して真側へ。A が偽なら B を評価する。
            target_false = f
            entry = None
            for expr in reversed(list(e.values)):
                entry = self._emit(expr, t, target_false, pt, pf)
                target_false = entry
            assert entry is not None
            return entry
        if isinstance(e, ast.UnaryOp) and isinstance(e.op, ast.Not):
            return self._emit(e.operand, f, t, pf, pt)
        if isinstance(e, ast.IfExp):
            c_entry = self._emit(e.body, t, f, pt, pf)
            e_entry = self._emit(e.orelse, t, f, pt, pf)
            return self._emit(e.test, c_entry, e_entry, [], [])
        if isinstance(e, ast.NamedExpr):
            # walrus: 代入は値の流れの話。分岐としては値そのものを test にする。
            return self._emit(e.value, t, f, pt, pf)
        return self._leaf(e, t, f, pt, pf)


# --------------------------------------------------------------------------
# 補助
# --------------------------------------------------------------------------


def _cannot_raise(node: ast.AST) -> bool:
    """保守側の判定: `Constant` のみの代入以外はすべて送出しうる（§2.5.1）。"""
    if isinstance(node, (ast.Pass, ast.Break, ast.Continue, ast.Global, ast.Nonlocal)):
        return True
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
        return all(isinstance(t, ast.Name) for t in node.targets)
    if isinstance(node, ast.AnnAssign) and (node.value is None or isinstance(node.value, ast.Constant)):
        return isinstance(node.target, ast.Name)
    if isinstance(node, ast.Constant):
        return True
    return False


def _is_suppress(expr: ast.AST) -> bool:
    """`contextlib.suppress(...)` か。"""
    if isinstance(expr, ast.Call):
        f = expr.func
        if isinstance(f, ast.Attribute) and f.attr == "suppress":
            return True
        if isinstance(f, ast.Name) and f.id == "suppress":
            return True
    return False


def build_comprehension_cfg(node: ast.AST) -> CFG:
    """内包表記を合成した無名関数として別 CFG にする。

    各 `comprehension` の `ifs` は test ノードになり、要素式をゲートする。
    G7（内包表記の `if` フィルタ）がこれを要求する。
    """
    fake = ast.FunctionDef(
        name="<comprehension>",
        args=ast.arguments(posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]),
        body=[],
        decorator_list=[],
        lineno=getattr(node, "lineno", 1),
        col_offset=getattr(node, "col_offset", 0),
    )
    b = CFGBuilder(fake)
    ctx = _Ctx()
    entry: Optional[int] = None
    pending: list[Exit] = []
    for gen in getattr(node, "generators", []):
        iter_id = b._new("loop_header", gen.iter, label="comp-iter")
        if entry is None:
            entry = iter_id
        b._connect(pending, iter_id)
        pending = [(iter_id, "true")]
        for cond in gen.ifs:
            tf = _TestBuilder(b, ctx).build(cond, None, b.exit)
            b._connect(pending, tf.entry)
            pending = tf.true_pending
    elt = getattr(node, "elt", None) or getattr(node, "value", None)
    elt_id = b._new("stmt", elt, label="comp-elt")
    if entry is None:
        entry = elt_id
    b._connect(pending, elt_id)
    b.cfg.add_edge(elt_id, b.exit)
    b.cfg.add_edge(b.entry, entry)
    return b.cfg


def build_cfg(func: ast.AST) -> CFG:
    """関数 AST から CFG を組む。"""
    return CFGBuilder(func).build()
