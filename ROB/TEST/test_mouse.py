import pypot.dynamixel
from motor_config import all_motors_not_compliant
from pypot.robot import from_json
from movement import *
from Tkinter import *
from kinematic import *
from math import *
from init_by_move import *
from walking import *

win=Tk()
win.geometry("1920x1080")
group_impair = 0
x_tmp = 0
y_tmp = 0
z_tmp = 0
debut = 1
leg = 0

def calcule_difference(x, y, z):
	global x_tmp, y_tmp, z_tmp, debut
	if debut == 1:
		x_tmp = x
		y_tmp = y
		z_tmp = z
		debut = 0

	liste = [x-x_tmp, y_tmp-y, z_tmp-z]
	x_tmp = x
	y_tmp = y
	z_tmp = z

	return liste

def xy(event):
	global group_impair, group_pair, leg
	liste = calcule_difference(event.x/10, event.y/10, event.delta/10)
	xm = liste[0]
	ym = liste[1]
	zm = liste[2]
	group_impair[0] = group_impair[0] + xm
	group_impair[3] = group_impair[3] + ym 
	group_impair[6] = group_impair[6] + zm 
	xy_data = "x1=%d,  y1=%d,  z1=%d,  patte=%s" % (group_impair[0], group_impair[3], group_impair[6], leg)
	set_pos_to_leg (xm, ym, zm, leg)
	lab=Label(win,text=xy_data)
	lab.grid(row=0,column=0)

def Control_mouse(impair, pair, l):
	global group_impair, group_pair, leg, rob
	group_impair = impair
	group_pair = pair
	leg = l
	win.title("Moving leg's windows")
	win.bind("<Motion>",xy)
	mainloop()



if __name__ == '__main__':
	pair = [120, 120, 120, 70, 0, -70, -70, -70, -70]
	impair = [120, 120, 120, 0, -70, 70, -70, -70, -70]

	choix = input ('choix patte: ')
	if choix ==  1:
		leg = 'rob.leg1'
	elif choix == 2:
		leg = 'rob.leg2'
	elif choix == 3:
		leg = 'rob.leg3'
	elif choix == 4:
		leg = 'rob.leg4'
	elif choix == 5:
		leg = 'rob.leg5'
	elif choix == 6:
		leg = 'rob.leg6'

	rob = from_json('rob.json')

	all_motors_not_compliant (rob)

	initialize_to_zero(rob, impair, gpair)

	Control_mouse(impair, pair, leg)

	rob.close()


