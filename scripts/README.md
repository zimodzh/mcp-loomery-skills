# scripts/ 目录

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

可执行脚本目录。agent 激活本技能后应直接跑这里的脚本，不要现场重写同等逻辑。

## 按规范，这是什么

Agent Skills 约定 `scripts/` 放**可执行代码**：自包含或声明依赖、友好报错、处理边界情况、面向 agent 调用（不交互、有 `--help`、结构化输出、幂等、`--dry-run`）。

## 当前脚本

| 脚本 | 做什么 |
| --- | --- |
| `scaffold.py` | 从 `assets/templates/` 生成最小可跑的 TS / Python MCP server |
| `check-server.py` | 静态扫描 stdout 污染、v1 API、弃用原语、工具名、HTTP 工厂注册位置 |

先读 `--help`。数据走 stdout，诊断走 stderr。默认 `--json` 便于 agent 解析。

### scaffold.py

```bash
python scripts/scaffold.py --name notes --lang typescript --transport stdio --out <绝对路径> --json
python scripts/scaffold.py --name notes --lang python --transport stdio --out <绝对路径> --dry-run --json
```

| 参数 | 说明 |
| --- | --- |
| `--name` | kebab-case 服务器名 |
| `--lang` | `typescript`（默认）或 `python` |
| `--transport` | `stdio`（默认）或 `http`（仅 TypeScript 有独立模板） |
| `--out` | **绝对路径**输出目录 |
| `--dry-run` | 只打印将写入的文件 |
| `--force` | 允许非空目录（仍拒绝覆盖已有文件） |
| `--json` | stdout 输出 JSON |

Python 的 HTTP 不是单独模板：先 `stdio` 脚手架，再用 `uv run mcp run server.py --transport streamable-http`。

退出码：`2` 参数不合法；`3` 目标非空；`4` 拒绝覆盖。

### check-server.py

```bash
python scripts/check-server.py --path <server 目录或文件> --json
python scripts/check-server.py --path <server 目录> --dry-run --json
```

`--dry-run` 只列出将扫描的源文件。有 `error` 级发现时退出码为 `2`；仅 warning 仍为 `0`。

## 脚本设计约束（给以后加脚本的人）

- **不交互**：全部用 flags / env / stdin。
- **`--help`**：agent 靠它学接口。
- **结构化输出**：优先 JSON。
- **幂等 + `--dry-run` + 有意义的退出码**。
