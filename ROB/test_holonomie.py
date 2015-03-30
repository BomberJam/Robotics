import sys
import os
import threading

joy = { 'leftx': 0.0, 'lefty': 0.0, 'rightx': 0.0, 'righty': 0.0, 
        'trig0': False, 'trig1': False, 'trig2': False, 'trig3': False, 
        'buttonup': False, 'buttondown': False, 'buttonleft': False, 'buttonright': False,
        'triangle': False, 'circle': False, 'cross': False, 'square': False, 
        'select': False, 'start': False, 'ps': False}


class ThreadClass(threading.Thread):
	def run(self):
		global pipe
		global action
		global spacing

		while 1:
			for character in pipe.read(1):
				action += ['%02X' % ord(character)]
				if len(action) == 8:

					num = int(action[5], 16)
					percent254 = str(((float(num)-128.0)/126.0)-100)[4:6]
					percent128 = str((float(num)/127.0))[2:4]

					if percent254 == '.0':
						percent254 = '100'
					if percent128 == '0':
						percent128 = '100'

					if action[6] == '01':
						if action[4] == '01':
							if action[7] == '0A':
								joy['trig0'] = True
							if action[7] == '0B':
								joy['trig1'] = True
							if action[7] == '08':
								joy['trig2'] = True
							if action[7] == '09':
								joy['trig3'] = True
							if action[7] == '04':
								joy['buttonup'] = True
							if action[7] == '05':
								joy['buttonright'] = True
							if action[7] == '06':
								joy['buttondown'] = True
							if action[7] == '07':
								joy['buttonleft'] = True
							if action[7] == '0C':
								joy['triangle'] = True
							if action[7] == '0D':
								joy['circle'] = True
							if action[7] == '0E':
								joy['cross'] = True
							if action[7] == '0F':
								joy['square'] = True
							if action[7] == '00':
								joy['select'] = True
							if action[7] == '03':
								joy['start'] = True
							if action[7] == '10':
								joy['ps'] = True
								exit()

						else:
							print action[7]
							choix = 0

					elif action[7] == '00':
						print action[7]
						num = int(action[5], 16)
						if num >= 128:
							joy['leftx'] = -int(percent254)
						elif num <= 127 \
						and num != 0:
							joy['leftx'] = int(percent128)
						else:
							joy['leftx'] = 0


					elif action[7] == '01':
						print action[7]
						num = int(action[5], 16)
						if num >= 128:
							joy['lefty'] = -int(percent254)
						elif num <= 127 \
						and num != 0:
							joy['lefty'] = int(percent128)
						else:
							joy['lefty'] = 0


					elif action[7] == '02':
						print action[7]
						num = int(action[5], 16)
						if num >= 128:
							joy['rightx'] = -int(percent254)
						elif num <= 127 \
						and num != 0:
							joy['rightx'] = int(percent128)
						else:
							joy['rightx'] = 0

					elif action[7] == '03':
						print action[7]
						num = int(action[5], 16)
						if num >= 128:
							joy['righty'] = -int(percent254)
						elif num <= 127 \
						and num != 0:
							joy['righty'] = int(percent128)
						else:
							joy['righty'] = 0
					action = []

t = ThreadClass()

def init(path):
	global pipe
	global action
	global spacing
	action = []
	spacing = 0
	try:
		pipe = open(path, 'r')
	except:
		return False
	t.start()
	return True

def get_state(bot):
	global joy, rob
	rob = bot

	return joy