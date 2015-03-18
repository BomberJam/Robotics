import pypot.dynamixel
from kinematic import *
from motor_config import *
from walking import *
from special_move import *



def initialize_to_zero(rob):
    set_pos_to_leg(120, 0, -70, rob.leg1)
    set_pos_to_leg(120, 70, -70, rob.leg2)
    set_pos_to_leg(120, -70, -70, rob.leg3)
    set_pos_to_leg(120, 0, -70, rob.leg4)
    set_pos_to_leg(120, 70, -70, rob.leg5)
    set_pos_to_leg(120, -70, -70, rob.leg6)


def switch_walking(rob, direction, speed, distance):
    parcour = 0
    while True:
        if direction == 1:
            forward(rob, speed, distance)
        elif direction == 2:
            backward(rob, speed, distance)
        elif direction == 3:
            left(rob, speed, distance)
        elif direction == 4:
            right(rob, speed, distance)
        parcour += distance*2
        print 'distance parcouru : ', parcour, '\n'


def switch_rotation(rob, direction):
    while True:
        if direction == 1:
            rotation_right2(rob)
        elif direction == 2:
            rotation_left2(rob)


def cheat(rob, cheat):
    if cheat == 1:
        script_auto_f5(rob)
    elif cheat == 2:
        move_10mm(rob)