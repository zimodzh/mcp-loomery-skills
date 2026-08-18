# mcp-loomery

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

一套遵循 [Agent Skills 规范](https://agentskills.io) 的技能，用于制作通用 [**Model Context Protocol（MCP）**](https://modelcontextprotocol.io) **服务器**。协议基线：**2026-07-28**。

## 这是什么

`mcp-loomery` 是一个 [Agent Skills](https://agentskills.io) 格式的技能（一个含 `SKILL.md` 的文件夹）。加载它之后，任何兼容的 agent（Cursor / Claude Code / Claude Desktop 等）都会获得一套标准流程，用来：

- **创建** MCP 服务器（tools / resources / prompts）
- **审查** TypeScript / Python SDK v2 接线与协议 **2026-07-28** 约定
- **调试**（MCP Inspector、stdio stdout、host 配置）
- **发布**到官方 MCP Registry（在你明确要求时）

内容蒸馏自官方英文文档（本地快照：`Documentation`、`Specification`、`Registry`、`Extensions`）以及官方 TypeScript / Python SDK v2 文档，而不是旧的 `initialize` / `FastMCP` / `@modelcontextprotocol/sdk` v1 默认栈。

## 技能里有什么

```
mcp-loomery/
├── SKILL.md              # 入口：frontmatter、硬规则、场景工作流、检查清单
├── scripts/              # 可执行脚本（说明见 scripts/README.md）
│   ├── scaffold.py
│   └── check-server.py
├── references/           # 按需加载的参考（索引见 references/README.md）
├── assets/               # 静态模板（说明见 assets/README.md）
├── evals/                # description 触发评测与质量评测
├── README.md             # 本文件（中文）
├── README.en.md          # 英文版
└── LICENSE
```

references 覆盖：原语分工 · 2026-07-28 协议差集 · TypeScript / Python SDK v2 · 传输 · 安全 · Inspector · host 配置 · Registry。

## 目录结构

```
mcp-loomery/
├── SKILL.md                                  # skill 入口：frontmatter、硬规则、场景工作流、检查清单
├── scripts/                                  # 可执行脚本（说明见 scripts/README.md）
│   ├── scaffold.py                           # 从模板生成最小 TS / Python MCP server
│   ├── check-server.py                       # 静态扫描 stdout 污染、v1 API、弃用原语、工具名
│   ├── README.md                             # 本目录说明（中文）
│   └── README.en.md                          # 本目录说明（英文）
├── references/                               # 按需加载的参考（渐进披露，索引见 references/README.md）
│   ├── primitives.md                         # Tools / Resources / Prompts
│   ├── protocol-2026.md                      # `_meta`、`server/discover`、双时代、弃用项
│   ├── sdk-typescript.md                     # `serveStdio`、`registerTool`、`createMcpHandler`
│   ├── sdk-python.md                         # `MCPServer`、`mcp dev` / `mcp run`
│   ├── transports.md                         # stdio vs Streamable HTTP
│   ├── security.md                           # server 作者的 MUST / MUST NOT
│   ├── inspector.md                          # MCP Inspector、`protocolEra`、调试回路
│   ├── client-config.md                      # Cursor / Claude Desktop mcp.json
│   ├── registry.md                           # 官方 MCP Registry 与所有权证明
│   ├── README.md                             # 本目录索引（中文）
│   └── README.en.md                          # 本目录索引（英文）
├── assets/                                   # 静态模板（说明见 assets/README.md）
│   ├── README.md
│   ├── README.en.md
│   └── templates/
│       ├── README.md                         # 生成进目标项目的 README（中文）
│       ├── README.en.md
│       ├── typescript-stdio/                 # 默认栈：TS + stdio + `serveStdio`
│       │   ├── package.json
│       │   ├── tsconfig.json
│       │   └── src/index.ts
│       ├── typescript-http/                  # TS + Streamable HTTP + `createMcpHandler`
│       │   ├── package.json
│       │   ├── tsconfig.json
│       │   └── src/index.ts
│       └── python-stdio/                     # Python SDK v2 + stdio
│           ├── pyproject.toml
│           └── server.py
├── evals/                                    # description 触发评测与质量评测
│   ├── trigger-queries.json                  # 20 条触发查询（10 正 + 10 负）
│   ├── train_queries.json                    # 训练集（12）
│   ├── validation_queries.json               # 验证集（8）
│   ├── evals.json                            # 质量评测任务与断言
│   ├── README.md                             # 评测方法（中文）
│   └── README.en.md                          # 评测方法（英文）
├── README.md                                 # 本文件（中文）
├── README.en.md                              # 英文版
├── LICENSE                                   # MIT
└── .gitignore
```

## 默认栈

用户未指定语言时：**TypeScript SDK v2 + stdio + Inspector**。已有 Python 项目或用户明确要求 Python 时改用 Python SDK v2（`mcp` / `MCPServer`）。官网 TypeScript 天气教程若仍是 `StdioServerTransport` + `connect()`，那是滞后的 2025 示例；新项目用 `serveStdio`。

## 安装

技能名为 `mcp-loomery`，Agent Skills 规范要求所在文件夹同名；本仓库名为 `mcp-loomery-skills`。克隆时直接指定目标文件夹名即可一步到位：

```bash
git clone https://github.com/zimodzh/mcp-loomery-skills.git <你的 skill 目录>/mcp-loomery
```

把 `<你的 skill 目录>` 换成所用 agent 的技能目录。也可以下载压缩包，解压后把文件夹改名为 `mcp-loomery`。

| Agent | 项目级 | 用户级 |
| --- | --- | --- |
| Cursor | `<project>/.cursor/skills/` | `~/.cursor/skills/` |
| Claude Code | `<project>/.claude/skills/` | `~/.claude/skills/` |
| VS Code Copilot | `<project>/.agents/skills/` | `~/.agents/skills/` |
| 其它兼容 agent | 按该 agent 的技能目录约定 | 同上 |

验证：向 agent 提问「写一个 MCP 服务器」或 “Create an MCP server”，技能应被触发。

## 校验本技能

```bash
python scripts/scaffold.py --help
python scripts/check-server.py --help
skills-ref validate .
```

## 脚手架一个最小 server

```bash
python scripts/scaffold.py --name notes --lang typescript --transport stdio --out <绝对路径> --json
```

然后用 MCP Inspector 做 `tools/list` 与至少一次 `tools/call`，再跑 `scripts/check-server.py`。

## 触发评测

[`evals/trigger-queries.json`](evals/trigger-queries.json) 是 description 的回归评测集（10 条正例 + 10 条负例）。修改 description 前先跑评测；方法论见 [`evals/README.md`](evals/README.md)。

## 范围边界

覆盖 MCP **server** 的编写、审查、调试、host 配置与 Registry 发布。不覆盖 DSH/Cordis 插件、Chrome 扩展、普通 REST API，也不覆盖完整的 MCP Apps UI 实现（仅在用户明确要求时再读官方 Extensions）。

## License

MIT——见 [LICENSE](LICENSE)。
