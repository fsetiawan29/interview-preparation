import { useEffect } from "react";
import { useTraceStore } from "@/stores/traceStore";
import { usePlaybackStore } from "@/stores/playbackStore";

function isTypingTarget(target: EventTarget | null): boolean {
  if (!(target instanceof HTMLElement)) return false;
  const tag = target.tagName;
  return tag === "INPUT" || tag === "TEXTAREA" || target.isContentEditable;
}

function isDialogOpen(): boolean {
  return document.querySelector('[role="dialog"]') !== null;
}

/** Space = play/pause, Left/Right = step, Home/End = first/last step. */
export function useKeyboardShortcuts(): void {
  useEffect(() => {
    function handleKeyDown(event: KeyboardEvent) {
      if (isTypingTarget(event.target) || isDialogOpen()) return;
      if (!useTraceStore.getState().trace) return;

      switch (event.key) {
        case " ":
          event.preventDefault();
          usePlaybackStore.getState().toggle();
          break;
        case "ArrowLeft":
          event.preventDefault();
          usePlaybackStore.getState().pause();
          useTraceStore.getState().stepBackward();
          break;
        case "ArrowRight":
          event.preventDefault();
          usePlaybackStore.getState().pause();
          useTraceStore.getState().stepForward();
          break;
        case "Home":
          event.preventDefault();
          usePlaybackStore.getState().pause();
          useTraceStore.getState().goToFirst();
          break;
        case "End":
          event.preventDefault();
          usePlaybackStore.getState().pause();
          useTraceStore.getState().goToLast();
          break;
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, []);
}
