from motors import Motors
#from sensob import CameraSensob


class Motob:
    """

    """
    def __init__(self):
        # Most recent motor recommendation sent to the motob
        self.values = []
        # Objektet Motors
        self.motor = Motors()
        self.speedDic = {100: 1,
                         75 : 0.75,
                         50 : 0.5,
                         25 : 0.25

        }




    def update(self, motor_recommandation):
        """
        receive a new motor recommendation, load it into the value slot, and operationalize it.
        :param motorvalue:
        :return: Nothing
        """
        self.values = motor_recommandation
        self.operationlize()

    def operationlize(self):
        """
        L - Left
        R - Right
        F - Forwards
        S - Stop
        B - Backwards
        The second vector elemnt is the degree og turning.
        Exp: rec
        :return:
        """

        for value in self.values:
            if value == "f":
                Motors().set_value([self.speedDic[100], self.speedDic[100]])
            elif value == "l":
                Motors().set_value([ -1 * self.speedDic[75], self.speedDic[75]], dur=self.turn_n_degrees(10))
            elif value == "r":
                Motors().set_value([self.speedDic[75], -1 * self.speedDic[75]], dur=self.turn_n_degrees(10) )
            elif value == "s":
                Motors().stop()

        # Kan legge til oppdatering av kamera hvis vi onsker det
        #    elif value == "p":
        #        CameraSensob().update()

    def turn_n_degrees(self, deg):
        """
        Takes in the desired turn degree and returns how long the motors have to turn at full speed.
        :param deg: Desired turn degree.
        :return: Time.
        """
        return 0.028*deg