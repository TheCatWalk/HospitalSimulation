import simpy
from config import WARM_UP_TIME
from data_collector import DataCollector

class ProcessMonitor:
    def __init__(self, env, queue, preparation, operation_theater, recovery):
        self.data_collector = DataCollector()
        self.env = env
        self.queue = queue
        self.preparation = preparation
        self.operation_theater = operation_theater
        self.recovery = recovery
        env.process(self.manage_patient_flow())

    def manage_patient_flow(self):
        while True:
            if self.env.now > WARM_UP_TIME and not self.queue.is_empty():
                patient = yield self.queue.patients.get()
                self.env.process(self.handle_patient(patient))
            yield self.env.timeout(1)

    def handle_patient(self, patient):
        # Handling preparation phase
        with self.preparation.resource.request() as req:
            yield req
            yield self.env.timeout(patient.p_time)

        # Handling operation phase
        is_recovery_busy = len(self.recovery.resource.users) == self.recovery.resource.capacity
        self.data_collector.record_operation_blocking(is_recovery_busy)
        with self.operation_theater.resource.request() as req:
            yield req
            yield self.env.timeout(patient.ot_time)

        # Handling recovery phase
        with self.recovery.resource.request() as req:
            yield req
            yield self.env.timeout(patient.r_time)
        is_recovery_busy = len(self.recovery.resource.users) == self.recovery.resource.capacity
        self.data_collector.record_recovery_room_busy(is_recovery_busy)
