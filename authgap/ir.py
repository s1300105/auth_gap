"""AuthGap の中間表現と束。

Def 1（主体ラベルと 2 つの束）と §2.6（val の値領域）の実装。

この module が守る規則（仕様書が名指しで禁じているもの）:

* **2 つの束は別物である。** `Prin`（ラベル束 P）と `Req`（要求束 P^op）は
  join 関数を共有しない。実装でも別クラスにし、相互変換を提供しない。
* **`Prin` に `UNKNOWN` を作らない。** 判定不能は `Prov` 側に一本化する。
* **`Prov` を clean に潰さない。** opaque は理由つきで伝播し、決して drop しない。
* **opaque の語彙は 2 系統ある。** val 側 8 語（値の解決に付く）とゲート側 8 語
  （支配の判定に付く）は別語彙で、同じ語が両方に現れても混ぜて集計しない。
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from typing import Any, Optional, Union

# --------------------------------------------------------------------------
# cap（§5.2。月 10 の解析指紋に含める。以後変更しない）
# --------------------------------------------------------------------------

#: 1 ユニットあたりのコンテナ / 文字列 / パスの要素上限。
#: `Seq.elems` / `Map.entries` / `Str.parts` / `Argv.elems` / `Path.segs` の 5 種すべてに適用する。
K = 16
#: 1 ユニットあたりの関数サマリ数の上限。
SUMMARY_CAP = 200
#: 1 ファイルあたりの AST ノード上限。
AST_NODE_CAP = 20000
#: 1 ファイルあたりの出力効果行の上限。
EFFECT_ROW_CAP = 200
#: 1 関数あたりの CFG ノード上限。
CFG_NODE_CAP = 2000
#: 1 ファイルあたりの壁時計上限（秒）。
WALL_CLOCK_CAP = 10.0
#: Def 4 の下向き呼び出し深さ。木内ユーザ定義の被呼び出しにのみ加算する。
MAX_DEPTH = 3


# --------------------------------------------------------------------------
# Def 1: ラベル束 P
# --------------------------------------------------------------------------


class Prin(enum.IntEnum):
    """ラベル束 P: ``USER ⊑ OP ⊑ MODEL``。結合は MODEL 方向への join。

    `trig` と `val` がこの束の値を取る。**`UNKNOWN` を追加してはならない**
    （判定不能は :class:`Prov` 側に一本化する）。
    """

    USER = 0
    OP = 1
    MODEL = 2

    def __str__(self) -> str:  # pragma: no cover - 表示のみ
        return self.name


def prin_join(*ps: Prin) -> Prin:
    """P 上の join（MODEL 方向）。空の join は最弱の USER。"""
    out = Prin.USER
    for p in ps:
        if p > out:
            out = p
    return out


# --------------------------------------------------------------------------
# Def 1: 要求束 P^op
# --------------------------------------------------------------------------


class Req(enum.IntEnum):
    """要求束 P^op: ``MODEL < OP < USER``。**ゲート無し = bottom = MODEL。**

    `req_occ` と `req_val` がこの束の値を取る。
    """

    MODEL = 0
    OP = 1
    USER = 2

    def __str__(self) -> str:  # pragma: no cover - 表示のみ
        return self.name


#: P^op の bottom。ゲートが 1 つも無い経路の要求主体。
REQ_BOTTOM = Req.MODEL


def req_join(*rs: Req) -> Req:
    """P^op 上の ⊔（1 本の経路の上では最強を採る。経路上のゲートは連言だから）。"""
    out = REQ_BOTTOM
    for r in rs:
        if r > out:
            out = r
    return out


def req_meet(*rs: Req) -> Req:
    """P^op 上の ⊓（経路の集合では最弱を採る。攻撃者が最弱経路を選ぶから）。

    引数が空のときは bottom を返す（到達経路が無い = ゲートされていない、
    ではなく「到達しない」なので呼び出し側で区別すること）。
    """
    if not rs:
        return REQ_BOTTOM
    out = Req.USER
    for r in rs:
        if r < out:
            out = r
    return out


# --------------------------------------------------------------------------
# Def 1: 確度 Prov（P と直積で持つ。P の第 4 の値にしない）
# --------------------------------------------------------------------------

#: val 側の opaque 語彙（§2.6。8 種）。値の解決に付く。
VAL_OPAQUE_REASONS = frozenset(
    {
        "depth",  # Def 4 の下向き深さ超過
        "unresolved",  # 木内で解決できない呼び出し
        "receiver",  # 受け手アクセスパスが深さ 2 を超える
        "recursion",  # 再帰
        "dynamic",  # 動的な属性 / 添字アクセス
        "cap",  # §5.2 の cap 到達
        "loop",  # 2 周固定点が安定しなかったループ本体
        "context",  # ゲート条件が呼び出し元引数に依存し文脈非依存サマリでは決まらない
    }
)

#: ゲート側の OPAQUE 語彙（§2.5.4。8 種）。支配の判定に付く。**val 側とは別語彙。**
GATE_OPAQUE_REASONS = frozenset(
    {
        "unresolved",
        "depth",
        "dynamic_registry",
        "lazy_genexp",
        "cfg_cap",
        "gate_name_only",
        "cycle",
        "unsupported_syntax",
    }
)

#: ゲート側の NODOM 語彙（§2.5.4。4 種）。**語彙外の理由を新設してはならない。**
GATE_NODOM_REASONS = frozenset(
    {
        "no_gate",
        "deny_reaches_effect",
        "non_binding_gate",
        "alt_entry",
    }
)


@dataclass(frozen=True, order=True)
class Prov:
    """確度。``resolved`` / ``opaque(reason)`` / ``remote`` の 3 値。

    `reasons` は val 側語彙（:data:`VAL_OPAQUE_REASONS`）のみを取る。
    **決して clean に潰さない。決して drop しない。**
    """

    kind: str  # "resolved" | "opaque" | "remote"
    reasons: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.kind not in ("resolved", "opaque", "remote"):
            raise ValueError(f"unknown provenance kind: {self.kind!r}")
        if self.kind != "opaque" and self.reasons:
            raise ValueError("reasons は opaque のときのみ持てる")
        for r in self.reasons:
            if r not in VAL_OPAQUE_REASONS:
                raise ValueError(f"val 側 opaque 語彙にない理由: {r!r}")

    @property
    def is_resolved(self) -> bool:
        return self.kind == "resolved"

    def __str__(self) -> str:  # pragma: no cover - 表示のみ
        if self.kind == "opaque":
            return "opaque(" + ",".join(self.reasons) + ")"
        return self.kind


RESOLVED = Prov("resolved")
REMOTE = Prov("remote")


def opaque(*reasons: str) -> Prov:
    """val 側の opaque を作る。理由は語彙で検査され、重複除去してソートする。"""
    return Prov("opaque", tuple(sorted(set(reasons))))


def prov_merge(*ps: Prov) -> Prov:
    """確度の合流。

    優先順は ``opaque > remote > resolved``。**「片方が resolved だから resolved」
    にしない**（それが無言の false-clean を作る）。opaque 理由は和集合を保つ。
    """
    reasons: set[str] = set()
    has_opaque = False
    has_remote = False
    for p in ps:
        if p.kind == "opaque":
            has_opaque = True
            reasons.update(p.reasons)
        elif p.kind == "remote":
            has_remote = True
    if has_opaque:
        return Prov("opaque", tuple(sorted(reasons)))
    if has_remote:
        return REMOTE
    return RESOLVED


# --------------------------------------------------------------------------
# §2.6: Shape
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Unknown:
    """形が分からない値。"""

    def kind(self) -> str:
        return "Unknown"


@dataclass(frozen=True)
class Atom:
    """スカラー。定数なら `const` に入る。仮引数由来なら `formal`。"""

    const: Optional[Any] = None
    formal: Optional[str] = None  # "Param(i)" / "Param(name)"

    def kind(self) -> str:
        return "Atom"


@dataclass(frozen=True)
class Str:
    """文字列の連結。`parts` は順序を保つ。K を超えた分は `tail` に畳む。"""

    parts: tuple[Value, ...] = ()
    tail: Optional[Value] = None

    def kind(self) -> str:
        return "Str"


@dataclass(frozen=True)
class Seq:
    """リスト / タプル。"""

    elems: tuple[Value, ...] = ()
    tail: Optional[Value] = None

    def kind(self) -> str:
        return "Seq"


@dataclass(frozen=True)
class Argv:
    """argv として使われる列（`shell=False` の spawn 引数）。"""

    elems: tuple[Value, ...] = ()
    tail: Optional[Value] = None

    def kind(self) -> str:
        return "Argv"


@dataclass(frozen=True)
class Map:
    """辞書。`entries` はキー文字列でソートする（決定論のため）。"""

    entries: tuple[tuple[str, Value], ...] = ()
    tail: Optional[Value] = None

    def kind(self) -> str:
        return "Map"


@dataclass(frozen=True)
class Path:
    """パス。`base` に対して `segs` を順に結合したもの。"""

    base: Optional[Value] = None
    segs: tuple[Value, ...] = ()
    tail: Optional[Value] = None

    def kind(self) -> str:
        return "Path"


@dataclass(frozen=True)
class Obj:
    """オブジェクト。**型だけでなく `fields` を持つ**（§2.6）。

    `fields` はカタログ化コンストラクタの実引数と、解析済みメソッドが
    `self.<name>` へ書いた値。F1（`git.Repo(p).git.checkout`）と
    F6（OpenManus `Bash` の `self._session._process.stdin`）がこれを要求する。
    """

    classes: tuple[str, ...] = ()
    fields: tuple[tuple[str, Value], ...] = ()

    def kind(self) -> str:
        return "Obj"


Shape = Union[Unknown, Atom, Str, Seq, Argv, Map, Path, Obj]

#: 値の属性語彙（§2.6。**val は等級を付けない。属性として記録するだけ**）。
VALUE_ATTRS = frozenset(
    {
        "tokenised",  # shlex.split 等でトークン化された
        "quoted",  # shlex.quote 等で引用された
        "canonicalised",  # symlink 解決子を通った
        "lexical_canon",  # 字句正規化子のみを通った（normpath / abspath）
        "joined",  # 連結で作られた
        "encoded",  # quote / urlencode 等
        "alias_mismatch",  # 検査された別名そのものではなく同じ root の別派生
        "post_check_append",  # 検査点より後に MODEL 要素が追加された
    }
)


# --------------------------------------------------------------------------
# §2.6: Value
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class Value:
    """三つ組 ``Prin × Prov × Shape`` に属性表と root 集合を添えたもの。"""

    prin: Prin = Prin.OP
    prov: Prov = RESOLVED
    shape: Shape = field(default_factory=Unknown)
    attrs: frozenset[str] = frozenset()
    #: この値が由来する MODEL 導入点（R1/R2）の集合。root id の文字列。
    roots: frozenset[str] = frozenset()

    def __post_init__(self) -> None:
        for a in self.attrs:
            if a not in VALUE_ATTRS:
                raise ValueError(f"未知の値属性: {a!r}")

    # -- 便利関数 ---------------------------------------------------------

    @property
    def const(self) -> Optional[Any]:
        """リテラル定数なら返す。そうでなければ None。"""
        if isinstance(self.shape, Atom):
            return self.shape.const
        return None

    def is_literal(self) -> bool:
        return isinstance(self.shape, Atom) and self.shape.const is not None

    def with_attr(self, *names: str) -> Value:
        return Value(self.prin, self.prov, self.shape, self.attrs | frozenset(names), self.roots)

    def with_prov(self, p: Prov) -> Value:
        return Value(self.prin, p, self.shape, self.attrs, self.roots)

    def with_shape(self, s: Shape) -> Value:
        return Value(self.prin, self.prov, s, self.attrs, self.roots)

    # -- 直列化（決定論のため。キーは常にソート順に出す）-------------------

    def to_json(self) -> dict:
        out: dict[str, Any] = {
            "prin": self.prin.name,
            "prov": self.prov.kind,
            "shape": _shape_json(self.shape),
        }
        if self.prov.reasons:
            out["prov_reasons"] = list(self.prov.reasons)
        if self.attrs:
            out["attrs"] = sorted(self.attrs)
        if self.roots:
            out["roots"] = sorted(self.roots)
        return out


def _shape_json(s: Shape) -> dict:
    k = s.kind()
    if isinstance(s, Atom):
        d: dict[str, Any] = {"k": k}
        if s.const is not None:
            d["const"] = s.const if isinstance(s.const, (str, int, float, bool)) else repr(s.const)
        if s.formal is not None:
            d["formal"] = s.formal
        return d
    if isinstance(s, Str):
        return _seqish_json(k, s.parts, s.tail)
    if isinstance(s, Seq):
        return _seqish_json(k, s.elems, s.tail)
    if isinstance(s, Argv):
        return _seqish_json(k, s.elems, s.tail)
    if isinstance(s, Path):
        d = {"k": k, "segs": [v.to_json() for v in s.segs]}
        if s.base is not None:
            d["base"] = s.base.to_json()
        if s.tail is not None:
            d["tail"] = s.tail.to_json()
        return d
    if isinstance(s, Map):
        d = {"k": k, "entries": [[key, v.to_json()] for key, v in s.entries]}
        if s.tail is not None:
            d["tail"] = s.tail.to_json()
        return d
    if isinstance(s, Obj):
        return {
            "k": k,
            "classes": list(s.classes),
            "fields": [[n, v.to_json()] for n, v in s.fields],
        }
    return {"k": k}


def _seqish_json(k: str, items: tuple[Value, ...], tail: Optional[Value]) -> dict:
    d: dict[str, Any] = {"k": k, "items": [v.to_json() for v in items]}
    if tail is not None:
        d["tail"] = tail.to_json()
    return d


# 既製の値 --------------------------------------------------------------

def lit(const: Any, prin: Prin = Prin.OP) -> Value:
    """リテラル定数の値。既定の主体は OP（コードに書いてあるもの = 運用者）。"""
    return Value(prin, RESOLVED, Atom(const=const))


def unknown_value(prov: Prov = RESOLVED, prin: Prin = Prin.OP) -> Value:
    return Value(prin, prov, Unknown())


def model_value(root: str, shape: Optional[Shape] = None) -> Value:
    """MODEL 導入点（R1/R2）が与える値。"""
    return Value(Prin.MODEL, RESOLVED, shape or Unknown(), frozenset(), frozenset({root}))


def value_join(a: Value, b: Value) -> Value:
    """分岐の合流。P 側は join、確度は :func:`prov_merge`、属性は**積**を採る。

    属性の積を採るのは、片方の経路でしか成り立たない性質（`canonicalised` など）を
    合流後の値に持ち越さないため。root は和集合（どちらの由来もありうる）。
    """
    return Value(
        prin_join(a.prin, b.prin),
        prov_merge(a.prov, b.prov),
        _shape_join(a.shape, b.shape),
        a.attrs & b.attrs,
        a.roots | b.roots,
    )


def _shape_join(a: Shape, b: Shape) -> Shape:
    if a == b:
        return a
    if isinstance(a, Atom) and isinstance(b, Atom):
        if a.const == b.const and a.formal == b.formal:
            return a
        return Atom()
    if isinstance(a, (Seq, Argv)) and type(a) is type(b):
        # **共通の先頭は要素ごとに join し、はみ出した要素は tail に畳む**（D17）。
        # 形だけ残して要素を捨てると、`cmd = ["sg", ...]; if f: cmd.append(x)` の合流で
        # argv0 のリテラル "sg" が消え、argv0 が列全体（MODEL）になる（A9 で発生）。
        n = min(len(a.elems), len(b.elems))
        prefix = tuple(value_join(x, y) for x, y in zip(a.elems[:n], b.elems[:n], strict=True))
        tail: Optional[Value] = None
        for extra in list(a.elems[n:]) + list(b.elems[n:]) + [t for t in (a.tail, b.tail) if t is not None]:
            tail = extra if tail is None else value_join(tail, extra)
        return type(a)(prefix, tail)
    if a.kind() == b.kind():
        # 同種だが中身が違う: 要素は畳んで Unknown 側に倒さず、形だけ残す。
        if isinstance(a, Str):
            return Str((), None)
        if isinstance(a, Seq):
            return Seq((), None)
        if isinstance(a, Argv):
            return Argv((), None)
        if isinstance(a, Map):
            return Map((), None)
        if isinstance(a, Path):
            return Path(None, (), None)
        if isinstance(a, Obj) and isinstance(b, Obj):
            return Obj(tuple(sorted(set(a.classes) | set(b.classes))), ())
    return Unknown()


# --------------------------------------------------------------------------
# §2.5: 3 値支配
# --------------------------------------------------------------------------


class DomKind(enum.Enum):
    """3 値支配。合成の優先順は ``NODOM > OPAQUE > DOM``。"""

    DOM = "DOM"
    OPAQUE = "OPAQUE"
    NODOM = "NODOM"


#: 合成の優先順（§2.5.5）。**OPAQUE を NODOM に潰しても DOM に潰してもならない。**
_DOM_PRIORITY = {DomKind.NODOM: 2, DomKind.OPAQUE: 1, DomKind.DOM: 0}


@dataclass(frozen=True)
class DomResult:
    """支配判定の結果。`reason` は 3 値ごとに別語彙で検査される。"""

    kind: DomKind
    reason: Optional[str] = None
    #: DOM のときの等級（P^op 上の値）。
    grade: Optional[Req] = None
    #: witness の行番号（`finally` 複製のときは脱出種別を併記した文字列）。
    witness: Optional[str] = None

    def __post_init__(self) -> None:
        if self.kind is DomKind.OPAQUE:
            if self.reason not in GATE_OPAQUE_REASONS:
                raise ValueError(f"ゲート側 OPAQUE 語彙にない理由: {self.reason!r}")
        elif self.kind is DomKind.NODOM:
            if self.reason not in GATE_NODOM_REASONS:
                raise ValueError(f"NODOM 語彙にない理由: {self.reason!r}")

    def to_json(self) -> dict:
        d: dict[str, Any] = {"verdict": self.kind.value}
        if self.reason is not None:
            d["reason"] = self.reason
        if self.grade is not None:
            d["grade"] = self.grade.name
        if self.witness is not None:
            d["witness"] = self.witness
        return d


def dom_combine(*rs: DomResult) -> DomResult:
    """3 値の合成。優先順 ``NODOM > OPAQUE > DOM`` を単一の共有関数で実装する。"""
    if not rs:
        return DomResult(DomKind.NODOM, "no_gate")
    best = rs[0]
    for r in rs[1:]:
        if _DOM_PRIORITY[r.kind] > _DOM_PRIORITY[best.kind]:
            best = r
        elif _DOM_PRIORITY[r.kind] == _DOM_PRIORITY[best.kind] and r.kind is DomKind.DOM:
            # DOM 同士は経路上の最強（⊔）を採る。
            if (r.grade or REQ_BOTTOM) > (best.grade or REQ_BOTTOM):
                best = r
    return best
