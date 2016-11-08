from motorob import Motob


class Arbitrator():

    def choose_action(self, behaviors):

        temp_be = None
        temp_weight = -1

        # Choosing a "winning" behavior and returns that behavors motor recommendations and halt flag
        for behavior in behaviors:

            # if a behavior has a halt request -> abort and report back to Bbcon
            if behavior.halt_request:
                return behavior.motor_recommendations, behavior.halt_request

            # Choose a winning behavior
            elif behavior.weight > temp_weight:
                temp_weight = behavior.weight
                temp_be = behavior

        # Winning behaviors motor recommendations gets sendt back to Bbcon
        return temp_be.motor_recommendations, temp_be.halt_request
