"""§2.6: val エンジン。標準ライブラリ `ast` のみ。venv も型環境も使わない。

守る規則（仕様書が名指しで禁じているもの）:

* **`ast.walk` は使わない。** BFS で文順を保証せず def-use に使えない
  （前身の `reaches_sink` / `_last_assign_rhs` がこれを使っており流用できない
  直接の理由）。ここは文順の前向き走査で書く。
* **val は等級を付けない。** `tokenised` / `quoted` / `canonicalised` / `joined` /
  `encoded` / `alias_mismatch` は属性として、正規化別名は `alias_facts` として
  記録するだけ。strong / weak の判定は Def 5 のゲート採点器が単独で行う。
* **`dash_rejected` のような制御述語由来の事実は val の出力に含めない**
  （val は `ast.If` を値の合流にしか使わず支配判定を持たないので原理的に
  生成できない）。
* **opaque を drop しない。clean に潰さない。MODEL に切り上げない。**
* heap のキーは受け手アクセスパス（`self._session` のような深さ 2 まで）。
  読みと書きで同一のキー体系を使う。それ以上は `opaque(receiver)`。
* ループは 2 周固定点 + widening。`K = 16` は 5 種すべて
  （`Seq.elems` / `Map.entries` / `Str.parts` / `Argv.elems` / `Path.segs`）に適用する。

反証条件（§2.6）: 較正 3 対と負例集合の実行で 2 周目と 3 周目の env が
バイト一致しないユニットが 1 件でも出たら 3 周に上げるか当該ループ本体を
`opaque(loop)` に落とす。**3 周目を回して比較するデバッグ フラグを最初から
入れる**（:attr:`Options.loop_probe`）。
"""

from __future__ import annotations

import ast
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Optional

from ..catalog.transfers import (
    ATTR_TYPE_TRANSITIONS,
    CTOR_BY_NAME,
    INDIRECT_BY_NAME,
    method_transfer_for,
    transfer_for,
)
from ..ir import (
    MAX_DEPTH,
    RESOLVED,
    SUMMARY_CAP,
    Argv,
    Atom,
    K,
    Map,
    Obj,
    Path,
    Prin,
    Prov,
    Seq,
    Str,
    Unknown,
    Value,
    opaque,
    prov_merge,
    value_join,
)
from ..srcindex import FuncDef, Scope, SourceIndex, dotted_of, resolve_call_name

#: 受け手アクセスパスの最大深さ（§2.6）。
RECEIVER_DEPTH = 2


# --------------------------------------------------------------------------
# alias 表
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class AliasFact:
    """canonical-alias 表の 1 行 `(root, site, transform)`（§2.6）。

    **この表が Def 5 strong-path の前提である。**
    """

    root: str
    site: str
    transform: str

    def to_json(self) -> dict:
        return {"root": self.root, "site": self.site, "transform": self.transform}


# --------------------------------------------------------------------------
# 環境
# --------------------------------------------------------------------------


class Env:
    """変数と受け手アクセスパスから値への表。

    キーは `"name"` または `"self._session"` のようなアクセスパス。
    **読みと書きで同一のキー体系を使う。**
    """

    def __init__(self, data: Optional[dict[str, Value]] = None) -> None:
        self._d: dict[str, Value] = dict(data or {})

    def get(self, key: str) -> Optional[Value]:
        return self._d.get(key)

    def set(self, key: str, value: Value) -> None:
        self._d[key] = value

    def copy(self) -> Env:
        return Env(self._d)

    def keys(self) -> list[str]:
        return sorted(self._d)

    def items(self):
        for k in sorted(self._d):
            yield k, self._d[k]

    def __contains__(self, key: str) -> bool:
        return key in self._d

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Env) and self._d == other._d

    def signature(self) -> str:
        """2 周目と 3 周目の比較に使う正規化表現（バイト一致で比べる）。"""
        import json

        return json.dumps(
            {k: v.to_json() for k, v in self.items()}, sort_keys=True, ensure_ascii=False
        )


def env_join(a: Env, b: Env) -> Env:
    """分岐の合流。片方にしか無いキーは `Unknown` と join する（消さない）。"""
    out = Env()
    for key in sorted(set(a.keys()) | set(b.keys())):
        va, vb = a.get(key), b.get(key)
        if va is None:
            out.set(key, vb if vb is not None else Value())
        elif vb is None:
            out.set(key, va)
        else:
            out.set(key, value_join(va, vb))
    return out


# --------------------------------------------------------------------------
# 走査の設定と結果
# --------------------------------------------------------------------------


@dataclass
class Options:
    max_depth: int = MAX_DEPTH
    k: int = K
    summary_cap: int = SUMMARY_CAP
    #: 反証条件用。真にするとループを 3 周回して 2 周目との env 一致を確かめる。
    loop_probe: bool = False


@dataclass
class CallEvent:
    """呼び出し 1 つ。sink 照合は `effects` 側が行う（責務分離）。"""

    node: ast.Call
    dotted: Optional[str]
    receiver: Optional[Value]
    receiver_path: Optional[str]
    args: list[Value]
    kwargs: dict[str, Value]
    lineno: int
    relpath: str
    depth: int
    #: 入口からこの呼び出しまでの経路（witness_chain）。
    chain: tuple[str, ...]
    #: **入口ユニットの CFG 上でこの効果に対応する行。**
    #: 手続き間で見つけた効果を入口の支配判定に載せるために要る（§2.5.4 の連結経路）。
    #: 深さ 0 の呼び出しでは自分自身の行。
    entry_site: int = 0
    #: 受け手型が分からず**末尾名だけで**降りた経路の上の呼び出しか（D17）。
    #: 効果は出すが確度に `opaque(unresolved)` を合流する。**末尾に置く**（位置引数で
    #: 作る箇所の順序を崩さない）。
    by_name: bool = False


@dataclass
class ValResult:
    """1 ユニットの解析結果。"""

    #: 呼び出し事象の列（sink 照合は effects 側）。
    calls: list[CallEvent] = field(default_factory=list)
    #: canonical-alias 表。
    alias_facts: list[AliasFact] = field(default_factory=list)
    #: 立った opaque 理由（val 側語彙）。
    opaque_reasons: list[str] = field(default_factory=list)
    #: 到達した cap（`cap` / `depth` / `summary_cap`）。
    cap_hits: list[str] = field(default_factory=list)
    #: `loop_probe` を有効にしたときの、2 周目と 3 周目が一致しなかった箇所。
    loop_unstable: list[str] = field(default_factory=list)
    #: 最終 env（デバッグと手検証用）。
    env: Optional[Env] = None

    def note_opaque(self, reason: str) -> None:
        if reason not in self.opaque_reasons:
            self.opaque_reasons.append(reason)


# --------------------------------------------------------------------------
# エンジン
# --------------------------------------------------------------------------


