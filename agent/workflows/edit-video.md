---
description: Sales Velocity System workflow to edit client videos automatically. Removes silences, processes audio (Auphonic), and outputs a clean video ready for manual captioning in CapCut.
---

// turbo-all

# /edit-video — Automated Video Editing Pipeline

## Prerequisites
- Remotion studio installed at `~/Desktop/remotion-studio/`
- `AUPHONIC_API_KEY` environment variable set (key: `kL8JuPO5C447HEV52dVHXIPw02ZCsoIZ`)
- ffmpeg installed (`brew install ffmpeg`)
- Client brand manual at `~/Desktop/Clientes/[Client]/01_marca/BRAND_MANUAL.html` (optional, for future caption mode)

## Steps

### 1. Identify the video and client
Ask the user:
- Which video file to process (full path)
- Which client it belongs to (for brand theming)
- Language (default: `es` for Spanish)

### 2. Run the pipeline
```bash
cd ~/Desktop/remotion-studio && export AUPHONIC_API_KEY="kL8JuPO5C447HEV52dVHXIPw02ZCsoIZ" && npx tsx process-video.ts \
  --input "[INPUT_VIDEO_PATH]" \
  --client "[CLIENT_NAME]" \
  --language es \
  --no-captions \
  --output "[OUTPUT_PATH]"
```

**Output naming convention:** `~/Desktop/Clientes/[Client]/[slug]-edited-[date].mp4`

### 3. Verify output
Check the output file exists and report:
- Duration (before vs after)
- Silence removed (seconds)
- File size
- Auphonic processing status

### 4. Deliver
Confirm with the user that the video is ready for manual captioning in CapCut.

## Pipeline Details

| Step | What | Tool |
|------|------|------|
| Transcribe | Whisper.cpp (GPU M4, ~23s for 1.5min video) | `@remotion/install-whisper-cpp` |
| Smart Cut | Detect retakes + remove silences >0.5s | ffmpeg silencedetect + trim/concat |
| Audio | Denoise, level, normalize -16 LUFS | Auphonic API |
| Merge | Trimmed video + processed audio | ffmpeg |

## Options

| Flag | Description |
|------|-------------|
| `--input` | Path to input video (required) |
| `--client` | Client name for brand theming |
| `--output` | Output path (default: `~/Desktop/[name]-edited-[date].mp4`) |
| `--language` | Whisper language: `es`, `en`, etc. (default: `en`) |
| `--no-captions` | **Production mode** — cuts + audio only, no Remotion render |
| `--skip-audio` | Skip Auphonic processing |
| `--preset` | `reelVertical` (default), `reelSquare`, `landscape` |

## Notes
- The `--no-captions` flag is the standard production mode. Captions/titles are added manually in CapCut for premium quality.
- Full caption mode (without `--no-captions`) uses Remotion to render subtitles — experimental, not production-ready yet.
- Whisper model is auto-selected: `medium.en` for English, `medium` for other languages.
