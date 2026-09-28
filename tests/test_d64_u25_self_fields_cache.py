"""D64 / U25: `analyze._self_fields` の cache（鍵と番兵）。所見 R5-r1-1 と R5-r1-9。

**期待値はこのテストで、`authgap/` を直す前に書いた（D64 / U25）。** v2 / v3 の件数には合わせず、
§5.2（同一入力で出力は決定的）、§7.1（DB: SQL が MODEL 由来 → 矛 / FS_WRITE → 矛）、規則 4（黙って安全側に
倒さない）、D17 改訂 4（RecursionError は TRUNCATED として残す）、D64 の U25 行から導いた。

- R5-r1-1（鍵）: cache の鍵が `id(index)` なので、死んだ index の番地が次の木で再利用されると、同じ
  module 名・クラス名を持つ別の木のフィールドが流用される。CPython の番地の再利用は確率的（再現は
  300 回中 22 回）なので、**`analyze` の中の `id` だけを差し替えて「番地の再利用」を決定的に起こす。**
  index ごとに cache を持つ直し方（インスタンス属性 / WeakKeyDictionary）なら差し替えは効かない。
- 検証役の反例（R5-r1-1）: **src_root を鍵にする直し方は不可。** 同じパスの木を書き換えて同じプロセスで
  解析し直すと前の中身のフィールドが残る（`scripts/mutation_test.py` が実際にこの使い方をする）。
- R5-r1-9（番兵）: `__init__` の評価で RecursionError が出ると番兵 `()` が cache に残り、同じクラスの
  2 つ目以降のユニットは印なしでフィールドを失う。D64: 失敗の印を cache に入れ、`self.<attr>` を
  opaque(unresolved) にしてユニットの残りの解析を続け、`TRUNCATED(recursion:self_fields)` を付ける。
- 検証役の反例（R5-r1-9）: **番兵を pop して再計算する直し方は不可。** 同じクラスの 2 つ目のユニットが
  `os.remove(path)` を直接呼ぶと、今は正しく D1 の矛が出るが、pop 案では再計算で RecursionError が
  再発してユニット全体が TRUNCATED になり、正しい矛が消える。

テストの分離: 各テストの前後で cache を空にし（属性が無くなっていれば何もしない）、テスト中に作られた
`SourceIndex` を生かしておく（本物の番地の再利用でテストの結果が揺れないように）。
"""

from __future__ import annotations

import builtins

import pytest

from authgap import analyze
from authgap.report import manifest_json
from authgap.runner import RunConfig, run
from authgap.srcindex import SourceIndex

HDR = 'import os\nimport sqlite3\n\nimport httpx\nfrom mcp.server.fastmcp import FastMCP\n\nmcp = FastMCP("t")\n\n\n'

#: 木 A（先に解析される）: `self.conn` は HTTP クライアント。module `server` / クラス `Store` は B と同じ。
SRC_HTTP = HDR + '''class Store:
    def __init__(self):
        self.conn = httpx.Client(base_url="https://api.example.com")

    @mcp.tool(annotations={"readOnlyHint": True})
    def query(self, sql: str) -> str:
        return self.conn.get(sql).text
'''

#: 木 B: `self.conn` は sqlite の接続。readOnlyHint: true で SQL が MODEL → §7.1 で D1 の矛。
SRC_DB = HDR + '''class Store:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")

    @mcp.tool(annotations={"readOnlyHint": True})
    def query(self, sql: str) -> str:
        return str(self.conn.execute(sql).fetchall())
'''

#: 木 H: `self.conn` は辞書（DB ではない）。単独では DB 効果も矛も無い（誤警報の向きの対照）。
SRC_HARMLESS = HDR + '''class Store:
    def __init__(self):
        self.conn = {}

    @mcp.tool(annotations={"readOnlyHint": True})
    def query(self, sql: str) -> str:
        return str(self.conn.execute(sql))
'''

#: `_closure_seed` の経路（注釈つきの外側引数 `store: Store`）。A / B の対。
SRC_CLOSURE_HTTP = HDR + '''class Store:
    def __init__(self):
        self.conn = httpx.Client(base_url="https://api.example.com")


def register(mcp, store: Store):
    @mcp.tool(annotations={"readOnlyHint": True})
    def query(sql: str) -> str:
        return store.conn.get(sql).text
'''

SRC_CLOSURE_DB = HDR + '''class Store:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")


def register(mcp, store: Store):
    @mcp.tool(annotations={"readOnlyHint": True})
    def query(sql: str) -> str:
        return str(store.conn.execute(sql).fetchall())
'''

