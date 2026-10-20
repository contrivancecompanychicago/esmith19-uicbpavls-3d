"""
Phenomenological Model for Early Glycation (Schiff Base & Amadori Product Formation)
"""

import numpy as np

def simulate_glycation(glucose_mg_dL, time_min, temp_c=37.0, ph=7.40, k_rate=0.00015):
    """
    Simulates early albumin glycation yielding fructosamine precursor concentration (uM).
    """
    temp_factor = 1.0 + 0.03 * (temp_c - 37.0)
    ph_factor = 1.0 + 0.1 * (ph - 7.40)
    effective_rate = k_rate * temp_factor * ph_factor
    
    # Second-order kinetic simplification for early-phase adduct formation
    adduct_conc = glucose_mg_dL * (1 - np.exp(-effective_rate * time_min))
    return adduct_conc
