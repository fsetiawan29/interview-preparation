import { X } from "lucide-react";
import type { Snapshot } from "@/types/snapshot";
import { getViewer } from "@/utils/viewerRegistry";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function VisualizationArea({
  snapshot,
  onClose,
}: {
  snapshot: Snapshot | null;
  onClose?: () => void;
}) {
  const Viewer = snapshot ? getViewer(snapshot.type) : undefined;

  return (
    <Card className="relative flex h-full min-h-96 items-center justify-center overflow-hidden p-0">
      {onClose && (
        <Button
          variant="ghost"
          size="icon-xs"
          className="absolute top-2 right-2 z-10"
          onClick={onClose}
          aria-label="Hide visualization panel"
        >
          <X />
        </Button>
      )}
      {!snapshot && <p className="text-sm text-muted-foreground">No visualization for this step</p>}
      {snapshot && !Viewer && (
        <p className="text-sm text-muted-foreground">No viewer registered for type "{snapshot.type}" yet</p>
      )}
      {snapshot && Viewer && (
        <div className="h-full w-full">
          <Viewer snapshot={snapshot} />
        </div>
      )}
    </Card>
  );
}
