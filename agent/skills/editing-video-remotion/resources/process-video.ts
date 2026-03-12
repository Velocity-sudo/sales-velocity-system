/**
 * process-video.ts — Full Orchestration Script
 *
 * Pipeline: Input Video → Transcribe → Smart Cut → Audio Processing → Brand Theme → Render
 *
 * Usage:
 *   npx tsx process-video.ts --input /path/to/video.mp4 --client "Jorge Vergara"
 *
 * Options:
 *   --input       Path to input video file (required)
 *   --client      Client name — auto-extracts brand colors from BRAND_MANUAL.html
 *   --output      Path for output file (default: ~/Desktop/[name]-edited-[date].mp4)
 *   --preset      Video preset: reelVertical | reelSquare | landscape (default: reelVertical)
 *   --skip-audio  Skip Auphonic audio processing step
 *   --language    Whisper language (default: en, use 'es' for Spanish)
 *   --model       Whisper model (default: medium.en, use 'medium' for non-English)
 */

import path from 'path';
import fs from 'fs';
import { execSync, exec } from 'child_process';
import {
  installWhisperCpp,
  downloadWhisperModel,
  transcribe,
  toCaptions,
} from '@remotion/install-whisper-cpp';
import { videoPresets, type VideoPreset } from './theme';
import { extractBrandTheme } from './extract-brand';

// ============================================================
// CONFIG
// ============================================================

interface BrandColors {
  brandAccent: string;
  brandBackground: string;
  brandFont: string;
}

interface ProcessConfig {
  inputPath: string;
  outputPath: string;
  preset: VideoPreset;
  skipAudio: boolean;
  language: string;
  whisperModel: string;
  projectDir: string;
  clientName: string;
  brand: BrandColors;
}

function parseArgs(): ProcessConfig {
  const args = process.argv.slice(2);
  const get = (flag: string, defaultVal = ''): string => {
    const idx = args.indexOf(flag);
    return idx !== -1 && args[idx + 1] ? args[idx + 1] : defaultVal;
  };

  const inputPath = get('--input');
  if (!inputPath) {
    console.error('❌ --input is required. Usage: npx tsx process-video.ts --input /path/to/video.mp4 --client "Client Name"');
    process.exit(1);
  }

  const inputName = path.basename(inputPath, path.extname(inputPath));
  const date = new Date().toISOString().split('T')[0];
  const clientName = get('--client', '');

  // Extract brand colors from client's brand manual
  let brand: BrandColors = {
    brandAccent: '#BFF549',
    brandBackground: '#0A0A0A',
    brandFont: 'Inter',
  };

  if (clientName) {
    console.log(`\n🎨 Loading brand theme for: ${clientName}`);
    const theme = extractBrandTheme(clientName);
    brand = {
      brandAccent: theme.brandAccent,
      brandBackground: theme.brandBackground,
      brandFont: theme.brandFontHeading,
    };
  } else {
    console.log('\n🎨 No --client specified. Using default Sales Velocity theme.');
  }

  return {
    inputPath: path.resolve(inputPath),
    outputPath: get('--output', path.join(process.env.HOME || '~', 'Desktop', `${inputName}-edited-${date}.mp4`)),
    preset: (get('--preset', 'reelVertical') as VideoPreset),
    skipAudio: args.includes('--skip-audio'),
    language: get('--language', 'en'),
    whisperModel: get('--model', 'medium.en'),
    projectDir: path.join(process.env.HOME || '~', 'Desktop', 'remotion-studio'),
    clientName,
    brand,
  };
}

// ============================================================
// STEP 1: Transcribe & Analyze
// ============================================================

interface TranscriptionResult {
  captions: Array<{ text: string; startMs: number; endMs: number; confidence: number; timestampMs: number }>;
  cleanTakeStart: number;  // ms
  cleanTakeEnd: number;    // ms
}

