import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PINS = [
    14,  # 1
    15,  # 2
    18,  # 4
    23,  # 8
]

def setup_and_off_pins():
    for p in (PINS):
        GPIO.setup(p, GPIO.OUT)
        print('Pin', p, ' enabled for OUT')
        GPIO.output(p, GPIO.LOW)
        print('Pin ', p, ' OFF')

setup_and_off_pins()

GPIO.cleanup()