import { Sparkles } from "lucide-react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";

export function EventPanel({ events }: { events: string[] }) {
  return (
    <Card className="gap-0 py-0">
      <CardHeader className="border-b py-3">
        <CardTitle>Events</CardTitle>
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
