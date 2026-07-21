import type { TreeNode } from "@/types/snapshot";

const NODE_SPACING = 72;
const LEVEL_HEIGHT = 96;

/**
 * In-order slot placement: cheap, deterministic, and overlap-free for
 * LeetCode-sized binary trees (Reingold-Tilford is overkill at this scale).
 * Assumes the tree's root is always id 0, which the tracer SDK guarantees.
 */
export function computeTreeLayout(nodes: TreeNode[]): Map<number, { x: number; y: number }> {
  const byId = new Map(nodes.map((n) => [n.id, n]));
  const positions = new Map<number, { x: number; y: number }>();
  let slot = 0;

  function visit(id: number | null, depth: number) {
    if (id === null) return;
    const node = byId.get(id);
    if (!node) return;
    visit(node.left, depth + 1);
    positions.set(id, { x: slot * NODE_SPACING, y: depth * LEVEL_HEIGHT });
    slot += 1;
    visit(node.right, depth + 1);
  }

  if (nodes.length > 0) visit(0, 0);
  return positions;
}
