import pygame
pygame.init()

import time

# Set up logging
import logging
logging.basicConfig()
log = logging.getLogger("demo")
log.setLevel(logging.DEBUG)

# Verify that the controller exists
pygame.joystick.init()
ct = pygame.joystick.get_count()
log.debug(f"There are {ct} joysticks")
if ct < 1:
    log.critical("No controller detected, aborting")
    exit()

# Get the controller
c = pygame.joystick.Joystick(0)
c.init()
log.debug(f"My joystick has {c.get_numaxes()} axes, {c.get_numhats()} hats, and {c.get_numbuttons()} buttons")
log.info(f"Joystick connected")

log.info("Started!")

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
    

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        
        # if event.type == pygame.JOYBUTTONDOWN:
        #     log.info(f"Button {event.button} pressed")

        # if event.type == pygame.JOYBUTTONUP:
        #     log.info(f"Button {event.button} released")

        # if e.type == pygame.JOYAXISMOTION:
        #     # log.info(f"Joystick! {' '.join([f'{c.get_axis(i):.2f}' for i in range(c.get_numaxes())])}")

        # Only respond to relevent events
        if event.type in [pygame.JOYBUTTONDOWN, pygame.JOYBUTTONUP, pygame.JOYAXISMOTION]:
            # Dead man's switch; require both R1 and L1 to be pressed to move
            if c.get_button(6) and c.get_button(7):
                m = calcMotors(c.get_axis(3)*-1, c.get_axis(2), c.get_axis(0))
                setMotors(m)
            else:
                setMotors(0)

# SteelSeries Stratus XL controller mapping:
# Buttons:
# 0:  A
# 1:  B
# 3:  X
# 4:  Y
# 11: >
# 6:  L1
# 7:  R1
# Axes:
# 0: L horiz +right
# 1: L vert  +down
# 2: R horiz +right
# 3: R vert  +down
# 4: rtrig   +pressed
# 5: ltrig   +pressed
