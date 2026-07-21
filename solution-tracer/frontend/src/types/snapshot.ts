export interface ArraySnapshot {
  type: "array";
  values: unknown[];
  highlights?: number[];
  pointers?: Record<string, number>;
}

export interface StackSnapshot {
  type: "stack";
  values: unknown[];
  highlights?: number[];
}

export interface QueueSnapshot {
  type: "queue";
  values: unknown[];
  highlights?: number[];
}

export interface HeapSnapshot {
  type: "heap";
  values: unknown[];
  highlights?: number[];
}

export interface TreeNode {
  id: number;
  val: unknown;
  left: number | null;
  right: number | null;
}

export interface TreeEdge {
  from: number;
  to: number;
}

export interface TreeSnapshot {
  type: "tree";
  nodes: TreeNode[];
  edges: TreeEdge[];
  current?: number | null;
  visited?: number[];
}

export interface GraphNode {
  id: string;
  label: string;
}

export interface GraphEdge {
  from: string;
  to: string;
}

export interface GraphSnapshot {
  type: "graph";
  nodes: GraphNode[];
  edges: GraphEdge[];
  current?: string | null;
  visited?: string[];
}

export interface LinkedListNode {
  id: number;
  val: unknown;
  next: number | null;
}

export interface LinkedListSnapshot {
  type: "linked-list";
  nodes: LinkedListNode[];
  current?: number | null;
}

export type Snapshot =
  | ArraySnapshot
  | StackSnapshot
  | QueueSnapshot
  | HeapSnapshot
  | TreeSnapshot
  | GraphSnapshot
  | LinkedListSnapshot;

export type SnapshotType = Snapshot["type"];
