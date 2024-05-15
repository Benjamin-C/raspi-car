from robocar import GameController

# Set up logging
import logging
logging.basicConfig()
log = logging.getLogger("demo")
log.setLevel(logging.DEBUG)

import time

def calcMotors(fb_speed, rl_speed, turnspeed):
    ''' Calculates motor speeds from desired direction
    
    fb_speed is the forward/backward speed, positive forward
    rl_speed is the right/left speed, positive is right
    turnspeed is the turning speed, positive is right
    
    Returns the wheel speeds (fr, fl, br, bl) in the range -1 to 1 '''
    # Normalize values so we can get full speed in all directions

    # Calculate wheel speed
    fr = (fb_speed + rl_speed - turnspeed)
    fl = (fb_speed - rl_speed + turnspeed)
    br = (fb_speed - rl_speed - turnspeed)
    bl = (fb_speed + rl_speed + turnspeed)

    # Only normalize if the speed for any motor would be too fast
    if abs(fr) > 1 or abs(fl) > 1 or abs(br) > 1 or abs(bl) > 1:
        norm = abs(fb_speed) + abs(rl_speed) + abs(turnspeed)
        fr /= norm
        fl /= norm
        br /= norm
        bl /= norm

    return (fr, fl, br, bl)

def setMotors(fr:float|list, fl:float=None, br:float=None, bl:float=None):
    ''' Sets the speed of the motors.
    
    If fr, fl, br, and bl are all floats, then they will set their respective motor speeds.
    If fr is the only value specified and is a float, then all motors will be set to that speed
    If fr is the only value specified and it is a list or a tuple, its values will be used for fr, fl, br, and bl motors
    '''

    m = None
    if fl is None:
        # If we have a list already
        if isinstance(fr, list) or isinstance(fr, tuple):
            m = fr
        # If we have a single float
        else:
            m = (fr, fr, fr, fr)
    else:
        # If we have several floats
        m = (fr, fl, br, bl)
    # Set motor speed. Just log for now, later talk to the mainboard to actually drive the motors
    log.info(f"Motors: {' '.join([f'{v:>-5.2f}' for v in m])}")

with GameController() as gc:
    while(True):
        if gc.getButton(GameController.BUTTON_L1) and gc.getButton(GameController.BUTTON_R1):
            m = calcMotors(gc.getAxies(GameController.AXES_RIGHT_VERT), gc.getAxies(GameController.AXES_RIGHT_HORIZ), gc.getAxies(GameController.AXES_LEFT_HORIZ))
            setMotors(m)
        else:
            setMotors(0)
        time.sleep(0.01)