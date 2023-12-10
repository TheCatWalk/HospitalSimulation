# data_collector.py

class DataCollector:
    def __init__(self):
        self.queue_lengths = []
        self.time_series_data = []  # New attribute for time series data
        self.blocking_events = 0
        self.total_operations = 0  # Ensure this is incremented for each operation

    def record_queue_length(self, length):
        self.queue_lengths.append(length)

    def get_average_queue_length(self):
        if not self.queue_lengths:
            return 0
        return sum(self.queue_lengths) / len(self.queue_lengths)

    def record_blocking_event(self):
        self.blocking_events += 1
        # print(f"Blocking event recorded. Total blocking events: {self.blocking_events}")

    def increment_operations(self):
        self.total_operations += 1
        # print(f"Total operations: {self.total_operations}")  # For debugging

    def calculate_blocking_probability(self):
        if self.total_operations == 0:
            return 0
        return self.blocking_events / self.total_operations

    def record_time_series_data(self, time, length):
        self.time_series_data.append((time, length))
