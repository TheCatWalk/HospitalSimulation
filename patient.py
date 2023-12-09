# patient.py
import simpy
import random
import config
from resources import Hospital

class Patient:
    def __init__(self, env, id, hospital):
        self.env = env
        self.id = id
        self.hospital = hospital
        env.process(self.process())

    def process(self):
        print(f"Patient {self.id} arrives at time {self.env.now}.")
        with self.hospital.preparation_rooms.request() as prep_req:
            yield prep_req
            print(f"Patient {self.id} enters preparation at time {self.env.now}.")
            yield self.env.timeout(random.expovariate(1.0 / config.PREPARATION_TIME_MEAN))
            print(f"Patient {self.id} leaves preparation at time {self.env.now}.")

        # Operation Process
        with self.hospital.operating_theatre.request() as op_req:
            yield op_req
            self.hospital.data_collector.increment_operations()  # Increment operation count here
            print(f"Patient {self.id} enters operation at time {self.env.now}.")
            yield self.env.timeout(random.expovariate(1.0 / config.OPERATION_TIME_MEAN))
            print(f"Patient {self.id} finishes operation at time {self.env.now}.")

            # Check for blocking
            if self.hospital.recovery_rooms.count == self.hospital.recovery_rooms.capacity:
                self.hospital.data_collector.record_blocking_event()
                print(f"Blocking event recorded for Patient {self.id} at time {self.env.now}.")


                # Recovery Process
        with self.hospital.recovery_rooms.request() as rec_req:
            yield rec_req
            print(f"Patient {self.id} enters recovery at time {self.env.now}.")
            yield self.env.timeout(random.expovariate(1.0 / config.RECOVERY_TIME_MEAN))
            print(f"Patient {self.id} leaves recovery at time {self.env.now}.")

def patient_arrival_process(env, hospital):
    patient_id = 1
    while True:
        yield env.timeout(random.expovariate(1.0 / config.INTERARRIVAL_TIME_MEAN))
        Patient(env, patient_id, hospital)
        patient_id += 1
