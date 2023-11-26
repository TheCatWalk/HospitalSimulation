# import simpy
# from queue import Queue
# from process_monitor import ProcessMonitor
# from resources import Preparation, OperationTheater, Recovery
# from config import SIMULATION_TIME
#
# def hospital_simulation():
#     env = simpy.Environment()
#     queue = Queue(env)
#     preparation = Preparation(env)
#     operation_theater = OperationTheater(env)
#     recovery = Recovery(env)
#     process_monitor = ProcessMonitor(env, queue, preparation, operation_theater, recovery)
#     env.run(until=SIMULATION_TIME)
#
# if __name__ == '__main__':
#     hospital_simulation()

import simpy
import random
from config import TIME_UNITS, WARM_UP_TIME, SYSTEM_CONFIGURATIONS, NUM_SAMPLES
from queue import Queue
from process_monitor import ProcessMonitor
from resources import Preparation, OperationTheater, Recovery
from statistical_analysis import calculate_mean, calculate_confidence_interval

def hospital_simulation(config):
    env = simpy.Environment()
    queue = Queue(env)
    preparation = Preparation(env, config['P'])
    operation_theater = OperationTheater(env, 1)  # Only one OT
    recovery = Recovery(env, config['R'])
    process_monitor = ProcessMonitor(env, queue, preparation, operation_theater, recovery)

    env.run(until=TIME_UNITS)

    # After simulation run, perform statistical analysis
    queue_lengths, blocking_probs, recovery_busy_probs = process_monitor.data_collector.calculate_metrics()

    # Statistical Analysis
    mean_queue_length = calculate_mean(queue_lengths)
    conf_interval_queue_length = calculate_confidence_interval(queue_lengths)

    mean_blocking_prob = calculate_mean(blocking_probs)
    conf_interval_blocking_prob = calculate_confidence_interval(blocking_probs)

    mean_recovery_busy_prob = calculate_mean(recovery_busy_probs)
    conf_interval_recovery_busy_prob = calculate_confidence_interval(recovery_busy_probs)

    # Print Results
    print(f"Mean Queue Length: {mean_queue_length}")
    print(f"Confidence Interval for Queue Length: {conf_interval_queue_length}")

    print(f"Mean Blocking Probability: {mean_blocking_prob}")
    print(f"Confidence Interval for Blocking Probability: {conf_interval_blocking_prob}")

    print(f"Mean Recovery Room Busy Probability: {mean_recovery_busy_prob}")
    print(f"Confidence Interval for Recovery Room Busy Probability: {conf_interval_recovery_busy_prob}")

if __name__ == '__main__':
    for config_name, config_values in SYSTEM_CONFIGURATIONS.items():
        print(f"Running simulation for configuration: {config_name}")
        for sample_number in range(NUM_SAMPLES):
            random.seed(sample_number)  # Set a consistent seed for each run
            hospital_simulation(config_values)
