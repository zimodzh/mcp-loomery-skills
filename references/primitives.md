# Tools / Resources / Prompts

Source: official *Understanding MCP servers* and the 2026-07-28 spec. Picking the wrong primitive is the most common design error.

## Who controls it, when to use it

| Primitive | Who decides to use it | Meaning | Typical methods |
| --- | --- | --- | --- |
| **Tools** | The model (hosts MAY add human confirmation) | An **action** with side effects or a computed result | `tools/list`, `tools/call` |
| **Resources** | The application (host fetches, then decides whether to feed the model) | **Read-only** context with a URI + MIME type | `resources/list`, `resources/templates/list`, `resources/read` |
| **Prompts** | The user, explicitly (slash command, command palette) | Parameterized message templates | `prompts/list`, `prompts/get` |

Do not expose the same capability as two primitives. “Should I search flights now?” → tool. Host attaching `calendar://events/2024` as context → resource. User clicks “Plan a vacation” and fills a form → prompt.

## Tools

- Each tool: `name`, `description` (when to call it), `inputSchema` (JSON Schema **object**, never `null`).
- Prefer a human `title` and a `description` on every parameter.
- No parameters: `{ "type": "object", "additionalProperties": false }`.
- `name`: 1–128 characters, case-sensitive, only `A-Za-z0-9_.-`, unique within this server.
- Declare the `tools` capability. If the list can change, set `listChanged: true` and send updates only to clients that `subscriptions/listen` with `toolsListChanged: true`.
- `tools/list` **SHOULD** be stably ordered (client cache and LLM prompt cache).
- Annotations (`readOnlyHint` / `destructiveHint` / `idempotentHint`) are hints. **Clients MUST treat annotations as untrusted** unless the server itself is trusted.
- Large payloads: return `resource_link`. Do not embed whole files in the tool result.
- With `outputSchema`: `structuredContent` **MUST** match; **SHOULD** also include JSON as text for older clients.

## Resources

- Each resource has a URI (`config://app`, `file:///...`). Templates use `{param}`: `weather://forecast/{city}/{date}`.
- The application decides how to use them (tree, search, auto-attach). The model cannot `resources/read` unless the host exposes that as a tool.
- Watch for changes: `subscriptions/listen` + `resourceSubscriptions`; the server sends `notifications/resources/updated`.
- Filesystem-backed resources: resolve the path first, confirm it stays inside the allowed root, reject `..`, encoding tricks, and escaping symlinks.

## Prompts

- User-invoked. Do not expect the model to pick them automatically.
- `prompts/get` returns a messages array (usually `role: user` + text). Use `completable` / completion to help fill arguments.

## Combining servers

A travel product can be three servers: flights as tools, weather as resources, calendar as a prompt. Split a general-purpose MCP the same way. Do not dump config reads, database writes, and slash templates into one `do_anything` tool.
