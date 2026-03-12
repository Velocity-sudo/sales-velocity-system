# Token Optimization Guide

## Why OpenClaw Burns Tokens

1. **System prompt bloat** — AGENTS.md/SOUL.md/USER.md load every turn
2. **Full conversation context** — entire session history replayed each turn
3. **Tool round-trips** — each tool call = full context + results
4. **Heartbeat overhead** — runs every 30m with full context
5. **Compaction failures** — sessions grow unbounded without proper config
6. **MCP tool descriptions** — each enabled MCP adds to system prompt

## Strategy Matrix (by savings)

| Strategy | Savings | Effort | Risk |
|---|---|---|---|
| Session resets (`/reset`, `/new`) | 40-60% | Low | Context loss |
| Model tiering (Flash for heartbeats) | 60-80% | Low | Quality variance |
| Prompt caching (sync heartbeat < TTL) | 30-50% | Medium | Config complexity |
| Workspace file pruning | 20-40% | Medium | Info loss |
| Local model fallback (Ollama) | 90%+ | Medium | Latency, quality |
| Output isolation (separate sessions) | 30-50% | Low | Routing complexity |
| Batched heartbeat tasks | 30-40% | Low | None |
| LiteLLM proxy routing | Variable | High | Infra overhead |

## Implementation Details

### 1. Model Tiering
```json
// openclaw.json — agent model config
{
  "agents": {
    "defaults": {
      "model": "claude-sonnet-4-20250514" // daily chat
    },
    "list": [
      {
        "agentId": "main",
        "heartbeat": {
          "model": "gemini-flash" // 60x cheaper
        }
      }
    ]
  }
}
```

### 2. Session Hygiene
- After any major task → `/compact` or `/reset`
- Set `session.idleMinutes: 60` to auto-reset
- Enable `compaction.mode: "safeguard"` for auto-compaction
- Enable `memoryFlush: true` to save state before compaction

### 3. Workspace File Optimization
- AGENTS.md: Keep under 1500 words (target: 500-800)
- Remove duplicate instructions across files
- Move rarely-used references to skills instead of workspace
- Use `#` sections so agent skims instead of re-reading

### 4. Heartbeat Optimization
- Use cheaper model for heartbeat (Gemini Flash / Haiku)
- Batch checklist items in HEARTBEAT.md to reduce turns
- Align heartbeat interval to cache TTL (e.g., 25min interval, 5min cache)
- Skip heartbeat if no pending tasks

### 5. Output Isolation
- Long reports → separate session (`cron:report-123`)
- Prevents output tokens from bloating main session
- Configure with cron jobs rather than inline requests

### 6. Local Model Fallbacks
```json
// openclaw.json — Ollama fallback
{
  "models": {
    "providers": {
      "ollama": {
        "baseUrl": "http://localhost:11434",
        "models": ["llama3:8b"]
      }
    }
  }
}
```
Use for: simple queries, file operations, formatting tasks.

## Cost Monitoring

- Check `contextTokens` in session metadata
- Review API provider dashboards weekly
- Set budget alerts on Anthropic/OpenAI/Google consoles
- Track cost per agent if running multi-agent
