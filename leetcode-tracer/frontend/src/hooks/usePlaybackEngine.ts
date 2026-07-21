import { useEffect } from "react";
import { useTraceStore } from "@/stores/traceStore";
import { usePlaybackStore } from "@/stores/playbackStore";

const BASE_INTERVAL_MS = 800;

/** Drives auto-advance during playback. Mount once near the app root. */
export function usePlaybackEngine(): void {
  const isPlaying = usePlaybackStore((s) => s.isPlaying);
  const speed = usePlaybackStore((s) => s.speed);

  useEffect(() => {
    if (!isPlaying) return;

    const id = window.setInterval(() => {
      const { trace, currentStepIndex, stepForward } = useTraceStore.getState();
      if (!trace || currentStepIndex >= trace.steps.length - 1) {
        usePlaybackStore.getState().pause();
        return;
      }
      stepForward();
    }, BASE_INTERVAL_MS / speed);

    return () => window.clearInterval(id);
  }, [isPlaying, speed]);
}