#: R5-r1-9 の引き金: `__init__` の右辺が `.cursor().connection` を 300 回つなげた式（評価で RecursionError）。
_CHAIN_300 = "sqlite3.connect('data.db')" + ".cursor().connection" * 300

#: メソッド形（`_seed` の経路）。a_remove が最初のユニット。c_remove は検証役の反例（直接の os.remove）。
SRC_SENTINEL = HDR + f'''class Store:
    def __init__(self):
        self.conn = {_CHAIN_300}

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def a_remove(self, path: str, sql: str) -> str:
        os.remove(path)
        return str(self.conn.execute(sql).fetchall())

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def b_query(self, sql: str) -> str:
        return str(self.conn.execute(sql).fetchall())

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def c_remove(self, path: str, sql: str) -> str:
        os.remove(path)
        return str(self.conn.execute(sql).fetchall())

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def d_plain(self, path: str) -> str:
        os.remove(path)
        return "x"
'''

#: 入れ子形（`_closure_seed` の経路）の番兵。
SRC_SENTINEL_CLOSURE = HDR + f'''class Store:
    def __init__(self):
        self.conn = {_CHAIN_300}


def register(mcp, store: Store):
    @mcp.tool(annotations={{"readOnlyHint": True}})
    def a_query(sql: str) -> str:
        return str(store.conn.execute(sql).fetchall())

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def b_remove(path: str, sql: str) -> str:
        os.remove(path)
        return str(store.conn.execute(sql).fetchall())
'''

#: 対照: 読める深さ（60 段の入れ子の呼び出し）の `__init__`。両ユニットとも DB 効果と D1 の矛。
_WRAP_60 = "wrap(" * 60 + "sqlite3.connect('data.db')" + ")" * 60
SRC_WRAP_60 = HDR + f'''def wrap(x):
    return x


class Store:
    def __init__(self):
        self.conn = {_WRAP_60}

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def query_a(self, sql: str) -> str:
        return str(self.conn.execute(sql).fetchall())

    @mcp.tool(annotations={{"readOnlyHint": True}})
    def query_b(self, sql: str) -> str:
        return str(self.conn.execute(sql).fetchall())
'''

#: 対照: 自分自身を構築するクラス（再帰の打ち切りが要る形）。止まって DB 効果が付く。
SRC_SELFREF = HDR + '''class Node:
    def __init__(self):
        self.conn = sqlite3.connect("data.db")
        self.parent = Node()

    @mcp.tool(annotations={"readOnlyHint": True})
    def query(self, sql: str) -> str:
        return str(self.parent.conn.execute(sql).fetchall())

    @mcp.tool(annotations={"readOnlyHint": True})
    def query2(self, sql: str) -> str:
        return str(self.conn.execute(sql).fetchall())
'''

SELF_FIELDS_MARK = "TRUNCATED(recursion:self_fields)"
_FORCED_ID = 12345


def _clear_cache():
    cache = getattr(analyze, "_SELF_FIELD_CACHE", None)
    if isinstance(cache, dict):
        cache.clear()


@pytest.fixture(autouse=True)
def _isolated(monkeypatch):
    """cache を空にし、テスト中の index を生かしておく（本物の番地の再利用で結果を揺らさない）。"""
    _clear_cache()
    alive: list[SourceIndex] = []
    orig = SourceIndex.__init__

    def _init(self, *args, **kwargs):
        orig(self, *args, **kwargs)
        alive.append(self)

    monkeypatch.setattr(SourceIndex, "__init__", _init)
    yield
    _clear_cache()


def _force_same_index_id(monkeypatch):
    """CPython が死んだ index の番地を次の index に再利用した状況を決定的に作る（R5-r1-1）。

    `analyze` の中の `id` だけを差し替え、`SourceIndex` には常に同じ値を返す。index ごとに cache を持つ
    直し方ならこの差し替えは結果に効かない。
    """

    def fake_id(o):
        return _FORCED_ID if isinstance(o, SourceIndex) else builtins.id(o)

    monkeypatch.setattr(analyze, "id", fake_id, raising=False)


def _write(d, src):
    (d / "server.py").write_text(src, encoding="utf-8")
    return d


def _scan(d):
    res = run(RunConfig(src_root=str(d), population="mcp_server", full=True))
    return res, {u["unit"]["qualname"]: u for u in manifest_json(res, "t")["units"]}


