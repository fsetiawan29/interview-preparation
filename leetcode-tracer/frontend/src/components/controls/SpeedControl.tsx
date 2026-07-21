import { SPEED_OPTIONS, type Speed } from "@/stores/playbackStore";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function SpeedControl({ speed, onChange }: { speed: Speed; onChange: (speed: Speed) => void }) {
  return (
    <div className="flex items-center gap-1 rounded-md border p-0.5">
      {SPEED_OPTIONS.map((option) => (
        <Button
          key={option}
          type="button"
          size="sm"
          variant="ghost"
          onClick={() => onChange(option)}
          className={cn(
            "h-7 px-2 text-xs",
            option === speed && "bg-accent font-semibold text-accent-foreground",
          )}
        >
          {option}x
        </Button>
      ))}
    </div>
  );
}
