"""
Control Definitions
"""

CONTROLS = {
    "C0": {
        "name": "Negative Protein Control",
        "description": "Albumin + buffer without experimental glucose exposure",
        "type": "NEGATIVE"
    },
    "C1": {
        "name": "Reagent Blank",
        "description": "Buffer matrix without albumin",
        "type": "BLANK"
    },
    "C2": {
        "name": "Positive Virtual Glycation Control",
        "description": "Albumin assigned a high simulated glycation state",
        "type": "POSITIVE",
        "classification": "SIMULATED"
    }
}
