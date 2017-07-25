import sys
import time
import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver.lcddriver import lcd

def theaterChaseRainbow(config):
    if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
    Settings.POWER_STRIP = True

    wait_ms=50 
        
    while 1:
        for j in range(256):
            for q in range(3):
                for i in range(0, Settings.STRIP.numPixels(), 3):
                    Settings.STRIP.setPixelColor(i+q, wheel((i+j) % 255))
                Settings.STRIP.show()
                time.sleep(wait_ms/1000.0)
                for i in range(0, Settings.STRIP.numPixels(), 3):
                    Settings.STRIP.setPixelColor(i+q, 0)


def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)
