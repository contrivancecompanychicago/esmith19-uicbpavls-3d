"""Minimal Python examples for the `uicbpavls_3d` microscope and assay API.

These examples use the simulated microscope mode and require no Raspberry Pi or serial
hardware support.
"""

from __future__ import annotations

import json
from typing import Any

import requests

BASE_URL = "http://127.0.0.1:8000"


def example_capture_only() -> dict[str, Any]:
    payload = {
        "sample_id": "sample-001",
        "assay_run_id": "assay-001",
        "mode": "simulated",
        "camera_resolution": "1920x1080",
        "metadata": {
            "experiment": "E001",
            "bench": "M1A",
            "notes": "initial simulated microscope validation",
        },
    }
    response = requests.post(f"{BASE_URL}/microscope/capture", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def example_assay_with_microscope() -> dict[str, Any]:
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
    response = requests.post(f"{BASE_URL}/assay/with-microscope", json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def example_status() -> dict[str, Any]:
    response = requests.get(f"{BASE_URL}/microscope/status", timeout=30)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    print(json.dumps(example_status(), indent=2))
    print(json.dumps(example_capture_only(), indent=2))
    print(json.dumps(example_assay_with_microscope(), indent=2))
