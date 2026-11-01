"""Microscope integration layer for the 3D Bioprocessing Automation Lab."""

from __future__ import annotations

from typing import Any, Dict, Optional

from .config import MicroscopeConfig
from .microscope.capture import capture_image
from .microscope.controller import MicroscopeController


class MicroscopeAdapter:
    """Thin adapter that keeps microscope logic separate from the lab backend."""

    def __init__(self, config: Optional[MicroscopeConfig] = None):
        self.config = config or MicroscopeConfig()
        self.controller = MicroscopeController(self.config)

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.config.enabled,
            "device_name": self.config.device_name,
            "mode": self.config.mode,
            "camera_resolution": self.config.camera_resolution,
            "output_dir": self.config.output_dir,
            "auto_focus_enabled": self.config.auto_focus_enabled,
            "magnification": self.config.magnification,
            "notes": self.config.notes,
        }

    def move(self, axis: str = "focus", steps: int = 10, direction: str = "positive") -> Dict[str, Any]:
        return self.controller.move(axis=axis, steps=steps, direction=direction)

    def auto_focus(self) -> Dict[str, Any]:
        return self.controller.auto_focus()

    def capture(
        self,
        sample_id: str = "sample-001",
        assay_run_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        metadata = metadata or {}
        capture_record = capture_image(
            config=self.config,
            sample_id=sample_id,
            assay_run_id=assay_run_id,
            metadata=metadata,
        )
        return {
            "status": "captured",
            "device_name": self.config.device_name,
            "sample_id": sample_id,
            "assay_run_id": assay_run_id,
            "image_path": capture_record["image_path"],
            "image_format": capture_record["image_format"],
            "record": capture_record,
        }


__all__ = ["MicroscopeAdapter"]
