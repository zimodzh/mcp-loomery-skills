# references/ directory

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

On-demand reference docs. `SKILL.md` keeps the workflow and hard rules; detail lives here. **Do not load every file at once.** The reference files themselves are English, matching the official MCP docs.

## Index

| File | What it covers | When to read it |
| --- | --- | --- |
| `primitives.md` | Tools / Resources / Prompts: who controls them, when to use each | Choosing primitives; avoid a catch-all tool |
| `protocol-2026.md` | 2026-07-28 delta vs older MCP: `_meta`, `server/discover`, dual-era, deprecations (including DCR) | Do not default to `initialize` / sampling / protocol logging / roots / DCR |
| `sdk-typescript.md` | TS SDK v2: `serveStdio`, `registerTool`, `createMcpHandler` | Default stack or the user asked for TypeScript |
| `sdk-python.md` | Python SDK v2: `MCPServer`, `mcp dev` / `mcp run` | User asked for Python or the project is already Python |
| `transports.md` | stdio vs Streamable HTTP wire rules | Choosing a transport; stdout; HTTP Host/Origin |
| `security.md` | MUST/MUST NOT for server authors | Paths, SSRF, handles, OAuth, token passthrough |
| `inspector.md` | MCP Inspector, `protocolEra`, and the debug loop | Cannot connect; tools missing; verify 2026 before host config |
| `client-config.md` | Cursor / Claude Desktop mcp.json | Host config, absolute paths, env |
| `registry.md` | Official MCP Registry and ownership proof | Only when the user asks to publish |

## Suggested order

- **New server:** `primitives.md` → `sdk-typescript.md` or `sdk-python.md` → `inspector.md` → `client-config.md`
- **Remote HTTP:** add `transports.md` and `security.md`
- **Protocol / older clients:** `protocol-2026.md`
- **Publish:** `registry.md`

That order follows scenarios A–E in `SKILL.md`.
