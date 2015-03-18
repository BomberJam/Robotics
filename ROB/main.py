import pypot.dynamixel
import time
import threading
import sys
import termios, fcntl, sys, os
from kinematic import *
from movement import *
from pypot.robot import from_json
from init_by_move import *
from walking import *

x = 0
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
	global x,verrou
	try:
		while x != 'n':
			try:
				x = sys.stdin.read(1)
				print "value changed", repr(x)
			except IOError: pass
	finally:
		termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
		fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
 
 
def commande() :
    global x,verrou, rob
    man = 0
    step_by_step = 0
    speed = 0.5
    distance = 20
    odometrie = 0
    liste = [1, 1]
    while True:
        verrou.acquire()
        if x == 'z':
            odometrie += distance
            print odometrie

            if step_by_step == 1:
                liste = move_step_by_step(liste[0], liste[1], 'f', rob)
            else:
                forward(rob, speed, distance)

        elif x == 's':
            odometrie += distance
            print odometrie

            if step_by_step == 1:
                liste = move_step_by_step(liste[0], liste[1], 'b', rob)
            else:
                backward(rob, speed, distance)

        elif x == 'q':
            odometrie += distance
            print odometrie

            if step_by_step == 1:
                liste = move_step_by_step2(liste[0], liste[1], 'l', rob)
            else:
                left(rob, speed, distance)

        elif x == 'd':
            odometrie += distance
            print odometrie

            if step_by_step == 1:
                liste = move_step_by_step2(liste[0], liste[1], 'r', rob)
            else:
                right(rob, speed, distance)

        elif x == 'a':
        	rotation_left2(rob, speed)
        elif x == 'e':
	        rotation_right2(rob, speed)
        elif x == '-':
        	print speed
        	speed -= 0.1
        	x = tmp
        elif x == '+':
        	print speed
        	speed += 0.1
        	x = tmp
        elif x == '_':
        	print distance
        	distance -= 1
        	x = tmp
        elif x == '=':
        	print distance
        	distance += 1
        	x = tmp
        elif x == 'x':
        	x = 0
        elif x == 'm':
       		if man == 1:
       			man = 0
       		else:
       			man = 1
       		x = 0
       	elif x == 'p':
       		if step_by_step == 0:
	       		step_by_step = 1
	       	else:
	       		step_by_step = 0
	       	x = 0
        elif x == 'n':
            break;
        elif x == 'i':
            initialize_to_zero(rob)
            print x
        elif x == '1':
        	cheat(rob, 1)
        	print x
        elif x == '2':
        	cheat(rob, 2)
        	print x

        tmp = x

        if man == 0:
        	x = 0

        verrou.release()
        time.sleep(0.1)


def ROB_control():
	t1=threading.Thread(target=commande)
	t2=threading.Thread(target=keyevent)
	t1.start()
	t2.start()
	t1.join()
	t2.join()


if __name__ == '__main__':
	rob = from_json('rob.json')

	all_motors_not_compliant (rob)

	ROB_control()

	rob.close()