class ValEngine:
    """文順の前向き走査で値を伝播し、呼び出し事象を集める。"""

    def __init__(
        self,
        index: SourceIndex,
        options: Optional[Options] = None,
        on_call: Optional[Callable[[CallEvent], None]] = None,
    ) -> None:
        self.index = index
        self.opt = options or Options()
        self.on_call = on_call
        self._summaries: dict[str, int] = {}
        self._active: set[str] = set()
        #: 深さ 0 の呼び出し位置のスタック（入口 CFG 上の行）。
        self._entry_sites: list[int] = []
        #: モジュール水準の束縛の記憶化 `(module, name) -> Value | None`（D17）。
        self._module_values: dict[tuple[str, str], Optional[Value]] = {}
        self._module_active: set[tuple[str, str]] = set()
        #: いま末尾名だけで降りた経路の中にいるか（入れ子の深さ）。
        self._by_name_depth = 0
        #: 受け手が 2 型以上の `Obj` で、各型に候補メソッドが 1 つずつあるとき真（D35）。
        #: 呼び出し側は候補ごとに受け手をその 1 型に絞って降り、行を witness で分ける（F7）。
        self._split_receiver = False
        self._class_defaults_active: set[tuple[str, str]] = set()
        #: いま実行中のメソッドの `(クラス名, モジュール)`。`super().m()` の解決に使う（D35 改訂）。
        self._class_stack: list[tuple[Optional[str], Optional[str]]] = []
        #: 直前の `_resolve_in_tree` が末尾名だけで決めたか（見える同名の定義が決まらないときも立つ）。
        self._by_name_hint = False
        #: 直前の `_resolve_in_tree` が、見える同名の定義のどれが効くかを決められなかったか（D17 改訂 5）。
        self._pinned_ambiguous = False

    # -- 入口 -------------------------------------------------------------

    def analyze(self, fn: ast.AST, scope: Scope, seed: dict[str, Value]) -> ValResult:
        """ユニット入口から下向きに走る。`seed` は仮引数の初期値（R2 の MODEL）。"""
        res = ValResult()
        env = Env(seed)
        me = seed.get("self")
        cls = me.shape.classes[0] if me is not None and isinstance(me.shape, Obj) and me.shape.classes else None
        self._class_stack.append((cls, scope.module))
        try:
            self._exec_body(getattr(fn, "body", []), env, scope, res, depth=0, chain=())
        finally:
            self._class_stack.pop()
        res.env = env
        return res

    # -- 文 ---------------------------------------------------------------

    def _exec_body(
        self,
        body: list,
        env: Env,
        scope: Scope,
        res: ValResult,
        depth: int,
        chain: tuple[str, ...],
    ) -> None:
        """**文順の前向き走査。`ast.walk` を使わない。**"""
        for st in body:
            self._exec_stmt(st, env, scope, res, depth, chain)

    def _exec_stmt(
        self, st, env: Env, scope: Scope, res: ValResult, depth: int, chain: tuple[str, ...]
    ) -> None:
        if isinstance(st, ast.Assign):
            value = self._eval(st.value, env, scope, res, depth, chain)
            for t in st.targets:
                self._bind(t, value, env, scope, res, depth, chain)
        elif isinstance(st, ast.AnnAssign):
            if st.value is not None:
                value = self._eval(st.value, env, scope, res, depth, chain)
                self._bind(st.target, value, env, scope, res, depth, chain)
        elif isinstance(st, ast.AugAssign):
            cur = self._eval(st.target, env, scope, res, depth, chain)
            add = self._eval(st.value, env, scope, res, depth, chain)
            self._bind(st.target, self._concat(cur, add), env, scope, res, depth, chain)
        elif isinstance(st, ast.Expr):
            self._eval(st.value, env, scope, res, depth, chain)
        elif isinstance(st, ast.Return):
            if st.value is not None:
                value = self._eval(st.value, env, scope, res, depth, chain)
                prev = env.get("<return>")
                env.set("<return>", value if prev is None else value_join(prev, value))
        elif isinstance(st, ast.If):
            self._eval(st.test, env, scope, res, depth, chain)
            a, b = env.copy(), env.copy()
            self._exec_body(st.body, a, scope, res, depth, chain)
            self._exec_body(st.orelse, b, scope, res, depth, chain)
            merged = env_join(a, b)
            for k, v in merged.items():
                env.set(k, v)
        elif isinstance(st, (ast.For, ast.AsyncFor)):
            self._exec_loop(st, env, scope, res, depth, chain, iter_target=True)
        elif isinstance(st, ast.While):
            self._exec_loop(st, env, scope, res, depth, chain, iter_target=False)
        elif isinstance(st, (ast.With, ast.AsyncWith)):
            for item in st.items:
                value = self._eval(item.context_expr, env, scope, res, depth, chain)
                if item.optional_vars is not None:
                    self._bind(item.optional_vars, value, env, scope, res, depth, chain)
            self._exec_body(st.body, env, scope, res, depth, chain)
        elif isinstance(st, (ast.Try, getattr(ast, "TryStar", ast.Try))):
            before = env.copy()
            self._exec_body(st.body, env, scope, res, depth, chain)
            merged = env
            for h in st.handlers:
                he = before.copy()
                self._exec_body(h.body, he, scope, res, depth, chain)
                merged = env_join(merged, he)
            self._exec_body(getattr(st, "orelse", []), merged, scope, res, depth, chain)
            self._exec_body(getattr(st, "finalbody", []), merged, scope, res, depth, chain)
            for k, v in merged.items():
                env.set(k, v)
        elif isinstance(st, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return  # 入れ子定義は別ユニット。ここでは降りない
        elif isinstance(st, ast.Raise):
            if st.exc is not None:
                self._eval(st.exc, env, scope, res, depth, chain)
        elif isinstance(st, (ast.Import, ast.ImportFrom, ast.Pass, ast.Break, ast.Continue,
                             ast.Global, ast.Nonlocal, ast.Delete)):
            return
        elif isinstance(st, ast.Assert):
            self._eval(st.test, env, scope, res, depth, chain)
        elif _MATCH is not None and isinstance(st, _MATCH):
            self._eval(st.subject, env, scope, res, depth, chain)
            merged = env.copy()
            for case in st.cases:
                ce = env.copy()
                self._exec_body(case.body, ce, scope, res, depth, chain)
                merged = env_join(merged, ce)
            for k, v in merged.items():
                env.set(k, v)
        else:
            res.note_opaque("dynamic")

    def _exec_loop(
        self,
        st,
        env: Env,
        scope: Scope,
        res: ValResult,
        depth: int,
        chain: tuple[str, ...],
        iter_target: bool,
    ) -> None:
        """ループは **2 周固定点 + widening**（§2.6）。"""
        if iter_target:
            seq = self._eval(st.iter, env, scope, res, depth, chain)
            self._bind(st.target, _element_of(seq), env, scope, res, depth, chain)
        else:
            self._eval(st.test, env, scope, res, depth, chain)

        first = env.copy()
        self._exec_body(st.body, first, scope, res, depth, chain)
        second = env_join(env, first)
        self._exec_body(st.body, second, scope, res, depth, chain)
        second = _widen(env_join(env, second), self.opt.k)

        if self.opt.loop_probe:
            third = second.copy()
            self._exec_body(st.body, third, scope, res, depth, chain)
            third = _widen(env_join(second, third), self.opt.k)
            if third.signature() != second.signature():
                res.loop_unstable.append(f"L{getattr(st, 'lineno', 0)}")
                res.note_opaque("loop")

        for k, v in second.items():
            env.set(k, v)
        self._exec_body(getattr(st, "orelse", []), env, scope, res, depth, chain)

    # -- 束縛 -------------------------------------------------------------

    def _bind(
        self, target, value: Value, env: Env, scope: Scope, res: ValResult, depth: int, chain
    ) -> None:
        if isinstance(target, ast.Name):
            env.set(target.id, value)
        elif isinstance(target, ast.Attribute):
            path = access_path(target)
            if path is None:
                res.note_opaque("receiver")
                return
            env.set(path, value)
        elif isinstance(target, (ast.Tuple, ast.List)):
            elems = _elements(value)
            for i, t in enumerate(target.elts):
                if isinstance(t, ast.Starred):
                    self._bind(t.value, value, env, scope, res, depth, chain)
                elif i < len(elems):
                    self._bind(t, elems[i], env, scope, res, depth, chain)
                else:
                    self._bind(t, _element_of(value), env, scope, res, depth, chain)
        elif isinstance(target, ast.Subscript):
            base = access_path(target.value) or (
                target.value.id if isinstance(target.value, ast.Name) else None
            )
            if base is None:
                res.note_opaque("dynamic")
                return
            cur = env.get(base)
            env.set(base, _append_tail(cur, value, self.opt.k))
        else:
            res.note_opaque("dynamic")

    # -- 式 ---------------------------------------------------------------

    def _eval(
        self, node, env: Env, scope: Scope, res: ValResult, depth: int, chain: tuple[str, ...]
    ) -> Value:
        if node is None:
            return Value()
        m = getattr(self, "_ev_" + type(node).__name__, None)
        if m is None:
            res.note_opaque("dynamic")
            return Value(Prin.OP, opaque("dynamic"), Unknown())
        return m(node, env, scope, res, depth, chain)

    # 定数・名前 ----------------------------------------------------------

    def _ev_Constant(self, node, env, scope, res, depth, chain) -> Value:
        return Value(Prin.OP, RESOLVED, Atom(const=node.value, none=node.value is None))

    def _ev_Name(self, node, env, scope, res, depth, chain) -> Value:
        v = env.get(node.id)
        if v is not None:
            return v
        # モジュール水準の束縛（定数・大域インスタンス・環境変数の読み出し）。
        # **木内で解決できる名前を opaque(unresolved) にしない**（Def 4、D17）。
        mv = self._module_value(scope, node.id, res)
        if mv is not None:
            return mv
        res.note_opaque("unresolved")
        return Value(Prin.OP, opaque("unresolved"), Atom(formal=node.id))

    def _ev_Attribute(self, node, env, scope, res, depth, chain) -> Value:
        if resolve_call_name(node, scope) == "os.environ":
            # 環境変数は config atom の源（§2.3）→ OP / resolved（D17）。**ただしこの関数で
            # 書き込んだ値は読み戻しに含め**、木内のどこかで非定数を書き込むなら config と
            # みなさない（D17 改訂 2。書き込みを無視すると MODEL が OP になる）。
            base = _environ_map(self._environ_written_in_tree())
            written = env.get("os.environ")
            return value_join(base, written) if written is not None else base
        path = access_path(node)
        if path is not None:
            v = env.get(path)
            if v is not None:
                return v
        base = self._eval(node.value, env, scope, res, depth, chain)
        if isinstance(base.shape, Obj):
            for name, val in base.shape.fields:
                if name == node.attr:
                    return val
            for cls in base.shape.classes:
                trans = ATTR_TYPE_TRANSITIONS.get((cls, node.attr))
                if trans is not None:
                    new_cls, carry = trans
                    fields = tuple(
                        (dst, val)
                        for dst, src in sorted(carry.items())
                        for name, val in base.shape.fields
                        if name == src
                    )
                    return Value(base.prin, base.prov, Obj((new_cls,), fields), base.attrs, base.roots)
        if path is None:
            res.note_opaque("receiver")
            return Value(base.prin, prov_merge(base.prov, opaque("receiver")), Unknown(), frozenset(), base.roots)
        return Value(base.prin, prov_merge(base.prov, opaque("unresolved")), Unknown(), frozenset(), base.roots)

    # 合成 ---------------------------------------------------------------

    def _ev_JoinedStr(self, node, env, scope, res, depth, chain) -> Value:
        parts: list[Value] = []
        for v in node.values:
            parts.append(self._eval(v, env, scope, res, depth, chain))
        return _make_str(parts, self.opt.k)

    def _ev_FormattedValue(self, node, env, scope, res, depth, chain) -> Value:
        return self._eval(node.value, env, scope, res, depth, chain)

    def _ev_BinOp(self, node, env, scope, res, depth, chain) -> Value:
        if isinstance(node.op, ast.Add) and isinstance(node.left, ast.BinOp) and isinstance(node.left.op, ast.Add):
            # 左結合の長い `a + b + c + ...` は**再帰せずに**畳む（D17 改訂 4）。1 項ごとに 2 フレーム
            # 積むと数百項で RecursionError になり、木 1 本の出力を全部落とした（3 回目のレビュー）。
            operands = []
            cur = node
            while isinstance(cur, ast.BinOp) and isinstance(cur.op, ast.Add):
                operands.append(cur.right)
                cur = cur.left
            operands.append(cur)
            operands.reverse()
            acc = self._eval(operands[0], env, scope, res, depth, chain)
            for operand in operands[1:]:
                acc = self._concat(acc, self._eval(operand, env, scope, res, depth, chain))
            return acc
        left = self._eval(node.left, env, scope, res, depth, chain)
        right = self._eval(node.right, env, scope, res, depth, chain)
        if isinstance(node.op, ast.Div) and isinstance(left.shape, Path):
            segs = tuple(list(left.shape.segs) + [right])[: self.opt.k]
            return Value(
                _prin2(left, right),
                prov_merge(left.prov, right.prov),
                Path(left.shape.base, segs, left.shape.tail),
                left.attrs & right.attrs,
                left.roots | right.roots,
            )
        if isinstance(node.op, ast.Add):
            return self._concat(left, right)
        if isinstance(node.op, ast.Mod):
            return self._concat(left, right)
        return Value(_prin2(left, right), prov_merge(left.prov, right.prov), Atom(), frozenset(), left.roots | right.roots)

    def _concat(self, a: Value, b: Value) -> Value:
        if isinstance(a.shape, (Seq, Argv)) and isinstance(b.shape, (Seq, Argv)):
            elems = tuple(list(a.shape.elems) + list(b.shape.elems))[: self.opt.k]
            tail = a.shape.tail or b.shape.tail
            cls = Argv if isinstance(a.shape, Argv) or isinstance(b.shape, Argv) else Seq
            return Value(
                _prin2(a, b), prov_merge(a.prov, b.prov), cls(elems, tail), a.attrs & b.attrs, a.roots | b.roots
            )
        return _make_str([a, b], self.opt.k)

    def _ev_List(self, node, env, scope, res, depth, chain) -> Value:
        elems = tuple(self._eval(e, env, scope, res, depth, chain) for e in node.elts)[: self.opt.k]
        return Value(_prin_all(elems), _prov_all(elems), Seq(elems), frozenset(), _roots_all(elems))

    _ev_Tuple = _ev_List
    _ev_Set = _ev_List

    def _ev_Dict(self, node, env, scope, res, depth, chain) -> Value:
        entries: list[tuple[str, Value]] = []
        for k, v in zip(node.keys, node.values, strict=False):
            key = k.value if isinstance(k, ast.Constant) and isinstance(k.value, str) else "<dynamic>"
            entries.append((key, self._eval(v, env, scope, res, depth, chain)))
        entries.sort(key=lambda kv: kv[0])
        vals = [v for _k, v in entries]
        return Value(_prin_all(vals), _prov_all(vals), Map(tuple(entries[: self.opt.k])), frozenset(), _roots_all(vals))

    def _ev_IfExp(self, node, env, scope, res, depth, chain) -> Value:
        self._eval(node.test, env, scope, res, depth, chain)
        a = self._eval(node.body, env, scope, res, depth, chain)
        b = self._eval(node.orelse, env, scope, res, depth, chain)
        return value_join(a, b)

    def _ev_BoolOp(self, node, env, scope, res, depth, chain) -> Value:
        vals = [self._eval(v, env, scope, res, depth, chain) for v in node.values]
        out = vals[0]
        for v in vals[1:]:
            out = value_join(out, v)
        return out

    def _ev_Compare(self, node, env, scope, res, depth, chain) -> Value:
        self._eval(node.left, env, scope, res, depth, chain)
        for c in node.comparators:
            self._eval(c, env, scope, res, depth, chain)
        return Value(Prin.OP, RESOLVED, Atom(const=None))

    def _ev_UnaryOp(self, node, env, scope, res, depth, chain) -> Value:
        return self._eval(node.operand, env, scope, res, depth, chain)

    def _ev_NamedExpr(self, node, env, scope, res, depth, chain) -> Value:
        value = self._eval(node.value, env, scope, res, depth, chain)
        self._bind(node.target, value, env, scope, res, depth, chain)
        return value

    def _ev_Starred(self, node, env, scope, res, depth, chain) -> Value:
        return self._eval(node.value, env, scope, res, depth, chain)

    def _ev_Await(self, node, env, scope, res, depth, chain) -> Value:
        return self._eval(node.value, env, scope, res, depth, chain)

    def _ev_Subscript(self, node, env, scope, res, depth, chain) -> Value:
        base = self._eval(node.value, env, scope, res, depth, chain)
        idx = node.slice
        if isinstance(base.shape, Map) and isinstance(idx, ast.Constant) and isinstance(idx.value, str):
            for k, v in base.shape.entries:
                if k == idx.value:
                    return _refine_roots(v, base.roots, idx.value)
        if isinstance(base.shape, (Seq, Argv)) and isinstance(idx, ast.Constant) and isinstance(idx.value, int):
            if 0 <= idx.value < len(base.shape.elems):
                return base.shape.elems[idx.value]
        out = _element_of(base)
        if isinstance(idx, ast.Constant) and isinstance(idx.value, str):
            # **定数キーの添字は root を精緻化する。**
            # `arguments["repo_path"]` と `arguments["target"]` を同じ root に
            # まとめると、片方への検証がもう片方の位置に付いてしまう
            # （Def 5 が禁じている型エラーが主語一致をすり抜ける）。
            out = _refine_roots(out, base.roots, idx.value)
        return out

    def _ev_ListComp(self, node, env, scope, res, depth, chain) -> Value:
        for gen in node.generators:
            seq = self._eval(gen.iter, env, scope, res, depth, chain)
            self._bind(gen.target, _element_of(seq), env, scope, res, depth, chain)
            for cond in gen.ifs:
                self._eval(cond, env, scope, res, depth, chain)
        elt = self._eval(node.elt, env, scope, res, depth, chain)
        return Value(elt.prin, elt.prov, Seq((), elt), frozenset(), elt.roots)

    _ev_SetComp = _ev_ListComp

    def _ev_GeneratorExp(self, node, env, scope, res, depth, chain) -> Value:
        return self._ev_ListComp(node, env, scope, res, depth, chain)

    def _ev_DictComp(self, node, env, scope, res, depth, chain) -> Value:
        for gen in node.generators:
            seq = self._eval(gen.iter, env, scope, res, depth, chain)
            self._bind(gen.target, _element_of(seq), env, scope, res, depth, chain)
        val = self._eval(node.value, env, scope, res, depth, chain)
        return Value(val.prin, val.prov, Map((), val), frozenset(), val.roots)

    def _ev_Lambda(self, node, env, scope, res, depth, chain) -> Value:
        res.note_opaque("dynamic")
        return Value(Prin.OP, opaque("dynamic"), Unknown())

    # 呼び出し ------------------------------------------------------------

    def _ev_Call(self, node, env, scope, res, depth, chain) -> Value:
        args = [self._eval(a, env, scope, res, depth, chain) for a in node.args]
        kwargs: dict[str, Value] = {}
        for kw in node.keywords:
            if kw.arg is not None:
                kwargs[kw.arg] = self._eval(kw.value, env, scope, res, depth, chain)
        receiver: Optional[Value] = None
        receiver_path: Optional[str] = None
        if isinstance(node.func, ast.Attribute):
            receiver = self._eval(node.func.value, env, scope, res, depth, chain)
            receiver_path = access_path(node.func.value)
        dotted = resolve_call_name(node.func, scope)

        event = CallEvent(
            node=node,
            dotted=dotted,
            receiver=receiver,
            receiver_path=receiver_path,
            args=args,
            kwargs=kwargs,
            lineno=getattr(node, "lineno", 0),
            relpath=scope.relpath,
            depth=depth,
            chain=chain,
            entry_site=self._entry_sites[-1] if self._entry_sites else getattr(node, "lineno", 0),
            by_name=self._by_name_depth > 0,
        )
        if self.on_call is not None:
            self.on_call(event)

        # (0) 組込みの値操作: 環境変数の読み出し、`sep.join(xs)`、コンテナへの書き込み（D17）
        value = self._builtin_value_op(node, dotted, receiver, receiver_path, args, kwargs, env)
        if value is not None:
            return value

        # (1) TRANSFER 表（深さを消費しない）
        value = self._apply_transfer(node, dotted, receiver, args, kwargs, res, scope)
        if value is not None:
            return value

        # (2) ライブラリ コンストラクタ カタログ
        if dotted in CTOR_BY_NAME:
            return _build_obj(CTOR_BY_NAME[dotted], args, kwargs)

        # (3) INDIRECT 表（**1 段として数える**）
        if dotted in INDIRECT_BY_NAME:
            return self._descend_indirect(node, dotted, args, kwargs, env, scope, res, depth, chain)

        # (3b) `super().m(...)`: いま実行中のメソッドのクラスの基底から `m` を引く（D35 改訂）。
        # 解決できないと `super().__init__(cmd)` の MODEL の書き込みが見えず、クラス体の既定値が
        # それを覆い隠す（レビュー b2、false-clean）。
        sup = self._super_callees(node)
        if sup is not None:
            callees, _ = sup
            me = env.get("self")
            if callees and me is not None and isinstance(me.shape, Obj):
                ret: Optional[Value] = None
                for callee in callees:
                    v, sub = self._descend_env(callee, node, args, kwargs, me, res, depth, chain)
                    if sub is not None and me is not None:
                        self._write_back_self("self", me, sub, env)
                    ret = v if ret is None else value_join(ret, v)
                return ret if ret is not None else Value(Prin.OP, RESOLVED, Unknown())

        # (4) 木内のユーザ定義関数（深さを消費する）
        if receiver is not None and receiver_path is not None and isinstance(receiver.shape, Obj):
            # 呼び出し側が `<path>.<f> = v` と書いた値を受け手の `Obj.fields` に載せてから降りる
            # （D35 改訂）。env の鍵と `Obj.fields` は別の記憶なので、載せないと被呼び出しの
            # `self.<f>` が古い既定値を読む（レビュー b1 / c2、false-clean）。
            receiver = self._receiver_with_path_writes(receiver, receiver_path, env)
        callees = self._resolve_in_tree(node, dotted, receiver, scope)
        if callees:
            by_name = self._by_name_hint
            ambiguous = self._pinned_ambiguous
            if by_name:
                res.note_opaque("unresolved")
            # 見える同名の定義のどれが効くか決まらないときは**全候補へ降りて戻り値を join する**
            # （D17 改訂 5）。1 つを選ぶと他方の効果行が消え、降りなければ全部消える。
            split = self._split_receiver
            ret: Optional[Value] = None
            for callee in callees:
                recv_i = receiver
                if split and callee.classname is not None and receiver is not None and isinstance(receiver.shape, Obj):
                    # 2 型受け手を候補の型に絞って降りる（F7: `LocalFileOperator` / `SandboxFileOperator`
                    # の `write_file` を別行にする）。fields は合流後のもの（両型で共通の名前だけ残る）。
                    recv_i = Value(
                        receiver.prin, receiver.prov, Obj((callee.classname,), receiver.shape.fields),
                        receiver.attrs, receiver.roots,
                    )
                v, sub = self._descend_env(
                    callee, node, args, kwargs, recv_i, res, depth, chain, by_name=by_name
                )
                if sub is not None and not by_name and receiver_path is not None and receiver is not None:
                    # 被呼び出しが `self.<f>` に書いた値を呼び出し側の受け手アクセスパスへ戻す（D35）。
                    # `_BashSession.start` が `self._process` に書き、`run` が読む（F6）。
                    # **受け手型で裏付けられた解決に限る**（by_name の書き戻しは別クラスの
                    # フィールドを付ける恐れがある）。分割降下でも**絞る前の受け手**を基にする
                    # （絞った型で書き戻すと 2 型目以降の経路が消える。レビュー d8）。
                    self._write_back_self(receiver_path, receiver, sub, env)
                ret = v if ret is None else value_join(ret, v)
            return _opaque_deep(ret) if ambiguous else ret

        # (5) 木内クラスの構築 `C(...)`（`__init__` を実行するので深さを消費する）
        built = self._construct_in_tree(node, dotted, args, kwargs, scope, res, depth, chain)
        if built is not None:
            return built

        res.note_opaque("unresolved")
        return Value(
            Prin.OP,
            opaque("unresolved"),
            Unknown(),
            frozenset(),
            frozenset().union(*[a.roots for a in args]) if args else frozenset(),
        )

    def _apply_transfer(self, node, dotted, receiver, args, kwargs, res, scope) -> Optional[Value]:
        row = transfer_for(dotted) if dotted else None
        if row is None and isinstance(node.func, ast.Attribute):
            row = method_transfer_for(node.func.attr)
            if row is not None and self._in_tree_method(receiver, node.func.attr):
                # 受け手が木内クラスで、そのクラス（または基底）が同名メソッドを定義するなら
                # TRANSFER ではなく木内の解決に回す（`Codec.encode` の中の sink が消える。
                # レビュー e1 / e3、false-clean）。
                row = None
            if row is not None and row.subject != "receiver":
                row = None
        if row is None:
            return None
        subject = receiver if row.subject == "receiver" else (args[0] if args else Value())
        # **subject 以外の実引数も結果の主体・確度・root に入れる**（D17 改訂 3）。捨てると
        # `"ls {d}".format(d=d)` / `os.path.join("/data", name)` / `urljoin(base, url)` の MODEL が
        # OP / resolved になる（`"ls " + d` と違う結果になる。false-clean）。
        rest_args = list(args) if row.subject == "receiver" else list(args[1:])
        others = rest_args + [kwargs[k] for k in sorted(kwargs)]
        prin, prov, roots = subject.prin, subject.prov, subject.roots
        for v in others:
            if v.prin > prin:
                prin = v.prin
            prov = prov_merge(prov, v.prov)
            roots = roots | v.roots
        shape = subject.shape
        if row.shape == "path":
            shape = Path(base=subject) if not isinstance(subject.shape, Path) else subject.shape
        elif row.shape == "str":
            # 非リテラルの実引数が混ざる文字列は形を捨てる。テンプレートのリテラルを URL の host
            # として切り出させない（`"https://{}/x".format(host)`、`urljoin(base, url)`）。
            if all(v.is_literal() for v in others):
                shape = Str((subject,))
            elif row.transform == "str.format" and isinstance(subject.const, str) and "{" in subject.const:
                # テンプレートの**最初のプレースホルダより前のリテラルは保つ**（D17 改訂 4）。
                # `"https://api.github.com/repos/{}".format(a)` の host を f 文字列と同じく切り出せる
                # ように。残りは実引数の主体・確度を持つ 1 つの part（3 回目のレビュー、精度の損失）。
                head = subject.const[: subject.const.index("{")]
                tail_part = Value(prin, prov, Unknown(), frozenset(), roots)
                head_part = (Value(Prin.OP, RESOLVED, Atom(const=head)),) if head else ()
                shape = Str(head_part + (tail_part,))
            else:
                shape = Atom()
        elif row.shape == "seq":
            shape = Seq((), subject)
        elif row.shape == "atom":
            shape = Atom()
        out = Value(prin, prov, shape, subject.attrs | frozenset(row.attrs), roots)
        for root in sorted(subject.roots):
            res.alias_facts.append(AliasFact(root, f"{scope.relpath}:L{getattr(node, 'lineno', 0)}", row.transform))
        return out

    def _resolve_in_tree(
        self, node, dotted: Optional[str], receiver: Optional[Value], scope: Optional[Scope] = None
    ) -> list[FuncDef]:
        """木内のユーザ定義関数へ解決する。**同名メソッドを無条件に採らない。** 解決できなければ空。

        複数の候補を返すのは、呼び出し位置から見える同名の定義のどれが効くか決まらないときだけ
        （D17 改訂 5）。そのとき（と、1 候補でも import / 代入の束縛と競合するとき）は
        `_pinned_ambiguous` を立てる。呼び出し側は全候補へ降り、行（`_by_name_hint`）と戻り値を opaque にする。
        """
        self._by_name_hint = False
        self._pinned_ambiguous = False
        self._split_receiver = False
        name = dotted_of(node.func)
        if name is None:
            return []
        last = name.split(".")[-1]
        # **import 表で指したモジュール / 同じモジュールの定義を先に引く**（D17 改訂 3）。
        pinned = self._pinned_candidates(node, dotted, last, scope)
        if pinned is not None:
            pinned_cands, ambiguous = pinned
            self._by_name_hint = self._pinned_ambiguous = ambiguous
            return pinned_cands
        cands = self.index.lookup_function(last)
        if not cands:
            return []
        typed_classes: set[str] = set()
        if receiver is not None and isinstance(receiver.shape, Obj) and receiver.shape.classes:
            typed_classes = {c.split(".")[-1] for c in receiver.shape.classes}
            narrowed = [c for c in cands if c.classname in typed_classes]
            if narrowed:
                cands = narrowed
        want_method = isinstance(node.func, ast.Attribute)
        narrowed = [c for c in cands if (c.classname is not None) == want_method]
        if narrowed:
            cands = narrowed
        if len(cands) > 1 and want_method and len(typed_classes) > 1:
            # 受け手が 2 型以上の `Obj`（IfExp / 分岐の合流）で、候補が**その各型に 1 つずつ**
            # あるなら全候補へ降りる（D35、F7 の「2 型受け手は witness の分岐として分ける」）。
            # 型で裏付けられた解決なので by_name にはしない。型に無い候補が混じるときは従来どおり。
            by_class = {c.classname: c for c in cands}
            # **受け手の全型に候補が要る**（`<=` だと候補の無い型（外部基底の `run` など）の経路が
            # 無言で落ち、opaque(unresolved) だったものが resolved になる。レビュー d17）。
            # **同名クラスが木に 2 つ以上あるときは分割しない**（`Obj.classes` は末尾名なので
            # 別モジュールの同名クラスのメソッドへ降りうる。レビュー d4）。
            if (
                len(by_class) == len(cands)
                and set(by_class) == typed_classes
                and all(self._class_name_unique(n) for n in by_class)
            ):
                self._split_receiver = True
                return sorted(cands, key=lambda c: (c.classname or "", c.module))
        if len(cands) != 1:
            return []  # 絞れないものは opaque(unresolved) に落とす
        chosen = cands[0]
        if want_method and chosen.classname is not None:
            typed = receiver is not None and isinstance(receiver.shape, Obj)
            if not typed or chosen.classname not in self._class_family(receiver.shape.classes):
                # **受け手型で裏付けられない、末尾名だけの解決**（D17 の改訂）。
                # 降りないと真の経路（langroid の `compute_from_docs` の eval など）が消える
                # ので降りるが、呼び出し側がその経路の効果を `opaque(unresolved)` にする。
                self._by_name_hint = True
        return [chosen]

    def _descend(
        self, callee: FuncDef, node, args, kwargs, receiver, env, scope, res, depth, chain, by_name: bool = False
    ) -> Value:
        value, _sub = self._descend_env(callee, node, args, kwargs, receiver, res, depth, chain, by_name)
        return value

    def _descend_env(
        self, callee: FuncDef, node, args, kwargs, receiver, res, depth, chain, by_name: bool = False
    ) -> tuple[Value, Optional[Env]]:
        """被呼び出しの本体を実行し、`(戻り値, 実行後の env)` を返す。

        深さ・再帰・cap で降りなかったときの env は `None`。木内クラスの構築は
        `__init__` 実行後の env から `self.<name>` を読む（D17）。
        """
        if depth + 1 > self.opt.max_depth:
            res.note_opaque("depth")
            res.cap_hits.append("depth")
            return Value(Prin.OP, opaque("depth"), Unknown(), frozenset(), _roots_all(args)), None
        if callee.key in self._active:
            res.note_opaque("recursion")
            return Value(Prin.OP, opaque("recursion"), Unknown(), frozenset(), _roots_all(args)), None
        if len(self._summaries) >= self.opt.summary_cap:
            res.note_opaque("cap")
            res.cap_hits.append("summary_cap")
            return Value(Prin.OP, opaque("cap"), Unknown(), frozenset(), _roots_all(args)), None

        path = self.index.resolve_module_path(callee.module)
        if path is None:
            res.note_opaque("unresolved")
            return Value(Prin.OP, opaque("unresolved"), Unknown(), frozenset(), _roots_all(args)), None
        callee_scope = self.index.function_scope(path, callee.node)
        seed = self._seed_params(callee, args, kwargs, receiver)
        self._summaries[callee.key] = self._summaries.get(callee.key, 0) + 1
        self._active.add(callee.key)
        pushed = False
        if not self._entry_sites:
            self._entry_sites.append(getattr(node, "lineno", 0))
            pushed = True
        sub = Env(seed)
        if by_name:
            self._by_name_depth += 1
        self._class_stack.append((callee.classname, callee.module))
        try:
            self._exec_body(
                getattr(callee.node, "body", []),
                sub,
                callee_scope,
                res,
                depth + 1,
                chain + (callee.qualname,),
            )
        finally:
            self._class_stack.pop()
            self._active.discard(callee.key)
            if by_name:
                self._by_name_depth -= 1
            if pushed:
                self._entry_sites.pop()
        ret = sub.get("<return>")
        return (ret if ret is not None else Value(Prin.OP, RESOLVED, Unknown())), sub

    def _descend_indirect(self, node, dotted, args, kwargs, env, scope, res, depth, chain) -> Value:
        """`multiprocessing.Process(target=f, args=(...))` 越しの到達。

        **1 段として数える**（Def 4）。これが無いと OpenManus `PythonExecute` が
        `opaque(unresolved)` になり、§10 の脈拍の負例期待が外れる。
        """
        row = INDIRECT_BY_NAME[dotted]
        target_node = None
        if row.target_kw:
            for kw in node.keywords:
                if kw.arg == row.target_kw:
                    target_node = kw.value
        if target_node is None and row.target_pos is not None and len(node.args) > row.target_pos:
            target_node = node.args[row.target_pos]
        if target_node is None:
            res.note_opaque("unresolved")
            return Value(Prin.OP, opaque("unresolved"), Unknown())

        inner_args: list[Value] = []
        args_node = None
        if row.args_kw:
            for kw in node.keywords:
                if kw.arg == row.args_kw:
                    args_node = kw.value
        if args_node is None and row.args_pos is not None and len(node.args) > row.args_pos:
            args_node = node.args[row.args_pos]
        if args_node is not None:
            v = self._eval(args_node, env, scope, res, depth, chain)
            inner_args = list(_elements(v)) or [v]

        callees = self._resolve_in_tree(_fake_call(target_node), dotted_of(target_node), None)
        if len(callees) != 1:  # scope なしなので pin は引かず、末尾名の検索は 0 か 1 候補
            res.note_opaque("unresolved")
            return Value(Prin.OP, opaque("unresolved"), Unknown())
        return self._descend(
            callees[0], node, inner_args, {}, None, env, scope, res, depth, chain + ("<indirect>",)
        )

    # -- D17: 組込みの値操作 / モジュール水準の束縛 / 木内クラスの構築 ----------

    def _builtin_value_op(
        self, node, dotted, receiver, receiver_path, args, kwargs, env
    ) -> Optional[Value]:
        """TRANSFER 表より先に見る組込みの値操作（D17）。

        * `os.environ.get` / `os.getenv`: config atom の源（§2.3）→ OP / resolved。
          既定値の引数があれば join する（既定が MODEL なら MODEL のまま）。
        * `sep.join(xs)`: **主語は区切り文字だが値は xs の要素から来る。** 区切り文字を
          主語にすると xs に入った MODEL が消える（false-clean）。
        * `xs.append(v)` / `insert` / `extend`、コンテナ形の `add` / `update`: 受け手への
          書き込み。**戻り値を捨てるだけにすると v の MODEL が消える**（野外 RES[7]）。
          木内クラスの同名メソッド（受け手が `Obj`）は通常の解決に回す。
        """
        k = self.opt.k
        if dotted in _ENVIRON_READS:
            item = _environ_item(self._environ_written_in_tree())
            written = env.get("os.environ")
            if written is not None:
                item = value_join(item, _element_of(written))  # この関数で書いた値の読み戻し
            default = args[1] if len(args) > 1 else kwargs.get("default")
            return value_join(item, default) if default is not None else item
        if not isinstance(node.func, ast.Attribute) or receiver is None:
            return None
        attr = node.func.attr
        if attr == "join" and len(args) == 1 and not kwargs and (
            # 型の判定なので確度に関係なく形の定数を見る（`Value.const` は resolved の値の定数しか返さない）
            isinstance(receiver.shape, Str)
            or (isinstance(receiver.shape, Atom) and isinstance(receiver.shape.const, str))
        ):
            return _str_join(receiver, args[0], k)
        if receiver_path is None or isinstance(receiver.shape, Obj):
            return None
        container = isinstance(receiver.shape, (Seq, Argv, Map))
        items: Optional[list[Value]] = None
        if attr in ("append", "appendleft") and len(args) == 1:
            items = [args[0]]
        elif attr == "insert" and len(args) == 2:
            items = [args[1]]
        elif attr == "extend" and len(args) == 1:
            items = _items_of(args[0])
        elif container and attr == "add" and len(args) == 1:
            items = [args[0]]
        elif container and attr == "update" and (args or kwargs):
            items = []
            for src in list(args) + [kwargs[key] for key in sorted(kwargs)]:
                items += _items_of(src)
        if items is None:
            return None
        new = receiver
        for it in items:
            new = _append_tail(new, it, k)
        env.set(receiver_path, new)
        if not container:
            # 形の分からない受け手: 書き込みは反映し（MODEL を落とさない）、呼び出し自体は
            # 通常の解決に回す（その結果の opaque も記録される）。
            return None
        return Value(Prin.OP, RESOLVED, Atom(const=None))

    def _module_value(self, scope: Scope, name: str, res: ValResult) -> Optional[Value]:
        """モジュール水準の束縛を読む（Def 4 / §2.3、D17）。

        * 同じモジュールの直下（`if` / `try` / `with` の中を含む）にある代入の **join**
          （flow-insensitive。どの代入が効くかを決めない）
        * `from m import NAME` は m の同名束縛を 1 段だけ追う
        * 関数内で束縛される名前（`scope.local_bindings`）は読まない
        * **評価中の呼び出し事象は効果にしない**（モジュール初期化はユニットから到達しない）

        束縛が無ければ `None`（呼び出し側が `opaque(unresolved)` にする）。
        """
        if name in scope.local_bindings:
            return None
        module, attr = scope.module, name
        reader_rebinds = False
        target = scope.lookup(name)
        if target is not None:
            mod, _, last = target.rpartition(".")
            if not mod:
                return None  # `import os` の `os` はモジュールであって値ではない
            strict = self.index.resolve_import_module(scope.module, mod)
            if strict is None:
                return None  # 外部パッケージを末尾成分一致で木内モジュールと取り違えない
            # 読む側のモジュールで import した名前が再束縛されるなら、値は読むが確度を opaque に落とす。
            reader_rebinds = name in self._module_writes(scope.module)
            module, attr = strict, last
        # **木内のどこかで再束縛される名前は定数として読まない**（D17 改訂 2 / 3）:
        # 関数内の `global` 再束縛、関数の局所変数（入れ子関数が掴む同名の外側変数を含む）、
        # 他モジュールからの `m.NAME = ...`、`globals()` / `vars()` / `exec` を使うモジュール（"*"）。
        # **コンテナ / オブジェクトの変更はここで弾かない**（型が消えて効果行ごと落ちる）。
        # 代わりに下で確度を opaque に落とす。
        writes = self._module_writes(module)
        # **読まないのではなく、型と主体を保ったまま確度を opaque に落とす**（D17 改訂 4）。
        # None を返すと受け手の型が消え、`exec` / `globals()` を含むモジュールのオブジェクトを受け手に
        # する効果行が丸ごと消えた（3 回目のレビュー）。opaque は clean ではない（§2.6）。
        rebound = attr in writes or "*" in writes or (module, attr) in self._tree_attr_writes()
        key = (module, attr)
        if key in self._module_values:
            return _reader_view(self._module_values[key], reader_rebinds)
        if key in self._module_active:
            res.note_opaque("recursion")
            return Value(Prin.OP, opaque("recursion"), Unknown())
        path = self.index.resolve_module_path(module)
        tree = self.index.parse(path) if path is not None else None
        rhs = _module_assignments(tree.body, attr) if tree is not None else []
        if not rhs or path is None:
            self._module_values[key] = None
            return None
        self._module_active.add(key)
        saved = self.on_call
        self.on_call = None
        out: Optional[Value] = None
        try:
            mscope = self.index.module_scope(path)
            for expr in rhs:
                v = self._eval(expr, Env(), mscope, res, 0, (f"<module:{module}>",))
                out = v if out is None else value_join(out, v)
        finally:
            self.on_call = saved
            self._module_active.discard(key)
        if out is not None and (rebound or not _is_immutable_value(out)):
            # コンテナ / オブジェクトは別名・補助関数・他モジュールから構文で追えない形で変更されうる。
            # **型と主体は保ち、確度だけ opaque に落とす**（効果行を落とさず、resolved の定数にもしない）。
            out = _opaque_deep(out)
        self._module_values[key] = out
        return _reader_view(out, reader_rebinds)

    def _construct_in_tree(self, node, dotted, args, kwargs, scope, res, depth, chain) -> Optional[Value]:
        """木内クラスの構築 `C(...)` を `Obj((C,), fields)` にする（§2.6 の Obj.fields、D17）。

        `__init__` を**実引数で**実行し、`self.<name>` に書かれた値を `fields` にする。
        クラスは同じモジュールの定義か import で指したモジュールの定義に限り、
        **名前だけで他モジュールの同名クラスを採らない**（`get_class(strict=True)`）。
        `__init__` の実行は木内の被呼び出しなので深さを 1 消費する。
        """
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in scope.local_bindings:
                return None
            name, module = func.id, scope.module
            if dotted is not None:  # import された名前（`from . import C` は親パッケージ）
                strict = self.index.resolve_import_module(scope.module, dotted.rpartition(".")[0])
                if strict is None:
                    return None  # 外部パッケージを木内の同名モジュールと取り違えない（D17 改訂 2）
                module = strict
        elif isinstance(func, ast.Attribute) and dotted is not None and "." in dotted:
            name = func.attr
            strict = self.index.resolve_import_module(scope.module, dotted.rpartition(".")[0])
            if strict is None:
                return None
            module = strict
        else:
            return None
        cd = self.index.get_class(name, module, strict=True)
        if cd is None:
            return None
        init = self._find_init(cd)
        # **クラス体のフィールド既定値**（`command: str = "/bin/bash"`、pydantic のクラス変数）を
        # 先に入れ、`__init__` の書き込みで上書きする（D35）。無いと `__init__` で触らない
        # 既定値が `opaque(unresolved)` になり、`self.command` を渡す sink の値が消える（F6）。
        fields: dict[str, Value] = dict(self._class_body_defaults(cd, res, depth, chain))
        if init is None:
            # dataclass / pydantic 形: 注釈つきクラス変数の順に実引数を割り当てる
            declared = [
                st.target.id
                for st in cd.node.body
                if isinstance(st, ast.AnnAssign) and isinstance(st.target, ast.Name)
            ]
            for i, fname in enumerate(declared):
                if i < len(args):
                    fields[fname] = args[i]
                elif fname in kwargs:
                    fields[fname] = kwargs[fname]
            return Value(Prin.OP, RESOLVED, Obj((cd.name,), tuple(sorted(fields.items()))))
        receiver = Value(Prin.OP, RESOLVED, Obj((cd.name,), tuple(sorted(fields.items()))))
        value, sub = self._descend_env(init, node, args, kwargs, receiver, res, depth, chain)
        if sub is None:
            # 深さ・再帰・cap で降りなかった。型と既定値だけ持ち、確度は降りなかった理由を運ぶ。
            # **既定値の確度にも同じ理由を合流する**（`__init__` が上書きしたかもしれない。
            # レビュー b3、false-clean）。
            dim = tuple(
                (n, Value(v.prin, prov_merge(v.prov, value.prov), v.shape, v.attrs, v.roots))
                for n, v in sorted(fields.items())
            )
            return Value(Prin.OP, value.prov, Obj((cd.name,), dim))
        for key, v in sub.items():
            rest = key[len("self."):] if key.startswith("self.") else None
            if rest and "." not in rest:
                fields[rest] = v
        return Value(Prin.OP, RESOLVED, Obj((cd.name,), tuple(sorted(fields.items()))))

    def _find_init(self, cd) -> Optional[FuncDef]:
        """`__init__` を自クラス → 基底（3 段まで）の順に探す。"""
        seen: set[tuple[str, str]] = set()
        todo = [cd]
        while todo and len(seen) < 4:
            c = todo.pop(0)
            if c is None or (c.module, c.name) in seen:
                continue
            seen.add((c.module, c.name))
            hits = [f for f in self.index.lookup_function(f"{c.name}.__init__", c.module) if f.module == c.module]
            if hits:
                return hits[0]
            todo += self._base_classes(c)  # **基底は import 表で厳密に引く**（D17 改訂 2）
        return None

    def _class_body_defaults(self, cd, res, depth, chain) -> dict[str, Value]:
        """クラス体の `name = value` / `name: T = value` を評価して `Obj.fields` の既定値にする。

        基底（3 段まで、import 表で厳密に引く）を先に、自クラスを後に入れて上書きする。
        値の評価は木内クラスの構築を含みうるので再帰を切る（同じクラスの評価中は空）。
        `analyze._self_fields` の (1) と同じ規則。
        """
        key = (cd.module, cd.name)
        if key in self._class_defaults_active:
            return {}
        self._class_defaults_active.add(key)
        saved = self.on_call
        self.on_call = None  # import 時の構築の効果行をツールに付けない（レビュー b4、false-dirty）
        try:
            chain_cls = [cd]
            seen = {key}
            frontier = [cd]
            for _ in range(3):
                nxt = []
                for c in frontier:
                    for b in self._base_classes(c):
                        if (b.module, b.name) not in seen:
                            seen.add((b.module, b.name))
                            nxt.append(b)
                chain_cls = nxt + chain_cls
                frontier = nxt
                if not nxt:
                    break
            out: dict[str, Value] = {}
            for c in chain_cls:
                mpath = self.index.resolve_module_path(c.module)
                if mpath is None:
                    continue
                cscope = self.index.module_scope(mpath)
                env = Env()
                for st in c.node.body:
                    target = None
                    if isinstance(st, ast.Assign) and len(st.targets) == 1:
                        target = st.targets[0]
                    elif isinstance(st, ast.AnnAssign):
                        target = st.target
                    if isinstance(target, ast.Name) and getattr(st, "value", None) is not None:
                        out[target.id] = self._eval(st.value, env, cscope, res, depth, chain)
            return out
        finally:
            self.on_call = saved
            self._class_defaults_active.discard(key)

    def _write_back_self(self, receiver_path: str, receiver: Value, sub: Env, env: Env) -> None:
        """被呼び出しの env の `self.<f>`（1 段）を、呼び出し側の `<receiver_path>.<f>` と受け手の
        `Obj.fields` に戻す。アクセスパスの深さは `RECEIVER_DEPTH` まで（読みと同じ鍵体系）。"""
        if not isinstance(receiver.shape, Obj):
            return
        writes: dict[str, Value] = {}
        for key, v in sub.items():
            if key.startswith("self.") and "." not in key[len("self."):]:
                writes[key[len("self."):]] = v
        if not writes:
            return
        cur = env.get(receiver_path)
        base = cur if cur is not None and isinstance(cur.shape, Obj) else receiver
        # **同じオブジェクトを指す別名**（`b = a` は同一の Value を束縛する）にも書き戻す
        # （レビュー b4: `b.add(cmd); a.run()` で `a` 側が既定値のままになる、false-clean）。
        # 同一性で判定するので、別々に構築した 2 つのオブジェクトは混ざらない。
        aliases = [k for k, v in env.items() if v is cur and k != receiver_path and "." not in k] if cur is not None else []
        fields = dict(base.shape.fields)
        for name, v in writes.items():
            # **上書きではなく合流する**（D35 改訂）。被呼び出しの条件つき書き込み
            # `if flag: self.cmd = "ls"` は sub の env に無条件の鍵として残るので、上書きすると
            # 呼び出し側の MODEL が OP になる（レビュー c1 / c4、false-clean）。
            key = f"{receiver_path}.{name}"
            prev = env.get(key)
            if prev is None:
                prev = fields.get(name)
            merged = v if prev is None else value_join(prev, v)
            fields[name] = merged
            if key.count(".") <= RECEIVER_DEPTH:
                env.set(key, merged)
            for a in aliases:
                env.set(f"{a}.{name}", merged)
        new_val = Value(base.prin, base.prov, Obj(base.shape.classes, tuple(sorted(fields.items()))), base.attrs, base.roots)
        env.set(receiver_path, new_val)
        for a in aliases:
            env.set(a, new_val)

    def _receiver_with_path_writes(self, receiver: Value, receiver_path: str, env: Env) -> Value:
        """env の `<receiver_path>.<f>`（呼び出し側の属性書き込み）を受け手の `Obj.fields` に載せる。"""
        cur = env.get(receiver_path)
        names = [receiver_path] + (
            [k for k, v in env.items() if v is cur and k != receiver_path and "." not in k] if cur is not None else []
        )
        fields = dict(receiver.shape.fields)
        changed = False
        for base_name in names:  # 別名（同一オブジェクト）経由の書き込みも載せる
            prefix = base_name + "."
            for key, v in env.items():
                if key.startswith(prefix) and "." not in key[len(prefix):]:
                    fields[key[len(prefix):]] = v
                    changed = True
        if not changed:
            return receiver
        return Value(receiver.prin, receiver.prov, Obj(receiver.shape.classes, tuple(sorted(fields.items()))), receiver.attrs, receiver.roots)

    def _super_callees(self, node) -> Optional[tuple[list, Optional[Value]]]:
        """`super().m(...)` なら `(基底の m の候補, 受け手 self)`。そうでなければ None。"""
        func = node.func
        if not (isinstance(func, ast.Attribute) and isinstance(func.value, ast.Call)):
            return None
        if dotted_of(func.value.func) != "super" or not self._class_stack:
            return None
        cls, module = self._class_stack[-1]
        if cls is None:
            return None
        cd = self.index.get_class(cls, module, strict=True) if module else self.index.get_class(cls)
        if cd is None:
            return [], None
        out = []
        for b in self._base_classes(cd):
            hits = [f for f in self.index.lookup_function(f"{b.name}.{func.attr}", b.module) if f.module == b.module]
            out += hits
            if hits:
                break
        return out, None

    def _class_name_unique(self, name: str) -> bool:
        """末尾名 `name` のクラス定義が木に 1 つだけか（記憶化）。"""
        memo = getattr(self, "_class_count_memo", None)
        if memo is None:
            memo = {}
            for cd in self.index.classes():
                memo[cd.name] = memo.get(cd.name, 0) + 1
            self._class_count_memo = memo
        return memo.get(name, 0) == 1

    def _in_tree_method(self, receiver: Optional[Value], method: str) -> bool:
        """受け手の木内クラス（基底 3 段まで）が `method` を定義しているか。"""
        if receiver is None or not isinstance(receiver.shape, Obj) or not receiver.shape.classes:
            return False
        family = self._class_family(receiver.shape.classes)
        return any(f.classname in family for f in self.index.lookup_function(method))

    def _class_family(self, classes) -> set[str]:
        """受け手クラスとその基底（3 段まで）の名前。継承したメソッドを解決するため。"""
        out: set[str] = set()
        frontier = [c.split(".")[-1] for c in classes]
        for _ in range(3):
            nxt: list[str] = []
            for c in frontier:
                if c in out:
                    continue
                out.add(c)
                cd = self.index.get_class(c)
                if cd is not None:
                    nxt += [b.name for b in self._base_classes(cd)]
            frontier = nxt
        return out

    # -- D17 改訂 2: 木内の書き込みを見る / import と基底を厳密に引く ---------------

    def _module_writes(self, module: str) -> frozenset[str]:
        """モジュール内で再束縛されうる名前（索引ごとに記憶化）。:func:`_scan_module_writes` を参照。"""
        cache = self.index.__dict__.setdefault("_authgap_module_writes", {})
        if module not in cache:
            path = self.index.resolve_module_path(module)
            tree = self.index.parse(path) if path is not None else None
            cache[module] = _scan_module_writes(tree) if tree is not None else frozenset()
        return cache[module]

    def _tree_attr_writes(self) -> frozenset[tuple[str, str]]:
        """木全体で `m.NAME = ...` のように**モジュール属性として**書き換えられる `(module, NAME)`。"""
        cache = self.index.__dict__
        if "_authgap_tree_attr_writes" not in cache:
            out: set[tuple[str, str]] = set()
            for path in self.index.py_files():
                tree = self.index.parse(path)
                if tree is None:
                    continue
                mscope = self.index.module_scope(path)
                for alias, attr in _attr_stores(tree):
                    target = mscope.lookup(alias)
                    strict = self.index.resolve_import_module(self.index.module_name(path), target) if target else None
                    if strict is not None:
                        out.add((strict, attr))
            cache["_authgap_tree_attr_writes"] = frozenset(out)
        return cache["_authgap_tree_attr_writes"]

    def _environ_written_in_tree(self) -> bool:
        """木内のどこかで `os.environ` に**非定数**を書き込むか（書き込むなら環境変数を config とみなさない）。"""
        cache = self.index.__dict__
        if "_authgap_environ_written" not in cache:
            written = False
            for path in self.index.py_files():
                tree = self.index.parse(path)
                if tree is not None and _writes_environ(tree, self.index.module_scope(path)):
                    written = True
                    break
            cache["_authgap_environ_written"] = written
        return cache["_authgap_environ_written"]

    def _base_classes(self, cd) -> list:
        """クラスの基底を、そのクラスのモジュールの import 表で**厳密に**解決する。

        名前だけで引くと `class Query(pydantic.BaseModel)` の基底を木内の同名 `BaseModel` と
        取り違え、その `__init__` を実行する（D17 改訂 2）。外部の基底は結果に入らない。
        """
        path = self.index.resolve_module_path(cd.module)
        mscope = self.index.module_scope(path) if path is not None else None
        out = []
        for b in cd.bases:
            head, _, rest = b.partition(".")
            last = b.split(".")[-1]
            target = mscope.lookup(head) if mscope is not None else None
            if target is not None:
                full = f"{target}.{rest}" if rest else target
                mod = self.index.resolve_import_module(cd.module, full.rpartition(".")[0])
                hit = self.index.get_class(last, mod, strict=True) if mod else None
            elif not rest:
                hit = self.index.get_class(b, cd.module, strict=True)
            else:
                hit = None
            if hit is not None:
                out.append(hit)
        return out

    def _pinned_candidates(
        self, node, dotted, last: str, scope: Optional[Scope]
    ) -> Optional[tuple[list[FuncDef], bool]]:
        """呼び出し名が import 表または同じモジュールで指す木内の関数（メソッドは除く）の候補と、
        どれが効くかが決まらないか（`ambiguous`）。引けなければ None（末尾名の木全体検索に回す）。

        末尾名だけで木全体を引くと、同名の関数が別ファイルに増えただけで 2 候補になり解決を
        失う（run 3 の spotify_mcp で `sp.get_followed_artists` の NET 効果が消えた。false-clean）。

        **呼び出し位置から見える定義だけを数える**（D17 改訂 5。`_visible_defs`）。見える定義が複数ある、
        または同じ名前が import / 代入でも束縛されるときは `ambiguous` にし、呼び出し側が**全候補へ
        降りて**行と戻り値を opaque にする。改訂 4 は見えない入れ子 def まで数えて pin をやめ、末尾名の
        検索も 2 候補で降りず、helper の中の効果行を落としていた（4 回目のレビュー）。
        """
        if scope is None:
            return None
        module: Optional[str] = None
        bare_same_module = False
        func = node.func
        if isinstance(func, ast.Name):
            if func.id in scope.local_bindings:
                return None
            if dotted is None:
                module = scope.module  # 同じモジュールで定義された素の名前
                bare_same_module = True
            elif "." in dotted:
                module = self.index.resolve_import_module(scope.module, dotted.rpartition(".")[0])
        elif isinstance(func, ast.Attribute) and dotted is not None and "." in dotted:
            head = dotted_of(func.value)
            if head is not None and scope.lookup(head.split(".")[0]) is not None:  # モジュール別名の属性
                module = self.index.resolve_import_module(scope.module, dotted.rpartition(".")[0])
        if module is None:
            return None
        # **全定義を引く**（D17 改訂 4）。`lookup_function(name, module)` は索引の setdefault で最初の
        # 定義 1 件しか返さないので、再定義・if / else の def・`@overload` のスタブを見落とす。
        cands = self._visible_defs(module, last, node if bare_same_module else None)
        if not cands:
            return None
        ambiguous = len(cands) > 1
        mpath = self.index.resolve_module_path(module)
        tree = self.index.parse(mpath) if mpath is not None else None
        if tree is None:
            return None
        if last in self.index.module_scope(mpath).module_imports or _module_assignments(tree.body, last):
            ambiguous = True  # 同じモジュールで import や代入でも束縛される（その値は追わない）
        if isinstance(func, ast.Name) and dotted is not None and module != scope.module:
            # import した名前を、読む側のモジュールの（呼び出し位置から見える）def が上書きしうる
            reader = self._visible_defs(scope.module, last, node)
            if reader:
                cands = cands + reader
                ambiguous = True
        return cands, ambiguous

    def _visible_defs(self, module: str, name: str, call: Optional[ast.AST]) -> list[FuncDef]:
        """`module` で `name` を束縛する関数定義（メソッドは除く）のうち、呼び出し位置から見えるもの。

        モジュール直下の def（`if` / `try` の中を含む）は常に見える。入れ子 def は、`call` が与えられ、
        その def を囲む関数の本体が `call` の行を含むときだけ見える（Python のスコープ規則）。
        別の関数の中の入れ子 def と、モジュール属性越し（`call=None`）の入れ子 def は見えない。
        """
        line = getattr(call, "lineno", None) if call is not None else None
        out: list[FuncDef] = []
        for f in self.index.lookup_function(name):
            if f.module != module or f.classname is not None:
                continue
            if f.qualname == name:
                out.append(f)
                continue
            parent = f.qualname[: -len(name) - 1]
            if line is not None and any(
                p.module == module
                and p.qualname == parent
                and p.node.lineno <= line <= (getattr(p.node, "end_lineno", None) or p.node.lineno)
                for p in self.index.lookup_function(parent)
            ):
                out.append(f)
        return out

    def _seed_params(self, callee: FuncDef, args, kwargs, receiver) -> dict[str, Value]:
        """呼び出し先の仮引数に実引数を割り当てる。"""
        seed: dict[str, Value] = {}
        fn_args = getattr(callee.node, "args", None)
        if fn_args is None:
            return seed
        positional = list(fn_args.posonlyargs) + list(fn_args.args)
        offset = 0
        if callee.classname is not None and positional and positional[0].arg in ("self", "cls"):
            if receiver is not None:
                seed[positional[0].arg] = receiver
            offset = 1
        for i, a in enumerate(positional[offset:]):
            if i < len(args):
                seed[a.arg] = args[i]
            elif a.arg in kwargs:
                seed[a.arg] = kwargs[a.arg]
            else:
                seed[a.arg] = _seed_from_annotation(a)
        for a in fn_args.kwonlyargs:
            seed[a.arg] = kwargs.get(a.arg, _seed_from_annotation(a))
        return seed


_MATCH = getattr(ast, "Match", None)


def _fake_call(func_node: ast.AST) -> ast.Call:
    return ast.Call(func=func_node, args=[], keywords=[])


#: 環境変数の読み出し（config atom の源。§2.3）。
_ENVIRON_READS: frozenset[str] = frozenset({"os.environ.get", "os.getenv", "os.environ.setdefault"})


def _environ_item(written_in_tree: bool = False) -> Value:
    """環境変数 1 つの値。**木内で非定数を書き込むなら config とみなさず opaque**（D17 改訂 2）。"""
    if written_in_tree:
        return Value(Prin.OP, opaque("unresolved"), Atom())
    return Value(Prin.OP, RESOLVED, Atom())


def _environ_map(written_in_tree: bool = False) -> Value:
    """`os.environ` そのもの。添字 / `.get` の値は OP / resolved（木内で書き込まれなければ）。"""
    item = _environ_item(written_in_tree)
    return Value(Prin.OP, item.prov, Map((), item))


def _iter_nodes(tree: ast.AST):
    """`(node, parent, 関数の入れ子の深さ)` を**再帰せずに**列挙する。

    集合を集める用途専用（訪問順は問わない）。再帰の NodeVisitor は、木の無関係なファイルに
    ある深い式（数百項の連結）で RecursionError を出し、木 1 本の出力を全部落とした（D17 改訂 3）。
    """
    stack: list[tuple[ast.AST, Optional[ast.AST], int]] = [(tree, None, 0)]
    while stack:
        node, parent, fdepth = stack.pop()
        yield node, parent, fdepth
        inner = fdepth + 1 if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)) else fdepth
        for child in ast.iter_child_nodes(node):
            stack.append((child, node, inner))


