import React, { useMemo } from 'react';
import {
  AbsoluteFill,
  Video,
  Audio,
  useCurrentFrame,
  useVideoConfig,
  interpolate,
  spring,
  staticFile,
  Easing,
} from 'remotion';
import { loadFont } from '@remotion/google-fonts/Inter';
import { captionTheme } from './theme';

const { fontFamily } = loadFont();

/**
 * Caption data structure (output from Whisper.cpp → toCaptions())
 */
interface Caption {
  text: string;
  startMs: number;
  endMs: number;
  confidence: number;
  timestampMs: number;
}

interface CaptionedVideoProps {
  videoSrc: string;           // Path relative to /public (e.g., 'trimmed.mp4')
  audioSrc?: string;          // Processed audio path (e.g., 'processed.aac') — optional
  captions: Caption[];        // Array of word-level captions from Whisper
  muteOriginal?: boolean;     // Mute original video audio (default: true if audioSrc provided)
}

/**
 * Cleans a word for display:
 * - Removes trailing punctuation (. , ;) if configured
 * - Preserves contractions (don't, it's, we're)
 * - Trims whitespace
 */
function cleanWord(word: string): string {
  let cleaned = word.trim();
  if (captionTheme.removeTrailingPunctuation) {
    cleaned = cleaned.replace(/[.,;:!?]+$/, '');
  }
  return cleaned;
}

/**
 * Groups captions into chunks of N words for display
 */
function chunkCaptions(captions: Caption[], wordsPerChunk: number): Caption[][] {
  const chunks: Caption[][] = [];
  for (let i = 0; i < captions.length; i += wordsPerChunk) {
    chunks.push(captions.slice(i, i + wordsPerChunk));
  }
  return chunks;
}

/**
 * Determines which chunk is active at a given time
 */
function getActiveChunk(chunks: Caption[][], currentTimeMs: number): { chunk: Caption[]; index: number } | null {
  for (let i = 0; i < chunks.length; i++) {
    const chunk = chunks[i];
    const chunkStart = chunk[0].startMs;
    const chunkEnd = chunk[chunk.length - 1].endMs;
    if (currentTimeMs >= chunkStart && currentTimeMs <= chunkEnd + 200) {
      return { chunk, index: i };
    }
  }
  return null;
}

/**
 * Single Word component with highlight animation
 */
const CaptionWord: React.FC<{
  word: Caption;
  currentTimeMs: number;
  frame: number;
  fps: number;
}> = ({ word, currentTimeMs, frame, fps }) => {
  const isCurrent = currentTimeMs >= word.startMs && currentTimeMs < word.endMs;
  const isPast = currentTimeMs >= word.endMs;

  // Spring animation for the current word scale
  const scaleSpring = spring({
    frame: isCurrent ? frame : 0,
    fps,
    config: { damping: 12, stiffness: 200 },
  });

  const scale = isCurrent
    ? interpolate(scaleSpring, [0, 1], [1, captionTheme.currentWordScale])
    : 1;

  let color: string;
  let textShadow = captionTheme.textShadow;

  if (isCurrent) {
    color = captionTheme.currentWordColor;
    textShadow = `${captionTheme.textShadow}, ${captionTheme.currentWordGlow}`;
  } else if (isPast) {
    color = captionTheme.pastWordColor;
  } else {
    color = captionTheme.futureWordColor;
  }

  return (
    <span
      style={{
        display: 'inline-block',
        color,
        textShadow,
        transform: `scale(${scale})`,
        transition: 'color 0.1s ease',
        marginRight: `${captionTheme.wordGap}px`,
      }}
    >
      {cleanWord(word.text)}
    </span>
  );
};

/**
 * Main CaptionedVideo composition
 *
 * Usage in Root.tsx:
 *   <Composition
 *     id="CaptionedVideo"
 *     component={CaptionedVideo}
 *     durationInFrames={durationInFrames}
 *     fps={30}
 *     width={1080}
 *     height={1920}
 *     defaultProps={{
 *       videoSrc: 'trimmed.mp4',
 *       audioSrc: 'processed.aac',
 *       captions: captionsData,
 *     }}
 *   />
 */
export const CaptionedVideo: React.FC<CaptionedVideoProps> = ({
  videoSrc,
  audioSrc,
  captions,
  muteOriginal,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTimeMs = (frame / fps) * 1000;

  const shouldMute = muteOriginal ?? !!audioSrc;

  // Pre-compute chunks
  const chunks = useMemo(
    () => chunkCaptions(captions, captionTheme.wordsPerChunk),
    [captions],
  );

  const activeResult = getActiveChunk(chunks, currentTimeMs);

  // Fade-in animation for caption chunk transitions
  const chunkOpacity = activeResult
    ? interpolate(
        currentTimeMs - activeResult.chunk[0].startMs,
        [0, 150],
        [0, 1],
        { extrapolateRight: 'clamp' },
      )
    : 0;

  return (
    <AbsoluteFill>
      {/* Base Video */}
      <Video
        src={staticFile(videoSrc)}
        volume={shouldMute ? 0 : 1}
        style={{
          width: '100%',
          height: '100%',
          objectFit: 'cover',
        }}
      />

      {/* Processed Audio Overlay */}
      {audioSrc && <Audio src={staticFile(audioSrc)} volume={1} />}

      {/* Bottom Gradient Overlay */}
      <div
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          right: 0,
          height: captionTheme.gradientHeight,
          background: `linear-gradient(to bottom, ${captionTheme.gradientFrom}, ${captionTheme.gradientTo})`,
          pointerEvents: 'none',
        }}
      />

      {/* Caption Container */}
      <div
        style={{
          position: 'absolute',
          bottom: `${captionTheme.captionBottomOffset}px`,
          left: 0,
          right: 0,
          display: 'flex',
          justifyContent: 'center',
          alignItems: 'center',
          padding: '0 40px',
          opacity: chunkOpacity,
        }}
      >
        {activeResult && (
          <div
            style={{
              fontFamily,
              fontSize: `${captionTheme.fontSize}px`,
              fontWeight: captionTheme.fontWeight,
              letterSpacing: captionTheme.letterSpacing,
              textAlign: 'center',
              lineHeight: 1.2,
            }}
          >
            {activeResult.chunk.map((word, i) => (
              <CaptionWord
                key={`${activeResult.index}-${i}`}
                word={word}
                currentTimeMs={currentTimeMs}
                frame={frame}
                fps={fps}
              />
            ))}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};

export default CaptionedVideo;
