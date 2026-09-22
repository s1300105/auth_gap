# 事前定義の地図（何を先に決めているか、なぜ、どれが自分で考えた部分か）

再現: `python scripts/catalog_map.py evidence/scan_v2_run5 --md docs/catalog_map.md`

**役割と出所の分類は判断であって測定ではない**（根拠は `docs/decisions.md` D37）。
行数と、下の「実際に使われた行」は測定値。

## まとめ

| 役割 | 表の数 | 行の合計 |
|---|---|---|
| 核（宣言 D と実効 M の照合に要る） | 22 | 243 |
| 付録（D36 で降ろした主張のもの） | 30 | 200 |
| 索引（派生。定義ではない） | 8 | 119 |

核の内訳（出所別の行数）:

| 出所 | 行 |
|---|---|
| 既知の知識の転記 | 172 |
| この研究で決めた | 53 |
| 解析器の自己申告 | 16 |
| 記録 | 2 |

**自分で一から考える必要があったのは「この研究で決めた」の行だけで、その中心は
`ENTRY_RULES`（ツールの入口 14 形）である。** 既存の静的解析はどの枠組みの入口も
知らないので代替が無い。危険な呼び出しと値の変換は Python と主要ライブラリの常識で、
既存ツールも同等の表を持つ（量はあるが難しさは無い）。

## 核の主張が実際に使っている行

`evidence/scan_v2_run5` の CONTRADICTION から逆に数えた。

- 関係した API: **13 種類**（`DIRECT_SINKS` 67 行のうち）
- 効果の形: {'direct': 138}
- 呼び出しを何段降りたか: 0 段 5, 1 段 27, 2 段 40, 3 段 63, 4 段 3

```
  builtins.open  os.chmod  os.makedirs  os.remove  os.replace  os.unlink  pathlib.Path.mkdir  pathlib.Path.open  pathlib.Path.unlink  pathlib.Path.write_bytes  pathlib.Path.write_text  shutil.rmtree  subprocess.run
```

## 母集団の宣言が割れている API

同じ API を呼ぶツールで、readOnly と destructive の明示が両方現れるもの。
3 ユニット以上から呼ばれる site が対象。

- 効果 site の総数: 41
- 宣言が割れている site: **20**

| API | 宣言の分かれ方 |
|---|---|
| `httpx.AsyncClient.request` | {'openWorldHint+readOnlyHint': 378, 'openWorldHint': 269, 'destructiveHint': 32, '(宣言なし)': 23, 'readOnlyHint': 19, 'destructiveHint+openWorldHint': 3} |
| `httpx.AsyncClient.get` | {'(宣言なし)': 102, 'destructiveHint': 19, 'readOnlyHint': 17, 'destructiveHint+openWorldHint': 8, 'openWorldHint+readOnlyHint': 8} |
| `httpx.AsyncClient.post` | {'(宣言なし)': 101, 'destructiveHint+openWorldHint': 10, 'readOnlyHint': 9, 'destructiveHint': 7} |
| `builtins.open` | {'(宣言なし)': 45, 'readOnlyHint': 9, 'destructiveHint': 4, 'destructiveHint+openWorldHint': 1, 'openWorldHint': 1} |
| `pathlib.Path.mkdir` | {'(宣言なし)': 23, 'destructiveHint': 19, 'readOnlyHint': 8, 'destructiveHint+openWorldHint': 3, 'openWorldHint': 1, 'openWorldHint+readOnlyHint': 1} |
| `subprocess.run` | {'(宣言なし)': 32, 'readOnlyHint': 12, 'destructiveHint': 3, 'destructiveHint+openWorldHint': 1, 'openWorldHint+readOnlyHint': 1, 'openWorldHint': 1} |
| `pathlib.Path.read_text` | {'readOnlyHint': 18, '(宣言なし)': 8, 'destructiveHint': 4} |
| `psycopg.Cursor.execute` | {'readOnlyHint': 13, '(宣言なし)': 6, 'destructiveHint+openWorldHint': 3, 'destructiveHint': 3, 'openWorldHint+readOnlyHint': 2} |
| `urllib.request.urlopen` | {'(宣言なし)': 6, 'readOnlyHint': 6, 'openWorldHint+readOnlyHint': 6, 'destructiveHint+openWorldHint': 2, 'destructiveHint': 1} |
| `os.chmod` | {'openWorldHint+readOnlyHint': 6, 'readOnlyHint': 4, '(宣言なし)': 3, 'destructiveHint': 1} |
| `os.unlink` | {'openWorldHint+readOnlyHint': 6, '(宣言なし)': 4, 'destructiveHint': 3} |
| `pathlib.Path.read_bytes` | {'readOnlyHint': 6, '(宣言なし)': 3, 'destructiveHint': 2} |
| `os.replace` | {'openWorldHint+readOnlyHint': 6, 'destructiveHint': 2, '(宣言なし)': 1} |
| `pathlib.Path.open` | {'(宣言なし)': 7, 'readOnlyHint': 1, 'destructiveHint+openWorldHint': 1} |
| `os.remove` | {'readOnlyHint': 5, 'destructiveHint+openWorldHint': 1, '(宣言なし)': 1} |
| `pathlib.Path.rglob` | {'(宣言なし)': 4, 'readOnlyHint': 1, 'destructiveHint': 1} |
| `httpx.get` | {'(宣言なし)': 3, 'readOnlyHint': 2, 'destructiveHint+openWorldHint': 1} |
| `os.makedirs` | {'(宣言なし)': 2, 'readOnlyHint': 2, 'destructiveHint+openWorldHint': 1} |
| `os.walk` | {'readOnlyHint': 2, 'destructiveHint': 2, '(宣言なし)': 1} |
| `os.listdir` | {'(宣言なし)': 1, 'destructiveHint+openWorldHint': 1, 'readOnlyHint': 1, 'destructiveHint': 1} |

