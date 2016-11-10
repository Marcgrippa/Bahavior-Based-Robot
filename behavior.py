from abc import abstractclassmethod
from sensob import *


class Behavior:

    def __init__(self, bbcon):

        self.bbcon = bbcon                                      # pointer to the controller that uses this behavior.
        self.sensobs = []                                       # a list of all sensobs that this behavior uses.
        self.motor_recommendations = []                         # a list of recommendations, one per motob, that this behavior provides to the arbitrator.
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
        print("Object Obstr created")
        self.u_sensob = UltrasonicSensob()
        self.sensobs.append(self.u_sensob)

    # activate behavior if obstruction is closer than 10cm
    def consider_activation(self):
        print("UltraSensob: ", self.u_sensob.get_value())
        if self.u_sensob.get_value() < 10:
            print("UltraSensob activated")
            self.bbcon.activate_bahavior(self)
            self.active_flag = True
            self.halt_request = True

    # deactive behavior if obstruction is further than 10cm
    def consider_deactivation(self):

        if self.u_sensob.get_value() > 10:
            print("UltraSensob deactivated")
            self.bbcon.deactive_behavior(self)
            self.active_flag = False
            self.halt_request = False

    # update behavior
    def update(self):
        print("Obstr-update")

        for sensor in self.sensobs:
            sensor.update()

        # if active, check if behavior should be deactivated
        if self.active_flag:
            print("Deactivating Obstr")
            self.consider_deactivation()

        # if deactivated, check if behavior should be activated
        elif not self.active_flag:
            print("Activate Obstr")
            self.consider_activation()

        # set weight = 0 if deactivated
        if not self.active_flag:
            print("Setting value to 0 - Obstr")
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
        print("DriveForward object crated")
        self.active_flag = True

    def consider_activation(self):
        if self.active_flag:
            print("Activated DriveForward")
            self.bbcon.activate_bahavior(self)

    def consider_deactivation(self):
        return

    def update(self):
        print("Updating DriveForward")
        self.consider_activation()
        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        self.motor_recommendations = ["f"]
        self.priority = 0.5
        self.match_degree = 0.5


class Camera(Behavior):
    """
    Behavior for kameraet. Skal kunne oppdatere kamera, ta bilde etc
    """

    def __init__(self, bbcon):
        """
        Legger til Kamera sensob i listen over alle sensorene
        """
        super(Camera, self).__init__(bbcon)
        self.sensobs.append(CameraSensob())

    def consider_activation(self) -> bool:
        """
        Bestemmer når kamera skal bli aktivtert
        """
        pass

    def consider_deactivation(self) -> bool:
        """
        Bestemmer når kamera ikke skal være aktivert
        """
        return not self.consider_activation()

    def update(self):
        """
        Oppdaterer kameraet
        """

        # Oppdaterer "active_flag" i henhold til de parameterene som er satt i consider_activation
        self.active_flag = self.consider_activation()

        # Tester om kamerat er aktiv, hvis ikke vil den sette weight til 0
        if not self.active_flag:
            self.weight = 0
            return

    def sense_and_act(self):
        """

        :return:
        """










































