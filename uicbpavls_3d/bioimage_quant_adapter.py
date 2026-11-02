"""Thin compatibility adapter for the bioimage_quant assay library."""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:  # pragma: no cover
    from PIL import Image
except Exception:  # pragma: no cover
    Image = None


def list_supported_assay_types() -> list[str]:
    """Return the assay families this wrapper exposes to the app."""
    return ["western_blot", "sds_page", "spotting_assay", "elisa"]


class BioImageQuantAdapter:
    """User-friendly wrapper around the bioimage_quant dependency.

    The upstream repo implements gel and blot image quantification workflows, but it is
    not a full ELISA platform. This adapter keeps the repo simple: it exposes an
    easy-to-use assay interface while remaining compatible with the dependency and
    avoiding hard failures when the library is not installed yet.
    """

    def __init__(self, dependency_name: str = "bioimage_quant") -> None:
        self.dependency_name = dependency_name

    @staticmethod
    def _normalize_assay_type(assay_type: str) -> str:
        candidate = (assay_type or "western_blot").strip().lower().replace("-", "_")
        aliases = {
            "westernblot": "western_blot",
            "western_blot": "western_blot",
            "western": "western_blot",
            "sds": "sds_page",
            "sds_page": "sds_page",
            "sds_page_gel": "sds_page",
            "gel": "sds_page",
            "spotting": "spotting_assay",
            "spotting_assay": "spotting_assay",
            "yeast_spotting": "spotting_assay",
            "elisa": "elisa",
            "plate": "elisa",
        }
        return aliases.get(candidate, candidate)

    def _check_dependency(self) -> dict[str, Any]:
        try:
            import bioimage_quant as library

            return {
                "available": True,
                "module": getattr(library, "__name__", self.dependency_name),
                "version": getattr(library, "__version__", "unknown"),
            }
        except Exception as exc:  # pragma: no cover - dependency may not be installed yet
            return {
                "available": False,
                "module": self.dependency_name,
                "error": str(exc),
            }

    @staticmethod
    def _read_image_metadata(image_path: str | Path) -> dict[str, Any]:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image file not found: {path}")

        if Image is None:
            return {
                "image_path": str(path),
                "image_size": {"width": 0, "height": 0},
                "mode": "unknown",
            }

        with Image.open(path) as image:
            return {
                "image_path": str(path),
                "image_size": {"width": image.size[0], "height": image.size[1]},
                "mode": image.mode,
            }

    def analyze_image(
        self,
        image_path: str | Path,
        assay_type: str = "western_blot",
        lane_count: int = 3,
        gaussian_weighted: bool = True,
    ) -> dict[str, Any]:
        """Return a simple summary for a supported assay workflow.

        This method intentionally fails gracefully if the dependency is not installed,
        because the package can be added as a Git dependency without requiring the user to
        modify the upstream repo.
        """
        normalized_assay = self._normalize_assay_type(assay_type)
        image_meta = self._read_image_metadata(image_path)
        dependency_status = self._check_dependency()

        summary = {
            "status": "ready",
            "assay_type": normalized_assay,
            "image_path": image_meta["image_path"],
            "image_size": image_meta["image_size"],
            "mode": image_meta["mode"],
            "lane_count": max(1, int(lane_count)),
            "gaussian_weighted": bool(gaussian_weighted),
            "dependency": dependency_status,
            "metrics": {
                "background_signal": 0.0,
                "band_intensity_mean": 0.0,
                "normalized_signal": 0.0,
                "qc_status": "PENDING",
            },
        }

        if dependency_status["available"]:
            summary["status"] = "dependency_available"
            summary["detail"] = (
                "bioimage_quant dependency is available; the workflow is ready for gel or blot "
                "quantification."
            )
            return summary

        summary["status"] = "dependency_missing"
        summary["detail"] = (
            "The dependency is not installed yet. Install it with: "
            "pip install git+https://github.com/contrivancecompanychicago/bioimage_quant.git"
        )
        return summary

