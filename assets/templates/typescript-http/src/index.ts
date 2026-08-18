#!/usr/bin/env node
import { createServer } from 'node:http';
import { createMcpHandler, McpServer } from '@modelcontextprotocol/server';
import { localhostHostValidation, localhostOriginValidation, toNodeHandler } from '@modelcontextprotocol/node';
import * as z from 'zod/v4';

function createNotesServer() {
  const server = new McpServer({ name: '{{SERVER_NAME}}', version: '1.0.0' });
  server.registerTool(
    'ping',
    {
      title: 'Ping',
      description: 'Return pong plus an optional message. Use to verify the MCP server is running.',
      inputSchema: z.object({
        message: z.string().optional().describe('Optional text to echo back')
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
  return server;
}

const handler = createMcpHandler(() => createNotesServer());
const nodeHandler = toNodeHandler(handler);
const validateHost = localhostHostValidation();
const validateOrigin = localhostOriginValidation();

const port = Number(process.env.PORT ?? 3000);
const httpServer = createServer((req, res) => {
  if (!validateHost(req, res) || !validateOrigin(req, res)) return;
  void nodeHandler(req, res);
});

httpServer.listen(port, '127.0.0.1', () => {
  console.error(`{{SERVER_NAME}} MCP server on http://127.0.0.1:${port}/mcp`);
});

process.on('SIGINT', () => {
  httpServer.close();
  void handler.close();
});
