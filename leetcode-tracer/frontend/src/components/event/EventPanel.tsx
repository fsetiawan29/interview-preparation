import { Sparkles, X } from "lucide-react";
import { Card, CardHeader, CardTitle, CardAction, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export function EventPanel({ events, onClose }: { events: string[]; onClose?: () => void }) {
  return (
    <Card className="gap-0 py-0">
      <CardHeader className="border-b py-3">
        <CardTitle>Events</CardTitle>
        {onClose && (
          <CardAction>
            <Button variant="ghost" size="icon-xs" onClick={onClose} aria-label="Hide events panel">
              <X />
            </Button>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className="p-3">
        {events.length === 0 ? (
          <p className="text-sm text-muted-foreground">No events at this step</p>
        ) : (
          <ul className="flex flex-wrap gap-2">
            {events.map((event, index) => (
              <li
                key={index}
                className="flex items-center gap-1.5 rounded-full border bg-card px-2.5 py-1 text-xs"
              >
                <Sparkles className="h-3 w-3 text-primary" />
                {event}
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}
