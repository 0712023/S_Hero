import time
import paho.mqtt.client as mqtt

#callback which is called when client get CONNACK response from server
def control_connect(client, userdata, flags, rc):
    print("Connected with voice ip_/start" + str(rc))
    client.subscribe("/control")

#make first loop to initiate
sign = b'111'

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
controlsub.connect("203.252.47.59", 1883)             #voice detector ip address
controlsub.on_connect = control_connect
controlsub.on_message = control_message

servopub = mqtt.Client()
servopub.connect("localhost", 1883)

#main loop
while True:
    controlsub.loop_start()
    servopub.loop_start()
    if sign == b'111':
        print('function operating')
        servopub.publish("/servo", "11111111")          #same string size
    else:
        print('function not operating')
        servopub.publish("/servo", "disadqua")
    time.sleep(2)
    controlsub.loop_stop()
    servopub.loop_stop()
