from sensors.motors import Motors
from sensob import CameraSensob


class Motob:
    """
    Interface between a behavior and one or more motors.
    """

    def __init__(self):
        self.__motor = Motors()  # List of motors whose settings will be determined by the motob
        self.__values = []  # The most recent recommendation sent to the motob

    def update(self, motor_recommendation):
        """
        Receives a new motor recommendation, loads it into the value slot and operationalizes it.
        """
        self.__values = motor_recommendation
        self.operationalize()

    def operationalize(self):
        """
        Convert motor recommendation into one or more settings, which are sent to the corresponding motor(s).
        """
        for value in self.__values:
            if value == "f":
                Motors().forward()
            elif value == "l":
                Motors().left(dur=0.3)
            elif value == "r":
                Motors().right(dur=0.3)
            elif value == "s":
                Motors().stop()
            elif value == "p":
                CameraSensob().update()

