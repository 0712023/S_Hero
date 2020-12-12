import cv2 as cv
import numpy as np
from picamera import PiCamera
from time import sleep
import video

camera = PiCamera()

for i in range(1, 3):
    sleep(3)
    camera.capture('/home/pi/1. workspace/coding/product%s.jpg' % i)
#start capturing pictures and save

    name = 'product' + str(i) + '.jpg'
#image name is 'product#.jpg'
    img1 = cv.imread(name, 0)
    img1 = cv.medianBlur(img1, 5)
    img2 = img1.copy()

    circles = cv.HoughCircles(img1, cv.HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30)
    if circles is not None:
        if len(circles.shape) < 3:
            print('circles not detected')
            break
        else:
            a, b, c = circles.shape
        for j in range(b):
            cv.circle(img3, (circles[0][j][0], circles[0][j][1]), circles[0][j][2], (0, 0, 255), 3, cv.LINE_AA)
    cv.namedWindow('detected circles', cv.WINDOW_NORMAL)
    cv.imshow("detected circles", img2)
    print('r = ',circles[0][j][2])
    ch = cv.waitKey(0)
    if ch == 27:
        break
cv.destroyAllWindows()
