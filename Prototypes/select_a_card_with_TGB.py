#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT
# Notes: 64 slots with microstepping in increments of 8 is the best we can do here 52 cards plus 12 extra slots 
# for sets of 4 of a kind) this gives us 51 cards and a single joker to work with in the normal slots and 12 sets 
# of 4 of a kind for a 4 of a kind swap
#NOTE CURRENTLY RUNNING WITH STEP OF 16 I'm not sure if this is any smoother but something I'm playing with, slots are now 50 microsteps appart vs 25 at MS8

import time
import logging
import sys
import board
import busio
import sqlite3
import subprocess
import tm1637 #7 segment display
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit
from gpiozero import LED, Button
from time import sleep
from signal import pause

# Logging bits
LOG_LEVEL = logging.INFO
#LOG_LEVEL = logging.DEBUG
LOG_FILE = "/home/madar/Rolodex/logging/select_a_card_with_TGB.log"
#LOG_FILE = "/dev/stdout"
LOG_FORMAT = "%(asctime)s %(levelname)s %(message)s"
logging.basicConfig(filename=LOG_FILE, format=LOG_FORMAT, level=LOG_LEVEL)
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

"""
logging.info("Informational message")
logging.debug("Helpful debugging info")
logging.error("Something bad happened")
"""

# Zero the Carousel

retcode = subprocess.call(["/usr/bin/python", "/home/madar/GIT/Rolodex/Prototypes/zero_carousel_smooth.py"])
if retcode != 0:
    logging.error("Carousel did not zero properly, exiting")
else:
    logging.info("The carousel is at zero")
# Set some variables we'll be needing

current_slot=0
con = sqlite3.connect("/home/madar/GIT/Rolodex/Prototypes/cards.db", check_same_thread=False)
cur = con.cursor()
CLK = 15
DIO = 14
DELAY = .2
tm = tm1637.TM1637(clk=CLK, dio=DIO)
kit = MotorKit(i2c=board.I2C())
travel = 0

# Display trick name

tm.scroll('Select a card with the Great Billsoni', 100) # 1 fps

#Button variables (what more variables?)

#actuator_button = Button(?)
actuator_button_state = 0 # 0 = down, 1 = up
suit_button = Button(4)
suit_button_count = 0 #unset 1=S, 2=H, 3=C, 4=D 5=unset if suit_button_count > 4: suit_button_count = 0
suitMap = {0:'',1:'S',2:'H',3:'C',4:'D',5:' unset'}
suit = "unset"
card_value_button = Button(26)
card_value_button_count = 0
card_valueMap = {0:'',1:'A',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'10',11:'J',12:'Q',13:'K',14:'unset '}
card_value = "unset"
position_button = Button(16)
position_button_state = 0 # this might need to be position_button_time stored in seconds?
selected_card = suit + card_value

# Position the carousel code

def position_carousel():
    res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
    target_slot = res.fetchone()[0]
    global current_slot
    if current_slot < target_slot: # we are going to go forward
        travel = (target_slot - current_slot) * 25
        logging.info("Required travel to desired_slot %s is %s steps moving forwards" % (target_slot, travel))
        
        step = 0
        while step < travel:
            kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
            time.sleep(.001)
            step +=1
        step = 0
        travel = 0
        current_slot = target_slot
        logging.info("Current slot is %s" % current_slot)
        logging.info("Releasing coils")
        kit.stepper1.release()

        
    if current_slot > target_slot: # we are going to go backwards
        travel = (current_slot - target_slot) * 25
        logging.info("Required travel to desired_slot %s is %s steps moving backwards" % (target_slot, travel))
        step = 0
        while step < travel:
            kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
            time.sleep(.001)
            step +=1
        step = 0
        travel = 0
        current_slot = target_slot
        logging.info("Current slot is %s" % current_slot)
        logging.info("Releasing coils")
        kit.stepper1.release()

# Lift the card (linear actuator time!)

def lift_card():
        logging.info("lift button pressed" )
        kit.stepper2.one

# Button Code

def change_suit():
    global suit_button_count
    global selected_card
    if suit_button_count > 4:
        suit_button_count = 0
    else:
        suit_button_count += 1
        global suit
        global tm
        suit = suitMap[suit_button_count]
        selected_card = card_value + suit
        logging.info("The suit is set to: %s" % suit)
        logging.info("The selected card is %s" % selected_card)
        if "unset" not in selected_card:
            res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
            target_slot = res.fetchone()[0]
            logging.info("target slot is %s" % target_slot)
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
        logging.info("The card value is set to: %s" % card_value)
        logging.info("The selected card is %s" % selected_card)
        if "unset" not in selected_card:
            res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
            target_slot = res.fetchone()[0]
            logging.info("Desired slot %s" % target_slot)
            tm.write([0,0,0,0])
            tm.show(selected_card)
            sleep(DELAY)

def position_motor():
    if "unset" not in selected_card:
        res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
        target_slot = res.fetchone()[0]
        logging.info("Actuator button has been pressed moving to slot %s to obtain %s" % (target_slot, selected_card))
        position_carousel()    
    else:
        logging.info("No card selected")

"""

def lift_card():
    global actuator_button_state
    if "unset" not in selected_card:
        res = cur.execute("SELECT slotVal FROM card2slot WHERE cardVal = ?", (selected_card,))       
        target_slot = res.fetchone()[0]
        logging.info("Actuator button has been pressed moving to slot %s to obtain %s" % (target_slot, selected_card))
        lift_car()    
    else:
        logging.info("No card selected")

"""

suit_button.when_pressed = change_suit
card_value_button.when_pressed = change_value
position_button.when_pressed = position_motor
#actuator_button.when_pressed = lift_card

pause()

