#!/bin/bash
# ============================================================
# Remotion Video Editing — One-Time Setup
# Sales Velocity System
# ============================================================
# Run this once to set up the Remotion video editing environment.
# Usage: bash ~/.agent/skills/editing-video-remotion/scripts/setup.sh
# ============================================================

set -e

echo "═══════════════════════════════════════════════════"
echo "  🎬 REMOTION VIDEO EDITING — SETUP"
echo "  Sales Velocity System"
echo "═══════════════════════════════════════════════════"

PROJECT_DIR="$HOME/Desktop/remotion-studio"
SKILL_DIR="$HOME/.agent/skills/editing-video-remotion"

# 1. Check Node.js
echo ""
echo "🔍 Checking Node.js..."
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo "  ✅ Node.js ${NODE_VERSION} found"
else
    echo "  ❌ Node.js not found. Install from: https://nodejs.org/en/download"
    exit 1
fi

# 2. Check ffmpeg
echo ""
echo "🔍 Checking ffmpeg..."
if command -v ffmpeg &> /dev/null; then
    echo "  ✅ ffmpeg found"
else
    echo "  ⚠️  ffmpeg not found. Installing via Homebrew..."
    if command -v brew &> /dev/null; then
        brew install ffmpeg
        echo "  ✅ ffmpeg installed"
    else
        echo "  ❌ Neither ffmpeg nor Homebrew found."
        echo "     Install ffmpeg: brew install ffmpeg"
        exit 1
    fi
fi

# 3. Create Remotion project
echo ""
echo "🎬 Setting up Remotion project..."
if [ -d "$PROJECT_DIR" ]; then
    echo "  ℹ️  Project directory already exists at $PROJECT_DIR"
else
    echo "  📁 Creating project at $PROJECT_DIR"
    mkdir -p "$PROJECT_DIR"
    cd "$PROJECT_DIR"
    npx -y create-video@latest ./ --template blank --package-manager npm
fi

# 4. Install dependencies
echo ""
echo "📦 Installing Remotion packages..."
cd "$PROJECT_DIR"
npm install --save-exact \
    remotion@4.0.434 \
    @remotion/cli@4.0.434 \
    @remotion/google-fonts@4.0.434 \
    @remotion/install-whisper-cpp@4.0.434

# 5. Install tsx for running TypeScript scripts
npm install -D tsx

# 6. Copy component files from skill resources
echo ""
echo "📋 Copying component files..."
mkdir -p "$PROJECT_DIR/src"
mkdir -p "$PROJECT_DIR/public"

cp "$SKILL_DIR/resources/CaptionedVideo.tsx" "$PROJECT_DIR/src/CaptionedVideo.tsx"
cp "$SKILL_DIR/resources/theme.ts" "$PROJECT_DIR/src/theme.ts"
cp "$SKILL_DIR/resources/process-video.ts" "$PROJECT_DIR/process-video.ts"

echo "  ✅ Files copied to project"

# 7. Check Auphonic API key
echo ""
echo "🔑 Checking environment variables..."
if [ -n "$AUPHONIC_API_KEY" ]; then
    echo "  ✅ AUPHONIC_API_KEY is set"
else
    echo "  ⚠️  AUPHONIC_API_KEY not set — audio processing will be skipped"
    echo "     Get a free key at: https://auphonic.com"
    echo "     Then: export AUPHONIC_API_KEY='your-key'"
fi

echo ""
echo "═══════════════════════════════════════════════════"
echo "  ✅ SETUP COMPLETE"
echo ""
echo "  Project: $PROJECT_DIR"
echo ""
echo "  To edit a video:"
echo "    cd $PROJECT_DIR"
echo "    npx tsx process-video.ts --input /path/to/video.mp4"
echo ""
echo "  First run will download Whisper model (~1.5GB)"
echo "═══════════════════════════════════════════════════"
