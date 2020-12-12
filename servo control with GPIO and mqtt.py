import serial
import time
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt

#callback which is executed when get CONNTACK response from server
def on_connect(client, userdata, flags, rc):
    print("connected with camera device")
    client.subscribe("/servo") #subscribe "nodemcu"

    #callback which is executed when get publish message from server
def on_message(client, userdata, msg):
    global signal
    signal = msg.payload


client = mqtt.Client()                      #create client object
client.on_connect = on_connect      #set callback
client.on_message = on_message #set callback
client.connect("192.168.0.3", 1883)

GPIO.setmode(GPIO.BOARD) #BCM or board
GPIO.setup(11, GPIO.IN)

ser = serial.Serial('/dev/ttyUSB0', 9600) #check USB list

data_saved = []
signal = 0
n = 1
m = 0 # whether product is in front of servo motor
while True :
    client.loop_start()
    if signal != None:
        data_saved.append(signal)
        signal = None
    if GPIO.input(11) == 1:
        m = 0
    elif GPIO.input(11) == 0:
        m += 1
        print(m)
    if m == 1:
        print(data_saved)
        if data_saved[n] == b'33':#product is defective
            ser.write('2'.encode())
            print("unsatisified")
        elif data_saved[n] == b'22':#product is adequate
            print("satisfied")
        n += 1
        time.sleep(0.25)
    client.loop_stop()
