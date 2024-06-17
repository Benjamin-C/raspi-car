import cv2 as cv
import numpy as np
import time
from robocar import P2Pro, Robot

import logging
log = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.DEBUG)

#ser = serial.
def count_white_pixels(frame):
    # Convert the image to grayscale
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    # Threshold the image to get binary image with white pixels
    _, thresh_frame = cv.threshold(gray_frame, 200, 255, cv.THRESH_BINARY)
    # Count white pixels
    white_pixel_count = np.sum(thresh_frame == 255)
    return white_pixel_count

framect = 0
lastframe = 0

with P2Pro() as tc:
    with Robot() as r:
        while True:        
            log.debug("Getting frame")
            print(framect, end='')
            thermalframe = tc.imdata  # Read thermal camera data
        
            # Get the dimensions of the frame
            log.debug("Getting frame size")
            height, width, _ = thermalframe.shape
            third_width = width // 3
            
            # Split the frame into three sections
            log.debug("Getting frame size")
            left_section = thermalframe[:, :third_width]
            middle_section = thermalframe[:, third_width:2*third_width]
            right_section = thermalframe[:, 2*third_width:]
            
            # Count white pixels in each section
            log.debug("Counting pixels")
            left_white_pixels = count_white_pixels(left_section)
            middle_white_pixels = count_white_pixels(middle_section)
            right_white_pixels = count_white_pixels(right_section)
            
            # Determine the section with the highest concentration of white pixels
            log.debug("Picking max area")
            max_white_pixels = max(left_white_pixels, middle_white_pixels, right_white_pixels)
            
            log.debug("Find direction")
            if max_white_pixels == left_white_pixels:
                log.debug("Direction was left")
                section_with_most_white = "Left"
                log.debug("Going left")
                r.sendDriveCommand(0,1,0,1)
                print("0 1 0 1", end='')
                #part where you tell robot to turn left

            elif max_white_pixels == middle_white_pixels:
                log.debug("Direction was mid")
                section_with_most_white = "Middle"
                log.debug("Going straight")
                r.sendDriveCommand(1,1,1,1)
                print("1 1 1 1", end='')
                #perhaps move forward or backward based on number of white pixels
                #maybe do a spin move every few cycles to prevent local maximum
                #cv.putText(thermalframe, f"Front wheel 0.2 forward", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            else:
                log.debug("Direction was right")
                section_with_most_white = "Right"
                log.debug("Going right")
                r.sendDriveCommand(1,0,1,0)
                print("1 0 1 0", end='')
                #part where you tell robot to turn right
            
            # Display the result
            log.debug("Render text")
            cv.putText(thermalframe, f"Target: {section_with_most_white}", (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv.LINE_AA)
            
            # Draw vertical red lines to separate the three sections
            log.debug("Render lines")
            cv.line(thermalframe, (third_width, 0), (third_width, height), (0, 0, 255), 2)
            cv.line(thermalframe, (2*third_width, 0), (2*third_width, height), (0, 0, 255), 2)
            
            # Display the thermal frame 
            #cv.imshow("thermal", thermalframe)
            log.debug("Saving image")
            cv.imwrite(f"img/{framect:03d}.png", thermalframe)
            framect += 1
            # Exit on 'q' key press
            # if cv.waitKey(1) == ord('q'):
            #     break
            
            # Wait 1 second
            log.debug("Sleeping")
            time.sleep(0.1)
            ft = time.time() - lastframe
            lastframe = time.time()
            print(f"took {ft:.3f}")

cv.destroyAllWindows()

