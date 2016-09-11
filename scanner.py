import RPi.GPIO as GPIO

class Scanner():
    def __init__(self, board_pin):
        self.board_pin = board_pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(board_pin, GPIO.OUT)

    def move(self):
        GPIO.output(self.board_pin, 1)

    def stop(self):
        GPIO.output(self.board_pin, 0)