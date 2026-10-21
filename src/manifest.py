"""
Sample Manifest and Dataframe Construction
"""

import pandas as pd

from src.config import (
    DATA_CLASSIFICATION,
    EXPERIMENT,
    GLUCOSE_LEVELS,
    LAB,
    REPLICATES,
    TRIAL,
    VERSION,
    TIME_POINTS,
)
from src.specimens import SPECIMEN


def build_sample_manifest():
    records = []

    for g in GLUCOSE_LEVELS:
        for t in TIME_POINTS:
            for r in REPLICATES:
                sample_id = f"M1A-E001-G{g:03d}-T{t:03d}-R{r}"

                records.append({
                    "experiment_id": EXPERIMENT,
                    "protocol_version": VERSION,
                    "trial": TRIAL,
                    "sample_id": sample_id,
                    "specimen_id": SPECIMEN["id"],
                    "glucose_mg_dl": g,
                    "exposure_time_min": t,
                    "temperature_c": LAB["temperature_c"],
                    "ph": LAB["ph"],
                    "replicate": r,
                    "model_type": None,
                    "model_version": None,
                    "parameter_status": None,
                    "glycation_fraction": None,
                    "raw_assay_signal": None,
                    "blank_signal": None,
                    "corrected_assay_signal": None,
                    "qc_status": "PENDING",
                    "data_type": DATA_CLASSIFICATION,
                })

    return pd.DataFrame(records)
