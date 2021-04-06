#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import sys

STEPS_FOR_REV = 512
REVS_FOR_OPEN = 4  # found out in experiment
STEPS_TO_OPEN_OR_CLOSE = REVS_FOR_OPEN * STEPS_FOR_REV
DELAY_BETWEEN_STEPS = 0.002 # seconds
DEFAULT_PERCENTAGE = 100
CCW = True
CW = False

try:
    arg_direction = CW if sys.argv[1] == 'close' else CCW
except IndexError:
    arg_direction = CCW

try:
    arg_percentage = int(sys.argv[2])
except IndexError:
    arg_percentage = DEFAULT_PERCENTAGE

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

PINS = [
    14,  # 1
    15,  # 2
    18,  # 4
    23,  # 8
]

def setup_pins():
    for p in (PINS):
        GPIO.setup(p, GPIO.OUT)

def off_all_pins():
    for p in (PINS):
        GPIO.output(p, GPIO.LOW)

def full_step(lst, sleep):
    for n, p in enumerate(lst):
        GPIO.output(lst[n-2], GPIO.LOW)
        GPIO.output(lst[n], GPIO.HIGH)
        time.sleep(sleep)

def calculate_steps(percentage = DEFAULT_PERCENTAGE, steps = STEPS_TO_OPEN_OR_CLOSE):
    if not percentage or percentage > DEFAULT_PERCENTAGE:
        percentage = DEFAULT_PERCENTAGE
    
    if percentage < 0:
        precentage = 0
    
    return round(percentage/DEFAULT_PERCENTAGE * steps)    

def run(sleep = DELAY_BETWEEN_STEPS, ccw = True, steps = STEPS_TO_OPEN_OR_CLOSE):
    print(sys.argv)
    lst = PINS if ccw else PINS[::-1]
    step = 0
    calculated_steps = calculate_steps(arg_percentage, steps)
    while step < calculated_steps:
        full_step(lst, sleep)
        step += 1

    off_all_pins()

setup_pins()

run(DELAY_BETWEEN_STEPS, arg_direction)

GPIO.cleanup()