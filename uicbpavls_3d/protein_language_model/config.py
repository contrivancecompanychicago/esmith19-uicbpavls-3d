"""Configuration for the isolated M1F protein language modeling module."""

from __future__ import annotations

from dataclasses import dataclass, field

DEFAULT_MODEL_NAME = "facebook/esm2_t6_8M_UR50D"
DEFAULT_MODEL_REVISION = "main"
DEFAULT_MAX_SEQUENCE_LENGTH = 1022
DEFAULT_EMBEDDING_DIMENSION = 320


@dataclass(frozen=True)
class ProteinLanguageModelConfig:
    """Runtime settings for a frozen ESM-style protein embedding model.

    The design keeps all model inference isolated from request handling and keeps
    the heavy ML dependencies optional. For production deployment, pin the upstream
    revision string to a specific release commit before running research workloads.
    """

    model_name: str = DEFAULT_MODEL_NAME
    model_revision: str = DEFAULT_MODEL_REVISION
    device: str = "cpu"
    allow_gpu: bool = True
    batch_size: int = 1
    max_sequence_length: int = DEFAULT_MAX_SEQUENCE_LENGTH
    embedding_dimension: int = DEFAULT_EMBEDDING_DIMENSION
    deterministic: bool = True
    cache_dir: str | None = None
    local_model_path: str | None = None
    inference_label: str = "frozen_esm2"
    data_classification: str = "sequence_embedding"
    sequence_metadata: dict[str, str] = field(default_factory=dict)

    @property
    def resolved_device(self) -> str:
        """Return the device to use for inference."""
        return "cuda" if self.device.lower() == "cuda" else "cpu"

    @property
    def model_identifier(self) -> str:
        """Return the model identifier, including revision when configured."""
        if self.model_revision:
            return f"{self.model_name}@{self.model_revision}"
        return self.model_name


DEFAULT_PROTEIN_LANGUAGE_MODEL_CONFIG = ProteinLanguageModelConfig()
