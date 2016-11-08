from behavior_based_controller import BehaviorBasedController
from behavior import *
from motors import Motors
from zumo_button import ZumoButton


def main():
    """
    Runs the program
    """
    bbcon = BehaviorBasedController()
    follow_line = FollowLine(bbcon)
    navigate_tall = NavigateTallObjects(bbcon)
    take_picture = TakePicture(bbcon)
    stop_obstruction = StopObstruction(bbcon)

    # Add behaviors and sensors
    bbcon.add_behaviour(follow_line)
    bbcon.add_behaviour(navigate_tall)
    bbcon.add_behaviour(take_picture)
    bbcon.add_behaviour(stop_obstruction)

    ZumoButton().wait_for_press()

    while bbcon.should_continue_operating():
        bbcon.run_one_timestep()

    Motors().stop()

if __name__ == "__main__":
    main()
