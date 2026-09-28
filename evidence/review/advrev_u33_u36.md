# 7440a2a（§9.6-1〜7、D64 / U33・U34・U36）の敵対的レビュー

CLAUDE.md の「解決率を上げる変更は、resolved にしてよい根拠を 1 件ずつ崩しに行く敵対的レビューを通す」による。
レビュー役は Opus の agent 1 体（2026-09-28）。本記録者は所見を読んで分類し、規則の改訂（§9.6 の改訂）と
記録（O42）に振り分けた。再現のスクリプトと出力は `advrev_u33_u36/` にある（`h.py` が判定関数の呼び出し、
`cases_*.py` が入力、`e2e.py` が `runner.run` を通した確認、`db_310.txt` / `db_312.txt` と `host_*.txt` が
Python 3.10.20 / 3.12.3 の出力。両版の結果は全件一致）。

**やり方**: 04147c6（旧）と 7440a2a（新）を worktree に取り出し、`_d1` / `_d2` / `_d4` / `_host_class` に
リテラルを直接渡して比べた。f1〜f6・f9・c1 の 8 件は `runner.run` を通しても同じ結果（psycopg / requests / httpx）。
HEAD 74a5cf8 と 7440a2a の差は dparse.py の docstring だけ。

## 所見

| id | 対象 | 入力（例） | 旧 | 新 | 向き | 新規か | 扱い |
|---|---|---|---|---|---|---|---|
| N1 | §9.6-1 入れ子コメント（PG / SQL Server / DuckDB） | `/* old /* x */ SELECT */ DELETE FROM t` | 不 | **内** | 誤 clear | **新規** | 改訂 1'(a) / 2'(c) |
| N2 | §9.6-1 `/*M!`（MariaDB の実行されるコメント） | `/*M!100100 INSERT INTO t */ SELECT * FROM u` | 不 | **内** | 誤 clear | **新規** | 改訂 1'(b) |
| N3 | §9.6-1 `\r` で終わる行コメント（PG） | `-- c\rDELETE FROM t;\nSELECT 1` | 不 | **内** | 誤 clear | **新規** | 改訂 1'(c) / 2'(c) |
| N4 | §9.6-2 分割に失敗すると先頭の矛を捨てる | `DELETE FROM t WHERE name = 'O\'Brien';` | **矛** db_modify | 不 | 矛の取りこぼし | **新規（退行）** | 改訂 2'(a) |
| N5 | §9.6-2 分割器と complete_statement の字句の食い違い | `SELECT $$it's$$; DELETE FROM t;` | 内 | 内 | 誤 clear | 結果は既存（規則の主張が不成立） | 改訂 2'(b) |
| N6 | §9.6-2 SQLite のトリガの状態機械を PG / MySQL に当てる | `CREATE TRIGGER trg … EXECUTE FUNCTION f(); DROP TABLE b;` | D2 / D4 内 | 同じ | 誤 clear | 結果は既存 | 改訂 2'(b) |
| N7 | §9.6-2 方言で字句が変わる形 | `SELECT 'a\'b'; DELETE FROM t; -- '`、`E'…'`、`#` コメント、`x$$` | 内 | 内 | 誤 clear | 結果は既存 | 改訂 2'(c)(d) |
| N8 | §9.6-7 `is_private` が 6to4 / Teredo なども含む | `http://[2002:808:808::1]:80/x` | external（矛） | **local（内）** | 誤 clear | **新規に届く**（ポート・userinfo つき） | 改訂 7' |
| N9 | 差分の外 `_split_url` | `httpx.Client(base_url=…).get("oauth/authorize?redirect_uri=http://localhost:8080/cb")` | D3 内 | 同じ | 誤 clear | 既存 | 記録（O42） |
| N10 | PRAGMA の正規表現 | `PRAGMA user_version /* c */ = 3`、`PRAGMA main . user_version = 3` | 内 | 同じ | 誤 clear | 既存 | 記録（O42） |
| N11 | `;` の無い T-SQL のバッチ | `SET NOCOUNT ON\nDELETE FROM t WHERE id = ?` | 内 | 同じ | 誤 clear | 既存 | 記録（O42） |
| A1 | D3 数字だけの IPv4 | `2130706433`、`127.1`、`0x7f.1`、`0177.0.0.1` | external | 同じ | 誤警報 | 既存 | 記録（O42） |
| A2 | D3 CGNAT・名前 | `100.64.0.0/10`、`host.docker.internal`、`localhost.localdomain` | external | 同じ | 誤警報 | 既存 | 100.64 は改訂 7' で不。名前は記録 |

ほかに、`/* c */;DELETE FROM t` が D1 / D2 で不（矛が正しい。旧も不）になる小さな不整合（`_db` は 1 文のとき全体を
読み、`_d4` は分割後を読む）→ 改訂 2'(e)。差分の外で §7.5 / D55 の表の選択として、D2 で `INSERT OR REPLACE` と
`ON CONFLICT DO UPDATE` は内・`REPLACE INTO` は矛、PG の `EXPLAIN ANALYZE DELETE` は読み取り扱い、MySQL の
`SET PERSIST` / `SET PASSWORD` は接続単位扱い（記録）。

**corpus の grep**（行単位。複数行の文字列は見ていない）: `/*M!` は 0 行。SQL 語を含む非 vendored の行で入れ子コメント・
`$$…'…$$`・`--…\r` に当たったのは 7 行で、関係するのは `v3-posit-dev__commons` の DuckDB の SQL ガードのテスト
（入れ子コメントを回避手段として試している）と teman2 のテストのコメント 1 行。

## 崩せなかった根拠

- §9.6-1: `/*!` は剥がさず不。文頭の `/*+` は MySQL でも普通のコメント。引用符を含むコメント・ブロック内の `--`・
  行コメント内の `/*` は SQLite / PG / MySQL と一致。閉じないコメント・コメントだけ・改行の無い `--` は不。Unicode 空白を
  飛ばしても実行される文は隠れない。MySQL の `--x` は文頭の構文エラー。
- §9.6-2: `''` の重ね、`'a;b'`、`$1`、`$tag$ ; $tag$`、SQLite の `CREATE TRIGGER … BEGIN … END`、`[a;b]`、最後の `;` の後の文、
  `;;`、末尾のコメント、`BEGIN; DELETE; COMMIT;`、`SET …; UPDATE …`（D4 は不）は意図どおり。分割できたときは先頭の文が
  必ず含まれ、その先頭語は旧版で全体から取った先頭語と同じ（分割で矛が内に落ちるのは N4 の経路だけ）。
- §9.6-3〜6: 厳しくなる向きか理由コードだけの変化。`%` `{` `}` を含む先頭語が変更の語の一覧に当たることは無い。
- §9.6-7: userinfo・`[::1]:8080`・末尾ドットの読みは urllib3 / requests と一致。読みが違った `[::1%@evil.example]` などは
  クライアントが例外か DNS 失敗で外部に繋がらない。`\` は unknown。`::ffff:8.8.8.8` と `64:ff9b::/96` は external。
  IP を先に試す段は `::1%x@evil.example` を local と読むが、scheme つきの URL では `_split_url` が `%` を含む権威部を
  分けないので届かない（潜在の穴。改訂 7' で `@` があるときは IP を先に試さない）。
