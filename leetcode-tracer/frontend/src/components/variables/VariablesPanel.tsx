import { X } from "lucide-react";
import { useDiffedVariables } from "@/hooks/useDiffedVariables";
import { Card, CardHeader, CardTitle, CardAction, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Table, TableBody } from "@/components/ui/table";
import { VariableRow } from "./VariableRow";

export function VariablesPanel({
  current,
  previous,
  onClose,
}: {
  current: Record<string, unknown>;
  previous?: Record<string, unknown>;
  onClose?: () => void;
}) {
  const variables = useDiffedVariables(current, previous);

  return (
    <Card className="flex h-full flex-col gap-0 py-0">
      <CardHeader className="border-b py-3">
        <CardTitle>Variables</CardTitle>
        {onClose && (
          <CardAction>
            <Button variant="ghost" size="icon-xs" onClick={onClose} aria-label="Hide variables panel">
              <X />
            </Button>
          </CardAction>
        )}
      </CardHeader>
      <CardContent className="flex-1 overflow-y-auto p-2">
        {variables.length === 0 ? (
          <p className="p-2 text-sm text-muted-foreground">No variables at this step</p>
        ) : (
          <Table>
            <TableBody>
              {variables.map((variable) => (
                <VariableRow key={variable.name} variable={variable} />
              ))}
            </TableBody>
          </Table>
        )}
      </CardContent>
    </Card>
  );
}
