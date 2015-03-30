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



def change_front_back(x1, y1, angle):
	x = x1*cos(radians(angle)) - y1*sin(radians(angle))
	y = x1*sin(radians(angle)) + y1*cos(radians(angle))
	if y > 0:
		y = y - 180
	elif y < 0:
		y = 180 - y

	return [x, y]

def change_side(x1, y1, angle):
	x = x1*cos(radians(angle)) - y1*sin(radians(angle))
	y = x1*sin(radians(angle)) + y1*cos(radians(angle))
	if x > 0:
		x = x -160
	elif x < 0:
		x = 160 - x

	if y > 0:
		y = y - 95
	elif y < 0:
		y = 95 - y

	return [x, y]

def after_init(leg_impair, pas):
	pas = 10 * 6
	parcour = 0

	while parcour != pas:

		leg_impair[6] += 1
		leg_impair[7] += 1
		leg_impair[8] += 1    

		set_pos_to_leg(leg_impair[3]-60, -leg_impair[0], leg_impair[6], rob.leg1)
		set_pos_to_leg(leg_impair[1]-40, -leg_impair[4]+25, leg_impair[7], rob.leg3)
		set_pos_to_leg(leg_impair[2]-40, leg_impair[5]-25, leg_impair[8], rob.leg5)

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
	global choix, rob,verrou
	odometry_straight_line = 0
	odometry_straight_line_par = 0
	odometry_rotation = 0
	odometry_rotation_par = 0
	nb_pas_rotation = 0
	start_odo = 0

	liste = 0
	x_f_b = 0
	y_f_b = 180
	x_s = 160
	y_s = 95
	group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
	group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]

	speed = 10

	hauteur = 0
	angle = 0
	angle_rotation = 0.5
	manual = 1
	pas = 2
	step = 10
	count_pas = step*1
	pos_init = 1
	direction = 0  

	while True:
		verrou.acquire()
		if choix == 'n':
			break
		elif choix == 'z':
			if direction != 'z':
				direction = 'z'
				count_pas = step*1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, -pas, pas, -pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, 0, 0, pas, -pas, -pas, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, -pas , pas , -pas , 0, 0, 0)	
				group_impair = modification_impair(group_impair, 0, 0, 0, pas , -pas , -pas , -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, pas , -pas , pas , rapport_step, rapport_step, rapport_step)
				group_impair = modification_impair(group_impair, 0, 0, 0, -pas , pas , pas , 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, pas , -pas , pas , -rapport_step, -rapport_step, -rapport_step)
				group_impair = modification_impair(group_impair, 0, 0, 0, -pas , pas , pas , 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			odometry_straight_line += pas
			if odometry_straight_line_par > 1:
				odometry_straight_line_par = odometry_straight_line_par - pas
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0

		elif choix == 's':
			if direction != 's':
				direction = 's'
				count_pas = step*1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step :
				group_pair = modification_pair(group_pair, 0, 0, 0, pas, -pas, pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, 0, 0, 0, -pas, pas, pas, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, pas, -pas, pas, 0, 0, 0)	
				group_impair = modification_impair(group_impair, 0, 0, 0, -pas, pas, pas, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, -pas, pas, -pas , rapport_step, rapport_step, rapport_step)
				group_impair = modification_impair(group_impair, 0, 0, 0, pas, -pas, -pas, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, 0, 0, 0, -pas, pas, -pas, -rapport_step, -rapport_step, -rapport_step)
				group_impair = modification_impair(group_impair, 0, 0, 0, pas, -pas, -pas, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0


			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			odometry_straight_line += pas
			if odometry_straight_line_par > 1:
				odometry_straight_line_par = odometry_straight_line_par - pas
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0

		elif choix == 'd':
			if direction != 'd':
				direction = 'd'
				count_pas = step*1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, -pas, -pas, pas, 0, 0, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, pas, pas, -pas, 0, 0, 0, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, -pas, -pas, pas, 0, 0, 0, 0, 0, 0)	
				group_impair = modification_impair(group_impair, pas, pas, -pas, 0, 0, 0, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, pas, pas, -pas, 0, 0,  0, rapport_step, rapport_step, rapport_step)					
				group_impair = modification_impair(group_impair, -pas, -pas, pas, 0, 0, 0, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, pas, pas, -pas, 0, 0, 0, -rapport_step, -rapport_step, -rapport_step)					
				group_impair = modification_impair(group_impair, -pas, -pas, pas, 0, 0, 0, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0


			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			odometry_straight_line += pas
			if odometry_straight_line_par > 1:
				odometry_straight_line_par = odometry_straight_line_par - pas
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0

		elif choix == 'q':
			if direction != 'q':
				direction = 'q'
				count_pas = step*1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				after_init(group_impair,pas)
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step :
				group_pair = modification_pair(group_pair, pas, pas, -pas, 0, 0, 0, 0, 0, 0)
				group_impair = modification_impair(group_impair, -pas, -pas, pas, 0, 0, 0, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, pas, pas, -pas, 0, 0, 0, 0, 0, 0)	
				group_impair = modification_impair(group_impair, -pas, -pas, pas, 0, 0, 0, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, -pas, -pas, pas, 0, 0,  0, rapport_step, rapport_step, rapport_step)					
				group_impair = modification_impair(group_impair, pas, pas, -pas, 0, 0, 0, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, -pas, -pas, pas, 0, 0, 0, -rapport_step, -rapport_step, -rapport_step)					
				group_impair = modification_impair(group_impair, pas, pas, -pas, 0, 0, 0, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0


			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			odometry_straight_line += pas
			if odometry_straight_line_par > 1:
				odometry_straight_line_par = odometry_straight_line_par - pas
				print odometry_straight_line_par
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0

		elif choix == 'a':
			if direction != 'a':
				direction = 'a'
				count_pas = step*1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, 0)
				time.sleep(0.1)

			if pos_init == 1:
				x_f_b = 0
				y_f_b = 180
				x_s = 160
				y_s = 95
				after_init(group_impair,pas)
				liste = change_front_back(x_f_b, y_f_b, angle_rotation)
				x_f_b = liste[0]
				y_f_b = liste[1]
				liste = change_side(x_s, y_s, angle_rotation)
				x_s = liste[0]
				y_s = liste[1]
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, -x_s, x_f_b, x_s, -y_s, y_f_b, y_s, 0, 0, 0)
				group_impair = modification_impair(group_impair, x_f_b, -x_s, x_s, y_f_b, -y_s, y_s, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, -x_s, x_f_b, x_s, -y_s, y_f_b, y_s, 0, 0, 0)
				group_impair = modification_impair(group_impair, x_f_b, -x_s, x_s, y_f_b, -y_s, y_s, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, x_s, -x_f_b, -x_s, y_s, -y_f_b, -y_s, rapport_step, rapport_step, rapport_step)		
				group_impair = modification_impair(group_impair, -x_f_b, x_s, -x_s, -y_f_b, y_s, -y_s, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, x_s, -x_f_b, -x_s, y_s, -y_f_b, -y_s, -rapport_step, -rapport_step, -rapport_step)				
				group_impair = modification_impair(group_impair, -x_f_b, x_s, -x_s, -y_f_b, y_s, -y_s, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			nb_pas_rotation = nb_pas_rotation - 1
			odometry_rotation = nb_pas_rotation * angle_rotation

			if odometry_rotation_par > 1:
				odometry_rotation_par = odometry_rotation_par - angle_rotation
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0
		elif choix =='e':
			if direction != 'e':
				direction = 'e'
				count_pas = 10
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, 0)
				time.sleep(0.1)
	
			if pos_init == 1:
				x_f_b = 0
				y_f_b = 180
				x_s = 160
				y_s = 95
				after_init(group_impair,pas)
				liste = change_front_back(x_f_b, y_f_b, angle_rotation)
				x_f_b = liste[0]
				y_f_b = liste[1]
				liste = change_side(x_s, y_s, angle_rotation)
				x_s = liste[0]
				y_s = liste[1]
				pos_init = 0

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, x_s, -x_f_b, -x_s, y_s, -y_f_b, -y_s, 0, 0, 0)
				group_impair = modification_impair(group_impair, -x_f_b, x_s, -x_s, -y_f_b, y_s, -y_s, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, x_s, -x_f_b, -x_s, y_s, -y_f_b, -y_s, 0, 0, 0)
				group_impair = modification_impair(group_impair, -x_f_b, x_s, -x_s, -y_f_b, y_s, -y_s, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, -x_s, x_f_b, x_s, -y_s, y_f_b, y_s, rapport_step, rapport_step, rapport_step)		
				group_impair = modification_impair(group_impair, x_f_b, -x_s, x_s, y_f_b, -y_s, y_s, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, -x_s, x_f_b, x_s, -y_s, y_f_b, y_s, -rapport_step, -rapport_step, -rapport_step)				
				group_impair = modification_impair(group_impair, x_f_b, -x_s, x_s, y_f_b, -y_s, y_s, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			nb_pas_rotation = nb_pas_rotation + 1
			odometry_rotation = nb_pas_rotation * angle_rotation

			if odometry_rotation_par > 1:
				odometry_rotation_par = odometry_rotation_par - angle_rotation
			elif start_odo == 1:
				choix = 0
				manual = 1
				start_odo = 0

		elif choix == 'i':
			count_pas = step*1
			pos_init = 1
			initialize_to_zero(rob, group_impair, group_pair, 0)
			hauteur = 0
			liste = 0
			angle = 0
		elif choix == 'w':
			angle = angle + 0.5
			liste = change_front_back(x_f_b, y_f_b, angle)
			x_f_b = liste[0]
			y_f_b = liste[1]
			liste = change_side(x_s, y_s, angle)
			x_s = liste[0]
			y_s = liste[1]
		elif choix == 'x':
			angle = angle - 0.5
			liste = change_front_back(x_f_b, y_f_b, angle)
			x_f_b = liste[0]
			y_f_b = liste[1]
			liste = change_side(x_s, y_s, angle)
			x_s = liste[0]
			y_s = liste[1]
		elif choix == 'g':
			initialize_to_zero(rob, group_impair, group_pair, 0)
			while True:
				if choix == 'z':
					group_pair = modification_pair(group_pair, 0, 0, 0, -pas*3, pas*3, -pas*3, 0, 0, 0)
					group_impair = modification_impair(group_impair, 0, 0, 0, -pas*3, pas*3, pas*3, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 's':
					group_pair = modification_pair(group_pair, 0, 0, 0, pas*3, -pas*3, pas*3, 0, 0, 0)
					group_impair = modification_impair(group_impair, 0, 0, 0, pas*3, -pas*3, -pas*3, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 'q':
					group_pair = modification_pair(group_pair, pas*3, pas*3, -pas*3, 0, 0, 0, 0, 0, 0)
					group_impair = modification_impair(group_impair, pas*3, pas*3, -pas*3, 0, 0, 0, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 'd':
					group_pair = modification_pair(group_pair, -pas*3, -pas*3, pas*3, 0, 0, 0, 0, 0, 0)
					group_impair = modification_impair(group_impair, -pas*3, -pas*3, pas*3, 0, 0, 0, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 'a':
					x_f_b = 0
					y_f_b = 180
					x_s = 160
					y_s = 95
					liste = change_front_back(x_f_b, y_f_b, angle_rotation)
					x_f_b = liste[0]
					y_f_b = liste[1]
					liste = change_side(x_s, y_s, angle_rotation)
					x_s = liste[0]
					y_s = liste[1]
					group_pair = modification_pair(group_pair, -x_s*2, x_f_b*2, x_s*2, -y_s*2, y_f_b*2, y_s*2, 0, 0, 0)
					group_impair = modification_impair(group_impair, -x_f_b*2, x_s*2, -x_s*2, -y_f_b*2, y_s*2, -y_s*2, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 'e':
					x_f_b = 0
					y_f_b = 180
					x_s = 160
					y_s = 95
					liste = change_front_back(x_f_b, y_f_b, angle_rotation)
					x_f_b = liste[0]
					y_f_b = liste[1]
					liste = change_side(x_s, y_s, angle_rotation)
					x_s = liste[0]
					y_s = liste[1]
					group_pair = modification_pair(group_pair, x_s*2, -x_f_b*2, -x_s*2, y_s*2, -y_f_b*2, -y_s*2, 0, 0, 0)
					group_impair = modification_impair(group_impair, x_f_b*2, -x_s*2, x_s*2, y_f_b*2, -y_s*2, y_s*2, 0, 0, 0)

					move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
					choix = 0
				elif choix == 'r':
					group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -6, -6, -6)
					group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -6, -6, -6)
					hauteur = hauteur - 6

				 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
				 	choix = 0
				elif choix == 'f':
					group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 6, 6, 6)
					group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 6, 6, 6)
					hauteur = hauteur + 6

				 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
				 	choix = 0
				elif choix == 'n':
					break

				time.sleep(0.02)
		elif choix == 'o':
			print odometry_rotation_par, ', ', odometry_straight_line_par, '\n'
			odometry_straight_line_par += 1
			odometry_rotation_par += 1
			start_odo = 1	

		elif choix == '+':
			speed = speed + 1
			print speed
			set_motor_speed(rob, speed)

		elif choix == '-':
			speed = speed - 1
			if(speed < 1):
				speed = 1
			print speed
			set_motor_speed(rob, speed)

		elif choix == 'p':
			if (step > 21):
				step = 22
			else:
				step = step + 1
			count_pas = step*1
			print step
		elif choix == 'm':

			if (step < 11):
				step = 10
			else:
				step = step - 1
			count_pas = step*1
			print step
		elif choix == 't':
			if manual == 1:
				manual = 0
			else:
				manual = 1
			choix = 0

		if manual == 1:
			choix = 0

		verrou.release()
		#print 'odometry_straight_line = ', odometry_straight_line, '; odometry_rotation = ', odometry_rotation, '\n' 
		time.sleep(0.005)


def ROB_control(bot):
	global rob
	rob = bot
	verrou = threading.Lock()
	t1=threading.Thread(target=holonomie)
	t2=threading.Thread(target=keyevent)
	t1.start()
	t2.start()
	t1.join()
	t2.join()