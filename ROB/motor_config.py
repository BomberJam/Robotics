import pypot.dynamixel
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