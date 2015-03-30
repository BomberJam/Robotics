import pypot.dynamixel
import numpy
from kinematic import *

def set_pos_to_leg (x, y, z, leg):
    angles = inverse_kinematic(x, y, z)
    #print angles
    i = 0
    for m in leg:
        m.goal_position = angles[i]
        i+=1

def all_motors_not_compliant (rob):
    for m in rob.motors:
        m.compliant = False

def set_motor_speed(rob, v):
    speed = 20 * numpy.cos(2 * numpy.pi * 1 )

    for s in rob.motors:
        s.moving_speed = speed * (v+1)#goal pour une danse

