"""Schemas for sequence validation and embedding results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SequenceValidationResult:
    sequence: str
    normalized_sequence: str
    is_valid: bool
    unsupported_residues: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    length: int = 0
    max_length: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ProteinSequenceRecord:
    accession: str | None = None
    species: str | None = None
    isoform: str | None = None
    source: str | None = None
    retrieval_version: str | None = None
    protein_name: str | None = None
    sequence: str = ""


@dataclass(frozen=True)
class EmbeddingResult:
    protein_name: str | None
    accession: str | None
    species: str | None
    isoform: str | None
    source: str | None
    retrieval_version: str | None
    sequence: str
    sequence_length: int
    model_name: str
    model_revision: str
    embedding: list[float]
    embedding_dimension: int
    inference_device: str
    inference_settings: dict[str, Any]
    data_classification: str = "sequence_embedding"
    provenance: dict[str, Any] = field(default_factory=dict)
