import picamera
import numpy as np
import cv2 as cv
import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.IN)

#callback which is called when client get CONNACK response from server
def control_connect(client, userdata, flags, rc):
    print("Connected with voice ip_/start" + str(rc))
    client.subscribe("/control")

#callback which is called when get PUBLISH message from server
def control_message(client, userdata, msg):
    global sign                                         #this code can go up
    sign = msg.payload
    #printing live status
    if sign == b'111':
        print("initiate detected_b\n")
    elif sign == '111':
        print("initiate detected_0\n")
    elif sign == b'000' :
        print("stop detected_b\n")
    elif sign == '000' :
        print("stop detected_0\n")

#Create MQTT Client object
controlsub = mqtt.Client()

#connect to MQTT server
controlsub.connect("192.168.0.13", 1883)             #voice detector ip address
controlsub.on_connect = control_connect
controlsub.on_message = control_message

servopub = mqtt.Client()
servopub.connect("localhost", 1883)

controlpub = mqtt.Client()                         #send conveyor state to server
controlpub.connect("localhost",1883)

#Arduino serial communication

#make first loop to initiate
sign = b'111'

#mqtt signal unification as b'111'
if sign == '111':
    sign = b'111'

n = 0 #int that make function taken only one time
p = 0 #product number counter
m = 0
#main loop
while True:
    controlpub.loop_start()
    controlsub.loop_start()
    servopub.loop_start()
    if sign == b'111':
        controlpub.publish("/conveyorstate", "111111")
        if m == 0:
            if GPIO.input(11) == 0:
                n += 1
                if n == 1:
                    p += 1
                    #function start
                    print('start circle detection')
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
                                group = "1"#adequate
                                servopub.publish("/servo", "22")          #same string size, 22222222 means product is adquate
                            else:
                                b = 0
                                group = "0"#defective
                                servopub.publish("/servo", "33")          #same string size, 33333333 means product is defective
                            for i in range(b):
                                cv.circle(image, (circles[0][i][0], circles[0][i][1]), circles[0][i][2], (0, 0, 255), 3, cv.LINE_AA)
                    #save result at log.txt
                    print('saving result')
                    p1 = str(p)
                    log = open('/home/pi/coding/product_result/results.txt', "a")
                    log.write('product' + p1 + ' is ' + group + '\n')
                    log.close()
                    #save image
                    print('saving product picture')
                    name = p1 + '.jpg'
                    cv.imwrite(name, image)
                    cv.destroyAllWindows()
                    #function end
        else:
            n = 0
        if GPIO.input(11) == 1:
            m = 0
            time.sleep(0.25)
    controlpub.publish("/conveyorstate", "000000")
    time.sleep(1)
    controlpub.loop_stop()
    controlsub.loop_stop()
    servopub.loop_stop()
