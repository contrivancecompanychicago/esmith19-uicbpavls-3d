"""
Laboratory Configuration and Metadata
"""

PROJECT = "UIC_PAVLS"
MODULE = "M1"
BENCH = "M1A"
EXPERIMENT = "E001"
VERSION = "0"
RUN_STATE = "PREFLIGHT"
DATA_CLASSIFICATION = "SIMULATED"
APP_NAME = "3D Bioprocessing Automation Lab"

LAB = {
    "temperature_c": 37.0,
    "ph": 7.40,
    "protein": "Albumin",
    "status": "READY"
}

# Experimental Design Conditions
GLUCOSE_LEVELS = [90, 140, 200, 300]  # mg/dL
TIME_POINTS = [0, 30, 60, 120]         # minutes
REPLICATES = [1]
