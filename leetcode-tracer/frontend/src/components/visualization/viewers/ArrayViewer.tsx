import { motion } from "framer-motion";
import type { ArraySnapshot } from "@/types/snapshot";
import { cn } from "@/lib/utils";

export function ArrayViewer({ snapshot }: { snapshot: ArraySnapshot }) {
  const { values, highlights = [], pointers = {} } = snapshot;

  const pointersByIndex = new Map<number, string[]>();
  for (const [label, index] of Object.entries(pointers)) {
    pointersByIndex.set(index, [...(pointersByIndex.get(index) ?? []), label]);
  }

  return (
    <div className="flex flex-wrap items-start justify-center gap-1 p-6">
      {values.map((value, index) => (
        <div key={index} className="flex flex-col items-center gap-1">
          <span className="text-xs text-muted-foreground">{index}</span>
          <motion.div
            layout
            className={cn(
              "flex h-12 w-12 items-center justify-center rounded-md border bg-card font-mono text-sm ring-1 ring-foreground/10",
              highlights.includes(index) && "border-primary bg-primary/10 font-semibold",
            )}
          >
            {String(value)}
          </motion.div>
          {pointersByIndex.has(index) && (
            <motion.span
              layout
              className="rounded bg-primary px-1.5 py-0.5 text-xs font-medium text-primary-foreground"
            >
              {pointersByIndex.get(index)!.join("/")}
            </motion.span>
          )}
        </div>
      ))}
      {values.length === 0 && <p className="text-sm text-muted-foreground">Empty array</p>}
    </div>
  );
}
