import picamera
import numpy as np
import cv2 as cv

print('start circle detection')
with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.framerate = 24
    image = np.empty((480, 640, 3), dtype=np.uint8)
    camera.capture(image, 'bgr')
    #start circledetection
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(image_gray, cv.HOUGH_GRADIENT, 1, 40, np.array([]), 50, 150, 100, 120)
    if len(circles.shape) == 3:
        a, b, c = circles.shape
    else:
        b = 0
    for i in range(b):
        cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
    cv.imshow("image", image)
    key = cv.waitKey(0)
    if key == 27:
        cv.destroyAllWindows()
