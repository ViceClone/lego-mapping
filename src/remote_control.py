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

tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
ir = InfraredSensor(INPUT_1)
# Set the remote to channel 1

remote=True

def top_left_channel_1_action(state):
    print("top left button")
    if remote :
        if state: # state is True (pressed) or False
                tank_drive.on(60,60)
        else:
                tank_drive.off()

def bottom_left_channel_1_action(state):
    print("bottom left button")
    if remote :
        if state:
                tank_drive.on(-60,-60)
        else:
                tank_drive.off()

def top_right_channel_1_action(state):
    print("top right button")
    if remote :
        if state:
                tank_drive.on_for_seconds(50, -50, 0.95)
				#tank_drive.on(50, -50)
        else:
                tank_drive.off()

def bottom_right_channel_1_action(state):
    print("bottom right button")
    if remote :
        if state:
			#90 degrees avec ~6 de batterie
                tank_drive.on_for_seconds(-50, 50, 1.9)
				#tank_drive.on(-50, 50)
        else:
                tank_drive.off()

def beacon_channel_1_action(state):
        print("beacon button")
        if state:
                remote= not remote
        else:
                tank_drive.off()

ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action
ir.on_channel1_beacon = beacon_channel_1_action


# Sensors and motors input and output
# leds = Leds()

# # Info logging
# logs = open("robot.csv","w")
# robot_positions = open("robot_positions.csv","w")

# # Info inisialization
# logs.write('infrared_distance, left_motor, right_motor, x, y\n')
# logs.write('100, 0, 0, 0, 0\n')
# robot_positions.write('x, y\n')
# robot_positions.write('0, 0\n')

# # Put the infrared sensor into proximity mode.
# ir.mode = 'IR-PROX'

# # Robot Position
# x,y = 0, 0

# # Position flags
# forward_flag =  1
# right_flag =    0
# backward_flag = 0
# left_flag =     0

# # Turn orientation, 0 for left and 1 for right
# turn_orientation = 0

# # Turn orientation probability
# turn_orientation_probability = 0.5

# # Probability of random turn while on stretch
# random_turn_proba = 0.35

# #Value indicating wether remote control mode is on(True) or off(False)

# # Updating the position
# def update_position(x,y):
#     if forward_flag:    y+=1
#     elif right_flag:    x+=1
#     elif backward_flag: y-=1
#     elif left_flag:     x-=1
#     return x,y

# # Updating the flags
# def update_flags_on_turn(forward_flag, right_flag, backward_flag, left_flag, turn_orientation=0):
#     if turn_orientation:
#         if forward_flag:    left_flag, forward_flag =   1, 0
#         elif left_flag:     backward_flag, left_flag =  1, 0
#         elif backward_flag: right_flag, backward_flag = 1, 0
#         elif right_flag:    forward_flag, right_flag =  1, 0
#     else:
#         if forward_flag:    right_flag, forward_flag =  1, 0
#         elif right_flag:    backward_flag, right_flag = 1, 0
#         elif backward_flag: left_flag, backward_flag =  1, 0
#         elif left_flag:     forward_flag, left_flag =   1, 0
#     return forward_flag, right_flag, backward_flag, left_flag

# # Generating the circuit
# # def generate_circuit():
# #     circuit_matrix = np.genfromtxt('robot_positions.csv', delimiter=',')
# #     plt.scatter(*zip(*circuit_matrix[1:]))
# #     plt.plot(*zip(*circuit_matrix[1:]))
# #     plt.show()

# # Handling the ^C key interruption
# def signal_handler(sig, frame):
#     print('\nGenerating the circuit')
#     logs.close()
#     robot_positions.close()
#     leds.set_color('LEFT', 'GREEN')  
#     leds.set_color('RIGHT', 'GREEN')  
#     # generate_circuit()
#     sys.exit(0)

# def signal_handler_with_thread(sig, frame,thread):
#     print('\nGenerating the circuit')
#     logs.close()
#     robot_positions.close()
#     leds.set_color('LEFT', 'GREEN')  
#     leds.set_color('RIGHT', 'GREEN')  
#     # generate_circuit()
#     thread.join()
#     sys.exit(0)

    

# # The deterministic exploration
# # def deterministic_exploration():
# #     while True:   
# #     distance = ir.value()

# #     # If an obstacle occurs
# #     if distance < 50:
# #         leds.set_color('LEFT', 'RED')
# #         leds.set_color('RIGHT', 'RED')
# #         left_speed, right_speed, = 100, 0
# #         tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# #         forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# #                                                                 right_flag, backward_flag, left_flag)
# #         x, y = update_position(x,y)
# #         logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# #         robot_positions.write(str(x) + ', ' + str(y) + '\n') 

# #     # No obstacle in front
# #     else:
# #         leds.set_color('LEFT', 'GREEN')   
# #         leds.set_color('RIGHT', 'GREEN')
# #         left_speed, right_speed, = 25, 25
# #         tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
# #         x, y = update_position(x,y)
# #         logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
# #         robot_positions.write(str(x) + ', ' + str(y) + '\n')

# #     # Handling the ^C key interruption
# #     signal.signal(signal.SIGINT, signal_handler)

# # # The naive exploration
# # def naive_exploration():
# #     while True:   
# #         distance = ir.value()

