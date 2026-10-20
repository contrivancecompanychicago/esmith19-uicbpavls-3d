"""
Sample Manifest and Dataframe Construction
"""

import pandas as pd
from src.config import GLUCOSE_LEVELS, TIME_POINTS, REPLICATES

def build_sample_manifest():
    records = []
    for g in GLUCOSE_LEVELS:
        for t in TIME_POINTS:
            for r in REPLICATES:
                sample_id = f"M1A-E001-G{g:03d}-T{t:03d}-R{r}"
                records.append({
                    "SampleID": sample_id,
                    "Glucose_mg_dL": g,
                    "Time_min": t,
                    "Replicate": r,
                    "Trial": 1,
                    "QC_Status": "PENDING",
                    "Signal": None
                })
    return pd.DataFrame(records)
