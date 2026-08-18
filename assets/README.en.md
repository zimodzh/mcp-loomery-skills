# assets/ directory

<p align="center">
  <samp>
    <a href="./README.md">中文</a> ·
    <strong>English</strong>
  </samp>
</p>

Static resources: templates, images, data files — material the skill **does not execute** but uses during the workflow. Runnable code lives in `scripts/`; narrative docs live in `references/`.

## Contents

```
assets/
└── templates/                 # source trees for scaffold.py
    ├── README.md              # copied into the generated project (Chinese)
    ├── README.en.md           # copied into the generated project (English)
    ├── typescript-stdio/
    ├── typescript-http/
    └── python-stdio/
```

`scripts/scaffold.py` copies the matching template for `--lang` / `--transport` and substitutes placeholders such as `{{SERVER_NAME}}`.

## What belongs here

- **Templates:** minimal MCP server projects (package.json / pyproject.toml / entry source).
- Long or scaffold-only files — keep them out of `SKILL.md` (progressive disclosure).

Short output-format snippets can stay inline in `SKILL.md`. This directory holds the full file trees written into the user’s project.
