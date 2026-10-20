"""
Quality Control Rules Engine
"""

def evaluate_qc(row, min_signal=0.0, max_signal=500.0):
    """
    Evaluates observed assay signals against laboratory QC criteria.
    """
    signal = row["Signal"]
    if signal is None:
        return "REJECTED_MISSING"
    if signal < min_signal or signal > max_signal:
        return "REJECTED_OUT_OF_BOUNDS"
    return "ACCEPTED"

def run_qc_pipeline(df):
    df["QC_Status"] = df.apply(evaluate_qc, axis=1)
    return df
