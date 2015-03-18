import itertools
import time
import numpy
import pypot.dynamixel
init_servo = 90

def blink(i):
    z = 0
    while z<10:
        dxl_io.switch_led_on({i:i})
        time.sleep(0.5)
        dxl_io.switch_led_off({i:i})
        time.sleep(0.5)
        z = z+1

def changementid ():

    liste = dxl_io.scan()
    print 'Detected:', liste
    while True:
        new_liste = []
        retour = 0
        for i in liste:
            #clignote l'alarme
            dxl_io.switch_led_on({i:i})
            blink(i)
            while retour==0:
                new_ids = input('choisir le new id')

                retour = initialisation(new_liste, i, new_ids)

            new_liste.append(new_ids)
            #dxl_io.switch_led_off({i:i})
            retour = 0

        return

def initialisation(liste, old_ids, new_ids):
    for i in liste:
        if i == new_ids:
            return 0

    dxl_io.change_id({old_ids:new_ids})
    return 1



def preinitialisation(liste, old_ids):
    init_servo = 90
    for i in liste:
        if i == new_ids:
            return 0

    dxl_io.change_id({old_ids:init_servo})
    init_servo = init_servo+1
    return 1


if __name__ == '__main__':

    # we first open the Dynamixel serial port
    with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:

        # we can scan the motors
        #found_ids = dxl_io.scan()  # this may take several seconds
        #print 'Detected:', found_ids

        changementid()
        found_ids = dxl_io.scan()  # this may take several seconds
        print 'Detected:', found_ids

        # we power on the motors
        dxl_io.enable_torque(found_ids)

        # we get the current positions
        print 'Current pos:', dxl_io.get_present_position(found_ids)

        # we create a python dictionnary: {id0 : position0, id1 : position1...}
        pos = dict(zip(found_ids, itertools.repeat(0)))
        #pos =  dict({10 : 0, 11: 0, 12: 0})
        print 'Cmd:', pos

        # we send these new positions
        dxl_io.set_goal_position(pos)
        time.sleep(1)  # we wait for 1s

        # we get the current positions
        print 'New pos:', dxl_io.get_present_position(found_ids)

        time.sleep(1)  # we wait for 1s

        t0 = time.time()
        while True:
            t = time.time()
            if (t - t0) > 10:
                break

            pos = 20 * numpy.sin(2 * numpy.pi * 0.5 * t)
            dxl_io.set_goal_position(dict(zip(found_ids, itertools.repeat(pos))))

            time.sleep(0.02)



        # we power off the motors
        dxl_io.disable_torque(found_ids)
