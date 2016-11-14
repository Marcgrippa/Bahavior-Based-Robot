from sensob import *
import abc
from image_manager import ImageManager
from sensors .motors import Motors


class Behavior:
    """
    A fundamental behavior for the robot. MUST NOT COMMUNICATE WITH OTHER BEHAVIORS.
    """

    def __init__(self, bbcon):
        self.bbcon = bbcon                  # Associated behavior-based controller
        self.sensobs = []                   # List of sensor objects
        self.motor_recommendations = []     # List of motor recommendations
        self.active_flag = None             # Whether or not this behavior is active
        self.halt_request = None            # Whether or not it should be halted
        self.priority = 0                # What kind of priority it has
        self.match_degree = 0            # Urgency and appropriatness of performing this behavior right now
        self.weight = 0                  # weight = priority * match_degree

    @abc.abstractmethod
    def consider_deactivation(self) -> bool:
        """
        If it is active, it should test if it should be deactivated.
        """
        return

    @abc.abstractmethod
    def consider_activation(self) -> bool:
        """
        If it is inactive, it should test if it should be activated.
        """
        return

    @abc.abstractmethod
    def update(self):
        """
        Main interface between the bbcon and the behavior.
            - Update the activity status
            - Call sense_and_act
            - Update behavior's weight: Use the match degree (calculated by sense and act) multiplied by the behavior’s
                user-defined priority.
        """
        return

    @abc.abstractmethod
    def sense_and_act(self):
        """
        The core computations performed by the behavior that use sensob readings to produce motor
            recommendations (and halt requests).
        """
        return

    def find_sensob(self, sensor_type):
        """
        Finds the sensob in the list of sensobs
        :param sensor_type: type of sensor we're looking for
        :return: the sensor we're looking for
        """
        for sensob in self.sensobs:
            if isinstance(sensob, sensor_type):
                return sensob


class TakePicture(Behavior):
    """
	Behavior that takes a picture if an object is close enough.
	"""
    # TODO: Refactor this so that is only takes a picture when the motor has stopped because of obstruction.

    def __init__(self, bbcon):
        super(TakePicture, self).__init__(bbcon)
        self.sensobs.append(CameraSensob())

    def consider_activation(self) -> bool:
        """
		If a behavior is requesting that a picture should be taken, do it.
		:return: bool indicating the presence of a request for a picture to be taken.
		"""
        if len(self.bbcon.notifications) > 0 and self.bbcon.notifications[0] == "p":
            self.bbcon.activate_behavior(self)
            self.match_degree = 1
            self.priority = 1
            return True
        else:
            self.bbcon.deactivate_behavior(self)
            self.match_degree = 0
            self.priority = 0
            return False

    def consider_deactivation(self) -> bool:
        """
		If object is further away than 10 cm, don't take picture.
		:return: bool if object is further away than 10 cm
		"""
        return not self.consider_activation()

    def update(self):
        """
        Updates the camera sensor;
        """
        # Update the activity tracker
        self.active_flag = self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()

        # Update behaviors weight
        self.weight = self.match_degree * self.priority

    def sense_and_act(self):
        """
        Shouldn't actually affect the motors, but should request that a picture should be taken.
        :return: a 
        """
        Motors().stop()

        image = self.find_sensob(CameraSensob).update()
        im = ImageManager(image=image)
        im.dump_image('/')

        triple2 = [0] * 3
        for x in range(im.xmax):
            for y in range(im.ymax):
                t = im.get_pixel(x, y)
                for i in range(len(triple2)):
                    triple2[i] += t[i]
        t3 = []
        for i in triple2:
            t3.append(i / (im.xmax * im.ymax))

        over_50 = False
        for i in t3:
            if i > 50:
                over_50 = True

        if over_50:
            self.priority = 1
            self.match_degree = 1
            self.motor_recommendations = ["r"]
        else:
            self.priority = 1
            self.match_degree = 1
            self.bbcon.notifications.append("q")
            print("We found our item!")

        # self.find_sensob(UltrasonicSensob).value = 11.0
        self.bbcon.notifications.remove("p")


