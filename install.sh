#!/bin/bash
# ============================================================
# Sales Velocity System — Installer / Sync Script
# ============================================================
# Run this after cloning the repo:
#   git clone git@github.com:Velocity-sudo/sales-velocity-system.git
#   cd sales-velocity-system
#   chmod +x install.sh
#   ./install.sh
#
# This script is IDEMPOTENT — safe to run multiple times.
# After a `git pull`, just run `./install.sh` again to sync.
# ============================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

log()   { echo -e "${GREEN}[✓]${NC} $1"; }
warn()  { echo -e "${YELLOW}[!]${NC} $1"; }
error() { echo -e "${RED}[✗]${NC} $1"; }

echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   🚀 Sales Velocity System — Installer       ║"
echo "╚══════════════════════════════════════════════╝"
echo ""

# ──────────────────────────────────────────────
# 1. SKILLS → ~/.agent/skills/
# ──────────────────────────────────────────────
echo "── Step 1: Installing Skills ──"
mkdir -p "$HOME/.agent/skills"

# Remove old skills and create fresh symlinks to repo
if [ -L "$HOME/.agent/skills" ]; then
    rm "$HOME/.agent/skills"
    mkdir -p "$HOME/.agent/skills"
fi

# Copy each skill folder (rsync for safety)
rsync -a --delete "$SCRIPT_DIR/agent/skills/" "$HOME/.agent/skills/"
log "Skills installed → ~/.agent/skills/ ($(ls "$HOME/.agent/skills" | wc -l | tr -d ' ') folders)"

# ──────────────────────────────────────────────
# 2. SOUL.md → ~/.agent/SOUL.md
# ──────────────────────────────────────────────
echo "── Step 2: Installing SOUL.md ──"
cp "$SCRIPT_DIR/agent/SOUL.md" "$HOME/.agent/SOUL.md"
log "SOUL.md installed → ~/.agent/SOUL.md"

# ──────────────────────────────────────────────
# 3. WORKFLOWS → 3 locations (critical!)
# ──────────────────────────────────────────────
echo "── Step 3: Installing Workflows (×3 locations) ──"

WORKFLOW_SOURCE="$SCRIPT_DIR/agent/workflows"
DEST_1="$HOME/.agent/workflows"
DEST_2="$HOME/.gemini/workflows"
DEST_3="$HOME/.gemini/antigravity/global_workflows"

mkdir -p "$DEST_1" "$DEST_2" "$DEST_3"

rsync -a --delete "$WORKFLOW_SOURCE/" "$DEST_1/"
rsync -a --delete "$WORKFLOW_SOURCE/" "$DEST_2/"
rsync -a --delete "$WORKFLOW_SOURCE/" "$DEST_3/"

