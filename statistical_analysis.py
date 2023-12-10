# statistical_analysis.py
import numpy as np
import config
def calculate_mean(data):
    return np.mean(data)

def calculate_std(data):
    return np.sqrt(np.sum((data - np.mean(data)) ** 2) / len(data))

def calculate_confidence_interval(data):
    mean = calculate_mean(data)
    std = calculate_std(data)
    n = len(data)
    z = 1.69  # z-value for 95% confidence interval
    margin_of_error = z * (std / np.sqrt(n))
    return mean - margin_of_error, mean + margin_of_error

def calculate_difference_ci(mean1, std1, n1, mean2, std2, n2):
    mean_diff = mean1 - mean2
    std_diff = np.sqrt(std1**2 / n1 + std2**2 / n2)
    z = 1.69  # z-value for 95% confidence interval
    margin_of_error = z * std_diff
    return mean_diff - margin_of_error, mean_diff + margin_of_error

def pairwise_comparison(results):
    comparison_results = []
    configurations = list(results.keys())

    for i in range(len(configurations) - 1):
        for j in range(i + 1, len(configurations)):
            config_1 = configurations[i]
            config_2 = configurations[j]

            # Calculate differences and confidence intervals
            diff_ql_mean = results[config_1]['mean_ql'] - results[config_2]['mean_ql']
            diff_bp_mean = results[config_1]['mean_bp'] - results[config_2]['mean_bp']
            ci_ql_diff = calculate_difference_ci(results[config_1]['mean_ql'], results[config_1]['std_ql'], config.NUM_SAMPLES,
                                                 results[config_2]['mean_ql'], results[config_2]['std_ql'], config.NUM_SAMPLES)
            ci_bp_diff = calculate_difference_ci(results[config_1]['mean_bp'], results[config_1]['std_bp'], config.NUM_SAMPLES,
                                                 results[config_2]['mean_bp'], results[config_2]['std_bp'], config.NUM_SAMPLES)

            comparison_results.append((f"{config_1} & {config_2}", diff_ql_mean, ci_ql_diff, diff_bp_mean, ci_bp_diff))

    return comparison_results

def calculate_serial_correlation(data, lag=1):
    n = len(data)
    mean = np.mean(data)
    total = 0
    denom = 0
    for i in range(n - lag):
        total += (data[i] - mean) * (data[i + lag] - mean)
    for i in range(n):
        denom += (data[i] - mean) ** 2
    return total / denom
