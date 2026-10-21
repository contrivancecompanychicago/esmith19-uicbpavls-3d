"""Configuration and metadata for the 3D Bioprocessing Automation Lab."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class LabConfig:
    project: str = "UIC_PAVLS"
    module: str = "M1"
    bench: str = "M1A"
    experiment: str = "E001"
    version: str = "0"
    app_name: str = "3D Bioprocessing Automation Lab"
    run_state: str = "PREFLIGHT"
    data_classification: str = "SIMULATED"
    samsung_xr_enabled: bool = True
    samsung_xr_platform: str = "Samsung XR"
    research_focus: str = "Molecular basis of diabetes disease pathways"
    temperature_c: float = 37.0
    ph: float = 7.40
    protein: str = "Albumin"
    glucose_levels: List[int] = field(default_factory=lambda: [90, 140, 200, 300])
    time_points: List[int] = field(default_factory=lambda: [0, 30, 60, 120])
    replicates: List[int] = field(default_factory=lambda: [1])

    @property
    def as_dict(self) -> Dict[str, object]:
        return {
            "project": self.project,
            "module": self.module,
            "bench": self.bench,
            "experiment": self.experiment,
            "version": self.version,
            "app_name": self.app_name,
            "run_state": self.run_state,
            "data_classification": self.data_classification,
            "samsung_xr_enabled": self.samsung_xr_enabled,
            "samsung_xr_platform": self.samsung_xr_platform,
            "research_focus": self.research_focus,
            "temperature_c": self.temperature_c,
            "ph": self.ph,
            "protein": self.protein,
            "glucose_levels": self.glucose_levels,
            "time_points": self.time_points,
            "replicates": self.replicates,
        }


DEFAULT_CONFIG = LabConfig()


def get_default_config() -> LabConfig:
    return LabConfig()
