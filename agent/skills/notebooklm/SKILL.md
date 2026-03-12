# NotebookLM MCP Skill

> **Version:** 1.0.0  
> **Status:** ✅ Installed & Configured  
> **Account:** marca@luchobranding.com

## Description

This skill enables Antigravity to interact with Google NotebookLM notebooks for AI-powered research and knowledge management.

## Quick Reference

### CLI Commands
```bash
# Login
/opt/homebrew/bin/nlm login

# List notebooks
/opt/homebrew/bin/nlm notebook list

# Get notebook info
/opt/homebrew/bin/nlm notebook get <notebook_id>

# Chat with a notebook
/opt/homebrew/bin/nlm note chat <notebook_id> "your question"
```

### MCP Configuration
Located at: `~/.gemini/antigravity/mcp_config.json`

```json
"notebooklm-mcp": {
  "command": "/opt/homebrew/bin/notebooklm-mcp",
  "args": []
}
```

## Available Notebooks

| ID | Title | Sources |
|----|-------|---------|
| `2d74d19b-212c-4c4c-8674-59fae29e0392` | OpenClaw Installation Guide | 0 |
| `9249629c-e770-440a-a384-7c20b3928319` | Agency OS Video Analysis | 1 |
| `177c8595-825f-4635-b58c-c9ab2710edfb` | Meta Ads 2026 - Tema 4: Estructura Simplificada | 32 |
| `aed33ea7-a95e-4cc9-a1b4-dd8d696251d1` | Meta Ads 2026 - Tema 2: Dominio del Video Vertical | 37 |
| `61b88789-b714-48e7-a3f3-d7c498bca6ba` | Meta Ads 2026 - Tema 1: Creatividad como Segmentación | 26 |
| `d68bf0e6-223f-4864-bd5f-85c1d6c9f798` | Meta Ads 2026 - Tema 5: Automatización e IA | 41 |
| `bf75f1ac-fc3b-4225-bafe-99da5d97b65b` | Meta Ads 2026 - Tema 3: Infraestructura de Datos | 33 |
| `d3f62218-67d5-45d9-8fc2-9de7aca208f1` | EstrategIA de Negocio | 8 |
| `dbfca223-d041-4397-a77f-c6578c44d0ea` | Marca | 1 |
| `247972a7-19b9-4640-a9b5-b5297adbafaf` | Brand Director Knowledge Base | 53 |

## Use Cases for Sales Velocity Agents

1. **Knowledge Brain:** Use notebooks as the knowledge base for agents
2. **Research Synthesis:** Query notebooks about specific topics
3. **Content Generation:** Ask notebooks to help generate insights

## Authentication

Credentials stored at: `~/.notebooklm-mcp-cli/profiles/default`

To re-authenticate:
```bash
rm -rf ~/.notebooklm-mcp-cli
/opt/homebrew/bin/nlm login
```
