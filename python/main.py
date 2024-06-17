# Main Python file

from robocar import DepthCamera, P2Pro, Robot
import cv2
import time

speed = 0.5
turnTime = 3.27

with Robot() as r:
    for i in range(4):
        r.turnLeft(speed, turnTime*0.25)
        r.driveForward(speed, 1/speed)