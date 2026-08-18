# references/ 目录

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

按需加载的参考文档。`SKILL.md` 只保留核心流程和硬规则；细节在这里，agent **不要一次全读**。参考文件本身是英文，与官方 MCP 文档一致。

## 目录索引

| 文件 | 讲什么 | 何时读 |
| --- | --- | --- |
| `primitives.md` | Tools / Resources / Prompts 谁控制、何时用 | 选原语、避免做成万能 tool |
| `protocol-2026.md` | 2026-07-28 相对旧 MCP 的差集：`_meta`、`server/discover`、双时代、弃用项（含 DCR） | 不要用 `initialize` / sampling / protocol logging / roots / DCR 当新默认 |
| `sdk-typescript.md` | TS SDK v2：`serveStdio`、`registerTool`、`createMcpHandler` | 默认栈或用户指定 TypeScript |
| `sdk-python.md` | Python SDK v2：`MCPServer`、`mcp dev` / `mcp run` | 用户指定 Python 或已有 Python 项目 |
| `transports.md` | stdio vs Streamable HTTP 导线规则 | 选传输、stdio stdout、HTTP Host/Origin |
| `security.md` | server 作者的 MUST/MUST NOT | 路径、SSRF、handle、OAuth、token passthrough |
| `inspector.md` | MCP Inspector、`protocolEra` 与调试回路 | 连不上、工具不出现、先于 host 配置验证 2026 |
| `client-config.md` | Cursor / Claude Desktop 的 mcp.json | 写 host 配置、绝对路径、env |
| `registry.md` | 官方 MCP Registry 发布与所有权证明 | 用户明确要求发布时 |

## 阅读顺序建议

- **新建 server**：`primitives.md` → `sdk-typescript.md` 或 `sdk-python.md` → `inspector.md` → `client-config.md`
- **远程 HTTP**：再加上 `transports.md` 与 `security.md`
- **协议/旧客户端**：`protocol-2026.md`
- **发布**：`registry.md`

该顺序对应 `SKILL.md` 场景 A–E。
