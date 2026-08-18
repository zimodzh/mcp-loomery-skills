# Python SDK v2

Source: official Python SDK README and Get started. `pip install mcp` **now installs 2.x**.

## Install

```bash
uv add "mcp[cli]"          # recommended; includes mcp dev / mcp run / mcp install
# or: pip install "mcp[cli]"
```

Requires Python **3.10+**. Unmigrated v1 must pin `mcp>=1.28,<2`. v1 `FastMCP` is not the default for new projects.

Docs: [https://py.sdk.modelcontextprotocol.io/](https://py.sdk.modelcontextprotocol.io/) (Get started, What’s new in v2, migration).

## Minimal server

The instance MUST be importable as `from server import mcp` (CLI and tests look for that object):

```python
from mcp.server import MCPServer

mcp = MCPServer("Demo")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers."""
    return a + b

@mcp.resource("greeting://{name}")
def greeting(name: str) -> str:
    """Greet someone by name."""
    return f"Hello, {name}!"
```

Type hints are the input schema; the docstring is the description. Do not hand-write JSON Schema unless the current SDK API requires it.

stdio logging:

```python
import logging
import sys

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)
```

Ban bare `print()` and `print(..., file=sys.stdout)` (both break stdio framing). `print(..., file=sys.stderr)` is allowed.

## Run and test

| Goal | Command |
| --- | --- |
| Inspector | `uv run mcp dev server.py` |
| stdio | `uv run mcp run server.py` |
| HTTP | `uv run mcp run server.py --transport streamable-http` |

In-process tests (official recommendation, no port):

```python
import pytest
from mcp import Client
from server import mcp

@pytest.mark.anyio
async def test_add() -> None:
    async with Client(mcp) as client:
        result = await client.call_tool("add", {"a": 1, "b": 2})
        assert result.structured_content == {"result": 3}
```

`Client("http://localhost:8000/mcp")` means Streamable HTTP; the client can also spawn a stdio subprocess. Structured HTTP tool results live in `result.structured_content`.

## Migration signals

If you see these, follow the v2 docs. Do not extend v1:

- `from mcp.server.fastmcp import FastMCP`
- `FastMCP("name")`
- Hand-rolled `InitializationOptions` / low-level `Server` + `stdio_server` as a new-project template

When the user wants Python **and** already has a FastAPI app, open the SDK “Running your server” page and mount MCP on that app. Do not start a second conflicting port.
