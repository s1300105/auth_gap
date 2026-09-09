"""付録 G の共通前置き。**すべて木内で解決できる。**

仕様書 §2.5 付録 G が列挙する部品をそのまま置く。ここに無いものを
G-mutant が参照してはならない（木内解決できることが前提条件だから）。
"""

import contextlib
import os


class ApprovalDenied(Exception):
    """承認が拒否されたことを表す例外。"""


#: モジュール定数・既定閉の allowlist（config atom の源: module_const）。
ALLOWED_TOOLS = {"git_log", "git_show"}


def confirm(name):
    """A 真偽形の承認割り込み。**拒否しても送出しない**（戻り値で返す）。"""
    answer = input(f"allow {name}? [y/N] ")
    return answer.strip().lower() == "y"


def require_approval(name):
    """A raise 形の承認割り込み。拒否側の出口はすべて raise。"""
    if not confirm(name):
        raise ApprovalDenied(name)


def is_allowed(name):
    """V allowlist。既定閉のモジュール定数を読む。"""
    return name in ALLOWED_TOOLS


def validate_path(path, root):
    """strong-path の 3 条件を満たす検証子。

    (i) `os.path.realpath` で canonical alias を得る
    (ii) `os.path.commonpath` で包含を確認する
    (iii) 他方の被演算子は引数 root（config root）
    """
    real = os.path.realpath(path)
    base = os.path.realpath(root)
    if os.path.commonpath([real, base]) != base:
        raise ValueError(path)
    return real


def _load_plugins():
    """木内で解決できない値を返す（G13 が要求する）。"""
    import importlib.metadata

    return {ep.name: ep.load() for ep in importlib.metadata.entry_points()}


def _run_tool(args):
    return args


TOOLS = {"git_log": _run_tool, "git_show": _run_tool}


class Gateway:
    """G8 / G11 / G13 が使うゲート保持クラス。"""

    default_tool = "git_log"
    plugins = _load_plugins()

    def is_allowed(self, name):
        return name in ALLOWED_TOOLS

    @contextlib.contextmanager
    def require_approval(self, name):
        """CM 形の承認ゲート。**`yield` より前の拒否経路の出口はすべて raise。**"""
        if not confirm(name):
            raise ApprovalDenied(name)
        yield name
