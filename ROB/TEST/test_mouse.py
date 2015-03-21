from Tkinter import *
win=Tk()
win.geometry("1920x1080")
group_impair = 0
x_tmp = 0
y_tmp = 0
z_tmp = 0
debut = 1

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
	global group_impair
	liste = calcule_difference(event.x/10, event.y/10, event.delta/10)
	xm = liste[0]
	ym = liste[1]
	zm = liste[2]
	group_impair[0] = group_impair[0] + xm
	group_impair[3] = group_impair[3] + ym 
	group_impair[6] = group_impair[6] + zm 
	xy_data = "x1=%d,  y1=%d,  z1=%d" % (group_impair[0], group_impair[3], group_impair[6])
	lab=Label(win,text=xy_data)
	lab.grid(row=0,column=0)

def Control_mouse(impair):
	global group_impair
	group_impair = impair
	win.title("Moving leg's windows")
	win.bind("<Motion>",xy)
	mainloop()



if __name__ == '__main__':
	impair = [120, 120, 120, 0, -70, 70, -70, -70, -70]
	Control_mouse(impair)