"""§2.5.2: 支配計算と「ゲートする」の定義。

**支配だけではゲートにならない。** 支配は「ゲートが評価されること」しか言わず
「拒否されたときに効果へ行かないこと」を言わない。監査 finding E が前身について
指摘したのはまさにこの取り違えであり、同じ取り違えを再生産しないために次の連言を
「ゲートする」の定義とする:

    ゲート `g` が効果 `d` を**ゲートする** ⇔
      (G-i)  `g` が `d` を支配する、かつ
      (G-ii) `g` の拒否後継 `deny(g)` のどれからも、`g` を通らずに `d` へ到達できない。
             形式的には `CFG∖{g}` において、すべての `s ∈ deny(g)` について
             `d ∉ Reach_{CFG∖{g}}(s)`。

**`CFG∖{g}` の除去は必須である。** 除去しないと G10（ループ内 `continue` の
allowlist）で `continue → header →（次の反復）→ 効果` が拒否辺からの到達路に見え、
正しいループ allowlist を誤って NODOM にする。

**後支配は使わない。** §2.5.1 で `finally` を脱出種別ごとに複製しているので
G12 は複製の ⊓ から構造的に出る。後支配版を (G-ii) の代わりに使うと
G6（except が承認例外を握り潰す）と G9（`contextlib.suppress` が吸収する）を
`DOM` と誤採点する — 本設計が潰すために存在する誤 clear の方向そのものである。

支配木は Cooper, Harvey, Kennedy, *A Simple, Fast Dominance Algorithm*,
Rice University CS TR-06-33870, 2006 (hdl:1911/96345) の反復 idom アルゴリズム。
**採用理由は実装量とテスト量のみである。速度の優劣は主張しない。**
反証条件: T3 の実行で支配計算が 1 ツールあたり中央値 0.5 秒を超えたら SNCA へ差し替える。
"""

from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import Optional

from .cfgbuild import CFG, Node

# --------------------------------------------------------------------------
# 支配木（Cooper–Harvey–Kennedy）
# --------------------------------------------------------------------------


def reverse_postorder(cfg: CFG, start: Optional[int] = None) -> list[int]:
    """ENTRY からの逆後行順。到達不能ノードは含まない。"""
    root = cfg.entry if start is None else start
    order: list[int] = []
    seen: set[int] = set()

    # 再帰を避けた明示スタックの後行順（決定論のため後継はソート順に積む）。
    stack: list[tuple[int, bool]] = [(root, False)]
    while stack:
        n, expanded = stack.pop()
        if expanded:
            order.append(n)
            continue
        if n in seen:
            continue
        seen.add(n)
        stack.append((n, True))
        for b in sorted({b for b, _k in cfg.succ.get(n, ())}, reverse=True):
            if b not in seen:
                stack.append((b, False))
    order.reverse()
    return order


@dataclass
class DomTree:
    """支配木。`idom[n]` は n の直接支配節点。root は自分自身。"""

    root: int
    idom: dict[int, int]
    rpo_index: dict[int, int]

    def dominates(self, a: int, b: int) -> bool:
        """a が b を支配するか（a == b も真）。到達不能な b は偽。"""
        if a == b:
            return True
        cur = b
        while cur in self.idom and self.idom[cur] != cur:
            cur = self.idom[cur]
            if cur == a:
                return True
        return False

    def is_reachable(self, n: int) -> bool:
        return n in self.rpo_index


def compute_dominators(cfg: CFG) -> DomTree:
    """CHK の反復アルゴリズムで支配木を作る。"""
    rpo = reverse_postorder(cfg)
    rpo_index = {n: i for i, n in enumerate(rpo)}
    root = cfg.entry
    idom: dict[int, int] = {root: root}

    def intersect(a: int, b: int) -> int:
        while a != b:
            while rpo_index[a] > rpo_index[b]:
                a = idom[a]
            while rpo_index[b] > rpo_index[a]:
                b = idom[b]
        return a

    changed = True
    while changed:
        changed = False
        for n in rpo:
            if n == root:
                continue
            preds = [p for p, _k in cfg.pred.get(n, ()) if p in rpo_index and p in idom]
            if not preds:
                continue
            new_idom = preds[0]
            for p in preds[1:]:
                new_idom = intersect(p, new_idom)
            if idom.get(n) != new_idom:
                idom[n] = new_idom
                changed = True
    return DomTree(root, idom, rpo_index)


# --------------------------------------------------------------------------
# §2.5.3: ゲート述語のセンス（拒否後継の決め方）
# --------------------------------------------------------------------------

#: 真になったら拒否を意味する述語名（否定センス）。
DENY_SENSE_NAMES: frozenset[str] = frozenset(
    {
        "is_denied",
        "is_blocked",
        "is_forbidden",
        "is_dangerous",
        "is_unsafe",
        "is_disallowed",
        "denied",
        "blocked",
        "forbidden",
    }
)


