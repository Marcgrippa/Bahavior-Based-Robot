from arbitrator import Arbitrator

class Bbcon():

    def __init__(self):
        self.behaviors = []                     # a list of all the behavior objects used by the bbcon
        self.active_behaviors = []              # a list of all behaviors that are currently active.
        self.sensobs = []                       # a list of all sensory objects used by the bbcon
        self.motobs = []                        # a list of all motor objects used by the bbcon
        self.arbitrator = Arbitrator()               # the arbitrator object that will resolve actuator requests produced by the behaviors.

    # append a newly-created behavior onto the behaviors list.
    def add_behavior(self, behavior):

        if behavior not in self.behaviors:
            self.behaviors.append(behavior)

    # append a newly-created sensob onto the sensobs list.
    def add_sensor(self, sensor):
        if sensor not in self.sensobs:
            self.sensobs.append(sensor)

    # add an existing behavior onto the active-behaviors list.
    def activate_bahavior(self, behavior):
        if behavior in self.behaviors:
            self.active_behaviors.append(behavior)

    # remove an existing behavior from the active behaviors list.
    def deactive_behavior(self, behavior):
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    # Constitutes the core BBCON activity
    def run_one_timestep(self):

        # Updates behaviours which in return updates sensobs.
        for behaviour in self.active_behaviors():
            behaviour.update()

        motor_recommendations, flag = self.arbitrator.choose_action(self.active_behaviors)   # List of recoms, halt_request_flag.



