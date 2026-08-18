# Inspector and debugging

Source: official MCP Inspector and Debugging. Inspector is the first stop. Do not poke host config first.

## Inspector (`@modelcontextprotocol/inspector`)

Requires **Node 22.19+**. One binary, three clients:

| Client | Invocation | For |
| --- | --- | --- |
| Web (default) | `npx @modelcontextprotocol/inspector <server cmd>` | GUI: list/call, notification stream |
| CLI | same plus `--cli` | CI, agents, pipes |
| TUI | same plus `--tui` | no browser |

```bash
# stdio
npx @modelcontextprotocol/inspector node ./dist/index.js
npx @modelcontextprotocol/inspector uv run mcp run server.py

# published package
npx -y @modelcontextprotocol/inspector npx @modelcontextprotocol/server-filesystem ~/Desktop

# remote HTTP
npx @modelcontextprotocol/inspector --server-url https://api.example.com/mcp --transport http
```

CLI examples:

```bash
npx @modelcontextprotocol/inspector --cli node ./dist/index.js --method tools/list
npx @modelcontextprotocol/inspector --cli node ./dist/index.js --method tools/call --tool-name add_note --tool-arg text=hello --format json
```

`--web` / `--cli` / `--tui` are recognized only at the **front** of the command line; a later `--cli` is forwarded to the server. `mcp-inspector --help` is launcher help; `mcp-inspector --cli --help` is the full CLI flag list.

Python shortcut: `uv run mcp dev server.py` (the SDK launches Inspector).

## Protocol era (do not skip)

Each Inspector server has `protocolEra`: `legacy` / `auto` / `modern`. In the web client: **Server Settings**. In a catalog or config file: the `protocolEra` field. CLI/TUI read the same file.

| Era | What Inspector does at connect |
| --- | --- |
| `legacy` | **The default.** Plain `initialize`, no probing. Accepts 2025-era *and* dual-era `serveStdio`. Does **not** prove 2026 wiring. |
| `auto` | `server/discover` first; fall back to `initialize` on any non-modern outcome. |
| `modern` | Pin `2026-07-28`. No fallback — a non-modern server fails loudly. |

When this skill says “verify with Inspector”, set **`auto` or `modern`**. Leaving the default `legacy` only checks that *some* handshake works.

## Development loop

1. Write a minimal tool → connect Inspector → Tools tab list + call.
2. `python scripts/check-server.py --path <server-dir> --json`
3. Then write Cursor/Claude config. **Fully quit** the host and reopen it.
4. Code changes: stdio needs a host restart. Iterate in Inspector while developing.

## When it will not connect

1. Can the command run alone in a terminal (absolute paths, deps, permissions)?
2. Is stdout mixed with non-JSON (banners, `print`, progress bars)?
3. `server/discover`: `-32022` → supported versions; `-32602` → `_meta`; `-32021` → client capabilities.
4. Host logs:
   - Claude macOS: `~/Library/Logs/Claude` (`mcp.log` + `mcp-server-NAME.log` is stderr)
   - Claude Windows: `%APPDATA%\Claude\logs`
   - Cursor: MCP output panel / logs (follow the current Cursor UI)
5. Valid JSON? Absolute paths? `env` filled in for variables the host does not inherit (Windows often needs `APPDATA`)?
6. Protocol era: Inspector default is `legacy`. Switch to `auto`/`modern` to test 2026. Confirm you did not set `serveStdio` `legacy: 'reject'` unless the host is known-modern.

## Logging

stdio: stderr only, structured, include tool name and duration, **never** secrets. HTTP: the MCP client does not capture stderr — use your own aggregation or OpenTelemetry. Protocol `notifications/message` is deprecated.