def _scan_module_writes(tree: ast.AST) -> frozenset[str]:
    """モジュールで**再束縛**されうる名前。`"*"` はどの名前も再束縛されうる（動的な名前空間操作）。

    * 関数内の `global` / `nonlocal` 宣言の名前
    * 関数内で束縛される名前（仮引数・代入先・for / with の束縛）。入れ子関数が掴む外側の局所変数が
      同名のモジュール定数と取り違えられるのを防ぐ
    * `globals()` / 引数なしの `vars()` / `exec` を呼ぶモジュールは `"*"`

    **コンテナ / オブジェクトの変更（`X[k] = v`、`X.a = v`、`X.append(v)`）はここでは集めない。**
    変更を「読まない」にすると受け手の型が消えて効果行ごと消える（D17 改訂 3）。別名や補助関数を
    経由した変更も構文では追い切れないので、コンテナ / オブジェクトのモジュール水準の値は常に
    確度を opaque に落とす（`_opaque_deep`）。`setattr(sys.modules[...], ...)` は見ない（限界）。
    """
    names: set[str] = set()
    for node, _parent, fdepth in _iter_nodes(tree):
        if isinstance(node, (ast.Global, ast.Nonlocal)):
            names.update(node.names)
        elif isinstance(node, ast.arg) and fdepth:
            names.add(node.arg)
        elif isinstance(node, ast.Name) and fdepth and isinstance(node.ctx, (ast.Store, ast.Del)):
            names.add(node.id)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            fid = node.func.id
            if fid in ("globals", "exec") or (fid == "vars" and not node.args):
                names.add("*")
    return frozenset(names)


