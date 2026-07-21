import { useMemo } from "react";
import { ReactFlow, Background, type Edge, type NodeTypes } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { TreeSnapshot } from "@/types/snapshot";
import { computeTreeLayout } from "@/utils/treeLayout";
import { CircleNode, type CircleNode as CircleNodeT } from "./CircleNode";

const nodeTypes: NodeTypes = { circle: CircleNode };

export function TreeViewer({ snapshot }: { snapshot: TreeSnapshot }) {
  const { nodes: treeNodes, edges: treeEdges, current, visited = [] } = snapshot;

  const { flowNodes, flowEdges } = useMemo(() => {
    const positions = computeTreeLayout(treeNodes);

    const flowNodes: CircleNodeT[] = treeNodes.map((node) => ({
      id: String(node.id),
      type: "circle",
      position: positions.get(node.id) ?? { x: 0, y: 0 },
      data: {
        label: String(node.val),
        orientation: "vertical",
        state: node.id === current ? "current" : visited.includes(node.id) ? "visited" : "default",
      },
      draggable: false,
    }));

    const flowEdges: Edge[] = treeEdges.map((edge) => ({
      id: `${edge.from}-${edge.to}`,
      source: String(edge.from),
      target: String(edge.to),
    }));

    return { flowNodes, flowEdges };
  }, [snapshot]);

  if (treeNodes.length === 0) {
    return <p className="p-6 text-center text-sm text-muted-foreground">Empty tree</p>;
  }

  return (
    <div className="h-full min-h-80 w-full">
      <ReactFlow nodes={flowNodes} edges={flowEdges} nodeTypes={nodeTypes} fitView proOptions={{ hideAttribution: true }}>
        <Background />
      </ReactFlow>
    </div>
  );
}
