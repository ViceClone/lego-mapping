import sys
import signal
import random

# import numpy as np
# import matplotlib.pyplot as plt

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
from ev3dev2.led import Leds
from ev3dev2.sound import Sound

# Sensors and motors input and output
ir = InfraredSensor(INPUT_1) 
leds = Leds()
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)

# Info logging
logs = open("robot.csv","w")
robot_positions = open("robot_positions.csv","w")

# Info inisialization
logs.write('infrared_distance, left_motor, right_motor, x, y\n')
logs.write('100, 0, 0, 0, 0\n')
robot_positions.write('x, y\n')
robot_positions.write('0, 0\n')

# Put the infrared sensor into proximity mode.
ir.mode = 'IR-PROX'

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

# Generating the circuit
# def generate_circuit():
#     circuit_matrix = np.genfromtxt('robot_positions.csv', delimiter=',')
#     plt.scatter(*zip(*circuit_matrix[1:]))
#     plt.plot(*zip(*circuit_matrix[1:]))
#     plt.show()

# Handling the ^C key interruption
def signal_handler(sig, frame):
    print('\nGenerating the circuit')
    logs.close()
    robot_positions.close()
    leds.set_color('LEFT', 'GREEN')  
    leds.set_color('RIGHT', 'GREEN')  
    # generate_circuit()
    sys.exit(0)

# The deterministic exploration
def deterministic_exploration():
    while True:   
        distance = ir.value()

        # If an obstacle occurs
        if distance < 25:
            leds.set_color('LEFT', 'RED')
            leds.set_color('RIGHT', 'RED')
            left_speed, right_speed, = 50, -50
            tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.90)
            forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                    right_flag, backward_flag, left_flag)
            x, y = update_position(x,y)
            logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
            robot_positions.write(str(x) + ', ' + str(y) + '\n') 

        # No obstacle in front
        else:
            leds.set_color('LEFT', 'GREEN')   
            leds.set_color('RIGHT', 'GREEN')
            left_speed, right_speed, = 25, 25
            tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
            x, y = update_position(x,y)
            logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
            robot_positions.write(str(x) + ', ' + str(y) + '\n')

        # Handling the ^C key interruption
        signal.signal(signal.SIGINT, signal_handler)

# The naive exploration
def naive_exploration():
    while True:   
        distance = ir.value()

        # If an obstacle occurs
        if distance < 50:
            leds.set_color('LEFT', 'RED')
            leds.set_color('RIGHT', 'RED')
            if random.random() < turn_orientation_probability:
                left_speed, right_speed, = -50, 50
                turn_orientation=0
            else:
                left_speed, right_speed, = 50, -50
                turn_orientation=1
            tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.89)
            forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                    right_flag, backward_flag, left_flag, turn_orientation)
            x, y = update_position(x,y)
            logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
            robot_positions.write(str(x) + ', ' + str(y) + '\n') 

        # No obstacle in front
        else:
            leds.set_color('LEFT', 'GREEN')   
            leds.set_color('RIGHT', 'GREEN')
            left_speed, right_speed, = 25, 25
            tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
            x, y = update_position(x,y)
            logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
            robot_positions.write(str(x) + ', ' + str(y) + '\n')
            
        # Handling the ^C key interruption
        signal.signal(signal.SIGINT, signal_handler)

# Algorithm demo
while True:   
    distance = ir.value()

    # If an obstacle occurs
    if distance < 25:
        leds.set_color('LEFT', 'RED')
        leds.set_color('RIGHT', 'RED')
        left_speed, right_speed, = 50, -50
        tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 0.91)
        forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
                                                                right_flag, backward_flag, left_flag)
        x, y = update_position(x,y)
        logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
        robot_positions.write(str(x) + ', ' + str(y) + '\n') 

    # No obstacle in front
    else:
        leds.set_color('LEFT', 'GREEN')   
        leds.set_color('RIGHT', 'GREEN')
        left_speed, right_speed, = 25, 25
        tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
        x, y = update_position(x,y)
        logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
        robot_positions.write(str(x) + ', ' + str(y) + '\n')

    # Handling the ^C key interruption
    signal.signal(signal.SIGINT, signal_handler)