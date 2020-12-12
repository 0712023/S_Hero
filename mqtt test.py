import time
import paho.mqtt.client as mqtt

#callback which is called when client get CONNACK response from server
def on_connect(client, userdata, flags, rc):
    print("Connected with voice ip_/start" + str(rc))
    client.subscribe("/control")

#make first loop to initiate
sign = b'111'

#callback which is called when get PUBLISH message from server
def on_message(client, userdata, msg):
    global sign
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
client = mqtt.Client()

#connect to MQTT server
client.connect("192.168.168.151", 1883)             #voice detector ip address
client.on_connect = on_connect
client.on_message = on_message

#main loop
while True:
    client.loop_start()
    if sign == b'111':
        print('function operating')
    else:
        print('function not operating')
    time.sleep(2)
    client.loop_stop()