**多数決を真理として使ってはならない。** `subprocess.run` は readOnly の宣言が
多数派になるが、プロセス起動が読み取り専用であるはずがない。多数派が誤っている。
この表は「少なくとも一方が誤っている」を言うためのもので、正解を決める材料ではない。

## 表の一覧

### 核（宣言 D と実効 M の照合に要る）

| 表 | 場所 | 行 | 出所 | 備考 |
|---|---|---|---|---|
| `DIRECT_SINKS` | sinks | 67 | 既知の知識の転記 | subprocess.run / open / rmtree / httpx.get。ただし destructive 印は領域固有 |
| `TRANSFERS` | transfers | 34 | 既知の知識の転記 | realpath / Path.resolve / shlex.quote / urlparse |
| `PROXY_SINKS` | sinks | 16 | 既知の知識の転記 | receiver 型経由の sink（git.Git.checkout など） |
| `DB_RECEIVER_TYPES` | sinks | 14 | 既知の知識の転記 | 非 DB の .execute() を数えないための受け手型 |
| `ENTRY_RULES` | entries | 14 | この研究で決めた | **既存の静的解析はどれも知らない。この研究の貢献の中心** |
| `CTORS` | transfers | 13 | 既知の知識の転記 | sqlite3.connect / httpx.Client / git.Repo |
| `INDIRECTS` | transfers | 9 | 既知の知識の転記 | multiprocessing.Process / Thread / partial / submit |
| `INTERPRETER_ARGV0` | sinks | 9 | 既知の知識の転記 | argv0 がインタプリタかの判定 |
| `VALUE_ATTRS` | ir | 8 | 解析器の自己申告 | 値に付く属性 8 語 |
| `VAL_OPAQUE_REASONS` | ir | 8 | 解析器の自己申告 | 値を解決できなかった理由 8 語 |
| `ATTR_TYPE_TRANSITIONS` | transfers | 7 | 既知の知識の転記 | repo.git → git.cmd.Git のような型の伝播 |
| `PRIMARY_SLOTS` | sinks | 7 | この研究で決めた | 主 slot 7 種（指標の分母） |
| `SLOTS` | sinks | 7 | この研究で決めた | 効果 kind 7 種と slot。宣言の語彙に合わせて決めた |
| `SUB_KINDS` | sinks | 7 | この研究で決めた | kind 粒度の副分類 |
| `DANGEROUS_KINDS` | sinks | 6 | この研究で決めた | 危険とみなす kind |
| `TOOLMESSAGE_META_FIELDS` | entries | 5 | この研究で決めた | langroid ToolMessage のメタ欄 |
| `FORMS` | sinks | 3 | この研究で決めた | direct / proxy / pipe |
| `PIPE_HANDLE_SOURCES` | sinks | 3 | 既知の知識の転記 | pipe ハンドルを生む spawn |
| `PIPE_SINKS` | sinks | 2 | この研究で決めた | stdin.write 形。仕様が「構造的理由のみ、CVE の裏付け無し」と明記 |
| `VOCABULARY_REVISIONS` | validators | 2 | 記録 | 語彙を動かした記録 |
| `LOWLEVEL_V2_KWARGS` | entries | 1 | この研究で決めた | 低レベル MCP v2 の kwargs |
| `R2_EXCEPTIONS` | entries | 1 | この研究で決めた | MODEL としない仮引数の例外 |