def _scan_src(tmp_path_factory, name, src):
    return _scan(_write(tmp_path_factory.mktemp(name), src))


def _kinds(u):
    return sorted({(e["kind"], e["site"]) for e in u["effects"]})


def _row_notes(u):
    return sorted(n for r in u["rows"] for n in r.get("notes", []))


def _sig(units):
    """木の効果行と判定行（ユニットごと）。「B 単独と一致」を比べる形。"""
    return {q: (_kinds(u), _row_notes(u)) for q, u in units.items()}


def _contra(u, decl):
    return any(n == f"contradiction:{decl}" for r in u["rows"] for n in r.get("notes", []))


def _has_db(u):
    return any(e["kind"] == "DB" for e in u["effects"])


def _has_fs_write(u):
    return any(e["kind"] == "FS_WRITE" and e["site"] == "os.remove" for e in u["effects"])


def _truncations_for(res, unit_id):
    return [t for t in res.wall_clock_truncations if t.startswith("TRUNCATED(recursion") and unit_id in t]


# ---------------------------------------------------------------------------
# R5-r1-1: 鍵。対照（今通る。直した後も通る）
# ---------------------------------------------------------------------------


def test_db_tree_alone_has_db_effect_and_d1(tmp_path_factory):
    """対照（R5-r1-1 の expected の基準）: B 単独で `self.conn.execute(sql)` は DB 効果、§7.1 で D1 の矛。"""
    _, b = _scan_src(tmp_path_factory, "b_alone", SRC_DB)
    assert _has_db(b["Store.query"])
    assert _contra(b["Store.query"], "D1")


def test_harmless_tree_alone_has_no_db_effect(tmp_path_factory):
    """対照（R5-r1-1 の誤警報の向きの基準）: H 単独（`self.conn = {}`）には DB 効果も D1 の矛も無い。"""
    _, h = _scan_src(tmp_path_factory, "h_alone", SRC_HARMLESS)
    assert not _has_db(h["Store.query"])
    assert not _contra(h["Store.query"], "D1")


def test_a_then_b_without_id_reuse_matches_b_alone(tmp_path_factory):
    """対照（R5-r1-1）: 番地の再利用が無ければ A→B の B は B 単独と一致する（欠陥は再利用のときだけ）。"""
    _, b_alone = _scan_src(tmp_path_factory, "b0", SRC_DB)
    _scan_src(tmp_path_factory, "a1", SRC_HTTP)
    _, b = _scan_src(tmp_path_factory, "b1", SRC_DB)
    assert _sig(b) == _sig(b_alone)


def test_same_tree_twice_in_one_process_is_identical(tmp_path_factory):
    """対照（§5.2 の決定論。`--determinism` が見ている形）: 同じ木を 1 プロセスで 2 回解析して同じ行。"""
    d = _write(tmp_path_factory.mktemp("twice"), SRC_DB)
    _, first = _scan(d)
    _, second = _scan(d)
    assert _sig(first) == _sig(second)


def test_same_path_rewritten_uses_new_contents(tmp_path_factory):
    """検証役の反例（R5-r1-1。src_root 鍵は不可）: 同じパスの木を書き換えて解析し直すと新しい中身が使われる。

    1 回目は `httpx.Client`（NET、矛なし）、2 回目は同じパスに `sqlite3.connect` → DB 効果と D1 の矛（§7.1）。
    src_root を鍵にすると 1 回目のフィールドが残り、DB 効果と矛が消える（false-clean）。
    """
    d = tmp_path_factory.mktemp("same_path")
    _, first = _scan(_write(d, SRC_HTTP))
    assert any(e["kind"] == "NET" for e in first["Store.query"]["effects"])
    assert not _contra(first["Store.query"], "D1")
    _, second = _scan(_write(d, SRC_DB))
    assert _has_db(second["Store.query"])
    assert _contra(second["Store.query"], "D1")


def test_same_path_rewritten_reverse_direction(tmp_path_factory):
    """検証役の反例（R5-r1-1。src_root 鍵は不可）の逆向き: DB → 辞書に書き換えると DB 効果と矛が消える（誤警報を残さない）。"""
    d = tmp_path_factory.mktemp("same_path_rev")
    _, first = _scan(_write(d, SRC_DB))
    assert _contra(first["Store.query"], "D1")
    _, second = _scan(_write(d, SRC_HARMLESS))
    assert not _has_db(second["Store.query"])
    assert not _contra(second["Store.query"], "D1")


