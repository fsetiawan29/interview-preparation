import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";
import type { LinkedListSnapshot } from "@/types/snapshot";
import { cn } from "@/lib/utils";

export function LinkedListViewer({ snapshot }: { snapshot: LinkedListSnapshot }) {
  const { nodes, current } = snapshot;

  return (
    <div className="flex flex-wrap items-center justify-center gap-2 p-6">
      {nodes.map((node, index) => (
        <div key={node.id} className="flex items-center gap-2">
          <motion.div
            layout
            className={cn(
              "flex h-12 w-12 items-center justify-center rounded-full border bg-card font-mono text-sm ring-1 ring-foreground/10",
              node.id === current && "border-primary bg-primary/10 font-semibold",
            )}
          >
            {String(node.val)}
          </motion.div>
          {(node.next !== null || index < nodes.length - 1) && (
            <ArrowRight className="h-4 w-4 text-muted-foreground" />
          )}
        </div>
      ))}
      <span className="font-mono text-sm text-muted-foreground">None</span>
      {nodes.length === 0 && <p className="text-sm text-muted-foreground">Empty list</p>}
    </div>
  );
}
