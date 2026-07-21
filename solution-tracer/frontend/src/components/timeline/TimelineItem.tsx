import { Circle, CircleDot } from "lucide-react";
import type { Step } from "@/types/trace";
import { cn } from "@/lib/utils";

export function TimelineItem({
  step,
  isCurrent,
  onClick,
}: {
  step: Step;
  isCurrent: boolean;
  onClick: () => void;
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(
        "flex w-full items-center gap-2 rounded-md px-2 py-1.5 text-left text-sm transition-colors hover:bg-accent",
        isCurrent && "bg-accent font-medium text-accent-foreground",
      )}
    >
      {isCurrent ? (
        <CircleDot className="h-3.5 w-3.5 shrink-0 text-primary" />
      ) : (
        <Circle className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
      )}
      <span className="truncate">{step.title}</span>
    </button>
  );
}