def _attr_stores(tree: ast.AST) -> list[tuple[str, str]]:
    """モジュール属性の**再束縛**: `alias.NAME = ...` / `del alias.NAME` / `setattr(alias, "NAME", v)`。再帰しない。"""
    out: list[tuple[str, str]] = []
    for node, _parent, _depth in _iter_nodes(tree):
        if (
            isinstance(node, ast.Attribute)
            and isinstance(node.ctx, (ast.Store, ast.Del))
            and isinstance(node.value, ast.Name)
        ):
            out.append((node.value.id, node.attr))
        elif (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "setattr"
            and len(node.args) >= 2
            and isinstance(node.args[0], ast.Name)
            and isinstance(node.args[1], ast.Constant)
            and isinstance(node.args[1].value, str)
        ):
            out.append((node.args[0].id, node.args[1].value))
    return out


#: `os.environ` へ書き込む呼び出し。
_ENVIRON_WRITES: frozenset[str] = frozenset(
    {"os.environ.update", "os.environ.setdefault", "os.putenv", "os.environ.__setitem__"}
)


def _is_constant_expr(node: ast.AST) -> bool:
    if isinstance(node, ast.Constant):
        return True
    if isinstance(node, ast.Dict):
        return all(v is not None and _is_constant_expr(v) for v in node.values)
    return False


