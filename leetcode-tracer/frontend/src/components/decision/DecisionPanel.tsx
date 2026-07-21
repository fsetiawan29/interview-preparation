import { Check, X } from "lucide-react";
import type { Decision } from "@/types/trace";
import { Card, CardHeader, CardTitle, CardAction, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

export function DecisionPanel({ decision, onClose }: { decision: Decision | null; onClose?: () => void }) {
  return (
    <Card className="flex h-full flex-col gap-0 py-0">
      <CardHeader className="border-b py-3">
        <CardTitle>Decision</CardTitle>
        {onClose && (
          <CardAction>
            <Button variant="ghost" size="icon-xs" onClick={onClose} aria-label="Hide decision panel">
              <X />
            </Button>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto p-3">
        {!decision ? (
          <p className="text-sm text-muted-foreground">No decision at this step</p>
        ) : (
          <div className="flex flex-col gap-3">
            <div>
              <p className="text-xs text-muted-foreground">Condition</p>
              <p className="font-mono text-sm">{decision.condition}</p>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Result</p>
              <Badge variant={decision.result ? "default" : "secondary"} className="gap-1">
                {decision.result ? <Check className="h-3 w-3" /> : <X className="h-3 w-3" />}
                {decision.result ? "TRUE" : "FALSE"}
              </Badge>
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Action</p>
              <p className="text-sm">{decision.action}</p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
