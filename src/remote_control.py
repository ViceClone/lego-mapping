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

end=False

def top_left_channel_1_action(state):
    print("top left button")
	if state: # state is True (pressed) or False
			tank_drive.on(60,60)
	else:
			tank_drive.off()

def bottom_left_channel_1_action(state):
    print("bottom left button")
	if state:
			tank_drive.on(-60,-60)
	else:
			tank_drive.off()

def top_right_channel_1_action(state):
    print("top right button")
	if state:
		tank_drive.on_for_seconds(50, -50, 0.95)
		#tank_drive.on(50, -50)
	else:
		tank_drive.off()

def bottom_right_channel_1_action(state):
    print("bottom right button")
    if not end :
        if state:
			#90 degrees avec ~6 de batterie
			tank_drive.on_for_seconds(-50, 50, 1.9)
			#tank_drive.on(-50, 50)
        else:
            tank_drive.off()

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



