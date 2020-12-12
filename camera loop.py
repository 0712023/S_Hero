import picamera
import numpy as np
import cv2 as cv

with picamera.PiCamera() as camera:
    camera.resolution = (320, 240)
    camera.framerate = 24
    image = np.empty((240, 320, 3), dtype=np.uint8)
    camera.capture(image, 'bgr')

    #start circledetection
    image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    circles = cv.HoughCircles(image_gray, cv.HOUGH_GRADIENT, 1, 20, np.array([]), 50, 60, 20, 30)
    if circles is not None:
        if len(circles.shape) == 3:
            a, b, c = circles.shape
            print("circles are detected") #adequate product
            group = "adequate"
        else:
            b = 0
            print("circles not detected") #defective product
            group = "defective"
        for i in range(b):
            cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)

#save result at log.txt
log = open('/home/pi/workspace/file write/product log.txt', "a")
log.write("\nproduct is " + group)
log.close()

#save image
cv.imwrite('product.jpg', image)
cv.destroyAllWindows()
