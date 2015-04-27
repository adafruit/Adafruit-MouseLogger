#!/usr/bin/env python

import ConfigParser
import os
import time

import RPi.GPIO as io
from Adafruit_IO import *

config = ConfigParser.ConfigParser()
config.read('mousetrap.cfg')
io_key = config.get('io', 'key')

aio = Client(io_key)
def send_value(field, value):
    print(field, value)
    aio.send(field, value)

io.setmode(io.BCM)

pir_pin = 18
door_pin = 23

# Activate input:
io.setup(pir_pin, io.IN)

# Activate input with PullUp:
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  

trap_activity = 0
previous_door_state = io.input(door_pin)
motion_detected = False
motion_instances = []
recent_problem_count = 0

while True:
    previous_trap_value = trap_activity
    previous_recent_problem_count = recent_problem_count

    motion_detected = False

    if io.input(pir_pin):
       motion_detected = True

    if motion_detected:
        motion_instances.append(1)
    else:
        motion_instances.append(0)

    if len(motion_instances) > 6:
        motion_instances.pop(0)

    if io.input(door_pin) != previous_door_state:
        previous_door_state = io.input(door_pin)
        trap_activity += 1

    if (previous_trap_value != trap_activity):
        send_value('Trap Activity', trap_activity)

    recent_problem_count = sum(motion_instances)
    if previous_recent_problem_count != recent_problem_count:
        send_value('Mouse Problems', sum(motion_instances))

    time.sleep(6)
