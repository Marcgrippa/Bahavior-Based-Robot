from bbcon import Bbcon


class Behavior():

    def __init__(self, bbcon):

        self.bbcon = bbcon                                      # pointer to the controller that uses this behavior.
        self.sensobs = []                                       # a list of all sensobs that this behavior uses.
        self.motor_recommendations = []                         # a list of recommendations, one per motob, that this behavior provides to the arbitrator.
        self.active_flag = False                                # boolean variable indicating that the behavior is currently active or inactive.
        self.halt_request = False                               # behaviors can request the robot to completely halt activity (and thus end the run).
        self.priority = 0                                       # a static, pre-defined value indicating the importance of this behavior.
        self.match_degree = 0                                   # a real number in the range [0, 1] indicating the degree to which current conditions warrant the performance of this behavior.
        self.weight = self.match_degree * self.priority         # weight - the product of the priority and the match degree, which the arbitrator uses as the basis for selecting the winning behavior for a timestep.

    # whenever a behavior is active, it should test whether it should deactivate.
    def consider_deactivation(self):
        if self not in self.bbcon.active_behaviors and self.active_flag is True:
            self.active_flag = False
            self.bbcon.deactive_behavior(self)

    # whenever a behavior is inactive, it should test whether it should activate.
    def consider_activation(self):
        if self in self.bbcon.active_behaviors and self.active_flag is False:
            self.active_flag = True
            self.bbcon.activate_bahavior(self)

    def update(self):
        #todo: Skriv ferdig
        pass

    def sense_and_act(self):
