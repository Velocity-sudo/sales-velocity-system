/**
 * Caption Theme — Design Tokens
 * 
 * Customize these values per client brand.
 * The defaults follow the "Sales Velocity" neon green highlight style.
 */

export const captionTheme = {
  // Typography
  fontFamily: 'Inter',
  fontSize: 72,
  fontWeight: 800 as const,
  letterSpacing: '0.02em',
  wordGap: 24,

  // Chunking
  wordsPerChunk: 4,

  // Word States
  currentWordColor: '#BFF549',        // Neon green — the highlighted word
  currentWordGlow: '0 0 40px rgba(191, 245, 73, 0.8)',
  currentWordScale: 1.1,
  pastWordColor: '#FFFFFF',            // White — already spoken
  futureWordColor: 'rgba(255, 255, 255, 0.5)',  // Semi-transparent — upcoming

  // Text Effects
  textShadow: '0 4px 20px rgba(0, 0, 0, 0.8)',

  // Position
  captionBottomOffset: 120,            // px from bottom edge

  // Gradient Overlay (bottom of video)
  gradientHeight: '40%',
  gradientFrom: 'transparent',
  gradientTo: 'rgba(0, 0, 0, 0.85)',

  // Cleanup Rules
  removeTrailingPunctuation: true,     // Remove . , at end of words
  preserveContractions: true,          // Keep don't, it's, etc.
} as const;

/**
 * Video Presets
 */
export const videoPresets = {
  reelVertical: {
    width: 1080,
    height: 1920,
    fps: 30,
    codec: 'h264' as const,
  },
  reelSquare: {
    width: 1080,
    height: 1080,
    fps: 30,
    codec: 'h264' as const,
  },
  landscape: {
    width: 1920,
    height: 1080,
    fps: 30,
    codec: 'h264' as const,
  },
} as const;

export type VideoPreset = keyof typeof videoPresets;
