import simpy

class Preparation:
    def __init__(self, env, capacity):
        self.resource = simpy.Resource(env, capacity=capacity)

class OperationTheater:
    def __init__(self, env, capacity):
        self.resource = simpy.Resource(env, capacity=capacity)

class Recovery:
    def __init__(self, env, capacity):
        self.resource = simpy.Resource(env, capacity=capacity)
