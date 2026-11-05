"""QC checks for M1F protein-language-model outputs."""

from __future__ import annotations

from typing import Sequence

import numpy as np


def evaluate_embedding_qc(embedding: Sequence[float], *, min_dimension: int = 1) -> dict[str, object]:
    """Run a lightweight QC pass over model embeddings."""
    array = np.asarray(embedding, dtype=float)
    if array.ndim != 1:
        raise ValueError("Embedding must be a one-dimensional vector.")
    if array.size < min_dimension:
        raise ValueError(f"Embedding is too small: expected at least {min_dimension} entries.")

    finite = np.isfinite(array)
    if not bool(finite.all()):
        return {"passes": False, "reason": "embedding_contains_non_finite_values"}

    return {
        "passes": True,
        "embedding_dimension": int(array.size),
        "mean": float(array.mean()),
        "std": float(array.std()),
        "min": float(array.min()),
        "max": float(array.max()),
    }
