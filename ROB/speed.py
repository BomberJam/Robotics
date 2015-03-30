import itertools
import time
import numpy
import pypot.dynamixel
from  motor_config import *
from motor_config import all_motors_not_compliant
from pypot.robot import from_json


if __name__ == '__main__':

	rob = from_json('rob.json')

	all_motors_not_compliant (rob)

	t = numpy.arange(0, 10, 0.01)
	speed = 20 * numpy.cos(2 * numpy.pi * 0.1 * t)

	positions = []

	for s in rob.motors:
		s.moving_speed = speed
		s.goal_position = 40
		time.sleep(0.05)

	rob.close()