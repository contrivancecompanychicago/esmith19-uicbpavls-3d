"""Tests for the isolated protein-language model module."""

from __future__ import annotations

import pytest

from uicbpavls_3d.protein_language_model import ProteinLanguageModelAdapter
from uicbpavls_3d.protein_language_model.config import ProteinLanguageModelConfig
from uicbpavls_3d.protein_language_model.validation import validate_protein_sequence


class MockEncoder:
    def __init__(self):
        self.model = object()

    def encode_sequence(self, sequence: str):
        assert sequence
        return [0.1, 0.2, 0.3]


def test_validate_protein_sequence_accepts_standard_amino_acids() -> None:
    result = validate_protein_sequence("MKTAYIA")
    assert result.is_valid is True
    assert result.normalized_sequence == "MKTAYIA"
    assert result.length == 7


def test_validate_protein_sequence_rejects_unsupported_residues() -> None:
    with pytest.raises(ValueError, match="Unsupported residues"):
        validate_protein_sequence("MKTAXY")


def test_validate_protein_sequence_rejects_oversized_sequence() -> None:
    with pytest.raises(ValueError, match="exceeds the supported maximum"):
        validate_protein_sequence("A" * 1023)


def test_adapter_uses_mock_encoder() -> None:
    adapter = ProteinLanguageModelAdapter(
        config=ProteinLanguageModelConfig(model_name="mock-model", model_revision="test", device="cpu"),
        encoder=MockEncoder(),
    )

    result = adapter.encode("MKTAYIA")
    assert result.embedding_dimension == 3
    assert result.model_name == "mock-model"
    assert result.sequence == "MKTAYIA"


def test_adapter_rejects_empty_sequence() -> None:
    adapter = ProteinLanguageModelAdapter(
        config=ProteinLanguageModelConfig(model_name="mock-model", model_revision="test", device="cpu"),
        encoder=MockEncoder(),
    )

    with pytest.raises(ValueError, match="cannot be empty"):
        adapter.encode("   ")
