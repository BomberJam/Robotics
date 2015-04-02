import itertools
import time
import numpy
import pypot.dynamixel


def changementid(old_id):
    new_ids = input('choisir le new id: ')
    dxl_io.change_id({old_id:new_ids})

if __name__ == '__main__':

    # we first open the Dynamixel serial port
    with pypot.dynamixel.DxlIO('/dev/ttyUSB0', baudrate=1000000) as dxl_io:
        
        found_ids = dxl_io.scan()
        print 'ids', found_ids

        dxl_io.disable_torque(found_ids)

        old_pos = dxl_io.get_present_position(found_ids)
        print 'current pos', old_pos

        i = len(old_pos)

        while True:
            new_pos = dxl_io.get_present_position(found_ids)
            y = 0

            while y < i:
                if (new_pos[y] > old_pos[y]+10) or (new_pos[y] < old_pos[y]-10):
                    print 'id:', found_ids[y]
                    changementid(found_ids[y])
                    found_ids = dxl_io.scan()
                    new_pos = dxl_io.get_present_position(found_ids)
                    old_pos = new_pos
                    break;

                y = y + 1