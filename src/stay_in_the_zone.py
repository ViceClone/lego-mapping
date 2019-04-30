#!/usr/bin/env python3

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# Write your program here

ir = InfraredSensor() 
leds = Leds()

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

print("The color changes due to distance.")


while True:   
    # Infrared sensor in proximity mode will measure distance to the closest
    # object in front of it.

    distance = ir.value()

    if distance < 50:
        Leds.set_color(Leds.LEFT, Leds.RED)
        Leds.set_color(Leds.RIGHT, Leds.RED)
        tank_drive.on_for_seconds(SpeedPercent(100), SpeedPercent(0), 15)
    else:
        Leds.set_color(Leds.LEFT, Leds.GREEN)
        Leds.set_color(Leds.RIGHT, Leds.GREEN)
        tank_drive.on_for_seconds(SpeedPercent(100), SpeedPercent(100), 3)
        
Sound.beep()       
Leds.set_color(Leds.LEFT, Leds.GREEN)  