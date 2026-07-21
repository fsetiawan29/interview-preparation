import { useState } from "react";
import { parseTraceFile } from "@/types/traceSchema";
import { useTraceStore } from "@/stores/traceStore";
import { SAMPLE_TRACES } from "@/data/sampleTraces";
import { DropZone } from "./DropZone";
import { FilePicker } from "./FilePicker";
import { SampleTraceMenu } from "./SampleTraceMenu";

export function EmptyState() {
  const loadTrace = useTraceStore((s) => s.loadTrace);
  const [error, setError] = useState<string | null>(null);

  async function handleFile(file: File) {
    setError(null);
    let json: unknown;
    try {
      json = JSON.parse(await file.text());
    } catch {
      setError(`"${file.name}" is not valid JSON.`);
      return;
    }
    const result = parseTraceFile(json);
    if (!result.success) {
      setError(result.error);
      return;
    }
    loadTrace(result.data);
  }

  return (
    <div className="mx-auto flex max-w-lg flex-1 flex-col items-center justify-center gap-6 p-6">
      <div className="text-center">
        <h1 className="text-2xl font-semibold">Solution Trace Visualizer</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Load a trace JSON file exported by the solution-tracer SDK to step through an algorithm's
          execution.
        </p>
      </div>

      <div className="w-full">
        <DropZone onFile={handleFile} />
      </div>

      {error && <p className="text-sm text-destructive">{error}</p>}

      <div className="flex flex-wrap items-center justify-center gap-3">
        <FilePicker onFile={handleFile} />
        <SampleTraceMenu samples={SAMPLE_TRACES} onSelect={(sample) => loadTrace(sample.data)} />
      </div>
    </div>
  );
}
