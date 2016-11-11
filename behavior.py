from abc import abstractclassmethod
from sensob import *


class Behavior:

    def __init__(self, bbcon):

        self.bbcon = bbcon                                      # pointer to the controller that uses this behavior.
        self.sensobs = []                                       # a list of all sensobs that this behavior uses.
        self.motor_recommendations = ["none"]                   # a list of recommendations, one per motob, that this behavior provides to the arbitrator.
        self.active_flag = False                                # boolean variable indicating that the behavior is currently active or inactive.
        self.halt_request = False                               # behaviors can request the robot to completely halt activity (and thus end the run).
        self.priority = 0                                       # a static, pre-defined value indicating the importance of this behavior.
        self.match_degree = 0                                   # a real number in the range [0, 1] indicating the degree to which current conditions warrant the performance of this behavior.
        self.weight = self.match_degree * self.priority         # weight - the product of the priority and the match degree, which the arbitrator uses as the basis for selecting the winning behavior for a timestep.

    @abstractclassmethod
    def consider_deactivation(self):
        # whenever a behavior is active, it should test whether it should deactivate.
        return

    @abstractclassmethod
    def consider_activation(self):
        # whenever a behavior is inactive, it should test whether it should activate.
        return

    @abstractclassmethod
    def update(self):
        # Update the activity status
        # Call sense and act
        # Update the behavior’s weight
        return

    @abstractclassmethod
    def sense_and_act(self):
        return


# stops the robot if the ultrasonic sensor detects something closer than 10cm
class Obstruction(Behavior):

    # add sensob to behavior
    def __init__(self, bbcon):
        super(Obstruction,self).__init__(bbcon)
        self.u_sensob = UltrasonicSensob()
        self.sensobs.append(self.u_sensob)

    # activate behavior if obstruction is closer than 10cm
    def consider_activation(self):
        if self.u_sensob.get_value() < 10:
            self.bbcon.activate_bahavior(self)
            self.active_flag = True
            self.halt_request = True

    # deactive behavior if obstruction is further than 10cm
    def consider_deactivation(self):

        if self.u_sensob.get_value() > 10:
            self.bbcon.deactive_behavior(self)
            self.active_flag = False
            self.halt_request = False

    # update behavior
    def update(self):

        for sensor in self.sensobs:
            sensor.update()

        # if active, check if behavior should be deactivated
        if self.active_flag:
            self.consider_deactivation()

        # if deactivated, check if behavior should be activated
        elif not self.active_flag:
            self.consider_activation()

        # set weight = 0 if deactivated
        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["s"]
        self.priority = 1
        self.match_degree = 1

        
# simple class for driving forward
class DriveForward(Behavior):
    def __init__(self, bbcon):
        super(DriveForward, self).__init__(bbcon)
        self.active_flag = True

    def consider_activation(self):
        if self.active_flag:
            self.bbcon.activate_bahavior(self)

    def consider_deactivation(self):
        return

    def update(self):
        self.consider_activation()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["f"]
        self.priority = 0.5
        self.match_degree = 0.5


class FollowLine(Behavior):

    def __init__(self, bbcon):
        super(FollowLine, self).__init__(bbcon)
        self.r_sensob = ReflectanceSensob()
        self.sensobs.append(self.r_sensob)
        self.treshold = 0.5

    def consider_activation(self):

        for value in self.r_sensob.update():
            if value < 0.5:
                self.bbcon.activate_bahavior(self)
                self.active_flag = True
                return

        # deactivating
        self.weight = 0
        self.bbcon.deactive_behavior(self)
        self.active_flag = False

    def consider_deactivation(self):
        self.consider_activation()

    def update(self):

        self.consider_activation()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        self.r_sensob.update()

        if self.r_sensob.get_value()[0] < self.treshold and self.r_sensob.get_value()[5] < self.treshold:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.2

        elif self.r_sensob.get_value()[0] < self.treshold:
            self.motor_recommendations = ["l"]
            self.match_degree = 0.9

        elif self.r_sensob.get_value()[5] < self.treshold:
            self.motor_recommendations = ["r"]
            self.match_degree = 0.9

        else:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.5

        self.priority = 0.5


class TallObstructions(Behavior):

    def __init__(self, bbcon):
        super(TallObstructions, self).__init__(bbcon)
        self.l_IR_sensob = IRSensobLeft()
        self.r_IR_sensob = IRSensobRight()

        self.sensobs.append(self.l_IR_sensob)
        self.sensobs.append(self.r_IR_sensob)

    def consider_activation(self):

        if self.l_IR_sensob.get_value() or self.r_IR_sensob.get_value():
            self.bbcon.activate_bahavior(self)
            self.active_flag = True


    def consider_deactivation(self):

        if not self.l_IR_sensob.get_value() and self.r_IR_sensob.get_value():
            self.bbcon.deactive_behavior(self)
            self.active_flag = False
            self.weight = 0

    def update(self):

        if self.active_flag:
            self.consider_deactivation()

        else:
            self.consider_activation()

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        self.match_degree = 0.01
        self.l_IR_sensob.update()
        self.r_IR_sensob.update()

        if self.r_IR_sensob.get_value():
            self.motor_recommendations = ["l"]
            self.match_degree = 0.8

        elif self.l_IR_sensob.get_value():
            self.motor_recommendations = ["r"]
            self.match_degree = 0.8

        self.priority = 0.4

class ReversePhoto(Behavior):

    def __init__(self, bbcon):
        super(ReversePhoto, self).__init__(bbcon)
        self.c_sensob = CameraSensob()
        self.sensobs.append(self.c_sensob)
        self.getSensobs()

    def getSensobs(self):

        self.l_IR_sensob = None
        self.r_IR_sensob = None

        for sensob in self.sensobs:
            if sensob.isinstance(IRSensobLeft):
                self.l_IR_sensob = sensob

            if sensob.insert(IRSensobRight):
                self.r_IR_sensob = sensob

        if self.l_IR_sensob is None or self.r_IR_sensob is None:
            self.l_IR_sensob = IRSensobLeft()
            self.r_IR_sensob = IRSensobRight()
            self.sensobs.append(self.l_IR_sensob)
            self.sensobs.append(self.r_IR_sensob)

    def consider_activation(self):

        if self.l_IR_sensob and self.r_IR_sensob:
            self.bbcon.activate_bahavior(self)
            self.active_flag = True
            self.halt_request = True

    def consider_deactivation(self):

        if not self.l_IR_sensob or not self.r_IR_sensob:
            self.bbcon.deactive_behavior(self)
            self.active_flag = False
            self.halt_request = False
            self.weight = 0

    def update(self):

        if self.active_flag:
            self.consider_deactivation()
        else:
            self.consider_activation()

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        if self.l_IR_sensob and self.r_IR_sensob:
            self.motor_recommendations = ["b"]
            self.match_degree = 0.9
            self.c_sensob.update()

        self.priority = 0.5