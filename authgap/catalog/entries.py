"""Def 2: MODEL ラベルの導入規則。出発点は R1 と R2 の 2 つだけ。

R1 と R2 は同一主体 MODEL の導入位置が 2 か所あるだけで、sink 表・ゲート採点・
判定は共有する。

**このカタログの外から MODEL を導入してはならない。** 追加するときは月 3 の
凍結物（`docs/fingerprint.json`）を更新し、指紋の sha256 を変える。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

# --------------------------------------------------------------------------
# R1: カタログ化した LLM 呼び出しの戻り値とその射影
# --------------------------------------------------------------------------

#: MODEL 値を返す呼び出し。dotted 名の**末尾一致**で照合する（別名 import と
#: 受け手の型消去に耐えるため）。照合単位は「属性アクセスの列」。
LLM_CALLS: tuple[str, ...] = (
    # OpenAI
    "chat.completions.create",
    "completions.create",
    "responses.create",
    "beta.chat.completions.parse",
    # Anthropic
    "messages.create",
    "messages.stream",
    # LiteLLM / 汎用
    "litellm.completion",
    "litellm.acompletion",
    # LangChain / LangGraph
    "llm.invoke",
    "llm.ainvoke",
    "llm.predict",
    "llm.generate",
    "chain.invoke",
    "model.invoke",
    "model.ainvoke",
    "ChatOpenAI.invoke",
    "bind_tools.invoke",
    # Google / Cohere / Ollama
    "generate_content",
    "generate_content_async",
    "ollama.chat",
    "client.chat",
    "cohere.chat",
    # フレームワーク内のラッパ
    "ask_tool",
    "ask",
)

#: LLM 戻り値の射影。ここに列挙した属性到達だけが MODEL を保つ。
#: **列挙外の射影に落ちた値は MODEL を失わない**（保守側に倒す）が、
#: 射影名は manifest の root 説明に出す。
LLM_PROJECTIONS: tuple[str, ...] = (
    "content",
    "text",
    "tool_calls",
    "name",
    "args",
    "arguments",
    "function",
    "input",
    "parsed",
    "choices",
    "message",
)


# --------------------------------------------------------------------------
# R2: カタログ化したツールエントリのパラメータ
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class EntryRule:
    """ツールエントリの認識規則。

    `kind` は認識の形:

    * ``decorator``      関数デコレータ（`@mcp.tool`、`@tool`、`@function_tool` …）
    * ``method``         クラスの特定メソッド（`BaseTool._run`、CrewAI `_run` …）
    * ``lowlevel_v1``    `@server.call_tool()` デコレータ + name 分岐
    * ``lowlevel_v2``    `Server(on_call_tool=...)` / `add_request_handler("tools/call", ...)`
    * ``spec_object``    `ToolSpec(...)` のようなオブジェクト構築（gptme）

    `framework` は unit id の第 1 成分になる。
    """

    kind: str
    framework: str
    #: デコレータ名 / メソッド名 / 構築子名の照合パターン（末尾一致）。
    names: tuple[str, ...]
    #: `method` 形のとき、受け手クラスがこれらの基底を継承していること。
    bases: tuple[str, ...] = ()
    #: 引数のうち MODEL としない名前（`self`、`cls`、実行文脈など）。
    exclude_params: tuple[str, ...] = ("self", "cls")
    note: str = ""


ENTRY_RULES: tuple[EntryRule, ...] = (
    # -- MCP 高レベル -------------------------------------------------------
    EntryRule(
        "decorator",
        "mcp",
        ("mcp.tool", "server.tool", "app.tool", "tool"),
        note="公式 SDK fastmcp(v1) / mcpserver(v2) の高レベル登録。執行表では Def 5 側",
    ),
    EntryRule(
        "decorator",
        "fastmcp",
        ("mcp.tool", "FastMCP.tool"),
        note="サードパーティ fastmcp（jlowin）。執行表では Def 5 側",
    ),
    # -- MCP 低レベル 2 形（Def 2 が名指しで要求）---------------------------
    EntryRule(
        "lowlevel_v1",
        "mcp-lowlevel-v1",
        ("server.call_tool", "call_tool"),
        note="v1 系デコレータ形。ハンドラ内の name 分岐が DISPATCH になる",
    ),
    EntryRule(
        "lowlevel_v2",
        "mcp-lowlevel-v2",
        ("Server", "add_request_handler"),
        note="v2 系。ハンドラは __init__ の on_call_tool= で渡される",
    ),
    # -- LangChain ---------------------------------------------------------
    EntryRule("decorator", "langchain", ("tool", "langchain.tool", "tools.tool")),
    EntryRule(
        "method",
        "langchain",
        ("_run", "_arun"),
        bases=("BaseTool", "StructuredTool", "BaseModel.BaseTool"),
    ),
    # -- CrewAI ------------------------------------------------------------
    EntryRule("method", "crewai", ("_run",), bases=("BaseTool", "CrewaiBaseTool")),
    # -- openai-agents -----------------------------------------------------
    EntryRule("decorator", "openai-agents", ("function_tool",)),
    # -- Semantic Kernel ---------------------------------------------------
    EntryRule(
        "decorator",
        "semantic-kernel",
        ("kernel_function",),
        note="name= / description= しか宣言しないので D ではない（Def 6）",
    ),
    # -- agno --------------------------------------------------------------
    EntryRule(
        "method",
        "agno",
        ("*",),
        bases=("Toolkit",),
        note="Toolkit のメソッドが register される。F9（ShellTools）が依存する",
    ),
    # -- gptme -------------------------------------------------------------
    EntryRule("spec_object", "gptme", ("ToolSpec",)),
)

#: 低レベル MCP の v2 ハンドラ登録キーワード。
LOWLEVEL_V2_KWARGS: tuple[str, ...] = ("on_call_tool",)
#: 低レベル MCP の v2 ハンドラ登録メソッドの第 1 引数。
LOWLEVEL_V2_REQUEST = "tools/call"


# --------------------------------------------------------------------------
# R2 の例外（Def 2）
#
# フレームワークが実行時に「このパラメータをモデルに見せない」ことを執行する
# 機械可読な指定がある引数は val = MODEL としない。
# この例外は執行表と同じ時点（月 3）で凍結する。
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class R2Exception:
    """`val = MODEL` としない引数の指定形。"""

    framework: str
    #: `Annotated[...]` の中に現れるキーと値。
    marker_key: str
    marker_value: object
    note: str
    #: 一次確認の出所。
    verified: str


R2_EXCEPTIONS: tuple[R2Exception, ...] = (
    R2Exception(
        framework="semantic-kernel",
        marker_key="include_in_function_choices",
        marker_value=False,
        note="Annotated[..., {'include_in_function_choices': False}] の引数はモデルに見せない",
        verified="Def 2 の R2 例外。一次確認は月 3 凍結時に fingerprint.json へ記録する",
    ),
)


# --------------------------------------------------------------------------
# 承認割り込みの語彙（Def 5。req_occ を USER へ引き上げうる形）
#
# 承認割り込みは M 側の req_occ であって D ではない。**二重計上しないこと。**
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class ApprovalRule:
    """承認割り込みの認識規則。

    `form`:

    * ``raises``      呼ぶと拒否時に送出する（A-a）
    * ``predicate``   戻り値が分岐条件として使われる（A-c）
    * ``kwarg``       登録時のキーワードで宣言する
    * ``decorator``   デコレータで宣言する
    * ``ctx_manager`` context manager 形（`yield` より前の拒否経路を見る）
    """

    name: str
    form: str
    framework: str
    note: str = ""


APPROVAL_INTERRUPTS: tuple[ApprovalRule, ...] = (
    ApprovalRule("confirm", "predicate", "generic"),
    ApprovalRule("input", "predicate", "generic", note="標準入力での確認"),
    ApprovalRule("interrupt", "raises", "langgraph"),
    ApprovalRule("require_approval", "raises", "generic"),
    ApprovalRule("requires_confirmation", "kwarg", "agno"),
    ApprovalRule("requires_user_input", "kwarg", "agno"),
    ApprovalRule("external_execution", "kwarg", "agno"),
    ApprovalRule("human_input", "kwarg", "crewai", note="Task(human_input=True)"),
    ApprovalRule("needs_approval", "kwarg", "openai-agents"),
    ApprovalRule("should_confirm", "predicate", "openhands", note="ConfirmationPolicy.should_confirm"),
    ApprovalRule("require_approval", "decorator", "praisonai", note="@require_approval(risk_level=...)"),
    ApprovalRule("HumanInTheLoopMiddleware", "kwarg", "langchain", note="interrupt_on="),
)

#: 承認割り込みの名前だけの集合（A-a/A-b/A-c のいずれも取れなければ
#: `OPAQUE(gate_name_only)`。**推定で A にしない**）。
APPROVAL_NAMES: frozenset[str] = frozenset(r.name for r in APPROVAL_INTERRUPTS)


# --------------------------------------------------------------------------
# 発生ゲート（Def 5-b。第 1 年は manifest 属性で verdict を持たない）
# --------------------------------------------------------------------------

#: 露出ゲートの形（前測での保有率 0.0%）。
EXPOSURE_GATE_FORMS: tuple[str, ...] = (
    "enabled",  # FastMCP 2.x @mcp.tool(..., enabled=<expr>)
    "disable",  # 3.0 以降 mcp.disable(names=|tags=)
    "enable",  # mcp.enable(..., only=True)
)

#: モードゲートの真偽 config atom 名（前測での保有率 12.5%）。
MODE_GATE_ATOMS: tuple[str, ...] = (
    "read_only",
    "readonly",
    "dry_run",
    "allow_write",
    "allow_writes",
    "allow_dangerous_operations",
    "allow_dangerous_requests",
    "enable_security_check",
    "safe_mode",
)

#: 被覆漏れ理由の語彙（4 語 + opaque）。**語彙外を新設しない。**
LEAK_REASONS: frozenset[str] = frozenset(
    {"parallel_entry", "sibling_reach", "default_open_atom", "fail_open_init", "opaque"}
)


def entry_frameworks() -> tuple[str, ...]:
    """unit id の第 1 成分になりうる framework 名。"""
    return tuple(sorted({r.framework for r in ENTRY_RULES}))


def find_entry_rule(kind: str, name: str) -> Optional[EntryRule]:
    """認識形と名前から規則を引く。名前は末尾一致で照合する。"""
    for rule in ENTRY_RULES:
        if rule.kind != kind:
            continue
        for pat in rule.names:
            if pat == "*" or name == pat or name.endswith("." + pat):
                return rule
    return None
