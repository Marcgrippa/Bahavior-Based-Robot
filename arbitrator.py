class Arbitrator():

    def __init__(self, bbcon):
        # Pointer to Bbcon-object
        bbcon_object = bbcon

    def choose_action(self, behaviors):

        temp_be = None
        temp_weight = -1

        #Choosing a "winning" behavior and returns that behavors motor recommendations and halt flag
        for behavior in behaviors:

            if behavior.weight > temp_weight:
                temp_weight = behavior.weight
                temp_be = behavior

        return temp_be.motor_recommendations, temp_be.halt_request



