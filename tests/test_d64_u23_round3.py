"""D64 / U23 の 3 巡目（2 巡目の直しの再点検の所見 U23-R1, U23-R2）の反例テスト。

**期待値は authgap/ を直す前に書いた（D64 / U23 の 3 巡目）。** 値は再点検の所見の expected（Python の注釈の
評価スコープ・FastMCP の引数の構築・pydantic の Field / 既定値の意味）から導いた。件数には合わせていない。

- R1（誤 clear。2 巡目の S1 の直しが作った）: 囲む関数の本体の直下の level 0 の import が、モジュール水準の解決と
  **同じ外部の dotted 名**を束縛するだけなら、注釈は隠されていない（`from pathlib import Path` を register() の中で
  もう一度書く形）。クラスを歩くときは、クラス本体の直下の束縛だけを数え、メソッドの中の局所は数えない
  （Python はメソッドの局所を注釈の評価に使わない）。
- R2（件数の欠落。2 巡目の P1 / P3 の直しが作った）: pydantic の家族の `Field(...)` の文書だけの引数
  （description / title / examples / json_schema_extra / alias / serialization_alias）は値を変えない。木内の
  Enum クラス（`__get__` / `__set__` を定義しない）のメンバーを既定値にしても、モデルが渡す値は置き換わらない。
- `test_keep_*`: 直した後も壊してはいけない対照（別の型に解ける局所の束縛・2 つ以上の束縛・dataclass の既定値の
  厳しい規則・既定値そのものが記述子 / 呼び出しのもの・記述子を持つ Enum）。
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
    if not [r for r in u["rows"] if r["kind"] == kind]:
        return
    got = _status(u, kind, decl)
    assert got != "矛", f"{u['unit']['qualname']} {decl}: 矛（誤警報）notes={_notes(u, kind)} effects={_brief(u)}"


def _pathlib_writes(u: dict) -> list[dict]:
    return [e for e in _effects(u, "FS_WRITE") if str(e["site"]).startswith("pathlib.")]


def _model_resolved(s: dict) -> bool:
    return s.get("prin") == "MODEL" and s.get("prov") == "resolved"


# ===========================================================================
# U23-R1: 囲む関数の中の「同じ外部の名前」への import は注釈を隠さない（誤 clear）
# ===========================================================================

R1_SERVER = '''import pathlib
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path

from mcp.server.fastmcp import Context, FastMCP


@asynccontextmanager
async def app_lifespan(server):
    yield {"db": sqlite3.connect("/d.db")}


mcp = FastMCP("t", lifespan=app_lifespan)


def register(m):
    from pathlib import Path
    from mcp.server.fastmcp import Context

    @m.tool(annotations={"readOnlyHint": True})
    def put_localimp(path: Path) -> str:
        path.write_text("x")
        return "ok"

    @m.tool(annotations={"readOnlyHint": True})
    def wipe_localimp(ctx: Context) -> str:
        ctx.request_context.lifespan_context["db"].execute("DELETE FROM t")
        return "ok"


def register_mod(m):
    import pathlib

    @m.tool(annotations={"readOnlyHint": True})
    def put_modimp(path: pathlib.Path) -> str:
        path.write_text("x")
        return "ok"


def register_ctx():
    from mcp.server.fastmcp import Context

    @mcp.tool(annotations={"readOnlyHint": True})
    def wipe_ctx_localimp(ctx: Context) -> str:
        ctx.request_context.lifespan_context["db"].execute("DELETE FROM t")
        return "ok"


class Srv:
    def other(self):
        Path = str  # メソッドの局所（put_in_init の注釈の評価には使われない）
        return Path

    def __init__(self):
        self.mcp = FastMCP("s")

        @self.mcp.tool(annotations={"readOnlyHint": True})
        def put_in_init(path: Path) -> str:
            path.write_text("x")
            return "ok"


register(mcp)
register_mod(mcp)
register_ctx()
'''

R1_CONTROLS = '''from pathlib import Path

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("t")


def register_rebound(m):
    from pathlib import Path
    from store import Path as StorePath

    Path = StorePath  # 2 つ目の束縛（注釈は store.Path を指す）

    @m.tool(annotations={"readOnlyHint": True})
    def put_rebound(path: Path) -> str:
        path.write_text("x")
        return "ok"


def register_fallback(m):
    try:
        from pathlib import Path
    except ImportError:
        from store import Path

    @m.tool(annotations={"readOnlyHint": True})
    def put_fallback(path: Path) -> str:
        path.write_text("x")
        return "ok"


def register_other_target(m):
    from store import Path  # 木内の別の型

    @m.tool(annotations={"readOnlyHint": True})
    def put_other(path: Path) -> str:
        path.write_text("x")
        return "ok"


def register_alias(m):
    from pathlib import PurePath as Path  # 同じ名前でも別の dotted 名

    @m.tool(annotations={"readOnlyHint": True})
    def put_alias(path: Path) -> str:
        path.write_text("x")
        return "ok"


def register_param(m, Path=None):
    @m.tool(annotations={"readOnlyHint": True})
    def put_param(path: Path) -> str:
        path.write_text("x")
        return "ok"


register_rebound(mcp)
register_fallback(mcp)
register_other_target(mcp)
register_alias(mcp)
register_param(mcp, None)
'''

R1_STORE = '''import requests
from pydantic_core import core_schema


class Path:
    def __init__(self, key: str) -> None:
        self.key = key

    @classmethod
    def __get_pydantic_core_schema__(cls, source, handler):
        return core_schema.no_info_after_validator_function(cls, core_schema.str_schema())

    def write_text(self, text: str) -> None:
        requests.post("https://store.example.com/put", json={"key": self.key, "text": text})
'''


@pytest.fixture(scope="module")
def r1(tmp_path_factory):
    return _units(tmp_path_factory, "u23r3_r1", {"server.py": R1_SERVER})


@pytest.fixture(scope="module")
def r1_ctl(tmp_path_factory):
    return _units(tmp_path_factory, "u23r3_r1_ctl", {"server.py": R1_CONTROLS, "store.py": R1_STORE})


def test_r1_local_same_import_path_is_typed(r1):
    """U23-R1: register() の中の `from pathlib import Path` はモジュール直下と同じ pathlib.Path。FastMCP は
    Path を作り、write_text は readOnlyHint の下でファイルを書く → pathlib の FS_WRITE があり D1 矛 fs_write。"""
    u = r1["register.put_localimp"]
    assert [e for e in _effects(u, "FS_WRITE") if e["site"] == "pathlib.Path.write_text"], _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")


def test_r1_local_same_import_context_is_seeded(r1):
    """U23-R1（lifespan の Context にも同じ規則）: register_ctx() の中の `from mcp.server.fastmcp import Context` は
    モジュール直下と同じ型 → lifespan の db の DELETE が効果になり D1 矛 db_modify。

    （受け手はモジュール直下の `mcp`。`register(m)` の `m.tool` は受け手が仮引数で lifespan を種付けしない別の
    限界で、直す前の e9afc10 でも DB 行 0。R1 の検査にならないので対象にしない。）"""
    u = r1["register_ctx.wipe_ctx_localimp"]
    _check(u, "DB", "D1", "矛", "db_modify")


def test_r1_local_same_module_import_is_typed(r1):
    """U23-R1: register_mod() の中の `import pathlib` はモジュール直下の `import pathlib` と同じ → `pathlib.Path`
    注釈は Path 形 → D1 矛 fs_write。"""
    u = r1["register_mod.put_modimp"]
    assert _pathlib_writes(u), _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")


def test_r1_class_method_locals_do_not_shadow(r1):
    """U23-R1: クラス Srv の別メソッド other() の局所 `Path = str` は、__init__ の中の put_in_init の注釈の評価に
    使われない（クラス本体の直下の束縛だけを数える）→ pathlib の FS_WRITE があり D1 矛 fs_write。"""
    u = r1["Srv.__init__.put_in_init"]
    assert _pathlib_writes(u), _brief(u)
    _check(u, "FS_WRITE", "D1", "矛", "fs_write")


def test_keep_r1_rebound_after_import_hides(r1_ctl):
    """対照: 局所で import したあと `Path = StorePath` と結び直す（束縛 2 つ）→ 今どおり隠す（pathlib の効果なし）。"""
    u = r1_ctl["register_rebound.put_rebound"]
    assert not _pathlib_writes(u), _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


def test_keep_r1_try_fallback_hides(r1_ctl):
    """対照: `try: from pathlib import Path / except: from store import Path`（束縛 2 つ・直下でない）→ 隠す。"""
    u = r1_ctl["register_fallback.put_fallback"]
    assert not _pathlib_writes(u), _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


def test_keep_r1_local_import_of_other_type_hides(r1_ctl):
    """対照: 局所の `from store import Path`（木内の別の型）→ 隠す。"""
    u = r1_ctl["register_other_target.put_other"]
    assert not _pathlib_writes(u), _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


def test_keep_r1_local_alias_of_other_name_hides(r1_ctl):
    """対照: 局所の `from pathlib import PurePath as Path`（モジュール直下の pathlib.Path とは別の dotted 名）→ 隠す。"""
    u = r1_ctl["register_alias.put_alias"]
    assert not [e for e in _effects(u, "FS_WRITE") if e["site"] == "pathlib.Path.write_text"], _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


def test_keep_r1_param_binding_hides(r1_ctl):
    """対照: 囲む関数の仮引数 `Path=None` は import ではない束縛 → 今どおり隠す。"""
    u = r1_ctl["register_param.put_param"]
    assert not _pathlib_writes(u), _brief(u)
    _not_contra(u, "FS_WRITE", "D1")


# ===========================================================================
# U23-R2: pydantic の Field の文書だけの引数と Enum メンバーの既定値（件数の欠落）
# ===========================================================================

R2_SERVER = '''import enum
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel, Field

from mcp.server.fastmcp import FastMCP

ROOT = "/srv"
FIXED = "/srv/fixed.txt"
PREFIX = "p_"


def build_examples():
    return ["a", "b"]


def extra(schema):
    schema["x"] = 1


EXAMPLES = build_examples()


class Mode(str, enum.Enum):
    A = "a"
    W = "w"


class DescMode(str, enum.Enum):
    A = "a"

    def __get__(self, obj, typ=None):
        return FIXED

    def __set__(self, obj, value):
        pass


class Picker(enum.Enum):
    A = 1

    def pick(self):
        return FIXED


class Confine:
    def __set_name__(self, owner, name):
        self.name = "_" + name

    def __get__(self, obj, typ=None):
        return FIXED if obj is None else getattr(obj, self.name, FIXED)

    def __set__(self, obj, value):
        object.__setattr__(obj, self.name, FIXED)


CONF = Confine()


def make_default():
    return FIXED


class ReqF(BaseModel):
    path: str = Field(description=f"file under {ROOT}")


class ReqE(BaseModel):
    path: str
    mode: Mode = Mode.A


class ReqFE(BaseModel):
    path: str = Field(..., title=f"path in {ROOT}", examples=EXAMPLES, json_schema_extra=extra)
    mode: Mode = Field(default=Mode.W, description=f"mode for {ROOT}")


class ReqAlias(BaseModel):
    path: str = Field(alias=PREFIX + "path", serialization_alias=PREFIX + "out")


class ReqD(BaseModel):
    path: str = Field(..., description="file", examples=["a", "b"])
    note: Optional[str] = None


class ReqDefConf(BaseModel):
    path: str
    other: str = Field(default=CONF, description=f"file under {ROOT}")


class ReqDefCall(BaseModel):
    path: str
    other: str = Field(default=make_default(), description="x")


class ReqDescEnum(BaseModel):
    path: str
    mode: DescMode = DescMode.A


class ReqPick(BaseModel):
    path: str
    how: Any = Picker.pick


@dataclass
class DcEnum:
    path: str
    mode: Mode = Mode.A


mcp = FastMCP("t")


def _w(p):
    open(p, "w").write("x")


@mcp.tool(annotations={"destructiveHint": False})
def wf(req: ReqF) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def we(req: ReqE) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wfe(req: ReqFE) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def walias(req: ReqAlias) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wd(req: ReqD) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wdefconf(req: ReqDefConf) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wdefcall(req: ReqDefCall) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wdescenum(req: ReqDescEnum) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wpick(req: ReqPick) -> str:
    open(req.path, "w").write("x")
    return "ok"


@mcp.tool(annotations={"destructiveHint": False})
def wdcenum(req: DcEnum) -> str:
    open(req.path, "w").write("x")
    return "ok"
'''


@pytest.fixture(scope="module")
def r2(tmp_path_factory):
    return _units(tmp_path_factory, "u23r3_r2", {"server.py": R2_SERVER})


def _model_path(u: dict) -> None:
    effs = _effects(u, "FS_WRITE")
    assert effs, _brief(u)
    assert all(_model_resolved(_slot(e, "path")) for e in effs), _brief(u)


def test_r2_fstring_description_is_documentation(r2):
    """U23-R2: `Field(description=f"file under {ROOT}")` の description は検証される値を変えない →
    req.path は MODEL/resolved のまま → D2 矛 fs_writeout_model_path。"""
    u = r2["wf"]
    _model_path(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_r2_enum_member_default_is_static(r2):
    """U23-R2: pydantic の `mode: Mode = Mode.A`（木内の str Enum、`__get__` / `__set__` なし）は、モデルが渡す
    値を置き換えない → D2 矛 fs_writeout_model_path。"""
    u = r2["we"]
    _model_path(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_r2_doc_kwargs_and_enum_field_default(r2):
    """U23-R2: title / examples（名前参照）/ json_schema_extra（関数）と `Field(default=Mode.W, description=f"...")`
    → どれも値を変えない → D2 矛 fs_writeout_model_path。"""
    u = r2["wfe"]
    _model_path(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_r2_alias_kwargs_are_not_checked(r2):
    """U23-R2: alias / serialization_alias の定数式は値を変えない → D2 矛 fs_writeout_model_path。"""
    u = r2["walias"]
    _model_path(u)
    _check(u, "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_keep_r2_literal_field_kwargs(r2):
    """対照: リテラルだけの Field（再点検の ReqD）は今どおり D2 矛。"""
    _check(r2["wd"], "FS_WRITE", "D2", "矛", "fs_writeout_model_path")


def test_keep_r2_descriptor_default_hides(r2):
    """対照: `Field(default=CONF, description=f"...")` の default は記述子のインスタンス → 今どおりフック扱い（不）。"""
    u = r2["wdefconf"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")


def test_keep_r2_call_default_hides(r2):
    """対照: `Field(default=make_default(), description="x")` の default は呼び出し → 今どおり不。"""
    u = r2["wdefcall"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")


def test_keep_r2_enum_with_descriptor_methods_hides(r2):
    """対照: `__get__` / `__set__` を定義する Enum のメンバーは記述子になりうる → 今どおり不。"""
    u = r2["wdescenum"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")


def test_keep_r2_enum_method_reference_hides(r2):
    """対照: `Picker.pick`（Enum のメソッド = 関数オブジェクト。記述子）はメンバーではない → 今どおり不。"""
    u = r2["wpick"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")


def test_keep_r2_dataclass_enum_default_strict(r2):
    """対照: dataclass の既定値の規則（記述子の恐れ）は変えない。`mode: Mode = Mode.A` の dataclass は今どおり不。"""
    u = r2["wdcenum"]
    _check(u, "FS_WRITE", "D2", "不", "fs_writeout_model_path_opaque")
