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

    # Additional methods for calculating metrics will be added later
