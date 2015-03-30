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
choix = 0

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
	global group_impair, group_pair, z_tmp, choix
	liste = calcule_difference(event.x/10, event.y/10, event.delta/10)
	xm = liste[0]
	ym = liste[1]

	if choix ==  1:
		leg = rob.leg1
		group_impair[0] = group_impair[0] + ym
		group_impair[3] = group_impair[3] - xm 
		group_impair[6] = group_impair[6] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_impair[0], group_impair[3], group_impair[6])
		set_pos_to_leg (group_impair[0], group_impair[3], group_impair[6], leg)
	elif choix == 2:
		leg = rob.leg2
		group_pair[0] = group_pair[0] + ym
		group_pair[3] = group_pair[3] - xm 
		group_pair[6] = group_pair[6] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_pair[0], group_pair[3], group_pair[6])
		set_pos_to_leg (group_pair[0], group_pair[3], group_pair[6], leg)
	elif choix == 3:
		leg = rob.leg3
		group_impair[1] = group_impair[1] + ym
		group_impair[4] = group_impair[4] - xm 
		group_impair[7] = group_impair[7] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_impair[1], group_impair[4], group_impair[7])
		set_pos_to_leg (group_impair[1], group_impair[4], group_impair[7], leg)
	elif choix == 4:
		leg = rob.leg4
		group_pair[1] = group_pair[1] + ym
		group_pair[4] = group_pair[4] - xm 
		group_pair[7] = group_pair[7] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_pair[1], group_pair[4], group_pair[7])
		set_pos_to_leg (group_pair[1], group_pair[4], group_pair[7], leg)
	elif choix == 5:
		leg = rob.leg5
		group_impair[2] = group_impair[2] + ym
		group_impair[5] = group_impair[5] - xm 
		group_impair[8] = group_impair[8] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_pair[2], group_pair[5], group_pair[8])
		set_pos_to_leg (group_pair[2], group_pair[5], group_pair[8], leg)
	elif choix == 6:
		leg = rob.leg6
		group_pair[2] = group_pair[2] + ym
		group_pair[5] = group_pair[5] - xm 
		group_pair[8] = group_pair[8] + z_tmp 
		z_tmp = 0
		xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_pair[2], group_pair[5], group_pair[8])
		set_pos_to_leg (group_pair[2], group_pair[5], group_pair[8], leg)

	lab=Label(win,text=xy_data)
	lab.grid(row=0,column=0)

def Control_mouse(impair, pair):
	global group_impair, group_pair, rob
	group_impair = impair
	group_pair = pair
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
	
	Control_mouse(impair, pair)

	rob.close()


