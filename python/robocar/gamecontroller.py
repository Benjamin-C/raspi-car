# Better looking logging
import logging
logging.basicConfig()
log = logging.getLogger("controller")
log.setLevel(logging.DEBUG)

# Get info from joystick
# TODO pick a differnet lib that is less resource intensive
import pygame
pygame.init()

# Threads to do things
import threading

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

class GameController():
    # Controller axis numbers
    AXES_LEFT_HORIZ: int = 0
    AXES_LEFT_VERT: int = 1
    AXES_LEFT_TRIGGER: int = 4
    AXES_RIGHT_HORIZ: int = 2
    AXES_RIGHT_VERT: int = 3
    AXES_RIGHT_TRIGGER: int = 5

    # A scale factor to apply to each axis. Used to make all joysticks +,+ be up and right
    AXIS_SCALE = {AXES_LEFT_HORIZ: 1, AXES_LEFT_VERT: -1, AXES_LEFT_TRIGGER: 1, AXES_RIGHT_HORIZ: 1, AXES_RIGHT_VERT: -1, AXES_RIGHT_TRIGGER: 1}

    # Controller button numbers
    BUTTON_A: int = 0
    BUTTON_B: int = 1
    BUTTON_X: int = 3
    BUTTON_Y: int = 4
    BUTTON_L1: int = 6
    BUTTON_R1: int = 7

    def __init__(self, joynum:int=0):
        # Initialize joysticks
        pygame.joystick.init()
        # Check if the joystick exists
        ct = pygame.joystick.get_count()
        log.debug(f"There are {ct} joysticks")
        if ct < joynum+1:
            log.critical("No controller detected, aborting")
            return
        # Get the joystick
        self.controller: pygame.joystick.Joystick = pygame.joystick.Joystick(joynum)
        self.controller.init()
        log.debug(f"My joystick has {self.controller.get_numaxes()} axes, {self.controller.get_numhats()} hats, and {self.controller.get_numbuttons()} buttons")
        log.info(f"Joystick connected")

        self._event = threading.Event()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exceptionType, exceptionValue, exceptionTraceback):
        # super().__exit__(exceptionType, exceptionValue, exceptionTraceback)
        self.stop()

    def start(self):
        self._event.set()
        self.pollthread = threading.Thread(target=self.__runthread)
        self.pollthread.start()

    def stop(self):
        self._event.clear()
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
        self._event.wait()

    def __runthread(self):
        while self._event.isSet():
            # We don't need to process the events now, just make sure they are captured.
            pygame.event.get()
        self._event.set()

    def getAxies(self, axis:int) -> float:
        ''' Gets the position of an axis. '''
        return self.controller.get_axis(axis) * self.AXIS_SCALE[axis]
    
    def getButton(self, button:int) -> bool:
        ''' Gets the state of a button '''
        return self.controller.get_button(button)