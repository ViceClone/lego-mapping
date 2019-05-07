import numpy as np 

from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, SpeedPercent, MoveTank
tank_drive = MoveTank(OUTPUT_A, OUTPUT_B)
from ev3dev2.sensor import INPUT_1, INPUT_4
from ev3dev2.sensor.lego import TouchSensor, InfraredSensor
ir = InfraredSensor(INPUT_1) 
rays_list = []
import time
import threading
f = open("log_scan.csv","w")
f.write("time , distance \n")
def get_ir_value():
    rays = []
    debut = time.time()
    while time.time()-debut<19:
        rays.extend([ir.value()])
        print(time.time()-debut," , ",ir.value())
        f.write(str(time.time()-debut)+" , "+str(ir.value())+"\n")
        time.sleep(0.01)
    return rays

def move_robot():
    thread1 = threading.Thread(target=tank_drive.on_for_seconds, args=(SpeedPercent(10), SpeedPercent(-10), 18.5))
    thread2 = threading.Thread(target=get_ir_value, args=())
    thread2.start()
    thread1.start()
    return 

if __name__=="__main__":
    move_robot()