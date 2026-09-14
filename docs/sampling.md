# 標本設計（§6 / §7.6 D14）

抽出日時 2026-09-14T13:19:44+09:00　**seed = 20260909（固定。動かさない）**

| 母集団 | フレーム件数 | 目標 | 抽出（割り増し込み） |
|---|---|---|---|
| MCP サーバ | 2299 | 60 | 90 |
| ツールパッケージ | 0 | 30 | 0 |
| アプリ（T3-app） | 8 | 8 | 8 |

割り増し率 1.5。**取得に失敗したら抽出順で次を繰り上げる。**
その場で選び直すと事後選択になる。失敗は件数として
`docs/fetch_failures.md` に残す。

較正対の repo は野外集合から除いている（採点集合と混ぜない）:

- `langroid/langroid`
- `mervinpraison/praisonai`
- `modelcontextprotocol/servers`
- `significant-gravitas/autogpt`

## T3-app のフレーム（**機械抽出できないので名前つきで先に固定する**）

| repo | 選定根拠 |
|---|---|
| `gptme/gptme` | §4 のケーススタディ 3 件のうちの 1 つ。in-tree の ToolSpec レジストリ |
| `TransformerOptimus/SuperAGI` | 同上。RESTRICTED モードの承認リストを出荷している |
| `OpenHands/agent-sdk` | 同上。ConfirmationPolicy.should_confirm を持つ |
| `OpenManus/OpenManus` | §2.6 の負例 fixture F5/F6/F7 の出所 |
| `microsoft/autogen` | 登録 API 経由の dispatch。assumed 側の対照 |
| `crewAIInc/crewAI` | 同上 |
| `Significant-Gravitas/AutoGPT` | CommandRegistry による実行時 dispatch（D10 の測定対象） |
| `smol-ai/developer` | 小さい木での挙動確認 |

## 抽出された repo

<details><summary>MCP サーバ</summary>

- `brendoncn/poc-as400`
- `aws-samples/sample-aidlc-demo`
- `eggressive/mcp-build`
- `yagrxu/serverless-demo-for-aiops`
- `curtcox/monorepo-crufty-parts`
- `sparshkapoor/promptcompactor`
- `actions-marketplace-validations/sattyamjjain_agent-audit-kit`
- `lilinji/genetind-life-skills`
- `1987-dmytro/voice-mcp-agent`
- `jakubblunar/aiko`
- `sparfenyuk/mcp-telegram`
- `picotrex/mind-brush`
- `shashank-samala/tagent`
- `giak/mnemo-lite`
- `edgemetric/mammothsdk`
- `lestercerioli/ai-agents-mcp-tools`
- `odaisuno/scholai`
- `saiyandev17/agent-sentinel`
- `gigabraingg/hyperliquid-mcp`
- `adityakes11/chatbotmcp_integrated`
- `thehumanworks/mcpctl`
- `santosh-k-singh10/rfxstarterkit-0.2`
- `jacobeverist/ts_api`
- `ob-labs/seekvfs`
- `tkontu/raappa`
- `jbogushefsky/hl7tofhir_rag_langchain_react`
- `sparshg3011/tripwire`
- `wranglatang/bridgeai`
- `tasnime-bbker/lunar-vision`
- `gobinfan/python-mcp-server-client`
- `javimaligno/mcp-server-bitbucket`
- `atharvsinha26052005/agent_sentinel_v1.0`
- `f5se/f5-guardrail-red-team-demo-app`
- `atara57769/mcp-system-info`
- `shettyodu/dhi`
- `manykarim/robotframework-heal`
- `zhiyuan-zhang0206/ava`
- `syedabdullah56/agentic-ai-class-2-giaic`
- `abelhubprog/writerzagents`
- `ancientdev0x/nanodistill`
- `datawhalechina/video-devour`
- `bullishoptionstrat-hub/quantumedgeflow`
- `amayuru1999/beehive`
- `fewsats/fewsats-python`
- `daksh-malhan/truth-constrained-resume-match-evaluator`
- `theritikasaini/mcp_gemini_cli`
- `stegish/bachelor-s-thesis`
- `cmput469/t8-ctrlaltelite`
- `saitejasathiraju/31-10-2025`
- `xianabcedesuba-ux/openai_api_key`
- `onurpolat05/n8n-assistant`
- `theailanguage/mcp-v2-server-examples`
- `arvind13s/papyrai-research-paper-assistant`
- `caraxesthebloodwyrm02/grove`
- `inoj-hettiarachchi/onelake-mcp`
- `mastermindx-market-intelligence/mastermind`
- `labscommunity/yeschef`
- `mykalmachon/outlook-mcp`
- `gymishra/sap_parent_mcp`
- `saintdoresh/yfinance-trader-mcp-claudedesktop`
- `fr0gger/mcp_security`
- `kevin-biot/mcp-lmstudio`
- `tusharmishra288/marketmeshai`
- `withsophie/be_sophie`
- `hiosdra/actions-latest-mcp`
- `m3tan01/openelia`
- `jagreehal/mcp-authz`
- `star-frost/k-context`
- `hucker/crcglot`
- `kazukodevv/mcp-examples`
- `oraichain/ragflow-mcp`
- `jesserweigel/get-legal-done`
- `hammadurrehman2006/the_evolution_of_todo`
- `dan1t0/gophish-mcp`
- `tool-genesis/tool-genesis`
- `aaa-927418924/sparkle`
- `pramoda-s-r/g7-cr`
- `testusuke/gpt-research-mcp`
- `eaglhuang/3klife`
- `mist-ic/haqdekho`
- `acaprino/daodan`
- `poojadesur/ai-powered-quantitative-trading-strategy-agent-`
- `pu11en/channel-brains`
- `kensou24/evernote-mcp`
- `ursuswh-metamorphic/pentestmatrix`
- `tosin2013/ansible-collection-mcp-audit`
- `bingstat/nexus`
- `arclio/github-projects-mcp`
- `scotmos/revit-mcp-copilot-integration`
- `taxicsv70-oss/claude-agents`

</details>

<details><summary>ツールパッケージ</summary>


</details>

