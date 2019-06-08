from picamera.array import PiRGBArray
from picamera       import PiCamera
import time
import cv2
import sys

cam = PiCamera()
cam.resolution = (320, 240)
cam.framerate = 30
raw = PiRGBArray( cam, size=(320, 240) )
time.sleep( 1 )
for frameBGR in cam.capture_continuous( raw, format="bgr", use_video_port=True ):
    imgBGR = frameBGR.array

    plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
    plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    plt.show() 

    key = cv2.waitKey(1) & 0xFF
    raw.truncate(0)
    if key == ord( "q" ):
        break
