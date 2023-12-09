# config.py
# Configuration settings for the simulation

# Simulation Parameters
TIME_UNITS = 1000     # Execution time of a single iteration
NUM_SAMPLES = 20      # Number of times the simulation is repeated for each configuration
WARM_UP_TIME = 1000    # Warm-up period after which data is collected

# System Configurations
CONFIGURATIONS = ['3p4r', '3p5r', '4p5r']

# Exponential Distribution Mean Values
INTERARRIVAL_TIME_MEAN = 25
PREPARATION_TIME_MEAN = 40
OPERATION_TIME_MEAN = 20
RECOVERY_TIME_MEAN = 40

print("Configuration settings loaded.")