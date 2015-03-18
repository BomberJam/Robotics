#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# inspiré de http://wikipython.flibuste.net/moin.py/QuestionsGenerales
 
import threading
import sys
import time
import termios, fcntl, sys, os
fd = sys.stdin.fileno()

oldterm = termios.tcgetattr(fd)
newattr = termios.tcgetattr(fd)
newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
termios.tcsetattr(fd, termios.TCSANOW, newattr)

oldflags = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, oldflags | os.O_NONBLOCK)

def keyevent():
    try:
        while 1:
            try:
                c = sys.stdin.read(1)
                print "Got character", repr(c)
            except IOError: pass
    finally:
        termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
        fcntl.fcntl(fd, fcntl.F_SETFL, oldflags)
 
x = 0
n = 1000
 
def fnadd() :
    global x,verrou
    while True:
        verrou.acquire()
        x += 1
        print x
        verrou.release()
        time.sleep(0.5)
 
def fnsub() :
    keyevent()
 
verrou = threading.Lock()
t1=threading.Thread(target=fnadd)
t2=threading.Thread(target=fnsub)
t1.start()
t2.start()
t1.join()
t2.join()
print "Valeur finale de la variable x = ", x