"""Embedding summaries and QC utilities for protein embeddings."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def summarize_embedding(embedding: Sequence[float]) -> dict[str, float]:
    """Return summary statistics for the embedding vector."""
    array = np.asarray(embedding, dtype=float)
    if array.ndim == 0 or array.size == 0:
        raise ValueError("Embedding must contain at least one value.")
    return {
        "mean": float(array.mean()),
        "std": float(array.std()),
        "min": float(array.min()),
        "max": float(array.max()),
        "norm_l2": float(np.linalg.norm(array)),
    }
