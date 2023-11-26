# import simpy
# from config import P_CAPACITY, OT_CAPACITY, R_CAPACITY
#
# class Preparation:
#     def __init__(self, env):
#         self.resource = simpy.Resource(env, capacity=P_CAPACITY)
#
# class OperationTheater:
#     def __init__(self, env):
#         self.resource = simpy.Resource(env, capacity=OT_CAPACITY)
#
# class Recovery:
#     def __init__(self, env):
#         self.resource = simpy.Resource(env, capacity=R_CAPACITY)

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
