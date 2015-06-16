#!/usr/bin/env python

import ConfigParser
import os
import os.path
import sys

from Adafruit_IO import *

# Handle a simple configuration file:
config = ConfigParser.RawConfigParser()
config.read('mousetrap.cfg')

print("Adafruit MouseLogger Feed Test")
print("Logging test values to Adafruit IO")
print("<:3)~~~")

# If the config for IO is defined...
io_key = False
if config.has_option('io', 'key'):
    io_key = config.get('io', 'key')
    adafruit_io = Client(io_key)
else:
    print("Please set an AIO key in mousetrap.cfg")
    sys.exit()

def send_value(field, value):
    print(field, value)
    if io_key:
        adafruit_io.send(field, value)

send_value('Trap Activity', 1)
send_value('Trap Activity', 2)
send_value('Trap Activity', 3)
send_value('Mouse Problems', 1)
send_value('Mouse Problems', 2)
send_value('Mouse Problems', 3)

print("Check your AIO feeds for recent updates to Trap Activity and Mouse Problems feeds:")
print("https://io.adafruit.com/feeds/")
