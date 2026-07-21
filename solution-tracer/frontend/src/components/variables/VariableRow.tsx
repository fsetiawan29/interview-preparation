import { motion } from "framer-motion";
import type { DiffedVariable } from "@/hooks/useDiffedVariables";
import { TableRow, TableCell } from "@/components/ui/table";

function formatValue(value: unknown): string {
  if (typeof value === "string") return value;
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}

export function VariableRow({ variable }: { variable: DiffedVariable }) {
  return (
    <TableRow>
      <TableCell className="font-mono text-sm text-muted-foreground">{variable.name}</TableCell>
      <TableCell className="font-mono text-sm">
        <motion.span
          key={formatValue(variable.value)}
          initial={variable.changed ? { opacity: 0, y: -4 } : false}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.2 }}
          className={variable.changed ? "rounded bg-primary/10 px-1 font-semibold text-primary" : undefined}
        >
          {formatValue(variable.value)}
        </motion.span>
      </TableCell>
    </TableRow>
  );
}
