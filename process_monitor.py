import simpy
from config import BATCH_INTERVAL
from data_collector import DataCollector
class ProcessMonitor:
    def __init__(self, env, queue, preparation, operation_theater, recovery):
        self.data_collector = DataCollector()
        self.env = env
        self.queue = queue
        self.preparation = preparation
        self.operation_theater = operation_theater
        self.recovery = recovery
        self.last_batch_generated_at = 0
        env.process(self.manage_patient_flow())

    def manage_patient_flow(self):
        while True:
            if self.should_generate_new_batch():
                self.queue.generate_patient_batch()
                self.last_batch_generated_at = self.env.now

            if not self.queue.is_empty():
                patient = yield self.queue.patients.get()
                yield self.env.process(self.handle_patient(patient))

            yield self.env.timeout(1)  # Check periodically

    def should_generate_new_batch(self):
        return self.env.now - self.last_batch_generated_at >= BATCH_INTERVAL \
            and self.is_ot_available() \
            and self.queue.is_empty()

    def is_ot_available(self):
        return len(self.operation_theater.resource.queue) == 0 \
            and self.operation_theater.resource.count == 0


    def handle_patient(self, patient):
        # print(f"Patient {patient.id} entering P at System time {self.env.now}")
        with self.preparation.resource.request() as req:
            yield req
            yield self.env.timeout(patient.p_time)
        # print(f"Patient {patient.id} entering OT at System time {self.env.now}")

        with self.operation_theater.resource.request() as req:
            yield req
            yield self.env.timeout(patient.ot_time)
        # print(f"Patient {patient.id} entering R at System time {self.env.now}")

        with self.recovery.resource.request() as req:
            yield req
            yield self.env.timeout(patient.r_time)
        # print(f"Patient {patient.id} completed at System time {self.env.now}")

        patient.end_time = self.env.now
        throughput_time = patient.end_time - patient.start_time
        facility_time = patient.p_time + patient.ot_time + patient.r_time
        # Record queue length
        self.data_collector.record_queue_length(len(self.queue.patients.items))

        # Record operation blocking
        is_recovery_busy = len(self.recovery.resource.users) == self.recovery.resource.capacity
        self.data_collector.record_operation_blocking(is_recovery_busy)

        # Record recovery room busy state
        if is_recovery_busy:
            self.data_collector.record_recovery_room_busy()

        #print(f"Total throughput time for Patient {patient.id}: {throughput_time}")
        #print(f"Total facility time for Patient {patient.id}: {facility_time}")