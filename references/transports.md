# Transports

Source: Architecture, stdio spec, Streamable HTTP, TypeScript serving docs.

## How to choose

| | **stdio** (default) | **Streamable HTTP** |
| --- | --- | --- |
| Process | Local child process spawned by the host | Standalone HTTP service, many clients |
| Channel | stdin JSON-RPC → stdout JSON-RPC; logs on stderr | HTTP POST; optional SSE |
| Auth | Usually OS user + host config | Bearer / OAuth (MCP recommends OAuth for tokens) |
| Fit | Cursor / Claude Desktop local servers | Remote, multi-user, horizontal scale |

The same tools can sit behind both entries (TS: `serveStdio` for stdio, `createMcpHandler` for HTTP; share a `createServer()` / factory).

## stdio wire rules (fragile — follow the spec)

- One JSON-RPC message per line. Embedded `\n` inside a message is forbidden.
- stdout MAY contain only valid MCP messages. `console.log` / `print` make the host fail to parse.
- stderr is free-form UTF-8. Hosts SHOULD NOT treat stderr as an error by itself.
- Modern path: the server MUST NOT write JSON-RPC *requests* to stdout. Ask the client via `InputRequiredResult`.
- Cancellation: `notifications/cancelled`. stdio has no per-request SSE stream to close.
- Graceful shutdown: the client closes stdin; the server SHOULD exit promptly on EOF. Windows has no POSIX signals; forced kill uses `TerminateProcess` / Job Objects.
- After a crash there is no session to restore. In-flight work is lost. Re-open `subscriptions/listen`.

## Streamable HTTP

- Client → server: HTTP POST. Streaming uses SSE.
- Stateless default: `createMcpHandler` builds a **new** `McpServer` per request. Sessions, resumable SSE, and multi-node fan-out live in SDK examples — do not add them preventively.
- Auth: verify in front of the handler, pass the result as `authInfo`. Do not forward a token issued for some other audience (token passthrough).
- Browser or localhost: validate `Host` (DNS rebinding) and `Origin`. Prefer `createMcpExpressApp` / `createMcpHonoApp`. Binding `0.0.0.0` needs `allowedHosts`.
- `x-mcp-header`: mirror **non-sensitive** primitive parameters as `Mcp-Param-*` for gateway routing. Never mark secrets or PII.

## Do not invent a third transport

Custom Unix sockets / TCP SHOULD reuse stdio’s newline-delimited JSON-RPC framing and only replace process lifecycle. Official transports are stdio and Streamable HTTP. Legacy SSE is not an option for new projects.
