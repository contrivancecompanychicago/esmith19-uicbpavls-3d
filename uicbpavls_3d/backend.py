"""FastAPI backend for the 3D Bioprocessing Automation Lab."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Optional

import numpy as np
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from .config import DEFAULT_CONFIG, LabConfig
from .database import get_recent_analyses, init_db, save_analysis
from .molecular_model import DetailedDiabetesPathwayModel
from .samsung_xr import build_diabetes_xr_profile

__version__ = "0"


def simulate_glycation(
    glucose_mg_dL: float,
    time_min: float,
    temp_c: float = 37.0,
    ph: float = 7.40,
    k_rate: float = 0.00015,
) -> float:
    temp_factor = 1.0 + 0.03 * (temp_c - 37.0)
    ph_factor = 1.0 + 0.1 * (ph - 7.40)
    effective_rate = k_rate * temp_factor * ph_factor
    adduct_conc = glucose_mg_dL * (1 - np.exp(-effective_rate * time_min))
    return float(adduct_conc)


def virtual_fructosamine_assay(
    glycated_conc: float,
    noise_level: float = 0.02,
    gain: float = 1.25,
    baseline: float = 0.05,
) -> float:
    true_signal = baseline + (glycated_conc * gain)
    noise = np.random.normal(0, noise_level * true_signal) if true_signal > 0 else 0
    observed_signal = max(0.0, true_signal + noise)
    return round(observed_signal, 4)


def evaluate_qc(row: pd.Series, min_signal: float = 0.0, max_signal: float = 500.0) -> str:
    signal = row.get("Signal")
    if signal is None:
        return "REJECTED_MISSING"
    if signal < min_signal or signal > max_signal:
        return "REJECTED_OUT_OF_BOUNDS"
    return "ACCEPTED"


class AssayRequest(BaseModel):
    glucose_levels: list[int] = Field(default_factory=lambda: [90, 140, 200, 300])
    time_points: list[int] = Field(default_factory=lambda: [0, 30, 60, 120])
    replicates: list[int] = Field(default_factory=lambda: [1])
    temperature_c: float = 37.0
    ph: float = 7.40
    output_dir: str = "data/results"


class XRResearchRequest(BaseModel):
    patient_id: str = "T2D-001"
    glucose_mg_dL: float = 180.0
    hba1c_pct: float = 7.4
    insulin_resistance_index: float = 0.72
    inflammatory_load: float = 0.68
    beta_cell_stress: float = 0.74


class LabBackend:
    def __init__(self, config: Optional[LabConfig] = None, output_dir: str | Path = "data/results"):
        self.config = config or DEFAULT_CONFIG
        self.output_dir = Path(output_dir)

    def build_sample_manifest(self) -> pd.DataFrame:
        records: list[dict[str, Any]] = []
        for glucose in self.config.glucose_levels:
            for time_point in self.config.time_points:
                for replicate in self.config.replicates:
                    sample_id = (
                        f"{self.config.bench}-{self.config.experiment}-"
                        f"G{glucose:03d}-T{time_point:03d}-R{replicate}"
                    )
                    records.append(
                        {
                            "SampleID": sample_id,
                            "Glucose_mg_dL": glucose,
                            "Time_min": time_point,
                            "Replicate": replicate,
                            "Trial": 1,
                            "QC_Status": "PENDING",
                            "Signal": None,
                        }
                    )
        return pd.DataFrame(records)

    def run_assay_workflow(self, df: Optional[pd.DataFrame] = None) -> pd.DataFrame:
        manifest = df.copy() if df is not None else self.build_sample_manifest()
        for index, row in manifest.iterrows():
            glycated_conc = simulate_glycation(
                glucose_mg_dL=float(row["Glucose_mg_dL"]),
                time_min=float(row["Time_min"]),
                temp_c=float(self.config.temperature_c),
                ph=float(self.config.ph),
            )
            manifest.at[index, "Signal"] = virtual_fructosamine_assay(glycated_conc)

        manifest["QC_Status"] = manifest.apply(evaluate_qc, axis=1)
        return manifest

    def export_results(self, df: Optional[pd.DataFrame] = None, *, output_dir: Optional[str | Path] = None) -> dict[str, str]:
        manifest = df.copy() if df is not None else self.run_assay_workflow()
        target_dir = Path(output_dir) if output_dir is not None else self.output_dir
        target_dir.mkdir(parents=True, exist_ok=True)

        csv_path = target_dir / f"{self.config.bench}_{self.config.experiment}_results.csv"
        json_path = target_dir / f"{self.config.bench}_{self.config.experiment}_protocol_log.json"

        manifest.to_csv(csv_path, index=False)

        log_data = {
            "project": self.config.project,
            "module": self.config.module,
            "bench": self.config.bench,
            "experiment": self.config.experiment,
            "version": self.config.version,
            "app_name": self.config.app_name,
            "lab_configuration": self.config.as_dict,
            "total_samples": int(len(manifest)),
            "qc_summary": manifest["QC_Status"].value_counts().to_dict(),
            "records": manifest.to_dict(orient="records"),
        }

        with json_path.open("w", encoding="utf-8") as handle:
            json.dump(log_data, handle, indent=4)

        return {"csv": str(csv_path), "json": str(json_path)}


class DiabetesResearchBackend(LabBackend):
    pass


app = FastAPI(
    title="3D Bioprocessing Automation Lab",
    description="Type 2 Diabetes Research backend with Samsung XR molecular modeling and database integration.",
    version=__version__,
)


@app.on_event("startup")
def startup_event() -> None:
    init_db()


@app.get("/")
def read_root() -> dict[str, str]:
    return {"service": "3D Bioprocessing Automation Lab", "version": __version__}


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/config")
def get_lab_config() -> dict[str, Any]:
    return DEFAULT_CONFIG.as_dict


@app.get("/xr/view")
def xr_view() -> FileResponse:
    viewer_path = Path(__file__).resolve().parent / "static" / "xr_viewer.html"
    return FileResponse(viewer_path)


@app.get("/xr/records")
def xr_records() -> dict[str, Any]:
    return {"records": get_recent_analyses(limit=20)}


@app.post("/simulate")
def simulate_assay(payload: AssayRequest) -> dict[str, Any]:
    config = LabConfig(
        glucose_levels=payload.glucose_levels,
        time_points=payload.time_points,
        replicates=payload.replicates,
        temperature_c=payload.temperature_c,
        ph=payload.ph,
    )
    backend = LabBackend(config=config, output_dir=payload.output_dir)
    manifest = backend.run_assay_workflow()
    return {
        "count": int(len(manifest)),
        "preview": manifest.head(10).to_dict(orient="records"),
        "qc_summary": manifest["QC_Status"].value_counts().to_dict(),
    }


@app.post("/export")
def export_assay(payload: AssayRequest) -> dict[str, Any]:
    config = LabConfig(
        glucose_levels=payload.glucose_levels,
        time_points=payload.time_points,
        replicates=payload.replicates,
        temperature_c=payload.temperature_c,
        ph=payload.ph,
    )
    backend = LabBackend(config=config, output_dir=payload.output_dir)
    manifest = backend.run_assay_workflow()
    exports = backend.export_results(manifest)
    return {"files": exports, "record_count": int(len(manifest))}


@app.post("/xr/diabetes")
def samsung_xr_diabetes_analysis(payload: XRResearchRequest) -> dict[str, Any]:
    base_profile = build_diabetes_xr_profile(
        patient_id=payload.patient_id,
        glucose_mg_dL=payload.glucose_mg_dL,
        hba1c_pct=payload.hba1c_pct,
        insulin_resistance_index=payload.insulin_resistance_index,
        inflammatory_load=payload.inflammatory_load,
        beta_cell_stress=payload.beta_cell_stress,
    )

    detailed_model = DetailedDiabetesPathwayModel(patient_id=payload.patient_id)
    detailed_profile = detailed_model.build_profile(
        glucose_mg_dL=payload.glucose_mg_dL,
        hba1c_pct=payload.hba1c_pct,
        insulin_resistance_index=payload.insulin_resistance_index,
        inflammatory_load=payload.inflammatory_load,
        beta_cell_stress=payload.beta_cell_stress,
    )

    payload_dict = payload.dict() if hasattr(payload, "dict") else payload.model_dump()
    save_analysis(payload_dict, base_profile)

    return {
        "platform": "Samsung XR",
        "focus": "Molecular basis of diabetes disease research",
        "analysis": base_profile,
        "molecular_model": detailed_profile,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("uicbpavls_3d.backend:app", host="0.0.0.0", port=8000, reload=True)
