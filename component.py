import RPi.GPIO as GPIO
from enums import PowerState


class Component:
    def __init__(self, pin: int) -> None:
        self.pin = pin
        self.state = PowerState.OFF

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.OUT, initial=GPIO.LOW)

    def on(self) -> None:
        GPIO.output(self.pin, GPIO.HIGH)
        self.state = PowerState.ON

    def off(self) -> None:
        GPIO.output(self.pin, GPIO.LOW)
        self.state = PowerState.OFF
