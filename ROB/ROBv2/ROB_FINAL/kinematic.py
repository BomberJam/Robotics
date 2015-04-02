# -*- coding:Utf-8 -*-
import itertools
import time
import numpy
#import pypot.dynamixel
import math

constL1 = 51
constL2 = 63.7
constL3 = 93
# Angle to match the theory with reality for theta 2 (measures of the triangle are 22.5, 60.7, 63.7). => Angle = -20.69
theta2Correction = -20.69
# Same goes for theta 3 : +90 - 20.69 - a. Where a = asin(8.2/93) = 5.06
theta3Correction = 90 + theta2Correction - 5.06

def kinematic(theta1, theta2, theta3, l1=constL1, l2=constL2,l3=constL3):
    theta1 = theta1 * math.pi / 180.0
    theta2 = (theta2 - theta2Correction) * math.pi / 180.0
    theta3 = -(theta3 - theta3Correction) * math.pi / 180.0
    planContribution = l1 + l2*math.cos(theta2) + l3*math.cos(theta2 + theta3)

    x = math.cos(theta1) * planContribution
    y = math.sin(theta1) * planContribution
    z = -(l2 * math.sin(theta2) + l3 * math.sin(theta2 + theta3))
    return [x, y, z]
    
def alkachi(a, b, c):
    try:
        alka = math.degrees(math.acos((a*a+b*b-c*c)/(2*a*b)))
        #print "value changed", repr(choix)
    except ValueError:
        alka = False
    return alka

def inverse_kinematic(x,y,z):
    #longueur de la patte
    l1 = 51 #de la base au deuxieme servomoteur
    l2 = 63.7 #du deuxieme servomoteur au troisieme servomoteur
    l3 = 93 # du troisieme servomoteur a l'extremité de la patte
    
    #degré de réajustement 
    alpha = 20.69
    beta = 5.06

    theta1 = math.atan2(y,x)
    theta1 = math.degrees(theta1) #angle du premier servomoteur sur l'axe x y

    d13 = math.sqrt(x*x+y*y)-l1 #distance entre le deuxieme servomoteur et l'extremité de la patte sur la projection x y
    d = math.sqrt(d13*d13+z*z) #distance entre le deuxieme servomoteur et l'extremité de la patte
    a = math.degrees(math.atan2(z,d13)) #angle entre d et d13
    b = alkachi(l2, d, l3) #angle entre l2 et d
    
    if b == False:
        return False

    theta2 = -(a+b+alpha) #angle du second servomoteur

    theta3 = 180 - alkachi(l2, l3, d)
    theta3 = - (theta3 -90 + alpha + beta) #angle du troisième servomoteur

    return [theta1, theta2, theta3]