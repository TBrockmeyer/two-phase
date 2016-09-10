from time import sleep

from driver import OpenTrons
from pipette import Pipette_P200
from scanner import Scanner

# Settings
scanner_pin = 2
pipette_calibration = 0, 10, 20
serial_device = 'COM4'  # or /dev/ttysomething
well_containing_two_phases = (100, 50)
top_phase_well = (200, 250)


scanner = Scanner(scanner_pin)  # Arduino motor controller
scanner.stop()

pipette = Pipette_P200()
pipette.calibrate(*pipette_calibration)

ot = OpenTrons(pipette)
ot.connect(serial_device, baudrate=115200)
sleep(5)

ot.home()  # init

ot.move(*well_containing_two_phases)
ot.plunger_to_first_stop()

interface_position = 20  # Complicated detection of interface

ot.move(z=interface_position)  # descend to interface
ot.release_plunger()  # remove top phase
ot.raise_pipette()
ot.move(*top_phase_well)
ot.move(z=30) # descend into well
ot.blowout()  # dump top phase
