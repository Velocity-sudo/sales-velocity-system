---
name: editing-video-remotion
description: Automates client video editing with Remotion — transcription, smart cut, broadcast-grade audio, and animated captions. Use when the user mentions editing video, remotion, editar video, reels, subtítulos automáticos, video captions, or automated video editing.
---

# Editing Video with Remotion

Zero-touch pipeline: raw footage → transcribed → smart-cut → pro audio → animated captions → broadcast-grade MP4.

## When to use this skill
- Client needs a video edited with professional captions (reels, content, testimonials)
- User mentions "remotion", "editar video", "subtítulos", "captions", "reels"
- Batch processing multiple client videos

## Prerequisites

### One-time setup (run once per machine)
```bash
# 1. Verify Node.js ≥16 and ffmpeg are installed
node --version && ffmpeg -version

# 2. Scaffold a Remotion project (if not already done)
cd ~/Desktop/remotion-studio
npx create-video@latest ./  # Select "Blank" template, yes to TailwindCSS, yes to Skills

# 3. Install required Remotion packages
npm install --save-exact remotion@4.0.434 @remotion/cli@4.0.434 @remotion/google-fonts@4.0.434 @remotion/install-whisper-cpp@4.0.434

# 4. Download Whisper model (~1.5GB, takes 5-10 min first time)
# This is handled automatically by process-video.ts on first run
```

### Environment Variables
```bash
export AUPHONIC_API_KEY="your-auphonic-api-key"  # Free tier: 2hrs/month
```

## Workflow

### Pre-flight checklist
- [ ] Video file exists at specified path
- [ ] `~/Desktop/remotion-studio` project exists (run setup if not)
- [ ] `AUPHONIC_API_KEY` env var is set (or skip audio processing step)
- [ ] Sufficient disk space (~3x the video file size for temp files)

### Pipeline (4 Steps)

#### Step 1 — Transcribe & Analyze (~30s per minute of video)
1. Extract audio from video with ffmpeg:
   ```bash
   ffmpeg -i input.mp4 -ar 16000 -ac 1 -c:a pcm_s16le audio.wav -y
   ```
2. Transcribe with Whisper.cpp (local, word-level timestamps):
   ```typescript
   import { installWhisperCpp, downloadWhisperModel, transcribe, toCaptions } from '@remotion/install-whisper-cpp';

   const whisperPath = path.join(process.cwd(), 'whisper.cpp');
   await installWhisperCpp({ to: whisperPath, version: '1.5.5' });
   await downloadWhisperModel({ model: 'medium.en', folder: whisperPath });

   const output = await transcribe({
     model: 'medium.en',
     whisperPath,
     whisperCppVersion: '1.5.5',
     inputPath: 'audio.wav',
     tokenLevelTimestamps: true,
   });

   const { captions } = toCaptions({ whisperCppOutput: output });
   ```
3. Parse transcript → detect false starts, "take 2" moments, filler mistakes
4. Identify the **clean take** with precise start/end timestamps

#### Step 2 — Smart Cut (~5s)
Use ffmpeg to trim to the clean take:
```bash
ffmpeg -i input.mp4 -ss [START] -to [END] -c copy trimmed.mp4 -y
```

#### Step 3 — Audio Processing via Auphonic (~60s)
> **Skip this step if no `AUPHONIC_API_KEY` is set.**

1. Create production via Auphonic API:
   ```bash
   curl -X POST https://auphonic.com/api/productions.json \
     -u "$AUPHONIC_API_KEY:" \
     -F "title=Client Video" \
     -F "algorithms[leveler]=true" \
     -F "algorithms[normloudness]=true" \
     -F "algorithms[loudnesstarget]=-16" \
     -F "algorithms[denoise]=true" \
     -F "algorithms[denoisemethod]=dynamic" \
     -F "output_files[0][format]=aac" \
     -F "output_files[0][bitrate]=192"
   ```
2. Upload trimmed audio → start processing → poll until complete → download result

#### Step 4 — Render with Remotion Captions (~2-3 min per minute of video)
1. Copy `CaptionedVideo.tsx` and `theme.ts` from `resources/` into the Remotion project `src/`
2. Place the trimmed video and processed audio in `public/`
3. Write `captions.json` (from Step 1) to `public/`
4. Register the composition in `src/Root.tsx`
5. Render:
   ```bash
   npx remotion render CaptionedVideo output.mp4 --codec h264
   ```
6. Output saved to Desktop

### Output
- **File**: `~/Desktop/[client-name]-edited-[date].mp4`
- **Format**: H.264 MP4, 1080x1920 (vertical reel) or 1920x1080 (landscape)
- **Audio**: Broadcast-grade (16 LUFS, denoised, AAC 192kbps)
- **Captions**: Animated word-by-word, neon green highlight

## Caption Styling Reference

| Property | Value |
|----------|-------|
| Font | Inter, 72px, weight 800 |
| Letter spacing | 0.02em |
| Words per chunk | 4 |
| Current word | `#BFF549` + glow + `scale(1.1)` |
| Past words | `#FFFFFF` |
| Future words | `rgba(255,255,255,0.5)` |
| Text shadow | `0 4px 20px rgba(0,0,0,0.8)` |
| Position | Bottom, 120px |
| Gradient overlay | 40% height, fade to `rgba(0,0,0,0.85)` |

To customize per client, edit `theme.ts` — change `currentWordColor` to match the client's brand accent color.

## Troubleshooting

- **Whisper model download fails**: Check internet connection. Model is ~1.5GB. Run manually: `downloadWhisperModel({ model: 'medium.en', folder: './whisper.cpp' })`
- **ffmpeg not found**: Install via `brew install ffmpeg` (macOS)
- **Auphonic timeout**: Free tier has processing queue. Wait 2-3 minutes. Poll status endpoint.
- **Render OOM**: For very long videos (>10 min), increase Node memory: `NODE_OPTIONS=--max-old-space-size=8192 npx remotion render ...`
- **Non-English audio**: Change Whisper model to `medium` (not `.en`) and set language param in `transcribe()`

## Resources
- [CaptionedVideo.tsx](resources/CaptionedVideo.tsx) — React component template
- [theme.ts](resources/theme.ts) — Caption design tokens
- [process-video.ts](resources/process-video.ts) — Full orchestration script
- [Remotion Docs](https://www.remotion.dev/docs/)
- [@remotion/install-whisper-cpp](https://www.remotion.dev/docs/install-whisper-cpp)
