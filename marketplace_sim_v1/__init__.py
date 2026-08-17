"""Importable public interface for the marketplace simulator.

Importing this package has no side effects. Call :func:`run_simulation` to
build a structured result, optionally with a deterministic seed.
"""

from .simulator import SimulationResult, run_simulation

__all__ = ["SimulationResult", "run_simulation"]

