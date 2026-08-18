#!/usr/bin/env node
import { McpServer } from '@modelcontextprotocol/server';
import { serveStdio } from '@modelcontextprotocol/server/stdio';
import * as z from 'zod/v4';

const handle = serveStdio(() => {
  const server = new McpServer(
    { name: '{{SERVER_NAME}}', version: '1.0.0' },
    {
      instructions: 'Call ping to verify the server is reachable.'
    }
  );

  server.registerTool(
    'ping',
    {
      title: 'Ping',
      description: 'Return pong plus an optional message. Use to verify the MCP server is running.',
      inputSchema: z.object({
        message: z.string().optional().describe('Optional text to echo back')
      }),
      outputSchema: z.object({
        ok: z.boolean(),
        echo: z.string()
      })
    },
    async ({ message }) => {
      const output = { ok: true, echo: message ?? 'pong' };
      return {
        content: [{ type: 'text', text: JSON.stringify(output) }],
        structuredContent: output
      };
    }
  );

  server.registerResource(
    'about',
    'about://server',
    {
      title: 'About',
      description: 'Static server identity',
      mimeType: 'text/plain'
    },
    async uri => ({
      contents: [{ uri: uri.href, text: '{{SERVER_NAME}} MCP server' }]
    })
  );

  return server;
});

console.error('{{SERVER_NAME}} MCP server listening on stdio');

process.on('SIGINT', () => {
  void handle.close();
});
