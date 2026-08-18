# {{SERVER_NAME}}

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

由 mcp-loomery 生成的本地 MCP 服务器。

## 运行

TypeScript：

```bash
npm install
npm run inspector
```

Python：

```bash
uv sync
uv run mcp dev server.py
```

stdio 日志只能写 **stderr**。不要对 stdout 使用 `console.log` / `print`。
