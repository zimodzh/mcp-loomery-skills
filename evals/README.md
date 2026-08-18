# evals/ 目录

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

`description` 的触发评测与输出质量评测。方法论分别来自 Agent Skills《Optimizing skill descriptions》与《Evaluating skills》。

## 文件

| 文件 | 用途 |
| --- | --- |
| `trigger-queries.json` | 20 条触发查询：10 正例 + 10 负例 |
| `train_queries.json` | 训练集（12 条，约 60%） |
| `validation_queries.json` | 验证集（8 条，约 40%） |
| `evals.json` | 质量评测：with-skill vs without-skill 的任务与断言 |

## 触发集

- **正例**：中英、口语、不出现 “MCP” 的隐式需求（给 Cursor 加工具）、传输 / Inspector / Registry。
- **负例**：近邻（DSH 插件、Agent Skill、普通 REST、Chrome 扩展、独立 MCP client、LangChain tools、LSP、OpenAPI）+ 少量无关任务。

评测查询可以是中文：那是**真实用户怎么问**，不是技能说明书。`SKILL.md` 与 `references/` 正文仍是英文，与官方 MCP 文档一致。

### 训练 / 验证划分（固定，防过拟合）

只根据训练集失败改 description；用验证集决定哪一版更好。不要把失败 query 的原句关键词抄进 description。

## 运行触发评测

1. 把每条 query 发给目标 agent，记录是否加载了 `mcp-loomery`。
2. `should_trigger` 与实际一致即通过。
3. 每条建议跑 3 次，计算触发率；默认阈值 0.5。

## 质量评测

`evals.json` 的断言必须可观察（用了 v2 入口、stdio 无 stdout 日志、原语选择正确），不要断言某一句固定英文。
