import simpy
from queue import Queue
from process_monitor import ProcessMonitor
from resources import Preparation, OperationTheater, Recovery
from config import SIMULATION_TIME

def hospital_simulation():
    env = simpy.Environment()
    queue = Queue(env)
    preparation = Preparation(env)
    operation_theater = OperationTheater(env)
    recovery = Recovery(env)
    process_monitor = ProcessMonitor(env, queue, preparation, operation_theater, recovery)
    env.run(until=SIMULATION_TIME)

if __name__ == '__main__':
    hospital_simulation()
