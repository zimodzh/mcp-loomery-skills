# Host config (Cursor / Claude Desktop)

Source: official *Connect to local MCP servers* and Debugging. Field names differ slightly by product; the meaning is the same: `command` + `args` + optional `env`.

Always use **absolute paths**. When a host launches stdio, cwd may be `/` or undefined.

## Cursor

Project: `.cursor/mcp.json`  
User: `~/.cursor/mcp.json` (Windows: `%USERPROFILE%\.cursor\mcp.json`)

```json
{
  "mcpServers": {
    "notes": {
      "command": "node",
      "args": ["C:/abs/path/to/notes/dist/index.js"]
    }
  }
}
```

Python:

```json
{
  "mcpServers": {
    "notes": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/abs/path/to/notes",
        "run",
        "mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

Remote:

```json
{
  "mcpServers": {
    "notes-remote": {
      "url": "https://api.example.com/mcp"
    }
  }
}
```

Follow the current Cursor docs: some builds use `url`, others `streamableHttp`. Mirror an existing entry in the user’s `mcp.json` when in doubt.

## Claude Desktop

- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

The official TypeScript weather tutorial points at `build/index.js`. npx wrapper:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "C:\\Users\\me\\Desktop"]
    }
  }
}
```

## env

stdio does **not** inherit the full user environment. Put API keys in `env`. If Windows logs show a literal `${APPDATA}`, write the expanded path into `env.APPDATA`.

## After editing config

Fully quit the app and start it again. For Claude, closing the window is not enough. Once connected, the Connectors / MCP panel should show the server name and tools. If it fails, reproduce without the host using [inspector.md](inspector.md).
