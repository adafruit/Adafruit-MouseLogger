#!/usr/bin/env python

import time

import RPi.GPIO as io

def send_value(field, value):
    print(field, value)

io.setmode(io.BCM)

pir_pin = 18
door_pin = 23

# Activate input:
io.setup(pir_pin, io.IN)

# Activate input with PullUp:
io.setup(door_pin, io.IN, pull_up_down=io.PUD_UP)  

trap_closed = False
motion_detected = False
motion_instances = []
recent_problem_count = 0

while True:
    previous_trap_value = trap_closed
    previous_recent_problem_count = recent_problem_count

    motion_detected = False
    trap_closed = False

    if io.input(pir_pin):
       motion_detected = True
       print "MOTION DETECTED!"

    if motion_detected:
        motion_instances.append(1)
    else:
        motion_instances.append(0)

    if len(motion_instances) > 6:
        motion_instances.pop(0)

    if io.input(door_pin):
       trap_closed = False
    else:
       trap_closed = True

    if (previous_trap_value != trap_closed):
        if trap_closed:
            send_value('Trap State', 'Trap Closed')
        else:
            send_value('Trap State', 'Trap Open')

    recent_problem_count = sum(motion_instances)
    if previous_recent_problem_count != recent_problem_count:
        send_value('Mouse Problems', sum(motion_instances))

    time.sleep(0.5)
