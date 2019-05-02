import ev3dev.ev3 as ev3
from include.odometrium.main import Odometrium
from time import sleep

# left='B'                  the left wheel is connected to port B
# right='C'                 the right wheel is connected to port C
# wheel_diameter=5.5        the wheel diameter is 5.5cm
# wheel_distance=12         the wheel distance is 12cm
# unit sidenote: as long as you are consistent, you can also use mm, inches, km.
# returned values are in these units
# counts per rotation are is the number of motor-internal 'tacho-counts'
# that the motor has to travel for one full revolution
# this is motor specific
#
# count_per_rot_left=None   use the default value returned by the motor for the left motor
# count_per_rot_right=360   for the right motor treat 360 tacho counts as one full revolution
# debug=False               print the current position (on motor speed change) and
#                           echo all the movement logs when the object is destroyed
# curve_adjustment=0.873    use curve adjustment factor of 0.873, see below ('percision')  
pos_info = Odometrium(left='B', right='C', wheel_diameter=5.5, wheel_distance=12,
                      count_per_rot_left=None, count_per_rot_right=360, debug=False,
                      curve_adjustment=1)

# drive for 3 seconds with both wheels at the speed of 50 (internal motor speed)
# when time is used, the command is by default blocking:
pos_info.move(left=50, right=50, time=3)
print('Done moving.')

# the command can be made non-blocking by using the parameter 'blocking':
pos_info.move(left=50, right=50, time=3, blocking=False)
print('Movement started...')
# now wait until the motors stopped
pos_info.wait()
print('Movement stopped.')

# start driving with the left wheel at 50 and the right wheel at 80
pos_info.move(left=50, right=80)
# wait for 3 seconds...
sleep(3)
# ... and stop both motors
pos_info.stop()

# also available as blocking, but quite useless then
# and your motors don't stop spinning!
pos_info.move(left=50, right=80, blocking=True)

# increase speed of the left wheel by 10
# and decrease the speed of the right wheel by 20
pos_info.change_speed(left=10, right=-20)

# decrease speed of the left wheel by 5
pos_info.change_speed(left=-5)

# make the left wheel 10 faster than the right wheel
pos_info.speed_left = pos_info.speed_right + 10

# and stop the right motor completly
pos_info.speed_right = 0

# query the current position
x = pos_info.x
y = pos_info.y

# get the current orientation in degrees
# the returned value is ≥0 and <2 * pi
# the start value is 0 degrees by default
# one quarter to the right e.g. return 0.5 * pi
orientation = pos_info.orientation