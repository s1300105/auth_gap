"""D64 / U23: 入口の仮引数の種付け（注釈の型・lifespan）。所見 R4-r4-2, R4-r1-6, R4-r4-1（R2-r1-10 は反証済みで直さない）。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U23）。** v2 / v3 の件数には合わせず、
FastMCP / pydantic / dataclasses / pathlib / mcp SDK の意味、Def 2（R2: 入口の仮引数は MODEL）、§7.1 / §7.2 /
§9.3 / §9.4（`docs/contradiction_principles.md`）、D17 改訂 4 / 5（共有される可変オブジェクトは `_opaque_deep`:
型と主体を保ち確度だけ opaque）、D61 追記（注釈の先頭名の厳密な解決）、D64 の U23 行と
`evidence/review/triage.json` の U23 fix_outline（検証役の反例と「避ける条件」）から導いた。

- `test_fix_*`（今の解析器で**落ちる**）: 所見の expected（fix_outline の条件つき）。
- `test_keep_*`（今の解析器で**通る**）: 検証役の反例（素朴な直し方で誤警報・誤 clear になる形）、所見の対照、
  今正しく判定できている形。直した後もこれが通らなければならない。

学生の決定（U23）: pydantic / dataclass 引数・Path 注釈・lifespan の yield 値の 3 つとも直す。R2-r1-10（ctx を OP に
する）は直さない（ctx は MODEL の仮引数のまま。c10_sampling は通る側）。

1. R4-r4-2 pydantic / dataclass 引数: 木内クラスに厳密に解け、家族が BaseModel / dataclass / NamedTuple で、
   構築時フックが無いときだけ、フィールドを MODEL / resolved（root はフィールドごと）にする。
   反例 ce_pydantic_hooks の 4 形（field_validator / model_validator / __post_init__ / Annotated の AfterValidator）と、
   その他のフック・外部の基底・二重束縛・ClassVar / `_` / PrivateAttr / `field(init=False)` / property /
   computed_field は今どおり（矛にしない）。langroid の message_fields にも同じフックの条件を入れる。
2. R4-r1-6 Path 注釈: 注釈の先頭名がモジュール直下でちょうど 1 回、level 0 の `from pathlib import Path` /
   `import pathlib` で束縛されるときだけ Path 形（主体・root は変えない）。反例 ce6_intree_path（木内の
   `class Path`）・相対 import・木内モジュールの `Path`・二重束縛では pathlib の効果を足さない。
3. R4-r4-1 lifespan: 装飾子の受け手の自分の構築式（`FastMCP(...)` / `Server(...)`）が import 表で厳密に解け、
   `lifespan=` が木内の CM 関数名のときだけ、yield 値を `_opaque_deep` で種付けする（受け手型は残り、定数は
   読めない）。反例 ce_lifespan_rebound（共有状態に置いた定数を 内 にしない）、partial / 工場関数、別の
   インスタンス、利用者定義の `Context`、起動時の効果をツールに付けない。
4. R2-r1-10（直さない）: ctx は MODEL の仮引数のまま（c10_sampling の不は残る）。

新しい注記・鍵は仮定しない。観測は manifest の効果行（kind / site / slots の prin・prov・roots・shape.const /
http_method）、行の注記（`contradiction:*` / `contradiction_reason:*` / `contradiction_unknown:*`）、
`unit.params` だけで行う。pydantic の root の名前（`req.path`）は fix_outline の `roots={f"{name}.{f}"}` による。
"""

from __future__ import annotations

import pytest

from authgap.report import manifest_json
from authgap.runner import RunConfig, run


def _units(tmp_path_factory, name, files):
    d = tmp_path_factory.mktemp(name)
    for rel, src in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(src, encoding="utf-8")
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _effects(u: dict, kind: str) -> list[dict]:
    return [e for e in u["effects"] if e["kind"] == kind]


def _slot(e: dict, name: str) -> dict:
    return (e.get("slots") or {}).get(name) or {}


def _brief(u: dict) -> list:
    out = []
    for e in u["effects"]:
        slots = {k: (v.get("prin"), v.get("prov"), v.get("roots"), (v.get("shape") or {}).get("const"))
                 for k, v in (e.get("slots") or {}).items()}
        out.append((e["kind"], e["site"], e.get("resolution"), e.get("http_method"), slots))
    return out


def _notes(u: dict, kind: str) -> list[str]:
    return [n for r in u["rows"] if r["kind"] == kind for n in r.get("notes", [])]


def _status(u: dict, kind: str, decl: str) -> str:
    """`kind` の行の宣言 `decl` の判定: 矛 / 不 / 内（tests/test_contradiction_principles.py と同じ読み方）。"""
    rows = [r for r in u["rows"] if r["kind"] == kind]
    assert rows, f"{u['unit']['qualname']}: {kind} の行が無い（効果行が消えている）: {_brief(u)}"
    notes = [n for r in rows for n in r.get("notes", [])]
    hit = any(n == f"contradiction:{decl}" for n in notes)
    unk = any(n.startswith(f"contradiction_unknown:{decl}:") for n in notes)
    assert not (hit and unk), f"{decl} が矛と不の両方: {notes}"
    if hit:
        assert any("CONTRADICTION" in r["verdicts"] for r in rows), "注記が矛なのに CONTRADICTION が無い"
        return "矛"
    return "不" if unk else "内"


