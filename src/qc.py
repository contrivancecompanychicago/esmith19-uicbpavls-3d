"""
Quality Control Rules Engine
"""

from src.config import DATA_CLASSIFICATION, EXECUTION_AUTHORIZED, GLUCOSE_LEVELS, REPLICATES, TIME_POINTS
from src.controls import CONTROLS
from src.specimens import SPECIMEN


REQUIRED_PREFLIGHT_COLUMNS = [
    "experiment_id",
    "protocol_version",
    "trial",
    "sample_id",
    "specimen_id",
    "glucose_mg_dl",
    "exposure_time_min",
    "temperature_c",
    "ph",
    "replicate",
    "data_type",
]


def validate_manifest(df):
    expected_samples = len(GLUCOSE_LEVELS) * len(TIME_POINTS) * len(REPLICATES)
    actual_samples = len(df)
    unique_sample_ids = df["sample_id"].nunique() if "sample_id" in df.columns else 0

    missing_required_columns = [
        column for column in REQUIRED_PREFLIGHT_COLUMNS if column not in df.columns
    ]

    if missing_required_columns:
        missing_required_values = True
    else:
        missing_required_values = bool(df[REQUIRED_PREFLIGHT_COLUMNS].isnull().any().any())

    checks = {
        "sample_count": actual_samples == expected_samples,
        "unique_sample_ids": unique_sample_ids == expected_samples,
        "required_columns": len(missing_required_columns) == 0,
        "required_values": not missing_required_values,
        "specimen_id": (
            "specimen_id" in df.columns
            and (df["specimen_id"] == SPECIMEN["id"]).all()
        ),
        "data_type": (
            "data_type" in df.columns
            and (df["data_type"] == DATA_CLASSIFICATION).all()
        ),
    }

    return {
        "expected_samples": expected_samples,
        "actual_samples": actual_samples,
        "unique_sample_ids": unique_sample_ids,
        "missing_required_columns": missing_required_columns,
        "missing_required_values": missing_required_values,
        "checks": checks,
        "pass": all(checks.values()),
    }


def validate_controls():
    required_controls = {"C0", "C1", "C2"}
    registered_controls = set(CONTROLS.keys())

    return {
        "required_controls": sorted(required_controls),
        "registered_controls": sorted(registered_controls),
        "pass": required_controls.issubset(registered_controls),
    }


def run_preflight_qc(df):
    manifest_qc = validate_manifest(df)
    controls_qc = validate_controls()

    preflight_pass = manifest_qc["pass"] and controls_qc["pass"]
    run_state = "QC_READY" if preflight_pass else "PREFLIGHT_FAILED"

    return {
        "expected_samples": manifest_qc["expected_samples"],
        "actual_samples": manifest_qc["actual_samples"],
        "unique_sample_ids": manifest_qc["unique_sample_ids"],
        "missing_required_values": manifest_qc["missing_required_values"],
        "controls_registered": len(CONTROLS),
        "data_type": DATA_CLASSIFICATION,
        "execution_authorized": EXECUTION_AUTHORIZED,
        "preflight": "PASS" if preflight_pass else "FAIL",
        "run_state": run_state,
        "manifest_qc": manifest_qc,
        "controls_qc": controls_qc,
    }


def evaluate_qc(row, min_signal=0.0, max_signal=500.0):
    """
    Evaluates observed assay signals against post-run laboratory QC criteria.
    """
    signal = row.get("corrected_assay_signal", None)
    if signal is None:
        return "REJECTED_MISSING"
    if signal < min_signal or signal > max_signal:
        return "REJECTED_OUT_OF_BOUNDS"
    return "ACCEPTED"


def run_qc_pipeline(df):
    df = df.copy()
    df["qc_status"] = df.apply(evaluate_qc, axis=1)
    return df
