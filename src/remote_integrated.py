import sys
import signal
import random
import threading

# import numpy as np
# import matplotlib.pyplot as plt

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank,MoveSteering
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# top left: go forwards 1
# bottom left: go backwards 2
# top right: turn right on the spot 3
# bottom right: turn left on the spot 4

leds = Leds()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
ir = InfraredSensor()
# Set the remote to channel 1

remote = False

def top_left_channel_1_action(state):
	print("top left button")
    if not remote:
	    tank_drive.on(60,60)

def bottom_left_channel_1_action(state):
	print("bottom left button")
    if not remote:
	    tank_drive.on(-60,-60)
	# else:
	# 	tank_drive.off()

def top_right_channel_1_action(state):
	print("top right button")
	if not remote:
	    tank_drive.on(50, -50)
	# if state:
		#tank_drive.on_for_seconds(50, -50, 0.95)
	# else:
	# 	tank_drive.off()

def bottom_right_channel_1_action(state):
	print("bottom right button")
	if not remote:
	    tank_drive.on(-50, 50)

def beacon_channel_1_action(state):
	print("beacon button")
    if remote:
        ir = InfraredSensor(INPUT_1) 
        ir.mode = 'IR-PROX'
    else:
        ir = InfraredSensor()
	remote= not remote

ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action
ir.on_channel1_beacon = beacon_channel_1_action

logs = open("robot.csv","w")
robot_positions = open("robot_positions.csv","w")

# Info inisialization
logs.write('infrared_distance, left_motor, right_motor, x, y\n')
logs.write('100, 0, 0, 0, 0\n')
robot_positions.write('x, y\n')
robot_positions.write('0, 0\n')

# Robot Position
x,y = 0, 0

# Position flags
forward_flag =  1
right_flag =    0
backward_flag = 0
left_flag =     0

# Turn orientation, 0 for left and 1 for right
turn_orientation = 0

# Turn orientation probability
turn_orientation_probability = 0.5

# Probability of random turn while on stretch
random_turn_proba = 0.1

# Updating the position
def update_position(x,y):
    if forward_flag:    y+=1
    elif right_flag:    x+=1
    elif backward_flag: y-=1
    elif left_flag:     x-=1
    return x,y

# Updating the flags
def update_flags_on_turn(forward_flag, right_flag, backward_flag, left_flag, turn_orientation=0):
    if turn_orientation:
        if forward_flag:    left_flag, forward_flag =   1, 0
        elif left_flag:     backward_flag, left_flag =  1, 0
        elif backward_flag: right_flag, backward_flag = 1, 0
        elif right_flag:    forward_flag, right_flag =  1, 0
    else:
        if forward_flag:    right_flag, forward_flag =  1, 0
        elif right_flag:    backward_flag, right_flag = 1, 0
        elif backward_flag: left_flag, backward_flag =  1, 0
        elif left_flag:     forward_flag, left_flag =   1, 0
    return forward_flag, right_flag, backward_flag, left_flag

def signal_handler(sig, frame):
    logs.close()
    robot_positions.close()
    leds.set_color('LEFT', 'GREEN')  
    leds.set_color('RIGHT', 'GREEN')  
    sys.exit(0)

distance = ir.value()

turn_distance = 25

print("ready")
while True: 
    if remote:
        ir.process()
        sleep(0.01)
    else:
        while not remote:  
            distance = ir.value() 
            # If an obstacle occurs or if aleatory turn occurs  
            if distance < turn_distance :
                leds.set_color('LEFT', 'RED')
                leds.set_color('RIGHT', 'RED')
                if correct_after_random_turn :
                    if  turn_orientation :
                        left_speed, right_speed, = 50, -50
                    else: 
                        left_speed, right_speed, = -50, 50
                    tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.90)
                    forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                            right_flag, backward_flag, left_flag, turn_orientation)
                    x, y = update_position(x,y)
                    logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
                    robot_positions.write(str(x) + ', ' + str(y) + '\n') 
                    correct_after_random_turn = False
                else:
                #If an obstacle occurs and we don't have the correction flag up
                    if random.random() < turn_orientation_probability:
                        left_speed, right_speed, = -50, 50
                        turn_orientation=0
                    else:
                        left_speed, right_speed, = 50, -50
                        turn_orientation=1
                    tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.90)
                    forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                            right_flag, backward_flag, left_flag, turn_orientation)
                    x, y = update_position(x,y)
                    logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
                    robot_positions.write(str(x) + ', ' + str(y) + '\n') 
                    # No obstacle in front
            else:
                if random.random()< random_turn_proba :
                    leds.set_color('LEFT', 'RED')
                    leds.set_color('RIGHT', 'RED')
                    if random.random() < turn_orientation_probability:
                        left_speed, right_speed, = -50, 50
                        turn_orientation=0
                    else:
                        left_speed, right_speed, = 50, -50
                        turn_orientation=1
                    tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.90)
                    forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                            right_flag, backward_flag, left_flag, turn_orientation)
                    x, y = update_position(x,y)
                    logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
                    robot_positions.write(str(x) + ', ' + str(y) + '\n') 
                    correct_after_random_turn = True
                else:
                    leds.set_color('LEFT', 'GREEN')   
                    leds.set_color('RIGHT', 'GREEN')
                    correct_after_random_turn = False
                    left_speed, right_speed, = 50, 50
                    tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
                    x, y = update_position(x,y)
                    logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
                    robot_positions.write(str(x) + ', ' + str(y) + '\n')
            # Handling the ^C key interruption
            signal.signal(signal.SIGINT, signal_handler)



