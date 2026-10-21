"""
UIC-PAVLS M1A package initialization.

This package exposes the core Part 1 configuration and preflight
components without executing the glycation model or assay workflow.
"""

from .config import (
    PROJECT,
    MODULE,
    BENCH,
    EXPERIMENT,
    PROTOCOL_ID,
    VERSION,
    TRIAL,
    TRIAL_TYPE,
    RUN_STATE,
    DATA_CLASSIFICATION,
    EXECUTION_AUTHORIZED,
    APP_NAME,
    LAB,
    GLUCOSE_LEVELS,
    TIME_POINTS,
    REPLICATES,
)
from .specimens import SPECIMEN
from .controls import CONTROLS
from .manifest import build_sample_manifest
from .qc import run_preflight_qc

__all__ = [
    "PROJECT",
    "MODULE",
    "BENCH",
    "EXPERIMENT",
    "PROTOCOL_ID",
    "VERSION",
    "TRIAL",
    "TRIAL_TYPE",
    "RUN_STATE",
    "DATA_CLASSIFICATION",
    "EXECUTION_AUTHORIZED",
    "APP_NAME",
    "LAB",
    "GLUCOSE_LEVELS",
    "TIME_POINTS",
    "REPLICATES",
    "SPECIMEN",
    "CONTROLS",
    "build_sample_manifest",
    "run_preflight_qc",
]
