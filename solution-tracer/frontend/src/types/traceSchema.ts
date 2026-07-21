import { z } from "zod";

const arraySnapshotSchema = z.object({
  type: z.literal("array"),
  values: z.array(z.unknown()),
  highlights: z.array(z.number()).optional(),
  pointers: z.record(z.string(), z.number()).optional(),
});

const stackSnapshotSchema = z.object({
  type: z.literal("stack"),
  values: z.array(z.unknown()),
  highlights: z.array(z.number()).optional(),
});

const queueSnapshotSchema = z.object({
  type: z.literal("queue"),
  values: z.array(z.unknown()),
  highlights: z.array(z.number()).optional(),
});

const heapSnapshotSchema = z.object({
  type: z.literal("heap"),
  values: z.array(z.unknown()),
  highlights: z.array(z.number()).optional(),
});

const treeSnapshotSchema = z.object({
  type: z.literal("tree"),
  nodes: z.array(
    z.object({
      id: z.number(),
      val: z.unknown(),
      left: z.number().nullable(),
      right: z.number().nullable(),
    }),
  ),
  edges: z.array(z.object({ from: z.number(), to: z.number() })),
  current: z.number().nullable().optional(),
  visited: z.array(z.number()).optional(),
});

const graphSnapshotSchema = z.object({
  type: z.literal("graph"),
  nodes: z.array(z.object({ id: z.string(), label: z.string() })),
  edges: z.array(z.object({ from: z.string(), to: z.string() })),
  current: z.string().nullable().optional(),
  visited: z.array(z.string()).optional(),
});

const linkedListSnapshotSchema = z.object({
  type: z.literal("linked-list"),
  nodes: z.array(
    z.object({
      id: z.number(),
      val: z.unknown(),
      next: z.number().nullable(),
    }),
  ),
  current: z.number().nullable().optional(),
});

const snapshotSchema = z.discriminatedUnion("type", [
  arraySnapshotSchema,
  stackSnapshotSchema,
  queueSnapshotSchema,
  heapSnapshotSchema,
  treeSnapshotSchema,
  graphSnapshotSchema,
  linkedListSnapshotSchema,
]);

const decisionSchema = z.object({
  condition: z.string(),
  result: z.boolean(),
  action: z.string(),
});

const stepSchema = z.object({
  id: z.number(),
  title: z.string(),
  timestamp: z.number(),
  variables: z.record(z.string(), z.unknown()),
  decision: decisionSchema.nullable(),
  events: z.array(z.string()),
  snapshot: snapshotSchema.nullable(),
  statistics: z.record(z.string(), z.number()).optional(),
});

const metadataSchema = z.object({
  problem: z.string(),
  difficulty: z.string().nullable(),
  language: z.string(),
  algorithm: z.string().nullable(),
  time_complexity: z.string().nullable(),
  space_complexity: z.string().nullable(),
});

const summarySchema = z.object({
  iterations: z.number(),
  skipped_iterations: z.number(),
  while_loops: z.number(),
  max_recursion_depth: z.number(),
  max_stack_size: z.number(),
  max_queue_size: z.number(),
  max_heap_size: z.number(),
  execution_time: z.number(),
  answer: z.unknown(),
});

export const traceFileSchema = z.object({
  schema_version: z.string(),
  problem: z.string(),
  metadata: metadataSchema,
  input: z.unknown().optional(),
  steps: z.array(stepSchema),
  summary: summarySchema,
});

export type TraceFileParseResult =
  | { success: true; data: z.infer<typeof traceFileSchema> }
  | { success: false; error: string };

export function parseTraceFile(json: unknown): TraceFileParseResult {
  const result = traceFileSchema.safeParse(json);
  if (result.success) {
    return { success: true, data: result.data };
  }
  const issue = result.error.issues[0];
  const path = issue.path.join(".") || "(root)";
  return { success: false, error: `Invalid trace file at "${path}": ${issue.message}` };
}
