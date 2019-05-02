#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# Write your program here

ir = InfraredSensor(INPUT_4) 
leds = Leds()

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Info logging

logs = open("robot.log","w")

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

print("The color changes due to distance.")

while True:   
    # Infrared sensor in proximity mode will measure distance to the closest
    # object in front of it.

    distance = ir.value()
    logs.write('infrared_distance ' + str(distance) + '\n')
    if distance < 75:
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')
        tank_drive.on_for_seconds(SpeedPercent(100), SpeedPercent(0), 1.2)
        logs.write('right_turn' + '\n')
    else:
        leds.set_color('LEFT', 'GREEN')   
        leds.set_color('RIGHT', 'GREEN')
        tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(30), 3)
        logs.write('move_forward' + '\n')

logs.close()
Sound.beep()       
leds.set_color('LEFT', 'GREEN')  