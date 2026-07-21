import type { Snapshot } from "@/types/snapshot";
import { getViewer } from "@/utils/viewerRegistry";
import { Card } from "@/components/ui/card";

export function VisualizationArea({ snapshot }: { snapshot: Snapshot | null }) {
  const Viewer = snapshot ? getViewer(snapshot.type) : undefined;

  return (
    <Card className="flex h-full min-h-96 items-center justify-center overflow-hidden p-0">
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
