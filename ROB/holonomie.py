import pypot.dynamixel
import time
import threading
import sys
import termios, fcntl, sys, os
from kinematic import *
from math import *
from movement import *
from pypot.robot import from_json
from init_by_move import *
from walking import *

choix = 0

rob = 0

verrou = threading.Lock()

fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)



def keyevent():
	global choix,verrou
	try:
		while choix != 'n':
			try:
				choix = sys.stdin.read(1)
				#print "value changed", repr(choix)
			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



def move(group_pair, group_impair):
    set_pos_to_leg(group_impair[0], group_impair[3], group_impair[6], rob.leg1)
    set_pos_to_leg(group_pair[0], group_pair[3], group_pair[6], rob.leg2)
    set_pos_to_leg(group_impair[1], group_impair[4], group_impair[7], rob.leg3)
    set_pos_to_leg(group_pair[1], group_pair[4], group_pair[7], rob.leg4)
    set_pos_to_leg(group_impair[2], group_impair[5], group_impair[8], rob.leg5)
    set_pos_to_leg(group_pair[2], group_pair[5], group_pair[8], rob.leg6)


def change_front_back(x1, y1, angle):
	x = x1*cos(radians(angle)) - y1*sin(radians(angle))
	y = x1*sin(radians(angle)) + y1*cos(radians(angle))

	return [x, y]

def change_side(x1, y1, angle):
	x = x1*cos(radians(angle)) - y1*sin(radians(angle))
	y = x1*sin(radians(angle)) + y1*cos(radians(angle))

	return [x, y]

def after_init(leg_impair, pas):
	# a modifier
	pas = 10 * 6
	parcour = 0
	while parcour != pas:
		leg_impair[6] += 1
		leg_impair[7] += 1
		leg_impair[8] += 1

		set_pos_to_leg(120, 0, leg_impair[6], rob.leg1)
		set_pos_to_leg(120, -70, leg_impair[7], rob.leg3)
		set_pos_to_leg(120, 70, leg_impair[8], rob.leg5)

		parcour += 1
		time.sleep(0.005)

def modification_impair(leg_impair, x1, x3, x5, y1, y3, y5, z1, z3, z5):
	leg_impair[0] += x1
	leg_impair[1] += x3
	leg_impair[2] += x5
	leg_impair[3] += y1
	leg_impair[4] += y3
	leg_impair[5] += y5
	leg_impair[6] += z1
	leg_impair[7] += z3
	leg_impair[8] += z5

	return leg_impair


def modification_pair(leg_pair, x2, x4, x6, y2, y4, y6, z2, z4, z6):
	leg_pair[0] += x2
	leg_pair[1] += x4
	leg_pair[2] += x6
	leg_pair[3] += y2
	leg_pair[4] += y4
	leg_pair[5] += y6
	leg_pair[6] += z2
	leg_pair[7] += z4
	leg_pair[8] += z6

	return leg_pair


