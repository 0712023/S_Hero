# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2 as cv
import numpy as np

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

# allow the camera to warmup
time.sleep(0.1)

n = 0
m = 0
l = 0

# capture frames from the camera
for frame in camera.capture_continuous(rawCapture, format='bgr', use_video_port=True):
	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
    img = frame.array
    image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    if signal == 1:
        n = n + 1
        if n == 1:
            l = l + 1
            name = print('product' + l)
            cv.imwrite(name, img)
        else:
            break

	    # show the frame
        circles = cv.HoughCircles(image, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 60, 20, 30)
        if circles is not None:
            if len(circles.shape) == 3:
                a, b, c = circles.shape
                m = m + 1
            else:
                b = 0
            for i in range(b):
                cv.circle(img, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
            cv.imshow("tracking", img)
            key = cv.waitKey(1)

	        # clear the stream in preparation for the next frame
            rawCapture.truncate(0)

	        # if the `esc` key was pressed, break from the loop
            if key == 27:
                break
        cv.destroyAllWindows()
    else:
        if m / n > 0.9:
            n = 1
        else:
            k = 0
        n = 0

        continue
