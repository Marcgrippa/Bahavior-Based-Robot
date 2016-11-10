from bbcon import Bbcon
from behavior import *
from zumo_button import ZumoButton


def main():
    """
    Runs the program
    """

    bbcon = Bbcon()
    #drive_forward = DriveForward(bbcon)
    follow_line = FollowLine(bbcon)
    obstruction = Obstruction(bbcon)
    fuck_offers = TallObstructions(bbcon)

    # Legger til behavior
    #bbcon.add_behavior(drive_forward)
    bbcon.add_behavior(follow_line)
    bbcon.add_behavior(obstruction)
    bbcon.add_behavior(fuck_offers)

    ZumoButton().wait_for_press()

    while True:
        bbcon.run_one_timestep()


if __name__ == "__main__":
    main()


