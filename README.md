# esmith19-uicbpavls-3d

3D Bioprocessing Automation Lab for Type 2 Diabetes Research.

Version: 0

This repository contains a Python package and FastAPI backend for diabetes-focused bioprocessing automation research, including Samsung XR molecular disease modeling for the molecular basis of diabetes.

## Overview

The project models an early-glycation assay workflow for a 3D bioprocessing automation lab. It provides:

- lab configuration and metadata
- sample manifest generation
- simulated glycation kinetics
- optical assay signal generation
- QC validation
- CSV and JSON export for analysis artifacts
- REST API access for automation workflows
- Samsung XR molecular disease analysis for diabetes research
- detailed molecular pathway modeling with PyMOL-ready output
- HTML/XR visualization layer
- SQLite database integration for stored research records

## Samsung XR diabetes research integration

The project includes a detailed molecular disease workflow designed for Samsung XR visualization and interpretation of diabetes mechanisms.

This research layer supports review of:

- beta-cell stress
- insulin signaling decline
- inflammatory pathway activation
- glycation burden and hyperglycemia-driven damage
- endothelial and vascular remodeling risk
- immersive 3D pathway interpretation in an XR environment

## Package structure

- `uicbpavls_3d/` — installable Python package
- `src/` — legacy module compatibility layer
- `uicbpavls_3d/static/xr_viewer.html` — HTML/XR visualization layer
- `uicbpavls_3d/molecular_model.py` — detailed molecular pathway model + PyMOL script generation
- `uicbpavls_3d/database.py` — SQLite storage for diabetes analyses
- `pyproject.toml` — packaging metadata and dependencies

## Installation

```bash
python -m pip install .
```

## Quick start

```python
from uicbpavls_3d import DiabetesResearchBackend, build_diabetes_xr_profile, DetailedDiabetesPathwayModel

backend = DiabetesResearchBackend()
manifest = backend.run_assay_workflow()
paths = backend.export_results(manifest)
print(paths)
print(manifest.head())

profile = build_diabetes_xr_profile(
    patient_id="T2D-001",
    glucose_mg_dL=180,
    hba1c_pct=7.4,
    insulin_resistance_index=0.72,
    inflammatory_load=0.68,
    beta_cell_stress=0.74,
)
print(profile)

model = DetailedDiabetesPathwayModel(patient_id="T2D-001")
print(model.build_profile())
```

## FastAPI backend

Start the API server:

```bash
uvicorn uicbpavls_3d.backend:app --reload
```

Available endpoints:

- `GET /` — service metadata
- `GET /health` — health check
- `GET /config` — lab configuration
- `GET /xr/view` — HTML/XR visualization page
- `GET /xr/records` — recent stored diabetic XR analyses
- `POST /simulate` — simulate the assay workflow
- `POST /export` — generate CSV and JSON exports
- `POST /xr/diabetes` — Samsung XR molecular diabetes analysis

Example XR analysis request:

```bash
curl -X POST http://127.0.0.1:8000/xr/diabetes \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "T2D-001",
    "glucose_mg_dL": 180,
    "hba1c_pct": 7.4,
    "insulin_resistance_index": 0.72,
    "inflammatory_load": 0.68,
    "beta_cell_stress": 0.74
  }'
```

## HTML/XR visualization

Open the visualization page in a browser:

```bash
http://127.0.0.1:8000/xr/view
```

The viewer renders a risk index, pathway signal cards, and a PyMOL-ready script output for the selected diabetes molecular profile.

## Database integration

The backend stores diabetes XR analysis records in SQLite at:

```text
data/diabetes_xr.db
```

This allows persistence of patient analyses, risk scoring, and pathway summaries for later review.

## Repository version

The project is declared as version 0 and includes Samsung XR-enabled molecular disease research, PyMOL-ready pathway modeling, HTML/XR visualization, and database-backed storage for type 2 diabetes workflows.

## Notes

This repository is structured as a research-oriented simulation and automation scaffold, suitable for extension with live instrument integrations, immersive XR scenes, richer molecular pathway logic, and downstream analytics workflows.
