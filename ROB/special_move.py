import pypot.dynamixel
from motor_config import *


def script_auto_f5(rob):
    set_pos_to_leg(80, 0, -40, rob.leg1)
    time.sleep(0.5)
    set_pos_to_leg(80, 0, -70, rob.leg1)
    time.sleep(0.5)


def move_10mm(rob):
    set_pos_to_leg(90, 0, -70, rob.leg1)
    set_pos_to_leg(120, 40, -70, rob.leg2)
    set_pos_to_leg(120, -100, -70, rob.leg3)
    set_pos_to_leg(150, 0, -70, rob.leg4)
    set_pos_to_leg(120, 100, -70, rob.leg5)
    set_pos_to_leg(120, -40, -70, rob.leg6)

    time.sleep(1)    

    set_pos_to_leg(150, 0, -70, rob.leg1)
    set_pos_to_leg(120, 100, -70, rob.leg2)
    set_pos_to_leg(120, -40, -70, rob.leg3)
    set_pos_to_leg(90, 0, -70, rob.leg4)
    set_pos_to_leg(120, 40, -70, rob.leg5)
    set_pos_to_leg(120, -100, -70, rob.leg6)

    time.sleep(1)


def rotation_left(rob):
    pair_height = 70
    impair_height = 70

    while True:
        impair_up(rob)
        impair_height = 20
        time.sleep(1)

        pair_rotate_right_to_left(rob, pair_height)
        time.sleep(1)
        impair_down(rob, -60)#position y de la patte quand elle est au sol
        impair_height = 70
        time.sleep(1)

        pair_up(rob)
        pair_height = 20
        time.sleep(1)

        impair_rotate_right_to_left(rob, impair_height)
        time.sleep(1)

        pair_down(rob, -60)
        pair_height = 70
        time.sleep(1)


def rotation_right(rob):
    pair_height = 70
    impair_height = 70

    while True:
        impair_up(rob)
        impair_height = 20
        time.sleep(1)

        pair_rotate_left_to_right(rob, pair_height)
        time.sleep(1)
        impair_down(rob, -60)#position y de la patte quand elle est au sol
        impair_height = 70
        time.sleep(1)

        pair_up(rob)
        pair_height = 20
        time.sleep(1)

        impair_rotate_left_to_right(rob, impair_height)
        time.sleep(1)

        pair_down(rob, -60)
        pair_height = 70
        time.sleep(1)


def impair_up(rob):
    set_pos_to_leg(120, 0, -20, rob.leg1)
    set_pos_to_leg(120, -70, -20, rob.leg3)
    set_pos_to_leg(120, 70, -20, rob.leg5)

def pair_up(rob):
    set_pos_to_leg(120, 70, -20, rob.leg2)
    set_pos_to_leg(120, 0, -20, rob.leg4)
    set_pos_to_leg(120, -70, -20, rob.leg6)

def impair_rotate_left_to_right(rob, height):
    set_pos_to_leg(120, -60, -height, rob.leg1)
    set_pos_to_leg(66, 39, -109, rob.leg3)
    set_pos_to_leg(66, 39, -109, rob.leg5)

def pair_rotate_left_to_right(rob, height):
    set_pos_to_leg(66, 39, -109, rob.leg2)
    set_pos_to_leg(120, -60, -height, rob.leg4)
    set_pos_to_leg(66, 39, -109, rob.leg6)


def impair_rotate_right_to_left(rob, height):
    set_pos_to_leg(120, 80, -height, rob.leg1)
    set_pos_to_leg(138.92, 0, -70, rob.leg3)
    set_pos_to_leg(89.30, 106.42, -70, rob.leg5)

def pair_rotate_right_to_left(rob, height):
    set_pos_to_leg(89.30, 106.42, -70, rob.leg2)
    set_pos_to_leg(120, 80, -height, rob.leg4)
    set_pos_to_leg(138.92, 0, -70, rob.leg6)


def rotation_left2(rob, speed):
    impair_up(rob)
    time.sleep(speed)

    pair_rotate_right_to_left2(rob)
    time.sleep(speed)

    impair_rotate_left_to_right2(rob)
    time.sleep(speed)

    pair_up(rob)
    time.sleep(speed)

    impair_rotate_right_to_left2(rob)
    time.sleep(speed)

    pair_rotate_left_to_right2(rob)
    time.sleep(speed)


def rotation_right2(rob, speed):
    impair_up(rob)
    time.sleep(speed)

    pair_rotate_left_to_right2(rob)
    time.sleep(speed)

    impair_rotate_right_to_left2(rob)
    time.sleep(speed)

    pair_up(rob)
    time.sleep(speed)

    impair_rotate_left_to_right2(rob)
    time.sleep(speed)

    pair_rotate_right_to_left2(rob)
    time.sleep(speed)

    
def impair_rotate_left_to_right2(rob):
    set_pos_to_leg(120, -70, -70, rob.leg1)
    set_pos_to_leg(68.4, -121, -70, rob.leg3)
    set_pos_to_leg(139, 0, -70, rob.leg5)

def pair_rotate_left_to_right2(rob):
    set_pos_to_leg(139, 0, -70, rob.leg2)
    set_pos_to_leg(120, -70, -70, rob.leg4)
    set_pos_to_leg(68.4, -121, -70, rob.leg6)


def impair_rotate_right_to_left2(rob):
    set_pos_to_leg(120, 70, -70, rob.leg1)
    set_pos_to_leg(139, 0, -70, rob.leg3)
    set_pos_to_leg(68.4, 121, -70, rob.leg5)

def pair_rotate_right_to_left2(rob):
    set_pos_to_leg(68.4, 121, -70, rob.leg2)
    set_pos_to_leg(120, 70, -70, rob.leg4)
    set_pos_to_leg(139, 0, -70, rob.leg6)
