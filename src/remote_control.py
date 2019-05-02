from ev3dev2.motor import OUTPUT_A, OUTPUT_B, MoveSteering
from ev3dev2.sensor.lego import InfraredSensor
from time import sleep

# top left: go forwards 1
# bottom left: go backwards 2
# top right: turn right on the spot 3
# bottom right: turn left on the spot 4

steer_pair = MoveSteering(OUTPUT_A, OUTPUT_B)
ir = InfraredSensor()
prev_action=0
# Set the remote to channel 1

def top_left_channel_1_action(state):
    if state: # state is True (pressed) or False
        if prev_action==2:
            steer_pair.on(steering=0, speed=0)
        else:
            steer_pair.on(steering=0, speed=40)
    else:
        steer_pair.off()

def bottom_left_channel_1_action(state):
    if state:
        if prev_action==1:
            steer_pair.on(steering=0, speed=0)
        else:
            steer_pair.on(steering=0, speed=-40)
    else:
        steer_pair.off()

def top_right_channel_1_action(state):
    if state:
        steer_pair.on(steering=100, speed=30)
    else:
        steer_pair.off()

def bottom_right_channel_1_action(state):
    if state:
        steer_pair.on(steering=-100, speed=30)
    else:
        steer_pair.off()

ir.on_channel1_top_left = top_left_channel_1_action
ir.on_channel1_bottom_left = bottom_left_channel_1_action
ir.on_channel1_top_right = top_right_channel_1_action
ir.on_channel1_bottom_right = bottom_right_channel_1_action

while True:
    prev_state=state
    ir.process()
    sleep(0.01)