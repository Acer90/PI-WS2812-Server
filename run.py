#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
from Driver.lcddriver import lcd
import RPi.GPIO as GPIO
from neopixel import *
from Scripts import *
import Server
import Settings

sys.path.append("pycharm-debug-py3k.egg")

print('Initialized Settings')
Settings.init()

#Disable LCD
status_lcd = lcd()
status_lcd.backlight_off()

# GPIO Nummern statt Board Nummern
GPIO.setmode(GPIO.BCM)

#Relai zuweisen
if(int(Settings.CONFIG.get('Relais','GPIO'))>0):
    RELAIS_GPIO=int(Settings.CONFIG.get('Relais', 'GPIO'))
    GPIO.setwarnings(False)
    GPIO.setup(RELAIS_GPIO, GPIO.OUT) # GPIO Modus zuweise
    GPIO.output(RELAIS_GPIO, GPIO.LOW) # aus


# LED strip configuration:
LED_COUNT = int(Settings.CONFIG.get('Strip', 'LED_COUNT'))     # Number of LED pixels.
LED_PIN = int(Settings.CONFIG.get('Strip', 'LED_PIN'))      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = int(Settings.CONFIG.get('Strip', 'LED_FREQ_HZ'))  # LED signal frequency in hertz (usually 800khz)
LED_DMA = int(Settings.CONFIG.get('Strip', 'LED_DMA'))  # DMA channel to use for generating signal (try 5)
LED_BRIGHTNESS = int(Settings.CONFIG.get('Strip', 'LED_BRIGHTNESS')) # Set to 0 for darkest and 255 for brightest
LED_INVERT = eval(Settings.CONFIG.get('Strip', 'LED_INVERT')) # True to invert the signal (when using NPN transistor level shift)

Settings.STRIP = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)
Settings.STRIP.begin()

def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, color)
            strip.show()
            time.sleep(wait_ms/1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)

theaterChase(Settings.STRIP, Color(0, 0, 255), 100, 1)
thread_SocketServer = Server.SocketServer()
thread_SocketServer.daemon = True
thread_SocketServer.start()

print('Initialized Complete')
Settings.INIT_COMPLETE = True

try:
    raw_input("Press Enter to Close...")
except (KeyboardInterrupt, SystemExit):
    print ('Stop Server!!!')

thread_SocketServer._Thread__stop()
if(Settings.thread_Programs.is_alive()):
    Settings.thread_Programs.terminate()
sys.exit(1)

Settings.EXIT = True