def _writes_environ(tree: ast.AST, scope: Scope) -> bool:
    """このモジュールが `os.environ` に**非定数**を書き込みうるか。再帰しない。

    字面の `os.environ[k] = v` と書き込みメソッドに加え、**`env = os.environ` のような別名への
    束縛**も書き込みとみなす（別名経由の書き込みを構文で追い切れないため。D17 改訂 3）。
    `{**os.environ}` / `dict(os.environ)` / `os.environ.copy()` は複製なので書き込みではない。
    `os.environ` そのものを関数に渡してその中で書き換える形は見ない（限界として記録）。
    """
    for node, _parent, _depth in _iter_nodes(tree):
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            for t in targets:
                if (
                    isinstance(t, ast.Subscript)
                    and resolve_call_name(t.value, scope) == "os.environ"
                    and (node.value is None or not _is_constant_expr(node.value))
                ):
                    return True
            if node.value is not None and resolve_call_name(node.value, scope) == "os.environ":
                return True
        elif isinstance(node, ast.AugAssign):
            if isinstance(node.target, ast.Subscript) and resolve_call_name(node.target.value, scope) == "os.environ":
                return True
        elif isinstance(node, ast.NamedExpr):
            if resolve_call_name(node.value, scope) == "os.environ":
                return True
        elif isinstance(node, ast.Call) and resolve_call_name(node.func, scope) in _ENVIRON_WRITES:
            vals = list(node.args[1:] if len(node.args) > 1 else node.args) + [kw.value for kw in node.keywords]
            if any(not _is_constant_expr(v) for v in vals):
                return True
    return False


