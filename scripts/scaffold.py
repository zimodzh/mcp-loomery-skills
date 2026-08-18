#!/usr/bin/env python3
"""Scaffold a minimal MCP server from mcp-loomery templates.

Never interactive. Data on stdout (human or --json); diagnostics on stderr.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = SKILL_ROOT / "assets" / "templates"
NAME_RE = re.compile(r"^[a-z0-9]([a-z0-9-]*[a-z0-9])?$")

LANGS = ("typescript", "python")
TRANSPORTS = ("stdio", "http")


def fail(code: int, message: str, *, json_mode: bool) -> None:
    if json_mode:
        print(json.dumps({"ok": False, "error": message}, ensure_ascii=False), file=sys.stdout)
    else:
        print(message, file=sys.stderr)
    raise SystemExit(code)


def to_package(name: str) -> str:
    return name.replace("_", "-")


def render(text: str, mapping: dict[str, str]) -> str:
    for key, value in mapping.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def iter_template_files(src: Path):
    for path in sorted(src.rglob("*")):
        if path.is_file():
            yield path


def plan(src: Path, dest: Path, mapping: dict[str, str]) -> list[dict[str, str]]:
    files = []
    for path in iter_template_files(src):
        rel = path.relative_to(src)
        files.append(
            {
                "from": str(path),
                "to": str(dest / rel),
                "rel": str(rel).replace("\\", "/"),
            }
        )
    for readme_name in ("README.md", "README.en.md"):
        readme_src = TEMPLATES / readme_name
        files.append(
            {
                "from": str(readme_src),
                "to": str(dest / readme_name),
                "rel": readme_name,
            }
        )
    return files


def write_files(items: list[dict[str, str]], mapping: dict[str, str], dest: Path) -> list[str]:
    written = []
    dest.mkdir(parents=True, exist_ok=True)
    for item in items:
        src = Path(item["from"])
        target = Path(item["to"])
        target.parent.mkdir(parents=True, exist_ok=True)
        text = render(src.read_text(encoding="utf-8"), mapping)
        if target.exists():
            raise FileExistsError(target)
        target.write_text(text, encoding="utf-8", newline="\n")
        written.append(item["rel"])
    return written


def next_steps(lang: str, transport: str, dest: Path) -> list[str]:
    if lang == "typescript":
        steps = [
            f"cd {dest}",
            "npm install",
            "npm run inspector" if transport == "stdio" else "npm run build && npm start  # then npm run inspector in another terminal",
        ]
    else:
        steps = [
            f"cd {dest}",
            "uv sync",
            "uv run mcp dev server.py"
            if transport == "stdio"
            else "uv run mcp run server.py --transport streamable-http",
        ]
    steps.append(f"python {SKILL_ROOT / 'scripts' / 'check-server.py'} --path {dest} --json")
    return steps


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Scaffold a minimal MCP server (TypeScript or Python, stdio or HTTP)."
    )
    parser.add_argument("--name", required=True, help="kebab-case server name, e.g. notes")
    parser.add_argument("--lang", choices=LANGS, default="typescript")
    parser.add_argument("--transport", choices=TRANSPORTS, default="stdio")
    parser.add_argument("--out", required=True, help="Absolute output directory (created if missing)")
    parser.add_argument("--dry-run", action="store_true", help="Print the plan; do not write files")
    parser.add_argument("--json", action="store_true", help="JSON on stdout")
    parser.add_argument("--force", action="store_true", help="Allow non-empty destination (still refuses overwrites)")
    args = parser.parse_args(argv)

    json_mode = args.json
    name = args.name.strip().lower()
    if not NAME_RE.match(name):
        fail(2, "--name must be kebab-case [a-z0-9][a-z0-9-]*[a-z0-9]", json_mode=json_mode)

    if args.lang == "python" and args.transport == "http":
        fail(
            2,
            "Python HTTP is not a separate template; scaffold --lang python --transport stdio then run: uv run mcp run server.py --transport streamable-http",
            json_mode=json_mode,
        )

    key = f"{args.lang}-{args.transport}"
    src = TEMPLATES / key
    if not src.is_dir():
        fail(2, f"missing template: {src}", json_mode=json_mode)

    dest = Path(args.out).expanduser()
    if not dest.is_absolute():
        fail(2, "--out must be an absolute path", json_mode=json_mode)
    if dest.exists() and any(dest.iterdir()) and not args.force and not args.dry_run:
        fail(3, f"destination is not empty: {dest} (pass --force to write alongside)", json_mode=json_mode)

    mapping = {
        "SERVER_NAME": name,
        "PACKAGE_NAME": to_package(name),
        "BIN_NAME": to_package(name),
    }
    items = plan(src, dest, mapping)

    if args.dry_run:
        payload = {
            "ok": True,
            "dry_run": True,
            "lang": args.lang,
            "transport": args.transport,
            "out": str(dest),
            "files": [i["rel"] for i in items],
            "next": next_steps(args.lang, args.transport, dest),
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False) if json_mode else json.dumps(payload, indent=2))
        return 0

    try:
        written = write_files(items, mapping, dest)
    except FileExistsError as exc:
        fail(4, f"refusing to overwrite existing file: {exc}", json_mode=json_mode)

    payload = {
        "ok": True,
        "dry_run": False,
        "lang": args.lang,
        "transport": args.transport,
        "out": str(dest),
        "files": written,
        "next": next_steps(args.lang, args.transport, dest),
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False) if json_mode else json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
