import { create } from "zustand";

export const SPEED_OPTIONS = [0.5, 1, 1.5, 2, 3, 4] as const;
export type Speed = (typeof SPEED_OPTIONS)[number];

interface PlaybackState {
  isPlaying: boolean;
  speed: Speed;
  play: () => void;
  pause: () => void;
  toggle: () => void;
  setSpeed: (speed: Speed) => void;
}

export const usePlaybackStore = create<PlaybackState>((set, get) => ({
  isPlaying: false,
  speed: 1,

  play: () => set({ isPlaying: true }),
  pause: () => set({ isPlaying: false }),
  toggle: () => set({ isPlaying: !get().isPlaying }),
  setSpeed: (speed) => set({ speed }),
}));
