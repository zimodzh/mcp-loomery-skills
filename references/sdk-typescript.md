# TypeScript SDK v2

Source: official TypeScript SDK Server Guide and the `serveStdio` / `createMcpHandler` docs. Package names follow npm `@modelcontextprotocol/server`.

## Which package

| Package | Use |
| --- | --- |
| `@modelcontextprotocol/server` | `McpServer`, `createMcpHandler`, `ResourceTemplate`, `completable` |
| `@modelcontextprotocol/server/stdio` | `serveStdio` (modern stdio entry) |
| `zod` **v4** | `import * as z from 'zod/v4'` for input/output schemas |
| `@modelcontextprotocol/express` / `hono` / matching Fastify helper | HTTP app factories (Host/Origin checks on by default) |
| `@modelcontextprotocol/node` | `toNodeHandler`, `localhostHostValidation` |
| `@modelcontextprotocol/sdk` | **v1 / 2025 line** — not the default for new projects |

## Minimal stdio server

```ts
import { McpServer } from '@modelcontextprotocol/server';
import { serveStdio } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const handle = serveStdio(() => {
  const server = new McpServer(
    { name: 'notes', version: '1.0.0' },
    {
      instructions:
        'Call list_notes before mutating. Titles are unique per caller.'
    }
  );

  server.registerTool(
    'add_note',
    {
      title: 'Add note',
      description: 'Save a short note. Use when the user asks to remember text.',
      inputSchema: z.object({
        text: z.string().describe('Note body')
      }),
      outputSchema: z.object({ id: z.string() })
    },
    async ({ text }) => {
      const output = { id: 'n1' };
      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output
      };
    }
  );

  return server;
});

console.error('notes MCP server listening on stdio');

process.on('SIGINT', () => {
  void handle.close();
});
```

`instructions` go into the host system prompt: cross-tool order and constraints. Do **not** repeat each tool’s description.

## Registration API

- Tools: `registerTool(name, { title, description, inputSchema, outputSchema?, annotations?, icons? }, handler)`
- Resources: `registerResource(name, uriOrTemplate, metadata, readHandler)`
- Templates: `new ResourceTemplate('user://{userId}/profile', { list })`
- Prompts: `registerPrompt(name, { title, description, argsSchema }, factory)`
- Completions: `completable(z.string(), prefix => suggestions)`

Handler signature: `(args, ctx)`. On a modern connection, read identity from `ctx.mcpReq.envelope`, not a connection-scoped cached clientInfo.

### Errors

Return `{ content: [{ type: 'text', text: '...' }], isError: true }`. Thrown exceptions become `isError`, but an explicit return controls the message. `isError: true` skips output-schema validation.

### Progress

Only if `ctx.mcpReq._meta?.progressToken` is set: `ctx.mcpReq.notify({ method: 'notifications/progress', params: { progressToken, progress, total?, message? } })`. `progress` MUST increase monotonically.

### Elicitation

`ctx.mcpReq.elicitInput({ mode: 'form' | 'url', ... })`. Secrets, payments, and OAuth MUST NOT use form mode.

## HTTP

```ts
import { createMcpHandler, McpServer } from '@modelcontextprotocol/server';

const handler = createMcpHandler(({ authInfo }) => {
  const server = new McpServer({ name: 'notes', version: '1.0.0' });
  // register tools HERE — factory runs once per request
  return server;
});
```

- Do not register on a module-level `McpServer` singleton.
- Keep heavy resources (DB pools) at module scope; the factory closes over them.
- `handler.fetch` is Web `Request => Response`. Node frameworks: `toNodeHandler(handler)`.
- **The handler does not check Host, Origin, or tokens.** Put framework factories or `localhostHostValidation` + `localhostOriginValidation` in front. After auth succeeds: `handler.fetch(request, { authInfo })`.
- `responseMode: 'json'` drops mid-call notifications and keeps only the terminal result.

Enable DNS-rebinding protection when binding `127.0.0.1` / `localhost`. Provide `allowedHosts` when binding `0.0.0.0`.

## Old wiring (do not use as the new stdio default)

```ts
// Pins 2025-era wire behavior
const transport = new StdioServerTransport();
await server.connect(transport);
```

The new default is always `serveStdio(() => server)`. Official docs: [Serve over stdio](https://ts.sdk.modelcontextprotocol.io/v2/serving/stdio.html). The website *Build an MCP server* TypeScript listing may still show `connect()`; treat it as lagged.
