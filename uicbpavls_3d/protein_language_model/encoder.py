"""Encoder utilities for a frozen ESM-style protein language model."""

from __future__ import annotations

import contextlib
import importlib
from typing import Any

import numpy as np

from .config import ProteinLanguageModelConfig


class ProteinLanguageModelDependencyError(RuntimeError):
    """Raised when optional ML dependencies are installed incorrectly."""


class ProteinLanguageModelHardwareError(RuntimeError):
    """Raised when the configured device is unavailable."""


class FrozenESM2Encoder:
    """Encode protein sequences with a frozen ESM-2 model.

    The actual model dependencies remain optional and are loaded lazily to keep
    ordinary FastAPI installation and existing endpoints unaffected.
    """

    def __init__(self, config: ProteinLanguageModelConfig | None = None):
        self.config = config or ProteinLanguageModelConfig()
        self._torch = None
        self._transformers = None
        self.model = None
        self.tokenizer = None
        self._load_dependencies()
        self._load_model()

    def _load_dependencies(self) -> None:
        try:
            self._torch = importlib.import_module("torch")
        except ModuleNotFoundError as exc:  # pragma: no cover - exercised by runtime env checks.
            raise ProteinLanguageModelDependencyError(
                "Optional protein-language-model dependencies are missing. Install them with: "
                "pip install 'esmith19-uicbpavls-3d[protein-language-model]'"
            ) from exc

        try:
            self._transformers = importlib.import_module("transformers")
        except ModuleNotFoundError as exc:  # pragma: no cover
            raise ProteinLanguageModelDependencyError(
                "The optional 'transformers' dependency is required for ESM-2 inference."
            ) from exc

    def _load_model(self) -> None:
        device = self.config.resolved_device
        if device == "cuda" and not self._torch.cuda.is_available():
            if self.config.allow_gpu:
                raise ProteinLanguageModelHardwareError(
                    "CUDA was requested for ESM-2 inference but no GPU resources are available. "
                    "Set device='cpu' or allow_gpu=False."
                )
            device = "cpu"

        AutoModel = self._transformers.AutoModel
        AutoTokenizer = self._transformers.AutoTokenizer

        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.config.model_name,
                revision=self.config.model_revision,
                cache_dir=self.config.cache_dir,
            )
            self.model = AutoModel.from_pretrained(
                self.config.model_name,
                revision=self.config.model_revision,
                cache_dir=self.config.cache_dir,
            )
        except Exception as exc:  # pragma: no cover - depends on network availability.
            raise ProteinLanguageModelDependencyError(
                "Unable to load the configured ESM-2 checkpoint. Confirm that the model revision is valid "
                "and that the optional ML dependencies are installed."
            ) from exc

        self.model.eval()
        for parameter in self.model.parameters():
            parameter.requires_grad = False

        if device == "cuda":
            self.model.to("cuda")

        if self.config.deterministic:
            with contextlib.suppress(AttributeError):
                self._torch.use_deterministic_algorithms(True)
            if device == "cuda":
                with contextlib.suppress(AttributeError):
                    self._torch.backends.cudnn.deterministic = True
                    self._torch.backends.cudnn.benchmark = False

    def encode_sequence(self, sequence: str) -> list[float]:
        """Encode a single protein sequence to a deterministic embedding vector."""
        if not sequence:
            raise ValueError("Protein sequence cannot be empty.")

        inputs = self.tokenizer(
            sequence,
            return_tensors="pt",
            add_special_tokens=False,
            truncation=True,
            max_length=self.config.max_sequence_length,
        )
        device = self.config.resolved_device
        if device == "cuda" and self._torch.cuda.is_available():
            inputs = {key: value.to("cuda") for key, value in inputs.items()}

        with self._torch.no_grad():
            outputs = self.model(**inputs)
            hidden = outputs.last_hidden_state
            embedding = hidden[0].mean(dim=0).cpu().numpy().astype(float)

        if embedding.size == 0:
            raise ProteinLanguageModelHardwareError("Model produced an empty embedding vector.")

        return embedding.tolist()
