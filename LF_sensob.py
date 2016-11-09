from abc import abstractmethod

from camera import *
from irproximity_sensor import *
from reflectance_sensors import *
from ultrasonic_sensor import *


class Sensob:
    """
    Sensob serves as the interface between one or more sensors and the BBCON's behaviors.
    """

    def __init__(self):
        # TODO: Should make these two instance variables open to subclasses.
        self.sensors = []  # List of sensors
        self.value = None  # Value

    def get_value(self):
        """
        Gets the vale of the sensob.
        :return: value of sensob.
        """
        return self.value

    @abstractmethod
    def update(self):
        """
        Main method for the sensob object. Force sensors to fetch relevant sensor values and convert them to
            pre-processed sensob values. Should only be done once per timestep.
        """
        return

    def reset(self):
        """
        Resets the sensors.
        """
        for sensor in self.sensors:
            sensor.reset()
        pass


class ReflectanceSensob(Sensob):
    """
    Leftmost reflectance sensor.
    """

    def __init__(self):
        super(ReflectanceSensob, self).__init__()
        self.sensors.append(ReflectanceSensors())
        self.value = False

    def update(self):
        """
        Updates values
        """
        self.value = self.sensors[0].update()
        return self.value

    def get_value(self):

        """
        :return: verdien til value
        """
        return self.value


class IRSensob(Sensob):
    """
    Super class for IRSensobLeft and IRSensobRight.
    """

    def update(self):
        """
        IRSensob is a superclass for IRSensobLeft and IRSensobRight, so we just return.
        :return:
        """
        return

    def __init__(self):
        super(IRSensob, self).__init__()
        self.sensors.append(IRProximitySensor())


class IRSensobLeft(IRSensob):
    """
    Leftmost ir sensor
    """

    def __init__(self):
        super(IRSensobLeft, self).__init__()
        self.value = False

    def update(self):
        """
        Updates values.
        """
        self.value = self.sensors[0].update()[1]  # self.__sensor.update() gir en liste [bool, bool]
        return self.value

    def get_value(self):
        """
        :return: verdien til value
        """
        return self.value


class IRSensobRight(IRSensob):
    """
    Leftmost ir sensor
    """

    def __init__(self):
        super(IRSensobRight, self).__init__()
        self.value = False

    def update(self):
        """
        Updates values.
        """
        self.value = self.sensors[0].update()[0]  # self.__sensor.update() gir en liste [bool, bool]
        return self.value

    def get_value(self):
        """
        :return: verdien til value
        """
        return self.value


class UltrasonicSensob(Sensob):
    """
    UltrasonicSensob
    """

    def __init__(self):
        super(UltrasonicSensob, self).__init__()
        self.sensors.append(UltrasonicSensor())

    def update(self):
        """
        updates values
        """

        print("Updating ultrasonic sensor ...")
        self.sensors[0].update()
        self.value = self.sensors[0].get_value()
        return self.value

    def get_value(self):
        """
        :return: verdien til value
        """
        return self.value


class CameraSensob(Sensob):
    """
    Kamera
    """

    def __init__(self):
        super(CameraSensob, self).__init__()
        self.sensors.append(Camera())
        self.value = None

    def update(self):
        """
        updates values
        """
        print("Updating camera sensor ...")
        self.sensors[0].update()
        self.value = self.sensors[0].get_value()
        return self.value

    def get_value(self):
        """
        :return: verdien til value
        """
        return self.value
