# main.py
import simpy
import config
from config import NUM_SAMPLES
from patient import patient_arrival_process
from resources import Hospital
from data_collector import DataCollector
from process_monitor import monitor_preparation_queue, monitor_blocking_probability
import statistical_analysis as sa
import pandas as pd
import random
import os


def run_simulation(configuration, env, seed):
    random.seed(seed)
    data_collector = DataCollector()
    hospital = Hospital(env, configuration, data_collector)
    env.process(patient_arrival_process(env, hospital))
    env.process(monitor_preparation_queue(env, hospital, data_collector))
    env.process(monitor_blocking_probability(env, hospital, data_collector))
    env.run(until=config.TIME_UNITS)
    return data_collector.get_average_queue_length(), data_collector.calculate_blocking_probability()

def multiple_runs(configuration, seed):
    queue_lengths = []
    blocking_probabilities = []

    for _ in range(config.NUM_SAMPLES):
        env = simpy.Environment()
        avg_queue_length, blocking_probability = run_simulation(configuration, env, seed)
        queue_lengths.append(avg_queue_length)
        blocking_probabilities.append(blocking_probability)

    return queue_lengths, blocking_probabilities

def format_dataframe(df, headers):
    # Define a formatter function for numerical values
    formatter = lambda x: f"{float(x):.4f}" if isinstance(x, (int, float)) else x

    # Format each column
    formatted_df = df.copy()
    for column in df.columns[1:]:  # Skip the 'Configuration' column
        formatted_df[column] = df[column].apply(formatter)

    # Construct the formatted string with headers
    formatted_str = " ".join(f"[{header}]" for header in headers) + "\n"
    for _, row in formatted_df.iterrows():
        formatted_str += " ".join(f"[{row[col]}]" for col in df.columns) + "\n"

    return formatted_str

def main():
    print("Starting simulation...")
    simulation_results = {}
    seed = random.random()
    print("Seed is:", seed)


# Dataframes to store the results
    ql_results = pd.DataFrame(columns=['Configuration', 'QL mean x̄', 'QL-Standard Deviation σ', 'QL-Confidence interval (95%)'])
    bp_results = pd.DataFrame(columns=['Configuration', 'BP mean x̄', 'BP-Standard Deviation σ', 'BP-Confidence interval (95%)'])

    for configuration in config.CONFIGURATIONS:
        queue_lengths, blocking_probabilities = multiple_runs(configuration, seed)

        # Calculate mean, standard deviation, and confidence intervals
        mean_ql = sa.calculate_mean(queue_lengths)
        std_ql = sa.calculate_std(queue_lengths)
        ci_ql = sa.calculate_confidence_interval(queue_lengths)

        mean_bp = sa.calculate_mean(blocking_probabilities)
        std_bp = sa.calculate_std(blocking_probabilities)
        ci_bp = sa.calculate_confidence_interval(blocking_probabilities)

        # Append results to the dataframes
        ql_results = ql_results._append({'Configuration': configuration,
                                        'QL mean x̄': mean_ql,
                                        'QL-Standard Deviation σ': std_ql,
                                        'QL-Confidence interval (95%)': f"({ci_ql[0]:.2f}, {ci_ql[1]:.2f})"},
                                       ignore_index=True)
        bp_results = bp_results._append({'Configuration': configuration,
                                        'BP mean x̄': mean_bp,
                                        'BP-Standard Deviation σ': std_bp,
                                        'BP-Confidence interval (95%)': f"({ci_bp[0]:.2f}, {ci_bp[1]:.2f})"},
                                       ignore_index=True)
        simulation_results[configuration] = {
            'mean_ql': mean_ql,
            'std_ql': std_ql,
            'mean_bp': mean_bp,
            'std_bp': std_bp,
            # ... [store other statistics if necessary] ...
        }

    ql_headers = ['Configuration', 'QL mean x̄', 'QL-Standard Deviation σ', 'QL-Confidence interval (95%)']
    bp_headers = ['Configuration', 'BP mean x̄', 'BP-Standard Deviation σ', 'BP-Confidence interval (95%)']

    print("\nQueue Length Results:")
    formatted_ql_results = format_dataframe(ql_results, ql_headers)
    print(formatted_ql_results)

    print("\nBlocking Probability Results:")
    formatted_bp_results = format_dataframe(bp_results, bp_headers)
    print(formatted_bp_results)

    print("\nAll simulations completed.")

    print("\nPairwise Comparison Results:")
    comparison_results = sa.pairwise_comparison(simulation_results)

    # Creating a DataFrame for pairwise comparison results
    pairwise_df = pd.DataFrame(comparison_results,
                               columns=['Configurations', 'Difference in Queue Length mean',
                                        'Difference in QL-Confidence interval',
                                        'Difference in Blocking Probability',
                                        'Difference in BP-Confidence interval'])

    # Formatting and printing the DataFrame
    formatted_pairwise_results = format_dataframe(pairwise_df, pairwise_df.columns)
    print(formatted_pairwise_results)

    print("Pairwise comparison completed.")

if __name__ == "__main__":
    main()
