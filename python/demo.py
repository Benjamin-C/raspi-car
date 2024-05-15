from depthcam import DepthCamera
from p2pro import P2Pro
import cv2
import time

with DepthCamera() as dc:
    with P2Pro() as tc:
        while True:

            distframe = dc.getDistFrame()
            # Available color maps: https://docs.opencv.org/3.4/d3/d50/group__imgproc__colormap.html
            distframe = cv2.applyColorMap(distframe, cv2.COLORMAP_JET)
            cv2.imshow("disparity", distframe)

            colframe = dc.getColorFrame()
            cv2.imshow("color", colframe)

            thermalframe = tc.imdata
            cv2.imshow("thermal", thermalframe)

            if cv2.waitKey(100) == ord('q'):
                break
                
            time.sleep(1)