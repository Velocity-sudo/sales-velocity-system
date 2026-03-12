# Multi-Agent Routing & Architecture

## Concept

An "agent" in OpenClaw is an isolated brain with its own:
- `agentId` (unique name)
- `agentDir` (state: auth, models, sessions at `~/.openclaw/agents/<agentId>/`)
- `workspace` (knowledge files: AGENTS.md, SOUL.md, etc.)
- Session store (`~/.openclaw/agents/<agentId>/sessions/`)
- Model configuration (can use different LLMs)
- Tool permissions (can have different access levels)

A single Gateway manages all agents.

## Routing Logic

Inbound messages are matched top-down by **most-specific wins**:

```
1. Peer Match       → specific user ID or group ID
2. Guild/Team ID    → Discord guild / Slack team
3. Account ID       → specific channel account (e.g. "Business WhatsApp")
4. Channel Match    → all traffic from a channel type
5. Default          → falls to "main" agent
```

## Configuration Example

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
        "model": "claude-sonnet-4-20250514",
        "heartbeat": {
          "model": "gemini-2.0-flash",
          "interval": "15m"
        }
      },
      {
        "agentId": "family",
        "workspace": "~/.openclaw/agents/family/workspace",
        "model": "gemini-2.0-flash"
      }
    ]
  },
  "bindings": [
    {
      "agentId": "work",
      "channel": "telegram",
      "peer": "WORK_GROUP_CHAT_ID"
    },
    {
      "agentId": "family",
      "channel": "whatsapp",
      "peer": "FAMILY_GROUP_ID"
    },
    {
      "agentId": "personal",
      "channel": "telegram"
    }
  ]
}
```

## Design Patterns

### 1. Role-Based Agents
- **Personal**: Casual tone, personal memory, all tools
- **Work**: Professional, CRM access, email integration
- **Family**: Friendly, limited tools, safe content

### 2. Model-Tiered Agents
- **Deep work agent**: Claude Opus for analysis and writing
- **Chat agent**: Claude Sonnet for daily interaction
- **Utility agent**: Gemini Flash for simple tasks (cheaper)

### 3. Channel-Dedicated Agents
- Telegram → one agent
- Discord → different agent
- WhatsApp → yet another agent

## Isolation Guarantees

- Sessions are completely isolated between agents
- Memory files (MEMORY.md) are per-agent workspace
- One agent **cannot** access another's sessions or files
- Heartbeat runs independently per agent
- Compaction is independent per agent

## Common Pitfalls

- Forgetting to create workspace directories for new agents
- Not setting unique `agentId` (collisions cause undefined behavior)
- Binding too broadly (channel-level) when peer-level is needed
- Running too many agents with expensive models (cost explosion)
- Not monitoring per-agent token usage separately
