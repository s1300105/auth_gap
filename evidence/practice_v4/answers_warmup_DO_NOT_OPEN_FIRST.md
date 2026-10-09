# 練習の練習（W-01）の参考の答え — **自分の記録を書き終えてから開く**

`evidence/practice_v4/warmup_and_timing.md` の 3.4 で開くファイルです。W-01 の分だけが入っています（P-M01〜P-M03・矛の練習の
答えは入っていません）。

**正解ではありません。** 下の 1 は v4 のときに本記録者（AI）が見落としの判定の形で付けたもの（`evidence/population_v4/v4_judgments.json`
の `R00`）、2 は 2026-10-09 に本記録者（AI）が原ソースを読み直して実態調査の形に直したものです。食い違ったら、どちらが手引きの規則に
合うかを考え、理由と行をメモしてください。

| 件 | 木 | ツール | 名簿の位置 |
|---|---|---|---|
| W-01（v4 の R00） | `v4-andrewbolster__mcp.bolster.online` | `check_availability` | `app.py:293`（`decorator`、宣言 `app.py:292`） |

## 1. v4 の記録（R00、2026-10 の v4 の判定。原文のまま）

- `outcome`: 反する動作は無い（実態調査の答えでは `違反でない`）
- `evidence`: app.py:292-326 check_availability calls get_access_token, ctx.info / ctx.warning (logs sent to the client) and
  availability.get_availability. availability.py:38-76 decodes an environment variable and calls the external library
  bolster.utils.calendars.get_merged_availability through to_thread. The tree contains no writes and no non-GET requests.
- `note`: The only external call is the one inside the bolster library (the docstring says it is requests-based and fetches ICS
  feeds). That library is outside the tree and was not read.

## 2. 実態調査の形の参考の記録（2026-10-09 の読み直し）

| 欄 | 値 |
|---|---|
| `outcome` | `違反でない` |
| `evidence` | 下の文 |
| `note` | 下の文 |
| `write_target`・`condition_type`・`condition`・`depth`・`unknown_reason` | 空（違反でないので書かない） |

`evidence`:

> 読んだ範囲: app.py:292-326（深さ 0、check_availability）、availability.py:60-76（深さ 1、get_availability。app.py:31 の import、
> app.py:317 で await）、availability.py:38-57（深さ 2、load_calendars。availability.py:68）。availability.py:48・56 の
> AvailabilityNotConfiguredError の構築は、木の中に `__init__` が無い（availability.py:34-35）。本体の動作は get_access_token
> （app.py:306、要求の認証の文脈を読む）、ctx.info / ctx.warning（app.py:314・319・322・325、クライアントへの通知）、
> get_availability。load_calendars は環境変数を読んで base64 と JSON を解くだけ（availability.py:46-57）。get_availability は
> 木の外の bolster.utils.calendars.get_merged_availability を asyncio.to_thread で呼ぶ（availability.py:69-76）。木の中に
> ファイル・DB の書き込み、プロセスの起動、HTTP の呼び出しは無い。logging の設定は app.py・availability.py・
> validation_middleware.py・main.py のどこにも無い（`logging`・`FileHandler`・`basicConfig` の検索で 0 件）。

`note`:

> get_merged_availability の中は読んでいない（木の外のライブラリ。18.2 の 2）。呼び出し側の docstring（availability.py:14-18）に
> 「取得・合成・整形」「requests ベース」とあり、名前も get で、環境を変えるライブラリの関数（requests.put など）には当たらない
> と読んだ。サーバ全体の middleware（app.py:43 の ToolValidationErrorMiddleware、validation_middleware.py:36-44。app.py:505 の
> AuthMiddleware と require_allowed_login、app.py:465-475）もツールの呼び出しで走るので読んだが、エラーの文の整形と環境変数の
> 読み取りだけ（middleware を読む範囲に入れるかは手引きに無い。O48）。

## 3. 見ておきたかった点（振り返りの手がかり）

| 点 | 何を見るか | 手引き |
|---|---|---|
| 深さ | get_availability が 1、load_calendars が 2。to_thread に渡した関数は木の外なので読まない | 18.2 の 2 |
| 通知とログ | `ctx.info` / `ctx.warning` はクライアントへの通知で、ファイルのログではない（反しない） | 15.1 の迷いやすい形 |
| モジュール水準のログの設定 | 無いことを検索で確かめ、確かめたことを `evidence` に書く | 18.3 |
| 木の外のライブラリ | 中は読まない。関数そのものが環境を変えるものかどうかだけを見る | 18.2 の 2・19 |
| 読む範囲の記録 | `違反でない` でも、読んだファイルと行を書く | 18.4 |
| 紛らわしいもの | 直前のツール send_contact_message（`readOnlyHint` ではない）の「has been logged」の文字列（app.py:289 付近）は別のツールで、実際のログも無い。`httpx` は import されているが、このツールでは `except httpx.HTTPError` に出るだけで呼んでいない（隣のツールが GET に使う） | 18.2 の 1 |
| 2 つの入口 | 同じツールが公開の `/mcp` と認証つきの `/auth/mcp`（app.py:498-507 の mount）で動く。認証の層（GitHubProvider・AuthMiddleware）は木の外のライブラリ | — |

## 4. 意見が分かれうるところ

- **`不明` にした場合**: get_merged_availability が中でファイルのキャッシュなどを使うかは、ライブラリの中を読まない範囲では
  分かりません。本記録者は「ライブラリの関数そのものが環境を変えるものだけを数える」（18.2 の 2）と読み、名前と docstring から
  数えませんでした。`不明（外の値）` にした人は、18.2 の 2 と 19 の「調べる範囲」をどう読んだかをメモしてください。手引きの
  曖昧な点の候補です（O48 の (3)）。
- **middleware を読まなかった場合**: 手引きはデコレータの wrapper は読むとしていますが、サーバ全体の middleware には触れていません
  （O48 の (1)）。読まなくても、この件では結論は変わりません。
