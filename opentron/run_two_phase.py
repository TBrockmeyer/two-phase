from time import sleep

from driver import OpenTrons
from pipette import Pipette_P200
# from scanner import Scanner

# Settings
scanner_pin = 2
pipette_calibration = 0, 16, 19
serial_device = 'COM4'  # or /dev/ttysomething on linux
well_containing_two_phases = (375, 60)
top_phase_well = (200, 250)
test_plunger = False


# scanner = Scanner(scanner_pin)  # Arduino motor controller
# scanner.stop()

pipette = Pipette_P200()
pipette.calibrate(*pipette_calibration)

ot = OpenTrons(pipette)
with ot.connect(serial_device, baudrate=115200):
    sleep(5)  # Perhaps optional

    ot.home()  # init

    # ot.move(375, 300)

    ot.plunger_to_first_stop()
    ot.move(*well_containing_two_phases)

    if test_plunger:
        ot.release_plunger()
        ot.plunger_to_first_stop()

    interface_position = 87  # Complicated detection of interface from other script

    ot.move(z=interface_position)  # descend to interface
    ot.release_plunger()  # remove top phase
    ot.home('z')
    ot.move(*top_phase_well)
    ot.move(z=90)  # descend into well
    ot.blowout()  # dump top phase

    ot.home()
    ot.drop_tip()
    ot.home()
