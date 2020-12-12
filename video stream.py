from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import numpy as np

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
    img = frame.array
    rows, cols = img.shape[:2]
    rotate = cv.getRotationMatrix2D((cols/2, rows/2),180, 1)
    rotateimage = cv.warpAffine(img, rotate,(cols, rows))
    cv.imshow("my room", rotateimage)
    key = cv.waitKey(1)
    rawCapture.truncate(0)
    if key == 27:
        break
cv.destroyAllWindows()
