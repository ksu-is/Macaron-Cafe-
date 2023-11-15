"""
this project is coded on python using numpy,opencv and a user defined library named conveyor_lib.py
for automatic stopping of the conveyor belt we require a webcam , raspberry pi ,a conveyor_belt and
a relay attached to it(to turn on and off the conveyor belt),as well as some nuts of a particularly different color
than the conveyor belt.
here the conveyor belt is connected to the relay which inturn is connected to the raspberry pi
In this prototype we have taken a black colored conveyor belt and silvered colored nuts for auto detection based on size
this project auto stops the belt(relay) whenever it detects the object(nuts) having size greater than the
 particular size (input in the programme)
"""

import cv2
import numpy as np
import conveyor_lib

cap = cv2.VideoCapture(0) # 0 is the first webcam if we have more webcam use 1,2... as index

# importing a custom library named Conveyor belt library conveyor_lib.py
relay = conveyor_lib.Conveyor()

while True:
    _, frame = cap.read() #

    # ROI (Belt)
    belt = frame[205: 329, 130: 281] # top right coordinates x,y=130,205 & bottom left x1,y1= 281,329

    """as we are using OpenCV in raspberry pi the co-ordinates of the mouse are visible
    and since we want only a particular portion of the frame to detect the sizes
    we will crop the frame having dimensions written above"""

    gray_belt = cv2.cvtColor(belt, cv2.COLOR_BGR2GRAY) #converting the frame to grayscale format
    _, threshold = cv2.threshold(gray_belt, 85, 255, cv2.THRESH_BINARY) #we want to apply threshold to the gray_belt

    '''here we are converting all the dark color like black and close to it into black color and 
    light colors like silver will get converted to white'''

    # Detection of the Nuts
    _, contours, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt) #contains a lot of coordinates representing the boundaries of each object

        # Calculate area to distinguish the objects based upon area
        area = cv2.contourArea(cnt)

        # Distinguish small and big nuts
        if area > 400:
            # these are big nuts
            cv2.rectangle(belt, (x, y), (x + w, y + h), (0, 0, 255), 2) # to make the rectangle blue and of 2 pixels

            # it will atomatically Stop the belt
            relay.turn_off()

        elif 100 < area < 400:
            cv2.rectangle(belt, (x, y), (x + w, y + h), (255, 0, 0), 2) #to make the bigger rectangle look red

        cv2.putText(belt, str(area), (x, y), 1, 1, (0, 255, 0)) #typecasting of area(number) into string format

    cv2.imshow("Frame", frame) # to show the frame on the screen
    cv2.imshow("belt", belt)
    cv2.imshow("threshold", threshold)

    key = cv2.waitKey(1) #to wait for 1 millisecond between each frame
    if key == 27:  # 27 is ASCII Code for esc button on keyboard
        break
    elif key == ord("n"): #pressing key 'n' on keyboard to switchon the belt
        relay.turn_on()
    elif key == ord("m"): #pressing key 'm' on the keyboard to turn off the belt
        relay.turn_off()

cap.release()  #to release the camera as we break the loop
cv2.destroyAllWindows() #to close all the windows as they are not going to get closed themselves automatically