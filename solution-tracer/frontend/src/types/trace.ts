import type { Snapshot } from "./snapshot";

export interface Decision {
  condition: string;
  result: boolean;
  action: string;
}

export interface Step {
  id: number;
  title: string;
  timestamp: number;
  variables: Record<string, unknown>;
  decision: Decision | null;
  events: string[];
  snapshot: Snapshot | null;
  statistics?: Record<string, number>;
}

export interface Metadata {
  problem: string;
  difficulty: string | null;
  language: string;
  algorithm: string | null;
  time_complexity: string | null;
  space_complexity: string | null;
}

export interface Summary {
  iterations: number;
  skipped_iterations: number;
  while_loops: number;
  max_recursion_depth: number;
  max_stack_size: number;
  max_queue_size: number;
  max_heap_size: number;
  execution_time: number;
  answer: unknown;
}

export interface TraceFile {
  schema_version: string;
  problem: string;
  metadata: Metadata;
  input?: unknown;
  steps: Step[];
  summary: Summary;
}
