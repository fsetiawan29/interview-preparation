import { useEffect, useRef } from "react";
import { X } from "lucide-react";
import type { Step } from "@/types/trace";
import { Card, CardHeader, CardTitle, CardAction, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { TimelineItem } from "./TimelineItem";

export function TimelinePanel({
  steps,
  currentIndex,
  onSelect,
  onClose,
}: {
  steps: Step[];
  currentIndex: number;
  onSelect: (index: number) => void;
  onClose?: () => void;
}) {
  const activeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    activeRef.current?.scrollIntoView({ block: "nearest" });
  }, [currentIndex]);

  return (
    <Card className="flex h-full flex-col gap-0 py-0">
      <CardHeader className="border-b py-3">
        <CardTitle>Timeline</CardTitle>
        {onClose && (
          <CardAction>
            <Button variant="ghost" size="icon-xs" onClick={onClose} aria-label="Hide timeline panel">
              <X />
            </Button>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto p-2">
        <div className="flex flex-col gap-0.5">
          {steps.map((step, index) => (
            <div key={step.id} ref={index === currentIndex ? activeRef : undefined}>
              <TimelineItem step={step} isCurrent={index === currentIndex} onClick={() => onSelect(index)} />
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
