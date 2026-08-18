# Protocol 2026-07-28 (delta vs older MCP)

Source: official Architecture, Specification, stdio transport, and deprecations. For new servers, memorize this delta. The SDK owns most wire details.

## Participants

- **Host**: the AI app (Cursor, Claude Desktop, …).
- **Client**: one client object inside the host per server.
- **Server**: the program that serves context. stdio ≈ local, one client; Streamable HTTP ≈ remote, many clients.

Two layers: data (JSON-RPC primitives) + transport (stdio / Streamable HTTP). MCP does **not** specify how the host uses an LLM.

## Stateless + per-request `_meta`

Every request MUST include:

- `params._meta["io.modelcontextprotocol/protocolVersion"]`
- `params._meta["io.modelcontextprotocol/clientCapabilities"]`
- Recommended: `io.modelcontextprotocol/clientInfo` (name/version)

Missing required fields → `-32602` Invalid params. Server needs elicitation but the request did not declare it → `-32021` MissingRequiredClientCapabilityError.

Do **not** store business state “on this TCP/stdio connection”. Authorization MAY filter `tools/list` using **this request’s** credentials.

## Discovery: `server/discover`

This replaces `initialize` capability exchange on the modern path.

- Every server **MUST** implement it. Official SDKs **answer it automatically** from registered tools/resources/prompts.
- Response includes `supportedVersions`, `capabilities`, `serverInfo` (in result `_meta`), optional `ttlMs` / `cacheScope`.
- Unsupported version → `-32022` UnsupportedProtocolVersionError with supported versions in `data`. The client retries a shared version. It MUST NOT fall back to `initialize` because of `-32022`.
- Calling discover is **optional**: a client may send a business request immediately and negotiate via `_meta` and errors.

## Subscriptions, not a connection-level notify switch

Change notifications are opt-in. The client sends `subscriptions/listen` with a filter such as `toolsListChanged: true`. The server first sends `notifications/subscriptions/acknowledged` (`_meta.subscriptionId` = that listen request’s JSON-RPC id). Later notifications carry the same id. Notifications have no `id`, need no reply, and are best-effort. Clients should still poll for freshness.

## Dual-era (especially stdio)

| Era | How the client opens | Your v2 entry |
| --- | --- | --- |
| 2025 / legacy | `initialize` handshake | `serveStdio` default `legacy: 'serve'`; same factory, another instance |
| 2026-07-28 | `_meta` envelope + optional `server/discover` | connection pinned to a modern instance |

Modern client probe: `server/discover` first. DiscoverResult → modern. `-32022` → still modern, pick another version, **do not** fall back to initialize. Any other error or timeout → treat as legacy, then `initialize`.

`serveStdio(..., { legacy: 'reject' })` refuses old hosts. Cursor / Claude Desktop often still open legacy during the transition — **do not reject by default**.

A hand-wired `new StdioServerTransport() + server.connect()` server is **pinned to 2025 wire semantics** even after you bump the SDK package. Modern stdio requires `serveStdio`. The modelcontextprotocol.io *Build an MCP server* TypeScript sample may still show `connect()` — do not copy it for new projects. SDK source: [Serve over stdio](https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio.html).

HTTP equivalent: `createMcpHandler(factory)`. Default HTTP legacy posture is per-request and stateless (`legacy: 'stateless'` in the SDK). Fresh instance per request.

MCP Inspector defaults to `protocolEra=legacy` (plain `initialize`). Use `auto` or `modern` when you need to prove 2026-07-28. See [inspector.md](inspector.md).

## Deprecated in 2026-07-28 (SEP-2577)

Deprecation window is at least twelve months. SDKs still run these APIs. **Do not use them in new code:**

| Deprecated | Do this instead |
| --- | --- |
| Sampling (`sampling/createMessage`) | Call an LLM provider API from the server |
| Logging (`notifications/message`) | stdio → stderr; any transport → OpenTelemetry |
| Roots | Tool arguments, resource URIs, or config |
| Dynamic Client Registration | Client ID Metadata Documents (load official Authorization docs when the user asks for OAuth) |

Elicitation is still a current client primitive (form / url), delivered through Multi Round-Trip Requests (`resultType: "input_required"`). Secrets: url mode only. On stdio the server **MUST NOT** write JSON-RPC **requests** to stdout; ask the client via InputRequiredResult.

## Result shape

Modern results carry `resultType` (`"complete"`, `"input_required"`, …). The SDK fills `ttlMs` / `cacheScope` from your cache hints.
