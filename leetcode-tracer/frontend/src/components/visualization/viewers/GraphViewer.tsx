import { useMemo } from "react";
import { ReactFlow, Background, type Edge, type NodeTypes } from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import type { GraphSnapshot } from "@/types/snapshot";
import { computeGraphLayout } from "@/utils/graphLayout";
import { CircleNode, type CircleNode as CircleNodeT } from "./CircleNode";

const nodeTypes: NodeTypes = { circle: CircleNode };

export function GraphViewer({ snapshot }: { snapshot: GraphSnapshot }) {
  const { flowNodes, flowEdges } = useMemo(() => {
    const { nodes: graphNodes, edges: graphEdges, current, visited = [] } = snapshot;
    const positions = computeGraphLayout(graphNodes, graphEdges);

    const flowNodes: CircleNodeT[] = graphNodes.map((node) => ({
      id: node.id,
      type: "circle",
      position: positions.get(node.id) ?? { x: 0, y: 0 },
      data: {
        label: node.label,
        orientation: "horizontal",
        state: node.id === current ? "current" : visited.includes(node.id) ? "visited" : "default",
      },
      draggable: false,
    }));

    const flowEdges: Edge[] = graphEdges.map((edge, index) => ({
      id: `${edge.from}-${edge.to}-${index}`,
      source: edge.from,
      target: edge.to,
    }));

    return { flowNodes, flowEdges };
  }, [snapshot]);

  if (snapshot.nodes.length === 0) {
    return <p className="p-6 text-center text-sm text-muted-foreground">Empty graph</p>;
  }

  return (
    <div className="h-full min-h-80 w-full">
      <ReactFlow nodes={flowNodes} edges={flowEdges} nodeTypes={nodeTypes} fitView proOptions={{ hideAttribution: true }}>
        <Background />
      </ReactFlow>
    </div>
  );
}
