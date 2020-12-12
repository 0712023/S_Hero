import picamera
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#signal from infrared light sensor
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

#subscribe from voice rp
def control_connect(client, userdata, flags, rc):
    print("Connected with voice device")
    client.subscribe("/control")

def control_message(client, userdata, msg):
    global sign                                #this code can go up
    sign = msg.payload
    #printing live status
    if sign == b'111':
        print("initiate voice detected")
    elif sign == b'000' :
        print("stop voice detected")

controlsub = mqtt.Client()
controlsub.connect("192.168.0.13", 1883)             #voice detector ip address
controlsub.on_connect = control_connect
controlsub.on_message = control_message

#publish for servo motor rp
servopub = mqtt.Client()
servopub.connect("localhost", 1883)

#publish for server
controlpub = mqtt.Client()
controlpub.connect("localhost",1883)

#make first loop to initiate
sign = b'111'

#mqtt signal unification as b'111'
if sign == '111':
    sign = b'111'

n = 0 #int that make function taken only one time
p = 0 #product number counter
#main loop
while True:
    controlpub.loop_start()
    controlsub.loop_start()
    servopub.loop_start()
    if sign == b'111':
        if GPIO.input(11) == 1: #product not exist in front of camera
            n = 0
        elif GPIO.input(11) == 0: #product exist in front of camera
            n += 1
        if n == 1:
            print('product arrived')
            p += 1
            #function start
            time.sleep(0.5)
            print('start circle detection')
            with picamera.PiCamera() as camera:
                camera.resolution = (640, 480)
                image = np.empty((480, 640, 3), dtype=np.uint8)
                camera.capture(image, 'bgr')
                #start circledetection
                image_gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
                circles = cv.HoughCircles(image_gray, cv.HOUGH_GRADIENT, 1, 40, np.array([]), 50, 190, 100, 120)
                if len(circles.shape) == 3:
                    a, b, c = circles.shape
                    result = "1" #result adequate
                    servopub.publish("/servo", "22") #22 means product is adquate
                    controlpub.publish("/sql", "id=x+timestamp=06/12/2018+topic=1+data=1") #server connection : topic is 1 and data is 1
                else:
                    b = 0
                    result = "0" #result defective
                    servopub.publish("/servo", "33") #33 means product is defective
                    controlpub.publish("/sql", "id=x+timestamp=06/12/2018+topic=1+data=0") #server connection : topic is 1 and data is 0
                for i in range(b):
                    cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
                print(result)
            #save image
            print('saving product picture')
            name = str(p) + '.jpg'
            cv.imwrite(name, image)
            #function end
    controlpub.loop_stop()
    controlsub.loop_stop()
    servopub.loop_stop()
    time.sleep(0.3)
