import { Handle, Position, type NodeProps, type Node } from "@xyflow/react";
import { cn } from "@/lib/utils";

export type CircleNodeData = {
  label: string;
  state: "default" | "current" | "visited";
  orientation: "vertical" | "horizontal";
};
export type CircleNode = Node<CircleNodeData, "circle">;

export function CircleNode({ data }: NodeProps<CircleNode>) {
  const [targetPos, sourcePos] =
    data.orientation === "horizontal" ? [Position.Left, Position.Right] : [Position.Top, Position.Bottom];

  return (
    <div
      className={cn(
        "flex h-12 w-12 items-center justify-center rounded-full border bg-card font-mono text-sm ring-1 ring-foreground/10",
        data.state === "visited" && "border-primary/50 bg-primary/5",
        data.state === "current" && "border-primary bg-primary/10 font-semibold",
      )}
    >
      <Handle type="target" position={targetPos} className="opacity-0" />
      {data.label}
      <Handle type="source" position={sourcePos} className="opacity-0" />
    </div>
  );
}
