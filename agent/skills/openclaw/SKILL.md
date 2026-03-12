---
name: managing-openclaw
description: Comprehensive OpenClaw management, configuration, optimization, and troubleshooting. Use when the user asks about openclaw.json configuration, token cost reduction, agent workspace setup, multi-agent routing, session management, compaction, heartbeat/cron setup, MCP integration, skill creation, security hardening, model routing, deployment, or any OpenClaw infrastructure topic.
---

# OpenClaw Mastery Skill

> **Knowledge Source:** NotebookLM notebook `1aadcef0-21d5-4834-8f96-3feda72b56d0` (45 sources)

## Architecture Overview

OpenClaw is an open-source, self-hosted AI agent framework. Core components:

| Component | Purpose |
|---|---|
| **Gateway** | Server process managing channels, sessions, routing |
| **Agents** | Isolated "brains" with workspace, memory, permissions |
| **Channels** | Telegram, WhatsApp, Discord, Slack connectors |
| **Workspace** | File-based identity + memory (`~/.openclaw/workspace/`) |
| **Skills** | Modular capabilities via `SKILL.md` + resources |
| **MCP** | Model Context Protocol for external tool integration |

## Workspace File System

Files loaded into LLM context at session start:

| File | Purpose | When Loaded |
|---|---|---|
| `AGENTS.md` | Core rules, directives, boundaries | Always (system prompt) |
| `SOUL.md` | Personality, tone, backstory | Always |
| `USER.md` | User profile, preferences, timezone | Always |
| `IDENTITY.md` | Agent name, role (multi-agent differentiation) | Always |
| `TOOLS.md` | Available tools, API references | Always |
| `HEARTBEAT.md` | Periodic checklist tasks | Every heartbeat (~30m) |
| `MEMORY.md` | Persistent long-term memory | On demand |

**CRITICAL**: These files consume tokens on every turn. Keep them concise.

## Key Operations

### Token Optimization (up to 97% savings)

See [references/token-optimization.md](references/token-optimization.md) for full strategies.

Quick wins:
1. **Model tiering** — Gemini Flash for heartbeats (60x cheaper than Opus)
2. **Session resets** — `/new` or `/reset` after tasks (saves 40-60%)
3. **Compact proactively** — `/compact` when sessions grow long
4. **Minimize workspace files** — bloated AGENTS.md bleeds money every turn
5. **Prompt caching** — sync heartbeat interval < cache TTL (saves 30-50%)
6. **Local fallbacks** — Ollama for simple tasks (free)

### Configuration (openclaw.json)

See [references/configuration.md](references/configuration.md) for full guide.

Key structure:
```
openclaw.json
├── gateway (port, auth, bind, tailscale)
├── channels (telegram, whatsapp, discord)
├── agents
│   ├── defaults (model, sandbox, tools, compaction, heartbeat)
│   └── list (agent overrides)
├── bindings (multi-agent routing rules)
├── models/providers (API keys, local models)
└── security (sandbox, skills)
```

### Multi-Agent Routing

See [references/multi-agent.md](references/multi-agent.md) for full guide.

Routing priority (most-specific wins):
1. Peer match (specific user/group ID)
2. Guild/Team ID
3. Account ID
4. Channel match
5. Default (`main` agent)

### Session & Compaction

- **Session lifecycle**: `sessionKey` → `sessionId` → `.jsonl` transcript
- **Compaction mode**: `"safeguard"` recommended
- **Memory flush**: Enable to save state before compaction
- **Idle reset**: `session.idleMinutes: 60` auto-resets stale sessions
- **Manual commands**: `/compact`, `/reset`, `/new`

### Heartbeat vs Cron

| | Heartbeat | Cron |
|---|---|---|
| **Runs in** | Main session (shared context) | Isolated session |
| **Schedule** | Interval (e.g., `30m`) | Cron expression (e.g., `0 9 * * 1`) |
| **Context** | Full awareness of recent chat | No user context |
| **Cost** | Adds to main session tokens | Separate cost |
| **Best for** | Monitoring, check-ins | Scheduled reports, backups |

### Security (3-Tier Model)

See [references/security.md](references/security.md) for full hardening guide.

| Tier | Focus | Key Actions |
|---|---|---|
| **1: Basic** | Isolation | Bind loopback, dmPolicy: pairing, firewall |
| **2: Standard** | Access control | Tool allowlisting, MCP version pinning, OAuth scoping |
| **3: Advanced** | Defense-in-depth | Docker sandbox, egress proxy, credential brokering |

### Deployment Options

| Option | Cost | Security | Best For |
|---|---|---|---|
| **Local (Mac/PC)** | Free | Low | Testing, personal use |
| **VPS (Hetzner/DO)** | ~$4-6/mo | High | Production |
| **Docker** | Variable | High | Isolation-critical setups |
| **Cloudflare Workers** | Low | Medium | Serverless/ephemeral |

### MCP Integration

Configure MCP servers in `mcp.json` or `openclaw.json`:
- **Always** pin server versions (`autoUpdate: false`)
- **Never** enable `enableAllProjectMcpServers: true`
- Disable `filesystem` and `shell` servers unless needed
- OpenClaw can also act AS an MCP server for other clients

### Skills System

- Skills live in `~/.openclaw/skills/` or workspace
- Install from ClawHub: `openclaw skills install <name>`
- **WARNING**: ~15% of community skills may be malicious — always review
- Skills run with agent's full privileges

## Troubleshooting

See [references/troubleshooting.md](references/troubleshooting.md) for full guide.

### ⚠️ Critical: Three Key Files (Most Common Issue)

```
.env                    → Skills read API keys from here (NOTION_API_KEY, etc.)
openclaw.json           → Config structure (models, channels, skill entries)
auth-profiles.json      → ACTUAL provider keys the gateway uses
```

**All three must be correct and consistent.** The #1 failure mode is keys being wrong in `auth-profiles.json` (`~/.openclaw/agents/main/agent/auth-profiles.json`). The wizard can accidentally assign the wrong key to a provider profile.

### Quick Diagnosis

| Symptom | Root Cause | Fix |
|---|---|---|
| Skill "not available" | Wrong key in `.env` or provider in cooldown | Check `.env`, clear cooldown in `auth-profiles.json` |
| Model falls back silently | Provider cooldown from auth errors | Check `openclaw doctor` for cooldown, fix `auth-profiles.json` |
| Tool called but does nothing (7ms) | Env var missing or invalid | Verify key with `curl`, update `.env` |
| `errorCount: 30` in auth-profiles | Wrong API key for that provider | Fix key, clear `usageStats`, restart |
| High costs | Heartbeat on expensive model | Set `heartbeat.model` to `gemini-2.0-flash` |
| Token overflow | Long sessions | `/compact`, `/reset`, trim AGENTS.md |
| Gateway won't start | Port conflict or bad config | `lsof -ti:3000`, validate JSON |

### Recovery Steps
```bash
# 1. Diagnose
openclaw doctor

# 2. If cooldown showing → edit auth-profiles.json:
#    Fix wrong keys, set errorCount:0, remove cooldownUntil

# 3. Restart
openclaw gateway restart

# 4. Tell the agent
/reset
```
