import pypot.dynamixel
import numpy
from kinematic import *

#fonction permettant de deplacer une patte en x y et z
def set_pos_to_leg (x, y, z, leg):
    angles = inverse_kinematic(x, y, z)

    if angles == False:
        print 'MoveError'
        return False

    #print angles
    i = 0
    for m in leg:
        m.goal_position = angles[i]
        i+=1

#fonction permettant d'empecher le movement des moteurs à la main
def all_motors_not_compliant (rob):
    for m in rob.motors:
        m.compliant = False


#fonction permettant le movement des moteurs à la main
def all_motors_compliant (rob):
    for m in rob.motors:
        m.compliant = True

#fonction modifant la vitesse des moteurs
def set_motor_speed(rob, v):
    speed = 20 * numpy.cos(2 * numpy.pi * 1 )
    print v
    for s in rob.motors:
        s.moving_speed = speed * (v+1)#goal pour une danse

