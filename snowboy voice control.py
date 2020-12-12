import snowboydecoder
import sys
import signal
import paho.mqtt.client as mqtt
import serial
import time

#arduino serial function
ser = serial.Serial('/dev/rfcomm0', 9600, timeout = 1)

#create mqtt client object(voice detector ip address)
mqtt = mqtt.Client()
mqtt.connect("localhost", 1883)

interrupted = False

def signal_handler(signal, frame):
    global interrupted
    interrupted = True

def interrupt_callback():
    global interrupted
    return interrupted

models = sys.argv[1:]

# capture SIGINT signal, e.g., Ctrl+C
signal.signal(signal.SIGINT, signal_handler)

sensitivity = [0.5]
detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)

def callback1():
    mqtt.publish("/control", "111")
    ser.write(str.encode('1'))

def callback2():
    mqtt.publish("/control", "000")
    ser.write(str.encode('0'))

mqtt.loop(2)                      #timeout 2 sec

callbacks = [callback1, callback2]

# main loop
detector.start(detected_callback=callbacks, interrupt_check=interrupt_callback, sleep_time=0.03)

detector.terminate()
