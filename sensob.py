from abc import abstractmethod

from reflectance_sensors import *
from ultrasonic import *
from irproximity_sensor import *
from camera import *


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


class IRSensob(Sensob):
    """
    Superclass for left and right IRSenobs
    """

    def __init__(self):
        super(IRSensob, self).__init__()
        self.sensors.append(IRProximitySensor())

    def update(self):
        return


class IRSensobLeft(IRSensob):
    """
    IR-sensor left.
    """

    def __init__(self):
        super(IRSensobLeft, self).__init__()
        self.value = False

    def update(self):
        """
        Updates values
        """
        self.value = self.sensors[0].update()[0]
        return self.value

    def get_value(self):
        """
        Getter for value.
        :return: Value
        """
        return self.value


class IRSensobRight(IRSensob):

    def __init__(self):
        super(IRSensobRight, self).__init__()
        self.value = False

    def update(self):
        """
        Updates values
        """
        self.value = self.sensors[0].update()[1]
        return self.value

    def get_value(self):
        """
        Getter for value.
        :return: Value
        """
        return self.value


class CameraSensob(Sensob):
    """
    Camera sensob
    """

    def __init__(self):
        super(CameraSensob, self).__init__()
        self.sensor = Camera()
        self.sensors.append(self.sensor)
        self.value = None

    def update(self):
        """
        Updates values
        """
        print('Updating camera sensor...')
        self.sensor.update()
        self.value = self.sensor.get_value()
        return self.value

    def get_value(self):
        """
        Getter for value
        :return: Value
        """
        return self.value
