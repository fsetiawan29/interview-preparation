import { useTraceStore } from "@/stores/traceStore";
import { usePlaybackEngine } from "@/hooks/usePlaybackEngine";
import { useKeyboardShortcuts } from "@/hooks/useKeyboardShortcuts";
import { TooltipProvider } from "@/components/ui/tooltip";
import { EmptyState } from "@/components/common/EmptyState";
import { VisualizerLayout } from "@/components/layout/VisualizerLayout";

export function App() {
  const trace = useTraceStore((s) => s.trace);

  usePlaybackEngine();
  useKeyboardShortcuts();

  return (
    <TooltipProvider>
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        {trace ? <VisualizerLayout /> : <EmptyState />}
      </div>
    </TooltipProvider>
  );
}
