import { Upload } from "lucide-react";
import type { Metadata, Summary } from "@/types/trace";
import { useTraceStore } from "@/stores/traceStore";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { SummaryPanel } from "@/components/summary/SummaryPanel";
import { ThemeToggle } from "./ThemeToggle";

export function Header({
  metadata,
  summary,
  currentStep,
  totalSteps,
}: {
  metadata: Metadata;
  summary: Summary;
  currentStep: number;
  totalSteps: number;
}) {
  const reset = useTraceStore((s) => s.reset);

  return (
    <header className="flex flex-col gap-3 border-b bg-background px-4 py-3 sm:flex-row sm:items-center sm:justify-between">
      <div className="flex flex-col gap-1">
        <div className="flex flex-wrap items-center gap-2">
          <h1 className="text-lg font-semibold">{metadata.problem}</h1>
          {metadata.difficulty && <Badge variant="secondary">{metadata.difficulty}</Badge>}
          {metadata.algorithm && <Badge variant="outline">{metadata.algorithm}</Badge>}
        </div>
        <div className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-muted-foreground">
          {metadata.time_complexity && <span>Time: {metadata.time_complexity}</span>}
          {metadata.space_complexity && <span>Space: {metadata.space_complexity}</span>}
          <span>
            Step {currentStep + 1} / {totalSteps}
          </span>
        </div>
      </div>

      <div className="flex items-center gap-2">
        <SummaryPanel summary={summary} metadata={metadata} />
        <Button variant="outline" size="sm" onClick={reset}>
          <Upload />
          Load another trace
        </Button>
        <ThemeToggle />
      </div>
    </header>
  );
}