def _reasons(u: dict, kind: str, decl: str) -> set[str]:
    out = set()
    for n in _notes(u, kind):
        for pre in (f"contradiction_reason:{decl}:", f"contradiction_unknown:{decl}:"):
            if n.startswith(pre):
                out.add(n[len(pre):])
    return out


def _check(u: dict, kind: str, decl: str, want: str, reason: str | None = None) -> None:
    got = _status(u, kind, decl)
    q = u["unit"]["qualname"]
    assert got == want, f"{q} {kind} {decl}: {got}（期待 {want}）notes={_notes(u, kind)} effects={_brief(u)}"
    if reason is not None:
        assert reason in _reasons(u, kind, decl), f"{q} {decl}: 理由 {_reasons(u, kind, decl)}（期待 {reason}）"


def _not_contra(u: dict, kind: str, decl: str) -> None:
    """誤警報の向きの反例の読み: 行が無いか、あっても矛にしない。"""
    if not [r for r in u["rows"] if r["kind"] == kind]:
        return
    got = _status(u, kind, decl)
    assert got != "矛", f"{u['unit']['qualname']} {decl}: 矛（誤警報）notes={_notes(u, kind)} effects={_brief(u)}"


def _not_clear_if_row(u: dict, kind: str, decl: str) -> None:
    """誤 clear の向きの反例の読み: 行が無い（今日の「不明」）か、あっても 内 にしない。"""
    if not [r for r in u["rows"] if r["kind"] == kind]:
        return
    got = _status(u, kind, decl)
    assert got in ("矛", "不"), f"{u['unit']['qualname']} {decl}: 内（誤 clear）notes={_notes(u, kind)} effects={_brief(u)}"


def _model_resolved(s: dict) -> bool:
    return s.get("prin") == "MODEL" and s.get("prov") == "resolved"


def _resolved_consts(v: dict) -> set:
    """値の形の中で確度 resolved の定数（Str の要素を含む）。"""
    out = set()
    if not v:
        return out
    shape = v.get("shape") or {}
    if v.get("prov") == "resolved" and "const" in shape:
        out.add(shape["const"])
    for it in shape.get("items") or []:
        out |= _resolved_consts(it)
    return out


# ===========================================================================
# 1. R4-r4-2 pydantic / dataclass で型付けした入口の仮引数
# ===========================================================================

PYD_MODELS = '''from pydantic import BaseModel


class XReq(BaseModel):
    path: str
'''

PYD_SERVER = '''import os
import subprocess
from dataclasses import dataclass
from typing import NamedTuple, Optional

from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP
from models import XReq

mcp = FastMCP("t")


class WriteReq(BaseModel):
    path: str = Field(description="file path")
    content: str


class CmdReq(BaseModel):
    cmd: str


@dataclass
class RmReq:
    path: str


class Target(BaseModel):
    path: str


class Req(BaseModel):
    target: Target
    argv: list[str]


class Base(BaseModel):
    path: str


class Derived(Base):
    content: str


class NtReq(NamedTuple):
    path: str


@mcp.tool(annotations={"destructiveHint": False})
def write_model(req: WriteReq) -> str:
    with open(req.path, "w") as f:
        f.write(req.content)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def sh_model(req: CmdReq) -> str:
    return str(os.system(req.cmd))


@mcp.tool(annotations={"destructiveHint": False})
def write_dc(req: RmReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def nested(req: Req, content: str) -> str:
    with open(req.target.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def argv_field(req: Req) -> str:
    return subprocess.run(req.argv, capture_output=True).stdout.decode()


@mcp.tool(annotations={"destructiveHint": False})
def optional_model(req: Optional[Derived] = None) -> str:
    if req is None:
        return "no"
    with open(req.path, "w") as f:
        f.write(req.content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def inherited(req: Derived) -> str:
    with open(req.path, "w") as f:
        f.write(req.content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_xmod(req: XReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_nt(req: NtReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_plain(path: str, content: str) -> str:
    # 対照
    with open(path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def sh_plain(cmd: str) -> str:
    # 対照
    return str(os.system(cmd))


@mcp.tool(annotations={"destructiveHint": False})
def write_dict(req: dict, content: str) -> str:
    # 対照: dict の添字は注釈に関係なく resolved のまま
    with open(req["path"], "w") as f:
        f.write(content)
    return "ok"
'''


@pytest.fixture(scope="module")
def pyd(tmp_path_factory):
    return _units(tmp_path_factory, "u23_pyd", {"models.py": PYD_MODELS, "server.py": PYD_SERVER})


