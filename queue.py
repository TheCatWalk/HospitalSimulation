import simpy
import numpy as np
from patient import Patient
from config import INTERARRIVAL_TIME_MEAN, PREPARATION_TIME_MEAN, OPERATION_TIME_MEAN, RECOVERY_TIME_MEAN

class Queue:
    def __init__(self, env):
        self.env = env
        self.patients = simpy.Store(env)
        self.env.process(self.generate_patients())

    def generate_patients(self):
        while True:
            # Exponentially distributed interarrival times
            yield self.env.timeout(np.random.exponential(INTERARRIVAL_TIME_MEAN))
            patient = Patient(self.env, np.random.exponential(PREPARATION_TIME_MEAN),
                              np.random.exponential(OPERATION_TIME_MEAN),
                              np.random.exponential(RECOVERY_TIME_MEAN))
            self.patients.put(patient)

    def is_empty(self):
        return len(self.patients.items) == 0