# #         # If an obstacle occurs
# #         if distance < 50:
# #             leds.set_color('LEFT', 'RED')
# #             leds.set_color('RIGHT', 'RED')
# #             if random.random() < turn_orientation_probability:
# #                 left_speed, right_speed, = 0, 100
# #                 turn_orientation=0
# #             else:
# #                 left_speed, right_speed, = 100, 0
# #                 turn_orientation=1
# #             tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# #             forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# #                                                                     right_flag, backward_flag, left_flag, turn_orientation)
# #             x, y = update_position(x,y)
# #             logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# #             robot_positions.write(str(x) + ', ' + str(y) + '\n') 

# #         # No obstacle in front
# #         else:
# #             leds.set_color('LEFT', 'GREEN')   
# #             leds.set_color('RIGHT', 'GREEN')
# #             left_speed, right_speed, = 25, 25
# #             tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
# #             x, y = update_position(x,y)
# #             logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
# #             robot_positions.write(str(x) + ', ' + str(y) + '\n')
            
# #         # Handling the ^C key interruption
# #         signal.signal(signal.SIGINT, signal_handler)

# #variable globale utilisee par le thread qui mesure les valeurs du senseur en reactive_exploration
# #comment on initialise???
# distance_thread = ir.value()

# def read_sensor():
# 	while(not remote):
# 		distance_thread = ir.value()

# # Indicates if we have to do a 180 turn 
# correct_after_turn = False

# correct_after_random_turn = False

# def make_turn():
# 	leds.set_color('LEFT', 'RED')
# 	leds.set_color('RIGHT', 'RED')
# 	if correct_after_turn :
# 		#turn 180 degrees vers le meme sens qu'il vient de tourner(turn_orientation reste egal) et on fait deux tours 90 degrees
# 		tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# 		forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# 																right_flag, backward_flag, left_flag, turn_orientation)
# 		x, y = update_position(x,y)
# 		logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# 		robot_positions.write(str(x) + ', ' + str(y) + '\n') 
# 		tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# 		forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# 																right_flag, backward_flag, left_flag, turn_orientation)
# 		x, y = update_position(x,y)
# 		logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# 		robot_positions.write(str(x) + ', ' + str(y) + '\n') 
# 		correct_after_turn = False  
# 	else:
# 		if correct_after_random_turn :
# 			if  turn_orientation :
# 				left_speed, right_speed, = 100, 0
# 			else: 
# 				left_speed, right_speed, = 0, 100
# 			tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# 			forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# 																	right_flag, backward_flag, left_flag, turn_orientation)
# 			x, y = update_position(x,y)
# 			logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# 			robot_positions.write(str(x) + ', ' + str(y) + '\n') 
# 			correct_after_random_turn = False
# 		else:
# 		#If an obstacle occurs and we don't have the correction flag up
# 			correct_after_turn = True
# 			if random.random() < turn_orientation_probability:
# 				left_speed, right_speed, = 0, 100
# 				turn_orientation=0
# 			else:
# 				left_speed, right_speed, = 100, 0
# 				turn_orientation=1
# 			tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# 			forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# 																	right_flag, backward_flag, left_flag, turn_orientation)
# 			x, y = update_position(x,y)
# 			logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# 			robot_positions.write(str(x) + ', ' + str(y) + '\n') 

# def reactive_exploration():
# 	thread_sensor = threading.Thread(target = read_sensor)
# 	thread_sensor.start()
# 	while  not remote:   
# 		# If an obstacle occurs or if aleatory turn occurs
# 		if distance_thread < 50 :
# 			make_turn()
# 			# No obstacle in front
# 		else:
# 			if random.random()< random_turn_proba :
# 				leds.set_color('LEFT', 'RED')
# 				leds.set_color('RIGHT', 'RED')
# 				if random.random() < turn_orientation_probability:
# 					left_speed, right_speed, = 0, 100
# 					turn_orientation=0
# 				else:
# 					left_speed, right_speed, = 100, 0
# 					turn_orientation=1
# 				tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1.8)
# 				forward_flag, right_flag, backward_flag, left_flag = update_flags_on_turn(forward_flag, 
# 																		right_flag, backward_flag, left_flag, turn_orientation)
# 				x, y = update_position(x,y)
# 				logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n') 
# 				robot_positions.write(str(x) + ', ' + str(y) + '\n') 
# 				correct_after_random_turn = True
# 			else:
# 				leds.set_color('LEFT', 'GREEN')   
# 				leds.set_color('RIGHT', 'GREEN')
# 				correct_after_turn = False
# 				correct_after_random_turn = False
# 				left_speed, right_speed, = 25, 25
# 				tank_drive.on_for_seconds(SpeedPercent(left_speed), SpeedPercent(right_speed), 1)
# 				x, y = update_position(x,y)
# 				logs.write(str(distance) + ', ' + str(left_speed) + ', ' + str(right_flag) + ', ' + str(x) + ', ' + str(y) + '\n')
# 				robot_positions.write(str(x) + ', ' + str(y) + '\n')
# 		# Handling the ^C key interruption
# 		signal.signal(signal.SIGINT, signal_handler)
# 	thread_sensor.join()

print("ready")
while not remote: 
	# if remote:
	ir.process()
	sleep(0.01)
	# else:
	# 	reactive_exploration() 


