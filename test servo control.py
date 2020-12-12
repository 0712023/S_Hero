import time
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO

#callback which is executed when get CONNTACK response from server
def on_connect(client, userdata, flags, rc):
    print("connected with result code "+str(rc))
    client.subscribe("/servo") #subscribe "nodemcu"

    #callback which is executed when get publish message from server
def on_message(client, userdata, msg):
    global sign
    sign = msg.payload

client = mqtt.Client()                      #create client object
client.on_connect = on_connect      #set callback
client.on_message = on_message #set callback
client.connect("192.168.0.3", 1883)

GPIO.setmode(GPIO.BOARD) #BCM or board
GPIO.setup(11, GPIO.IN)

data_saved = []

sign = 0
n = 1
m = 0 # whether product is in front of servo motor
while True :
    client.loop_start()
    if sign != None:
        data_saved.append(sign)
        sign = None
    if m == 0:
        if GPIO.input(11) == 0:
            if data_saved[n] == b'44':#product is defective
                print("product is defective")
            elif data_saved[n] == b'33':#product is adequate
                print("product is adequate")
            print(data_saved)
            n +=1
            m = 1
            time.sleep(0.25)
    if GPIO.input(11) == 1: #non-detected
        m = 0
        time.sleep(0.25)
    client.loop_stop()
