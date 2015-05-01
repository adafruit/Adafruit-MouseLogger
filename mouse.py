#!/usr/bin/env python

import ConfigParser
import os
import os.path
import sqlite3
import time

import RPi.GPIO as GPIO
from Adafruit_IO import *

# Handle a simple configuration file:
config = ConfigParser.RawConfigParser()
config.read('mousetrap.cfg')
trap_pin = config.getint('sensors', 'trap_pin')
pir_pin = config.getint('sensors', 'pir_pin')

sqlite_log = False
if os.path.isfile('mice.db'):
    print "Logging to mice.db"
    sqlite_log = True
    sqlite_conn = sqlite3.connect('mice.db', isolation_level=None)

# If the config for IO is defined...
io_key = False
if config.has_option('io', 'key'):
    print "Logging to Adafruit IO"
    io_key = config.get('io', 'key')
    adafruit_io = Client(io_key)

def send_value(field, value):
    print(field, value)
    if io_key:
        adafruit_io.send(field, value)
    if sqlite_log:
        cursor = sqlite_conn.cursor()
        if field == "Mouse Problems":
            event_type = 1
        if field == "Trap Activity":
            event_type = 2
        cursor.execute(
            "INSERT INTO events (timestamp, value, event_type) VALUES (DATETIME(), ?, ?);",
            (value, event_type)
            )

GPIO.setmode(GPIO.BCM)

# Activate input:
GPIO.setup(pir_pin, GPIO.IN)

# Activate input with PullUp:
GPIO.setup(trap_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  

trap_activity = 0
previous_trap_state = GPIO.input(trap_pin)

motion_detected = False
motion_instances = []
recent_problem_count = 0

while True:
    previous_recent_problem_count = recent_problem_count

    motion_detected = False

    if GPIO.input(pir_pin):
       motion_detected = True

    if motion_detected:
        motion_instances.append(1)
    else:
        motion_instances.append(0)

    if len(motion_instances) > 6:
        motion_instances.pop(0)

    trap_state = GPIO.input(trap_pin)
    if trap_state != previous_trap_state:
        trap_activity += 1
        previous_trap_state = trap_state
        send_value('Trap Activity', trap_activity)

    recent_problem_count = sum(motion_instances)
    if previous_recent_problem_count != recent_problem_count:
        send_value('Mouse Problems', sum(motion_instances))

    time.sleep(6)
