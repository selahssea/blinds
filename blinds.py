#!/usr/bin/python3

import RPi.GPIO as GPIO
import time
import sys

try:
        arg_percentage = int(sys.argv[2])
except IndexError:
        arg_percentage = 100

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.OUT)  # 1
GPIO.setup(15, GPIO.OUT)  # 2
GPIO.setup(18, GPIO.OUT)  # 4
GPIO.setup(23, GPIO.OUT)

pins = [
    14,  # 1
    15,  # 2
    18,  # 4
    23,  # 8
]

all_steps = 2048

def off_all_pins():
    for p in (pins):
        GPIO.output(p, GPIO.LOW)

def full_step(lst, sleep):
    for n, p in enumerate(lst):
        GPIO.output(lst[n-2], GPIO.LOW)
        GPIO.output(lst[n], GPIO.HIGH)
        time.sleep(sleep)

def calculate_steps(percentage = 100, steps = all_steps):
    if not percentage or percentage > 100:
        percentage = 100
    
    if percentage < 0:
        precentage = 0
    
    return round(percentage/100 * steps)    

def run(sleep = 0.002, ccw = True, steps = all_steps):
    print(sys.argv)
    lst = pins if ccw else pins[::-1]
    step = 0
    calculated_steps = calculate_steps(arg_percentage, steps)
    while step < calculated_steps:
        full_step(lst, sleep)
        step += 1

    off_all_pins()

ccw = False if sys.argv[1] == 'close' else True

run(0.002, ccw)