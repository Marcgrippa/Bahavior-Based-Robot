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
        print(self.values)
        for value in self.values:
            if value == "f":
                Motors().set_value([1,1])
            elif value == "l":
                Motors().set_value([-1,1], dur=self.turn_n_degrees(90) )
            elif value == "r":
                Motors().set_value([1, -1], dur=self.turn_n_degrees(90))
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