COUNT=$(ls "$DEST_1"/*.md 2>/dev/null | wc -l | tr -d ' ')
log "Workflows installed → 3 locations × $COUNT workflows each"
log "  ├─ ~/.agent/workflows/"
log "  ├─ ~/.gemini/workflows/"
log "  └─ ~/.gemini/antigravity/global_workflows/"

# ──────────────────────────────────────────────
# 4. GEMINI.md → ~/.gemini/GEMINI.md
# ──────────────────────────────────────────────
echo "── Step 4: Installing Global Rule (GEMINI.md) ──"
mkdir -p "$HOME/.gemini"
cp "$SCRIPT_DIR/gemini/GEMINI.md" "$HOME/.gemini/GEMINI.md"
log "GEMINI.md installed → ~/.gemini/GEMINI.md"

# ──────────────────────────────────────────────
# 5. MCP CONFIG → ~/.gemini/antigravity/mcp_config.json
# ──────────────────────────────────────────────
echo "── Step 5: Installing MCP Config ──"
mkdir -p "$HOME/.gemini/antigravity"
cp "$SCRIPT_DIR/gemini/antigravity/mcp_config.json" "$HOME/.gemini/antigravity/mcp_config.json"
log "MCP config installed → ~/.gemini/antigravity/mcp_config.json"

# ──────────────────────────────────────────────
# 6. CLIENT CONFIG + SCRIPTS
# ──────────────────────────────────────────────
echo "── Step 6: Installing Client Config & Scripts ──"
mkdir -p "$HOME/Desktop/Clientes/LuchoBranding/config"
mkdir -p "$HOME/Desktop/Clientes/LuchoBranding/scripts"
mkdir -p "$HOME/Desktop/Clientes/LuchoBranding/logs"

cp "$SCRIPT_DIR/clientes/LuchoBranding/config/clients_config.json" \
   "$HOME/Desktop/Clientes/LuchoBranding/config/clients_config.json"
log "clients_config.json installed"

rsync -a "$SCRIPT_DIR/clientes/LuchoBranding/scripts/" \
         "$HOME/Desktop/Clientes/LuchoBranding/scripts/"
chmod +x "$HOME/Desktop/Clientes/LuchoBranding/scripts/"*.sh 2>/dev/null || true
log "Scripts installed + made executable"

# ──────────────────────────────────────────────
# 7. DEPENDENCY CHECKS
# ──────────────────────────────────────────────
echo ""
echo "── Step 7: Checking Dependencies ──"

check_dep() {
    if command -v "$1" &>/dev/null; then
        log "$1 found → $(command -v "$1")"
        return 0
    else
        warn "$1 NOT FOUND — install it: $2"
        return 1
    fi
}

MISSING=0
check_dep "node"    "brew install node"        || MISSING=$((MISSING+1))
check_dep "npm"     "brew install node"        || MISSING=$((MISSING+1))
check_dep "npx"     "brew install node"        || MISSING=$((MISSING+1))
check_dep "python3" "brew install python3"     || MISSING=$((MISSING+1))
check_dep "git"     "brew install git"         || MISSING=$((MISSING+1))
check_dep "rsync"   "should be pre-installed"  || MISSING=$((MISSING+1))

# Check gh CLI
if [ -f "$HOME/.local/bin/gh" ]; then
    log "GitHub CLI found → ~/.local/bin/gh"
elif command -v gh &>/dev/null; then
    log "GitHub CLI found → $(command -v gh)"
else
    warn "GitHub CLI (gh) not found — install: brew install gh"
    MISSING=$((MISSING+1))
fi

# Check notebooklm-mcp
if command -v notebooklm-mcp &>/dev/null || [ -f "/opt/homebrew/bin/notebooklm-mcp" ]; then
    log "notebooklm-mcp found"
else
    warn "notebooklm-mcp not found — install: pip install notebooklm-mcp"
    MISSING=$((MISSING+1))
fi

# Check Python dependencies for scripts
echo ""
echo "── Checking Python packages ──"
python3 -c "import requests" 2>/dev/null && log "requests ✓" || warn "Missing: pip3 install requests"

# ──────────────────────────────────────────────
# 8. SUMMARY
# ──────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════╗"
echo "║   ✅ Installation Complete!                   ║"
echo "╚══════════════════════════════════════════════╝"
echo ""
echo "Installed:"
echo "  • Skills:      ~/.agent/skills/ ($(ls "$HOME/.agent/skills" | wc -l | tr -d ' ') folders)"
echo "  • Workflows:   3 locations × $COUNT workflows"
echo "  • SOUL.md:     ~/.agent/SOUL.md"
echo "  • GEMINI.md:   ~/.gemini/GEMINI.md"
echo "  • MCP Config:  ~/.gemini/antigravity/mcp_config.json"
echo "  • Client Config + Scripts"
echo ""

if [ $MISSING -gt 0 ]; then
    echo -e "${YELLOW}⚠️  $MISSING dependencies missing — install them before using workflows.${NC}"
else
    echo -e "${GREEN}All dependencies found! System ready. 🎉${NC}"
fi

echo ""
echo "To sync changes from the other computer:"
echo "  git pull && ./install.sh"
echo ""
