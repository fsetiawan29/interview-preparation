import { AnimatePresence, motion } from "framer-motion";
import type { StackSnapshot } from "@/types/snapshot";
import { cn } from "@/lib/utils";

export function StackViewer({ snapshot }: { snapshot: StackSnapshot }) {
  const { values, highlights = [] } = snapshot;
  const topIndex = values.length - 1;

  return (
    <div className="flex flex-col items-center gap-2 p-6">
      <span className="text-xs text-muted-foreground">Top</span>
      <div className="flex flex-col-reverse gap-1">
        <AnimatePresence initial={false}>
          {values.map((value, index) => (
            <motion.div
              key={`${index}-${String(value)}`}
              layout
              initial={{ opacity: 0, y: -12 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -12 }}
              className={cn(
                "flex h-10 w-28 items-center justify-center rounded-md border bg-card font-mono text-sm ring-1 ring-foreground/10",
                index === topIndex && "border-primary bg-primary/10 font-semibold",
                highlights.includes(index) && "border-primary bg-primary/10 font-semibold",
              )}
            >
              {String(value)}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      {values.length === 0 && <p className="text-sm text-muted-foreground">Empty stack</p>}
    </div>
  );
}
