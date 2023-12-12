# config.py
# Configuration settings for the simulation

# Simulation Parameters
TIME_UNITS = 1000     # Execution time of a single iteration
NUM_SAMPLES = 20      # Number of times the simulation is repeated for each configuration
WARM_UP_TIME = 1000    # Warm-up period after which data is collected

# System Configurations
CONFIGURATIONS = ['3p4r', '3p5r', '4p5r']

# Exponential Distribution Mean Values
INTERARRIVAL_TIME_MEAN = 5
PREPARATION_TIME_MEAN = 40
OPERATION_TIME_MEAN = 20
RECOVERY_TIME_MEAN = 40

# Uniform Distribution Limits (used if DISTRIBUTION_TYPE is 'uniform')
UNIFORM_LOWER_LIMIT = 15
UNIFORM_UPPER_LIMIT = 35

EXPERIMENT_CONFIGS = {
    'Config1': {'Interarrival': 'Exp', 'Preparation': 'Exp', 'Recovery': 'Exp', 'PrepUnits': 4, 'RecoveryUnits': 4},
    'Config2': {'Interarrival': 'Exp', 'Preparation': 'Exp', 'Recovery': 'Unif', 'PrepUnits': 5, 'RecoveryUnits': 5},
    'Config3': {'Interarrival': 'Unif', 'Preparation': 'Unif', 'Recovery': 'Exp', 'PrepUnits': 4, 'RecoveryUnits': 5},
    'Config4': {'Interarrival': 'Unif', 'Preparation': 'Unif', 'Recovery': 'Unif', 'PrepUnits': 5, 'RecoveryUnits': 4},
    'Config5': {'Interarrival': 'Exp', 'Preparation': 'Unif', 'Recovery': 'Exp', 'PrepUnits': 5, 'RecoveryUnits': 4},
    'Config6': {'Interarrival': 'Exp', 'Preparation': 'Unif', 'Recovery': 'Unif', 'PrepUnits': 4, 'RecoveryUnits': 5},
    'Config7': {'Interarrival': 'Unif', 'Preparation': 'Exp', 'Recovery': 'Exp', 'PrepUnits': 5, 'RecoveryUnits': 5},
    'Config8': {'Interarrival': 'Unif', 'Preparation': 'Exp', 'Recovery': 'Unif', 'PrepUnits': 4, 'RecoveryUnits': 4}
}

print("Configuration settings loaded.")