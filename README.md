# 🚀 Sales Velocity System

Sistema centralizado de configuración para el agente Antigravity.

## ¿Qué contiene?

| Componente | Descripción |
|---|---|
| `agent/skills/` | 39+ carpetas de skills especializados |
| `agent/workflows/` | 27 workflows (`/comandos`) |
| `agent/SOUL.md` | Identidad y propósito del agente |
| `gemini/GEMINI.md` | Regla global del sistema (303 líneas) |
| `gemini/antigravity/mcp_config.json` | Servidores MCP (Notion, NotebookLM, Firecrawl) |
| `clientes/LuchoBranding/config/` | Credenciales API (Meta, GHL, SMTP) |
| `clientes/LuchoBranding/scripts/` | Scripts de automatización |

## Instalación

```bash
git clone git@github.com:Velocity-sudo/sales-velocity-system.git
cd sales-velocity-system
chmod +x install.sh
./install.sh
```

## Sincronización

Después de hacer cambios en cualquier máquina:

```bash
# Máquina donde hiciste cambios:
git add . && git commit -m "update: descripción" && git push

# Otra máquina:
git pull && ./install.sh
```

## ⚠️ Seguridad

Este repo es **PRIVADO**. Contiene API keys y tokens. **Nunca hacerlo público.**

## Estructura de destino

```
~/.agent/
├── SOUL.md
├── skills/          ← 39+ carpetas
└── workflows/       ← 27 workflows (copia 1/3)

~/.gemini/
├── GEMINI.md        ← Regla global
├── workflows/       ← 27 workflows (copia 2/3)
└── antigravity/
    ├── mcp_config.json
    └── global_workflows/  ← 27 workflows (copia 3/3)

~/Desktop/Clientes/LuchoBranding/
├── config/clients_config.json
└── scripts/
```
