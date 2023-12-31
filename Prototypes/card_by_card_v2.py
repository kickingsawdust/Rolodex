#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Notes: 64 slots with microstepping in increments of 8 is the best we can do here 52 cards plus 12 extra slots 
# for sets of 4 of a kind) this gives us 51 cards and a single joker to work with in the normal slots and 12 sets 
# of 4 of a kind for a 4 of a kind swap

import time
import board
import busio
import sqlite3
import subprocess
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

retcode = subprocess.call(["/usr/bin/python", "zero_carousel.py"])
if retcode != 0:
    print("Carousel did not zero properly, exiting")

# Raspberry Pi Python 3 TM1637 quad 7-segment LED display driver examples
from time import sleep
import tm1637

con = sqlite3.connect("cards.db")
cur = con.cursor()
CLK = 15
DIO = 14
DELAY = .2

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
tm.scroll('Select a card with the Great Billsoni', 100) # 1 fps

#define MICROSTEP 8
kit = MotorKit(i2c=board.I2C())
#kit = MotorKit(i2c=busio.I2C( board.SCL, board.SDA, frequency=400_000)
#kit.stepper1.release()

slot = 0
while slot < 64:
    #tm.show('AS')
    res = cur.execute("SELECT cardVal FROM card2slot WHERE slotVal = ?", (slot,))       
    card = res.fetchone()[0]
    print("%s" % card)
    tm.show(card)
    sleep(DELAY)
    tm.write([0,0,0,0])
    #print("%s" % (card,))
    count = 0
    while count < 50:
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        time.sleep(.001)
        count +=1
    slot +=1
    time.sleep(.1)

#origin = 0
#count = 0

kit.stepper1.release()
