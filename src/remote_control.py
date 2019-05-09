import sys
import signal
import random
import threading

# import numpy as np
# import matplotlib.pyplot as plt

from time import sleep
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, MoveTank
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

end = False

def top_left_channel_1_action(state):
	print("top left button")
	tank_drive.on_for_seconds(60,60,0.5)

def bottom_left_channel_1_action(state):
	print("bottom left button")
	tank_drive.on_for_seconds(-60,-60,0.5)
	# else:
	# 	tank_drive.off()

def top_right_channel_1_action(state):
	print("top right button")
	tank_drive.on_for_seconds(-50,50,0.5)

def bottom_right_channel_1_action(state):
	print("bottom right button")
	tank_drive.on_for_seconds(50,-50,0.5)

def beacon_channel_1_action(state):
	print("beacon button")
	if state:
		end= True
	else:
		tank_drive.off()

ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action
ir.on_channel1_beacon = beacon_channel_1_action

print("ready")
while not end: 
	ir.process()
	sleep(0.01)
sys.exit(0)



