from behavior import Behavior
from random import *


class arbOb:
    """
    Decides which behavior wins and thus gets its motor recommendations transferred to the agent’s motobs,
        which will then determine the overt action(s) of the agent.
    """

    def __init__(self, bbcon, stochastic_mode=False):
        self.__stochastic_mode = stochastic_mode
        self.__bbcon = bbcon

    def choose_action(self) -> tuple:
        """
        Chooses which action to take depending on the mode the arbOb is set to.
        This mode is configured in the init.
        :return: tuple: (motor recommendation, boolean indiciating if it should be halted or not)
        """

        if self.__stochastic_mode:
            behavior = self.__choose_stochastic_action__()
        else:
            behavior = self.__choose_deterministic_action__()

        return behavior.motor_recommendations, behavior.halt_request

    def __choose_deterministic_action__(self) -> Behavior:
        """
        Picks the behavior with the heighest weight.
        :return: Returns the behavior with the highest weight
        """
        max_behavior_weight = -1
        max_behavior = None

        for behavior in self.__bbcon.active_behaviors:
            if behavior.weight > max_behavior_weight:
                max_behavior_weight = behavior.weight
                max_behavior = behavior

        return max_behavior

    def __choose_stochastic_action__(self) -> Behavior:
        """
        To get a weighted random choice:
            - For each behavior: add weight times ten to list of behaviors
            - Use random.choice() to get an element from the list.
            - Behavior with heighest weight is more likely to be chosen.
        :return: Returns a weigted random behavior
        """

        list_of_behaviors = []
        for behavior in self.__bbcon.get_active_behaviors():
            list_of_behaviors.append(behavior * (behavior.weight * 10))

        return choice(list_of_behaviors)
