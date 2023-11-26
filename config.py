# Original Simulation parameters for Assignment 2 (May not be needed)
SIMULATION_TIME = 1000  # Total simulation time
P_TIME_RANGE = (5, 15)  # Range of time for Preparation phase (You may not need this anymore)
OT_TIME_RANGE = (10, 30)  # Range of time for Operation Theater phase (You may not need this anymore)
R_TIME_RANGE = (5, 20)  # Range of time for Recovery phase (You may not need this anymore)

# Queue and generation
QUEUE_BATCH_SIZE = 5  # Number of patients per batch
BATCH_INTERVAL = 0  # After which new batch is generated

# Resource capacities (These might be replaced by the SYSTEM_CONFIGURATIONS)
P_CAPACITY = 2  # Number of parallel preparation rooms
OT_CAPACITY = 1  # Number of operation theaters
R_CAPACITY = 100000  # Using a very high number to simulate 'infinite' capacity

# New simulation parameters for assignment 3
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

# Experiment setup for the assignment
TIME_UNITS = 1000
NUM_SAMPLES = 20
WARM_UP_TIME = 150
