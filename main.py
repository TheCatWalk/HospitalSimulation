import simpy
import config
from patient import patient_arrival_process
from resources import Hospital
from data_collector import DataCollector
from process_monitor import monitor_preparation_queue, monitor_blocking_probability
import statistical_analysis as sa
from statistical_analysis import calculate_serial_correlation, compare_autocorrelation
import pandas as pd
import random
import os
import matplotlib.pyplot as plt
from datetime import datetime

current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")

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
    data_collectors = []

    for _ in range(config.NUM_SAMPLES):
        env = simpy.Environment()
        data_collector = DataCollector()
        hospital = Hospital(env, configuration, data_collector)
        env.process(patient_arrival_process(env, hospital))
        env.process(monitor_preparation_queue(env, hospital, data_collector))
        env.process(monitor_blocking_probability(env, hospital, data_collector))
        env.run(until=config.TIME_UNITS)
        avg_queue_length, blocking_probability = data_collector.get_average_queue_length(), data_collector.calculate_blocking_probability()
        queue_lengths.append(avg_queue_length)
        blocking_probabilities.append(blocking_probability)
        data_collectors.append(data_collector)

    queue_length_series = [[length for _, length in dc.time_series_data] for dc in data_collectors]
    return queue_lengths, blocking_probabilities, queue_length_series

def format_dataframe(df, headers):
    formatter = lambda x: f"{float(x):.4f}" if isinstance(x, (int, float)) else x
    formatted_df = df.copy()
    for column in df.columns[1:]:
        formatted_df[column] = df[column].apply(formatter)

    formatted_str = " ".join(f"[{header}]" for header in headers) + "\n"
    for _, row in formatted_df.iterrows():
        formatted_str += " ".join(f"[{row[col]}]" for col in df.columns) + "\n"
    return formatted_str

def plot_autocorrelation(data, max_lag=20):
    autocorrelations = [calculate_serial_correlation(data, lag) for lag in range(1, max_lag + 1)]
    plt.stem(range(1, max_lag + 1), autocorrelations)
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation Function')

def main():
    print("Starting simulation...")
    simulation_results = {}
    seed = random.random()
    print("Seed is:", seed)

    ql_results = pd.DataFrame(columns=['Configuration', 'QL mean x̄', 'QL-Standard Deviation σ', 'QL-Confidence interval (95%)'])
    bp_results = pd.DataFrame(columns=['Configuration', 'BP mean x̄', 'BP-Standard Deviation σ', 'BP-Confidence interval (95%)'])

    autocorrelation_data = {}

    for config_name, config_values in config.EXPERIMENT_CONFIGS.items():
        print(f"\nRunning simulation for configuration: {config_name}")
        interarrival = config_values['Interarrival']
        preparation = config_values['Preparation']
        recovery = config_values['Recovery']
        prep_units = config_values['PrepUnits']
        recovery_units = config_values['RecoveryUnits']

        configuration = f"{prep_units}p{recovery_units}r"

        config_dir = f"results/{config_name}"
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)

        queue_lengths, blocking_probabilities, all_series = multiple_runs(configuration, seed)


        mean_ql = sa.calculate_mean(queue_lengths)
        std_ql = sa.calculate_std(queue_lengths)
        ci_ql = sa.calculate_confidence_interval(queue_lengths)

        mean_bp = sa.calculate_mean(blocking_probabilities)
        std_bp = sa.calculate_std(blocking_probabilities)
        ci_bp = sa.calculate_confidence_interval(blocking_probabilities)

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
            'std_bp': std_bp
        }

        autocorrelations_list = []
        for series_index, series in enumerate(all_series):
            autocorrelations = [calculate_serial_correlation(series, lag) for lag in range(1, 21)]
            autocorrelations_list.append(autocorrelations)
            plt.figure()
            plt.stem(range(1, 21), autocorrelations)
            plt.xlabel('Lag')
            plt.ylabel('Autocorrelation')
            plt.title(f'Autocorrelation Function for {config_name} - Series {series_index}')
            plt.savefig(f'{config_dir}/autocorrelation_series{series_index}_{current_datetime}.png')
            plt.close()


        # # Diagnostic print to check the time series data
        # print(f"\nTime Series Data Sample for {config_name}:")
        # for i, series in enumerate(all_series):
        #     print(f"Series {i}: {series[:10]}")  # Print the first 10 elements of each series

        avg_autocorrelations = [sum(x)/len(x) for x in zip(*autocorrelations_list)]
        autocorrelation_data[config_name] = avg_autocorrelations

        pd.DataFrame({'Queue Lengths': queue_lengths}).to_csv(f'{config_dir}/queue_lengths_{current_datetime}.csv', index=False)
        pd.DataFrame({'Blocking Probabilities': blocking_probabilities}).to_csv(f'{config_dir}/blocking_probabilities_{current_datetime}.csv', index=False)

    ql_headers = ['Configuration', 'QL mean x̄', 'QL-Standard Deviation σ', 'QL-Confidence interval (95%)']
    bp_headers = ['Configuration', 'BP mean x̄', 'BP-Standard Deviation σ', 'BP-Confidence interval (95%)']

    # Define the folder name
    output_folder = 'qlbpOutput'

    # Check if the folder exists, and create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Save ql_results to a CSV file inside the 'qlbpOutput' folder with the current date and time
    ql_results.to_csv(os.path.join(output_folder, f'queue_length_results_{current_datetime}.csv'), index=False)

    # Save bp_results to a CSV file inside the 'qlbpOutput' folder with the current date and time
    bp_results.to_csv(os.path.join(output_folder, f'blocking_probability_results_{current_datetime}.csv'), index=False)


    print("\nQueue Length Results:")
    formatted_ql_results = format_dataframe(ql_results, ql_headers)
    print(formatted_ql_results)

    print("\nBlocking Probability Results:")
    formatted_bp_results = format_dataframe(bp_results, bp_headers)
    print(formatted_bp_results)

    print("\nAll simulations completed.")

    print("\nPairwise Comparison Results:")
    comparison_results = sa.pairwise_comparison(simulation_results)
    pairwise_df = pd.DataFrame(comparison_results,
                               columns=['Configurations', 'Difference in Queue Length mean',
                                        'Difference in QL-Confidence interval',
                                        'Difference in Blocking Probability',
                                        'Difference in BP-Confidence interval'])
    formatted_pairwise_results = format_dataframe(pairwise_df, pairwise_df.columns)
    print(formatted_pairwise_results)

    print("Pairwise comparison completed.")

    # print("\nAutocorrelation Comparisons:")
    # for i, config1 in enumerate(config.EXPERIMENT_CONFIGS):
    #     for config2 in list(config.EXPERIMENT_CONFIGS)[i+1:]:
    #         comparison_results = compare_autocorrelation(autocorrelation_data[config1], autocorrelation_data[config2])
    #         print(f"\nComparison between {config1} and {config2}:")
    #         for result in comparison_results:
    #             lag, ac1, ac2, diff = result
    #             print(f"Lag {lag}: {config1}={ac1:.4f}, {config2}={ac2:.4f}, Difference={diff:.4f}")


if __name__ == "__main__":
    main()
