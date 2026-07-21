import { BarChart3 } from "lucide-react";
import type { Metadata, Summary } from "@/types/trace";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";

function formatValue(value: unknown): string {
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

const STAT_LABELS: Array<[key: keyof Summary, label: string]> = [
  ["iterations", "Iterations"],
  ["skipped_iterations", "Skipped"],
  ["while_loops", "While loops"],
  ["max_recursion_depth", "Max recursion depth"],
  ["max_stack_size", "Max stack size"],
  ["max_queue_size", "Max queue size"],
  ["max_heap_size", "Max heap size"],
];

export function SummaryPanel({ summary, metadata }: { summary: Summary; metadata: Metadata }) {
  return (
    <Dialog>
      <DialogTrigger asChild>
        <Button variant="outline" size="sm">
          <BarChart3 />
          Statistics
        </Button>
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{metadata.problem} — Statistics</DialogTitle>
        </DialogHeader>
        <div className="grid grid-cols-2 gap-3">
          {STAT_LABELS.map(([key, label]) => (
            <div key={key} className="rounded-md border p-3">
              <p className="text-xs text-muted-foreground">{label}</p>
              <p className="font-mono text-lg">{summary[key] as number}</p>
            </div>
          ))}
          <div className="rounded-md border p-3">
            <p className="text-xs text-muted-foreground">Execution time</p>
            <p className="font-mono text-lg">{summary.execution_time.toFixed(6)}s</p>
          </div>
          <div className="col-span-2 rounded-md border p-3">
            <p className="text-xs text-muted-foreground">Answer</p>
            <p className="font-mono text-lg">{formatValue(summary.answer)}</p>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  );
}
