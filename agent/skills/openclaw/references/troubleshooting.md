# OpenClaw Troubleshooting Guide

## Critical File Locations

| File | Purpose | Common Issues |
|---|---|---|
| `~/.openclaw/openclaw.json` | Main config | Model names, skill entries, gateway settings |
| `~/.openclaw/.env` | API keys (env vars) | **Skills read from here**, not from openclaw.json |
| `~/.openclaw/agents/main/agent/auth-profiles.json` | Actual keys used by gateway | **Wrong keys cause silent failures + cooldowns** |
| `~/.openclaw/agents/main/sessions/sessions.json` | Active sessions | Stale sessions may cache old state |

## ⚠️ The Auth-Profiles Trap (Critical)

`auth-profiles.json` stores the actual API keys the gateway uses per provider. It is **separate** from:
- `openclaw.json` (config structure, not keys)
- `.env` (env vars for skills)

### Symptoms of Wrong Key in auth-profiles.json
- Model responds but falls back to a different provider silently
- `openclaw doctor` shows `cooldown (XXm)` on a provider
- `errorCount: 30` and `failureCounts.auth` in the file
- Skills that depend on a model fail without clear error

### How to Fix
```bash
# 1. Check current state
cat ~/.openclaw/agents/main/agent/auth-profiles.json

# 2. Verify each key matches its provider:
#    - anthropic: starts with "sk-ant-api03-..."
#    - google: starts with "AIzaSy..."
#    - openai: starts with "sk-proj-..."

# 3. If wrong, edit the file directly — fix the key AND clear usageStats:
#    "errorCount": 0, remove "cooldownUntil", remove "disabledUntil"

# 4. Restart gateway
openclaw gateway restart
```

### Prevention
When running `openclaw doctor --fix` or wizard, **always verify** that the keys in `auth-profiles.json` match the correct provider. The wizard can accidentally assign the same key to multiple profiles.

## Skill Not Available (e.g., Notion)

### How OpenClaw Skills Work
- Skills are `SKILL.md` files with instructions (curl examples, CLI usage)
- Some skills register as **tools** (appear in `tool=notion` in logs)
- Skills with `requires.env` need the env var in `.env` to activate
- The `apiKey` in `openclaw.json → skills.entries.notion` is for config display; the **actual key** comes from `NOTION_API_KEY` in `.env`

### Debugging Checklist
```bash
# 1. Is the skill listed as ready?
openclaw skills list | grep notion
# Must show ✓ ready

# 2. Is the env var set correctly?
grep NOTION_API_KEY ~/.openclaw/.env
# Must have the correct, current key

# 3. Verify the key works directly
curl -s https://api.notion.com/v1/users/me \
  -H "Authorization: Bearer $(grep NOTION_API_KEY ~/.openclaw/.env | cut -d= -f2)" \
  -H "Notion-Version: 2022-06-28"
# Must return user object, not 401

# 4. Check if the tool is being called in logs
openclaw logs | grep "tool=notion"
# If start→end in <10ms with no error = key issue or skill not loading

# 5. Is the model in cooldown?
openclaw doctor | grep cooldown
# If yes → fix auth-profiles.json (see above)

# 6. Restart and reset
openclaw gateway restart
# Then tell Niko: /reset
```

### Key Insight: .env vs openclaw.json
```
.env (NOTION_API_KEY=xxx)          → Used by the skill runtime
openclaw.json (skills.entries.notion.apiKey) → Used by config display only
auth-profiles.json                  → Used by the LLM provider gateway
```
**All three must be correct and consistent.**

## Provider Cooldown

When a provider key fails repeatedly, OpenClaw puts it in cooldown:
- After ~5 auth failures → short cooldown (~5m)
- After ~30 failures → long cooldown (~60m)
- `disabledReason: "billing"` may appear even for auth errors

### Clear Cooldown Manually
Edit `~/.openclaw/agents/main/agent/auth-profiles.json`:
- Set `errorCount: 0`
- Remove `cooldownUntil`
- Remove `disabledUntil`
- Remove `failureCounts`

Then `openclaw gateway restart`.

## Model Not Working

### Quick Test
```bash
# Test Anthropic
curl -s https://api.anthropic.com/v1/messages \
  -H "x-api-key: YOUR_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-sonnet-4-20250514","max_tokens":10,"messages":[{"role":"user","content":"hi"}]}'

# Test Google
curl -s "https://generativelanguage.googleapis.com/v1beta/models?key=YOUR_KEY" | head -5

# Test OpenAI
curl -s https://api.openai.com/v1/chat/completions \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gpt-4o","messages":[{"role":"user","content":"hi"}],"max_tokens":10}'
```

## Gateway Won't Start
```bash
# Check if already running
lsof -ti:3000
# Kill if needed
kill -9 $(lsof -ti:3000)
# Restart
openclaw gateway restart
# Check logs
openclaw logs | tail -20
```

## Notion-Specific Tips

- Database IDs can be extracted from Notion URLs
- The integration must be **connected** to each database via Share → Connections
- `Notion-Version: 2025-09-03` uses "data_sources" instead of "databases" for queries
- Rate limit: ~3 requests/second
