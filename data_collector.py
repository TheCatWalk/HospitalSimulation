class DataCollector:
    def __init__(self):
        self.queue_lengths = []
        self.operation_blocking_events = 0
        self.total_operations = 0
        self.recovery_room_busy_counts = 0
        self.recovery_room_check_counts = 0

    def record_queue_length(self, length):
        self.queue_lengths.append(length)

    def record_operation_blocking(self, is_blocked):
        if is_blocked:
            self.operation_blocking_events += 1
        self.total_operations += 1

    def record_recovery_room_busy(self, is_busy):
        if is_busy:
            self.recovery_room_busy_counts += 1
        self.recovery_room_check_counts += 1

    def calculate_metrics(self):
        avg_queue_length = sum(self.queue_lengths) / len(self.queue_lengths) if self.queue_lengths else 0
        blocking_probability = (self.operation_blocking_events / self.total_operations) if self.total_operations else 0
        recovery_room_busy_probability = (self.recovery_room_busy_counts / self.recovery_room_check_counts) if self.recovery_room_check_counts else 0
        return self.queue_lengths, [blocking_probability] * len(self.queue_lengths), [recovery_room_busy_probability] * len(self.queue_lengths)
