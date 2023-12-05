#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Notes: 64 slots with microstepping in increments of 8 is the best we can do here 52 cards plus 12 extra slots 
# for sets of 4 of a kind) this gives us 51 cards and a single joker to work with in the normal slots and 12 sets 
# of 4 of a kind for a 4 of a kind swap
#NOTE CURRENTLY RUNNING WITH STEP OF 16 I'm not sure if this is any smoother but something I'm playing with, slots are now 50 microsteps appart vs 25 at MS8

import time
import board
import busio
import sqlite3
import subprocess
import tm1637 #7 segment display
#import RPi.GPIO as GPIO
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from gpiozero import LED, Button
from time import sleep
from signal import pause

#Zero Code (remember we need to get a non-locking hall sensor :( )

retcode = subprocess.call(["/usr/bin/python", "zero_carousel_smooth.py"])
if retcode != 0:
    print("Carousel did not zero properly, exiting")
slot=0

# Set some variables we'll be needing
#GPIO.setmode(GPIO.BCM)
con = sqlite3.connect("cards.db", check_same_thread=False)
cur = con.cursor()
CLK = 15
DIO = 14
DELAY = .2
tm = tm1637.TM1637(clk=CLK, dio=DIO)
travel = 0
tm.scroll('Select a card with the Great Billsoni', 100) # 1 fps

#Button variables (what more variables?)

suit_button = Button(4)
suit_button_count = 0 #unset 1=S, 2=H, 3=C, 4=D 5=unset if suit_button_count > 4: suit_button_count = 0
suitMap = {0:'',1:'S',2:'H',3:'C',4:'D',5:' unset'}
suit = "unset"
card_value_button = Button(26)
card_value_button_count = 0
card_valueMap = {0:'',1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K',14:'unset '}
card_value = "unset"
#actuator_button = Button(4)
actuator_button_state = 0 # this might need to be actuator_button_time stored in seconds?
selected_card = suit + card_value

#tm.scroll('more crap here', 100) # 1 fps


# Button Code

def change_suit():
    global suit_button_count
    global selected_card
    if suit_button_count > 4:
        suit_button_count = 0
        #print("The suit has been unset")
    else:
        suit_button_count += 1
        global suit
        global tm
        suit = suitMap[suit_button_count]
        selected_card = card_value + suit
        print("The suit is set to: %s" % suit)
        print("The selected card is %s" % selected_card)
        if "unset" not in selected_card:
            res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
            slot = res.fetchone()[0]
            print("current slot %s" % slot)
            tm.write([0,0,0,0])
            tm.show(selected_card)
            sleep(DELAY)

def change_value():
    global card_value_button_count
    global selected_card
    if card_value_button_count > 13:
        card_value_button_count = 0
    else:
        global card_value
        card_value_button_count += 1
        card_value = card_valueMap[card_value_button_count]
        selected_card = card_value + suit
        print("The card value is set to: %s" % card_value)
        print("The selected card is %s" % selected_card)
        if "unset" not in selected_card:
            res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
            slot = res.fetchone()[0]
            print("current slot %s" % slot)
            tm.write([0,0,0,0])
            tm.show(selected_card)
            sleep(DELAY)
        


    #res = cur.execute("SELECT cardVal FROM card2slot WHERE slotVal = ?", (slot,))       
    #card = res.fetchone()[0]
    #print("%s" % card)
    #tm.show(selected_card)
    #sleep(DELAY)
    #tm.write([0,0,0,0])

def actuator_motor():
    global actuator_button_state


suit_button.when_pressed = change_suit
card_value_button.when_pressed = change_value
#actuator_button.when_pressed = actuator_motor
pause()


"""

### NONE OF THIS WORKS PROBABLY COULD JUST REMOVE THIS SECTION COMPLETELY ###
while True:
    suit_button_count = 0
    suit_button.when_pressed()
    suit_button_count += 1
    suit = suitMap[suit_button_count]
    print("The suit is set to: %s" % suit)
    if suit_button_count > 4:
        suit_button_count = 0
        print("Suit has been unset")

while True:
    card_value_button.wait_for_press()
    card_value_button_count += 1
    card_value = card_valueMap[card_value_button_count]
    print("The value is set to: %s" % card_value)
    start_time=time.time()
    if (time.time() - start_time) >=4:
        selected_card = card_value + suit
        res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))          
        slot = res.fetchone()[0]
        print("Slot is set to %s to obtain card %s" % (slot,selected_card))
        travel = slot*50
        count = 0
        while count < travel:
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
            count += 1
            time.sleep(.001)

while True:
    actuator_button.wait_for_press()
    actuator__button_count += 1
    
    #Figure this crap out, basically if it's pressed actuator engages and pushes the card up. When switch is let go it decends to 0 point
    #Call to update X card to the selected_card and place the previous X card into the current slot.


##########End of garbage button code section################

"""

"""

#reference code below, most will be re integrated into this script at some point.
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

#define MICROSTEP 16
kit = MotorKit(i2c=board.I2C())
#kit = MotorKit(i2c=busio.I2C( board.SCL, board.SDA, frequency=400_000)
#kit.stepper1.release()

# print name of card as we cycle forward one slot at a time through all 64 slots (to be reused somehow)
slot = 0
travel = 0

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

"""
