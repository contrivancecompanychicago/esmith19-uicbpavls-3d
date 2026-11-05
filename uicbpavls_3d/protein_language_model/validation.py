"""Sequence validation utilities for M1F protein language model research."""

from __future__ import annotations

from .schemas import SequenceValidationResult

VALID_AMINO_ACIDS = set("ACDEFGHIKLMNPQRSTVWY")


def validate_protein_sequence(sequence: str, *, max_length: int = 1022) -> SequenceValidationResult:
    """Validate a protein sequence against the supported residue alphabet.

    The module intentionally does not allow ambiguous or unsupported residues such
    as B, J, O, U, X, or Z. This keeps the inference stack explicit and prevents
    ambiguous model inputs from being treated as valid data.
    """
    if not isinstance(sequence, str):
        raise TypeError("Protein sequence must be provided as a string.")

    if not sequence or not sequence.strip():
        raise ValueError("Protein sequence cannot be empty.")

    cleaned = "".join(char.upper() for char in sequence if char.isalpha())
    if not cleaned:
        raise ValueError("Protein sequence does not contain any amino-acid letters.")

    unsupported = sorted({char for char in cleaned if char not in VALID_AMINO_ACIDS})
    if unsupported:
        raise ValueError(
            "Unsupported residues detected in protein sequence: "
            + ", ".join(unsupported)
            + ". Supported residues: A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y."
        )

    if len(cleaned) > max_length:
        raise ValueError(
            f"Protein sequence length {len(cleaned)} exceeds the supported maximum of {max_length} residues."
        )

    return SequenceValidationResult(
        sequence=sequence,
        normalized_sequence=cleaned,
        is_valid=True,
        unsupported_residues=[],
        warnings=[],
        length=len(cleaned),
        max_length=max_length,
        metadata={"alphabet": "standard_aa_20", "length_limit": max_length},
    )