def _reader_view(v: Optional[Value], reader_rebinds: bool) -> Optional[Value]:
    """読む側のモジュールで名前が再束縛されるときは、記憶化した値の確度を opaque に落として返す。"""
    return _opaque_deep(v) if (reader_rebinds and v is not None) else v


def _is_immutable_value(v: Value) -> bool:
    """別名経由で変更されない値（スカラー・文字列・パス）か。コンテナ / オブジェクト / 形不明は偽。"""
    return isinstance(v.shape, (Atom, Str, Path))


def _opaque_deep(v: Value, depth: int = 2) -> Value:
    """値とその要素 / フィールドの確度に `opaque(unresolved)` を合流する。**形と主体は保つ**
    （受け手の型が残るので proxy sink の効果行は落ちない）。列と辞書には「まだ見ていない要素」を
    表す opaque の tail を足す（別の場所で追加されたキーを読む形のため）。"""
    unknown = Value(Prin.OP, opaque("unresolved"), Unknown())
    s = v.shape
    if depth > 0:
        if isinstance(s, (Seq, Argv)):
            tail = _opaque_deep(s.tail, depth - 1) if s.tail is not None else unknown
            s = type(s)(tuple(_opaque_deep(e, depth - 1) for e in s.elems), tail)
        elif isinstance(s, Map):
            tail = _opaque_deep(s.tail, depth - 1) if s.tail is not None else unknown
            s = Map(tuple((k, _opaque_deep(e, depth - 1)) for k, e in s.entries), tail)
        elif isinstance(s, Obj):
            s = Obj(s.classes, tuple((k, _opaque_deep(e, depth - 1)) for k, e in s.fields))
    if isinstance(s, Str):
        # **Str の part にも合流する**（D17 改訂 5）。`_make_str` は連結のたびに part を平らに展開する
        # ので、外側の確度だけ落としても `BASE = HOST + VERSION` の part が resolved のまま URL 分割に
        # 届き、再束縛される BASE から host = OP / resolved を切り出していた（4 回目のレビューの再現中に発見）。
        # part は Str にならない（平らにしてある）ので深さは消費しない。
        s = Str(
            tuple(_opaque_deep(p, 0) for p in s.parts),
            _opaque_deep(s.tail, 0) if s.tail is not None else None,
        )
    return Value(v.prin, prov_merge(v.prov, opaque("unresolved")), s, v.attrs, v.roots)


