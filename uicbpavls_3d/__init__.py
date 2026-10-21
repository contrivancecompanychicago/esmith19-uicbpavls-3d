"""3D Bioprocessing Automation Lab package."""

from .backend import DiabetesResearchBackend, LabBackend
from .config import DEFAULT_CONFIG, get_default_config
from .samsung_xr import SamsungXRDiabetesResearch, build_diabetes_xr_profile

__all__ = [
    "DEFAULT_CONFIG",
    "DiabetesResearchBackend",
    "LabBackend",
    "SamsungXRDiabetesResearch",
    "build_diabetes_xr_profile",
    "get_default_config",
]

__version__ = "0"
