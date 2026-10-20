"""
Virtual Fructosamine Assay Instrument Simulation
"""

import numpy as np

def virtual_fructosamine_assay(glycated_conc, noise_level=0.02, gain=1.25, baseline=0.05):
    """
    Transforms chemical concentration into an optical signal (Absorbance @ 540nm).
    """
    true_signal = baseline + (glycated_conc * gain)
    noise = np.random.normal(0, noise_level * true_signal) if true_signal > 0 else 0
    observed_signal = max(0.0, true_signal + noise)
    return round(observed_signal, 4)
