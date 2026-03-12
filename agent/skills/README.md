# 🚀 Agent Skills - Velocity Sudo

Backup global de todos los skills de AI para Antigravity/OpenCode y Claude Code.

## 📁 Estructura

```
agent-skills/
├── ads/                         # 🎯 Orchestrador Ads (6 plataformas, 190 checks)
│   └── references/              # 12 archivos de referencia (scoring, benchmarks, etc.)
├── ads-audit/                   # Auditoría multi-plataforma
├── ads-google/                  # Google Ads (74 checks)
├── ads-meta/                    # Meta Ads (46 checks)
├── ads-youtube/                 # YouTube Ads
├── ads-linkedin/                # LinkedIn Ads (25 checks)
├── ads-tiktok/                  # TikTok Ads (25 checks)
├── ads-microsoft/               # Microsoft/Bing Ads (20 checks)
├── ads-creative/                # Auditoría creativa cross-platform
├── ads-landing/                 # Calidad de landing pages
├── ads-budget/                  # Asignación de presupuesto y bidding
├── ads-plan/                    # Planificación estratégica
│   └── assets/                  # 11 industry templates
├── ads-competitor/              # Inteligencia competitiva
├── brand-designer/              # Skill para diseño de marca
├── brand-director/              # Skill para dirección de marca
├── brand-identity/              # Skill para identidad de marca
├── copy-viral/                  # Copy viral
├── creating-100m-offers/        # Ofertas ($100M Offers)
├── creating-ads/                # Creación de anuncios
├── creating-skills/             # Crear nuevos skills
├── creating-vsl/                # Creación de VSLs
├── error-handling-patterns/     # Patrones de manejo de errores
├── gmail/                       # Skill para Gmail
├── managing-influencers/        # Gestión de influencers
├── managing-notion/             # Gestión de Notion
├── notebooklm/                  # NotebookLM (research, audio, video)
├── notion-automation/           # Automatización de Notion
├── openclaw/                    # OpenClaw
├── orchestrator/                # Orquestador
├── skool-manager/               # Gestión de Skool
├── superpowers/                 # 🔥 Framework Superpowers (14 sub-skills)
├── youtube-scriptmaster/        # Scripts para YouTube
├── claude-code-config/          # ⚙️ Configuración de Claude Code
│   ├── settings.json
│   └── skills/
└── workflows/                   # Workflows globales
```

## 🔧 Instalación en un computador nuevo

### 1. Clonar este repo
```bash
git clone https://github.com/Velocity-sudo/agent-skills.git ~/Desktop/AntiGravity/agent-skills
```

### 2. Copiar skills a un proyecto
```bash
cp -r ~/Desktop/AntiGravity/agent-skills/* /path/to/project/.antigravity/skills/
```

### 3. Instalar skills de Claude Code (opcional)
```bash
cp ~/.agent/skills/claude-code-config/settings.json ~/.claude/settings.json
mkdir -p ~/.claude/skills
cp -R ~/.agent/skills/claude-code-config/skills/* ~/.claude/skills/
```

### 4. Instalar GitHub CLI (si no está)
```bash
curl -L "https://github.com/cli/cli/releases/latest" -o /tmp/gh.zip
# O en Mac: brew install gh
gh auth login --web
```

### 5. ¡Listo! 🎉
Los skills están disponibles globalmente para Antigravity, OpenCode y Claude Code.

## 📅 Última actualización
- **Fecha:** 2026-02-18
- **Cambios:** Ads skill añadido (13 skills, 190 checks, 6 plataformas). SOUL.md actualizado. README actualizado.
