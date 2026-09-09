"""Def 5 のゲート語彙と §6 F0a の validator 形状語彙。**語彙の唯一の定義点。**

仕様書は「§0 と §10 はここを参照し語彙を再掲しない」と定めている。実装でも
同じ規則を課す — 他の module が weak 理由や形状名の文字列リテラルを持たない。

月 6 の凍結対象:

* :data:`VALIDATOR_SHAPES`（11 語）
* :data:`WEAK_REASONS`（19 語）
* strong の 4 定義（:func:`strong_path_requirements` ほか）
* :data:`CONFIG_ATOM_SOURCES`（4 源）
* :data:`WITNESS_TEMPLATES`
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

# --------------------------------------------------------------------------
# §6 F0a: 構文的 validator 形状の語彙（11 語）
#
# **本節が唯一の定義点。** 第 3 版は §0 で 7 語、§6 で 8 語、§10 で別の 8 語と
# 3 通りに書き、3 つとも `Path.resolve` と `relative_to` を欠いていた。A1 の
# 修正版はその 2 つだけで構成されるので、旧語彙では脈拍が A1 を判別できない。
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ShapeRule:
    """validator 形状 1 語の認識規則。

    `dotted` は完全 dotted 名、`methods` は受け手を主語とするメソッド名。
    支配判定を必要としない（F0a は支配なしで抽出する）。
    """

    name: str
    dotted: tuple[str, ...] = ()
    methods: tuple[str, ...] = ()
    note: str = ""


VALIDATOR_SHAPES: tuple[ShapeRule, ...] = (
    ShapeRule(
        "realpath",
        dotted=("os.path.realpath", "os.realpath"),
        methods=("resolve",),
        note="symlink 解決子。Def 5 strong-path (i) を満たす唯一の系統",
    ),
    ShapeRule(
        "lexical_canon",
        dotted=("os.path.normpath", "os.path.abspath"),
        note="字句正規化子。**単独では (i) を満たさない**",
    ),
    ShapeRule(
        "containment",
        dotted=("os.path.commonpath", "os.path.commonprefix"),
        methods=("is_relative_to", "relative_to"),
        note="包含述語。Def 5 strong-path (ii)",
    ),
    ShapeRule("prefix", methods=("startswith",), note="前置一致。単独では境界を持たない"),
    ShapeRule(
        "urlparse",
        dotted=("urllib.parse.urlparse", "urllib.parse.urlsplit"),
        methods=("hostname",),
    ),
    ShapeRule("shlex_split", dotted=("shlex.split",)),
    ShapeRule("shlex_quote", dotted=("shlex.quote", "pipes.quote")),
    ShapeRule("shlex_join", dotted=("shlex.join",)),
    ShapeRule("split", methods=("split", "rsplit", "partition")),
    ShapeRule("ctor_path", dotted=("pathlib.Path",), note="Path(...) は正規化ではない（F7）"),
    ShapeRule(
        "exists",
        dotted=("os.path.exists", "os.path.isfile", "os.path.isdir"),
        methods=("exists", "is_file", "is_dir", "rev_parse"),
        note="存在検証。`git rev_parse` 型を含む（Def 5 strong-token）",
    ),
)

#: 形状語彙の名前だけ（11 語）。
SHAPE_NAMES: tuple[str, ...] = tuple(r.name for r in VALIDATOR_SHAPES)
assert len(SHAPE_NAMES) == 11, "validator 形状語彙は 11 語（§6 F0a）"


def shape_for_dotted(dotted: str) -> Optional[str]:
    for r in VALIDATOR_SHAPES:
        if dotted in r.dotted:
            return r.name
    return None


def shape_for_method(method: str) -> Optional[str]:
    for r in VALIDATOR_SHAPES:
        if method in r.methods:
            return r.name
    return None


# --------------------------------------------------------------------------
# Def 5: 等級
# --------------------------------------------------------------------------

#: 値検証の等級。**`strong` は推定で出さない。**
GRADES: tuple[str, ...] = ("strong-path", "strong-token", "strong-enum", "strong-eval", "weak", "unknown", "none")

#: strong-eval は任意（既定では実装しない。§7.4 切り詰め順序の (0)）。
IMPLEMENT_STRONG_EVAL = False


# -- strong-path -----------------------------------------------------------

#: (ii) の包含述語。**これ以外は包含述語として認めない。**
CONTAINMENT_PREDICATES: tuple[str, ...] = (
    "os.path.commonpath",  # commonpath(...) == root
    "is_relative_to",  # Path.is_relative_to
    "relative_to",  # Path.relative_to を ValueError 捕捉で使う形
    "startswith_sep",  # startswith(root + os.sep)（root が os.sep 終端に正規化されている形）
    "exact_allowlist",  # 完全一致 allowlist
    "hostname_allowlist",  # urlparse().hostname の allowlist 比較
)

#: (iii) 述語の他方の被演算子として認めるもの。
ALLOWED_OPERANDS: tuple[str, ...] = ("literal", "config_root", "os.getcwd")


def strong_path_requirements() -> tuple[str, str, str]:
    """strong-path の 3 条件（可読な形で 1 か所に置く。判定は gate.py が行う）。"""
    return (
        "(i) 制御引数の root について symlink 解決子を通った canonical alias が存在する",
        "(ii) 同じ root の canonical alias に包含述語が適用され、その述語が sink をゲートする",
        "(iii) 述語の他方の被演算子が定数 / config root / os.getcwd()",
    )


#: root-equal 条件で許される差（これ以外があれば strong にしない）。
ROOT_EQUAL_STEPS: tuple[str, ...] = (
    "identity",
    "canonicalising_transform",  # 向きは問わない
    "op_literal_segment_append",  # principal が OP かつリテラルの Path.segs / Str.parts 要素の追加
)


# -- strong-token ----------------------------------------------------------

def strong_token_requirements() -> tuple[str, str, str]:
    return (
        "メタ文字・フラグ拒否（startswith('-') 拒否、argv の -- セパレータ）",
        "存在検証（値が既存の名前空間要素に解決されることの確認。git rev_parse 型）",
        "argv 実行（shell=False）",
    )


#: フラグ拒否の認識形。
DASH_REJECT_FORMS: tuple[str, ...] = ("startswith_dash", "dashdash_separator")


# -- strong-enum -----------------------------------------------------------

#: strong-enum が読む値域語彙（Def 6 の D_dom 語彙と同じ文字列だが役割が違う）。
#: **読む側（strong-enum）は B3、数える側（r_dom）は Def 6 の実装条件を満たすまで 0。**
ENUM_BINDING_FORMS: tuple[str, ...] = ("enum", "Literal", "Enum", "scalar")

#: strong にしない値域語彙（否定規則）。
NOT_STRONG_DOMAINS: tuple[str, ...] = ("format", "bounded", "length", "path_type", "url_type")


# --------------------------------------------------------------------------
# Def 5: weak 理由の語彙（19 語。月 6 凍結）
#
# **語彙外の理由を新設してはならない。**
# --------------------------------------------------------------------------

WEAK_REASONS: tuple[str, ...] = (
    "first_token",
    "prefix_no_canon",
    "prefix_no_boundary",
    "no_containment",
    "no_symlink_resolution",
    "post_check_append",
    "split_colon",
    "no_dashdash",
    "no_existence_check",
    "no_dash_reject",
    "fuzzy_name",
    "docker_fallback",
    "fail_open",
    "denylist_enum",
    "regex_no_canon",
    "regex_denylist",
    "validate_then_fetch",
    "underscore_denylist",
    "lexical_canon_only",
)
assert len(WEAK_REASONS) == 19, "weak 理由語彙は 19 語（Def 5）"
WEAK_REASON_SET = frozenset(WEAK_REASONS)


def validate_weak_reason(reason: str) -> None:
    if reason not in WEAK_REASON_SET:
        raise ValueError(f"weak 理由語彙（19 語）にない理由: {reason!r}")


# --------------------------------------------------------------------------
# 共通の格下げ（値検証に適用）
#
# **`self_granted` は weak 理由語彙ではなく格下げ属性である**（§5.2）。
# manifest では `weak_reason` 列ではなく `downgrade` 列に出す。
# --------------------------------------------------------------------------

DOWNGRADES: tuple[str, ...] = (
    "tainted",  # 述語オペランドが MODEL
    "self_granted",  # 述語オペランドが被支配側で局所構成されたリテラル由来オブジェクト
    "config_conditional",  # config atom 依存（既定が開なら req は MODEL のまま）
    "opaque",  # 未解決
)


# --------------------------------------------------------------------------
# config atom の源は 4 種（Def 5）
# --------------------------------------------------------------------------

CONFIG_ATOM_SOURCES: tuple[str, ...] = (
    "ctor_kwarg",  # コンストラクタ kwarg
    "module_const",  # モジュール定数
    "environ",  # os.environ 読み出し
    "cli_default",  # CLI オプションの既定値（argparse dest+default、click/typer option 既定）
)

#: hook 登録チェーン、generator 越し、HTTP 越しは opaque（Def 5）。
CONFIG_ATOM_OPAQUE_FORMS: tuple[str, ...] = ("hook_chain", "through_generator", "over_http")

#: 既定値がこれらなら default-open とし `req` は MODEL のまま（Def 5）。
DEFAULT_OPEN_VALUES: tuple[object, ...] = (None, True, "*", "all")


def is_default_closed(default: object) -> Optional[bool]:
    """config atom の既定が「閉」か。判定できなければ None を返す（推定しない）。"""
    if default is None:
        return False
    if isinstance(default, bool):
        return default is False
    if isinstance(default, str):
        if default in ("*", "all", ""):
            return False
        return True
    if isinstance(default, (list, tuple, set, frozenset)):
        return len(default) > 0
    return None


# --------------------------------------------------------------------------
# fail-open 規則（Def 5）
#
# ゲート述語の関数が、例外・未認識入力・None 返却の経路で許可側の値を返す場合は
# weak(fail_open) とし strong に上げない。
#
# **ただし fail_open は両側判別には使えない**（Omnigent A17 は修正版も
# abstain=ALLOW のまま）。F0a の測定量および GAP 理由としてのみ使い、
# T1 の合格数には寄与させない。
# --------------------------------------------------------------------------

FAIL_OPEN_COUNTS_FOR_TWO_SIDED = False


# --------------------------------------------------------------------------
# witness テンプレート（§5.2。weak 理由ごとに全部決める）
# --------------------------------------------------------------------------

WITNESS_TEMPLATES: dict[str, str] = {
    "first_token": "ls; <続きのコマンド>",
    "split_colon": "allowed.com:@evil",
    "prefix_no_canon": "<allowed_root>/../etc/passwd",
    "prefix_no_boundary": "<root>_evil/x（root の兄弟で前置一致する名前）",
    "no_containment": "/etc/passwd（絶対パス）",
    "no_symlink_resolution": "<root>/link -> /etc（シンボリックリンク。`../` ではない）",
    "no_dashdash": "--upload-pack=touch /tmp/x（フラグ様のファイル名）",
    "no_dash_reject": "--upload-pack=touch /tmp/x（フラグ様のファイル名）",
    "fuzzy_name": "allowlist 名から 1 編集距離の名前",
    "docker_fallback": "同じ argv を docker 不在で実行しローカル分岐を示す",
    "post_check_append": "検査後に MODEL 要素が連結される箇所（値ではなく行を示す）",
    "no_existence_check": "名前空間に存在しない値（存在しないブランチ名 / リビジョン）",
    "underscore_denylist": "拒否語彙に載っていない dunder（`__class__` 経由の到達など）",
    "lexical_canon_only": "シンボリックリンク（no_symlink_resolution と同形。差は包含述語の有無）",
    "fail_open": "ゲートが未認識と判定する入力（未知のラッパ、`bash -lc` 等）",
    "denylist_enum": "拒否語彙に載っていない同義構文",
    "regex_denylist": "拒否語彙に載っていない同義構文",
    "regex_no_canon": "引用識別子 / インラインコメント / スキーマ修飾",
    "validate_then_fetch": "検証を通す初期 URL からのリダイレクト先",
}

#: 格下げ属性の witness（weak 理由語彙には含めない）。
DOWNGRADE_WITNESS: dict[str, str] = {
    "self_granted": "ゲート述語が読む権限コンテキストを局所で構成している箇所（値ではなく行を示す）",
}

assert set(WITNESS_TEMPLATES) == WEAK_REASON_SET, "全 weak 理由に witness テンプレートが要る（§5.2）"


#: witness は effect view がこれらのときのみ出力する（§5.2）。
WITNESS_VIEWS: tuple[str, ...] = ("shell_string", "raw_path", "raw_url")

#: argv モードの SPAWN には `no_dashdash` witness は出すが `first_token` は出さない。
ARGV_MODE_SUPPRESSED_WITNESS: frozenset[str] = frozenset({"first_token"})


# --------------------------------------------------------------------------
# 否定規則（Def 5）
# --------------------------------------------------------------------------

#: `shlex.split` の存在だけでは strong に上げない（AutoGPT A5 の実例が反例）。
SHLEX_SPLIT_ALONE_IS_NOT_STRONG = True


# --------------------------------------------------------------------------
# 未解決事項（黙って安全側に倒さないための記録）
# --------------------------------------------------------------------------

#: 仕様書内で解決していない語彙の食い違い。月 6 の凍結前に学生が決める。
OPEN_VOCABULARY_QUESTIONS: tuple[tuple[str, str], ...] = (
    (
        "absolute_only / existence_only",
        "§2.6 の fixture F7 は「weak 理由 absolute_only / existence_only / no_containment を"
        "追加する根拠」と書くが、Def 5 の凍結語彙 19 語にこの 2 語は無い。"
        "本実装は 19 語を採り、2 語は追加していない。月 6 凍結前に決めること。"
        "docs/open_questions.md に記録。",
    ),
)
