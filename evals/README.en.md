# evals/ directory

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

Trigger evals for the `description` and quality evals for skill output. Methods: Agent Skills *Optimizing skill descriptions* and *Evaluating skills*.

## Files

| File | Purpose |
| --- | --- |
| `trigger-queries.json` | 20 trigger queries: 10 should-trigger + 10 should-not |
| `train_queries.json` | Train split (12, ~60%) |
| `validation_queries.json` | Validation split (8, ~40%) |
| `evals.json` | Quality cases: with-skill vs without-skill prompts and assertions |

## Trigger set

- **Positives:** English and Chinese, casual phrasing, implicit MCP (“add a tool the agent can use”), transports / Inspector / Registry.
- **Negatives:** near-misses (DSH plugins, Agent Skills, plain REST, Chrome extensions, standalone MCP clients, LangChain tools, LSP, OpenAPI) plus a few unrelated tasks.

Chinese queries stay on purpose: they are **how users actually ask**, not skill prose. `SKILL.md` and `references/` remain English, matching the official MCP docs.

### Train / validation (fixed, anti-overfit)

Change the description only from train failures. Pick the best iteration by validation pass rate. Do not copy failed-query wording into the description.

## Running trigger evals

1. Send each query to the target agent; record whether it loaded `mcp-loomery`.
2. A pass is `should_trigger` matching reality.
3. Run each query ~3 times; trigger-rate threshold 0.5.

## Quality evals

Assertions in `evals.json` must be observable (v2 entrypoint, no stdout logs, correct primitives). Do not assert a fixed English phrase.
