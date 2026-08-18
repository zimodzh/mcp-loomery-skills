# scripts/ directory

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

Executable scripts. After this skill activates, the agent should run these instead of reinventing the same logic.

## What this is, per the spec

Agent Skills put **runnable code** in `scripts/`: self-contained or clearly declared deps, useful errors, edge-case handling, agent-friendly (never interactive, `--help`, structured output, idempotent, `--dry-run`).

## Scripts

| Script | What it does |
| --- | --- |
| `scaffold.py` | Generate a minimal runnable TS / Python MCP server from `assets/templates/` |
| `check-server.py` | Static scan for stdout pollution, v1 APIs, deprecated primitives, tool names, HTTP factory registration |

Read `--help` first. Data on stdout, diagnostics on stderr. Prefer `--json` for agents.

### scaffold.py

```bash
python scripts/scaffold.py --name notes --lang typescript --transport stdio --out <absolute-path> --json
python scripts/scaffold.py --name notes --lang python --transport stdio --out <absolute-path> --dry-run --json
```

| Flag | Meaning |
| --- | --- |
| `--name` | kebab-case server name |
| `--lang` | `typescript` (default) or `python` |
| `--transport` | `stdio` (default) or `http` (TypeScript template only) |
| `--out` | **absolute** output directory |
| `--dry-run` | print the file plan only |
| `--force` | allow a non-empty destination (still refuses overwrites) |
| `--json` | JSON on stdout |

Python HTTP is not a separate template: scaffold `stdio`, then `uv run mcp run server.py --transport streamable-http`.

Exit codes: `2` bad args; `3` destination not empty; `4` refuse overwrite.

### check-server.py

```bash
python scripts/check-server.py --path <server dir or file> --json
python scripts/check-server.py --path <server dir> --dry-run --json
```

`--dry-run` lists files that would be scanned. Exit `2` when any finding has severity `error`; warnings still exit `0`.

## Rules for adding scripts later

- Never interactive: flags / env / stdin only.
- `--help`: how the agent learns the interface.
- Structured output: prefer JSON.
- Idempotent, `--dry-run`, meaningful exit codes.