async function step1_transcribe(config: ProcessConfig): Promise<TranscriptionResult> {
  console.log('\n🎙️  STEP 1: Transcribe & Analyze');
  console.log('─'.repeat(50));

  const whisperPath = path.join(config.projectDir, 'whisper.cpp');
  const audioPath = path.join(config.projectDir, 'public', 'audio.wav');

  // Extract audio as 16kHz WAV
  console.log('  📤 Extracting audio from video...');
  execSync(
    `ffmpeg -i "${config.inputPath}" -ar 16000 -ac 1 -c:a pcm_s16le "${audioPath}" -y`,
    { stdio: 'pipe' },
  );

  // Install Whisper.cpp if needed
  console.log('  🔧 Checking Whisper.cpp installation...');
  await installWhisperCpp({ to: whisperPath, version: '1.5.5' });
  await downloadWhisperModel({ model: config.whisperModel, folder: whisperPath });

  // Transcribe
  console.log('  🧠 Transcribing with Whisper.cpp...');
  const whisperOutput = await transcribe({
    model: config.whisperModel,
    whisperPath,
    whisperCppVersion: '1.5.5',
    inputPath: audioPath,
    tokenLevelTimestamps: true,
    language: config.language === 'en' ? undefined : config.language,
  });

  const { captions } = toCaptions({ whisperCppOutput: whisperOutput });
  console.log(`  ✅ Transcribed ${captions.length} words`);

  // Simple clean take detection:
  // Look for common "take 2" phrases or assume the full transcript is clean
  let cleanTakeStart = 0;
  let cleanTakeEnd = captions[captions.length - 1]?.endMs || 0;

  const retakePatterns = ['take two', 'take 2', 'let me start over', 'actually wait', 'sorry let me'];
  for (let i = 0; i < captions.length - 2; i++) {
    const phrase = captions.slice(i, i + 3).map(c => c.text.toLowerCase()).join(' ');
    for (const pattern of retakePatterns) {
      if (phrase.includes(pattern)) {
        // Start the clean take from the next sentence after the retake phrase
        const nextWordIndex = Math.min(i + 4, captions.length - 1);
        cleanTakeStart = captions[nextWordIndex].startMs;
        console.log(`  ✂️  Detected retake at ${(cleanTakeStart / 1000).toFixed(1)}s— starting clean take from there`);
        break;
      }
    }
  }

  return { captions, cleanTakeStart, cleanTakeEnd };
}

// ============================================================
// STEP 2: Smart Cut
// ============================================================

function step2_smartCut(config: ProcessConfig, result: TranscriptionResult): string {
  console.log('\n✂️  STEP 2: Smart Cut');
  console.log('─'.repeat(50));

  const trimmedPath = path.join(config.projectDir, 'public', 'trimmed.mp4');
  const startSec = (result.cleanTakeStart / 1000).toFixed(3);
  const endSec = (result.cleanTakeEnd / 1000).toFixed(3);

  if (result.cleanTakeStart === 0) {
    // No trimming needed, just copy
    console.log('  ℹ️  No retakes detected — using full video');
    execSync(`cp "${config.inputPath}" "${trimmedPath}"`, { stdio: 'pipe' });
  } else {
    console.log(`  ✂️  Trimming: ${startSec}s → ${endSec}s`);
    execSync(
      `ffmpeg -i "${config.inputPath}" -ss ${startSec} -to ${endSec} -c copy "${trimmedPath}" -y`,
      { stdio: 'pipe' },
    );
  }

  // Filter captions to only include the clean take
  result.captions = result.captions.filter(
    c => c.startMs >= result.cleanTakeStart && c.endMs <= result.cleanTakeEnd,
  );

  // Re-zero the captions timestamps to start from 0
  const offset = result.cleanTakeStart;
  result.captions = result.captions.map(c => ({
    ...c,
    startMs: c.startMs - offset,
    endMs: c.endMs - offset,
    timestampMs: c.timestampMs - offset,
  }));

  console.log(`  ✅ Trimmed video saved. ${result.captions.length} caption words retained.`);
  return trimmedPath;
}

// ============================================================
// STEP 3: Audio Processing (Auphonic)
// ============================================================

