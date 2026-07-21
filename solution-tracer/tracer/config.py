"""Runtime configuration for :class:`tracer.recorder.TraceRecorder`."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class TracerConfig:
    #: Use the optional `rich` library for console output when it is installed.
    use_rich: bool = True
    #: Number of decimal places used when rendering execution time.
    time_precision: int = 6