class FollowLine(Behavior):
    """
    Behavior that follow a black line with the sensors under the robot
    """

    def __init__(self, bbcon):
        super(FollowLine, self).__init__(bbcon)
        self.threshold = 0.5  # If the sensor is under this value it will return true when considering activation
        self.sensobs.append(ReflectanceSensob())

    def consider_deactivation(self) -> bool:
        """
        :return: bool true if there is not a black line under the robot
        """
        return not self.consider_activation()

    def consider_activation(self) -> bool:
        """
        Should be activated when there is a black line underneath the robot.
        If one of the sensors has a value above some set value, consider activation
        :return: bool if one of the sensors have a value above some set value
        """

        reflectance_sensor = self.find_sensob(ReflectanceSensob)

        for sensor_value in reflectance_sensor.update():
            if sensor_value < self.threshold:

                self.bbcon.activate_behavior(self)
                return True

        self.weight = 0
        self.bbcon.deactivate_behavior(self)
        return False

    def update(self):
        """
        Updates the behavior
        """
        self.active_flag = self.consider_activation()

        self.sense_and_act()

        self.weight = self.priority * self.match_degree

    def sense_and_act(self):

        """
        If the leftmost sensor is activated turn left
        If the rightmost sensor is activated turn right
        Else continue forward
        """

        reflectance_sensor = self.find_sensob(ReflectanceSensob)

        # If the leftmost sensor is activated
        if reflectance_sensor.get_value()[0] < self.threshold and reflectance_sensor.get_value()[5] < self.threshold:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.2
        elif reflectance_sensor.get_value()[0] < self.threshold:
            self.motor_recommendations = ["l"]
            self.match_degree = 0.9
        elif reflectance_sensor.get_value()[5] < self.threshold:
            self.motor_recommendations = ["r"]
            self.match_degree = 0.9
        else:
            self.motor_recommendations = ["f"]
            self.match_degree = 0.5

        self.priority = 0.5


class NavigateTallObjects(Behavior):
    """
    Behavior for navigating between tall objects.
    IR Sensors can originally see 5cm, but 2cm are cut off because of the wheels of the robot. Threshold at 3cm.
    """

    def __init__(self, bbcon):
        super(NavigateTallObjects, self).__init__(bbcon)
        self.sensobs.append(IRSensobLeft())
        self.sensobs.append(IRSensobRight())

    def consider_activation(self) -> bool:
        """
        Should consider activation when the IR sensors senses tall objects. What about ultrasonic sensor?
        :return: returns a bool if the sensors "see" anything, which means objects are closer than 5cm (actually 3cm).
        """

        should_activate = self.sensobs[0].get_value() or self.sensobs[1].get_value()

        if should_activate:
            self.bbcon.activate_behavior(self)
        else:
            self.bbcon.deactivate_behavior(self)

        return should_activate

    def consider_deactivation(self):
        """
        When no walls are near, deactivate this.
        """
        return not self.consider_activation()

    def update(self):
        """
        Updates the behavior.
        """
        self.active_flag = self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        """
        If left sensor is true, move right. If right sensor is true, move left.
        :return:
        """

        self.match_degree = 0.01

        if self.sensobs[0].update() and self.sensobs[1].update():
            self.motor_recommendations = ["f"]
            self.match_degree = 0.2

        elif self.sensobs[0].update():
            self.motor_recommendations = ["l"]
            self.match_degree = 0.9

        elif self.sensobs[1].update():
            self.motor_recommendations = ["r"]
            self.match_degree = 0.9

        self.priority = 0.4


class StopObstruction(Behavior):
    """
    Behavior for stopping when in front of an obstruction.
    """

    def __init__(self, bbcon):
        super(StopObstruction, self).__init__(bbcon)
        self.sensobs.append(UltrasonicSensob())

    def consider_activation(self) -> bool:
        """
        Should consider stopping if there is something closer than 10cm to the robot.
        :return: true if obstruction is less than 10cm in front of robot
        """
        b = self.find_sensob(UltrasonicSensob).get_value() < 10.0
        print(self.find_sensob(UltrasonicSensob).get_value())

        if b:
            self.bbcon.activate_behavior(self)
        else:
            self.bbcon.deactivate_behavior(self)

        return b

    def consider_deactivation(self) -> bool:
        """
        If no objects are closer than 10cm, deactivate.
        :return:
        """
        return not self.consider_activation()

    def update(self):
        """
        Updates the behavior.
        """
        self.active_flag = self.consider_activation()

        if not self.active_flag:
            self.weight = 0
            return

        self.sense_and_act()
        self.weight = self.priority * self.match_degree

    def sense_and_act(self):
        """
        If ultrasonic sensor sees something less than 10cm, tell motors to stop and take a picture.
        """
        self.motor_recommendations = ["s"]
        self.bbcon.notifications.append("p")
        self.priority = 0.9
        self.match_degree = 0.9