async function step3_audioProcessing(config: ProcessConfig, trimmedPath: string): Promise<string | null> {
  console.log('\n🎧  STEP 3: Audio Processing (Auphonic)');
  console.log('─'.repeat(50));

  const apiKey = process.env.AUPHONIC_API_KEY;

  if (config.skipAudio || !apiKey) {
    console.log('  ⏭️  Skipping audio processing (no API key or --skip-audio flag)');
    return null;
  }

  const processedAudioPath = path.join(config.projectDir, 'public', 'processed.aac');

  // Extract audio from trimmed video
  const trimmedAudioPath = path.join(config.projectDir, 'public', 'trimmed-audio.wav');
  execSync(
    `ffmpeg -i "${trimmedPath}" -ar 16000 -ac 1 -c:a pcm_s16le "${trimmedAudioPath}" -y`,
    { stdio: 'pipe' },
  );

  // Create Auphonic production
  console.log('  📡 Creating Auphonic production...');
  const createResult = execSync(
    `curl -s -X POST https://auphonic.com/api/productions.json ` +
    `-u "${apiKey}:" ` +
    `-H "Content-Type: application/json" ` +
    `-d '${JSON.stringify({
      title: 'Sales Velocity Video Edit',
      algorithms: {
        leveler: true,
        normloudness: true,
        loudnesstarget: -16,
        denoise: true,
        denoisemethod: 'dynamic',
      },
      output_files: [{ format: 'aac', bitrate: '192' }],
    })}'`,
    { encoding: 'utf-8' },
  );

  const productionData = JSON.parse(createResult);
  const productionUuid = productionData.data?.uuid;

  if (!productionUuid) {
    console.log('  ⚠️  Failed to create Auphonic production. Skipping audio processing.');
    return null;
  }

  // Upload audio
  console.log('  📤 Uploading audio to Auphonic...');
  execSync(
    `curl -s -X POST https://auphonic.com/api/production/${productionUuid}/upload.json ` +
    `-u "${apiKey}:" ` +
    `-F "input_file=@${trimmedAudioPath}"`,
    { stdio: 'pipe' },
  );

  // Start processing
  console.log('  ⚙️  Starting Auphonic processing...');
  execSync(
    `curl -s -X POST https://auphonic.com/api/production/${productionUuid}/start.json ` +
    `-u "${apiKey}:"`,
    { stdio: 'pipe' },
  );

  // Poll for completion
  console.log('  ⏳ Waiting for Auphonic to finish...');
  let status = 0;
  const maxAttempts = 60;
  for (let attempt = 0; attempt < maxAttempts; attempt++) {
    await new Promise(resolve => setTimeout(resolve, 3000));
    const statusResult = execSync(
      `curl -s https://auphonic.com/api/production/${productionUuid}.json -u "${apiKey}:"`,
      { encoding: 'utf-8' },
    );
    const statusData = JSON.parse(statusResult);
    status = statusData.data?.status;

    if (status === 3) { // 3 = Done
      console.log('  ✅ Auphonic processing complete!');
      break;
    }
    if (status === 9 || status === 11) { // Error states
      console.log('  ⚠️  Auphonic processing failed. Using original audio.');
      return null;
    }
  }

  if (status !== 3) {
    console.log('  ⚠️  Auphonic timed out. Using original audio.');
    return null;
  }

  // Download processed audio
  const outputUrl = `https://auphonic.com/api/production/${productionUuid}/output_files.json`;
  const outputResult = execSync(
    `curl -s "${outputUrl}" -u "${apiKey}:"`,
    { encoding: 'utf-8' },
  );
  const outputData = JSON.parse(outputResult);
  const downloadUrl = outputData.data?.[0]?.download_url;

  if (downloadUrl) {
    execSync(`curl -s -o "${processedAudioPath}" "${downloadUrl}" -u "${apiKey}:"`, { stdio: 'pipe' });
    console.log('  📥 Processed audio downloaded.');
    return 'processed.aac';
  }

  return null;
}

// ============================================================
// STEP 4: Render with Remotion
// ============================================================

