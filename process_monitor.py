# process_monitor.py
import simpy
from data_collector import DataCollector

def monitor_preparation_queue(env, hospital, data_collector):
    while True:
        yield env.timeout(1)  # Check queue length at regular intervals
        queue_length = len(hospital.preparation_rooms.queue)
        data_collector.record_queue_length(queue_length)

def monitor_blocking_probability(env, hospital, data_collector):
    while True:
        yield env.timeout(1)  # Monitor at regular intervals
        if hospital.operating_theatre.count == 0 and len(hospital.recovery_rooms.queue) >= hospital.recovery_rooms.capacity:
            data_collector.record_blocking_event()
