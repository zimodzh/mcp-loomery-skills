# assets/ 目录

<p align="center">
  <samp>
    <strong>中文</strong> ·
    <a href="./README.en.md">English</a>
  </samp>
</p>

静态资源目录。放模板、图片、数据文件等 skill **不执行、但流程会用到**的素材。可执行代码在 `scripts/`，说明文档在 `references/`。

## 当前内容

```
assets/
└── templates/                 # scaffold.py 的源模板
    ├── README.md              # 生成进目标项目的说明（中文）
    ├── README.en.md           # 生成进目标项目的说明（英文）
    ├── typescript-stdio/
    ├── typescript-http/
    └── python-stdio/
```

`scripts/scaffold.py` 按 `--lang` / `--transport` 复制对应模板，并把 `{{SERVER_NAME}}` 等占位符替换掉。

## 什么样的东西放这里

- **模板**：最小 MCP server 工程（package.json / pyproject.toml / 入口源码）。
- 长模板或只在脚手架时用到的文件——不要内联进 `SKILL.md`，以保持渐进披露。

短的输出格式模板可以直接写在 `SKILL.md`；这里只放会生成到用户项目里的完整文件树。
