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
	global x_tmp, y_tmp, debut
	if debut == 1:
		x_tmp = x
		y_tmp = y
		debut = 0

	liste = [x-x_tmp, y_tmp-y]
	x_tmp = x
	y_tmp = y

	return liste

def incre_z(event):
	global z_tmp
	z_tmp = z_tmp + 1

def decre_z(event):
	global z_tmp
	z_tmp = z_tmp - 1

def xy(event):
	global group_impair, group_pair, leg, z_tmp
	liste = calcule_difference(event.x/10, event.y/10, event.delta/10)
	xm = liste[0]
	ym = liste[1]
	group_impair[0] = group_impair[0] + ym
	group_impair[3] = group_impair[3] - xm 
	group_impair[6] = group_impair[6] + z_tmp 
	z_tmp = 0
	xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_impair[0], group_impair[3], group_impair[6])
	set_pos_to_leg (group_impair[0], group_impair[3], group_impair[6], leg)
	lab=Label(win,text=xy_data)
	lab.grid(row=0,column=0)

def Control_mouse(impair, pair, l):
	global group_impair, group_pair, leg, rob
	group_impair = impair
	group_pair = pair
	leg = l
	win.title("Moving leg's windows")
	win.bind("<Motion>",xy)
	win.bind("<B1-Motion>", decre_z)
	win.bind("<B3-Motion>", incre_z)
	mainloop()



if __name__ == '__main__':
	rob = from_json('rob.json')

	all_motors_not_compliant (rob)

	pair = [120, 120, 120, 70, 0, -70, -70, -70, -70]
	impair = [120, 120, 120, 0, -70, 70, -70, -70, -70]

	initialize_to_zero(rob, impair, pair)

	choix = input ('choix patte: ')
	if choix ==  1:
		leg = rob.leg1
	elif choix == 2:
		leg = rob.leg2
	elif choix == 3:
		leg = rob.leg3
	elif choix == 4:
		leg = rob.leg4
	elif choix == 5:
		leg = rob.leg5
	elif choix == 6:
		leg = rob.leg6

	Control_mouse(impair, pair, leg)

	rob.close()