# ---------------------------------------------------------------------------
# R5-r1-1: 鍵。直すべき挙動（今落ちる）
# ---------------------------------------------------------------------------


def test_b_after_a_with_reused_index_id_matches_b_alone(tmp_path_factory, monkeypatch):
    """R5-r1-1（§5.2 / §7.1）: 死んだ A の index の番地を B が得ても、B は B 単独と同じ行（DB 効果 + D1 の矛）。

    今は A の `self.conn`（httpx）が流用され、B の DB 効果と矛が消える（false-clean）。
    """
    _, b_alone = _scan_src(tmp_path_factory, "b_base", SRC_DB)
    _force_same_index_id(monkeypatch)
    _scan_src(tmp_path_factory, "a_prev", SRC_HTTP)
    _, b = _scan_src(tmp_path_factory, "b_after", SRC_DB)
    assert _has_db(b["Store.query"])
    assert _contra(b["Store.query"], "D1")
    assert _sig(b) == _sig(b_alone)


def test_harmless_after_db_with_reused_index_id_matches_alone(tmp_path_factory, monkeypatch):
    """R5-r1-1（誤警報の向き）: 死んだ B の index の番地を H が得ても、H に DB 効果・D1 の矛は立たない。

    今は B の `self.conn`（sqlite）が流用され、H に無い DB 効果と矛が立つ（false-alarm）。
    """
    _, h_alone = _scan_src(tmp_path_factory, "h_base", SRC_HARMLESS)
    _force_same_index_id(monkeypatch)
    _scan_src(tmp_path_factory, "b_prev", SRC_DB)
    _, h = _scan_src(tmp_path_factory, "h_after", SRC_HARMLESS)
    assert not _has_db(h["Store.query"])
    assert not _contra(h["Store.query"], "D1")
    assert _sig(h) == _sig(h_alone)


def test_closure_seed_after_other_tree_with_reused_index_id(tmp_path_factory, monkeypatch):
    """R5-r1-1（`_closure_seed` の経路。analyze.py:286）: 注釈つき外側引数 `store: Store` のフィールドも流用しない。"""
    _, b_alone = _scan_src(tmp_path_factory, "cb_base", SRC_CLOSURE_DB)
    assert _contra(b_alone["register.query"], "D1")  # 前提: 単独では DB 効果 + D1 の矛
    _force_same_index_id(monkeypatch)
    _scan_src(tmp_path_factory, "ca_prev", SRC_CLOSURE_HTTP)
    _, b = _scan_src(tmp_path_factory, "cb_after", SRC_CLOSURE_DB)
    assert _has_db(b["register.query"])
    assert _contra(b["register.query"], "D1")
    assert _sig(b) == _sig(b_alone)


# ---------------------------------------------------------------------------
# R5-r1-9: 番兵。対照（今通る。直した後も通る）
# ---------------------------------------------------------------------------


def test_sentinel_premise_recursion_happens(tmp_path_factory):
    """前提（R5-r1-9）: 300 段の連結の `__init__` は評価で RecursionError を起こす（どこかに TRUNCATED(recursion…) が付く）。"""
    res, units = _scan_src(tmp_path_factory, "sent_premise", SRC_SENTINEL)
    notes = [n for u in units.values() for n in u["notes"]]
    assert any(n.startswith("TRUNCATED(recursion") for n in notes)
    assert any(t.startswith("TRUNCATED(recursion") for t in res.wall_clock_truncations)


def test_sentinel_direct_sink_in_later_unit_keeps_d1(tmp_path_factory):
    """検証役の反例（R5-r1-9。pop して再計算は不可）: 2 つ目以降のユニットの直接の `os.remove(path)` は FS_WRITE + D1 の矛のまま（§7.1）。

    pop 案では再計算で RecursionError が再発してユニット全体が TRUNCATED になり、この正しい矛が消える。
    """
    _, units = _scan_src(tmp_path_factory, "sent_ce", SRC_SENTINEL)
    c = units["Store.c_remove"]
    assert _has_fs_write(c)
    assert _contra(c, "D1")


def test_sentinel_unit_without_self_use_keeps_d1(tmp_path_factory):
    """対照（R5-r1-9）: 同じクラスで `self.<attr>` を使わないユニットの直接の sink は FS_WRITE + D1 の矛のまま。"""
    _, units = _scan_src(tmp_path_factory, "sent_plain", SRC_SENTINEL)
    d = units["Store.d_plain"]
    assert _has_fs_write(d)
    assert _contra(d, "D1")


