#! /usr/bin/env python

import pypot.dynamixel
from motor_config import all_motors_not_compliant
from pypot.robot import from_json
from holonomie import ROB_control
import test_holonomie


if __name__ == '__main__':
	rob = from_json('rob.json')
	test_holonomie.init("/dev/input/js0")

	all_motors_not_compliant (rob)

	while(1):
		state = test_holonomie.get_state(rob)
		if(state['ps'] == True):
			break

	#ROB_control(rob)

	rob.close()

