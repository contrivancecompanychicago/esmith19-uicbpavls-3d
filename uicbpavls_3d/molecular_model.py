"""Detailed molecular pathway model and PyMOL script generation for diabetes research."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List


@dataclass
class PathwayNode:
    name: str
    role: str
    color: str
    coordinates: List[float]
    weight: float
    description: str


class DetailedDiabetesPathwayModel:
    """Detailed diabetes molecular model with a PyMOL-ready pathway visualization."""

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
        nodes = [
            PathwayNode(
                name="GLUCOSE_INGESTION",
                role="metabolic_signal",
                color="red",
                coordinates=[0.0, 0.0, 1.0],
                weight=max(0.0, min(1.0, glucose_mg_dL / 300.0)),
                description="Hyperglycemia drives glycation and oxidative stress.",
            ),
            PathwayNode(
                name="BETA_CELL_STRESS",
                role="cellular_dysfunction",
                color="orange",
                coordinates=[2.0, 1.0, 0.0],
                weight=max(0.0, min(1.0, beta_cell_stress)),
                description="Stress restricts insulin secretion and vesicle trafficking.",
            ),
            PathwayNode(
                name="INSULIN_RECEPTOR",
                role="signaling",
                color="yellow",
                coordinates=[2.5, 3.0, 1.0],
                weight=max(0.0, min(1.0, 1.0 - insulin_resistance_index)),
                description="Insulin receptor signaling declines under resistance conditions.",
            ),
            PathwayNode(
                name="NF_KB_CYTOKINE",
                role="inflammatory",
                color="purple",
                coordinates=[5.0, 2.0, 0.5],
                weight=max(0.0, min(1.0, inflammatory_load)),
                description="Inflammatory cytokines amplify metabolic and vascular stress.",
            ),
            PathwayNode(
                name="AGE_GLYCATION",
                role="damage",
                color="blue",
                coordinates=[6.0, 5.0, 2.0],
                weight=max(0.0, min(1.0, min(1.0, glucose_mg_dL / 300.0))),
                description="Advanced glycation end products accumulate with persistent hyperglycemia.",
            ),
            PathwayNode(
                name="MITOCHONDRIAL_DYSFUNCTION",
                role="metabolic_decline",
                color="cyan",
                coordinates=[8.0, 3.0, 1.5],
                weight=max(0.0, min(1.0, (beta_cell_stress + inflammatory_load) / 2.0)),
                description="Mitochondrial dysfunction reduces energetic efficiency and insulin production.",
            ),
            PathwayNode(
                name="ENDOTHELIAL_DAMAGE",
                role="vascular_risk",
                color="green",
                coordinates=[10.0, 6.0, 2.5],
                weight=max(0.0, min(1.0, (glucose_mg_dL / 300.0) * 0.8 + inflammatory_load * 0.2)),
                description="Endothelial stress increases vascular remodeling and microvascular damage.",
            ),
        ]

        risk_index = round(
            (
                (glucose_mg_dL / 300.0) * 0.18
                + (hba1c_pct / 10.0) * 0.12
                + insulin_resistance_index * 0.24
                + inflammatory_load * 0.24
                + beta_cell_stress * 0.22
            ),
            3,
        )

        pathway_scores = [
            {
                "name": node.name,
                "role": node.role,
                "weight": round(node.weight, 3),
                "description": node.description,
                "coordinates": node.coordinates,
                "color": node.color,
            }
            for node in nodes
        ]

        pymol_script = self.generate_pymol_script(nodes)

        return {
            "patient_id": self.patient_id,
            "device": "Samsung XR",
            "focus": "Detailed molecular pathway model for diabetes disease research",
            "risk_index": min(1.0, risk_index),
            "pathway_scores": pathway_scores,
            "pymol_script": pymol_script,
            "summary": {
                "primary_driver": "Insulin signaling collapse and inflammatory signaling amplification",
                "mechanism": "Hyperglycemia enhances glycation and inflammatory stress, leading to beta-cell dysfunction and vascular injury.",
            },
        }

    def generate_pymol_script(self, nodes: List[PathwayNode]) -> str:
        script_lines = [
            "from pymol import cmd",
            "cmd.bg_color('white')",
            "cmd.set('sphere_scale', 0.45)",
            "cmd.set('ray_ambient', 0.5)",
            "cmd.set('line_width', 2)",
            "cmd.hide('everything')",
            "cmd.show('spheres')",
        ]

        for index, node in enumerate(nodes):
            x, y, z = node.coordinates
            script_lines.append(
                f"cmd.sphere('( {x},{y},{z} )', color='{node.color}', radius={node.weight + 0.25})"
            )
            script_lines.append(f"cmd.label('( {x},{y},{z} )', '{node.name}')")
            script_lines.append(f"cmd.set_name('obj{index}', '{node.name}')")

        script_lines.append("cmd.orient()")
        script_lines.append("cmd.zoom()")
        return "\n".join(script_lines)


def generate_pymol_script(
    glucose_mg_dL: float = 180.0,
    hba1c_pct: float = 7.4,
    insulin_resistance_index: float = 0.72,
    inflammatory_load: float = 0.68,
    beta_cell_stress: float = 0.74,
    patient_id: str = "T2D-001",
) -> str:
    model = DetailedDiabetesPathwayModel(patient_id=patient_id)
    profile = model.build_profile(
        glucose_mg_dL=glucose_mg_dL,
        hba1c_pct=hba1c_pct,
        insulin_resistance_index=insulin_resistance_index,
        inflammatory_load=inflammatory_load,
        beta_cell_stress=beta_cell_stress,
    )
    return profile["pymol_script"]
