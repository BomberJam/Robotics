import pypot.dynamixel
from kinematic import *
from motor_config import *
from walking import *
from special_move import *
from math import *



def initialize_to_zero(rob, group_impair, group_pair):
    etat = 0
    x1 = 0
    x2 = 0
    x3 = 0
    xx1 = 0
    xx2 = 0
    xx3 = 0
    y1 = 0
    y2 = 0
    y3 = 0
    yy1 = 0
    yy2 = 0
    yy3 = 0
    z1 = 0
    z2 = 0
    z3 = 0
    zz1 = 0
    zz2 = 0
    zz3 = 0

    while etat != 18:
        if group_pair[0] < 120:
            group_pair[0] += 1
        elif group_pair[0] > 120:
            group_pair[0] -= 1
        elif x1 == 0:
            x1 = 1
            etat += 1
        if group_pair[1] < 120:
            group_pair[1] += 1
        elif group_pair[1] > 120:
            group_pair[1] -= 1
        elif x2 == 0:
            x2 = 1
            etat += 1
        if group_pair[2] < 120:
            group_pair[2] += 1
        elif group_pair[2] > 120:
            group_pair[2] -= 1
        elif x3 == 0:
            x3 = 1
            etat += 1
        if group_impair[0] < 120:
            group_impair[0] += 1
        elif group_impair[0] > 120:
            group_impair[0] -= 1
        elif xx1 == 0:
            xx1 = 1
            etat += 1
        if group_impair[1] < 120:
            group_impair[1] += 1
        elif group_impair[1] > 120:
            group_impair[1] -= 1
        elif xx2 == 0:
            xx2 = 1
            etat += 1
        if group_impair[2] < 120:
            group_impair[2] += 1
        elif group_impair[2] > 120:
            group_impair[2] -= 1
        elif xx3 == 0:
            xx3 = 1
            etat += 1

        if group_pair[3] < 70:
            group_pair[3] += 1
        elif group_pair[3] > 70:
            group_pair[3] -= 1
        elif y1 == 0:
            y1 = 1
            etat += 1
        if group_pair[4] < 0:
            group_pair[4] += 1
        elif group_pair[4] > 0:
            group_pair[4] -= 1
        elif y2 == 0:
            y2 = 1
            etat += 1
        if group_pair[5] < -70:
            group_pair[5] += 1
        elif group_pair[5] > -70:
            group_pair[5] -= 1
        elif y3 == 0:
            y3 = 1
            etat += 1
        if group_impair[3] < 0:
            group_impair[3] += 1
        elif group_impair[3] > 0:
            group_impair[3] -= 1
        elif yy1 == 0:
            yy1 = 1
            etat += 1
        if group_impair[4] < -70:
            group_impair[4] += 1
        elif group_impair[4] > -70:
            group_impair[4] -= 1
        elif yy2 == 0:
            yy2 = 1
            etat += 1
        if group_impair[5] < 70:
            group_impair[5] += 1
        elif group_impair[5] > 70:
            group_impair[5] -= 1
        elif yy3 == 0:
            yy3 = 1
            etat += 1

        if group_pair[6] < -70:
            group_pair[6] += 1
        elif group_pair[6] > -70:
            group_pair[6] -= 1
        elif z1 == 0:
            z1 = 1
            etat += 1
        if group_pair[7] < -70:
            group_pair[7] += 1
        elif group_pair[7] > -70:
            group_pair[7] -= 1
        elif z2 == 0:
            z2 = 1
            etat += 1
        if group_pair[8] < -70:
            group_pair[8] += 1
        elif group_pair[8] > -70:
            group_pair[8] -= 1
        elif z3 == 0:
            z3 = 1
            etat += 1
        if group_impair[6] < -70:
            group_impair[6] += 1
        elif group_impair[6] > -70:
            group_impair[6] -= 1
        elif zz1 == 0:
            zz1 = 1
            etat += 1
        if group_impair[7] < -70:
            group_impair[7] += 1
        elif group_impair[7] > -70:
            group_impair[7] -= 1
        elif zz2 == 0:
            zz2 = 1
            etat += 1
        if group_impair[8] < -70:
            group_impair[8] += 1
        elif group_impair[8] > -70:
            group_impair[8] -= 1
        elif zz3 == 0:
            zz3 = 1
            etat += 1

        set_pos_to_leg(group_impair[0], group_impair[3], group_impair[6], rob.leg1)
        set_pos_to_leg(group_pair[0], group_pair[3], group_pair[6], rob.leg2)
        set_pos_to_leg(group_impair[1], group_impair[4], group_impair[7], rob.leg3)
        set_pos_to_leg(group_pair[1], group_pair[4], group_pair[7], rob.leg4)
        set_pos_to_leg(group_impair[2], group_impair[5], group_impair[8], rob.leg5)
        set_pos_to_leg(group_pair[2], group_pair[5], group_pair[8], rob.leg6)

        time.sleep(0.005)



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