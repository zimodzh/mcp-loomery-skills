# mcp-loomery

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

一套遵循 [Agent Skills 规范](https://agentskills.io) 的技能，用于制作通用 [**Model Context Protocol（MCP）**](https://modelcontextprotocol.io) **服务器**。协议基线：**2026-07-28**。

内容蒸馏自官方英文文档（本地快照：`Documentation`、`Specification`、`Registry`、`Extensions`）以及官方 TypeScript / Python SDK v2 文档，而不是旧的 `initialize` / `FastMCP` / `@modelcontextprotocol/sdk` v1 默认栈。

加载本技能后，agent 会按同一套工作流：选原语、用 SDK v2 脚手架、用 MCP Inspector 验证、写 host 配置，并在需要时发布到官方 MCP Registry。

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
