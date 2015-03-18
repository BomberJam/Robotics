import pypot.dynamixel
import time
from kinematic import *
from movement import *
from pypot.robot import from_json


if __name__ == '__main__':
	speed = 0.3

	rob = from_json('rob.json')
	initialize_to_zero(rob)

	all_motors_not_compliant (rob)

	time.sleep(1)

	k = kinematic(0, -38, -26.11)
	print k
	print inverse_kinematic(120, 70, -70)

	#rotation(rob)

	forward(rob, speed)

	#move_10mm(rob)

	#script_auto_f5(rob)

	rob.close()