import { useTraceStore } from "@/stores/traceStore";
import { Header } from "./Header";
import { TimelinePanel } from "@/components/timeline/TimelinePanel";
import { VariablesPanel } from "@/components/variables/VariablesPanel";
import { DecisionPanel } from "@/components/decision/DecisionPanel";
import { EventPanel } from "@/components/event/EventPanel";
import { VisualizationArea } from "@/components/visualization/VisualizationArea";
import { PlaybackControls } from "@/components/controls/PlaybackControls";

export function VisualizerLayout() {
  const trace = useTraceStore((s) => s.trace);
  const resolvedSnapshots = useTraceStore((s) => s.resolvedSnapshots);
  const currentStepIndex = useTraceStore((s) => s.currentStepIndex);
  const goToStep = useTraceStore((s) => s.goToStep);

  if (!trace) return null;

  const currentStep = trace.steps[currentStepIndex];
  const previousStep = currentStepIndex > 0 ? trace.steps[currentStepIndex - 1] : undefined;
  const snapshot = resolvedSnapshots[currentStepIndex] ?? null;

  return (
    <div className="flex h-screen flex-col">
      <Header
        metadata={trace.metadata}
        summary={trace.summary}
        currentStep={currentStepIndex}
        totalSteps={trace.steps.length}
      />

      <div className="flex flex-1 flex-col gap-3 overflow-hidden p-3">
        <div className="grid flex-1 grid-cols-1 gap-3 overflow-hidden md:grid-cols-[minmax(0,220px)_minmax(0,1fr)_minmax(0,260px)]">
          <div className="min-h-48 overflow-hidden md:min-h-0">
            <TimelinePanel steps={trace.steps} currentIndex={currentStepIndex} onSelect={goToStep} />
          </div>
          <div className="flex flex-col gap-3 overflow-hidden">
            <div className="min-h-48 flex-1 overflow-hidden">
              <VariablesPanel current={currentStep.variables} previous={previousStep?.variables} />
            </div>
            <EventPanel events={currentStep.events} />
          </div>
          <div className="min-h-48 overflow-hidden md:min-h-0">
            <DecisionPanel decision={currentStep.decision} />
          </div>
        </div>

        <div className="min-h-72 flex-[2]">
          <VisualizationArea snapshot={snapshot} />
        </div>

        <PlaybackControls />
      </div>
    </div>
  );
}
