import picamera
import numpy as np
import cv2 as cv
from pyfirmata import Arduino, util
import time

board = Arduino('/dev/ttyUSB0')
pin9_sensor = board.get_pin('d:9:i')
it = util.Iterator(board)
it.start()
pin9_sensor.enable_reporting

pin_code = pin9_sensor

n = 0 #int that make function taken only one time
m = 0 #control int from voice detection
p = 0
while True:
    if m == 0:
        if pin_code.read() == False:
            n = n + 1
            if n == 1:
                p = p + 1
                #function start
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
                            group = "adequate"
                        else:
                            b = 0
                            group = "defective"
                        for i in range(b):
                            cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
                #save result at log.txt
                p1 = str(p)
                log = open('/home/pi/product log.txt', "a")
                log.write('\nproduct' + p1 + ' is ' + group)
                log.close()

                #save image
                name = 'product' + p1 + '.jpg'
                cv.imwrite(name, image)
                cv.destroyAllWindows()
                #function end
        else:
            n = 0
        time.sleep(2)
