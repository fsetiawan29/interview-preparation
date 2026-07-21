import { ChevronDown } from "lucide-react";
import type { SampleTrace } from "@/data/sampleTraces";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";

export function SampleTraceMenu({
  samples,
  onSelect,
}: {
  samples: SampleTrace[];
  onSelect: (sample: SampleTrace) => void;
}) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="secondary">
          Try a sample trace
          <ChevronDown />
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="center">
        {samples.map((sample) => (
          <DropdownMenuItem key={sample.id} onSelect={() => onSelect(sample)}>
            <span className="flex-1">{sample.label}</span>
            <span className="text-xs text-muted-foreground">{sample.snapshotType}</span>
          </DropdownMenuItem>
        ))}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
