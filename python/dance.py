# Main Python file

from robocar import DepthCamera, P2Pro, Robot
import cv2
import time

speed = 1
turnTime = 3.27

dance = "square"
dance = "plus"

with Robot() as r:
    if dance == "square":
        for i in range(4):
            r.turnLeft(speed, turnTime*0.25)
            r.driveForward(speed, 1/speed)
    if dance == "plus":
        r.driveLeft(1, 1)
        r.driveRight(1, 1)
        for i in range(4):
            for j in range(3):
                r.driveForward(speed, 0.25)
                time.sleep(0.25)
                r.driveBackward(speed, 0.25)
                time.sleep(0.25)
            r.turnLeft(speed, (turnTime*0.27)/speed)
            time.sleep(1 - (turnTime*0.27)/speed)
            time.sleep(4)
        r.driveLeft(1, 1)
        r.driveRight(1, 1)


