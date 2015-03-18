import pypot.dynamixel
from motor_config import *
from special_move import *


def forward(rob, speed, distance):
    impair_up(rob)
    time.sleep(speed)

    pair_forward(rob, distance)
    time.sleep(speed)
    
    impair_forward(rob, distance)
    time.sleep(speed)
    
    pair_up(rob)
    time.sleep(speed)
    
    impair_backward(rob, distance)
    time.sleep(speed)
    
    pair_backward(rob, distance)
    time.sleep(speed)

def backward(rob, speed, distance):
    impair_up(rob)
    time.sleep(speed)

    pair_backward(rob, distance)
    time.sleep(speed)
    
    impair_backward(rob, distance)
    time.sleep(speed)
    
    pair_up(rob)
    time.sleep(speed)
    
    impair_forward(rob, distance)
    time.sleep(speed)
    
    pair_forward(rob, distance)
    time.sleep(speed)



def impair_up(rob):
    set_pos_to_leg(120, 0, -20, rob.leg1)
    set_pos_to_leg(120, -70, -20, rob.leg3)
    set_pos_to_leg(120, 70, -20, rob.leg5)

def pair_up(rob):
    set_pos_to_leg(120, 70, -20, rob.leg2)
    set_pos_to_leg(120, 0, -20, rob.leg4)
    set_pos_to_leg(120, -70, -20, rob.leg6)

def impair_forward(rob, distance):
    set_pos_to_leg(120 + distance, 0, -70, rob.leg1)
    set_pos_to_leg(120, -70 + distance, -70, rob.leg3)
    set_pos_to_leg(120, 70 - distance, -70, rob.leg5)

def pair_forward(rob, distance):
    set_pos_to_leg(120, 70 - distance, -70, rob.leg2)
    set_pos_to_leg(120 + distance, 0, -70, rob.leg4)
    set_pos_to_leg(120, -70 + distance, -70, rob.leg6)


def impair_backward(rob, distance):
    set_pos_to_leg(120 - distance, 0, -70, rob.leg1)
    set_pos_to_leg(120, -70 - distance, -70, rob.leg3)
    set_pos_to_leg(120, 70 + distance , -70, rob.leg5)

def pair_backward(rob, distance):
    set_pos_to_leg(120, 70 + distance, -70, rob.leg2)
    set_pos_to_leg(120 - distance, 0, -70, rob.leg4)
    set_pos_to_leg(120, -70 - distance, -70, rob.leg6)




def left(rob, speed, distance):
    impair_up(rob)
    time.sleep(speed)

    pair_left(rob, distance)
    time.sleep(speed)
    
    impair_left(rob, distance)
    time.sleep(speed)
    
    pair_up(rob)
    time.sleep(speed)
    
    impair_right(rob, distance)
    time.sleep(speed)
    
    pair_right(rob, distance)
    time.sleep(speed)


def right(rob, speed, distance):
    impair_up(rob)
    time.sleep(speed)

    pair_right(rob, distance)
    time.sleep(speed)
    
    impair_right(rob, distance)
    time.sleep(speed)
    
    pair_up(rob)
    time.sleep(speed)
    
    impair_left(rob, distance)
    time.sleep(speed)
    
    pair_left(rob, distance)
    time.sleep(speed)


def impair_left(rob, distance):
    set_pos_to_leg(120, 0 + distance, -70, rob.leg1)
    set_pos_to_leg(120 - distance, -70, -70, rob.leg3)
    set_pos_to_leg(120 + distance, 70, -70, rob.leg5)

def pair_left(rob, distance):
    set_pos_to_leg(120 + distance, 70, -70, rob.leg2)
    set_pos_to_leg(120, 0 + distance, -70, rob.leg4)
    set_pos_to_leg(120 - distance, -70, -70, rob.leg6)


def impair_right(rob, distance):
    set_pos_to_leg(120, 0 - distance, -70, rob.leg1)
    set_pos_to_leg(120 + distance, -70, -70, rob.leg3)
    set_pos_to_leg(120 - distance, 70, -70, rob.leg5)

def pair_right(rob, distance):
    set_pos_to_leg(120 - distance, 70, -70, rob.leg2)
    set_pos_to_leg(120, 0 - distance, -70, rob.leg4)
    set_pos_to_leg(120 + distance, -70, -70, rob.leg6)



