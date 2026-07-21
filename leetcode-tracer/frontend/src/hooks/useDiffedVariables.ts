import { useMemo } from "react";

export interface DiffedVariable {
  name: string;
  value: unknown;
  changed: boolean;
}

/** Pairs each variable in `current` with whether it changed from `previous`. */
export function useDiffedVariables(
  current: Record<string, unknown>,
  previous: Record<string, unknown> | undefined,
): DiffedVariable[] {
  return useMemo(() => {
    return Object.entries(current).map(([name, value]) => ({
      name,
      value,
      changed: previous ? !Object.is(stringify(previous[name]), stringify(value)) : false,
    }));
  }, [current, previous]);
}

function stringify(value: unknown): string {
  try {
    return JSON.stringify(value);
  } catch {
    return String(value);
  }
}
