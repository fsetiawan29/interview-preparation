import { Slider } from "@/components/ui/slider";

export function TimelineSlider({
  index,
  max,
  onChange,
}: {
  index: number;
  max: number;
  onChange: (index: number) => void;
}) {
  return (
    <div className="flex flex-1 items-center gap-3">
      <span className="w-16 shrink-0 font-mono text-xs text-muted-foreground">
        {index + 1} / {max + 1}
      </span>
      <Slider
        value={[index]}
        min={0}
        max={max}
        step={1}
        onValueChange={([value]) => onChange(value)}
        aria-label="Timeline position"
      />
    </div>
  );
}
