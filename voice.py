#python3 demo.py resources/models/snowboy.umdl
#snowboydecoer.py must be at the same path with initiate.py

import snowboydecoder
import sys
import signal

interrupted = False

#interrupted destroy the main loop
def signal_handler(signal, frame):
    global interrupted
    interrupted = True

#callback function when interrupted
def interrupt_callback():
    global interrupted
    return interrupted

#error detect. if there is no errer, delete below code
if len(sys.argv) == 1:
    print("Error: need to specify model name")
    print("Usage: python demo.py your.model")
    sys.exit(-1)
######################################################

#resource from command line
model = sys.argv[1]

# interrupting signal is 'Ctrl + V'
signal.signal(signal.SIGINT, signal_handler)

#define hotword detecting function
detector = snowboydecoder.HotwordDetector(model, sensitivity=0.5)

#define callback function
def callback():
    log = open('/home/pi/test.txt', "a")
    log.write("start function\n")
    log.close()

# main loop
detector.start(detected_callback=callback,
               interrupt_check=interrupt_callback,
               sleep_time=0.03)

detector.terminate()
