from motors import Motors

class motob():

    def __init__(self):
        # A list of the motors whose settings will be determined by the motob(this class)
        self.motors = []
        # Most recent motor recommendation sent to the motob
        self.value = None




    def update(self, motorvalue):
        """
        receive a new motor recommendation, load it into the value slot, and operationalize it.
        :param motorvalue:
        :return: Nothing
        """
        self.value = motorvalue

    def operationlize(self, recommendation):
        """

        :param recommendation: Vector with to parameters, the first
        is one of the following
        L - Left
        R - Right
        F - Forwards
        S - Stop
        B - Backwards
        The second vector elemnt is the degree og turning.
        Exp: rec
        :return:
        """
        pass
