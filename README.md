# esmith19-uicbpavls-3d

3D Bioprocessing Automation Lab for Type 2 Diabetes Research.

Version: 0

This repository contains a Python package and a FastAPI backend for the research automation workflow used in diabetes-related bioprocessing simulations.

## Overview

The project models an early-glycation assay workflow for a 3D bioprocessing automation lab. It provides:

- lab configuration and metadata
- sample manifest generation
- simulated glycation kinetics
- optical assay signal generation
- QC validation
- CSV and JSON export for analysis artifacts
- REST API access for automation workflows

## Package structure

- `uicbpavls_3d/` — installable Python package
- `src/` — legacy module compatibility layer
- `pyproject.toml` — packaging metadata and dependencies

## Installation

```bash
python -m pip install .
```

## Quick start

```python
from uicbpavls_3d import DiabetesResearchBackend

backend = DiabetesResearchBackend()
manifest = backend.run_assay_workflow()
paths = backend.export_results(manifest)
print(paths)
print(manifest.head())
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
- `POST /simulate` — simulate the assay workflow
- `POST /export` — generate CSV and JSON exports

Example request:

```bash
curl -X POST http://127.0.0.1:8000/simulate \
  -H "Content-Type: application/json" \
  -d '{
    "glucose_levels": [90, 140, 200, 300],
    "time_points": [0, 30, 60, 120],
    "replicates": [1],
    "temperature_c": 37.0,
    "ph": 7.4
  }'
```

## Repository version

The project is declared as version 0 in both the package metadata and the core configuration.

## Notes

This repository is structured as a research-oriented simulation and automation scaffold, suitable for extension with live instrument integrations, dashboards, data persistence, or additional API services.
