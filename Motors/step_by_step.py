#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Notes: 64 slots with microstepping in increments of 8 is the best we can do here 52 cards plus 12 extra slots 
# for sets of 4 of a kind) this gives us 51 cards and a single joker to work with in the normal slots and 12 sets 
# of 4 of a kind for a 4 of a kind swap

import time
import board
import busio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

# Raspberry Pi Python 3 TM1637 quad 7-segment LED display driver examples
from time import sleep
import tm1637

CLK = 15
DIO = 14
DELAY = .3

tm = tm1637.TM1637(clk=CLK, dio=DIO)

# all segments on "88:88"
tm.write([127, 255, 127, 127])
#tm.write(bytearray([127, 255, 127, 127]))
#tm.write(b'\x7F\xFF\x7F\x7F')
#tm.show('8888', True)
#tm.numbers(88, 88, True)
sleep(DELAY)

# all segments off
tm.write([0, 0, 0, 0])
#tm.show('    ')
sleep(DELAY)

# Scroll trick name
tm.scroll('Select a card with the Great Billsoni') # 4 fps






#define MICROSTEP 16
kit = MotorKit(i2c=board.I2C())
#kit = MotorKit(i2c=busio.I2C( board.SCL, board.SDA, frequency=400_000)
#kit.stepper1.release()

# Scroll trick name
tm.scroll('Select a card with the Great Billsoni') # 4 fps

slot = 0
while slot < 54:
    count = 0
    while count < 25:
    '''
    print("Single coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.SINGLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.SINGLE)

    print("Double coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.DOUBLE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.DOUBLE)

    print("Interleaved coil steps")
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.INTERLEAVE)
    for i in range(100):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.INTERLEAVE)
    '''

    # self test loops
    #   print("Microsteps")
    #   for i in range(1600):
    #       kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
    #       time.sleep(.0001)
    #   for i in range(1600):
    #       kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
    #       time.sleep(.0001)
    #   count +=1
    #   print("Microsteps")

        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        time.sleep(.0001)
        count +=1
    slot +=1
    time.sleep(.3)
 


#origin = 0
#count = 0

kit.stepper1.release()
