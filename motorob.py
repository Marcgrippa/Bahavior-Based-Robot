from motors import Motors

# Thomas er noob

class motob():

    def __init__(self):
        # A list of the motors whose settings will be determined by the motob(this class)
        self.motors = []
        # Most recent motor recommendation sent to the motob
        self.value = None
        # Objektet Motors
        self.motor = Motors()




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
        val = recommendation[0]
        dur = recommendation[1]

        if(val == 'S'):
            self.motor.stop()
        elif(val == 'F'):
            self.motor.set_value(1,1)
        elif(val == 'L'):
            pass
        elif(val == 'R'):
            pass
        elif(val == 'B'):
            self.motor.set_value(1,1)

        pass
