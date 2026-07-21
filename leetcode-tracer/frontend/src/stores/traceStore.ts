import { create } from "zustand";
import type { Snapshot } from "@/types/snapshot";
import type { TraceFile } from "@/types/trace";

function resolveSnapshots(trace: TraceFile): (Snapshot | null)[] {
  const resolved: (Snapshot | null)[] = [];
  let last: Snapshot | null = null;
  for (const step of trace.steps) {
    last = step.snapshot ?? last;
    resolved.push(last);
  }
  return resolved;
}

interface TraceState {
  trace: TraceFile | null;
  resolvedSnapshots: (Snapshot | null)[];
  currentStepIndex: number;
  loadTrace: (trace: TraceFile) => void;
  goToStep: (index: number) => void;
  stepForward: () => void;
  stepBackward: () => void;
  goToFirst: () => void;
  goToLast: () => void;
  reset: () => void;
}

export const useTraceStore = create<TraceState>((set, get) => ({
  trace: null,
  resolvedSnapshots: [],
  currentStepIndex: 0,

  loadTrace: (trace) =>
    set({
      trace,
      resolvedSnapshots: resolveSnapshots(trace),
      currentStepIndex: 0,
    }),

  goToStep: (index) => {
    const { trace } = get();
    if (!trace) return;
    const clamped = Math.max(0, Math.min(index, trace.steps.length - 1));
    set({ currentStepIndex: clamped });
  },

  stepForward: () => {
    const { trace, currentStepIndex } = get();
    if (!trace) return;
    if (currentStepIndex < trace.steps.length - 1) {
      set({ currentStepIndex: currentStepIndex + 1 });
    }
  },

  stepBackward: () => {
    const { currentStepIndex } = get();
    if (currentStepIndex > 0) {
      set({ currentStepIndex: currentStepIndex - 1 });
    }
  },

  goToFirst: () => set({ currentStepIndex: 0 }),

  goToLast: () => {
    const { trace } = get();
    if (!trace) return;
    set({ currentStepIndex: trace.steps.length - 1 });
  },

  reset: () => set({ trace: null, resolvedSnapshots: [], currentStepIndex: 0 }),
}));
