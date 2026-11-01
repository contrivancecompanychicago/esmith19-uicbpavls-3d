"""Image capture support for the microscope adapter."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from ..config import MicroscopeConfig


def _slugify(value: str) -> str:
    return "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value).strip("-").lower() or "sample"


def _write_placeholder_ppm(path: Path, width: int = 320, height: int = 240, sample_id: str = "sample") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = f"P6\n{width} {height}\n255\n".encode("ascii")
    pixels = bytearray()
    for y in range(height):
        for x in range(width):
            r = (x * 4 + y * 2 + len(sample_id) * 3) % 256
            g = (x * 3 + y * 5 + 77) % 256
            b = (x + y * 7 + 123) % 256
            pixels.extend((r, g, b))
    path.write_bytes(header + bytes(pixels))


def capture_image(
    config: MicroscopeConfig,
    sample_id: str = "sample-001",
    assay_run_id: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Create a placeholder image artifact for a microscope capture.

    This keeps the integration usable in simulated and CI environments without requiring
    the full Raspberry Pi / Arduino hardware stack on every run.
    """

    metadata = metadata or {}
    output_dir = Path(config.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = _slugify(sample_id)
    filename = f"{slug}_{timestamp}.ppm"
    image_path = output_dir / filename
    _write_placeholder_ppm(image_path, width=320, height=240, sample_id=sample_id)

    record = {
        "sample_id": sample_id,
        "assay_run_id": assay_run_id,
        "device_name": config.device_name,
        "mode": config.mode,
        "image_path": str(image_path),
        "image_format": "ppm",
        "focus_position": 0.0,
        "magnification": config.magnification,
        "illumination_level": config.illumination_level,
        "metadata": {
            **metadata,
            "camera_resolution": config.camera_resolution,
            "captured_at": timestamp,
            "objective": config.objective,
            "sample_stage": config.sample_stage,
        },
    }
    return record


__all__ = ["capture_image"]
