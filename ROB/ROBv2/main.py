#! /usr/bin/env python

import pypot.dynamixel
from motor_config import all_motors_not_compliant
from pypot.robot import from_json
from holonomie import *
import time


if __name__ == '__main__':
	rob = from_json('rob.json')

	all_motors_not_compliant (rob)

	ROB_control("/dev/input/js0", rob)

	all_motors_compliant (rob)

	rob.close()