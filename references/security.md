# Security (server authors)

Source: Specification *Security and Trust & Safety* plus official Security Best Practices. Only MUST/MUST NOT items that server authors commonly get wrong. Open the full OAuth-proxy write-up when the user explicitly wants authorization.

## Principles

1. User consent and control: destructive tools SHOULD be visible and deniable in the host.
2. Data minimization: do not log raw tool arguments.
3. Tool descriptions and annotations are **untrusted** (prompt injection from an untrusted server). When you author your own server: describe real behavior only; do not hide extra instructions.
4. Validate all inputs; rate-limit; sanitize outputs (especially text that will be fed back to a model).

## Filesystem and URLs

- Paths: after resolve, they MUST remain inside the allowed root. Reject `..`, encoding tricks, and escaping symlinks.
- Tools that take a URL and fetch it: constrain scheme/host against SSRF. Default-deny link-local `169.254.169.254` and private networks unless the product is intentionally internal and the user knows that.

## Cross-call handles

The protocol has no session object. Strings like `basket_id`:

- **MUST NOT** treat possession of the handle as authorization. Re-check the caller’s identity every call.
- On an unauthenticated server the handle is a bearer token: high entropy (UUIDv4) + short TTL.
- Opaque. Do not encode internal paths.
- On expiry, return a **tool execution error** (`isError: true`) so the model can create a new one.

## OAuth / remote servers

- **MUST NOT** token-passthrough: accept only tokens **issued to this MCP server** (audience), then mint your own downstream credentials.
- MCP proxies that use a static third-party `client_id` MUST collect **per-MCP-client consent** before forwarding to the third party; exact `redirect_uri` match; write `state` only **after** the user consents; one-time, short TTL.
- Localhost HTTP: validate the Host header (DNS rebinding).
- Opening authorization URLs: do not shell out through `cmd.exe` / `sh` / PowerShell (injection). Use OS URL APIs.

## stdio used as a proxy

A stdio server runs as the user. Do not interpolate model-supplied strings into a shell. Execute external programs with an argument vector and a whitelist of binaries.

## While debugging

Redact tokens, cookies, emails, and sensitive path segments from logs.
