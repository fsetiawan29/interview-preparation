import { ChevronFirst, ChevronLast, ChevronLeft, ChevronRight, Pause, Play, RotateCcw } from "lucide-react";
import { useTraceStore } from "@/stores/traceStore";
import { usePlaybackStore } from "@/stores/playbackStore";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { TimelineSlider } from "./TimelineSlider";
import { SpeedControl } from "./SpeedControl";

export function PlaybackControls() {
  const trace = useTraceStore((s) => s.trace);
  const currentStepIndex = useTraceStore((s) => s.currentStepIndex);
  const goToStep = useTraceStore((s) => s.goToStep);
  const stepForward = useTraceStore((s) => s.stepForward);
  const stepBackward = useTraceStore((s) => s.stepBackward);
  const goToFirst = useTraceStore((s) => s.goToFirst);
  const goToLast = useTraceStore((s) => s.goToLast);

  const isPlaying = usePlaybackStore((s) => s.isPlaying);
  const speed = usePlaybackStore((s) => s.speed);
  const toggle = usePlaybackStore((s) => s.toggle);
  const pause = usePlaybackStore((s) => s.pause);
  const setSpeed = usePlaybackStore((s) => s.setSpeed);

  if (!trace) return null;

  const isFirst = currentStepIndex === 0;
  const isLast = currentStepIndex === trace.steps.length - 1;

  function restart() {
    pause();
    goToFirst();
  }

  function withPause(action: () => void) {
    pause();
    action();
  }

  return (
    <Card className="flex flex-col gap-3 p-3 sm:flex-row sm:items-center">
      <div className="flex items-center justify-center gap-1">
        <Button variant="ghost" size="icon-sm" aria-label="First step" onClick={() => withPause(goToFirst)} disabled={isFirst}>
          <ChevronFirst />
        </Button>
        <Button variant="ghost" size="icon-sm" aria-label="Previous step" onClick={() => withPause(stepBackward)} disabled={isFirst}>
          <ChevronLeft />
        </Button>
        <Button variant="default" size="icon" aria-label={isPlaying ? "Pause" : "Play"} onClick={toggle} disabled={isLast && !isPlaying}>
          {isPlaying ? <Pause /> : <Play />}
        </Button>
        <Button variant="ghost" size="icon-sm" aria-label="Next step" onClick={() => withPause(stepForward)} disabled={isLast}>
          <ChevronRight />
        </Button>
        <Button variant="ghost" size="icon-sm" aria-label="Last step" onClick={() => withPause(goToLast)} disabled={isLast}>
          <ChevronLast />
        </Button>
        <Button variant="ghost" size="icon-sm" aria-label="Restart" onClick={restart}>
          <RotateCcw />
        </Button>
      </div>

      <TimelineSlider index={currentStepIndex} max={trace.steps.length - 1} onChange={(i) => withPause(() => goToStep(i))} />

      <SpeedControl speed={speed} onChange={setSpeed} />
    </Card>
  );
}
