# main.py
import simpy
import config
from patient import patient_arrival_process
from resources import Hospital
from data_collector import DataCollector
from process_monitor import monitor_preparation_queue, monitor_blocking_probability

def run_simulation(configuration, env):
    print(f"Running simulation for configuration: {configuration}")
    data_collector = DataCollector()
    hospital = Hospital(env, configuration, data_collector)
    env.process(patient_arrival_process(env, hospital))
    env.process(monitor_preparation_queue(env, hospital, data_collector))
    env.process(monitor_blocking_probability(env, hospital, data_collector))
    env.run(until=config.TIME_UNITS)
    print(f"Average Queue Length: {data_collector.get_average_queue_length()}")
    print(f"Blocking Probability: {data_collector.calculate_blocking_probability()}")
    print("Simulation complete for this configuration.\n")

def main():
    print("Starting simulation...")
    for configuration in config.CONFIGURATIONS:
        env = simpy.Environment()
        run_simulation(configuration, env)

    print("All simulations completed.")

if __name__ == "__main__":
    main()
