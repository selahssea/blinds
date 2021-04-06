import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

pins = [
    14,  # 1
    15,  # 2
    18,  # 4
    23,  # 8
]

def setup_pins():
    for p in (pins):
        GPIO.setup(p, GPIO.OUT)
        print('Pin', p, ' enabled for OUT')

def off_all_pins():
    for p in (pins):
        GPIO.output(p, GPIO.LOW)
        print('Pin ', p, ' OFF')

setup_pins()

off_all_pins()

GPIO.cleanup()