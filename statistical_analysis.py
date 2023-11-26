import numpy as np
from scipy import stats

def calculate_mean(data):
    return np.mean(data)

def calculate_confidence_interval(data, confidence=0.95):
    mean = np.mean(data)
    sem = stats.sem(data)
    margin = sem * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
    return mean - margin, mean + margin
