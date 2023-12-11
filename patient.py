import simpy
import random
import config
from resources import Hospital

class Patient:
    def __init__(self, env, id, hospital, config_values):
        self.env = env
        self.id = id
        self.hospital = hospital
        self.config_values = config_values  # Store the configuration values
        env.process(self.process())

    def get_time_based_on_distribution(self, mean, dist_type):
        if dist_type == 'Unif':
            return random.uniform(config.UNIFORM_LOWER_LIMIT, config.UNIFORM_UPPER_LIMIT)
        else:  # Default to exponential
            return random.expovariate(1.0 / mean)

    def process(self):
        with self.hospital.preparation_rooms.request() as prep_req:
            yield prep_req
            prep_time = self.get_time_based_on_distribution(config.PREPARATION_TIME_MEAN, self.config_values['Preparation'])
            yield self.env.timeout(prep_time)

        with self.hospital.operating_theatre.request() as op_req:
            yield op_req
            self.hospital.data_collector.increment_operations()
            op_time = random.expovariate(1.0 / config.OPERATION_TIME_MEAN)  # Assuming operation time is always exponential
            yield self.env.timeout(op_time)

            if self.hospital.recovery_rooms.count == self.hospital.recovery_rooms.capacity:
                self.hospital.data_collector.record_blocking_event()

        with self.hospital.recovery_rooms.request() as rec_req:
            yield rec_req
            rec_time = self.get_time_based_on_distribution(config.RECOVERY_TIME_MEAN, self.config_values['Recovery'])
            yield self.env.timeout(rec_time)

def patient_arrival_process(env, hospital, config_values):
    patient_id = 1
    while True:
        interarrival_time = get_time_based_on_distribution(config.INTERARRIVAL_TIME_MEAN, config_values['Interarrival'])
        yield env.timeout(interarrival_time)
        Patient(env, patient_id, hospital, config_values)
        patient_id += 1

# Add a helper function to get time based on distribution
def get_time_based_on_distribution(mean, dist_type):
    if dist_type == 'Unif':
        return random.uniform(config.UNIFORM_LOWER_LIMIT, config.UNIFORM_UPPER_LIMIT)
    else:  # Default to exponential
        return random.expovariate(1.0 / mean)
