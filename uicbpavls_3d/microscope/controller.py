"""Microscope controller logic for the MicroscoPy-style hardware integration."""

from __future__ import annotations

from typing import Any, Dict

from ..config import MicroscopeConfig


class MicroscopeController:
    """Low-level microscope control interface for stage, focus, and illumination."""

    def __init__(self, config: MicroscopeConfig):
        self.config = config

    def status(self) -> Dict[str, Any]:
        return {
            "enabled": self.config.enabled,
            "mode": self.config.mode,
            "device_name": self.config.device_name,
            "serial_port": self.config.serial_port,
            "camera_resolution": self.config.camera_resolution,
            "illumination_level": self.config.illumination_level,
        }

    def move(self, axis: str = "focus", steps: int = 10, direction: str = "positive") -> Dict[str, Any]:
        if not self.config.enabled:
            return {"status": "disabled", "axis": axis, "steps": steps, "direction": direction}

        if self.config.mode == "simulated":
            return {
                "status": "simulated",
                "axis": axis,
                "steps": steps,
                "direction": direction,
                "position": steps if direction == "positive" else -steps,
            }

        return {
            "status": "queued",
            "axis": axis,
            "steps": steps,
            "direction": direction,
            "device": self.config.device_name,
            "serial_port": self.config.serial_port,
        }

    def auto_focus(self) -> Dict[str, Any]:
        if not self.config.enabled:
            return {"status": "disabled", "focus_step": 0, "auto_focus": False}

        focus_step = self.config.focus_steps if self.config.auto_focus_enabled else 0
        return {
            "status": "simulated" if self.config.mode == "simulated" else "queued",
            "auto_focus": self.config.auto_focus_enabled,
            "focus_step": focus_step,
            "device": self.config.device_name,
        }

    def set_illumination(self, level: int) -> Dict[str, Any]:
        effective = max(0, min(255, int(level)))
        return {
            "status": "simulated" if self.config.mode == "simulated" else "queued",
            "illumination_level": effective,
            "device": self.config.device_name,
        }


__all__ = ["MicroscopeController"]
