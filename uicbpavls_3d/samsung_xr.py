"""Samsung XR research utilities for diabetes molecular disease modeling."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class DiabetesMolecularSignal:
    pathway: str
    biomarker: str
    signal_value: float
    interpretation: str


class SamsungXRDiabetesResearch:
    """Immersive XR review of diabetes molecular pathways."""

    def __init__(self, patient_id: str = "T2D-001") -> None:
        self.patient_id = patient_id

    def build_profile(
        self,
        glucose_mg_dL: float = 180.0,
        hba1c_pct: float = 7.4,
        insulin_resistance_index: float = 0.72,
        inflammatory_load: float = 0.68,
        beta_cell_stress: float = 0.74,
    ) -> Dict[str, Any]:
        signals = [
            DiabetesMolecularSignal(
                pathway="Pancreatic beta-cell stress",
                biomarker="beta-cell viability",
                signal_value=max(0.0, min(1.0, beta_cell_stress)),
                interpretation="Elevated stress suggests impaired insulin secretion and glucose dysregulation.",
            ),
            DiabetesMolecularSignal(
                pathway="Insulin signaling",
                biomarker="insulin receptor activity",
                signal_value=max(0.0, min(1.0, 1.0 - insulin_resistance_index)),
                interpretation="Reduced receptor efficiency supports systemic insulin resistance.",
            ),
            DiabetesMolecularSignal(
                pathway="Inflammatory signaling",
                biomarker="NF-kB / cytokine tone",
                signal_value=max(0.0, min(1.0, inflammatory_load)),
                interpretation="Chronic inflammatory signaling contributes to metabolic dysfunction and fibrosis.",
            ),
            DiabetesMolecularSignal(
                pathway="Glycation burden",
                biomarker="advanced glycation marker",
                signal_value=max(0.0, min(1.0, min(1.0, glucose_mg_dL / 300.0))),
                interpretation="Persistent hyperglycemia increases protein glycation and vascular injury risk.",
            ),
        ]

        overall_risk = round(
            (
                (glucose_mg_dL / 300.0) * 0.35
                + (hba1c_pct / 10.0) * 0.25
                + insulin_resistance_index * 0.20
                + inflammatory_load * 0.10
                + beta_cell_stress * 0.10
            ),
            3,
        )

        xr_scene = {
            "device": "Samsung XR",
            "mode": "molecular disease atlas",
            "patient_id": self.patient_id,
            "layers": [
                "insulin signaling network",
                "beta-cell stress response",
                "glycation and inflammation pathways",
                "vascular remodeling risk",
            ],
            "annotation": {
                "summary": "Diabetes molecular pathways are visualized in an immersive 3D XR view to support mechanistic interpretation.",
                "recommendation": "Prioritize targeted intervention on insulin resistance, glycemic control, and inflammatory pathways.",
            },
        }

        return {
            "patient_id": self.patient_id,
            "device": "Samsung XR",
            "focus": "Molecular basis of diabetes disease research",
            "risk_index": min(1.0, overall_risk),
            "signals": [
                {
                    "pathway": s.pathway,
                    "biomarker": s.biomarker,
                    "signal_value": round(s.signal_value, 3),
                    "interpretation": s.interpretation,
                }
                for s in signals
            ],
            "scene": xr_scene,
        }


def build_diabetes_xr_profile(
    patient_id: str = "T2D-001",
    glucose_mg_dL: float = 180.0,
    hba1c_pct: float = 7.4,
    insulin_resistance_index: float = 0.72,
    inflammatory_load: float = 0.68,
    beta_cell_stress: float = 0.74,
) -> Dict[str, Any]:
    engine = SamsungXRDiabetesResearch(patient_id=patient_id)
    return engine.build_profile(
        glucose_mg_dL=glucose_mg_dL,
        hba1c_pct=hba1c_pct,
        insulin_resistance_index=insulin_resistance_index,
        inflammatory_load=inflammatory_load,
        beta_cell_stress=beta_cell_stress,
    )
