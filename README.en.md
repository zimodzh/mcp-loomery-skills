# mcp-loomery

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

An [Agent Skills](https://agentskills.io) skill for building general-purpose [**Model Context Protocol (MCP)**](https://modelcontextprotocol.io) **servers**. Protocol baseline: **2026-07-28**.

Distilled from the official English docs (local snapshot: `Documentation`, `Specification`, `Registry`, `Extensions`) and the official TypeScript / Python SDK v2 docs — not the old `initialize` / `FastMCP` / `@modelcontextprotocol/sdk` v1 default stack.

Once loaded, the agent follows one workflow: pick primitives, scaffold with SDK v2, verify with MCP Inspector, write host config, and publish to the official MCP Registry when asked.

## What’s in the skill

```
mcp-loomery/
├── SKILL.md              # entry: frontmatter, hard rules, scenarios, checklist
├── scripts/              # executables (see scripts/README.md)
│   ├── scaffold.py
│   └── check-server.py
├── references/           # on-demand docs (index: references/README.md)
├── assets/               # static templates (see assets/README.md)
├── evals/                # description trigger evals and quality evals
├── README.md             # Chinese
├── README.en.md          # this file
└── LICENSE
```

## Default stack

If the user does not name a language: **TypeScript SDK v2 + stdio + Inspector**. Switch to Python SDK v2 (`mcp` / `MCPServer`) when the project is already Python or the user asks for Python. If the website TypeScript weather sample still uses `StdioServerTransport` + `connect()`, that is a lagged 2025-era listing — new projects use `serveStdio`.

## Install

The skill name is `mcp-loomery`; the folder must match. The GitHub repository is `mcp-loomery-skills`. Clone into the skill folder name in one step:

```bash
git clone https://github.com/zimodzh/mcp-loomery-skills.git <your-skills-dir>/mcp-loomery
```

Replace `<your-skills-dir>` with the agent’s skills path. You can also unpack a zip and rename the folder to `mcp-loomery`.

| Agent | Project | User |
| --- | --- | --- |
| Cursor | `<project>/.cursor/skills/` | `~/.cursor/skills/` |
| Claude Code | `<project>/.claude/skills/` | `~/.claude/skills/` |
| VS Code Copilot | `<project>/.agents/skills/` | `~/.agents/skills/` |
| Other compatible agents | per that agent’s convention | same |

Verify: ask the agent to “create an MCP server” or 「写一个 MCP 服务器」— this skill should load.

## Validate this skill

```bash
python scripts/scaffold.py --help
python scripts/check-server.py --help
skills-ref validate .
```

## Scaffold a minimal server

```bash
python scripts/scaffold.py --name notes --lang typescript --transport stdio --out <absolute-path> --json
```

Then Inspector: `tools/list` plus at least one `tools/call`. Run `scripts/check-server.py`.

## Trigger evals

[`evals/trigger-queries.json`](evals/trigger-queries.json) is the description regression set (10 should-trigger + 10 should-not). Run it before changing the description. Method: [`evals/README.en.md`](evals/README.en.md).

## Scope

Covers writing, reviewing, debugging MCP **servers**, host config, and Registry publishing. Does not cover DSH/Cordis plugins, Chrome extensions, ordinary REST APIs, or a full MCP Apps UI implementation (load official Extensions only when the user asks).

## License

MIT — see [LICENSE](LICENSE).