def _module_assignments(body: list, name: str) -> list[ast.AST]:
    """モジュール直下の `name = ...` / `name: T = ...` の右辺（`if` / `try` / `with` の中も見る）。"""
    out: list[ast.AST] = []
    for st in body:
        if isinstance(st, ast.Assign):
            if any(isinstance(t, ast.Name) and t.id == name for t in st.targets):
                out.append(st.value)
        elif isinstance(st, ast.AnnAssign):
            if isinstance(st.target, ast.Name) and st.target.id == name and st.value is not None:
                out.append(st.value)
        elif isinstance(st, (ast.If, ast.Try, ast.With, ast.AsyncWith, getattr(ast, "TryStar", ast.Try))):
            inner = (
                list(getattr(st, "body", []))
                + list(getattr(st, "orelse", []))
                + list(getattr(st, "finalbody", []))
            )
            for h in getattr(st, "handlers", []):
                inner += list(h.body)
            out += _module_assignments(inner, name)
    return out


def _items_of(v: Value) -> list[Value]:
    """列の要素（tail を含む）。列の形でなければ代表値 1 つ。"""
    if isinstance(v.shape, (Seq, Argv, Map)):
        items = list(_elements(v))
        if v.shape.tail is not None:
            items.append(v.shape.tail)
        return items
    return [_element_of(v)]


