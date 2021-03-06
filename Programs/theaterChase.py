import sys
import time

import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver.lcddriver import lcd
        
def theaterChase(config, strip):
        if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
            GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
        Settings.POWER_STRIP = True

        wait_ms=50
        color = Color(0, 0, 255)
        iterations=10
        
        while 1:
            for j in range(iterations):
                for q in range(3):
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, color)
                    strip.show()
                    time.sleep(wait_ms/1000.0)
                    for i in range(0, strip.numPixels(), 3):
                        strip.setPixelColor(i+q, 0)