def test_sense(expr: Optional[ast.AST]) -> str:
    """test 式のセンス。``"positive"``（真 = 許可）か ``"negative"``（真 = 拒否）。

    CFG 構築で `not` は既に脱糖されているので、ここで見るのは式そのものの形だけ。

    規則（**述語の意味から決める。構造からは決めない**）:

    * `==` / `in` / `is`         → positive（真 = 許可）
    * `!=` / `not in` / `is not` → negative（真 = 拒否）
    * 呼び出し先が :data:`DENY_SENSE_NAMES` → negative
    * それ以外 → positive

    **「raise へ行く方が deny」という構造的な規則にしてはならない。** それだと
    (G-ii) が自明に成立し、mutant 8（ガード偽側の分岐に効果がある形）を
    誤って DOM と採点する。センスは述語の意味から決め、構造はその後で検査する。

    等号系を規則に入れているのは、`os.path.commonpath([real, base]) != base` の
    ような包含述語の否定形（G5）が実データの主要形だからである。
    """
    if expr is None:
        return "positive"
    if isinstance(expr, ast.Compare) and expr.ops:
        op = expr.ops[0]
        if isinstance(op, (ast.NotIn, ast.NotEq, ast.IsNot)):
            return "negative"
        if isinstance(op, (ast.In, ast.Eq, ast.Is)):
            return "positive"
    if isinstance(expr, ast.Call):
        name = _callee_name(expr.func)
        if name and name.split(".")[-1] in DENY_SENSE_NAMES:
            return "negative"
    if isinstance(expr, ast.Name) and expr.id in DENY_SENSE_NAMES:
        return "negative"
    if isinstance(expr, ast.Attribute) and expr.attr in DENY_SENSE_NAMES:
        return "negative"
    return "positive"


def _callee_name(func: ast.AST) -> Optional[str]:
    parts: list[str] = []
    cur = func
    while True:
        if isinstance(cur, ast.Attribute):
            parts.append(cur.attr)
            cur = cur.value
        elif isinstance(cur, ast.Name):
            parts.append(cur.id)
            break
        else:
            return None
    return ".".join(reversed(parts))


# --------------------------------------------------------------------------
# deny(g)
# --------------------------------------------------------------------------


def deny_successors(cfg: CFG, g: int, raises_form: bool = False) -> set[int]:
    """`deny(g)` を計算する（§2.5.2）。

    * 述語形: 肯定センスなら false 辺の後継、否定センスなら true 辺の後継。
    * 送出形（A-a / A-b、`ENTER(cm)` を含む）: そのノードから出るすべての例外辺の後継。
    * 両方持つ場合は和集合。

    :param raises_form: A-a / A-b で「呼ぶと拒否時に送出する」と分かっているとき真。
    """
    node = cfg.nodes[g]
    out: set[int] = set()
    if node.kind == "test":
        sense = test_sense(node.test_expr)
        label = "false" if sense == "positive" else "true"
        out |= set(cfg.successors(g, (label,)))
    if raises_form or node.kind in ("enter_cm", "stmt", "handler"):
        out |= set(cfg.successors(g, ("exc",)))
    return out


# --------------------------------------------------------------------------
# gates(g, d)
# --------------------------------------------------------------------------


@dataclass
class GateCheck:
    """`gates(g, d)` の結果と、そうでない場合の理由。"""

    ok: bool
    #: 不成立の理由（NODOM 語彙）。成立時は None。
    reason: Optional[str] = None
    #: (G-ii) を破った拒否後継（witness）。
    escaping_deny: Optional[int] = None


def gates(cfg: CFG, dom: DomTree, g: int, d: int, raises_form: bool = False) -> GateCheck:
    """`(G-i) ∧ (G-ii)` を判定する。

    (G-i) が成立し (G-ii) が成立しないゲートは ``NODOM(deny_reaches_effect)`` と
    して **witness 付きで manifest に残す**（「ゲートは在るが握り潰されている」は
    報告価値が最も高い行である）。
    """
    if not dom.is_reachable(d):
        return GateCheck(False, "no_gate")
    if g == d:
        # **同一 CFG ノードのゲートは支配しない。** 1 文の中には制御フローの
        # 順序が無いので、`return [f(x) for x in xs if ok(x)]` のような行で
        # 「同じ行にゲート語彙がある」ことを支配と読むのは、前身の AST 兄弟文
        # 方式そのものである。内包表記の `if` は §2.5.1 の別 CFG（subgraph）で
        # 採点する。
        return GateCheck(False, "no_gate")
    if not dom.dominates(g, d):
        return GateCheck(False, "no_gate")
    deny = deny_successors(cfg, g, raises_form)
    if not deny:
        # 支配はするが拒否側が無い = ゲートしていない。
        return GateCheck(False, "no_gate")
    blocked = frozenset({g})
    for s in sorted(deny):
        if d in cfg.reachable_from(s, blocked):
            return GateCheck(False, "deny_reaches_effect", s)
    return GateCheck(True)


# --------------------------------------------------------------------------
# 主語一致（§2.5.3。V にのみ課す）
# --------------------------------------------------------------------------


def subject_names(expr: Optional[ast.AST]) -> frozenset[str]:
    """述語のオペランドに現れる名前（`a.b.c` は `a` と `a.b.c` の両方）。"""
    if expr is None:
        return frozenset()
    names: set[str] = set()
    for node in ast.walk(expr):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            dotted = _callee_name(node)
            if dotted:
                names.add(dotted)
    return frozenset(names)


def subject_matches(pred_expr: Optional[ast.AST], value_names: frozenset[str]) -> bool:
    """述語のオペランドが当該制御位置の値（または前向き def-use での派生）か。

    **主語一致に失敗した述語は `NODOM(non_binding_gate)` に落ちる**
    （`OPAQUE(gate_name_only)` にはしない。主語不一致は呼び出し先本体を
    見なくても決まるから）。承認割り込み A には課さない。
    """
    if not value_names:
        return False
    return bool(subject_names(pred_expr) & value_names)


# --------------------------------------------------------------------------
# 効果ノードの複製（§2.5.1 の `finally` 複製）
# --------------------------------------------------------------------------


def effect_copies(cfg: CFG, lineno: int) -> list[int]:
    """効果行に対応する CFG ノード（`finally` 複製で複数になりうる）。

    **効果の verdict はその効果行の全複製について計算し ⊓（最弱）を採る。**
    """
    return sorted(cfg.nodes_for_line(lineno))


def node_witness(cfg: CFG, nid: int) -> str:
    n: Node = cfg.nodes[nid]
    return n.witness()
