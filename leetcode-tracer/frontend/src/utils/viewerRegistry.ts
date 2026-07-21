import type { ComponentType } from "react";
import type { Snapshot, SnapshotType } from "@/types/snapshot";

type ViewerComponent<T extends Snapshot = Snapshot> = ComponentType<{ snapshot: T }>;

const registry = new Map<SnapshotType, ViewerComponent<never>>();

export function registerViewer<T extends SnapshotType>(
  type: T,
  component: ViewerComponent<Extract<Snapshot, { type: T }>>,
): void {
  registry.set(type, component as ViewerComponent<never>);
}

export function getViewer(type: SnapshotType): ViewerComponent | undefined {
  return registry.get(type) as ViewerComponent | undefined;
}
