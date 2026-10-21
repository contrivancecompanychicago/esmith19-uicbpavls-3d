"""
Laboratory Configuration and Metadata
"""

PROJECT = "UIC_PAVLS"
MODULE = "M1"
BENCH = "M1A"
EXPERIMENT = "E001"
PROTOCOL_ID = "UIC-PAVLS-M1A-E001"
VERSION = "0.1"
TRIAL = 1
TRIAL_TYPE = "Range Finding"
RUN_STATE = "PREFLIGHT"
DATA_CLASSIFICATION = "SIMULATED"
EXECUTION_AUTHORIZED = False
APP_NAME = "3D Bioprocessing Automation Lab"

LAB = {
    "temperature_c": 37.0,
    "ph": 7.40,
    "protein": "Albumin",
    "protein_amount": "FIXED",
    "sample_volume": "FIXED",
    "buffer": "STANDARDIZED_VIRTUAL_BUFFER",
    "assay_model": "FIXED",
    "status": "READY"
}

# Experimental Design Conditions
GLUCOSE_LEVELS = [90, 140, 200, 300]  # mg/dL
TIME_POINTS = [0, 30, 60, 120]         # minutes
REPLICATES = [1]
