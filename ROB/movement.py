import pypot.dynamixel
from kinematic import *
from motor_config import *
from walking import *
from special_move import *
from math import *



def initialize_to_zero(rob, group_impair, group_pair, hauteur = 0):

    group_pair[0] = int (group_pair[0])
    group_pair[1] = int (group_pair[1])
    group_pair[2] = int (group_pair[2])
    group_pair[3] = int (group_pair[3])
    group_pair[4] = int (group_pair[4])
    group_pair[5] = int (group_pair[5])
    group_pair[6] = int (group_pair[6])
    group_pair[7] = int (group_pair[7])
    group_pair[8] = int (group_pair[8])

    group_impair[0] = int (group_impair[0])
    group_impair[1] = int (group_impair[1])
    group_impair[2] = int (group_impair[2])
    group_impair[3] = int (group_impair[3])
    group_impair[4] = int (group_impair[4])
    group_impair[5] = int (group_impair[5])
    group_impair[6] = int (group_impair[6])
    group_impair[7] = int (group_impair[7])
    group_impair[8] = int (group_impair[8])


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
        if group_pair[0] < 160:
            group_pair[0] += 1
        elif group_pair[0] > 160:
            group_pair[0] -= 1
        elif x1 == 0:
            x1 = 1
            etat += 1
        if group_pair[1] < 0:
            group_pair[1] += 1
        elif group_pair[1] > 0:
            group_pair[1] -= 1
        elif x2 == 0:
            x2 = 1
            etat += 1
        if group_pair[2] < 160:
            group_pair[2] += 1
        elif group_pair[2] > 160:
            group_pair[2] -= 1
        elif x3 == 0:
            x3 = 1
            etat += 1
        if group_impair[0] < 0:
            group_impair[0] += 1
        elif group_impair[0] > 0:
            group_impair[0] -= 1
        elif xx1 == 0:
            xx1 = 1
            etat += 1
        if group_impair[1] < 160:
            group_impair[1] += 1
        elif group_impair[1] > 160:
            group_impair[1] -= 1
        elif xx2 == 0:
            xx2 = 1
            etat += 1
        if group_impair[2] < 160:
            group_impair[2] += 1
        elif group_impair[2] > 160:
            group_impair[2] -= 1
        elif xx3 == 0:
            xx3 = 1
            etat += 1

        if group_pair[3] < 95:
            group_pair[3] += 1
        elif group_pair[3] > 95:
            group_pair[3] -= 1
        elif y1 == 0:
            y1 = 1
            etat += 1
        if group_pair[4] < 180:
            group_pair[4] += 1
        elif group_pair[4] > 180:
            group_pair[4] -= 1
        elif y2 == 0:
            y2 = 1
            etat += 1
        if group_pair[5] < 95:
            group_pair[5] += 1
        elif group_pair[5] > 95:
            group_pair[5] -= 1
        elif y3 == 0:
            y3 = 1
            etat += 1
        if group_impair[3] < 180:
            group_impair[3] += 1
        elif group_impair[3] > 180:
            group_impair[3] -= 1
        elif yy1 == 0:
            yy1 = 1
            etat += 1
        if group_impair[4] < 95:
            group_impair[4] += 1
        elif group_impair[4] > 95:
            group_impair[4] -= 1
        elif yy2 == 0:
            yy2 = 1
            etat += 1
        if group_impair[5] < 95:
            group_impair[5] += 1
        elif group_impair[5] > 95:
            group_impair[5] -= 1
        elif yy3 == 0:
            yy3 = 1
            etat += 1

        if group_pair[6] < -70 + hauteur:
            group_pair[6] += 1
        elif group_pair[6] > -70 - hauteur:
            group_pair[6] -= 1
        elif z1 == 0:
            z1 = 1
            etat += 1
        if group_pair[7] < -70 + hauteur:
            group_pair[7] += 1
        elif group_pair[7] > -70 - hauteur:
            group_pair[7] -= 1
        elif z2 == 0:
            z2 = 1
            etat += 1
        if group_pair[8] < -70 + hauteur:
            group_pair[8] += 1
        elif group_pair[8] > -70 - hauteur:
            group_pair[8] -= 1
        elif z3 == 0:
            z3 = 1
            etat += 1
        if group_impair[6] < -70 + hauteur:
            group_impair[6] += 1
        elif group_impair[6] > -70 - hauteur:
            group_impair[6] -= 1
        elif zz1 == 0:
            zz1 = 1
            etat += 1
        if group_impair[7] < -70 + hauteur:
            group_impair[7] += 1
        elif group_impair[7] > -70 - hauteur:
            group_impair[7] -= 1
        elif zz2 == 0:
            zz2 = 1
            etat += 1
        if group_impair[8] < -70 + hauteur:
            group_impair[8] += 1
        elif group_impair[8] > -70 - hauteur:
            group_impair[8] -= 1
        elif zz3 == 0:
            zz3 = 1
            etat += 1

        move (rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

        time.sleep(0.005)


def move(rob, group_pair, group_impair):
    set_pos_to_leg(group_impair[0], group_impair[3], group_impair[6], rob.leg1)
    set_pos_to_leg(group_pair[0], group_pair[3], group_pair[6], rob.leg2)
    set_pos_to_leg(group_impair[1], group_impair[4], group_impair[7], rob.leg3)
    set_pos_to_leg(group_pair[1], group_pair[4], group_pair[7], rob.leg4)
    set_pos_to_leg(group_impair[2], group_impair[5], group_impair[8], rob.leg5)
    set_pos_to_leg(group_pair[2], group_pair[5], group_pair[8], rob.leg6)

def modification_repere_bot_impair(leg_impair):
    leg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    leg[0] = leg_impair[3] - 60
    leg[1] = leg_impair[1] - 40
    leg[2] = leg_impair[2] - 40

    leg[3] = -leg_impair[0]
    leg[4] = -leg_impair[4] + 25
    leg[5] = leg_impair[5] - 25

    leg[6] = leg_impair[6]
    leg[7] = leg_impair[7]
    leg[8] = leg_impair[8]

    return leg


def modification_repere_bot_pair(leg_pair):
    leg = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    leg[0] = leg_pair[0] - 40
    leg[1] = leg_pair[4] - 60
    leg[2] = leg_pair[2] - 40

    leg[3] = leg_pair[3] - 25
    leg[4] = leg_pair[1]
    leg[5] = -(leg_pair[5] - 25)

    leg[6] = leg_pair[6]
    leg[7] = leg_pair[7]
    leg[8] = leg_pair[8]

    return leg

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