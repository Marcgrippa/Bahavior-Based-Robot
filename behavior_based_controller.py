from behavior import Behavior
from sensob import *
from arbitrator import Arbitrator
from motob import Motob


class BehaviorBasedController:
    """
    BBCON (Behaviour-Based CONtroller); one instance per robot. Robot calls this class for the next move.
    """

    def __init__(self):
        self.__behaviors = []                   # List of all behaviors
        self.active_behaviors = []              # List of all _active_ behaviors
        self.__sensobs = []                     # List of all sensory objects
        self.motob = Motob()                    # List of all motor objects
        self.__arbitrator = Arbitrator(self)    # Arbitrator chooses the next behavior

        self.timesteps = 0
        self.notifications = []

    def should_continue_operating(self):
        return "q" not in self.notifications

    def add_behaviour(self, behavior: Behavior):
        """
        Adds a newly created behavior into the behaviors list.
        :param behavior: behavior to be added
        """
        if behavior not in self.__behaviors:
            self.__behaviors.append(behavior)
            # TODO: Refactor this because the method is doing more than it's name is implying.
            for sensob in behavior.sensobs:
                self.add_sensob(sensob)

    def remove_behaviour(self, behavior: Behavior):
        """
        Adds a newly created behavior into the behaviors list.
        :param behavior: behavior to be added
        """
        if behavior in self.__behaviors:
            self.__behaviors.remove(behavior)

    def add_sensob(self, sensob: Sensob):
        """
        Adds a newly created sensob into the sensobs list.
        :param sensob: sensob to be added
        """
        if sensob not in self.__sensobs:
            self.__sensobs.append(sensob)

    def remove_sensob(self, sensob: Sensob):
        """
        Removes a previously added sensob from the sensobs list.
        :param sensob: sensob to be removed
        """
        if sensob in self.__sensobs:
            self.__sensobs.remove(sensob)

    def activate_behavior(self, behavior: Behavior):
        """
        Activates a behavior by moving it to the active behaviors list.
        :param behavior: behavior to be activated
        """
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactivate_behavior(self, behavior: Behavior):
        """
        Deactivates a behavior by removing it from the active behaviors list.
        :param behavior: behavior to be deactivated
        """
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)

    def run_one_timestep(self):
        """
        The core BBCON activity; updates sensors and behaviors, invokes arbitrator, invokes sensors, waits, resets
            sensors..
        """

        # Update all sensors
        # TODO: Couldn't this actually be done in every behavior? behavior.reset_sensors()?
        for sensob in self.__sensobs:
            if isinstance(sensob, CameraSensob):
                if len(self.notifications) > 0 and self.notifications[0] == "p":
                    sensob.update()
                else:
                    continue
            else:
                sensob.update()

        # Update all behaviors
        for behavior in self.__behaviors:
            behavior.update()

        print("Active behaviors: {}".format(self.active_behaviors))

        if len(self.active_behaviors) > 0:
            # TODO: Change implementation to use halt request
            motor_recommendations, halt_request = self.__arbitrator.choose_action()
            print("Next recommendation: {}".format(motor_recommendations))

            # Update motobs based on motor recommendations
            self.motob.update(motor_recommendations)
        else:
            # Default behavior; this is just temporary.
            # TODO: Implement default behavior
            print("No active behaviors, will drive forward.")
            self.motob.update(["f"])

        # Reset sensobs
        for sensob in self.__sensobs:
            sensob.reset()

        self.timesteps += 1
