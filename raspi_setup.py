import RPi.GPIO as GPIO
import time
import azure_setup
import fcm_server
import subprocess
from datetime import datetime

# Pins usados por lcd: 7,8,25,24,23,18
# Pins que quieres usar
presence = 4
button = 17
led = 26

def my_callback(presence):
    print "\nPresence detected. Uploading image"
    subprocess.check_call(["fswebcam", "--no-banner", "imagen.jpg"])
    date = datetime.now()
    azure_setup.upload(date, "imagen.jpg")
    subprocess.check_call(["rm", "imagen.jpg"])
    print "\nSending Presence notification"
    fcm_server.send_notification(fcm_server.token, "SecuredHome.Presence detected!", azure_setup.base_url+date)


def light():
    GPIO.output(led, 1)
    time.sleep(3)
    GPIO.output(led, 0)
    print "LIGHT!"

def setup():

    # No physical numeration
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(presence, GPIO.IN)
    # When it is not connected, it detects 0 (Pull down).
    GPIO.setup(presence, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(button, GPIO.IN)
    GPIO.setup(button, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.setup(led, GPIO.OUT)

    # https://sourceforge.net/p/raspberry-gpio-python/wiki/Inputs/
    # Sensor de presencia. Delay 3s - 5mins (3s actualmente)
    # GPIO.add_event_detect(presence, GPIO.RISING, callback=my_callback)
    print "\nGPIO Set"