### 付録（D36 で降ろした主張のもの）

| 表 | 場所 | 行 | 出所 | 備考 |
|---|---|---|---|---|
| `LLM_CALLS` | entries | 24 | 既知の知識の転記 | SELECT 座標（trig）。traced 0.6% で §3 の格下げ条項が発火（D36） |
| `WEAK_REASONS` | validators | 22 | この研究で決めた | **自作**。弱い検証の理由 22 語。設計に最も時間がかかった |
| `WITNESS_TEMPLATES` | validators | 22 | この研究で決めた | weak 理由ごとの witness 文言 |
| `APPROVAL_INTERRUPTS` | entries | 12 | この研究で決めた | 承認割り込みの認識 |
| `VALIDATOR_SHAPES` | validators | 12 | この研究で決めた | **自作**。Def 5 の検証子の形 |
| `LLM_PROJECTIONS` | entries | 11 | 既知の知識の転記 | 同上 |
| `MODE_GATE_ATOMS` | entries | 9 | この研究で決めた | モードのゲート |
| `GATE_OPAQUE_REASONS` | ir | 8 | 解析器の自己申告 | ゲート側の OPAQUE 8 語 |
| `GRADES` | validators | 7 | この研究で決めた | 値検証の等級 |
| `CONTAINMENT_PREDICATES` | validators | 6 | 既知の知識の転記 | 包含述語（commonpath / relative_to …） |
| `POLICY_FILE_PATTERNS` | sinks | 6 | この研究で決めた | D_op の方針ファイル |
| `LEAK_REASONS` | entries | 5 | この研究で決めた | Def 5-b の Leak |
| `NOT_STRONG_DOMAINS` | validators | 5 | この研究で決めた | strong にしない slot 領域 |
| `PATH_DOMAIN_SLOTS` | sinks | 5 | この研究で決めた | strong-path が効く slot（D25） |
| `CONFIG_ATOM_SOURCES` | validators | 4 | この研究で決めた | config atom の源 |
| `DEFAULT_OPEN_VALUES` | validators | 4 | この研究で決めた | 既定が開いている値 |
| `DOWNGRADES` | validators | 4 | この研究で決めた | 格下げ属性 |
| `ENUM_BINDING_FORMS` | validators | 4 | この研究で決めた |  |
| `GATE_NODOM_REASONS` | ir | 4 | 解析器の自己申告 | ゲート側の NODOM 4 語 |
| `ALLOWED_OPERANDS` | validators | 3 | この研究で決めた | Def 5 (iii) の被演算子 |
| `CONFIG_ATOM_OPAQUE_FORMS` | validators | 3 | この研究で決めた |  |
| `EXPOSURE_GATE_FORMS` | entries | 3 | この研究で決めた | 露出ゲートの形 |
| `ROOT_EQUAL_STEPS` | validators | 3 | この研究で決めた | root-equal と認める変換 |
| `WITNESS_VIEWS` | validators | 3 | この研究で決めた | witness の見せ方 |
| `_DOM_PRIORITY` | ir | 3 | 解析器の自己申告 | 3 値支配の優先順 |
| `DASH_REJECT_FORMS` | validators | 2 | この研究で決めた | `--` 拒否の形 |
| `LEXICAL_CANONS` | transfers | 2 | 既知の知識の転記 | 字句正規化子 |
| `SYMLINK_RESOLVERS` | transfers | 2 | 既知の知識の転記 | Def 5 (i) の正規化子 |
| `ARGV_MODE_SUPPRESSED_WITNESS` | validators | 1 | この研究で決めた |  |
| `DOWNGRADE_WITNESS` | validators | 1 | この研究で決めた |  |

### 索引（派生。定義ではない）

| 表 | 場所 | 行 | 出所 | 備考 |
|---|---|---|---|---|
| `TRANSFER_BY_NAME` | transfers | 34 | - | TRANSFERS の索引 |
| `WEAK_REASON_SET` | validators | 22 | - | WEAK_REASONS の集合 |
| `CTOR_BY_NAME` | transfers | 13 | - | CTORS の索引 |
| `SHAPE_NAMES` | validators | 12 | - | VALIDATOR_SHAPES の名前 |
| `APPROVAL_NAMES` | entries | 11 | - | APPROVAL_INTERRUPTS の名前 |
| `METHOD_TRANSFERS` | transfers | 11 | - | TRANSFERS の受け手主語だけ |
| `INDIRECT_BY_NAME` | transfers | 9 | - | INDIRECTS の索引 |
| `KINDS` | sinks | 7 | - | SLOTS の鍵 |

