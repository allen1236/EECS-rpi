from picamera.array import PiRGBArray
from picamera       import PiCamera
from matplotlib import pyplot as plt
import time
import cv2
import sys

cam = PiCamera()
cam.resolution = (320, 240)
cam.framerate = 30
raw = PiRGBArray( cam, size=(320, 240) )
time.sleep( 1 ) # camera warm up
cam.start_preview()

for frameBGR in cam.capture_continuous( raw, format="bgr", use_video_port=True ):
    imgBGR = frameBGR.array
    imgRGB = imgBGR[:,:,::-1]
    print( imgRGB.shape )
    raw.truncate(0) #clear the buffer
