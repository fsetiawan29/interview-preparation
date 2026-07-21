# LeetCode Trace Visualizer

A React app that loads a JSON trace exported by the `leetcode-tracer` Python
SDK and lets you step through / play back an algorithm's execution —
inspecting variables, decisions, and events while watching the underlying
data structure (array, stack, queue, tree, graph, linked list) change at
each step.

This is read-only: it never executes Python. It only renders JSON produced
by `trace.render_json()` / `trace.export_json(path)` (see `../docs/trace-schema.md`
for the contract).

## Setup

```bash
npm install
npm run dev      # start the dev server
npm run build    # type-check and produce a production build
```

## Using it

On load, drag a trace JSON file onto the drop zone, use the file picker, or
pick one of the six bundled sample traces (`src/data/samples/`, regenerated
from `../examples/*.py`) — one for each supported snapshot type.

To visualize a solution of your own, run
`python -m tracer.generate <path/to/solution.py> <method>` from
`leetcode-tracer/` — it works on any unmodified LeetCode-style solution, no
instrumentation needed (see the main [README](../README.md#generating-a-json-trace-for-the-visualizer)),
though without manual `trace.decision`/`event`/`snapshot_*` calls the
Visualization panel stays empty.

Once a trace is loaded:

- **Timeline** (left) — click any step to jump to it.
- **Variables / Decision / Events** — the algorithm's state at the current step.
- **Visualization** (center) — the data structure, driven by the step's
  snapshot (or the last-known snapshot, forward-filled, if the step didn't
  redraw it).
- **Controls** (bottom) — play/pause, step, restart, scrub the timeline
  slider, change speed (0.5x–4x).
- **Keyboard**: Space = play/pause, ←/→ = step, Home/End = first/last step.

## Architecture

- `src/types/` — the trace JSON contract as TypeScript types
  (`trace.ts`, `snapshot.ts`) and a mirrored Zod schema (`traceSchema.ts`)
  used to validate untrusted, drag-and-dropped files at import time.
- `src/stores/` — Zustand: `traceStore` (loaded trace, current step,
  forward-filled snapshots), `playbackStore` (play/pause/speed),
  `themeStore` (light/dark/system, persisted).
- `src/hooks/usePlaybackEngine.ts` — the `setInterval`-driven auto-advance
  loop; mounted once in `App`.
- `src/utils/viewerRegistry.ts` + `src/components/visualization/viewers/` —
  a `registerViewer(type, Component)` registry so the visualization area
  looks up a viewer by the current snapshot's `type` at render time.

### Adding a new visualization type

1. Add the type to the `Snapshot` union in `src/types/snapshot.ts` and to
   `src/types/traceSchema.ts`.
2. Create `src/components/visualization/viewers/YourViewer.tsx`.
3. Register it in `src/components/visualization/viewers/index.ts`:
   ```ts
   registerViewer("your-type", YourViewer);
   ```
   No other file needs to change — `VisualizationArea` picks it up
   automatically, and an unregistered type degrades to a placeholder instead
   of crashing.

## Scope

This is the **Core MVP**: array, stack, queue, tree, graph, and linked-list
viewers (the types the bundled example scripts produce), plus the full
layout/timeline/playback/theme/import shell. Deferred to a follow-up pass:
matrix/heap/trie/union-find viewers, the Monaco code viewer, PNG/Markdown
export, and virtualization for 10k+ step traces (the timeline is already
built as a flat, index-rendered list so swapping in `@tanstack/react-virtual`
later shouldn't require restructuring it).
