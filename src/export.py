"""
Export Utility for ELN Artifacts
"""

import os
import json

def export_artifacts(df, lab_config, specimen_info, output_dir="data/results"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Export CSV Manifest
    csv_path = os.path.join(output_dir, "M1A_E001_results.csv")
    df.to_csv(csv_path, index=False)
    
    # 2. Export Protocol & Run Log JSON
    json_path = os.path.join(output_dir, "M1A_E001_protocol_log.json")
    log_data = {
        "lab_configuration": lab_config,
        "specimen": specimen_info,
        "total_samples": len(df),
        "qc_summary": df["QC_Status"].value_counts().to_dict(),
        "records": df.to_dict(orient="records")
    }
    with open(json_path, "w") as f:
        json.dump(log_data, f, indent=4)
        
    print(f"[Export Complete] Saved CSV to {csv_path}")
    print(f"[Export Complete] Saved JSON to {json_path}")
