import { AnimatePresence, motion } from "framer-motion";
import type { QueueSnapshot } from "@/types/snapshot";
import { cn } from "@/lib/utils";

export function QueueViewer({ snapshot }: { snapshot: QueueSnapshot }) {
  const { values, highlights = [] } = snapshot;

  return (
    <div className="flex flex-col items-center gap-2 p-6">
      <span className="text-xs text-muted-foreground">Front</span>
      <div className="flex gap-1">
        <AnimatePresence initial={false}>
          {values.map((value, index) => (
            <motion.div
              key={`${index}-${String(value)}`}
              layout
              initial={{ opacity: 0, x: 16 }}
              animate={{ opacity: 1, x: 0 }}
              exit={{ opacity: 0, x: -16 }}
              className={cn(
                "flex h-10 w-12 items-center justify-center rounded-md border bg-card font-mono text-sm ring-1 ring-foreground/10",
                index === 0 && "border-primary bg-primary/10 font-semibold",
                highlights.includes(index) && "border-primary bg-primary/10 font-semibold",
              )}
            >
              {String(value)}
            </motion.div>
          ))}
        </AnimatePresence>
      </div>
      {values.length === 0 && <p className="text-sm text-muted-foreground">Empty queue</p>}
    </div>
  );
}
