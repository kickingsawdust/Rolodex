# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
import board
import busio
from adafruit_motor import stepper
from adafruit_motorkit import MotorKit

#define MICROSTEP 16
kit = MotorKit(i2c=board.I2C())
#kit = MotorKit(i2c=busio.I2C( board.SCL, board.SDA, frequency=400_000)
#kit.stepper1.release()

count = 0
while count < 1:
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

    print("Microsteps")
    for i in range(1600):
        kit.stepper1.onestep(direction=stepper.FORWARD, style=stepper.MICROSTEP)
        time.sleep(.0001)
    for i in range(1600):
        kit.stepper1.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        time.sleep(.0001)
    count +=1



kit.stepper1.release()
