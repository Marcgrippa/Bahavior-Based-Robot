from behavior import Behavior


class Arbitrator:
    """
    Bestemmer hvilken av behavior som vinner og får sin motor recommandation valgt

    """

    def choose_action(self, behaviors):
        winning_behavior = None
        max_weight = -1

        # Choosing a "winning" behavior and returns that behavors motor recommendations and halt flag
        for behavior in behaviors:

            # if a behavior has a halt request -> abort and report back to Bbcon
            if behavior.halt_request:
                print(behavior.name, "won!")
                return behavior.motor_recommendations

            # Choose a winning behavior
            elif behavior.weight > max_weight:
                max_weight = behavior.weight
                winning_behavior = behavior


        # Winning behaviors motor recommendations gets sent back to Bbcon

        if winning_behavior is None:
            print("Winning behavior is None. Driving forward!")
            return ["f"]
        print(winning_behavior.name, "won!")
        return winning_behavior.motor_recommendations
