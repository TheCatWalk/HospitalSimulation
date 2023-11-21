# Simulation parameters
SIMULATION_TIME = 500  # Total simulation time
P_TIME_RANGE = (5, 15)  # Range of time for Preparation phase
OT_TIME_RANGE = (10, 30)  # Range of time for Operation Theater phase
R_TIME_RANGE = (5, 20)  # Range of time for Recovery phase

# Queue and generation
QUEUE_BATCH_SIZE = 5  # Number of patients per batch
BATCH_INTERVAL = 0  # After which new batch is generated

# Resource capacities
P_CAPACITY = 1  # Number of parallel preparation rooms
OT_CAPACITY = 1  # Number of operation theaters
R_CAPACITY = 100000  # Using a very high number to simulate 'infinite' capacity

