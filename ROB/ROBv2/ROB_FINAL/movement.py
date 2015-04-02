import pypot.dynamixel
from kinematic import *
from motor_config import *
from math import *


#fonction d'initialisation des moteurs
def initialize_to_zero(rob, group_impair, group_pair, hauteur = 0):

    #cast des coordonnes pour eviter les chiffres  a virgule
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

    h = -hauteur

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

        if hauteur < 0:
            if ((group_pair[6] == (-70-h)) and z1 == 0):
                z1 = 1
                etat += 1
            elif z1 == 0:
                if group_pair[6] < (-70-h):
                    group_pair[6] = group_pair[6] + 1
                elif group_pair[6] > (-70 - h):
                    group_pair[6] = group_pair[6] - 1

            if ((group_pair[7] == (-70-h)) and z2 == 0):
                z2 = 1
                etat += 1
            elif z2 == 0:
                if group_pair[7] < (-70-h):
                    group_pair[7] = group_pair[7] + 1
                elif group_pair[7] > (-70 - h):
                    group_pair[7] = group_pair[7] - 1

            if ((group_pair[8] == (-70-h)) and z3 == 0):
                z3 = 1
                etat += 1
            elif z3 == 0:
                if group_pair[8] < (-70-h):
                    group_pair[8] = group_pair[8] + 1
                elif group_pair[8] > (-70 - h):
                    group_pair[8] = group_pair[8] - 1

            if group_impair[6] != (-70 - hauteur) and zz1 == 0:
                if group_impair[6] < (-70 - hauteur):
                    group_impair[6] += 1
                elif group_impair[6] > (-70 - hauteur):
                    group_impair[6] -= 1
            elif zz1 == 0:
                zz1 = 1
                etat += 1
            if group_impair[7] != (-70 - hauteur) and zz2 == 0:
                if group_impair[7] < (-70 - hauteur):
                    group_impair[7] += 1
                elif group_impair[7] > (-70 - hauteur):
                    group_impair[7] -= 1
            elif zz2 == 0:
                zz2 = 1
                etat += 1
            if group_impair[8] != (-70 - hauteur) and zz3 == 0:
                if group_impair[8] < (-70 - hauteur):
                    group_impair[8] += 1
                elif group_impair[8] > (-70 - hauteur):
                    group_impair[8] -= 1
            elif zz3 == 0:
                zz3 = 1
                etat += 1
        else:


            if ((group_pair[6] == (-70-h)) and z1 == 0):
                z1 = 1
                etat += 1
            elif z1 == 0:
                if group_pair[6] < (-70-h):
                    group_pair[6] = group_pair[6] + 1
                elif group_pair[6] > (-70 - h):
                    group_pair[6] = group_pair[6] - 1

            if ((group_pair[7] == (-70-h)) and z2 == 0):
                z2 = 1
                etat += 1
            elif z2 == 0:
                if group_pair[7] < (-70-h):
                    group_pair[7] = group_pair[7] + 1
                elif group_pair[7] > (-70 - h):
                    group_pair[7] = group_pair[7] - 1

            if ((group_pair[8] == (-70-h)) and z3 == 0):
                z3 = 1
                etat += 1
            elif z3 == 0:
                if group_pair[8] < (-70-h):
                    group_pair[8] = group_pair[8] + 1
                elif group_pair[8] > (-70 - h):
                    group_pair[8] = group_pair[8] - 1

            if group_impair[6] != (-70 + hauteur) and zz1 == 0:
                if group_impair[6] < (-70 + hauteur):
                    group_impair[6] += 1
                elif group_impair[6] > (-70 + hauteur):
                    group_impair[6] -= 1
            elif zz1 == 0:
                zz1 = 1
                etat += 1
            if group_impair[7] != (-70 + hauteur) and zz2 == 0:
                if group_impair[7] < (-70 + hauteur):
                    group_impair[7] += 1
                elif group_impair[7] > (-70 + hauteur):
                    group_impair[7] -= 1
            elif zz2 == 0:
                zz2 = 1
                etat += 1
            if group_impair[8] != (-70 + hauteur) and zz3 == 0:
                if group_impair[8] < (-70 + hauteur):
                    group_impair[8] += 1
                elif group_impair[8] > (-70 + hauteur):
                    group_impair[8] -= 1
            elif zz3 == 0:
                zz3 = 1
                etat += 1

        #print group_impair, '\n', group_pair, '\n', etat
        move (rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

        time.sleep(0.005)

#fonction permettant le deplacement des moteus
def move(rob, group_pair, group_impair):
    set_pos_to_leg(group_impair[0], group_impair[3], group_impair[6], rob.leg1)
    set_pos_to_leg(group_pair[0], group_pair[3], group_pair[6], rob.leg2)
    set_pos_to_leg(group_impair[1], group_impair[4], group_impair[7], rob.leg3)
    set_pos_to_leg(group_pair[1], group_pair[4], group_pair[7], rob.leg4)
    set_pos_to_leg(group_impair[2], group_impair[5], group_impair[8], rob.leg5)
    set_pos_to_leg(group_pair[2], group_pair[5], group_pair[8], rob.leg6)


#fonction convertissant les coordonnees du repere du robot vers celle des pattes
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


#fonction convertissant les coordonnees du repere du robot vers celle des pattes
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

#fonction permettant de savoir quelles pattes va etre controle
def init_leg(x, y, leg):
    set_pos_to_leg(x, y, -10, leg)
    time.sleep(0.5)
    set_pos_to_leg(x, y, -70, leg)

#fonction permettant de controler une patte individuellement
def move_leg(x, y, z, leg):
    set_pos_to_leg(x, y, z, leg)
    print 'X: ', x, '\n Y: ', y, '\n Z: ', z, '\n'
    time.sleep(0.05)


#fonction facilitant le calcules des coordonnees
#permet d'obtenir juste le deplacement en x y et z qui va avoir lieu entre des points dans le repere
def calcule_difference(x, y, z):
    global x_tmp, y_tmp, debut
    if debut == 1:
        x_tmp = x
        y_tmp = y
        debut = 0

    liste = [x-x_tmp, y_tmp-y]
    x_tmp = x
    y_tmp = y

    return liste