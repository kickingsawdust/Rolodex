#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Notes: 64 slots with microstepping in increments of 8 is the best we can do here 52 cards plus 12 extra slots 
# for sets of 4 of a kind) this gives us 51 cards and a single joker to work with in the normal slots and 12 sets 
# of 4 of a kind for a 4 of a kind swap

import time
import board
import RPi.GPIO as gpio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

# Raspberry Pi Python 3 TM1637 quad 7-segment LED display driver examples
from time import sleep
import tm1637

HALLPIN = 18
CLK = 15
DIO = 14
DELAY = .3

tm = tm1637.TM1637(clk=CLK, dio=DIO)

# all segments on "88:88"
tm.write([127, 255, 127, 127])
sleep(DELAY)

# all segments off
tm.write([0, 0, 0, 0])
sleep(DELAY)

# Scroll trick name
tm.scroll('Zeroing Carousel', 100) # 1 fps

gpio.setmode(gpio.BCM)
#gpio.setwarnings(False)
hallpin = 18

#define MICROSTEP 8
kit = MotorKit(i2c=board.I2C())

gpio.setup(HALLPIN, gpio.IN)
slot = 0
while slot < 64:
    count = 0
    while count < 25:
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        time.sleep(.001)
        count +=1
    if(gpio.input(hallpin) == False):
        tm.scroll('Carousel is at zero', 100) # 1 fps
        slot = 0
        break
    else:
        slot +=1
        time.sleep(.3)
  
#origin = 0
#count = 0

kit.stepper1.release()
