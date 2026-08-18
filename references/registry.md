# Publishing to the official MCP Registry

Source: Registry Quickstart / package types. The Registry is still **preview** — breaking changes or data resets may happen. Do this section only when the user asks to publish.

Prerequisites: Inspector-stable list/call, README with the launch command, a decided version.

## server.json

- `$schema`: current official schema URL (see Registry docs; example `https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json`).
- `name`: reverse-DNS, e.g. `io.github.username/email-integration-mcp`.
- `packages[]`: `registryType` + `identifier` + `version` + `transport`.

## Package types and ownership proof

| registryType | Identifier | Proof |
| --- | --- | --- |
| `npm` | npm package name | `package.json` `mcpName` **MUST** equal `server.json` `name` |
| `pypi` | PyPI project name | README contains `mcp-name: io.github...` (may be an HTML comment) |
| `nuget` | NuGet id | README `mcp-name:` the same way |
| `oci` | `registry/ns/repo:tag` | Docker LABEL `io.modelcontextprotocol.server.name` |
| `mcpb` | GitHub/GitLab release URL | URL contains `mcp`; `fileSha256` required (clients verify) |

npm is `registry.npmjs.org` only; PyPI is pypi.org only. OCI: docker.io / ghcr.io / `*.pkg.dev` / `*.azurecr.io` / mcr.microsoft.com.

## Remote servers

Remote packages use the HTTP transport description (*Publishing Remote Servers*). Do not put local absolute paths in the registry.

## Auth and automation

Publishing auth, GitHub Actions, and versioning follow the official Registry pages (Quickstart, authentication, GitHub Actions, versioning). Do not put registry tokens in this skill repo or in example `env`.
