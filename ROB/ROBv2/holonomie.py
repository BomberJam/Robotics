import sys
import os
import threading
import termios, fcntl, sys, os
import time

from movement import *

choix = 0

rob = 0

x = 0

y = 0

z= 0

auto = 0

joy = { 'leftx': 0.0, 'lefty': 0.0, 'rightx': 0.0, 'righty': 0.0, 
        'trig0': False, 'trig1': False, 'trig2': False, 'trig3': False, 
        'buttonup': False, 'buttondown': False, 'buttonleft': False, 'buttonright': False,
        'triangle': False, 'circle': False, 'cross': False, 'square': False, 
        'select': False, 'start': False, 'ps': False}

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
		while 1:
			try:

				global pipe
				global action
				global spacing
				global verrou
				global x, y, z

				while 1:
					verrou.acquire()
					for character in pipe.read(1):
						action += ['%02X' % ord(character)]
						if len(action) == 8:

							num = int(action[5], 16)
							percent254 = str(((float(num)-128.0)/126.0)-100)[4:6]
							percent128 = str((float(num)/127.0))[2:4]

							if percent254 == '.0':
								percent254 = '100'
							if percent128 == '0':
								percent128 = '100'

							if action[6] == '01':
								if action[4] == '01':
									choix = action[7]

									if action[7] == '10':
										verrou.release()
										exit()

								else:
									if auto == 0:
										choix = 0

							elif action[7] == '00':
								num = int(action[5], 16)
								if num >= 128:
									joy['leftx'] = -int(percent254)
								elif num <= 127 \
								and num != 0:
									joy['leftx'] = int(percent128)
								else:
									joy['leftx'] = 0
								x = round (((float (joy['leftx']))/100)*2, 1)


							elif action[7] == '01':
								num = int(action[5], 16)
								if num >= 128:
									joy['lefty'] = -int(percent254)
								elif num <= 127 \
								and num != 0:
									joy['lefty'] = int(percent128)
								else:
									joy['lefty'] = 0
								y = round (-(((float (joy['lefty']))/100)*2), 1)


							elif action[7] == '02':
								num = int(action[5], 16)
								if num >= 128:
									joy['rightx'] = -int(percent254)
								elif num <= 127 \
								and num != 0:
									joy['rightx'] = int(percent128)
								else:
									joy['rightx'] = 0

							elif action[7] == '03':
								num = int(action[5], 16)
								if num >= 128:
									joy['righty'] = -int(percent254)
								elif num <= 127 \
								and num != 0:
									joy['righty'] = int(percent128)
								else:
									joy['righty'] = 0
								z = round (-(((float (joy['righty']))/100)*2), 1)

							action = []

					verrou.release()

			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)



