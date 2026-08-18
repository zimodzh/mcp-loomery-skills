"""{{SERVER_NAME}} MCP server."""

from __future__ import annotations

import logging
import sys

from mcp.server import MCPServer

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logger = logging.getLogger(__name__)

mcp = MCPServer("{{SERVER_NAME}}")


@mcp.tool()
def ping(message: str | None = None) -> dict[str, object]:
    """Return pong plus an optional message. Use to verify the MCP server is running."""
    echo = message or "pong"
    logger.info("ping echo=%s", echo)
    return {"ok": True, "echo": echo}


@mcp.resource("about://server")
def about() -> str:
    """Static server identity."""
    return "{{SERVER_NAME}} MCP server"
