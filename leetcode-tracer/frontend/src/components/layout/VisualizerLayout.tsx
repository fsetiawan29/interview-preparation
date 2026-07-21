import { useState } from "react";
import { PanelLeft, Variable, Sparkles, GitBranch, Image } from "lucide-react";
import { useTraceStore } from "@/stores/traceStore";
import { Header } from "./Header";
import { TimelinePanel } from "@/components/timeline/TimelinePanel";
import { VariablesPanel } from "@/components/variables/VariablesPanel";
import { DecisionPanel } from "@/components/decision/DecisionPanel";
import { EventPanel } from "@/components/event/EventPanel";
import { VisualizationArea } from "@/components/visualization/VisualizationArea";
import { PlaybackControls } from "@/components/controls/PlaybackControls";
import { Button } from "@/components/ui/button";

type PanelKey = "timeline" | "variables" | "events" | "decision" | "visualization";

const PANEL_TOGGLES: { key: PanelKey; label: string; icon: typeof PanelLeft }[] = [
  { key: "timeline", label: "Timeline", icon: PanelLeft },
  { key: "variables", label: "Variables", icon: Variable },
  { key: "events", label: "Events", icon: Sparkles },
  { key: "decision", label: "Decision", icon: GitBranch },
  { key: "visualization", label: "Visualization", icon: Image },
];

export function VisualizerLayout() {
  const trace = useTraceStore((s) => s.trace);
  const resolvedSnapshots = useTraceStore((s) => s.resolvedSnapshots);
  const currentStepIndex = useTraceStore((s) => s.currentStepIndex);
  const goToStep = useTraceStore((s) => s.goToStep);

  const [visiblePanels, setVisiblePanels] = useState<Record<PanelKey, boolean>>({
    timeline: true,
    variables: true,
    events: true,
    decision: true,
    visualization: true,
  });

  if (!trace) return null;

  const currentStep = trace.steps[currentStepIndex];
  const previousStep = currentStepIndex > 0 ? trace.steps[currentStepIndex - 1] : undefined;
  const snapshot = resolvedSnapshots[currentStepIndex] ?? null;

  const togglePanel = (key: PanelKey) =>
    setVisiblePanels((prev) => ({ ...prev, [key]: !prev[key] }));

  const showTimeline = visiblePanels.timeline;
  const showVariables = visiblePanels.variables;
  const showEvents = visiblePanels.events;
  const showMiddleColumn = showVariables || showEvents;
  const showDecision = visiblePanels.decision;

  const panelColumns = [
    showTimeline && "minmax(0,220px)",
    showMiddleColumn && "minmax(0,1fr)",
    showDecision && "minmax(0,260px)",
  ]
    .filter(Boolean)
    .join(" ");

  return (
    <div className="flex h-screen flex-col">
      <Header
        metadata={trace.metadata}
        summary={trace.summary}
        currentStep={currentStepIndex}
        totalSteps={trace.steps.length}
      />

      <div className="flex flex-1 flex-col gap-3 overflow-hidden p-3">
        <div className="flex items-center gap-1.5">
          {PANEL_TOGGLES.map(({ key, label, icon: Icon }) => (
            <Button
              key={key}
              variant={visiblePanels[key] ? "secondary" : "outline"}
              size="sm"
              onClick={() => togglePanel(key)}
              aria-pressed={visiblePanels[key]}
            >
              <Icon />
              {label}
            </Button>
          ))}
        </div>

        <div
          className="grid flex-1 grid-cols-1 gap-3 overflow-hidden md:grid-cols-[var(--panel-cols)]"
          style={panelColumns ? ({ "--panel-cols": panelColumns } as React.CSSProperties) : undefined}
        >
          {showTimeline && (
            <div className="min-h-48 overflow-hidden md:min-h-0">
              <TimelinePanel
                steps={trace.steps}
                currentIndex={currentStepIndex}
                onSelect={goToStep}
                onClose={() => togglePanel("timeline")}
              />
            </div>
          )}
          {showMiddleColumn && (
            <div className="flex flex-col gap-3 overflow-hidden">
              {showVariables && (
                <div className="min-h-48 flex-1 overflow-hidden">
                  <VariablesPanel
                    current={currentStep.variables}
                    previous={previousStep?.variables}
                    onClose={() => togglePanel("variables")}
                  />
                </div>
              )}
              {showEvents && (
                <EventPanel events={currentStep.events} onClose={() => togglePanel("events")} />
              )}
            </div>
          )}
          {showDecision && (
            <div className="min-h-48 overflow-hidden md:min-h-0">
              <DecisionPanel decision={currentStep.decision} onClose={() => togglePanel("decision")} />
            </div>
          )}
        </div>

        {visiblePanels.visualization && (
          <div className="min-h-72 flex-[2]">
            <VisualizationArea snapshot={snapshot} onClose={() => togglePanel("visualization")} />
          </div>
        )}

        <PlaybackControls />
      </div>
    </div>
  );
}
