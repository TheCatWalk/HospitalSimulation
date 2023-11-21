import simpy
import random
from patient import Patient
from config import P_TIME_RANGE, OT_TIME_RANGE, R_TIME_RANGE, QUEUE_BATCH_SIZE

class Queue:
    def __init__(self, env):
        self.env = env
        self.patients = simpy.Store(env)

    def generate_patient_batch(self):
        for _ in range(QUEUE_BATCH_SIZE):
            p_time = random.randint(*P_TIME_RANGE)
            ot_time = random.randint(*OT_TIME_RANGE)
            r_time = random.randint(*R_TIME_RANGE)
            patient = Patient(self.env, p_time, ot_time, r_time)
            self.patients.put(patient)

    def is_empty(self):
        return len(self.patients.items) == 0