def holonomie():
	global choix, rob
	liste = 0
	x_f_b = 120
	y_f_b = 0
	x_s = 120
	y_s = 70
	group_pair = [120, 120, 120, 70, 0, -70, -70, -70, -70]
	group_impair = [120, 120, 120, 0, -70, 70, -70, -70, -70]
	angle = 0.5#11.25
	manual = 1
	pas = 2
	count_pas = 10
	pos_init = 1
	direction = 0

	while True:
		if choix == 'n':
			break
		elif choix == 'z':
			if direction != 'z':
				direction = 'z'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			if count_pas < 10 :
				group_pair = modification_pair(group_pair, 0, pas, 0 , -pas, 0, pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, pas, 0, 0, 0, pas, -pas, 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, 0, pas, 0 , -pas, 0, pas, 0, 0, 0)	
				group_impair = modification_impair(group_impair, pas, 0, 0, 0, pas, -pas, -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, 0, -pas, 0 , pas, 0, -pas, 6, 6, 6)					
				group_impair = modification_impair(group_impair, -pas, 0, 0, 0, -pas, pas, 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, 0, -pas, 0 , pas, 0, -pas, -6, -6, -6)					
				group_impair = modification_impair(group_impair, -pas, 0, 0, 0, -pas, pas, 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)
		elif choix == 's':
			if direction != 's':
				direction = 's'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			if count_pas < 10 :
				group_pair = modification_pair(group_pair, 0, -pas, 0 , pas, 0, -pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, -pas, 0, 0, 0, -pas, pas, 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, 0, -pas, 0 , pas, 0, -pas, 0, 0, 0)	
				group_impair = modification_impair(group_impair, -pas, 0, 0, 0, -pas, pas, -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, 0, pas, 0 , -pas, 0, pas, 6, 6, 6)					
				group_impair = modification_impair(group_impair, pas, 0, 0, 0, pas, -pas, 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, 0, pas, 0 , -pas, 0, pas, -6, -6, -6)					
				group_impair = modification_impair(group_impair, pas, 0, 0, 0, pas, -pas, 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)


		elif choix == 'd':
			if direction != 'd':
				direction = 'd'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			if count_pas < 10 :
				group_pair = modification_pair(group_pair, -pas, 0, pas , 0, -pas, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, pas, -pas, -pas, 0, 0, 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, -pas, 0, pas , 0, -pas, 0, 0, 0, 0)	
				group_impair = modification_impair(group_impair, 0, pas, -pas, -pas, 0, 0, -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, pas, 0, -pas , 0, pas, 0, 6, 6, 6)					
				group_impair = modification_impair(group_impair, 0, -pas, pas, pas, 0, 0, 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, pas, 0, -pas , 0, pas, 0, -6, -6, -6)					
				group_impair = modification_impair(group_impair, 0, -pas, pas, pas, 0, 0, 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)

		elif choix == 'q':
			if direction != 'q':
				direction = 'q'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			if count_pas < 10 :
				group_pair = modification_pair(group_pair, pas, 0, -pas , 0, pas, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, -pas, pas, pas, 0, 0, 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, pas, 0, -pas , 0, pas, 0, 0, 0, 0)	
				group_impair = modification_impair(group_impair, 0, -pas, pas, pas, 0, 0, -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, -pas, 0, pas , 0, -pas, 0, 6, 6, 6)					
				group_impair = modification_impair(group_impair, 0, pas, -pas, -pas, 0, 0, 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, -pas, 0, pas , 0, -pas, 0, -6, -6, -6)					
				group_impair = modification_impair(group_impair, 0, pas, -pas, -pas, 0, 0, 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)
		elif choix == 'a':
			if direction != 'a':
				direction = 'a'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			print group_pair, '\n'

			if count_pas < 10:
				group_pair = modification_pair(group_pair, x_s-120, 120-x_f_b, 120-x_s, (y_s-70), y_f_b, -(70-y_s), 0, 0, 0)
				group_impair = modification_impair(group_impair, x_f_b-120, x_s-120, 120-x_s, -y_f_b, (70-y_s), -(y_s-70), 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, x_s-120, 120-x_f_b, 120-x_s, (y_s-70), y_f_b, -(70-y_s), 0, 0, 0)
				group_impair = modification_impair(group_impair, x_f_b-120, x_s-120, 120-x_s, -y_f_b, (70-y_s), -(y_s-70), -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, 120-x_s, x_f_b-120, x_s-120, -(y_s-70), -y_f_b, (70-y_s), 6, 6, 6)		
				group_impair = modification_impair(group_impair, 120-x_f_b, 120-x_s, x_s-120, y_f_b, (y_s-70), (y_s-70), 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, 120-x_s, x_f_b-120, x_s-120, -(y_s-70), -y_f_b, (70-y_s), -6, -6, -6)				
				group_impair = modification_impair(group_impair, 120-x_f_b, 120-x_s, x_s-120, y_f_b, (y_s-70), (y_s-70), 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)
		elif choix =='e':
			if direction != 'q':
				direction = 'q'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			if count_pas < 10 :
				group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 6, 6, 6)
			elif count_pas < 20:
				group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -6, -6, -6)
			elif count_pas < 30:
				group_pair = modification_pair(group_pair, 0, 0, 0 , 0, 0, 0, 6, 6, 6)		
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 0, 0, 0)
			elif count_pas < 40:
				group_pair = modification_pair(group_pair, 0, 0, 0 , 0, 0, 0, -6, -6, -6)				
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 0, 0, 0)

			count_pas += 1	

			if count_pas == 40:
				count_pas = 0

			move(group_pair, group_impair)
		elif choix == 'i':
			count_pas = 10
			pos_init = 1
			initialize_to_zero(rob, group_impair, group_pair)
		elif choix == 'w':
			angle += 1
			liste = change_front_back(x_f_b, y_f_b, angle)
			x_f_b = liste[0]
			y_f_b = liste[1]
			print liste
			liste = change_side(x_s, y_s, angle)
			x_s = liste[0]
			y_s = liste[1]
			print liste
		elif choix == 'x':
			angle -= 1
			liste = change_front_back(x_f_b, y_f_b, angle)
			x_f_b = liste[0]
			y_f_b = liste[1]
			print liste
			liste = change_side(x_s, y_s, angle)
			x_s = liste[0]
			y_s = liste[1]
			print liste
		elif choix == 'm':
			if manual == 1:
				manual = 0
			else:
				manual = 1
			choix = 0

		if manual == 1:
			choix = 0

		time.sleep(0.002)

def ROB_control(bot):
	global rob
	rob = bot
	t1=threading.Thread(target=holonomie)
	t2=threading.Thread(target=keyevent)
	t1.start()
	t2.start()
	t1.join()
	t2.join()