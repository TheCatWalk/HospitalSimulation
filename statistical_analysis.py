import numpy as np
from scipy import stats


def calculate_mean(data):
    return np.mean(data)


def calculate_sem(data):
    return stats.sem(data)


def calculate_confidence_interval(data, confidence=0.95):
    mean = calculate_mean(data)
    sem = calculate_sem(data)
    margin = sem * stats.t.ppf((1 + confidence) / 2, len(data) - 1)
    return mean - margin, mean + margin


def calculate_metrics(data_collections):
    means = []
    sems = []
    margins = []
    confidence_intervals = []
    for data in data_collections:
        mean = calculate_mean(data)
        sem = calculate_sem(data)
        conf_interval = calculate_confidence_interval(data)
        margin = sem * stats.t.ppf((1 + 0.95) / 2, len(data) - 1)

        means.append(mean)
        sems.append(sem)
        margins.append(margin)
        confidence_intervals.append(conf_interval)
    return means, sems, margins, confidence_intervals