def move_step_by_step(count, step, direction, rob):
    if direction == 'f':
        dep = count
    elif direction == 'b':
        dep = -count

    if step == 1:
        set_pos_to_leg(120+dep, 0, -70+dep*2, rob.leg1)
        set_pos_to_leg(120, 70-dep, -70, rob.leg2)
        set_pos_to_leg(120, -70+dep, -70+dep*2, rob.leg3)
        set_pos_to_leg(120+dep, 0, -70, rob.leg4)
        set_pos_to_leg(120, 70-dep, -70+dep*2, rob.leg5)
        set_pos_to_leg(120, -70+dep, -70, rob.leg6)
    elif step == 2:
        set_pos_to_leg(120+dep, 0, -70-dep*2, rob.leg1)
        set_pos_to_leg(120, 70-dep, -70, rob.leg2)
        set_pos_to_leg(120, -70+dep, -70-dep*2, rob.leg3)
        set_pos_to_leg(120+dep, 0, -70, rob.leg4)
        set_pos_to_leg(120, 70-dep, -70-dep*2, rob.leg5)
        set_pos_to_leg(120, -70+dep, -70, rob.leg6)
    elif step == 3:
        set_pos_to_leg(120+dep, 0, -70, rob.leg1)
        set_pos_to_leg(120, 70-dep, -70+dep*2, rob.leg2)
        set_pos_to_leg(120, -70+dep, -70, rob.leg3)
        set_pos_to_leg(120+dep, 0, -70+dep*2, rob.leg4)
        set_pos_to_leg(120, 70-dep, -70, rob.leg5)
        set_pos_to_leg(120, -70+dep, -70+dep*2, rob.leg6)
    elif step == 4:
        set_pos_to_leg(120+dep, 0, -70, rob.leg1)
        set_pos_to_leg(120, 70-dep, -70-dep*2, rob.leg2)
        set_pos_to_leg(120, -70+dep, -70, rob.leg3)
        set_pos_to_leg(120+dep, 0, -70-dep*2, rob.leg4)
        set_pos_to_leg(120, 70-dep, -70, rob.leg5)
        set_pos_to_leg(120, -70+dep, -70-dep*2, rob.leg6)

    count += 1

    if count > 10:
        step += 1

    if count > 20:
        count = 1

    if step > 4:
        step = 1

    return [count, step]


def move_step_by_step2(count, step, direction, rob):
    if direction == 'r':
        dep = 1
    elif direction == 'l':
        dep = -1

    if step == 1:
        set_pos_to_leg(120, 0+dep, -70+dep*2, rob.leg1)
        set_pos_to_leg(120+dep, 70, -70, rob.leg2)
        set_pos_to_leg(120-dep, -70, -70+dep*2, rob.leg3)
        set_pos_to_leg(120, 0+dep, -70, rob.leg4)
        set_pos_to_leg(120+dep, 70, -70+dep*2, rob.leg5)
        set_pos_to_leg(120-dep, -70, -70, rob.leg6)
    elif step == 2:
        set_pos_to_leg(120, 0+dep, -70-dep*2, rob.leg1)
        set_pos_to_leg(120, 70-dep, -70, rob.leg2)
        set_pos_to_leg(120-dep, -70+dep, -70-dep*2, rob.leg3)
        set_pos_to_leg(120, 0+dep, -70, rob.leg4)
        set_pos_to_leg(120+dep, 70-dep, -70-dep*2, rob.leg5)
        set_pos_to_leg(120, -70+dep, -70, rob.leg6)
    elif step == 3:
        set_pos_to_leg(120, 0-dep, -70, rob.leg1)
        set_pos_to_leg(120-dep, 70, -70+dep*2, rob.leg2)
        set_pos_to_leg(120+dep, -70, -70, rob.leg3)
        set_pos_to_leg(120, 0-dep, -70+dep*2, rob.leg4)
        set_pos_to_leg(120-dep, 70, -70, rob.leg5)
        set_pos_to_leg(120+dep, -70, -70+dep*2, rob.leg6)
    elif step == 4:
        set_pos_to_leg(120, 0-dep, -70, rob.leg1)
        set_pos_to_leg(120-dep, 70, -70-dep*2, rob.leg2)
        set_pos_to_leg(120+dep, -70, -70, rob.leg3)
        set_pos_to_leg(120, 0-dep, -70-dep*2, rob.leg4)
        set_pos_to_leg(120-dep, 70, -70, rob.leg5)
        set_pos_to_leg(120+dep, -70, -70-dep*2, rob.leg6)

    count += 1

    if count > 10:
        step += 1

    if step > 4:
        step = 1

    return [count, step]