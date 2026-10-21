"""Compatibility package for the lab modules.

This package keeps the original repository layout and allows the project to be
installed as a proper Python package while preserving import paths used by the
existing simulation modules.
"""

from .assay import virtual_fructosamine_assay
from .config import *
from .glycation import simulate_glycation
from .qc import evaluate_qc, run_qc_pipeline

__all__ = [
    "virtual_fructosamine_assay",
    "simulate_glycation",
    "evaluate_qc",
    "run_qc_pipeline",
]
