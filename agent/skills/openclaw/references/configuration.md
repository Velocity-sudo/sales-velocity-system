# openclaw.json Configuration Reference

## Full Structure Map

```
openclaw.json
├── gateway
│   ├── port (default: 3000)
│   ├── bind (default: "127.0.0.1" — NEVER "0.0.0.0")
│   ├── auth (Bearer token for API access)
│   └── tailscale (mesh VPN integration)
│
├── channels
│   ├── telegram
│   │   ├── token (Bot token from BotFather)
│   │   ├── dmPolicy ("pairing" | "allowlist" | "open")
│   │   └── pollingMode ("long-poll" | "webhook")
│   ├── whatsapp (via bridge or Baileys)
│   ├── discord (bot token + guild IDs)
│   └── slack (app token + workspace)
│
├── agents
│   ├── defaults
│   │   ├── model (default LLM for all agents)
│   │   ├── sandbox (file system permissions)
│   │   ├── tools (allowed/denied tool lists)
│   │   ├── compaction
│   │   │   ├── mode ("safeguard" | "manual" | "disabled")
│   │   │   ├── memoryFlush (bool — save state pre-compact)
│   │   │   └── contextTokens (max before auto-compact)
│   │   └── heartbeat
│   │       ├── interval ("30m")
│   │       ├── model (cheaper model for heartbeats)
│   │       └── checklist (path to HEARTBEAT.md)
│   └── list[]
│       ├── agentId (unique identifier)
│       ├── agentDir (state/auth directory)
│       ├── workspace (files directory)
│       ├── model (override default)
│       └── ... (any defaults override)
│
├── bindings[]
│   ├── agentId (which agent handles this)
│   ├── channel (telegram | whatsapp | discord)
│   ├── account (specific channel account)
│   ├── peer (user or group ID)
│   └── guild (Discord guild / Slack team)
│
├── models
│   └── providers
│       ├── anthropic (apiKey, models[])
│       ├── openai (apiKey, models[])
│       ├── google (apiKey, models[])
│       ├── ollama (baseUrl, models[])
│       └── litellm (baseUrl, apiKey)
│
├── security
│   ├── sandbox
│   │   ├── allowedPaths[]
│   │   ├── deniedPaths[]
│   │   └── readOnlyPaths[]
│   └── skills
│       ├── allowedSources[] (clawhub, local, git)
│       └── autoUpdate (bool)
│
└── mcp
    ├── enableAllProjectMcpServers (NEVER true)
    └── servers{}
        └── <serverName>
            ├── command
            ├── args[]
            ├── env{}
            ├── version
            └── autoUpdate (false recommended)
```

## Common Configurations

### Minimal Production Config
```json
{
  "gateway": {
    "port": 3000,
    "bind": "127.0.0.1"
  },
  "channels": {
    "telegram": {
      "token": "BOT_TOKEN",
      "dmPolicy": "pairing"
    }
  },
  "agents": {
    "defaults": {
      "model": "claude-sonnet-4-20250514",
      "compaction": {
        "mode": "safeguard",
        "memoryFlush": true
      }
    }
  },
  "models": {
    "providers": {
      "anthropic": {
        "apiKey": "sk-ant-..."
      }
    }
  }
}
```

### Multi-Agent Setup
```json
{
  "agents": {
    "list": [
      {
        "agentId": "personal",
        "workspace": "~/.openclaw/agents/personal/workspace",
        "model": "claude-sonnet-4-20250514"
      },
      {
        "agentId": "work",
        "workspace": "~/.openclaw/agents/work/workspace",
        "model": "claude-sonnet-4-20250514"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "work",
      "channel": "telegram",
      "peer": "GROUP_ID_WORK"
    },
    {
      "agentId": "personal",
      "channel": "telegram"
    }
  ]
}
```

### Cost-Optimized Config
```json
{
  "agents": {
    "defaults": {
      "model": "claude-sonnet-4-20250514",
      "heartbeat": {
        "interval": "30m",
        "model": "gemini-2.0-flash"
      },
      "compaction": {
        "mode": "safeguard",
        "memoryFlush": true,
        "contextTokens": 50000
      },
      "session": {
        "idleMinutes": 60
      }
    }
  }
}
```

## Critical Do's and Don'ts

### ✅ DO
- Bind to `127.0.0.1` (loopback only)
- Set `dmPolicy: "pairing"` or `"allowlist"`
- Pin MCP server versions
- Enable `memoryFlush: true`
- Use `compaction.mode: "safeguard"`
- Use model tiering for heartbeat vs chat

### ❌ DON'T
- Set `bind: "0.0.0.0"` (exposes to public internet)
- Use `dmPolicy: "open"` (anyone can talk to your agent)
- Set `enableAllProjectMcpServers: true`
- Leave `autoUpdate: true` on MCP servers
- Store API keys directly in openclaw.json (use env vars)
