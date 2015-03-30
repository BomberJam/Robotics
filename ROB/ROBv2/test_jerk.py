#! /usr/bin/env python

import time


if __name__ == '__main__':
	x = 1
	while x < 200:
		n = x/(200.0-1.0)
		print 'n: ', n
		m = (200.0-1.0-x)/(200.0-1.0)
		print 'm: ', m
		speed = m*x + n*200.0
		print 'speed: ', speed
		time.sleep(0.1)
		x = x + 1

	exit()