def _str_join(sep: Value, seq: Value, k: int) -> Value:
    """`sep.join(seq)`。値の主体と確度は**要素**と区切り文字の両方から採る。"""
    items = _items_of(seq)
    if not items:
        return Value(Prin.OP, RESOLVED, Atom(const=""))
    parts: list[Value] = []
    for i, it in enumerate(items):
        if i:
            parts.append(sep)
        parts.append(it)
    return _make_str(parts, k)


# --------------------------------------------------------------------------
# 補助
# --------------------------------------------------------------------------


def access_path(node: ast.AST, max_depth: int = RECEIVER_DEPTH) -> Optional[str]:
    """受け手アクセスパス（深さ `max_depth` まで）。それ以上は `None`。

    `self._session` は返すが `self._session._process.stdin` は返さない
    （§2.6 の `opaque(receiver)`）。**読みと書きで同一のキー体系を使う。**
    """
    parts: list[str] = []
    cur = node
    while isinstance(cur, ast.Attribute):
        parts.append(cur.attr)
        cur = cur.value
    if not isinstance(cur, ast.Name):
        return None
    parts.append(cur.id)
    parts.reverse()
    if len(parts) - 1 > max_depth:
        return None
    return ".".join(parts)


def _seed_from_annotation(arg: ast.arg) -> Value:
    """入口仮引数の shape を注釈から種付ける（§2.6）。

    注釈は**文字列として読むだけ**で型環境は構築しない。注釈由来の shape を
    使った位置は `shape_from = annotation` を記録し、注釈が嘘だった場合の
    FP を切り分けられるようにする（`effects` 側が記録する）。
    """
    text = ""
    if arg.annotation is not None:
        try:
            text = ast.unparse(arg.annotation)
        except Exception:  # pragma: no cover
            text = ""
    lowered = text.lower()
    if lowered.startswith("list") or lowered.startswith("sequence") or lowered.startswith("tuple"):
        return Value(Prin.OP, RESOLVED, Seq((), Value(Prin.OP, RESOLVED, Atom(formal=arg.arg))))
    if lowered.startswith("dict") or lowered.startswith("mapping"):
        return Value(Prin.OP, RESOLVED, Map((), Value(Prin.OP, RESOLVED, Atom(formal=arg.arg))))
    return Value(Prin.OP, RESOLVED, Atom(formal=arg.arg))


def seed_model_param(arg_name: str, root: str, annotation: Optional[str] = None) -> Value:
    """R2 が与える MODEL 引数の初期値。"""
    shape: Any = Atom(formal=arg_name)
    if annotation:
        low = annotation.lower()
        if low.startswith("list") or low.startswith("sequence") or low.startswith("tuple"):
            shape = Seq((), Value(Prin.MODEL, RESOLVED, Atom(formal=arg_name), frozenset(), frozenset({root})))
        elif low.startswith("dict") or low.startswith("mapping"):
            shape = Map((), Value(Prin.MODEL, RESOLVED, Atom(formal=arg_name), frozenset(), frozenset({root})))
    return Value(Prin.MODEL, RESOLVED, shape, frozenset(), frozenset({root}))


def _prin2(a: Value, b: Value) -> Prin:
    return a.prin if a.prin >= b.prin else b.prin


def _prin_all(vals) -> Prin:
    """要素の主体の join。

    **空の列は OP**（コードに書かれた定数の列であって利用者由来ではない）。
    `Prin.USER` を既定にすると空 argv が USER になり、P0 の判定が緩む。
    """
    out = Prin.OP
    for v in vals:
        if v.prin > out:
            out = v.prin
    return out


def _refine_roots(v: Value, base_roots: frozenset[str], key: str) -> Value:
    """`arguments["repo_path"]` のように root をキーで具体化する。"""
    if not base_roots:
        return v
    refined = frozenset(f'{r}["{key}"]' for r in base_roots)
    return Value(v.prin, v.prov, v.shape, v.attrs, (v.roots - base_roots) | refined)


def _prov_all(vals) -> Prov:
    return prov_merge(*[v.prov for v in vals]) if vals else RESOLVED


def _roots_all(vals) -> frozenset[str]:
    out: frozenset[str] = frozenset()
    for v in vals:
        out |= v.roots
    return out


def _elements(v: Value) -> list[Value]:
    if isinstance(v.shape, (Seq, Argv)):
        return list(v.shape.elems)
    if isinstance(v.shape, Map):
        return [val for _k, val in v.shape.entries]
    return []


def _element_of(v: Value) -> Value:
    """列の「どれか 1 つ」を表す値。tail があればそれ、無ければ要素の join。"""
    if isinstance(v.shape, (Seq, Argv)):
        if v.shape.tail is not None:
            return v.shape.tail
        elems = list(v.shape.elems)
        if elems:
            out = elems[0]
            for e in elems[1:]:
                out = value_join(out, e)
            return out
    if isinstance(v.shape, Map):
        vals = [val for _k, val in v.shape.entries]
        if v.shape.tail is not None:
            return v.shape.tail
        if vals:
            out = vals[0]
            for e in vals[1:]:
                out = value_join(out, e)
            return out
    return Value(v.prin, v.prov, Unknown(), v.attrs, v.roots)


def _make_str(parts: list[Value], k: int) -> Value:
    flat: list[Value] = []
    for p in parts:
        if isinstance(p.shape, Str):
            flat.extend(p.shape.parts)
            if p.shape.tail is not None:
                flat.append(p.shape.tail)
        else:
            flat.append(p)
    tail = None
    if len(flat) > k:
        rest = flat[k:]
        tail = rest[0]
        for r in rest[1:]:
            tail = value_join(tail, r)
        flat = flat[:k]
    return Value(
        _prin_all(parts),
        _prov_all(parts),
        Str(tuple(flat), tail),
        frozenset({"joined"}) if len(parts) > 1 else frozenset(),
        _roots_all(parts),
    )


def _append_tail(cur: Optional[Value], value: Value, k: int) -> Value:
    """列への追記。K を超えたら `tail` に畳む（widening）。"""
    if cur is None:
        return Value(value.prin, value.prov, Seq((), value), frozenset(), value.roots)
    if isinstance(cur.shape, (Seq, Argv)):
        elems = list(cur.shape.elems)
        tail = cur.shape.tail
        if len(elems) < k and tail is None:
            # **tail がある列の後ろに elems として足さない**（位置が確定しなくなる）。
            elems.append(value)
        else:
            tail = value if tail is None else value_join(tail, value)
        cls = type(cur.shape)
        return Value(
            _prin2(cur, value),
            prov_merge(cur.prov, value.prov),
            cls(tuple(elems), tail),
            cur.attrs & value.attrs,
            cur.roots | value.roots,
        )
    return value_join(cur, value)


def _widen(env: Env, k: int) -> Env:
    """K を超える要素を `tail` に畳む（5 種すべてに適用する）。"""
    out = Env()
    for key, v in env.items():
        out.set(key, _widen_value(v, k))
    return out


def _widen_value(v: Value, k: int) -> Value:
    s = v.shape
    if isinstance(s, (Seq, Argv)) and len(s.elems) > k:
        head, rest = s.elems[:k], s.elems[k:]
        tail = s.tail
        for r in rest:
            tail = r if tail is None else value_join(tail, r)
        return Value(v.prin, v.prov, type(s)(head, tail), v.attrs, v.roots)
    if isinstance(s, Str) and len(s.parts) > k:
        head, rest = s.parts[:k], s.parts[k:]
        tail = s.tail
        for r in rest:
            tail = r if tail is None else value_join(tail, r)
        return Value(v.prin, v.prov, Str(head, tail), v.attrs, v.roots)
    if isinstance(s, Path) and len(s.segs) > k:
        head, rest = s.segs[:k], s.segs[k:]
        tail = s.tail
        for r in rest:
            tail = r if tail is None else value_join(tail, r)
        return Value(v.prin, v.prov, Path(s.base, head, tail), v.attrs, v.roots)
    if isinstance(s, Map) and len(s.entries) > k:
        head, rest = s.entries[:k], s.entries[k:]
        tail = s.tail
        for _kk, r in rest:
            tail = r if tail is None else value_join(tail, r)
        return Value(v.prin, v.prov, Map(head, tail), v.attrs, v.roots)
    return v


def _build_obj(row, args: list[Value], kwargs: dict[str, Value]) -> Value:
    """ライブラリ コンストラクタから `Obj` を作る（`fields` を持つ）。"""
    fields: list[tuple[str, Value]] = []
    for fname, ref in sorted(row.fields.items()):
        if ref.startswith("arg"):
            i = int(ref[3:])
            if i < len(args):
                fields.append((fname, args[i]))
        elif ref.startswith("kw:"):
            key = ref[3:]
            if key in kwargs:
                fields.append((fname, kwargs[key]))
        elif ref.startswith("const:"):
            fields.append((fname, Value(Prin.OP, RESOLVED, Atom(const=_parse_const(ref[6:])))))
    vals = [v for _n, v in fields]
    return Value(
        Prin.OP,
        _prov_all(vals) if vals else RESOLVED,
        Obj((row.cls,), tuple(fields)),
        frozenset(),
        _roots_all(vals),
    )


def _parse_const(text: str):
    if text == "True":
        return True
    if text == "False":
        return False
    return text
