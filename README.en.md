# mcp-loomery

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

An [Agent Skills](https://agentskills.io) skill for building general-purpose [**Model Context Protocol (MCP)**](https://modelcontextprotocol.io) **servers**. Protocol baseline: **2026-07-28**.

## What is this

`mcp-loomery` is an [Agent Skills](https://agentskills.io)-format skill (a folder containing a `SKILL.md`). Once loaded, any compatible agent (Cursor / Claude Code / Claude Desktop, and others) gains a standard workflow to:

- **Create** an MCP server (tools / resources / prompts)
- **Review** TypeScript / Python SDK v2 wiring against protocol **2026-07-28**
- **Debug** (MCP Inspector, stdio stdout, host config)
- **Publish** to the official MCP Registry (when you ask)

Distilled from the official English docs (local snapshot: `Documentation`, `Specification`, `Registry`, `Extensions`) and the official TypeScript / Python SDK v2 docs — not the old `initialize` / `FastMCP` / `@modelcontextprotocol/sdk` v1 default stack.

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

references cover: primitives · 2026-07-28 protocol delta · TypeScript / Python SDK v2 · transports · security · Inspector · host config · Registry.

## Directory structure

```
mcp-loomery/
├── SKILL.md                                  # entry: frontmatter, hard rules, scenarios, checklist
├── scripts/                                  # executables (see scripts/README.md)
│   ├── scaffold.py                           # generate a minimal TS / Python MCP server from templates
│   ├── check-server.py                       # scan stdout pollution, v1 APIs, deprecated primitives, tool names
│   ├── README.md                             # this directory (Chinese)
│   └── README.en.md                          # this directory (English)
├── references/                               # on-demand docs (progressive disclosure; index: references/README.md)
│   ├── primitives.md                         # Tools / Resources / Prompts
│   ├── protocol-2026.md                      # `_meta`, `server/discover`, dual-era, deprecations
│   ├── sdk-typescript.md                     # `serveStdio`, `registerTool`, `createMcpHandler`
│   ├── sdk-python.md                         # `MCPServer`, `mcp dev` / `mcp run`
│   ├── transports.md                         # stdio vs Streamable HTTP
│   ├── security.md                           # MUST / MUST NOT for server authors
│   ├── inspector.md                          # MCP Inspector, `protocolEra`, debug loop
│   ├── client-config.md                      # Cursor / Claude Desktop mcp.json
│   ├── registry.md                           # official MCP Registry and ownership proof
│   ├── README.md                             # directory index (Chinese)
│   └── README.en.md                          # directory index (English)
├── assets/                                   # static templates (see assets/README.md)
│   ├── README.md
│   ├── README.en.md
│   └── templates/
│       ├── README.md                         # README copied into generated projects (Chinese)
│       ├── README.en.md
│       ├── typescript-stdio/                 # default stack: TS + stdio + `serveStdio`
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
├── evals/                                    # description trigger evals and quality evals
│   ├── trigger-queries.json                  # 20 trigger queries (10 should / 10 should-not)
│   ├── train_queries.json                    # train split (12)
│   ├── validation_queries.json               # validation split (8)
│   ├── evals.json                            # quality tasks and assertions
│   ├── README.md                             # eval method (Chinese)
│   └── README.en.md                          # eval method (English)
├── README.md                                 # Chinese
├── README.en.md                              # this file
├── LICENSE                                   # MIT
└── .gitignore
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
