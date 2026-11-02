# esmith19-uicbpavls-3d

3D Bioprocessing Automation Lab for Type 2 Diabetes Research.

Version: 0

This repository contains a Python package and FastAPI backend for diabetes-focused bioprocessing automation research, including assay simulation, SQLite-backed research record storage, Samsung XR molecular disease analysis, and a simulated microscope integration layer.

## Overview

The project models an early-glycation assay workflow in a 3D bioprocessing automation lab. It provides:

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
- a simulated microscope integration layer that can later be upgraded to real Raspberry Pi / Arduino hardware

## Microscope integration note

This repo now includes a microscope abstraction designed around the MicroscoPy hardware concept, without requiring Raspberry Pi or serial hardware support yet.

The current implementation is intentionally simulation-first so you can:

- validate the API contract
- test the workflow end-to-end
- capture metadata to the project database
- connect microscope capture into research automation without physical hardware

The integration is structured as a hardware adapter layer, so the real hardware path can be added later with minimal disruption to the existing application.

## Samsung XR diabetes research integration

The project includes a detailed molecular disease workflow designed for Samsung XR visualization and interpretation of diabetes mechanisms.

This research layer supports review of:

- beta-cell stress
- insulin signaling decline
- inflammatory pathway activation
- glycation burden and hyperglycemia-driven damage
- endothelial and vascular remodeling risk
- immersive 3D pathway interpretation in an XR environment

## Bioimage quant integration

This project also includes a lightweight adapter for the bioimage_quant dependency, which is useful for simple biological image quantification workflows such as:

- western blot analysis
- SDS-PAGE gel lane quantification
- spotting assay quantification
- ELISA-style plate/assay wrappers in a simple app-facing interface

This repo does not modify the upstream bioimage_quant project. Instead, it acts as a clean integration layer so your automation workflow can call bioimage_quant in a simple, dependency-friendly way.

Install the assay dependency directly from GitHub:

```bash
python -m pip install git+https://github.com/contrivancecompanychicago/bioimage_quant.git
```

Or install the project in editable mode:

```bash
python -m pip install -e .
```

Example usage:

```python
from uicbpavls_3d import BioImageQuantAdapter

adapter = BioImageQuantAdapter()
result = adapter.analyze_image(
    image_path="/path/to/gel_or_blot.png",
    assay_type="western_blot",
    lane_count=3,
    gaussian_weighted=True,
)
print(result)
```

The adapter will normalize common assay names such as:

- western
- western_blot
- sds
- sds_page
- gel
- spotting
- spotting_assay
- elisa

If the dependency is not installed yet, the adapter returns a helpful structured status with installation guidance instead of failing unexpectedly.

## Package structure

- `uicbpavls_3d/` — installable Python package
- `src/` — legacy module compatibility layer
- `uicbpavls_3d/static/xr_viewer.html` — HTML/XR visualization layer
- `uicbpavls_3d/molecular_model.py` — detailed molecular pathway model + PyMOL script generation
- `uicbpavls_3d/database.py` — SQLite storage for diabetes analyses and microscope captures
- `uicbpavls_3d/microscope/` — microscope adapter, controller, and capture handling
- `examples/microscope_python_example.py` — minimal simulated microscope usage examples
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
- `GET /assays/types` — supported bioimage assay types
- `POST /assays/bioimage-quant` — run a simple bioimage quant assay adapter request
- `GET /xr/view` — HTML/XR visualization page
- `GET /xr/records` — recent stored diabetic XR analyses
- `GET /microscope/status` — microscope adapter status
- `GET /microscope/records` — recent stored microscope captures
- `POST /simulate` — simulate the assay workflow
- `POST /assay/with-microscope` — run assay logic and automatically capture a microscope image in simulated mode
- `POST /microscope/capture` — direct microscope capture request
- `POST /microscope/move` — move the stage/focus axis in simulated mode
- `POST /microscope/auto-focus` — run autofocusing in simulated mode
- `POST /export` — generate CSV and JSON exports
- `POST /xr/diabetes` — Samsung XR molecular diabetes analysis

Example bioimage quant request:

```bash
curl -X POST http://127.0.0.1:8000/assays/bioimage-quant \
  -H "Content-Type: application/json" \
  -d '{
    "image_path": "/path/to/gel_or_blot.png",
    "assay_type": "western_blot",
    "lane_count": 3,
    "gaussian_weighted": true
  }'
```

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

Example direct microscope capture request:

```bash
curl -X POST http://127.0.0.1:8000/microscope/capture \
  -H "Content-Type: application/json" \
  -d '{
    "sample_id": "sample-001",
    "assay_run_id": "assay-001",
    "mode": "simulated",
    "camera_resolution": "1920x1080",
    "metadata": {
      "experiment": "E001",
      "bench": "M1A",
      "notes": "initial simulated microscope validation"
    }
  }'
```

## Minimal Python example

A minimal example script is available at:

```text
examples/microscope_python_example.py
```

It demonstrates how to call the simulated microscope endpoints from Python without requiring Raspberry Pi hardware.

```python
import requests

base_url = "http://127.0.0.1:8000"

payload = {
    "sample_id": "sample-001",
    "assay_run_id": "assay-workflow-001",
    "glucose_levels": [90, 140, 200],
    "time_points": [0, 30, 60],
    "replicates": [1],
    "temperature_c": 37.0,
    "ph": 7.4,
    "output_dir": "data/results",
    "capture_enabled": True,
    "microscope_mode": "simulated",
    "microscope_output_dir": "data/microscope",
    "metadata": {
        "source": "example-script",
        "run_label": "demo",
    },
}

response = requests.post(f"{base_url}/assay/with-microscope", json=payload, timeout=30)
print(response.status_code)
print(response.json())
```

## HTML/XR visualization

Open the visualization page in a browser:

```text
http://127.0.0.1:8000/xr/view
```

The viewer renders a risk index, pathway signal cards, and a PyMOL-ready script output for the selected diabetes molecular profile.

## Database integration

The backend stores diabetes XR analysis records and microscope capture records in SQLite at:

```text
data/diabetes_xr.db
```

This allows persistence of patient analyses, risk scoring, pathway summaries, and microscope image metadata for later review.

## Repository version

This repository is an initial release of a research-oriented framework for diabetes-focused bioprocessing automation, immersive XR analysis, and structured data capture. It includes Samsung XR-enabled molecular analysis, a simulated microscope adapter, and a simple bioimage_assay integration layer for gel/blot and spotting-style workflows.

## Notes

This repository is structured as a research-oriented simulation and automation scaffold, suitable for extension with live instrument APIs, visualization dashboards, richer molecular pathway logic, and assay-specific quantification workflows.

The microscope interface is intentionally separated from the assay pipeline so physical hardware can be added later without rewriting the rest of the project.

The bioimage_quant adapter is intentionally lightweight and dependency-friendly, so the project can integrate analysis tools without forking or rewriting the upstream assay library.
