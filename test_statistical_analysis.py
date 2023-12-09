# test_statistical_analysis.py
from statistical_analysis import calculate_mean, calculate_confidence_interval

# Sample data arrays for testing
sample_queue_lengths = [2.5, 3.0, 3.5, 2.0, 4.0, 3.5, 2.5, 3.0, 4.5, 3.5]
sample_blocking_probabilities = [0.2, 0.25, 0.15, 0.3, 0.2, 0.25, 0.1, 0.2, 0.25, 0.3]

# Calculate and print mean and confidence interval for queue lengths
mean_queue_length = calculate_mean(sample_queue_lengths)
ci_queue_length = calculate_confidence_interval(sample_queue_lengths)
print(f"Mean Queue Length: {mean_queue_length}, CI: {ci_queue_length}")

# Calculate and print mean and confidence interval for blocking probabilities
mean_blocking_probability = calculate_mean(sample_blocking_probabilities)
ci_blocking_probability = calculate_confidence_interval(sample_blocking_probabilities)
print(f"Mean Blocking Probability: {mean_blocking_probability}, CI: {ci_blocking_probability}")
