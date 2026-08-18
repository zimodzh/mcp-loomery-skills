---
name: mcp-loomery
description: "制作、审查、调试或发布 Model Context Protocol（MCP）服务器：tools、resources、prompts、stdio 与 Streamable HTTP、TypeScript SDK v2（@modelcontextprotocol/server）与 Python SDK v2（mcp / MCPServer）、MCP Inspector、Cursor/Claude Desktop mcp.json、OAuth、官方 MCP Registry。当需要创建或修复 MCP 服务器、MCP 工具、resource、prompt、本地 agent 能力或 host 配置时使用——即使用户没说 MCP。不要用于 DSH/Cordis 插件、Chrome 扩展、或不接 MCP host 的普通 REST API。 Build, review, debug, or publish a Model Context Protocol (MCP) server: tools, resources, prompts, stdio and Streamable HTTP, TypeScript SDK v2 (@modelcontextprotocol/server) and Python SDK v2 (mcp / MCPServer), MCP Inspector, Cursor/Claude Desktop mcp.json, OAuth, and the official MCP Registry. Use when creating or fixing an MCP server, MCP tool, resource, prompt, local agent capability, or host config — even if the user does not say MCP. Do not use for DSH/Cordis plugins, Chrome extensions, or ordinary REST APIs with no MCP host."
license: MIT
compatibility: "Any Agent Skills host. Default stack: Node 22.19+ or Python 3.10+, network for SDKs/Inspector. Protocol baseline: 2026-07-28."
metadata:
  author: zimo
  version: "1.3.0"
  protocol: "2026-07-28"
---

# Build a general-purpose MCP server

