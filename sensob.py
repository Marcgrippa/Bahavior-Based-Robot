from abc import abstractmethod

from reflectance_sensors import *
from ultrasonic import *

class Sensob:
    """
    Sensob serves as an interface between one or more sensors and the BBCON's behaviours.
    """

    def __init__(self):
        self.sensors = []
        self.value = None

    def get_value(self):
        return self.value

    @abstractmethod
    def update(self):
        """
        Main updater. Forces sensors to get values once per timestep.
        """
        return

    def reset(self):
        """
        Resets sensors.
        """
        for sensor in self.sensors:
            sensor.reset()


class ReflectanceSensob(Sensob):
    """
    Left reflectance sensor.
    """

    def __init__(self):
        super(ReflectanceSensob, self).__init__()
        self.sensor = ReflectanceSensors()
        self.sensors.append(self.sensor)

    def update(self):
        """
        Updates values.
        :return: Sensors value.
        """
        self.sensor.update()
        self.value = self.sensor.get_value()

    def get_value(self):
        """
        Getter for value.
        :return: Value
        """
        return self.value


class UltrasonicSensob(Sensob):
    """
    Ultrasonic sensob
    """

    def __init__(self):
        super(UltrasonicSensob, self).__init__()
        self.sensor = Ultrasonic()
        self.sensors.append(self.sensor)

    def update(self):
        """
        Updates ultrasonic values
        """
        print('Updating ultrasonic sensor...')
        self.sensor.update()
        self.value = self.sensor.get_value()
        return self.value

    def get_value(self):
        """
        Getter for value.
        :return: Value
        """
        return self.value

