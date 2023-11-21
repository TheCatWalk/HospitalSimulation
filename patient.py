class Patient:
    id_counter = 0

    def __init__(self, env, p_time, ot_time, r_time):
        self.env = env
        self.p_time = p_time
        self.ot_time = ot_time
        self.r_time = r_time
        self.start_time = env.now
        self.end_time = None
        self.id = Patient.id_counter
        Patient.id_counter += 1

    def process(self):
        # EXpands in process_monitor
        pass
