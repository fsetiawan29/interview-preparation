import dagre from "@dagrejs/dagre";
import type { GraphEdge, GraphNode } from "@/types/snapshot";

const NODE_SIZE = 56;

/**
 * Deterministic layered layout via dagre — avoids the frame-to-frame
 * jitter a force simulation would produce as the graph redraws on every
 * traversal step during playback.
 */
export function computeGraphLayout(
  nodes: GraphNode[],
  edges: GraphEdge[],
): Map<string, { x: number; y: number }> {
  const g = new dagre.graphlib.Graph();
  g.setGraph({ rankdir: "LR", nodesep: 40, ranksep: 80 });
  g.setDefaultEdgeLabel(() => ({}));

  for (const node of nodes) {
    g.setNode(node.id, { width: NODE_SIZE, height: NODE_SIZE });
  }
  for (const edge of edges) {
    g.setEdge(edge.from, edge.to);
  }

  dagre.layout(g);

  const positions = new Map<string, { x: number; y: number }>();
  for (const node of nodes) {
    const pos = g.node(node.id);
    if (pos) positions.set(node.id, { x: pos.x, y: pos.y });
  }
  return positions;
}
