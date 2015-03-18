import threading
import sys
import time
import termios, fcntl, sys, os
#from walking import *

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
 
 
def fnadd() :
    global x,verrou, rob
    speed = 5
    distance = 0
    while True:
        verrou.acquire()
        if x == 'z':
            print 'run'
            #forward(rob, speed, distance)
        elif x == 's':
            print 'run'
            #backward(rob, speed, distance)
        elif x == 'q':
            print 'run'
            #left(rob, speed, distance)
        elif x == 'd':
            print 'run'
            #right(rob, speed, distance)
        elif x == 'a':
            print 'run'
            #rotation_left(rob)
        elif x == 'e':
            print 'run'
            #rotation_right(rob)
        elif x == '-':
            print speed
            speed += 0.1
        elif x == '+':
            print speed
            speed -= 0.1
        elif x == '_':
            print distance
            distance -= 1
        elif x == '=':
            print distance
            distance += 1
        elif x == 'n':
            break;
        x = 0

        verrou.release()
 

def fnsub() :
    keyevent()

def ROB_control(bot):
	global rob
	rob = bot
	t1=threading.Thread(target=fnadd)
	t2=threading.Thread(target=fnsub)
	t1.start()
	t2.start()
	t1.join()
	t2.join()

if __name__ == '__main__':
    ROB_control(0)



