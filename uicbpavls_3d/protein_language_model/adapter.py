"""Adapter runtime for the M1F protein language model module."""

from __future__ import annotations

from typing import Any, Iterable

from .config import DEFAULT_PROTEIN_LANGUAGE_MODEL_CONFIG, ProteinLanguageModelConfig
from .embedding import summarize_embedding
from .encoder import FrozenESM2Encoder, ProteinLanguageModelDependencyError
from .qc import evaluate_embedding_qc
from .schemas import EmbeddingResult, ProteinSequenceRecord
from .validation import validate_protein_sequence


class ProteinLanguageModelAdapter:
    """Simple adapter with isolated model inference and deterministic configuration."""

    def __init__(self, config: ProteinLanguageModelConfig | None = None, encoder: FrozenESM2Encoder | None = None):
        self.config = config or DEFAULT_PROTEIN_LANGUAGE_MODEL_CONFIG
        self.encoder = encoder or FrozenESM2Encoder(self.config)

    def is_available(self) -> bool:
        """Return True when the model backend can run inference."""
        try:
            return self.encoder is not None and self.encoder.model is not None
        except ProteinLanguageModelDependencyError:
            return False

    def encode(
        self,
        sequence: str,
        *,
        protein_name: str | None = None,
        accession: str | None = None,
        species: str | None = None,
        isoform: str | None = None,
        source: str | None = None,
        retrieval_version: str | None = None,
    ) -> EmbeddingResult:
        validation = validate_protein_sequence(sequence, max_length=self.config.max_sequence_length)
        embedding = self.encoder.encode_sequence(validation.normalized_sequence)
        qc = evaluate_embedding_qc(embedding)
        if not qc["passes"]:
            raise ValueError(f"Embedding QC failed: {qc['reason']}")

        summary = summarize_embedding(embedding)
        provenance = {
            "model_name": self.config.model_name,
            "model_revision": self.config.model_revision,
            "sequence_metadata": self.config.sequence_metadata,
            "retrieval_version": retrieval_version or "not_recorded",
            "source": source or "documented_protein_database",
            "classification": self.config.data_classification,
        }

        return EmbeddingResult(
            protein_name=protein_name,
            accession=accession,
            species=species,
            isoform=isoform,
            source=source,
            retrieval_version=retrieval_version,
            sequence=validation.normalized_sequence,
            sequence_length=validation.length,
            model_name=self.config.model_name,
            model_revision=self.config.model_revision,
            embedding=embedding,
            embedding_dimension=len(embedding),
            inference_device=self.config.resolved_device,
            inference_settings={
                "device": self.config.resolved_device,
                "allow_gpu": self.config.allow_gpu,
                "batch_size": self.config.batch_size,
                "deterministic": self.config.deterministic,
                "max_sequence_length": self.config.max_sequence_length,
            },
            data_classification=self.config.data_classification,
            provenance={
                **provenance,
                "summary": summary,
                "qc": qc,
            },
        )

    def encode_records(self, records: Iterable[ProteinSequenceRecord]) -> list[EmbeddingResult]:
        """Encode a batch of protein records while keeping the process isolated."""
        return [
            self.encode(
                record.sequence,
                protein_name=record.protein_name,
                accession=record.accession,
                species=record.species,
                isoform=record.isoform,
                source=record.source,
                retrieval_version=record.retrieval_version,
            )
            for record in records
        ]
