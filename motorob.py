from motors import Motors
from sensob import CameraSensob


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

        for value in self.values:
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