This skill turns the official MCP docs ([modelcontextprotocol.io](https://modelcontextprotocol.io), protocol **2026-07-28**) into an executable workflow: a discoverable, callable, debuggable server for any MCP host (Cursor, Claude Desktop, and others). Do not treat older MCP patterns from training data (`initialize` handshake, `FastMCP`, `@modelcontextprotocol/sdk` v1) as the current default.

Authoritative sources are the official documentation snapshot beside this repo (`Documentation`, `Specification`, `Registry`, `Extensions`) and the matching SDK docs. Write only conventions the agent gets wrong.

## Scope

- Create or change an MCP **server** that exposes tools, resources, and/or prompts.
- Choose a transport (default **stdio**; **Streamable HTTP** for remote or multi-client), use an official SDK, verify with Inspector, write host config, and publish to the MCP Registry when asked.
- This skill does **not** cover: DSH/Cordis plugins; a standalone MCP **client** app (except to test the server you are building); a full MCP Apps UI implementation (load official Extensions only when the user asks for that).

## Hard rules (every scenario)

1. **Protocol baseline is 2026-07-28.** The data layer is stateless JSON-RPC. Every request carries `_meta` (`io.modelcontextprotocol/protocolVersion`, `clientCapabilities`, and recommended `clientInfo`). Discovery is **`server/discover`**. The SDK answers discover and stamps `resultType` / `ttlMs` / `cacheScope` — do not hand-write discover or initialize handlers.
2. **New projects use SDK v2, not the v1 default stack.** TypeScript: `@modelcontextprotocol/server` + `serveStdio` / `createMcpHandler`. Python: `mcp` 2.x `MCPServer` + `@mcp.tool()`. `@modelcontextprotocol/sdk` and `FastMCP` are the old line; use them only when maintaining existing code. The modelcontextprotocol.io *Build an MCP server* TypeScript sample may still show `StdioServerTransport` + `server.connect()` — that pins 2025-era wire; do not copy it for new work. Official TS stdio entry: [https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio.html](https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio.html).
3. **stdio stdout is MCP messages only.** Log to stderr (TS: `console.error`; Python: `logging` to stderr). Ban `console.log`, bare `print()`, and `print(..., file=sys.stdout)`. `print(..., file=sys.stderr)` is allowed. Messages are newline-delimited and **MUST NOT** contain embedded newlines.
4. **Pick the primitive before writing code.** Tools = model-decided actions; Resources = app-fetched read-only context; Prompts = user-invoked templates. Do not mix those jobs. See [references/primitives.md](references/primitives.md).
5. **Tool execution failures are `isError: true` tool results** so the model can self-correct. JSON-RPC errors are only for unknown tools, malformed requests, and server faults. If you declare `outputSchema`, `structuredContent` MUST match it, and you SHOULD also return serialized JSON as text content.
6. **No implicit session on the connection.** The protocol has no connection-scoped business state. Carry cross-call state as an explicit handle returned by a tool (opaque, TTL, re-check auth every call). A handle is **not** a capability.
7. **Secure defaults.** Validate every tool input; filesystem resources must block `..` and symlink escape; treat annotations as untrusted hints; no token passthrough (accept only tokens issued to this MCP server); localhost HTTP MUST validate Host/Origin (DNS rebinding). Do not collect secrets via form elicitation or `x-mcp-header`.
8. **New code must not depend on deprecated features.** As of 2026-07-28, **Sampling, protocol Logging (`notifications/message`), Roots, and Dynamic Client Registration (DCR)** are deprecated (removal no earlier than 2027-07-28). Log to stderr or OpenTelemetry; call a provider API when you need an LLM; pass workspace paths via tool arguments, resource URIs, or config. For OAuth, use Client ID Metadata Documents instead of DCR — load the official Authorization docs only when the user asks for auth.
9. **Absolute paths in config and debugging.** A host-spawned stdio process may have cwd `/`. Inspector first, then Cursor / Claude config.

## Default stack (not a menu)

If the user does not name a language: **TypeScript SDK v2 + stdio + Inspector**. Switch to Python SDK v2 when the project is already Python or the user asks for Python. Other official SDKs (C#, Go, Java, Rust, Ruby, PHP, Kotlin, Swift) only when the user specifies that language — open that SDK’s docs first.

The website TypeScript weather sample may still use `StdioServerTransport` + `connect()`. Treat that as a lagged 2025-era example. New servers use `serveStdio`.

| Need | Default |
| --- | --- |
| Local, host-spawned child process | stdio + `serveStdio` / `mcp run` |
| Remote, multi-client, horizontally scalable | Streamable HTTP + `createMcpHandler` (fresh instance per request) |
| Verification | `npx @modelcontextprotocol/inspector` (Node **22.19+**) |
| Structured tool arguments | TS: Zod v4 (`zod/v4`); Python: type hints are the schema |

## Standard workflow

### Scenario A: New general-purpose MCP server

1. In one sentence: what **actions** the model should take (tools), what **read-only context** the app should fetch (resources), whether the user needs a **slash template** (prompts). Most servers start with 1–3 tools. Do not add every primitive preventively.
2. Choose language and transport. Default TS + stdio.
3. Scaffold (run against the target directory; `--dry-run` first):

```bash
python scripts/scaffold.py --name <server-name> --lang typescript --transport stdio --out <abs-path> --json
```

4. Put business logic in `registerTool` / `@mcp.tool`: `name` (1–128, `A-Za-z0-9_.-`), `title`, `description` (when to call it), `inputSchema`. Tool names are unique **within this server**.
5. Run Inspector with **`protocolEra=auto` or `modern`** (the Inspector default is **`legacy`** = plain `initialize`, which cannot tell 2026 wiring from 2025). Then `tools/list` plus at least one successful `tools/call`. Then `scripts/check-server.py`.
6. Write host config ([references/client-config.md](references/client-config.md)) with **absolute** command/args. Fully quit and restart the host.

### Scenario B: Add a tool / resource / prompt to an existing server

1. Read the entrypoint. Confirm v2 (`McpServer` / `MCPServer`) vs v1. Change v1 in-place with that SDK; do not mix both package lines as the default.
2. HTTP path: register **inside the factory** (`createMcpHandler(() => { ... register ... })`), never on a module-level shared instance.
3. Inspector regression: list + get/call/read for the new primitive. If the list can change, declare `listChanged` and use `subscriptions/listen`.

### Scenario C: Turn it into a remote HTTP server

1. Read [references/transports.md](references/transports.md) and the HTTP section of [references/sdk-typescript.md](references/sdk-typescript.md).
2. Use `createMcpHandler(factory)`. The factory **builds a new `McpServer` per request**. Heavy objects (DB pools) live at module scope.
3. Mount Host/Origin checks: prefer `createMcpExpressApp` / `createMcpHonoApp` / `createMcpFastifyApp` (on by default for localhost). Bare `node:http` must compose `localhostHostValidation` + `localhostOriginValidation`. Binding `0.0.0.0` requires `allowedHosts`.
4. Verify auth **in front of** the handler, then pass `authInfo` into `fetch`. The handler does not verify tokens.

### Scenario D: Cannot connect / tools missing / calls crash

Follow [references/inspector.md](references/inspector.md): Inspector standalone → stderr → host logs → `server/discover` and `_meta` → config JSON / absolute paths / env. Common codes: `-32022` protocol version; `-32602` missing `_meta` or malformed params; `-32021` missing client capability (e.g. elicitation).

### Scenario E: Publish to the official MCP Registry

Inspector-stable list/call first, then [references/registry.md](references/registry.md). The Registry is still preview. Package type determines ownership proof (`mcpName` on npm, `mcp-name:` in a PyPI README, and so on).

## Decision table

| I want to… | Do this | Details |
| --- | --- | --- |
| Let the model take an action | `registerTool` / `@mcp.tool` | [references/primitives.md](references/primitives.md) |
| Give the app read-only context | `registerResource` / `@mcp.resource` | same |
| Give the user an invokable template | `registerPrompt` / `@mcp.prompt` | same |
| Wire a local Cursor/Claude server | stdio + mcp.json / claude_desktop_config.json | [references/client-config.md](references/client-config.md) |
| Serve many remote clients | Streamable HTTP | [references/transports.md](references/transports.md) |
| Keep older clients working | `serveStdio` default `legacy: 'serve'`; `legacy: 'reject'` only for 2026-only | [references/protocol-2026.md](references/protocol-2026.md) |
| Ask the user for non-secret input | elicitation `mode: 'form'` (via MRTR) | [references/sdk-typescript.md](references/sdk-typescript.md) |
| Ask for secrets / payments | elicitation `mode: 'url'` or an out-of-band flow | same |
| Report long-running progress | `notifications/progress` only if `_meta.progressToken` is present | same |

## Scripts

- **`scripts/scaffold.py`** — minimal TS or Python server (`--lang` `--transport` `--out` `--dry-run` `--json`).
- **`scripts/check-server.py`** — scan for stdout pollution, v1 APIs, deprecated primitives, tool names, HTTP factory registration (`--path` `--json`).

Read `--help` first. Never interactive. Data on stdout, diagnostics on stderr.

## Checklist before you stop

- [ ] Primitive choice is correct: action = tool, read-only context = resource, user template = prompt.
- [ ] SDK v2 entry (`serveStdio` / `createMcpHandler` or Python `MCPServer`); no hand-written `server/discover`.
- [ ] stdio: no stdout logs; host config uses absolute command/args/env.
- [ ] Each tool has a clear description, a legal name, and an object `inputSchema` (no-args: `{ "type": "object", "additionalProperties": false }`).
- [ ] Business errors return `isError: true`; `outputSchema` implies valid `structuredContent`.
- [ ] File/URL inputs are path- or SSRF-constrained.
- [ ] HTTP: Host/Origin validation; no token passthrough.
- [ ] New code does not add sampling / protocol logging / roots.
- [ ] Inspector: `protocolEra=auto` or `modern`; `tools/list` + at least one successful `tools/call`; `check-server.py` reports no errors.

## References (load on demand; do not read all at once)

- [references/primitives.md](references/primitives.md) — when to use tool / resource / prompt
- [references/protocol-2026.md](references/protocol-2026.md) — 2026-07-28 discovery, `_meta`, dual-era, deprecations
- [references/sdk-typescript.md](references/sdk-typescript.md) — TS v2 registration and serving
- [references/sdk-python.md](references/sdk-python.md) — Python v2 `MCPServer`
- [references/transports.md](references/transports.md) — stdio vs Streamable HTTP
- [references/security.md](references/security.md) — official security MUST/MUST NOT
- [references/inspector.md](references/inspector.md) — Inspector and debug loop
- [references/client-config.md](references/client-config.md) — Cursor / Claude Desktop config
- [references/registry.md](references/registry.md) — publishing to the official Registry

## Gotchas

- After changing host config, **fully quit** the client and reopen it. Closing a window is not enough.
- A stdio server’s cwd is often not the project directory; relative paths fail silently.
- The `tools/list` set MUST NOT change as a side effect of other requests on the same connection; it MAY vary by **this request’s** authorization.
- Aggregators collide on tool names; do not treat `serverInfo.name` as a globally unique id.
- Inspector’s default `protocolEra` is **`legacy`** (plain `initialize`, no probing). That path will accept both `serveStdio` and a hand-wired `connect()`. To verify 2026-07-28, set Server Settings / config to `auto` or `modern`. `serveStdio` is dual-era by default (`legacy: 'serve'`). Do not set `legacy: 'reject'` just to be “pure” — Cursor/Claude may fail to connect.
- Python: `pip install mcp` now installs 2.x. Pin `mcp>=1.28,<2` only when maintaining v1.

## Validation

- With the CLI: `skills-ref validate .`
- Trigger regression: `evals/trigger-queries.json` (split in `evals/README.md`)
- Behavior: scaffold a minimal server → Inspector list/call → `scripts/check-server.py` clean
