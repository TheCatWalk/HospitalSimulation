# resources.py
import simpy
import config
from data_collector import DataCollector

class Hospital:
    def __init__(self, env, config_name, data_collector):
        self.env = env
        self.data_collector = data_collector
        prep_rooms, recovery_rooms = self.parse_configuration(config_name)
        self.preparation_rooms = simpy.Resource(env, capacity=prep_rooms)
        self.operating_theatre = simpy.Resource(env, capacity=1)  # Assuming one operating theatre
        self.recovery_rooms = simpy.Resource(env, capacity=recovery_rooms)

    def parse_configuration(self, config_name):
        # Split the configuration name at 'p' and 'r'
        parts = config_name.split('p')
        prep = parts[0]  # Number before 'p'
        recovery = parts[1].split('r')[0]  # Number before 'r'
        return int(prep), int(recovery)
