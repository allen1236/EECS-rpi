from picamera.array import PiRGBArray
from picamera       import PiCamera
from matplotlib import pyplot as plt
from collections import deque
from imutils.video import VideoStream
import numpy as np
import imutils
import time
import cv2
import sys

maskLower = ( 0, 0, 0 )
maskUpper = ( 0, 0, 255 )
pts = deque(maxlen=10) 

cam = PiCamera()
cam.resolution = (320, 240)
cam.framerate = 30
raw = PiRGBArray( cam, size=(320, 240) )
time.sleep( 1 ) # camera warm up
cam.start_preview()

for frameBGR in cam.capture_continuous( raw, format="bgr", use_video_port=True ):
    frame = frameBGR.array

    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV) 

    mask = cv2.inRange(hsv, maskLower, maskUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2) 

    # find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    center = None 

    # only proceed if at least one contour was found
    if len(cnts) > 0:

        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        print( x, y )
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        # only proceed if the radius meets a minimum size
        if radius > 10:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, center, 5, (0, 0, 255), -1)
    else:
        print( 'nothing found' )
 
    # update the points queue
    pts.appendleft(center) 
    # loop over the set of tracked points
    for i in range(1, len(pts)):
        # if either of the tracked points are None, ignore
        # them
        if pts[i - 1] is None or pts[i] is None:
            continue

        # otherwise, compute the thickness of the line and
        # draw the connecting lines
        #thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), 10)

    # Display the resulting frame

    #TODO: cannot use this function in rpi
    cv2.imshow('frame',frame)

    #cv2.imshow('frame',mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


    raw.truncate(0) #clear the buffer
