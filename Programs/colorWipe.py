import sys
import time
import threading
from thread import *
import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver import *
from Driver.lcddriver import lcd

class colorWipe (threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        
    def run(self, name, config):
        if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
            GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
        Settings.POWER_STRIP = True

        if('wait' in config): 
            wait_ms = int(config['wait']) 
        else: 
            wait_ms = 50

        if('color' in config): 
            colors = ipsymcon.ColorToRGB(int(config['color'])) 
            color = Color(colors["red"], colors["green"], colors["blue"])
        else: 
            color = Color(0, 0, 255)

        if('wait' in config): 
            iterations = int(config['iterations']) 
        else: 
            iterations=1
        
        while 1:
            for i in range(Settings.STRIP.numPixels()):
                Settings.STRIP.setPixelColor(i, color)
                Settings.STRIP.show()
                time.sleep(wait_ms/1000.0)

    def stop(self):
        self.stopped = True