"""§2.5.3 + §2.5.5 + Def 5: ゲートの認識・等級づけ・最弱等級の計算。

評価順は **(1) 主語一致 → (2) ゲート認識（A-a/A-b/A-c）→ (3) 支配**（§2.5.3）。

この module が守る規則:

* **推定で A にしない。** 名前だけカタログに一致し A-a/A-b/A-c のどれも取れず、
  呼び出し先が木内で解決できない場合は ``OPAQUE(gate_name_only)``。
  呼び出し先が解決できて「ゲートしない」と分かった場合は ``NODOM(no_gate)``
  （こちらは判定できているので OPAQUE にしない）。
* **主語一致に失敗した述語は `NODOM(non_binding_gate)`。** `OPAQUE(gate_name_only)`
  にはしない（主語不一致は呼び出し先本体を見なくても決まるから）。主語一致は
  V にのみ課す。承認は位置ではなく効果の発生に対する承認である。
* **`strong` は推定で出さない。** 判定不能は `unknown`。
* 3 値の合成の優先順は ``NODOM > OPAQUE > DOM``（:func:`authgap.ir.dom_combine`）。

§2.5.5 の不動点と、ここで使う直接計算の関係:

    in[n]  = ⊓_{p ∈ pred(n)} out[p]
    out[n] = in[n] ⊔ ( grade(n) if gates(n, e) else bottom )
    req(e) = ⊓_{c ∈ Copies(e)} in[c]

`gates(n, e)` は (G-i) に支配を含むので、`gates(n,e)` が成り立つ n は
**e へのすべての経路上にある**。したがって各経路の ⊔ は同一集合の ⊔ になり、
経路集合の ⊓ もその値に一致する。すなわち

    req(e) = ⊔ { grade(n) : gates(n, e) }

で厳密に等しい。実装は右辺（経路を列挙しない）を採り、左辺の不動点は
:func:`req_by_fixpoint` として残して**テストで両者の一致を確認する**
（学生が手で追える形にするため）。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass, field
from typing import Optional

from .catalog import validators as V
from .catalog.entries import APPROVAL_INTERRUPTS, APPROVAL_NAMES
from .catalog.transfers import LEXICAL_CANONS, SYMLINK_RESOLVERS
from .cfgbuild import CFG, build_cfg
from .dominance import (
    DomTree,
    compute_dominators,
    deny_successors,
    gates,
    subject_names,
)
from .ir import REQ_BOTTOM, DomKind, DomResult, Req, req_join, req_meet, stable_repr
from .srcindex import FuncDef, Scope, SourceIndex, dotted_of, resolve_call_name

#: A-b のゲート要約を取るときの木内解決の深さ上限（§2.5.3）。
GATE_SUMMARY_DEPTH = 2

#: SQL を構文木へ正規化する呼び出し。`statement_type_only` の判定に使う。
#: **これらは「値を安全にする」ものではない。** 文型が読めるようになるだけで、
#: 許可された文型のまま危険な操作はできる（A18 の witness）。
SQL_CANONICALISERS: frozenset[str] = frozenset(
    {"sqlglot.parse", "sqlglot.parse_one", "sqlparse.parse", "sqlparse.parsestream"}
)

#: 承認割り込みのうち「呼ぶと拒否時に送出する」とカタログが宣言する名前（A-a）。
RAISES_FORM_NAMES: frozenset[str] = frozenset(
    r.name for r in APPROVAL_INTERRUPTS if r.form == "raises"
)


# --------------------------------------------------------------------------
# config atom（Def 5。源は 4 種）
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ConfigAtom:
    """ゲート述語が読む設定値。既定が開なら `req` は MODEL のまま。"""

    name: str
    source: str
    default: object = None
    #: 既定が閉か。**判定できなければ None**（推定しない）。
    default_closed: Optional[bool] = None

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "source": self.source,
            "default": self.default if isinstance(self.default, (str, int, float, bool, type(None))) else stable_repr(self.default),
            "default_closed": self.default_closed,
        }


def module_constants(tree: ast.Module) -> dict[str, ast.expr]:
    """モジュール水準の定数代入（config atom の源: ``module_const``）。"""
    out: dict[str, ast.expr] = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    out[t.id] = node.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name) and node.value is not None:
            out[node.target.id] = node.value
    return out


def literal_of(expr: ast.expr) -> tuple[bool, object]:
    """式がリテラルなら `(True, 値)`。そうでなければ `(False, None)`。"""
    try:
        return True, ast.literal_eval(expr)
    except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError):
        return False, None


#: 木ごとの config atom 表。`find_gate_candidates` に渡す。
_ATOM_INDEX_CACHE: dict[str, object] = {}


def atom_index_for(index: Optional[SourceIndex]):
    """木の config atom 表（4 源）。**1 回だけ作って使い回す。**"""
    if index is None:
        return None
    key = index.src_root
    if key not in _ATOM_INDEX_CACHE:
        from .atoms import build_atom_index

        _ATOM_INDEX_CACHE[key] = build_atom_index(index)
    return _ATOM_INDEX_CACHE[key]


def resolve_atom_via_scope(
    name: str, tree: Optional[ast.Module], scope: Optional[Scope], index: Optional[SourceIndex]
) -> Optional[ConfigAtom]:
    """定数名を、まず当該モジュールで、次に import 元の木内モジュールで解決する。

    `from _prelude import ALLOWED_TOOLS` のように**別モジュールの定数を主語に
    する allowlist** が母集団の主要形なので、当該モジュールだけを見ると
    既定の開閉が決まらず、既定閉の allowlist が全部 MODEL のままになる。
    """
    if tree is not None:
        hit = resolve_atom(name, tree)
        if hit is not None and hit.default_closed is not None:
            return hit
    # **4 源すべてを見る**（Def 5）。モジュール定数だけだと、pydantic の
    # クラス既定値や CLI 既定値で開閉が決まる atom を読み落とし、
    # `config-conditional(atom, default)` による `req` の引き上げが
    # 常に効かなくなる（A18 / A14 がその形）。
    ai = atom_index_for(index)
    if ai is not None:
        hit = ai.lookup(name, scope.module if scope is not None else None)
        if hit is not None:
            return ConfigAtom(hit.name, hit.source, hit.default, hit.default_closed)
    if scope is not None and index is not None:
        dotted = scope.lookup(name)
        if dotted:
            mod = dotted.rsplit(".", 1)[0] if "." in dotted else dotted
            path = index.resolve_module_path(mod)
            if path:
                other = index.parse(path)
                if other is not None:
                    hit2 = resolve_atom(dotted.rsplit(".", 1)[-1], other)
                    if hit2 is not None:
                        return hit2
    return resolve_atom(name, tree) if tree is not None else None


def resolve_atom(name: str, tree: ast.Module) -> Optional[ConfigAtom]:
    """名前をモジュール定数として解決する（4 源のうち ``module_const``）。

    コンストラクタ kwarg / `os.environ` / CLI 既定値は val エンジンの env が
    必要なので、ここでは扱わず呼び出し側が :class:`ConfigAtom` を渡す。
    """
    consts = module_constants(tree)
    if name not in consts:
        return None
    ok, value = literal_of(consts[name])
    if not ok:
        if isinstance(consts[name], ast.Call):
            fn = dotted_of(consts[name].func) or ""
            if fn.endswith("environ.get") or fn.endswith("getenv"):
                return ConfigAtom(name, "environ", None, None)
        return ConfigAtom(name, "module_const", None, None)
    return ConfigAtom(name, "module_const", value, V.is_default_closed(value))


# --------------------------------------------------------------------------
# 関数サマリ（A-b のゲート要約と、値検証子の等級づけ）
# --------------------------------------------------------------------------


@dataclass
class FuncSummary:
    """木内のユーザ定義関数についてゲート判定に要る情報。"""

    key: str
    #: 拒否側の出口がすべて raise / exit か。**判定できなければ None。**
    raises_on_deny: Optional[bool] = None
    is_contextmanager: bool = False
    #: 値検証としての等級（`strong-path` / `strong-token` / `weak` / `unknown` / None）。
    value_grade: Optional[str] = None
    weak_reason: Optional[str] = None
    #: 本体に現れた validator 形状（§6 F0a の 11 語）。
    shapes: frozenset[str] = frozenset()
    #: 本体が読む config atom 名。
    atom_names: frozenset[str] = frozenset()
    #: 解決済みの config atom。**検証子が定義されたモジュールで解決する**
    #: （呼び出し側のモジュールには定数が無いことが普通だから）。
    atom: Optional[ConfigAtom] = None
    #: 本体が返り値で allowlist 判定をしているときの被参照集合名。
    membership_sets: frozenset[str] = frozenset()
    #: **検証述語が実際に見ている仮引数の名前。**
    #: `git_diff(repo, target)` の dash 検査は `target` を見ているので、
    #: `repo` 経由で無関係な位置（`cwd`）に等級が付くのを防ぐ。
    checked_params: frozenset[str] = frozenset()
    notes: tuple[str, ...] = ()


def _decorator_names(fn: ast.AST) -> set[str]:
    out: set[str] = set()
    for d in getattr(fn, "decorator_list", []):
        name = dotted_of(d.func if isinstance(d, ast.Call) else d)
        if name:
            out.add(name)
            out.add(name.split(".")[-1])
    return out


def _shapes_in(fn: ast.AST, scope: Scope) -> tuple[set[str], set[str]]:
    """本体に現れた validator 形状と、その dotted / メソッド名。"""
    shapes: set[str] = set()
    seen: set[str] = set()
    for node in ast.walk(fn):
        if not isinstance(node, ast.Call):
            continue
        dotted = resolve_call_name(node.func, scope)
        if dotted:
            s = V.shape_for_dotted(dotted)
            if s:
                shapes.add(s)
                seen.add(dotted)
        if isinstance(node.func, ast.Attribute):
            s = V.shape_for_method(node.func.attr)
            if s:
                shapes.add(s)
                seen.add(node.func.attr)
    for node in ast.walk(fn):
        if isinstance(node, ast.Attribute) and V.shape_for_method(node.attr):
            shapes.add(V.shape_for_method(node.attr))  # type: ignore[arg-type]
    return shapes, seen


def _transform_names(fn: ast.AST, scope: Scope) -> set[str]:
    """本体で適用された正規化子の transform 名。"""
    out: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            dotted = resolve_call_name(node.func, scope)
            if dotted in ("os.path.realpath", "os.realpath"):
                out.add("realpath")
            elif dotted == "os.path.normpath":
                out.add("normpath")
            elif dotted == "os.path.abspath":
                out.add("abspath")
        if isinstance(node, ast.Attribute) and node.attr == "resolve":
            out.add("Path.resolve")
    return out


def _containment_forms(fn: ast.AST, scope: Scope) -> set[str]:
    """本体に現れた包含述語（Def 5 strong-path (ii)）。"""
    out: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            dotted = resolve_call_name(node.func, scope)
            if dotted == "os.path.commonpath":
                out.add("os.path.commonpath")
            if isinstance(node.func, ast.Attribute):
                if node.func.attr in ("is_relative_to", "relative_to"):
                    out.add(node.func.attr)
                if node.func.attr == "startswith":
                    # **`startswith("-")` はフラグ拒否であって包含述語ではない。**
                    # 包含述語として数えると、`git_diff` のような
                    # 「引数の先頭がハイフンかを見るツール実装」がパス検証子に
                    # 化け、無関係な位置に weak(prefix_no_canon) が付く。
                    if _is_dash_literal(node.args):
                        out.add("dash_reject")
                    else:
                        out.add("startswith")
        if isinstance(node, ast.Compare):
            for op, comp in zip(node.ops, node.comparators, strict=False):
                if isinstance(op, (ast.In, ast.NotIn)) and isinstance(comp, (ast.Set, ast.List, ast.Tuple, ast.Name)):
                    out.add("exact_allowlist")
    return out


def _is_first_token_check(fn: ast.AST, scope: Scope) -> bool:
    """`split(...)[0]` の結果が会員判定に入る形か（Def 5 の `first_token`）。

    `command.split()[0] in config.shell_allowlist`（A5 脆弱側）も
    `shlex.split(command_line)[0] in allowlist`（A5 修正側）も同じ形で、
    **どちらも先頭トークンしか見ていない**。修正が `shlex` を入れても
    等級が上がらないことを示すのがこの判定である
    （否定規則: `shlex.split` の存在だけでは strong に上げない）。
    """
    first_tokens: set[str] = set()
    for node in ast.walk(fn):
        # `X.split(...)[0]` / `shlex.split(X)[0]`
        if not isinstance(node, ast.Subscript):
            continue
        idx = node.slice
        if not (isinstance(idx, ast.Constant) and idx.value == 0):
            continue
        val = node.value
        if not isinstance(val, ast.Call):
            continue
        dotted = resolve_call_name(val.func, scope)
        attr = val.func.attr if isinstance(val.func, ast.Attribute) else None
        if dotted in ("shlex.split",) or attr in ("split", "rsplit"):
            first_tokens.add("yes")
    if not first_tokens:
        return False
    # 会員判定（`in` / `not in`）が本体にあること。
    for node in ast.walk(fn):
        if isinstance(node, ast.Compare) and node.ops:
            if isinstance(node.ops[0], (ast.In, ast.NotIn)):
                return True
    return False


def _is_statement_type_check(fn: ast.AST, scope: Scope) -> bool:
    """SQL を構文木に正規化してから**文型**の allowlist を掛ける形か。

    A18（langroid）の修正がこれ。`sqlglot.parse(query)` の結果の型名を
    `allowed_statement_types` と突き合わせる。**値そのものは自由な SQL のまま**
    なので strong ではなく、拒否リストでもないので `denylist_enum` でもない。
    """
    canon = False
    member = False
    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            dotted = resolve_call_name(node.func, scope)
            if dotted in SQL_CANONICALISERS:
                canon = True
        elif isinstance(node, ast.Compare) and node.ops:
            if isinstance(node.ops[0], (ast.In, ast.NotIn)):
                member = True
    return canon and member


def _is_dash_literal(args: list) -> bool:
    for a in args:
        if isinstance(a, ast.Constant) and isinstance(a.value, str) and a.value in ("-", "--"):
            return True
    return False


def _predicate_operands(fn: ast.AST, scope: Scope) -> set[str]:
    """本体の検証述語が見ている**名前**を集める。

    * `X.startswith(...)` / `X.resolve()` / `X.relative_to(Y)` → 受け手 X
    * `os.path.commonpath([a, b])` / `rev_parse(a)` / `exists(a)` → 実引数
    * `x in S` → 左辺 x
    """
    names: set[str] = set()

    def add(node) -> None:
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                names.add(sub.id)
            elif isinstance(sub, ast.Attribute):
                d = dotted_of(sub)
                if d:
                    names.add(d)

    for node in ast.walk(fn):
        if isinstance(node, ast.Call):
            dotted = resolve_call_name(node.func, scope)
            shape = V.shape_for_dotted(dotted) if dotted else None
            attr = node.func.attr if isinstance(node.func, ast.Attribute) else None
            mshape = V.shape_for_method(attr) if attr else None
            if shape is None and mshape is None:
                continue
            if mshape is not None and attr in ("startswith", "resolve", "relative_to", "is_relative_to"):
                add(node.func.value)
            else:
                for a in node.args:
                    add(a)
        elif isinstance(node, ast.Compare) and node.ops:
            if isinstance(node.ops[0], (ast.In, ast.NotIn, ast.Eq, ast.NotEq)):
                add(node.left)
    return names


def _checked_params(fn: ast.AST, scope: Scope) -> frozenset[str]:
    """検証述語のオペランドを局所の代入連鎖で仮引数まで遡る。"""
    operands = _predicate_operands(fn, scope)
    if not operands:
        return frozenset()
    seen = set(operands)
    changed = True
    while changed:
        changed = False
        for node in ast.walk(fn):
            targets: list = []
            value = None
            if isinstance(node, ast.Assign):
                targets, value = list(node.targets), node.value
            elif isinstance(node, ast.AnnAssign) and node.value is not None:
                targets, value = [node.target], node.value
            elif isinstance(node, (ast.For, ast.AsyncFor)):
                # `for f in files:` の `f` は `files` に由来する。
                # ここを落とすと A4 の `for f in files: (root / f).resolve()` が
                # 「どの仮引数も検査していない」と読まれ、修正が見えなくなる。
                targets, value = [node.target], node.iter
            elif isinstance(node, ast.comprehension):
                targets, value = [node.target], node.iter
            elif isinstance(node, ast.withitem) and node.optional_vars is not None:
                targets, value = [node.optional_vars], node.context_expr
            if value is None:
                continue
            tnames: set[str] = set()
            for t in targets:
                for sub in ast.walk(t):
                    if isinstance(sub, ast.Name):
                        tnames.add(sub.id)
            if tnames & seen:
                for sub in ast.walk(value):
                    if isinstance(sub, ast.Name) and sub.id not in seen:
                        seen.add(sub.id)
                        changed = True
    params: set[str] = set()
    args = getattr(fn, "args", None)
    if args is not None:
        for a in list(args.posonlyargs) + list(args.args) + list(args.kwonlyargs):
            if a.arg in seen and a.arg not in ("self", "cls"):
                params.add(a.arg)
    return frozenset(params)


def _startswith_has_sep(fn: ast.AST) -> bool:
    """`startswith(root + os.sep)`（root が `os.sep` 終端に正規化されている形）か。

    Def 5(ii) が包含述語として認めるのはこの形であって、素の `startswith` では
    ない。**引数の式だけを見てはならない。** 母集団の主要形は

        if not abs_dir.endswith(os.sep):
            abs_dir += os.sep
        return abs_file.startswith(abs_dir)

    のように**前の文で境界を正規化してから**素の名前を渡す形で、引数の式だけを
    見ると境界の無い前置一致に見える。これを取り違えると
    `strong-path` が `weak(prefix_no_boundary)` に落ち、正しく直した修正版が
    脆弱版と同じ等級になる（A10 が実例）。
    """
    subjects: set[str] = set()
    for node in ast.walk(fn):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr != "startswith":
                continue
            for a in node.args:
                # (1) 引数の式そのものが `root + os.sep` / 末尾が区切りのリテラル
                for sub in ast.walk(a):
                    if isinstance(sub, ast.Attribute) and sub.attr in ("sep", "altsep"):
                        return True
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                        if sub.value.endswith(("/", "\\")):
                            return True
                # (2) 引数が名前なら、その名前が本体のどこかで区切り終端に
                #     正規化されているかを見る
                if isinstance(a, ast.Name):
                    subjects.add(a.id)
    if not subjects:
        return False
    return any(_normalised_to_sep(fn, name) for name in sorted(subjects))


def _normalised_to_sep(fn: ast.AST, name: str) -> bool:
    """`name` が本体のどこかで `os.sep` 終端に正規化されているか。

    認める形は 3 つだけ（**推定で広げない**）:

    * ``name += os.sep`` / ``name = name + os.sep``
    * ``name = name.rstrip(os.sep) + os.sep``
    * ``name = os.path.join(name, "")``
    """
    for node in ast.walk(fn):
        target = None
        value = None
        if isinstance(node, ast.AugAssign) and isinstance(node.op, ast.Add):
            target, value = node.target, node.value
        elif isinstance(node, ast.Assign) and len(node.targets) == 1:
            target, value = node.targets[0], node.value
        if not isinstance(target, ast.Name) or target.id != name or value is None:
            continue
        for sub in ast.walk(value):
            if isinstance(sub, ast.Attribute) and sub.attr in ("sep", "altsep"):
                return True
            if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
                if sub.value in ("/", "\\") or sub.value.endswith(("/", "\\")):
                    return True
            if isinstance(sub, ast.Call):
                fname = dotted_of(sub.func) or ""
                if fname.endswith("path.join") and len(sub.args) >= 2:
                    last = sub.args[-1]
                    if isinstance(last, ast.Constant) and last.value == "":
                        return True
    return False


def _value_grade(
    transforms: set[str],
    containments: set[str],
    shapes: set[str],
    fn: ast.AST,
    first_token: bool = False,
    statement_type: bool = False,
) -> tuple[Optional[str], Optional[str]]:
    """Def 5 の値検証等級。**strong は推定で出さない。**

    **weak 理由は値の領域ごとに分かれている。** `prefix_no_canon` /
    `no_containment` / `no_symlink_resolution` はパス領域の語であり、
    シェルコマンドの allowlist に付けてはならない（A5 がその実例で、
    `command.split()[0] in allowlist` は `first_token` である）。
    したがって領域を先に決める:

    1. 先頭トークン検査（`split()[0]` が会員判定に入る）→ `weak(first_token)`
    2. パス正規化子がある → パス領域の規則
    3. どちらでもない → 会員判定は config atom 規則に任せて等級は付けない
    """
    has_symlink = bool(transforms & SYMLINK_RESOLVERS)
    has_lexical = bool(transforms & LEXICAL_CANONS)
    dash_reject = "dash_reject" in containments
    existence = "exists" in shapes

    if first_token:
        # **A5 / A6 の形。** 先頭トークンだけを見る allowlist / denylist は
        # `ls; rm -rf /` のような witness で抜けられる。
        return "weak", "first_token"

    if statement_type:
        # **A18 の形。** 文型は絞れているが値は自由な SQL のまま。
        return "weak", "statement_type_only"

    # -- strong-token（Def 5）: メタ文字・フラグ拒否 + 存在検証 + argv 実行。
    # **argv 実行の確認は効果側の exec_mode で行う**（検証子の本体からは
    # 分からない）ので、ここでは 2 条件までを見て `strong-token` を返し、
    # 3 条件目は `analyze._grade_of` が効果を見て確かめる。
    if dash_reject and existence:
        return "strong-token", None
    if dash_reject and not existence:
        return "weak", "no_existence_check"
    if existence and not dash_reject and not transforms:
        return "weak", "no_dash_reject"
    strong_containment = containments & {
        "os.path.commonpath",
        "is_relative_to",
        "relative_to",
        "exact_allowlist",
    }
    prefix_only = "startswith" in containments and not strong_containment

    if has_symlink and (strong_containment or (prefix_only and _startswith_has_sep(fn))):
        return "strong-path", None
    if has_symlink and prefix_only:
        return "weak", "prefix_no_boundary"
    if has_symlink and not containments:
        return "weak", "no_containment"
    if has_lexical and (strong_containment or (prefix_only and _startswith_has_sep(fn))):
        return "weak", "no_symlink_resolution"
    if has_lexical and prefix_only:
        return "weak", "prefix_no_canon"
    if has_lexical and not containments:
        return "weak", "lexical_canon_only"
    if not transforms and prefix_only:
        return "weak", "prefix_no_canon"
    if not transforms and "exact_allowlist" in containments:
        # 完全一致 allowlist。等級は config atom 規則が決める（既定閉なら OP）。
        return "allowlist", None
    path_containment = containments & {
        "os.path.commonpath",
        "is_relative_to",
        "relative_to",
    }
    if path_containment and not transforms:
        # 包含述語はあるが正規化子が無い（パス領域）。
        return "weak", "no_symlink_resolution"
    absolute_only = "absolute" in shapes
    existence_only = "exists" in shapes
    if not transforms and not containments and (absolute_only or existence_only):
        # **F7 の形。** 絶対パスか存在かだけを見る検証子は木の外を止めない。
        # 絶対パス検査を先に採る（`/etc/passwd` は絶対かつ存在する）。
        return "weak", "absolute_only" if absolute_only else "existence_only"

    if "exact_allowlist" in containments and not transforms:
        # **完全一致 allowlist だけ。** 領域が決まらないので等級は付けず、
        # `req` の引き上げは config atom 規則（既定閉なら OP）に任せる。
        # ここでパス領域の理由を付けると A5 のような対で誤った weak 理由が出る。
        return "allowlist", None
    # **形状語彙の語が本体に出るだけでは検証子にしない。**
    # §6 F0a の 11 語は構文的な棚卸しの語彙であって、`split` や `Path()` は
    # 値の変換である。`repo.git.log(*args).split("\n")` を「等級 unknown の
    # 検証子」と読むと、検証が 1 つも無い脆弱側に等級が付き、両側の差が消える。
    del shapes
    return None, None


class SummaryCache:
    """関数サマリの記憶化。`(module, qualname)` で引く。

    サマリは記憶化により**文脈非依存**である。「同一の効果サイトが呼び出し文脈に
    よってゲート述語の真偽を変える」形は原理的に捉えられない（§2.6 の限界節）。
    該当形は `opaque(context)` として出力し、**決して clean にしない。**
    """

    def __init__(self, index: SourceIndex) -> None:
        self.index = index
        self._cache: dict[str, FuncSummary] = {}
        self._in_progress: set[str] = set()

    def get(self, fd: FuncDef, depth: int = 0) -> FuncSummary:
        if fd.key in self._cache:
            return self._cache[fd.key]
        if fd.key in self._in_progress:
            return FuncSummary(fd.key, notes=("recursion",))
        self._in_progress.add(fd.key)
        try:
            summary = self._summarize(fd, depth)
        finally:
            self._in_progress.discard(fd.key)
        self._cache[fd.key] = summary
        return summary

    # -- 実装 -------------------------------------------------------------

    def _summarize(self, fd: FuncDef, depth: int) -> FuncSummary:
        path = self.index.resolve_module_path(fd.module)
        if path is None:
            return FuncSummary(fd.key, notes=("unresolved_module",))
        scope = self.index.function_scope(path, fd.node)
        decorators = _decorator_names(fd.node)
        is_cm = "contextmanager" in decorators or "asynccontextmanager" in decorators
        shapes, _ = _shapes_in(fd.node, scope)
        transforms = _transform_names(fd.node, scope)
        containments = _containment_forms(fd.node, scope)
        atoms = self._atom_names(fd.node, path)
        first_token = _is_first_token_check(fd.node, scope)
        statement_type = _is_statement_type_check(fd.node, scope)
        checked = _checked_params(fd.node, scope)
        raises = self._raises_on_deny(fd, path, scope, is_cm, depth)
        grade, weak_reason = _value_grade(
            transforms, containments, shapes, fd.node, first_token, statement_type
        )
        tree = self.index.parse(path)
        atom: Optional[ConfigAtom] = None
        if tree is not None:
            for a in sorted(atoms):
                atom = resolve_atom(a, tree)
                if atom is not None:
                    break
        return FuncSummary(
            key=fd.key,
            raises_on_deny=raises,
            is_contextmanager=is_cm,
            value_grade=grade,
            weak_reason=weak_reason,
            shapes=frozenset(shapes),
            atom_names=frozenset(atoms),
            atom=atom,
            membership_sets=frozenset(atoms),
            checked_params=checked,
        )

    def _atom_names(self, fn: ast.AST, path: str) -> set[str]:
        tree = self.index.parse(path)
        if tree is None:
            return set()
        consts = set(module_constants(tree))
        used: set[str] = set()
        for node in ast.walk(fn):
            if isinstance(node, ast.Name) and node.id in consts:
                used.add(node.id)
        return used

    def _raises_on_deny(
        self, fd: FuncDef, path: str, scope: Scope, is_cm: bool, depth: int
    ) -> Optional[bool]:
        """A-b のゲート要約: 拒否側の出口がすべて raise / exit か。

        CM の場合は「`yield` より前の拒否経路の出口がすべて raise / exit」を見る。
        **判定できなければ None を返す**（False に倒すと誤 clear になる）。
        """
        if not _has_raise_or_exit(fd.node):
            # 送出も終了もしない関数は、呼ぶだけでは絶対にゲートしない。
            # **ここを None にすると `confirm` のような真偽形が全部 OPAQUE になる。**
            return False
        if depth >= GATE_SUMMARY_DEPTH:
            return None
        cfg = build_cfg(fd.node)
        dom = compute_dominators(cfg)
        yield_nodes = _yield_nodes(cfg) if is_cm else set()
        inner = list(find_gate_candidates(cfg, scope, self.index, depth + 1, self))
        if not inner:
            return None
        decided = False
        for cand in inner:
            if cand.recognition in ("opaque",):
                return None
            deny = deny_successors(cfg, cand.node, cand.raises_form)
            if not deny:
                continue
            blocked = frozenset({cand.node})
            escapes = False
            for s in deny:
                reach = cfg.reachable_from(s, blocked)
                if cfg.exit in reach:
                    escapes = True
                if yield_nodes & reach:
                    escapes = True
            if not escapes:
                decided = True
        del dom
        return True if decided else False

def _yield_nodes(cfg: CFG) -> set[int]:
    out: set[int] = set()
    for nid, node in cfg.nodes.items():
        if node.ast_node is None:
            continue
        for sub in ast.walk(node.ast_node):
            if isinstance(sub, (ast.Yield, ast.YieldFrom)):
                out.add(nid)
                break
    return out


def _has_raise_or_exit(fn: ast.AST) -> bool:
    """本体に `raise` またはプロセス終了呼び出しがあるか。"""
    from .cfgbuild import _is_process_exit

    for node in ast.walk(fn):
        if isinstance(node, ast.Raise):
            return True
        if isinstance(node, ast.Expr) and _is_process_exit(node):
            return True
    return False


# --------------------------------------------------------------------------
# ゲート候補
# --------------------------------------------------------------------------


@dataclass
class GateCandidate:
    """CFG 上の 1 つのゲート候補。"""

    node: int
    #: ``approval``（req_occ 側）か ``value``（req_val 側）か。
    form: str
    #: ``A-a`` / ``A-b`` / ``A-c`` / ``V`` / ``opaque`` / ``not_a_gate``
    recognition: str
    name: str
    expr: Optional[ast.AST] = None
    subjects: frozenset[str] = frozenset()
    grade: Optional[Req] = None
    value_grade: Optional[str] = None
    weak_reason: Optional[str] = None
    downgrade: Optional[str] = None
    atom: Optional[ConfigAtom] = None
    opaque_reason: Optional[str] = None
    raises_form: bool = False
    witness_node: Optional[int] = None
    #: 述語のオペランドが由来する MODEL 導入点（`Value.roots`）。
    #: **位置引数の並びを崩さないよう必ず末尾に置く。**
    subject_roots: frozenset[str] = frozenset()
    #: 述語のオペランドの式そのもの。`arguments["branch_name"]` のような
    #: 添字式から root を精緻化するために要る（名前だけだと `arguments` に潰れ、
    #: 別の引数への検証が同じ root に見えてしまう）。
    subject_exprs: tuple = ()

    def to_json(self) -> dict:
        d = {
            "node": self.node,
            "form": self.form,
            "recognition": self.recognition,
            "name": self.name,
            "subjects": sorted(self.subjects),
        }
        if self.grade is not None:
            d["grade"] = self.grade.name
        if self.value_grade:
            d["value_grade"] = self.value_grade
        if self.weak_reason:
            d["weak_reason"] = self.weak_reason
        if self.downgrade:
            d["downgrade"] = self.downgrade
        if self.atom is not None:
            d["atom"] = self.atom.to_json()
        if self.opaque_reason:
            d["opaque_reason"] = self.opaque_reason
        return d


def _calls_in(node_ast: Optional[ast.AST]) -> list[ast.Call]:
    if node_ast is None:
        return []
    if isinstance(node_ast, ast.Call):
        return [node_ast] + [c for c in ast.walk(node_ast) if isinstance(c, ast.Call) and c is not node_ast]
    return [c for c in ast.walk(node_ast) if isinstance(c, ast.Call)]


def find_gate_candidates(
    cfg: CFG,
    scope: Scope,
    index: SourceIndex,
    depth: int = 0,
    summaries: Optional[SummaryCache] = None,
) -> list[GateCandidate]:
    """CFG 上のゲート候補を列挙する（支配判定はまだ行わない）。"""
    summaries = summaries or SummaryCache(index)
    tree = index.parse(index.resolve_module_path(scope.module) or "") if scope.module else None
    out: list[GateCandidate] = []
    # `x = gate(...)` → 後で `if x:` に使われる形（A-c）を拾うための表。
    assigned_gate: dict[str, GateCandidate] = {}

    for nid in sorted(cfg.nodes):
        node = cfg.nodes[nid]
        subject_expr = node.test_expr if node.kind == "test" else node.ast_node
        if subject_expr is None:
            continue

        # 1) 会員判定（allowlist / denylist）
        if node.kind == "test" and isinstance(subject_expr, ast.Compare):
            cand = _membership_candidate(nid, subject_expr, tree, scope, index)
            if cand is not None:
                out.append(cand)
                continue

        # 2) 呼び出し形
        for call in _calls_in(subject_expr):
            cand = _call_candidate(nid, node.kind, call, scope, index, summaries, depth, tree)
            if cand is None:
                continue
            if node.kind == "test":
                out.append(cand)
            else:
                target = _assign_target(node.ast_node, call)
                if target is not None:
                    assigned_gate[target] = cand
                out.append(cand)

    # A-c: 代入された戻り値が test で使われている場合、ゲート節点を test へ移す。
    if assigned_gate:
        for nid in sorted(cfg.nodes):
            node = cfg.nodes[nid]
            if node.kind != "test" or node.test_expr is None:
                continue
            used = subject_names(node.test_expr)
            for name, cand in assigned_gate.items():
                if name in used:
                    out.append(
                        GateCandidate(
                            node=nid,
                            form=cand.form,
                            recognition="A-c" if cand.form == "approval" else "V",
                            name=cand.name,
                            expr=node.test_expr,
                            subjects=cand.subjects,
                            grade=cand.grade,
                            value_grade=cand.value_grade,
                            weak_reason=cand.weak_reason,
                            atom=cand.atom,
                            witness_node=cand.node,
                        )
                    )
    return out


def _assign_target(stmt: Optional[ast.AST], call: ast.Call) -> Optional[str]:
    if isinstance(stmt, ast.Assign) and stmt.value is call:
        for t in stmt.targets:
            if isinstance(t, ast.Name):
                return t.id
    if isinstance(stmt, ast.AnnAssign) and stmt.value is call and isinstance(stmt.target, ast.Name):
        return stmt.target.id
    return None


def _membership_candidate(
    nid: int,
    cmp_node: ast.Compare,
    tree,
    scope: Optional[Scope] = None,
    index: Optional[SourceIndex] = None,
) -> Optional[GateCandidate]:
    """`x in S` / `x not in S` の allowlist ゲート。

    等級は config atom 規則に従い、**既定閉なら OP、既定開なら MODEL のまま**。
    """
    if not cmp_node.ops or not isinstance(cmp_node.ops[0], (ast.In, ast.NotIn)):
        return None
    container = cmp_node.comparators[0]
    atom: Optional[ConfigAtom] = None
    inline_literal = False
    if isinstance(container, (ast.Name, ast.Attribute)):
        cname = container.id if isinstance(container, ast.Name) else (dotted_of(container) or "")
        atom = resolve_atom_via_scope(cname, tree, scope, index) if cname else None
    else:
        # **インラインのリテラル集合は config atom ではない**（Def 5 の 4 源:
        # コンストラクタ kwarg / モジュール定数 / os.environ / CLI 既定値）。
        # ここを atom と見なすと、低レベル MCP の `if name in ("a","b"):` という
        # **ディスパッチそのもの**が「運用者 allowlist」として req_occ を
        # 引き上げてしまい、すべての低レベルサーバが clear される。
        inline_literal = True
    grade = Req.OP if (atom is not None and atom.default_closed) else REQ_BOTTOM
    downgrade = None
    if atom is not None and atom.default_closed is None:
        downgrade = "opaque"
    elif atom is not None and atom.default_closed is False:
        downgrade = "config_conditional"
    return GateCandidate(
        node=nid,
        form="value",
        recognition="V",
        name=dotted_of(container) or ("<inline_literal>" if inline_literal else "<literal>"),
        expr=cmp_node,
        subjects=subject_names(cmp_node.left),
        subject_exprs=(cmp_node.left,),
        grade=grade,
        value_grade="allowlist",
        downgrade=downgrade,
        atom=atom,
    )


def _call_candidate(
    nid: int,
    node_kind: str,
    call: ast.Call,
    scope: Scope,
    index: SourceIndex,
    summaries: SummaryCache,
    depth: int,
    tree,
) -> Optional[GateCandidate]:
    name = dotted_of(call.func)
    if name is None:
        return None
    last = name.split(".")[-1]
    subjects = frozenset().union(*(subject_names(a) for a in call.args)) if call.args else frozenset()

    is_approval_name = last in APPROVAL_NAMES
    fds = index.lookup_function(last)
    if len(fds) > 1:
        # 受け手つき（`gw.require_approval`）ならメソッド、裸名ならモジュール関数。
        # **同名メソッドを無条件に 1 つ採らない**（前身 `find_method` の欠陥）。
        want_method = isinstance(call.func, ast.Attribute)
        narrowed = [f for f in fds if (f.classname is not None) == want_method]
        fds = narrowed or fds
    if len(fds) > 1:
        fds = [f for f in fds if f.qualname == last] or fds
    summary = summaries.get(fds[0], depth) if len(fds) == 1 else None

    if is_approval_name:
        # §2.5.3 の認識順。**A-c を最初に見る。**
        # 「戻り値が分岐条件として使われる」ことは呼び出し先の中身を知らなくても
        # 決まるので、ここで raises_on_deny の判定不能を持ち込んではならない
        # （持ち込むと `confirm` のような真偽形が全部 OPAQUE になる）。
        if node_kind == "test":
            return GateCandidate(nid, "approval", "A-c", name, call, subjects, Req.USER)
        if summary is not None and summary.raises_on_deny is True:
            return GateCandidate(nid, "approval", "A-b", name, call, subjects, Req.USER, raises_form=True)
        if summary is not None and summary.raises_on_deny is False:
            # 解決できて「呼ぶだけでは拒否できない」と分かった。**OPAQUE にしない。**
            return GateCandidate(nid, "approval", "not_a_gate", name, call, subjects, None)
        if last in RAISES_FORM_NAMES:
            return GateCandidate(nid, "approval", "A-a", name, call, subjects, Req.USER, raises_form=True)
        # 名前だけ一致し呼び出し先が木内で解決できない。**推定で A にしない。**
        return GateCandidate(
            nid, "approval", "opaque", name, call, subjects, None, opaque_reason="gate_name_only"
        )

    # 値検証: 木内の検証子か、カタログ形状の直接呼び出し。
    if summary is not None and summary.value_grade:
        subj, exprs = _subjects_for_checked(call, fds[0] if fds else None, summary, subjects)
        cand = _value_candidate(
            nid, name, call, subj, summary.value_grade, summary.weak_reason, summary, tree
        )
        cand.subject_exprs = exprs
        return cand
    dotted = resolve_call_name(call.func, scope)
    shape = V.shape_for_dotted(dotted) if dotted else None
    if shape is None and isinstance(call.func, ast.Attribute):
        shape = V.shape_for_method(call.func.attr)
        if shape is not None:
            subjects = subjects | subject_names(call.func.value)
    if shape is not None and shape in PREDICATE_SHAPES:
        # **inline 形は単一形状からしか等級を出さない（weak 止まり）。**
        # D21 は囲み関数の本体全体を helper と同じ規則で採点する `_grade_inline`
        # を入れたが、CFG も支配も主語も適用順序も見ない袋詰め採点なので、
        # ログ用の realpath 1 行や死に分岐の検査が別の述語に strong-path を貸し、
        # false-clean を 25 形入れた（`tests/test_d21_adversarial.py`、D25）。
        # Def 5 を inline で満たす形が weak に留まる誤り（false-dirty、安全側）は
        # `docs/open_questions.md` O8 に未解決として残す。
        grade, weak = _grade_from_shape(shape)
        cand = _value_candidate(nid, name, call, subjects, grade, weak, None, tree)
        cand.subject_exprs = tuple(call.args) + (
            (call.func.value,) if isinstance(call.func, ast.Attribute) else ()
        )
        return cand
    return None


def _subjects_for_checked(
    call: ast.Call, fd, summary: FuncSummary, fallback: frozenset[str]
) -> tuple[frozenset[str], tuple]:
    """呼び出し先が実際に検証している仮引数に対応する**実引数**の名前だけを返す。

    これが無いと `git_diff(repo, arguments["target"])` の dash 検査が、
    `repo` 経由で `cwd` 位置にも等級を付けてしまう。
    """
    if fd is None or not summary.checked_params:
        return fallback, tuple(call.args)
    args = getattr(fd.node, "args", None)
    if args is None:
        return fallback, tuple(call.args)
    formals = [a.arg for a in list(args.posonlyargs) + list(args.args)]
    if fd.classname is not None and formals and formals[0] in ("self", "cls"):
        formals = formals[1:]
    out: set[str] = set()
    exprs: list = []
    for i, formal in enumerate(formals):
        if formal not in summary.checked_params:
            continue
        if i < len(call.args):
            out |= subject_names(call.args[i])
            exprs.append(call.args[i])
    for kw in call.keywords:
        if kw.arg in summary.checked_params:
            out |= subject_names(kw.value)
            exprs.append(kw.value)
    return (frozenset(out) if out else frozenset({"<no-checked-arg>"})), tuple(exprs)


#: 単独で「ゲート候補」になりうる形状。
#:
#: §6 F0a の 11 語は**構文的な棚卸しの語彙**であって、全部がゲートではない。
#: 正規化子（`realpath` / `lexical_canon`）とトークン化（`shlex_*` / `split` /
#: `ctor_path` / `urlparse`）は**値の変換**であり、val が属性と alias 事実として
#: 記録する。それらが等級になるのは、検証子関数の本体をまとめて採点したとき
#: （`FuncSummary.value_grade`）だけである。
#:
#: これを分けないと `Path(arguments["repo_path"])` が「検証」に化け、
#: 検証が 1 つも無い脆弱側に `unknown` の等級が付く（F7 の
#: 「`Path()` は正規化ではない」と同じ論点）。
PREDICATE_SHAPES: frozenset[str] = frozenset({"containment", "prefix", "exists"})


def _grade_from_shape(shape: str) -> tuple[str, Optional[str]]:
    """単一形状だけから決まる等級。**単独で strong にはしない。**

    inline 形（ツール本体に直接書かれた述語）の等級はここでしか決まらない。
    strong-path に上げるには Def 5 の (i)(ii)(iii) と root-equal を**当該述語と
    sink に届く値について**確かめる必要があり、それは未実装（O8）。
    """
    if shape == "prefix":
        return "weak", "prefix_no_canon"
    if shape == "lexical_canon":
        return "weak", "lexical_canon_only"
    if shape == "realpath":
        return "weak", "no_containment"
    if shape == "containment":
        return "weak", "no_symlink_resolution"
    if shape == "exists":
        return "unknown", None
    return "unknown", None


def _value_candidate(
    nid: int,
    name: str,
    call: ast.Call,
    subjects: frozenset[str],
    value_grade: Optional[str],
    weak_reason: Optional[str],
    summary: Optional[FuncSummary],
    tree,
) -> GateCandidate:
    atom: Optional[ConfigAtom] = summary.atom if summary is not None else None
    del tree
    if value_grade and value_grade.startswith("strong"):
        grade = Req.OP
    elif value_grade == "allowlist":
        grade = Req.OP if (atom is not None and atom.default_closed) else REQ_BOTTOM
    else:
        grade = REQ_BOTTOM
    downgrade = None
    if atom is not None and atom.default_closed is False:
        downgrade = "config_conditional"
    return GateCandidate(
        node=nid,
        form="value",
        recognition="V",
        name=name,
        expr=call,
        subjects=subjects,
        grade=grade,
        value_grade=value_grade,
        weak_reason=weak_reason,
        downgrade=downgrade,
        atom=atom,
    )


# --------------------------------------------------------------------------
# 変異点の継ぎ目
#
# 実装変異試験（§2.5.6）が突く 2 つの判断をここに切り出す。関数にしてあるのは
# 変異試験が差し替えられるようにするためであって、呼び出し側で分岐を書き換えて
# 同じことをしてはならない（差し替え点が 1 か所であることが試験の前提）。
# --------------------------------------------------------------------------


def subject_ok(cand: GateCandidate, subjects: frozenset[str]) -> bool:
    """主語一致（§2.5.3。**V にのみ課す**）。

    ゲートしていても、述語のオペランドが当該効果の当該制御位置の値、または
    前向き def-use でその値から導かれる値でなければ `req` を引き上げない。
    承認は位置ではなく効果の発生に対する承認なので A には課さない。

    照合は **root 集合を優先**する（`Value.roots` = MODEL 導入点の集合）。
    root は名前の書き換え（`safe = validate_path(path)`）を跨いで保たれるので、
    AST 名の一致より正確である。root が無いときだけ名前一致に落ちる。
    """
    if cand.form != "value" or not subjects:
        return True
    if cand.subject_roots:
        return bool(cand.subject_roots & subjects)
    return bool(cand.subjects & subjects)


def opaque_beats_no_gate() -> bool:
    """解決できていない経路を `NODOM(no_gate)` に潰さないこと。

    潰すと前身の幻の TP（判定不能をガード不在と読む）と G13 の誤 clean が
    再生産される。**`True` を返すことが仕様である。**
    """
    return True


# --------------------------------------------------------------------------
# 採点
# --------------------------------------------------------------------------


@dataclass
class GateScore:
    """1 つの効果に対するゲート採点の結果。"""

    result: DomResult
    req: Req
    candidates: list[GateCandidate] = field(default_factory=list)
    #: `gates(g,d)` を通ったゲート。
    passing: list[GateCandidate] = field(default_factory=list)
    #: 各複製ごとの結果（`finally` 複製の ⊓ を追えるようにするため）。
    per_copy: list[tuple[int, str]] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_json(self) -> dict:
        return {
            "gate": self.result.to_json(),
            "req": self.req.name,
            "candidates": [c.to_json() for c in self.candidates],
            "passing": [c.node for c in self.passing],
            "per_copy": [{"node": n, "status": s} for n, s in self.per_copy],
            "notes": sorted(set(self.notes)),
        }


#: NODOM 理由の情報量の順（強いほど先に採る）。
_NODOM_PRIORITY = {
    "deny_reaches_effect": 3,
    "non_binding_gate": 2,
    "alt_entry": 1,
    "no_gate": 0,
}


def score_gates(
    cfg: CFG,
    dom: DomTree,
    candidates: list[GateCandidate],
    effect_nodes: list[int],
    coordinate: str,
    subjects: frozenset[str] = frozenset(),
    path_opaque: tuple[str, ...] = (),
    alt_entry: bool = False,
    opaque_witness: Optional[str] = None,
    alt_entry_witness: Optional[str] = None,
) -> GateScore:
    """効果に対する 3 値の verdict と `req` を計算する。

    :param coordinate: ``"occ"``（`req_occ`）か ``"val"``（`req_val`）。
    :param subjects: `req_val` のときの当該制御位置の値に対応する名前集合
        （前向き def-use での派生を含む）。**`req_occ` のときはセレクタの名前。**
    :param path_opaque: 連結経路の解決で立った OPAQUE 理由（`dynamic_registry` など）。
    :param alt_entry: 同一の効果本体に、ゲートを持つ別のユニット入口が在るか。
    :param opaque_witness: 解決に失敗した箇所の witness（`L15` など）。
        **OPAQUE 行にも witness を付ける** — 「どこで解けなかったか」が
        報告価値の中身だからである。
    :param alt_entry_witness: 別入口に在るゲートの witness。
        「ゲートは在るが、この入口からは通らない」ことを示す。
    """
    relevant = [c for c in candidates if _is_relevant(c, coordinate, subjects)]
    passing: list[GateCandidate] = []
    failures: list[tuple[str, GateCandidate, Optional[int]]] = []
    opaque_reasons: list[str] = list(path_opaque)

    for cand in relevant:
        # (1) 主語一致 → (2) ゲート認識 → (3) 支配（§2.5.3 の評価順）
        if not subject_ok(cand, subjects):
            failures.append(("non_binding_gate", cand, None))
            continue
        if cand.recognition == "opaque":
            if cand.opaque_reason:
                opaque_reasons.append(cand.opaque_reason)
            continue
        if cand.recognition == "not_a_gate":
            failures.append(("no_gate", cand, None))
            continue
        ok_all = True
        witness_deny: Optional[int] = None
        for d in effect_nodes:
            chk = gates(cfg, dom, cand.node, d, cand.raises_form)
            if not chk.ok:
                ok_all = False
                witness_deny = chk.escaping_deny
                failures.append((chk.reason or "no_gate", cand, chk.escaping_deny))
                break
        if ok_all:
            passing.append(cand)
        del witness_deny

    req = req_join(*(c.grade or REQ_BOTTOM for c in passing)) if passing else REQ_BOTTOM
    per_copy = [(n, "gated" if passing else "ungated") for n in effect_nodes]

    if passing and req > REQ_BOTTOM:
        witness_node = passing[0].witness_node or passing[0].node
        best = max(passing, key=lambda c: (c.grade or REQ_BOTTOM))
        witness_node = best.witness_node or best.node
        result = DomResult(
            DomKind.DOM,
            None,
            req,
            cfg.nodes[witness_node].witness(),
        )
        return GateScore(result, req, relevant, passing, per_copy)

    if alt_entry:
        return GateScore(
            DomResult(DomKind.NODOM, "alt_entry", None, alt_entry_witness),
            REQ_BOTTOM,
            relevant,
            passing,
            per_copy,
        )

    # 明確な失敗（deny_reaches_effect / non_binding_gate）は OPAQUE より優先する。
    positive_failures = [f for f in failures if f[0] in ("deny_reaches_effect", "non_binding_gate")]
    if positive_failures:
        reason, cand, deny = max(positive_failures, key=lambda f: _NODOM_PRIORITY[f[0]])
        wnode = cand.witness_node or cand.node
        return GateScore(
            DomResult(DomKind.NODOM, reason, None, cfg.nodes[wnode].witness()),
            REQ_BOTTOM,
            relevant,
            passing,
            per_copy,
            notes=[f"escaping_deny={deny}"] if deny is not None else [],
        )

    # 経路が解決できていないなら OPAQUE。**no_gate に潰さない**
    # （潰すと前身の幻の TP と G13 の誤 clean が再生産される）。
    if opaque_reasons and opaque_beats_no_gate():
        return GateScore(
            DomResult(DomKind.OPAQUE, sorted(set(opaque_reasons))[0], None, opaque_witness),
            REQ_BOTTOM,
            relevant,
            passing,
            per_copy,
        )

    if failures:
        reason, cand, _deny = max(failures, key=lambda f: _NODOM_PRIORITY.get(f[0], 0))
        wnode = cand.witness_node or cand.node
        return GateScore(
            DomResult(DomKind.NODOM, reason, None, cfg.nodes[wnode].witness()),
            REQ_BOTTOM,
            relevant,
            passing,
            per_copy,
        )
    return GateScore(DomResult(DomKind.NODOM, "no_gate"), REQ_BOTTOM, relevant, passing, per_copy)


def _is_relevant(c: GateCandidate, coordinate: str, subjects: frozenset[str] = frozenset()) -> bool:
    """座標ごとに見るゲートを分ける（Def 5 の `req_occ` / `req_val` 分割）。

    **1 つにまとめてはならない。** まとめると、無関係な引数への強い検証が
    ツール全体の SELECT 判定を消す（型エラー）。

    `req_occ` に入る allowlist は「**ディスパッチキー（セレクタ）そのものを
    主語とする**もの」に限る。セレクタが特定できない（`subjects` が空の）
    ユニットでは allowlist を `req_occ` に数えない — 数えると値位置への
    allowlist がツール全体の SELECT 判定を消す。
    """
    if coordinate == "occ":
        if c.form == "approval":
            return True
        return c.value_grade == "allowlist" and bool(subjects)
    # req_val: 承認割り込み ∪（位置 p の値検証）
    return True


# --------------------------------------------------------------------------
# §2.5.5 の不動点（直接計算との一致をテストで確認するために残す）
# --------------------------------------------------------------------------


def req_by_fixpoint(
    cfg: CFG,
    dom: DomTree,
    passing: list[GateCandidate],
    effect_nodes: list[int],
) -> Req:
    """§2.5.5 の前向きデータフローの最小不動点で `req(e)` を計算する。

        in[n]  = ⊓_{p ∈ pred(n)} out[p]          （ENTRY では bottom = MODEL）
        out[n] = in[n] ⊔ ( grade(n) if gates(n, e) else bottom )
        req(e) = ⊓_{c ∈ Copies(e)} in[c]

    **MFP = MOP の根拠**: P^op は鎖なので分配束であり、遷移関数が
    ``λx. x ⊔ k`` の形で ⊓ 上に分配する。

    :func:`score_gates` は同値な直接計算（⊔ over passing gates）を使う。
    両者が一致することを `tests/test_gate_fixpoint.py` が確認する。
    """
    grade_at: dict[int, Req] = {}
    for c in passing:
        grade_at[c.node] = req_join(grade_at.get(c.node, REQ_BOTTOM), c.grade or REQ_BOTTOM)

    nodes = [n for n in cfg.nodes if dom.is_reachable(n)]
    in_: dict[int, Req] = {n: Req.USER for n in nodes}
    out: dict[int, Req] = {n: Req.USER for n in nodes}
    in_[cfg.entry] = REQ_BOTTOM
    out[cfg.entry] = req_join(REQ_BOTTOM, grade_at.get(cfg.entry, REQ_BOTTOM))

    changed = True
    while changed:
        changed = False
        for n in nodes:
            if n == cfg.entry:
                continue
            preds = [p for p, _k in cfg.pred.get(n, ()) if p in out]
            new_in = req_meet(*(out[p] for p in preds)) if preds else Req.USER
            new_out = req_join(new_in, grade_at.get(n, REQ_BOTTOM))
            if new_in != in_[n] or new_out != out[n]:
                in_[n], out[n] = new_in, new_out
                changed = True

    copies = [c for c in effect_nodes if c in in_]
    return req_meet(*(in_[c] for c in copies)) if copies else REQ_BOTTOM
