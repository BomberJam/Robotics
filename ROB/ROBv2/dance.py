import time
import pygame
from movement import *
from motor_config import *


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
def dance(rob):
	group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
	group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]
	initialize_to_zero(rob, group_impair, group_pair, 0)

	pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer to avoid sound lag
	pygame.init()
	pygame.mixer.music.load("music.wav")
	pygame.mixer.music.play()
	
	time.sleep(2)
	p1 = 50
	p2 = 50
	p3 = 50
	p4 = 50
	p5 = 50
	p6 = 50

	x = 0
	while x < 10:
		group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -p2, -p4, -p6)
	 	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -p1, -p3, -p5)
	 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
	 	time.sleep(0.6)

	 	if x == 3:
	 		p6 = +50
	 	elif x == 4:
	 		p3 = +50
	 	elif x == 5:
	 		p2 = +50
	 	elif x == 6:
	 		p5 = +50
		
	 	group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, +p2, +p4, +p6)
	 	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, +p1, +p3, +p5)
	 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
	 	time.sleep(0.6)

	 	if x == 3:
	 		p6 = -50
	 	elif x == 4:
	 		p3 = -50
	 	elif x == 5:
	 		p2 = -50
	 	elif x == 6:
	 		p5 = -50

	 	x = x + 1


	group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -50, -50, -50)
	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -50, -50, -50)
	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

	time.sleep(1.5)

	group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, +100, +100, +100)
	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, +100, +100, +100)
	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

	time.sleep(0.2)

	group_pair = modification_pair(group_pair, 40, 0, 40, 20, 45, 20, +100, +100, +100)
	group_impair = modification_impair(group_impair, 0, 40, 40, 45, 20, 20, +100, +100, +100)
	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

	x = 0
	while x < 36:
		if x == 0 or x == 6 or x == 12:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 0, 0, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -25, 0, 0)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x == 1 or x == 7 or x == 13:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -25, 0, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 25, 0, 0)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x == 2 or x == 8 or x == 14:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 25, 0, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -25, -25, 0)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x == 3 or x == 9 or x == 15:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -25, -25, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 25, 25, 0)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x == 4 or x == 10 or x == 16:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 25, 25, 0)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -25, -25, -25)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x == 5 or x == 11 or x == 17:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -25, -25, -25)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 25, 25, 25)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		elif x % 2 == 0:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, 25, 25, 25)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -25, -25, -25)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		else:
			group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -25, -25, -25)
			group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, 25, 25, 25)
			move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))

		x = x + 1
		time.sleep(0.2)

	group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
	group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]
	initialize_to_zero(rob, group_impair, group_pair, 0)


	x =  0
	pas = 2

	while x < 4:
		
		group_pair = modification_pair(group_pair, 0, 0, 0, -pas*10, pas*10, -pas*10, 0, 0, 0)
		group_impair = modification_impair(group_impair, 0, 0, 0, -pas*10, pas*10, pas*10, 0, 0, 0)

		move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		group_pair = modification_pair(group_pair, -pas*10, -pas*10, pas*10, 0, 0, 0, 0, 0, 0)
		group_impair = modification_impair(group_impair, -pas*10, -pas*10, pas*10, 0, 0, 0, 0, 0, 0)

		move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, -25, -25, -25)
	 	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, -25, -25, -25)

	 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		group_pair = modification_pair(group_pair, 0, 0, 0, pas*10, -pas*10, pas*10, 0, 0, 0)
		group_impair = modification_impair(group_impair, 0, 0, 0, pas*10, -pas*10, -pas*10, 0, 0, 0)

		move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		group_pair = modification_pair(group_pair, pas*10, pas*10, -pas*10, 0, 0, 0, 0, 0, 0)
		group_impair = modification_impair(group_impair, pas*10, pas*10, -pas*10, 0, 0, 0, 0, 0, 0)

		move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		group_pair = modification_pair(group_pair, 0, 0, 0, 0, 0, 0, +25, +25, +25)
	 	group_impair = modification_impair(group_impair, 0, 0, 0, 0, 0, 0, +25, +25, +25)

	 	move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		x = x + 1


	group_impair = [0, 160, 160, 180, 95, 95, -70, -70, -70]
	group_pair = [160, 0, 160, 95, 180, 95, -70, -70, -70]
	initialize_to_zero(rob, group_impair, group_pair, 0)

	time.sleep(0.2)

	set_motor_speed(rob, -5)

	while x < 10:
		group_pair = modification_pair(group_pair, 0, 0, 0, -pas*10, pas*10, -pas*10, 0, 0, 0)
		group_impair = modification_impair(group_impair, 0, 0, 0, -pas*10, pas*10, pas*10, 0, 0, 0)

		move(rob, modification_repere_bot_pair(group_pair), modification_repere_bot_impair(group_impair))
		time.sleep(0.2)
		x = x + 1


	set_motor_speed(rob, 5)
