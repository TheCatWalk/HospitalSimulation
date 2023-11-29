# Updated simulation parameters for Assignment 3
TIME_UNITS = 1000  # Total simulation time for each run
NUM_SAMPLES = 20   # Number of samples for each configuration
WARM_UP_TIME = 150 # Warm-up time before data collection

# Mean values for exponentially distributed times
INTERARRIVAL_TIME_MEAN = 25  # Mean interarrival time
PREPARATION_TIME_MEAN = 40   # Mean preparation time
OPERATION_TIME_MEAN = 20     # Mean operation time
RECOVERY_TIME_MEAN = 40      # Mean recovery time

# System configurations for the assignment
SYSTEM_CONFIGURATIONS = {
    '3p4r': {'P': 3, 'R': 4},
    '3p5r': {'P': 3, 'R': 5},
    '4p5r': {'P': 4, 'R': 5}
}
