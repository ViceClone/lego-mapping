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

logs = open("robot.csv","w")
logs.write('infrared_distance, left_motor, right_motor, x, y\n')
logs.write('100, 0, 0, 0, 0\n')

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

# Robot Position
x,y = 0, 0

# Position flags
forward_flag =  1
right_flag =    0
backward_flag = 0
left_flag =     0

while True:   
    distance = ir.value()
    if distance < 50:
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')
        tank_drive.on_for_seconds(SpeedPercent(100), SpeedPercent(0), 1.3)
        forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                right_flag, backward_flag, left_flag)
        x, y = updated_position(x,y)
        logs.write(str(distance) + ', 100, 0, ' + str(x) + ', ' + str(y) + '\n')
    else:
        leds.set_color('LEFT', 'GREEN')   
        leds.set_color('RIGHT', 'GREEN')
        tank_drive.on_for_seconds(SpeedPercent(30), SpeedPercent(30), 3)
        x, y = updated_position(x,y)
        logs.write(str(distance) + ', 30, 30, ' + str(x) + ', ' + str(y) + '\n')

logs.close()
Sound.beep()       
leds.set_color('LEFT', 'GREEN')  

def updated_position(x,y):
    if forward_flag:    y+=1
    elif right_flag:    x+=1
    elif backward_flag: y-=1
    elif left_flag:     x-=1
    return x,y

def update_flags_on_turn(forward_flag, right_flag, backward_flag, left_flag):
    if forward_flag:    right_flag, forward_flag =  1, 0
    elif right_flag:    backward_flag, right_flag = 1, 0
    elif backward_flag: left_flag, backward_flag =  1, 0
    elif left_flag:     forward_flag, left_flag =   1, 0
    return forward_flag, right_flag, backward_flag, left_flag