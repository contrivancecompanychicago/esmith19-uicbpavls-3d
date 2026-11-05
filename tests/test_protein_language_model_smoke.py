"""Optional smoke test for pretrained ESM-2 inference."""

from __future__ import annotations

import os

import pytest

from uicbpavls_3d.protein_language_model import ProteinLanguageModelAdapter


@pytest.mark.skipif(
    not os.environ.get("UICBPAVLS_ENABLE_M1F_SMOKE_TEST"),
    reason="Set UICBPAVLS_ENABLE_M1F_SMOKE_TEST=1 to run the optional pretrained-model smoke test.",
)
def test_pretrained_esm2_smoke() -> None:
    adapter = ProteinLanguageModelAdapter()
    if not adapter.is_available():
        pytest.skip("Optional protein-language-model dependencies are not installed.")

    result = adapter.encode("MKTAYIAFVSLLGCLLQTLQGKNQEKLVRLFRK")
    assert result.embedding_dimension > 0
    assert len(result.embedding) == result.embedding_dimension
    assert result.model_name
