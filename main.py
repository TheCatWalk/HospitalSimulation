import random
import simpy
from config import TIME_UNITS, SYSTEM_CONFIGURATIONS, NUM_SAMPLES
from queue import Queue
from resources import Preparation, OperationTheater, Recovery
from process_monitor import ProcessMonitor
from statistical_analysis import calculate_metrics


def hospital_simulation(config):
    env = simpy.Environment()
    queue = Queue(env)
    preparation = Preparation(env, config['P'])
    operation_theater = OperationTheater(env, 1)  # Only one OT
    recovery = Recovery(env, config['R'])
    process_monitor = ProcessMonitor(env, queue, preparation, operation_theater, recovery)

    env.run(until=TIME_UNITS)  # Run the simulation for the defined time units
    return process_monitor.data_collector


if __name__ == '__main__':
    for config_name, config_values in SYSTEM_CONFIGURATIONS.items():
        print(f"\nSimulation results for configuration: {config_name}")
        queue_lengths_all_runs = []
        blocking_probs_all_runs = []
        recovery_busy_probs_all_runs = []

        for sample_number in range(NUM_SAMPLES):
            random.seed(sample_number)
            data_collector = hospital_simulation(config_values)
            queue_lengths_all_runs.append(data_collector.queue_lengths if data_collector.queue_lengths else [0])

            blocking_prob = (data_collector.operation_blocking_events /
                             data_collector.total_operations if data_collector.total_operations > 0 else 0)
            blocking_probs_all_runs.append(blocking_prob)

            recovery_busy_prob = (data_collector.recovery_room_busy_counts /
                                  data_collector.recovery_room_check_counts if data_collector.recovery_room_check_counts > 0 else 0)
            recovery_busy_probs_all_runs.append(recovery_busy_prob)


        # Calculate and print metrics
        mean_queue_lengths, queue_sems, queue_margins, ci_queue_lengths = calculate_metrics([queue_lengths_all_runs])
        mean_blocking_probs, blocking_sems, blocking_margins, ci_blocking_probs = calculate_metrics([blocking_probs_all_runs])
        mean_recovery_busy_probs, recovery_busy_sems, recovery_busy_margins, ci_recovery_busy_probs = calculate_metrics([recovery_busy_probs_all_runs])

        print(f"Mean Queue Lengths: {mean_queue_lengths}, SEM: {queue_sems}, MoE: {queue_margins}, CI: {ci_queue_lengths}")
        print(f"Mean Blocking Probabilities: {mean_blocking_probs}, SEM: {blocking_sems}, MoE: {blocking_margins}, CI: {ci_blocking_probs}")
        print(f"Mean Recovery Room Busy Probabilities: {mean_recovery_busy_probs}, SEM: {recovery_busy_sems}, MoE: {recovery_busy_margins}, CI: {ci_recovery_busy_probs}")
