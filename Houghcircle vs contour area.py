import cv2 as cv
import numpy as np

img1 = cv.imread('example.jpg', 0)
img1 = cv.medianBlur(img1,5)
img2 = img1.copy

circles = cv.HoughCircles(img1, cv.HOUGH_GRADIENT, 1, 10, np.array([]), 100, 30, 1, 30)
if circles is not None:
    if len(circles.shape) < 3:
        print('circles not detected')
    else:
        a, b, c = circles.shape
    for j in range(b):
        cv.circle(img3, (circles[0][j][0], circles[0][j][1]), circles[0][j][2], (0, 0, 255), 3, cv.LINE_AA)
print('expected area = ', 3.14*circles[0][j][2]**2)

ret, th = cv.threshold(img1, 150, 255, cv.THRESH_BINARY)
image, contours, hierarchy = cv.findContours(th, 1, 2)
img3 = cv.drawContours(img1, contours, -1 (0, 255, 0), 3)
area = cv.contourArea(contours[0])
print('real area = ', area)