def test_sentinel_closure_direct_sink_in_later_unit_keeps_d1(tmp_path_factory):
    """検証役の反例（R5-r1-9、`_closure_seed` の経路）: 2 つ目のユニットの直接の `os.remove(path)` は FS_WRITE + D1 の矛のまま。"""
    _, units = _scan_src(tmp_path_factory, "sent_clos_ce", SRC_SENTINEL_CLOSURE)
    b = units["register.b_remove"]
    assert _has_fs_write(b)
    assert _contra(b, "D1")


def test_readable_init_gives_fields_to_every_unit(tmp_path_factory):
    """対照（R5-r1-9）: 読める深さの `__init__`（60 段）なら両ユニットとも DB 効果 + D1 の矛で、打ち切りの印は無い。"""
    res, units = _scan_src(tmp_path_factory, "wrap60", SRC_WRAP_60)
    for q in ("Store.query_a", "Store.query_b"):
        assert _has_db(units[q]), q
        assert _contra(units[q], "D1"), q
        assert not any(n.startswith("TRUNCATED") for n in units[q]["notes"]), q
    assert not [t for t in res.wall_clock_truncations if t.startswith("TRUNCATED(recursion")]


def test_self_constructing_class_terminates_and_resolves(tmp_path_factory):
    """対照（再帰の打ち切りは残す。D64 U25「pop は不可、番兵自体は残す」）: 自分を構築するクラスも止まり、DB 効果 + D1 の矛。"""
    _, units = _scan_src(tmp_path_factory, "selfref", SRC_SELFREF)
    for q in ("Node.query", "Node.query2"):
        assert _has_db(units[q]), q
        assert _contra(units[q], "D1"), q
        assert not any(n.startswith("TRUNCATED") for n in units[q]["notes"]), q


# ---------------------------------------------------------------------------
# R5-r1-9: 番兵。直すべき挙動（今落ちる）
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("qualname", ["Store.a_remove", "Store.b_query", "Store.c_remove"])
def test_sentinel_every_unit_using_self_fields_is_marked(tmp_path_factory, qualname):
    """R5-r1-9（規則 4 / D64 U25）: `self.conn` を使う各ユニットに `TRUNCATED(recursion:self_fields)` が付く。

    今は最初のユニットだけがユニット全体の `TRUNCATED(recursion)` になり、2 つ目以降は印なしでフィールドを失う。
    """
    _, units = _scan_src(tmp_path_factory, "sent_mark", SRC_SENTINEL)
    assert SELF_FIELDS_MARK in units[qualname]["notes"]


@pytest.mark.parametrize("qualname", ["Store.a_remove", "Store.b_query", "Store.c_remove"])
def test_sentinel_every_marked_unit_is_counted_in_truncations(tmp_path_factory, qualname):
    """R5-r1-9（規則 4 / triage fix_outline「印は wall_clock_truncations 側の件数にも載せる」）: 打ち切りの件数から漏れない。"""
    res, units = _scan_src(tmp_path_factory, "sent_count", SRC_SENTINEL)
    uid = units[qualname]["unit"]["unit_id"]
    assert _truncations_for(res, uid), res.wall_clock_truncations


def test_sentinel_first_unit_keeps_direct_sink(tmp_path_factory):
    """R5-r1-9（D64 U25「ユニットの残りの解析を続ける」、§7.1）: 最初のユニットの直接の `os.remove(path)` も FS_WRITE + D1 の矛。

    今は最初のユニットでだけ RecursionError がユニット全体を打ち切り、直接の sink の矛が消える。
    並び順で結果が変わらないこと（c_remove と同じ形の a_remove が同じ判定）を兼ねる。
    """
    _, units = _scan_src(tmp_path_factory, "sent_first", SRC_SENTINEL)
    a = units["Store.a_remove"]
    assert _has_fs_write(a)
    assert _contra(a, "D1")
    assert "TRUNCATED(recursion)" not in a["notes"]
    assert _sig({"x": a}) == _sig({"x": units["Store.c_remove"]})


@pytest.mark.parametrize("qualname", ["register.a_query", "register.b_remove"])
def test_sentinel_closure_every_unit_is_marked(tmp_path_factory, qualname):
    """R5-r1-9（`_closure_seed` の経路。analyze.py:286、D64 U25）: 外側引数 `store: Store` を使う各ユニットに印が付く。"""
    _, units = _scan_src(tmp_path_factory, "sent_clos_mark", SRC_SENTINEL_CLOSURE)
    assert SELF_FIELDS_MARK in units[qualname]["notes"]
