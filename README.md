# AuthGap

Python の LLM エージェント（アプリ / ツールパッケージ / MCP サーバ）について、
**インストール前のパッケージ木のみ**を入力とする静的解析で、コードがモデルに
実際に渡している権限（実効権限 M）を推論し、宣言権限 D または明示ベースライン
P0 を超える箇所を報告する。

- 仕様の正本: [AUTHGAP_BRIEF_v3.md](AUTHGAP_BRIEF_v3.md)（この repo で唯一の仕様書）
- 解析中核は標準ライブラリ `ast` のみ。venv も型環境も構築しない。
- LLM を判定入力に使わない。出力は決定的（同一入力で 3 回バイト一致）。

## CLI

    python -m authgap probe <path>    # F0a の測定量（効果 / validator 形状 / 宣言）
    python -m authgap scan  <path>    # manifest + verdict

## レイアウト

    authgap/     解析器
    docs/        設計文書・凍結物・triage
    fixtures/    受け入れ fixture と期待値（手検証の入口）
    corpus/      解析対象の木（gitignore、scripts/fetch_corpus.py が生成）
    evidence/    実行の証拠（gitignore、evidence/w0 のみ例外）
    scripts/     取得・前測・検証スクリプト
    tests/       単体・回帰・決定論

## 手で検証するには

`fixtures/*/expected.json` が行単位の期待値であり、これが手検証の入口である。
`docs/verification_guide.md` に「どのファイルを、どの順で、何と突き合わせるか」を書く。