def holonomie():
	global choix, verrou, rob
	global x, y, z
	global auto

	print '-------------------------------------'
	print '-------------STARTING UP-------------'
	print '-------------------------------------'

	step = 10
	count_pas = step * 1
	pas = 2

	pos_init = 1

	hauteur = 0

	liste = 0

	angle = 0

	speed = 10

	rotation = 0

	up_down = 0

	leg = 0

	option = 0# 0 = no option 1 = move leg 2 = jerk 3 = odomotry

	etat_walk_rotation = 0# 1 = walk 2 = r_left 3 = r_right

	jerk = 0

	auto = 0
	first = 0

	x_temp = 0
	y_temp = 0

	x_f_b = 0
	y_f_b = 180
	x_s = 160
	y_s = 95
	angle_rotation = 0.5

	odometry_straight_line = 0
	odometry_straight_line_par = 0
	odometry_rotation = 0
	odometry_rotation_par = 0
	nb_pas_rotation = 0
	start_odo = 0

	group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
	group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]

	while 1:
		if choix == '10':
			print '-------------------------------------'
			print '--------------SHUT DOWN--------------'
			print '-------------------------------------'
			break

		elif choix == '0A':

			if (step < 11):
				step = 10
			else:
				step = step - 1
			count_pas = step*1
			print 'Run: ', step

		elif choix == '0B':

			if (step > 19):
				step = 20
			else:
				step = step + 1
			count_pas = step*1
			print 'Run: ', step

		elif choix == '08':
			if speed < 2:
				speed = 1
			else:
				speed = speed - 1
			print 'Speed: ', speed
			set_motor_speed(rob, speed)

		elif choix == '09':

			speed = speed + 1
			print 'Speed: ', speed
			set_motor_speed(rob, speed)

		elif choix == '07' and option == 1:
			leg = leg - 1
			group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
			group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]
			initialize_to_zero(rob, group_impair, group_pair, 0)

			leg_chosen = []

			if leg == 1:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[0], leg_chosen[3], rob.leg1)
			elif leg == 2:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[0], leg_chosen[3], rob.leg2)
			elif leg == 3:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[1], leg_chosen[4], rob.leg3)
			elif leg == 4:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[1], leg_chosen[4], rob.leg4)
			elif leg == 5:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[2], leg_chosen[5], rob.leg5)
			elif leg == 6:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[2], leg_chosen[5], rob.leg6)
			elif leg < 1:
				leg = 7

		elif choix == '05' and option == 1:
			leg = leg + 1
			group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
			group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]
			initialize_to_zero(rob, group_impair, group_pair, 0)

			leg_chosen = []

			if leg == 1:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[0], leg_chosen[3], rob.leg1)
			elif leg == 2:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[0], leg_chosen[3], rob.leg2)
			elif leg == 3:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[1], leg_chosen[4], rob.leg3)
			elif leg == 4:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[1], leg_chosen[4], rob.leg4)
			elif leg == 5:
				leg_chosen = modification_repere_bot_impair(group_impair)
				init_leg(leg_chosen[2], leg_chosen[5], rob.leg5)
			elif leg == 6:
				leg_chosen = modification_repere_bot_pair(group_pair)
				init_leg(leg_chosen[2], leg_chosen[5], rob.leg6)
			elif leg > 6:
				leg = 0

		elif (x != 0 or y !=0 or z!= 0) and option == 1:
			if leg == 1:
				group_pair = modification_impair(group_impair, x*3, 0, 0, y*3, 0, 0, z*3, 0, 0)
				leg_chosen = modification_repere_bot_impair(group_impair)
				move_leg(leg_chosen[0], leg_chosen[3], leg_chosen[6], rob.leg1)
			elif leg == 2:
				group_pair = modification_pair(group_pair, x*3, 0, 0, y*3, 0, 0, z*3, 0, 0)
				leg_chosen = modification_repere_bot_pair(group_pair)
				move_leg(leg_chosen[0], leg_chosen[3], leg_chosen[6], rob.leg2)
			elif leg == 3:
				group_pair = modification_impair(group_impair, 0, x*3, 0, 0, y*3, 0, 0, z*3, 0)
				leg_chosen = modification_repere_bot_impair(group_impair)
				move_leg(leg_chosen[1], leg_chosen[4], leg_chosen[7], rob.leg3)
			elif leg == 4:
				group_pair = modification_pair(group_pair, 0, x*3, 0, 0, y*3, 0, 0, z*3, 0)
				leg_chosen = modification_repere_bot_pair(group_pair)
				move_leg(leg_chosen[1], leg_chosen[4], leg_chosen[7], rob.leg4)
			elif leg == 5:
				group_pair = modification_impair(group_impair, 0, 0, x*3, 0, 0, y*3, 0, 0, z*3)
				leg_chosen = modification_repere_bot_impair(group_impair)
				move_leg(leg_chosen[2], leg_chosen[5], leg_chosen[8], rob.leg5)
			elif leg == 6:
				group_pair = modification_pair(group_pair, 0, 0, x*3, 0, 0, y*3, 0, 0, z*3)
				leg_chosen = modification_repere_bot_pair(group_pair)
				move_leg(leg_chosen[2], leg_chosen[5], leg_chosen[8], rob.leg6)

		elif choix == '04' and option == 3:
			#buttonup
			odometry_straight_line_par += 1
			print 'Odometry straight line: ', odometry_straight_line_par
			start_odo = 1
		elif choix == '05' and option == 3:
			#buttonright
			odometry_rotation_par += 1
			print 'Odometry theta rotation: ', odometry_rotation_par
			start_odo = 1
		elif choix == '06' and option == 3:
			#buttondown
			if odometry_straight_line_par < 1:
				odometry_straight_line_par = 0
			else:
				odometry_straight_line_par -= 1
			print 'Odometry straight line: ', odometry_straight_line_par
			start_odo = 1
		elif choix == '07' and option == 3:
			#buttonleft
			if odometry_rotation_par < 1:
				odometry_rotation_par = 0
			else:
				odometry_rotation_par -= 1
			print 'Odometry theta rotation: ', odometry_rotation_par
			start_odo = 1

		elif choix == '04' and up_down == 0:
			#buttonup
			group_pair = modification_pair(group_pair, 0, 0, 0, -pas*3, pas*3, -pas*3, 0, 0, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, -pas*3, pas*3, pas*3, 0, 0, 0)

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		elif choix == '05' and rotation == 0 and up_down == 0:
			#buttonright
			group_pair = modification_pair(group_pair, -pas*3, -pas*3, pas*3, 0, 0, 0, 0, 0, 0)
			group_impair = modification_impair(group_impair, -pas*3, -pas*3, pas*3, 0, 0, 0, 0, 0, 0)

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		elif choix == '06' and up_down == 0:
			#buttondown
			group_pair = modification_pair(group_pair, 0, 0, 0, pas*3, -pas*3, pas*3, 0, 0, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, pas*3, -pas*3, -pas*3, 0, 0, 0)

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		elif choix == '07' and rotation == 0 and up_down == 0:
			#buttonleft
			group_pair = modification_pair(group_pair, pas*3, pas*3, -pas*3, 0, 0, 0, 0, 0, 0)
			group_impair = modification_impair(group_impair, pas*3, pas*3, -pas*3, 0, 0, 0, 0, 0, 0)

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif choix == '07' and up_down == 0:
			if etat_walk_rotation != 2:
				count_pas = step*1
				etat_walk_rotation = 2
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				x_f_b = 0
				y_f_b = 180
				x_s = 160
				y_s = 95
				if hauteur > -1:
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

			if odometry_rotation_par > 1 and option == 3:
				odometry_rotation_par = odometry_rotation_par - abs(angle_rotation)
				choix = '05'
			elif option == 3:
				auto = 0

		elif choix == '05' and up_down == 0:
			if etat_walk_rotation != 3:
				count_pas = step*1
				etat_walk_rotation = 3
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				x_f_b = 0
				y_f_b = 180
				x_s = 160
				y_s = 95
				if hauteur > -1:
					after_init(group_impair,pas)
				pos_init = 0
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

			if odometry_rotation_par > 1 and option == 3:
				odometry_rotation_par = odometry_rotation_par - abs(angle_rotation)
				choix = '05'
			elif option == 3:
				auto = 0

		elif choix == '04':
			if hauteur < -42:
				hauteur = -48
			else:
				group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -6, -6, -6)
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -6, -6, -6)
				hauteur = hauteur - 6
			print hauteur

			etat_walk_rotation = 0

		 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif choix == '06':
			if hauteur > 18:
				hauteur = 24
			else:
				group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 6, 6, 6)
				group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 6, 6, 6)
				hauteur = hauteur + 6
			print hauteur

			etat_walk_rotation = 0

		 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif choix == '05':
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

		elif choix == '07':
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

		elif choix == '0C':
			if up_down == 1:
				up_down = 0
				print '-----------------DOWN----------------'
			else:
				up_down = 1
				print '------------------UP-----------------'
				print '------------STOP ROTATION------------'
				rotation = 0
		elif choix == '0D':
			if rotation == 1:
				rotation = 0
				print '------------STOP ROTATION------------'
			else:
				rotation = 1
				print '---------------ROTATION--------------'
		elif choix == '0E':
			if auto == 1:
				auto = 0
				print '----------MANUAL MONITORING----------'
			else:
				auto = 1
				choix = 0
				first = 1
				print '--------AUTOMATIQUE MONITORING-------'
		elif choix == '0F':
			joy['square'] = True
		elif choix == '00':
			initialize_to_zero(rob, group_impair, group_pair, hauteur)
			option = option + 1

			if option == 1:
				print '-----------MOVING LEG MODE-----------'
			elif option == 2:
				print '--------------JERK MODE--------------'
			elif option == 3:
				print '------------AODOMETRY MODE-----------'
			elif option > 3:
				print '----------------NO MODE--------------'
				option = 0
		elif choix == '03':
			count_pas = step*1
			pos_init = 1
			hauteur = 0
			liste = 0
			angle = 0
			speed = 10
			step = 10
			auto = 0
			x_temp = 0
			y_temp = 0
			initialize_to_zero(rob, group_impair, group_pair, 0)
			print '----------------RESET----------------'
			print '----------MANUAL MONITORING----------'

		elif (x != 0 or y !=0) and option == 0 and auto == 0:
			if etat_walk_rotation != 1:
				count_pas = step*1
				etat_walk_rotation = 1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				if hauteur > -1:
					after_init(group_impair,pas)
				pos_init = 0


			if (x > 0 and x_temp < 0) or (x < 0 and x_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1

			if (y > 0 and y_temp < 0) or (y < 0 and y_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1

			x_pas = x
			y_pas = y
			x_temp = x_pas
			y_temp = y_pas

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)	
				group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, rapport_step, rapport_step, rapport_step)
				group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, -rapport_step, -rapport_step, -rapport_step)
				group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif (option == 0 or option == 3) and auto == 1:
			if etat_walk_rotation != 1:
				count_pas = step*1
				etat_walk_rotation = 1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				if hauteur > -1:
					after_init(group_impair,pas)
				pos_init = 0


			if (x > 0 and x_temp < 0) or (x < 0 and x_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1

			if (y > 0 and y_temp < 0) or (y < 0 and y_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1

			if x != 0:
				x_pas = x
				x_temp = x_pas
			else:
				x_pas = x_temp

			if y != 0:
				y_pas = y
				y_temp = y_pas
			else:
				y_pas = y_temp

			rapport_step = 60/step

			if count_pas < 1*step:
				group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)
				group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, rapport_step, rapport_step, rapport_step)
			elif count_pas < 2*step:
				group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)	
				group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, -rapport_step, -rapport_step, -rapport_step)
			elif count_pas < 3*step:
				group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, rapport_step, rapport_step, rapport_step)
				group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)
			elif count_pas < 4*step:
				group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, -rapport_step, -rapport_step, -rapport_step)
				group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)

			count_pas += 1	

			if count_pas == 4*step:
				count_pas = 0

			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

			if odometry_straight_line_par > 0 and option == 3:
				if x_pas > y_pas:
					odometry_straight_line_par -= abs(x_pas)
				else:
					odometry_straight_line_par -= abs(y_pas)
			elif option == 3:
				auto = 0


		elif (x != 0 or y !=0) and option == 2 and auto == 1:
			if etat_walk_rotation != 1:
				count_pas = step*1
				etat_walk_rotation = 1
				pos_init = 1
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				time.sleep(0.1)

			if pos_init == 1:
				if hauteur > -1:
					after_init(group_impair,pas)
				pos_init = 0


			if (x > 0 and x_temp < 0) or (x < 0 and x_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1

			if (y > 0 and y_temp < 0) or (y < 0 and y_temp > 0):
				initialize_to_zero(rob, group_impair, group_pair, hauteur)
				if hauteur > -1:
					after_init(group_impair,pas)
				count_pas = step*1


			x_pas = x
			y_pas = y
			x_temp = x_pas
			y_temp = y_pas

			rapport_step = 60/step


			xt = 1
			while xt < 200:
				n = xt/(200.0-1.0)
				m = (200.0-1.0-xt)/(200.0-1.0)
				speed = m*xt + n*200.0

				set_motor_speed(rob, speed)
				print x_temp, ', ', y_temp

				if count_pas < 1*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, rapport_step, rapport_step, rapport_step)
				elif count_pas < 2*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)	
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, -rapport_step, -rapport_step, -rapport_step)
				elif count_pas < 3*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, rapport_step, rapport_step, rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)
				elif count_pas < 4*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, -rapport_step, -rapport_step, -rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)

				count_pas += 1	

				if count_pas == 4*step:
					count_pas = 0

				move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))


				xt = xt + 1

				time.sleep(0.05)

			while choix != '00':	

				if x != 0:
					x_pas = x
					x_temp = x_pas
				else:
					x_pas = x_temp

				if y != 0:
					y_pas = y
					y_temp = y_pas
				else:
					y_pas = y_temp

				if count_pas < 1*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, rapport_step, rapport_step, rapport_step)
				elif count_pas < 2*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)	
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, -rapport_step, -rapport_step, -rapport_step)
				elif count_pas < 3*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, rapport_step, rapport_step, rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)
				elif count_pas < 4*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, -rapport_step, -rapport_step, -rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)

				count_pas += 1	

				if count_pas == 4*step:
					count_pas = 0

				move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

				time.sleep(0.05)

			xt = 200
			while xt > 1:
				n = xt/(200.0-1.0)
				m = (200.0-1.0-xt)/(200.0-1.0)
				speed = m*xt + n*200.0

				set_motor_speed(rob, speed)

				if count_pas < 1*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, rapport_step, rapport_step, rapport_step)
				elif count_pas < 2*step:
					group_pair = modification_pair(group_pair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, -y_pas, 0, 0, 0)	
					group_impair = modification_impair(group_impair, x_pas, x_pas, -x_pas, y_pas, -y_pas, -y_pas, -rapport_step, -rapport_step, -rapport_step)
				elif count_pas < 3*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, rapport_step, rapport_step, rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)
				elif count_pas < 4*step:
					group_pair = modification_pair(group_pair, x_pas, x_pas, -x_pas, y_pas, -y_pas, y_pas, -rapport_step, -rapport_step, -rapport_step)
					group_impair = modification_impair(group_impair, -x_pas, -x_pas, x_pas, -y_pas, y_pas, y_pas, 0, 0, 0)

				count_pas += 1	

				if count_pas == 4*step:
					count_pas = 0

				move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))


				xt = xt - 1

				time.sleep(0.05)				

		time.sleep(0.02)


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


def calcule(xa, ya ,xb , yb, xc, yc):
	xab = xb-xa
	yab = yb-ya
	xac = xc-xa
	yac = yc-ya

	AB = sqrt(xab*xab + yab*yab)
	AC = sqrt(xac*xac + yac*yac)

	angle = acos((xab*yab + xac*yac)/AB*AC)

	return angle


def ROB_control(path, bot):
	global rob
	global pipe
	global action
	global spacing
	rob = bot
	verrou = threading.Lock()
	t1=threading.Thread(target=holonomie)
	t2=threading.Thread(target=keyevent)
	action = []
	spacing = 0
	try:
		pipe = open(path, 'r')
	except:
		return False

	t1.start()
	t2.start()
	t1.join()
	t2.join()