#!/usr/bin/env python3
"""Static checks for an MCP server tree. Never interactive.

Exit codes: 0 clean (warnings allowed), 1 usage, 2 findings with severity=error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

SKIP_DIRS = {
    "node_modules",
    ".git",
    "dist",
    "build",
    ".venv",
    "venv",
    "__pycache__",
    ".cursor",
}

TOOL_NAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")

CONSOLE_LOG = re.compile(r"\bconsole\.log\s*\(")
PRINT_CALL = re.compile(r"(?m)^\s*print\s*\(")
PRINT_STDERR = re.compile(r"file\s*=\s*sys\.stderr")
FASTMCP = re.compile(r"FastMCP|mcp\.server\.fastmcp")
LEGACY_TS_SDK = re.compile(r"from ['\"]@modelcontextprotocol/sdk['\"]|require\(['\"]@modelcontextprotocol/sdk['\"]\)")
STDIO_CONNECT = re.compile(r"new\s+StdioServerTransport\s*\(")
SAMPLING = re.compile(r"requestSampling|sampling/createMessage")
PROTOCOL_LOG = re.compile(r"sendLoggingMessage|notifications/message")
LIST_ROOTS = re.compile(r"\blistRoots\s*\(")
CREATE_HANDLER = re.compile(r"createMcpHandler\s*\(")
REGISTER_OUTSIDE_HINT = re.compile(r"register(Tool|Resource|Prompt)\s*\(")
SERVE_STDIO = re.compile(r"serveStdio\s*\(")
REGISTER_TOOL_NAME = re.compile(r"registerTool\s*\(\s*['\"]([^'\"]+)['\"]")
PY_TOOL_DEF = re.compile(r"@mcp\.tool\(\)\s*\n(?:async\s+)?def\s+([^\s(:]+)", re.M)
PY_TOOL_STR = re.compile(r"@mcp\.tool\(\s*(?:name\s*=\s*)?['\"]([^'\"]+)['\"]")


def iter_source_files(root: Path):
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in {".ts", ".js", ".mjs", ".cts", ".mts", ".py"}:
            yield path


def add(findings: list[dict], path: Path, line: int, severity: str, code: str, message: str) -> None:
    findings.append(
        {
            "file": str(path),
            "line": line,
            "severity": severity,
            "code": code,
            "message": message,
        }
    )


def check_file(path: Path, findings: list[dict]) -> None:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.splitlines()
    rel = path

    for i, line in enumerate(lines, 1):
        if CONSOLE_LOG.search(line) and not line.strip().startswith("//"):
            add(findings, rel, i, "error", "stdout-console-log", "stdio servers must not write console.log to stdout; use console.error")
        if path.suffix == ".py" and PRINT_CALL.search(line) and not line.lstrip().startswith("#") and not PRINT_STDERR.search(line):
            add(findings, rel, i, "error", "stdout-print", "print() goes to stdout and breaks stdio JSON-RPC; log to sys.stderr")
        if FASTMCP.search(line):
            add(findings, rel, i, "warning", "python-v1-fastmcp", "FastMCP is Python SDK v1; new servers should use MCPServer from mcp.server")
        if LEGACY_TS_SDK.search(line):
            add(findings, rel, i, "warning", "ts-v1-sdk", "@modelcontextprotocol/sdk is the v1 line; new servers should use @modelcontextprotocol/server")
        if STDIO_CONNECT.search(line) and not SERVE_STDIO.search(text):
            add(findings, rel, i, "warning", "stdio-legacy-connect", "StdioServerTransport+connect pins 2025-era wire; prefer serveStdio(factory) for 2026-07-28")
        if SAMPLING.search(line):
            add(findings, rel, i, "warning", "deprecated-sampling", "Sampling is deprecated in 2026-07-28; call an LLM provider API from the server")
        if PROTOCOL_LOG.search(line):
            add(findings, rel, i, "warning", "deprecated-logging", "Protocol logging is deprecated; use stderr or OpenTelemetry")
        if LIST_ROOTS.search(line):
            add(findings, rel, i, "warning", "deprecated-roots", "Roots are deprecated; pass paths via tool args, resource URIs, or config")

    for match in REGISTER_TOOL_NAME.finditer(text):
        name = match.group(1)
        if not TOOL_NAME_RE.match(name) or " " in name:
            add(findings, rel, 1, "error", "tool-name", f"invalid tool name {name!r}; use 1-128 chars of A-Za-z0-9_.-")

    if path.suffix == ".py":
        py_names: list[tuple[int, str]] = []
        for match in PY_TOOL_STR.finditer(text):
            py_names.append((text[: match.start()].count("\n") + 1, match.group(1)))
        for match in PY_TOOL_DEF.finditer(text):
            py_names.append((text[: match.start()].count("\n") + 1, match.group(1)))
        seen: set[tuple[int, str]] = set()
        for line_no, name in py_names:
            key = (line_no, name)
            if key in seen:
                continue
            seen.add(key)
            if not TOOL_NAME_RE.match(name) or " " in name:
                add(
                    findings,
                    rel,
                    line_no,
                    "error",
                    "tool-name",
                    f"invalid tool name {name!r}; use 1-128 chars of A-Za-z0-9_.-",
                )

    if CREATE_HANDLER.search(text):
        # Heuristic: register* at module level (column 0) while createMcpHandler exists.
        for i, line in enumerate(lines, 1):
            if REGISTER_OUTSIDE_HINT.search(line) and not line.startswith((" ", "\t")):
                add(
                    findings,
                    rel,
                    i,
                    "error",
                    "http-register-outside-factory",
                    "createMcpHandler runs a fresh instance per request; register tools inside the factory, not on a module-level server",
                )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Scan an MCP server tree for stdio, SDK, and protocol gotchas.")
    parser.add_argument("--path", required=True, help="Server directory or file")
    parser.add_argument("--json", action="store_true", help="JSON on stdout")
    parser.add_argument("--dry-run", action="store_true", help="List files that would be scanned")
    args = parser.parse_args(argv)

    root = Path(args.path).expanduser().resolve()
    if not root.exists():
        print(json.dumps({"ok": False, "error": f"path not found: {root}"}) if args.json else f"path not found: {root}", file=sys.stderr if not args.json else sys.stdout)
        return 1

    files = [root] if root.is_file() else list(iter_source_files(root))
    if args.dry_run:
        payload = {"ok": True, "dry_run": True, "files": [str(p) for p in files]}
        print(json.dumps(payload, indent=2, ensure_ascii=False))
        return 0

    findings: list[dict] = []
    for path in files:
        check_file(path, findings)

    errors = sum(1 for f in findings if f["severity"] == "error")
    warnings = sum(1 for f in findings if f["severity"] == "warning")
    payload = {
        "ok": errors == 0,
        "scanned": len(files),
        "errors": errors,
        "warnings": warnings,
        "findings": findings,
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    if not args.json:
        # JSON already printed as structured output (agent-friendly).
        pass
    return 2 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
