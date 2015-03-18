from kinematic import *


if __name__ == '__main__':

	while True:
		x = input('x:')
		y = input('y:')
		z = input('z:')

		print inverse_kinematic(x, y, z)