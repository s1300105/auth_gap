# 前測スクリプトの出所

救出 2026-09-08 20:41。元の所在はセッション固有の一時ディレクトリ:
`/tmp/claude-1003/-home-yudai-.../72bc174b-.../scratchpad/tmp_authgap/an/`

新規 repo では `scripts/premeasure/` に置くこと。合計 591 行。

```
87ab0197c5b852a0ad5e657013289ade6fe1888db1aed94c22f424d440b14999  drift2.py
f503cf19390d2baa4dab4241a9486c42c3f0d12498c895ccb7f8e1044eeb687a  lowlevel.py
0923c51cdcebe49c82752c9dd4d754f5ffde7f07281b279c41f7fbde8057dee8  scan.py
a9f24845cd53ddd0595a3350df8ddc97a088f504893e7ae592acee0d1de8b7e8  stats.py
f2717cdde9d31a208d2bb861a44db950adf473efc221badeb01ab5ff3b17cc92  drift.sh
```

**前測コーパス（clone した MCP サーバ群）は commit SHA を記録していないため再現できない。** スクリプトとフレーム定義（検索クエリ・取得日）のみ救出した。数値を再取得する場合はフレームを引き直して測り直す。