function step4_render(config: ProcessConfig, result: TranscriptionResult, audioSrc: string | null): void {
  console.log('\n🎬  STEP 4: Render with Remotion');
  console.log('─'.repeat(50));

  const preset = videoPresets[config.preset];
  const captionsPath = path.join(config.projectDir, 'public', 'captions.json');

  // Write captions file
  fs.writeFileSync(captionsPath, JSON.stringify(result.captions, null, 2));
  console.log(`  📝 Wrote ${result.captions.length} captions to captions.json`);

  // Calculate duration in frames
  const lastCaption = result.captions[result.captions.length - 1];
  const durationMs = lastCaption ? lastCaption.endMs + 500 : 10000;  // +500ms buffer
  const durationInFrames = Math.ceil((durationMs / 1000) * preset.fps);

  // Build input props — includes brand colors from client's manual
  const inputProps = JSON.stringify({
    videoSrc: 'trimmed.mp4',
    audioSrc: audioSrc || undefined,
    captions: result.captions,
    muteOriginal: !!audioSrc,
    brandAccent: config.brand.brandAccent,
    brandBackground: config.brand.brandBackground,
    brandFont: config.brand.brandFont,
  });

  const propsPath = path.join(config.projectDir, 'input-props.json');
  fs.writeFileSync(propsPath, inputProps);

  // Render
  console.log(`  🖥️  Rendering ${preset.width}x${preset.height} @ ${preset.fps}fps...`);
  console.log(`  🎨 Brand: accent=${config.brand.brandAccent}, font=${config.brand.brandFont}`);
  console.log(`  ⏱️  Duration: ${(durationMs / 1000).toFixed(1)}s (${durationInFrames} frames)`);

  execSync(
    `cd "${config.projectDir}" && npx remotion render CaptionedVideo "${config.outputPath}" ` +
    `--codec ${preset.codec} ` +
    `--width ${preset.width} ` +
    `--height ${preset.height} ` +
    `--fps ${preset.fps} ` +
    `--frames=0-${durationInFrames - 1} ` +
    `--props "${propsPath}"`,
    { stdio: 'inherit' },
  );

  console.log(`\n🎉  Done! Output saved to: ${config.outputPath}`);
}

// ============================================================
// MAIN
// ============================================================

async function main(): Promise<void> {
  console.log('═'.repeat(50));
  console.log('  🎬 REMOTION VIDEO EDITING PIPELINE');
  console.log('  Sales Velocity System — Automated Video Editor');
  console.log('═'.repeat(50));

  const config = parseArgs();

  console.log(`  📁 Input:   ${config.inputPath}`);
  console.log(`  📁 Output:  ${config.outputPath}`);
  console.log(`  🖥️  Preset:  ${config.preset}`);
  console.log(`  🌐 Language: ${config.language}`);
  if (config.clientName) {
    console.log(`  🎨 Client:  ${config.clientName} → accent ${config.brand.brandAccent}`);
  }

  // Verify input exists
  if (!fs.existsSync(config.inputPath)) {
    console.error(`❌ Input file not found: ${config.inputPath}`);
    process.exit(1);
  }

  // Verify project dir exists
  if (!fs.existsSync(config.projectDir)) {
    console.error(`❌ Remotion project not found at: ${config.projectDir}`);
    console.error('   Run the setup script first: bash ~/.agent/skills/editing-video-remotion/scripts/setup.sh');
    process.exit(1);
  }

  // Ensure public dir exists
  const publicDir = path.join(config.projectDir, 'public');
  if (!fs.existsSync(publicDir)) {
    fs.mkdirSync(publicDir, { recursive: true });
  }

  // Run pipeline
  const transcriptionResult = await step1_transcribe(config);
  const trimmedPath = step2_smartCut(config, transcriptionResult);
  const processedAudio = await step3_audioProcessing(config, trimmedPath);
  step4_render(config, transcriptionResult, processedAudio);
}

main().catch(err => {
  console.error('❌ Pipeline failed:', err);
  process.exit(1);
});