@pytest.mark.parametrize(
    "tool,kind,decl,reason",
    [
        ("write_model", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("sh_model", "SPAWN", "D1", "spawn_model"),
        ("write_dc", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("nested", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("argv_field", "SPAWN", "D1", "spawn_model"),
        ("optional_model", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("inherited", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("write_xmod", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("write_nt", "FS_WRITE", "D2", "fs_writeout_model_path"),
    ],
)
def test_fix_pydantic_field_is_chosen(pyd, tool, kind, decl, reason):
    """R4-r4-2 / §9.3「選べる」: フックの無い木内の BaseModel / dataclass / NamedTuple のフィールドは MODEL/resolved →
    対照（平の仮引数）と同じ矛。入れ子（深さ 2）・list フィールド・Optional・木内の基底・別モジュールの定義を含む。"""
    _check(pyd[tool], kind, decl, "矛", reason)


def test_fix_pydantic_field_root_is_per_field(pyd):
    """R4-r4-2 fix_outline: フィールドの root はフィールドごと（`req.path`。主語一致 D25 / O34）。仮引数全体の `req` にしない。"""
    [e] = _effects(pyd["write_model"], "FS_WRITE")
    s = _slot(e, "path")
    assert _model_resolved(s), _brief(pyd["write_model"])
    assert s.get("roots") == ["req.path"], s


@pytest.mark.parametrize(
    "tool,kind,decl,reason",
    [
        ("write_plain", "FS_WRITE", "D2", "fs_writeout_model_path"),
        ("sh_plain", "SPAWN", "D1", "spawn_model"),
        ("write_dict", "FS_WRITE", "D2", "fs_writeout_model_path"),
    ],
)
def test_keep_pydantic_controls(pyd, tool, kind, decl, reason):
    """R4-r4-2 の対照（今正しい）: 平の仮引数と dict の添字は MODEL/resolved → 矛。"""
    _check(pyd[tool], kind, decl, "矛", reason)


PYD_HOOKS = '''import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import (
    AfterValidator,
    BaseModel,
    PrivateAttr,
    computed_field,
    field_validator,
    model_validator,
    root_validator,
    validator,
)

from extlib.models import RequestBase
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")
BASE = "/srv/data"
FIXED = "/srv/data/report.txt"
FLAG = os.environ.get("FLAG") == "1"


class ConfinedReq(BaseModel):
    path: str

    @field_validator("path")
    @classmethod
    def _confine(cls, v: str) -> str:
        return os.path.join(BASE, os.path.basename(v))


class FixedReq(BaseModel):
    path: str = ""

    @model_validator(mode="after")
    def _fix(self):
        self.path = FIXED
        return self


@dataclass
class PostReq:
    path: str

    def __post_init__(self):
        self.path = str((Path(BASE) / self.path).resolve())


def _confine(v: str) -> str:
    return os.path.join(BASE, os.path.basename(v))


class AnnReq(BaseModel):
    path: Annotated[str, AfterValidator(_confine)]


class V1Req(BaseModel):
    path: str

    @validator("path")
    def _v1(cls, v):
        return os.path.join(BASE, os.path.basename(v))


class RootReq(BaseModel):
    path: str

    @root_validator(pre=True)
    def _root(cls, values):
        values["path"] = FIXED
        return values


class PostInitReq(BaseModel):
    path: str

    def model_post_init(self, __context) -> None:
        self.path = FIXED


class InitReq(BaseModel):
    path: str

    def __init__(self, **data):
        data["path"] = FIXED
        super().__init__(**data)


class HookBase(BaseModel):
    path: str

    @field_validator("path")
    @classmethod
    def _confine(cls, v: str) -> str:
        return os.path.join(BASE, os.path.basename(v))


class HookDerived(HookBase):
    content: str


class ExtReq(RequestBase):
    path: str


if FLAG:
    class TwiceReq(BaseModel):
        path: str
else:
    class TwiceReq(BaseModel):
        path: str

        @field_validator("path")
        @classmethod
        def _confine(cls, v: str) -> str:
            return os.path.join(BASE, os.path.basename(v))


class ClassVarReq(BaseModel):
    OUT: ClassVar[str] = FIXED
    name: str


class UnderReq(BaseModel):
    _out: str = FIXED
    name: str


class PrivReq(BaseModel):
    _out: str = PrivateAttr(default=FIXED)
    name: str


@dataclass
class InitFalseReq:
    name: str
    out: str = field(init=False, default=FIXED)


class PropReq(BaseModel):
    name: str

    @property
    def out(self) -> str:
        return FIXED


class ComputedReq(BaseModel):
    name: str

    @computed_field
    @property
    def out(self) -> str:
        return FIXED


@mcp.tool(annotations={"destructiveHint": False})
def write_confined(req: ConfinedReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_fixed(req: FixedReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_post(req: PostReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_ann(req: AnnReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_v1(req: V1Req, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_root(req: RootReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_post_init(req: PostInitReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_init(req: InitReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_base_hook(req: HookDerived) -> str:
    with open(req.path, "w") as f:
        f.write(req.content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_ext(req: ExtReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_twice(req: TwiceReq, content: str) -> str:
    with open(req.path, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_classvar(req: ClassVarReq, content: str) -> str:
    with open(req.OUT, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_under(req: UnderReq, content: str) -> str:
    with open(req._out, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_priv(req: PrivReq, content: str) -> str:
    with open(req._out, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_init_false(req: InitFalseReq, content: str) -> str:
    with open(req.out, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_prop(req: PropReq, content: str) -> str:
    with open(req.out, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_computed(req: ComputedReq, content: str) -> str:
    with open(req.out, "w") as f:
        f.write(content)
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def write_plain_confined(path: str, content: str) -> str:
    # 対照: 同じ変換を本体に書く（モデリングした操作 → resolved → 矛）
    with open(os.path.join(BASE, os.path.basename(path)), "w") as f:
        f.write(content)
    return "ok"
'''


@pytest.fixture(scope="module")
def hooks(tmp_path_factory):
    return _units(tmp_path_factory, "u23_hooks", {"server.py": PYD_HOOKS})


@pytest.mark.parametrize(
    "tool",
    [
        # 検証役の反例 ce_pydantic_hooks の 4 形
        "write_confined",
        "write_fixed",
        "write_post",
        "write_ann",
        # fix_outline の「フック」の残り（validator / root_validator / model_post_init / __init__）と、家族の基底のフック
        "write_v1",
        "write_root",
        "write_post_init",
        "write_init",
        "write_base_hook",
        # 外部の基底（フックが読めない）と、クラス名の二重束縛（D61 追記の条件で厳密に解けない）
        "write_ext",
        "write_twice",
    ],
)
def test_keep_pydantic_hooks_stay_unknown(hooks, tool):
    """R4-r4-2 の反例（ce_pydantic_hooks ほか）: 構築時フックがある / 家族を読めない / 解けないクラスは今どおり
    MODEL に opaque を合流 → §9.3 で 不（fs_writeout_model_path_opaque）。無条件に resolved にすると矛（誤警報）になる。"""
    u = hooks[tool]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


@pytest.mark.parametrize(
    "tool",
    ["write_classvar", "write_under", "write_priv", "write_init_false", "write_prop", "write_computed"],
)
def test_keep_pydantic_non_fields_not_model_chosen(hooks, tool):
    """R4-r4-2 fix_outline の除外: ClassVar / `_` 始まり / PrivateAttr / `field(init=False)` / property / computed_field は
    モデルが埋めるフィールドではない（値は OP の定数 FIXED）。MODEL/resolved にして矛を出すと誤警報。"""
    u = hooks[tool]
    _not_contra(u, "FS_WRITE", "D2")
    for e in _effects(u, "FS_WRITE"):
        assert not _model_resolved(_slot(e, "path")), _brief(u)


def test_keep_pydantic_hook_control(hooks):
    """ce_pydantic_hooks の対照: 同じ変換を本体に書けばモデリングした操作なので MODEL/resolved → 矛（今正しい）。"""
    _check(hooks["write_plain_confined"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


# ---------------------------------------------------------------------------
# 1b. langroid の message_fields（fix_outline:「同じ穴があるので同じ条件を入れる」）
# ---------------------------------------------------------------------------

LANGROID_SRC = '''import os

from langroid.agent.chat_agent import ChatAgent
from langroid.agent.tool_message import ToolMessage
from pydantic import field_validator

BASE = "/srv/data"


class WriteMsg(ToolMessage):
    request: str = "write_file"
    purpose: str = "write"
    path: str
    content: str


class ConfinedMsg(ToolMessage):
    request: str = "write_confined"
    purpose: str = "write"
    path: str
    content: str

    @field_validator("path")
    @classmethod
    def _confine(cls, v: str) -> str:
        return os.path.join(BASE, os.path.basename(v))


class Agent(ChatAgent):
    def write_file(self, msg: WriteMsg) -> str:
        with open(msg.path, "w") as f:
            f.write(msg.content)
        return "ok"

    def write_confined(self, msg: ConfinedMsg) -> str:
        with open(msg.path, "w") as f:
            f.write(msg.content)
        return "ok"
'''


@pytest.fixture(scope="module")
def lr(tmp_path_factory):
    return _units(tmp_path_factory, "u23_langroid", {"agent.py": LANGROID_SRC})


def test_fix_langroid_hook_field_is_opaque(lr):
    """R4-r4-2 fix_outline（langroid にも同じ条件）/ §9.3: field_validator が構築時に path を変換するので、
    `msg.path` は MODEL に opaque を合流する（今は MODEL/resolved）。"""
    u = lr["Agent.write_confined"]
    effs = _effects(u, "FS_WRITE")
    assert effs, _brief(u)
    for e in effs:
        s = _slot(e, "path")
        assert s.get("prin") == "MODEL" and s.get("prov") != "resolved", _brief(u)


def test_keep_langroid_plain_field_is_chosen(lr):
    """langroid の message_fields（フック無し）は今どおり MODEL/resolved、root はフィールドごと（`msg.path`）。"""
    u = lr["Agent.write_file"]
    [e] = _effects(u, "FS_WRITE")
    s = _slot(e, "path")
    assert _model_resolved(s) and s.get("roots") == ["msg.path"], _brief(u)


# ===========================================================================
# 2. R4-r1-6 Path 注釈の入口の仮引数
# ===========================================================================

PATH_FIX = '''import pathlib
from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def write_p(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def write_p2(path: pathlib.Path, text: str) -> str:
    path.write_text(text)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def unlink_p(path: Path) -> str:
    path.unlink()
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def write_str_control(path: str, text: str) -> str:
    Path(path).write_text(text)
    return "ok"
'''


@pytest.fixture(scope="module")
def pth(tmp_path_factory):
    return _units(tmp_path_factory, "u23_path", {"server.py": PATH_FIX})


@pytest.mark.parametrize(
    "tool,site",
    [
        ("write_p", "pathlib.Path.write_text"),
        ("write_p2", "pathlib.Path.write_text"),
        ("unlink_p", "pathlib.Path.unlink"),
    ],
)
def test_fix_path_annotation_types_receiver(pth, tool, site):
    """R4-r1-6 / §7.1: `from pathlib import Path` / `import pathlib` に厳密に解ける注釈の入口引数は Path 形 →
    pathlib の sink が受け手型で当たり、readOnly × FS_WRITE で D1 矛（対照 write_str_control と同じ）。
    主体と root は変えない（MODEL/resolved、roots=path）。"""
    u = pth[tool]
    effs = [e for e in _effects(u, "FS_WRITE") if e["site"] == site]
    assert effs, _brief(u)
    s = _slot(effs[0], "path")
    assert _model_resolved(s) and s.get("roots") == ["path"], _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")


def test_keep_path_str_control(pth):
    """R4-r1-6 の対照（今正しい）: `Path(path)` の構築は Path 形 → D1 矛。"""
    u = pth["write_str_control"]
    assert [e for e in _effects(u, "FS_WRITE") if e["site"] == "pathlib.Path.write_text"], _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")


# 反例 ce6_intree_path（木内の `class Path`。write_text は HTTP POST）
PATH_CE6 = '''import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


class Path:
    """木の中の `Path`（遠隔ストレージのキー）。pathlib ではない。"""

    def __init__(self, key: str) -> None:
        self.key = key

    def write_text(self, text: str) -> None:
        requests.post("https://store.example.com/put", json={"key": self.key, "text": text})


@mcp.tool(annotations={"readOnlyHint": True})
def put_object(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"
'''

_REMOTE_PATH = '''import requests


class Path:
    def __init__(self, key: str) -> None:
        self.key = key

    def write_text(self, text: str) -> None:
        requests.post("https://store.example.com/put", json={"key": self.key, "text": text})
'''

# 相対 import の `Path`（木内パッケージの利用者定義クラス）
PATH_REL_SERVER = '''from mcp.server.fastmcp import FastMCP

from .compat import Path

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def put_rel(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"
'''

# 木内モジュールからの絶対 import の `Path`
PATH_INTREE_SERVER = '''from mcp.server.fastmcp import FastMCP

from store_compat import Path

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def put_intree(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"
'''

# モジュール直下で 2 回束縛される `Path`（最後の束縛は外部の remote_store）
PATH_TWICE_SERVER = '''from pathlib import Path

from mcp.server.fastmcp import FastMCP
from remote_store import Path

mcp = FastMCP("t")


@mcp.tool(annotations={"readOnlyHint": True})
def put_twice(path: Path, text: str) -> str:
    path.write_text(text)
    return "ok"
'''


@pytest.fixture(scope="module")
def pth_keep(tmp_path_factory):
    # ce6 は単独の木にする（同名の `class Path` が他のモジュールにもあると、末尾名の降下が曖昧になって NET も消える）
    units = _units(tmp_path_factory, "u23_path_ce6", {"server.py": PATH_CE6})
    return units | _units(
        tmp_path_factory,
        "u23_path_keep",
        {
            "pkg/__init__.py": "",
            "pkg/compat.py": _REMOTE_PATH,
            "pkg/server.py": PATH_REL_SERVER,
            "store_compat.py": _REMOTE_PATH,
            "intree_server.py": PATH_INTREE_SERVER,
            "twice_server.py": PATH_TWICE_SERVER,
        },
    )


@pytest.mark.parametrize("tool", ["put_object", "put_rel", "put_intree", "put_twice"])
def test_keep_path_annotation_not_pathlib(pth_keep, tool):
    """R4-r1-6 の反例 ce6_intree_path ほか: 注釈の先頭名が pathlib に厳密に解けない（木内の `class Path`・相対 import・
    木内モジュール・二重束縛）なら pathlib の FS_WRITE を足さない（足すと readOnly への D1 の誤警報）。"""
    u = pth_keep[tool]
    assert not [e for e in u["effects"] if e["site"].startswith("pathlib.")], _brief(u)
    assert not _effects(u, "FS_WRITE"), _brief(u)


def test_keep_path_ce6_net_is_kept(pth_keep):
    """ce6_intree_path: 木内の `Path.write_text` の NET（requests.post）は今どおり出る（§7.1 readOnly × POST → D1 不 net_post）。"""
    u = pth_keep["put_object"]
    assert _effects(u, "NET"), _brief(u)
    _check(u, "NET", "D1", "不", "net_post")


# ===========================================================================
# 3. R4-r4-1 lifespan の yield 値（`ctx.request_context.lifespan_context` / `server.request_context.lifespan_context`）
# ===========================================================================

LS_DC = '''import sqlite3
import subprocess
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

import httpx

from mcp.server.fastmcp import Context, FastMCP


@dataclass
class AppContext:
    db: sqlite3.Connection
    client: httpx.Client
    tool_path: str


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    db = sqlite3.connect("/data/app.db")
    client = httpx.Client(base_url="https://api.example.com")
    with open("/var/run/app.pid", "w") as fh:
        fh.write("1")
    try:
        yield AppContext(db=db, client=client, tool_path="/usr/bin/helper")
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)
other = FastMCP("o")
DB = sqlite3.connect("/data/app.db")
CLIENT = httpx.Client(base_url="https://api.example.com")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_attr(item_id: str, ctx: Context) -> str:
    db = ctx.request_context.lifespan_context.db
    db.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_const(ctx: Context) -> str:
    ctx.request_context.lifespan_context.db.execute("DELETE FROM items")
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_attr(item: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context.client.request("DELETE", "/items/" + item)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def spawn_via_ctx(arg: str, ctx: Context) -> str:
    subprocess.run([ctx.request_context.lifespan_context.tool_path, arg])
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_module(item_id: str) -> str:
    # 対照: モジュール水準の接続
    DB.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def net_module(item: str) -> str:
    # 対照: モジュール水準のクライアント
    CLIENT.request("DELETE", "/items/" + item)
    return "ok"


@other.tool(annotations={"readOnlyHint": True})
def purge_other(item_id: str, ctx: Context) -> str:
    # 別のインスタンス（lifespan= なし）のツール: mcp の lifespan を種にしない
    ctx.request_context.lifespan_context.db.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

LS_DICT = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    db = sqlite3.connect("/data/app.db")
    try:
        yield {"db": db}
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)
DB = sqlite3.connect("/data/app.db")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_dict(item_id: str, ctx: Context) -> str:
    db = ctx.request_context.lifespan_context["db"]
    db.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_dict_module(item_id: str) -> str:
    # 対照
    DB.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

LS_FM2 = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from fastmcp import Context, FastMCP


@dataclass
class AppContext:
    db: sqlite3.Connection


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    db = sqlite3.connect("/data/app.db")
    try:
        yield AppContext(db=db)
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)
DB = sqlite3.connect("/data/app.db")


@mcp.tool(annotations={"readOnlyHint": True})
def purge_fm2(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context.db.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def purge_fm2_module(item_id: str) -> str:
    # 対照
    DB.execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
'''

LS_LOW = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from mcp.server import Server
from mcp.types import TextContent, Tool, ToolAnnotations


@asynccontextmanager
async def lifespan(server: Server) -> AsyncIterator[dict]:
    db = sqlite3.connect("/data/app.db")
    try:
        yield {"db": db}
    finally:
        db.close()


server = Server("t", lifespan=lifespan)


@server.list_tools()
async def list_tools():
    return [
        Tool(name="purge", description="purge", inputSchema={}, annotations=ToolAnnotations(readOnlyHint=True)),
    ]


@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "purge":
        db = server.request_context.lifespan_context["db"]
        db.execute("DELETE FROM items WHERE id = " + arguments["id"])
        return [TextContent(type="text", text="ok")]
    raise ValueError(name)
'''


@pytest.fixture(scope="module")
def ls(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_dc", {"server.py": LS_DC})


@pytest.fixture(scope="module")
def ls_dict(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_dict", {"server.py": LS_DICT})


@pytest.fixture(scope="module")
def ls_fm2(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_fm2", {"server.py": LS_FM2})


@pytest.fixture(scope="module")
def ls_low(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_low", {"server.py": LS_LOW})


def test_keep_ls_module_controls(ls, ls_dict, ls_fm2):
    """R4-r4-1 の対照（今正しい）: モジュール水準の接続・クライアントは受け手型が付き、readOnly に対して D1 矛。"""
    _check(ls["purge_module"], "DB", "D1", "矛")
    _check(ls["net_module"], "NET", "D1", "矛", "net_modify")
    _check(ls_dict["purge_dict_module"], "DB", "D1", "矛")
    _check(ls_fm2["purge_fm2_module"], "DB", "D1", "矛")


def test_fix_ls_dataclass_attr_db(ls):
    """R4-r4-1 / §9.4 の 2: yield した `AppContext(db=...)` の `.db` は sqlite3 の接続（確度は opaque でも受け手型は残る）。
    SQL は MODEL を連結 → 対照 purge_module と同じ D1 矛・同じ理由。"""
    u = ls["purge_attr"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")
    assert _reasons(u, "DB", "D1") == _reasons(ls["purge_module"], "DB", "D1")


def test_fix_ls_const_delete(ls):
    """R4-r4-1 / §7.1: 本体の定数 `DELETE FROM items` は resolved の定数（lifespan の値ではない）→ D1 矛 db_modify。"""
    _check(ls["purge_const"], "DB", "D1", "矛", "db_modify")


def test_fix_ls_net_client(ls):
    """R4-r4-1: lifespan の httpx クライアントの `request("DELETE", ...)` → 対照 net_module と同じ D1 矛 net_modify
    （今は NET の行もサイトの痕跡も無い）。"""
    u = ls["net_attr"]
    assert _effects(u, "NET"), _brief(u)
    _check(u, "NET", "D1", "矛", "net_modify")


def test_fix_ls_dict_subscript(ls_dict):
    """R4-r4-1: dict を yield する形の `lifespan_context["db"]` も同じ（対照 purge_dict_module と同じ判定）。"""
    u = ls_dict["purge_dict"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")
    assert _reasons(u, "DB", "D1") == _reasons(ls_dict["purge_dict_module"], "DB", "D1")


def test_fix_ls_fastmcp2(ls_fm2):
    """R4-r4-1 fix_outline: fastmcp 2.x（`from fastmcp import Context, FastMCP`）の同じ形。"""
    u = ls_fm2["purge_fm2"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")


def test_fix_ls_lowlevel(ls_low):
    """R4-r4-1: 低レベル `Server(lifespan=...)` の `server.request_context.lifespan_context["db"]` も同じ DB 行と D1 矛
    （`arguments["id"]` は MODEL/resolved）。"""
    u = ls_low["call_tool"]
    assert _effects(u, "DB"), _brief(u)
    _check(u, "DB", "D1", "矛")


def test_keep_ls_no_startup_effects(ls):
    """R4-r4-1 fix_outline（`_descend_env` を `on_call=None`）: lifespan 本体の起動時の効果（pid ファイルの書き込み・
    接続）はツールに付けない。readOnly のツールに起動時の FS_WRITE を付けると D1 の誤警報になる。"""
    for tool in ("purge_attr", "purge_const", "net_attr", "spawn_via_ctx"):
        u = ls[tool]
        assert not _effects(u, "FS_WRITE"), (tool, _brief(u))


def test_keep_ls_spawn_argv0_not_chosen(ls):
    """R4-r4-1 条件 (4) / §7.1 SPAWN: lifespan の `tool_path` はモデルが選べない（今は ctx 根の MODEL/opaque、直した後は
    OP/opaque）。どちらでも argv0 は「選べる」でないので D1 は 不（内 にも 矛 にもしない）。"""
    _check(ls["spawn_via_ctx"], "SPAWN", "D1", "不")


def test_keep_ls_ctx_is_still_model_param(ls):
    """R2-r1-10 は直さない: `ctx` は凍結した語彙のもとで入口の仮引数（MODEL）のまま。ユニットの params から外さない。"""
    names = [p["name"] for p in ls["purge_attr"]["unit"]["params"]]
    assert "ctx" in names and "item_id" in names, names


def test_keep_ls_other_instance_not_seeded(ls):
    """R4-r4-1 条件 (2): 種は装飾子の受け手の**自分の**構築式の `lifespan=` からだけ置く。lifespan の無い別の
    インスタンス `other` のツールに `mcp` の yield 値を種付けしない（DB 行を出さない）。"""
    u = ls["purge_other"]
    assert not _effects(u, "DB"), _brief(u)


# 反例 ce_lifespan_rebound（共有の可変状態に別のツールが MODEL を書き込む）
LS_REBOUND = '''import sqlite3
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    db = sqlite3.connect("/data/app.db")
    client = httpx.Client(base_url="https://api.example.com")
    try:
        yield {"db": db, "client": client, "sql": "SELECT 1", "method": "GET"}
    finally:
        db.close()


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool()
def set_query(sql: str, method: str, ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["sql"] = sql
    st["method"] = method
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def run_saved(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["db"].execute(st["sql"])
    return "ok"


@mcp.tool(annotations={"readOnlyHint": True})
def call_saved(ctx: Context) -> str:
    st = ctx.request_context.lifespan_context
    st["client"].request(st["method"], "/items")
    return "ok"
'''


@pytest.fixture(scope="module")
def ls_rebound(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_rebound", {"server.py": LS_REBOUND})


def test_keep_ls_rebound_not_clear(ls_rebound):
    """反例 ce_lifespan_rebound: lifespan_context は呼び出しをまたぐ可変の共有状態。起動時の定数 "SELECT 1" / "GET" を
    resolved で読むと READ / HTTP_SAFE → 内（新しい誤 clear）。行が無い（今）か、あっても 内 にせず、定数を resolved で読まない。"""
    run_saved, call_saved = ls_rebound["run_saved"], ls_rebound["call_saved"]
    _not_clear_if_row(run_saved, "DB", "D1")
    _not_clear_if_row(call_saved, "NET", "D1")
    for e in _effects(run_saved, "DB"):
        assert "SELECT 1" not in _resolved_consts(_slot(e, "sql")), _brief(run_saved)
    for e in _effects(call_saved, "NET"):
        assert e.get("http_method") not in ("GET", "HEAD", "OPTIONS"), _brief(call_saved)


def test_fix_ls_rebound_unreadable_const(ls_rebound):
    """R4-r4-1 fix_outline 条件 (1): `_opaque_deep` なら受け手型は残り（DB / NET の行が出る）、共有状態の定数は読めない →
    DB は D1 不 db_sql_unreadable、NET は D1 不（メソッドが読めない）。"""
    run_saved, call_saved = ls_rebound["run_saved"], ls_rebound["call_saved"]
    assert _effects(run_saved, "DB"), _brief(run_saved)
    _check(run_saved, "DB", "D1", "不", "db_sql_unreadable")
    assert _effects(call_saved, "NET"), _brief(call_saved)
    _check(call_saved, "NET", "D1", "不")


# 条件 (2) / (3) の反例: 種を置かない形（今日と同じく DB 行 0 のまま）
LS_NOSEED = {
    # lifespan= が partial（名前ではない）
    "partial_srv.py": '''import functools
import sqlite3
from contextlib import asynccontextmanager

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server, path):
    yield {"db": sqlite3.connect(path)}


mcp = FastMCP("t", lifespan=functools.partial(app_lifespan, path="/data/app.db"))


@mcp.tool(annotations={"readOnlyHint": True})
def purge_partial(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
''',
    # lifespan= が工場関数の呼び出し
    "factory_srv.py": '''import sqlite3
from contextlib import asynccontextmanager

from mcp.server.fastmcp import Context, FastMCP


def make_lifespan(path):
    @asynccontextmanager
    async def _ls(server):
        yield {"db": sqlite3.connect(path)}

    return _ls


mcp = FastMCP("t", lifespan=make_lifespan("/data/app.db"))


@mcp.tool(annotations={"readOnlyHint": True})
def purge_factory(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
''',
    # 利用者定義の `Context`（同じモジュールのクラス。mcp の Context ではない）
    "userctx_srv.py": '''import sqlite3
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP


@asynccontextmanager
async def app_lifespan(server):
    yield {"db": sqlite3.connect("/data/app.db")}


class Context:
    request_context: dict


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool(annotations={"readOnlyHint": True})
def purge_userctx(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
''',
    # `Context` がモジュール直下で 2 回束縛（最後は利用者定義）
    "twicectx_srv.py": '''import sqlite3
from contextlib import asynccontextmanager

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server):
    yield {"db": sqlite3.connect("/data/app.db")}


class Context:  # noqa: F811
    request_context: dict


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool(annotations={"readOnlyHint": True})
def purge_twicectx(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
''',
    # 相対 import の `Context`（木内パッケージの利用者定義クラス）
    "rpkg/__init__.py": "",
    "rpkg/ctxmod.py": '''class Context:
    request_context: dict
''',
    "rpkg/server.py": '''import sqlite3
from contextlib import asynccontextmanager

from mcp.server.fastmcp import FastMCP

from .ctxmod import Context


@asynccontextmanager
async def app_lifespan(server):
    yield {"db": sqlite3.connect("/data/app.db")}


mcp = FastMCP("t", lifespan=app_lifespan)


@mcp.tool(annotations={"readOnlyHint": True})
def purge_relctx(item_id: str, ctx: Context) -> str:
    ctx.request_context.lifespan_context["db"].execute("DELETE FROM items WHERE id = " + item_id)
    return "ok"
''',
}


@pytest.fixture(scope="module")
def ls_noseed(tmp_path_factory):
    return _units(tmp_path_factory, "u23_ls_noseed", LS_NOSEED)


@pytest.mark.parametrize(
    "tool", ["purge_partial", "purge_factory", "purge_userctx", "purge_twicectx", "purge_relctx"]
)
def test_keep_ls_not_seeded_outside_conditions(ls_noseed, tool):
    """R4-r4-1 条件 (2)（`lifespan=` が木内の CM 関数名のときだけ。partial / 工場関数では何もしない）と条件 (3)
    （`Context` は mcp / fastmcp のものに厳密に解けるときだけ。利用者定義・二重束縛・相対 import には付けない）:
    今日と同じく DB 行を出さない。"""
    u = ls_noseed[tool]
    assert not _effects(u, "DB"), _brief(u)


# ===========================================================================
# 4. R2-r1-10（直さない）: ctx は MODEL の仮引数のまま
# ===========================================================================

C10 = {
    # 検証役の反例 c10_sampling: サンプリングの結果（LLM が生成した文字列）を SQL に連結
    "sampling/server.py": '''import sqlite3

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import SamplingMessage, TextContent, ToolAnnotations

mcp = FastMCP("t")
conn = sqlite3.connect("notes.db")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def lookup(topic: str, ctx: Context) -> str:
    r = await ctx.session.create_message(
        messages=[SamplingMessage(role="user", content=TextContent(type="text", text="pick a note title"))],
        max_tokens=50,
    )
    title = r.content.text
    rows = conn.execute("SELECT body FROM notes WHERE title = '" + title + "'").fetchall()
    return str(rows)
''',
    # c10_lifespan: `lifespan=` の無いインスタンスでは lifespan_context の値は ctx 根の MODEL のまま
    "nolifespan/server.py": '''import sqlite3

from mcp.server.fastmcp import Context, FastMCP
from mcp.types import ToolAnnotations

mcp = FastMCP("t")
conn = sqlite3.connect("notes.db")


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True))
async def lookup_table(topic: str, ctx: Context) -> str:
    table = ctx.request_context.lifespan_context.table
    rows = conn.execute("SELECT body FROM " + table).fetchall()
    return str(rows)
''',
}


@pytest.fixture(scope="module")
def c10(tmp_path_factory):
    return _units(tmp_path_factory, "u23_c10", C10)


def test_keep_c10_sampling_stays_unknown(c10):
    """R2-r1-10 の反例 c10_sampling（学生の決定: 直さない）: サンプリング結果は ctx の MODEL の種だけが MODEL に保つ。
    SELECT の接頭辞 + MODEL/opaque の SQL → §9.4 で D1 不 db_sql_model_opaque（ctx を OP にすると READ → 内 の誤 clear）。"""
    u = c10["lookup"]
    _check(u, "DB", "D1", "不", "db_sql_model_opaque")
    for e in _effects(u, "DB"):
        assert _slot(e, "sql").get("prin") == "MODEL", _brief(u)


def test_keep_c10_no_lifespan_kwarg(c10):
    """c10_lifespan / R4-r4-1 条件 (2): `FastMCP("t")` に `lifespan=` が無いので種を置かない。ctx 根の MODEL/opaque のまま
    D1 不 db_sql_model_opaque（内 にしない）。"""
    _check(c10["lookup_table"], "DB", "D1", "不", "db_sql_model_opaque")
