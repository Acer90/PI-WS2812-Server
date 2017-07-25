import sys
import time
import threading
import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver import *
from Driver.lcddriver import lcd


def out2inWipe (config):
    if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
    Settings.POWER_STRIP = True

    if('speed' in config): 
        speed = float(config['speed'])
    else: 
        speed = 500

    wait_ms = float(speed / (Settings.STRIP.numPixels() / 2))
    colordata = ipsymcon.ReadColorData(str(config['data']))

    if Settings.STRIP.numPixels() % 2: #ungrade 
        half = (Settings.STRIP.numPixels() - 1) / 2
        startp = 0
        startm = Settings.STRIP.numPixels() - 1
    else: #grade 
        half = (Settings.STRIP.numPixels() - 1) / 2
        startp = 0
        startm = Settings.STRIP.numPixels() - 1
        
    for i in range((half +1)):
        time1 = time.time()
        pixel1 = startp + i
        pixel2 = startm - i
        change = False

        if(pixel1 in colordata):
            c = ipsymcon.ColorToRGB(colordata[pixel1])
            Settings.STRIP.setPixelColor(pixel1, Color(c["red"], c["green"], c["blue"]))
            change = True


        if(pixel2 in colordata and pixel1 != pixel2):
            c = ipsymcon.ColorToRGB(colordata[pixel2])
            Settings.STRIP.setPixelColor(pixel2, Color(c["red"], c["green"], c["blue"]))
            change = True

        if (change == True):
            Settings.STRIP.show()
            time2 = time.time()
            span = time2-time1
            #print("%s seconds"%(span))
            wtime = (wait_ms/1000) - float(span)
            
            if(wtime > 0):
                time.sleep(wtime)

    if(int(Settings.CONFIG.get('Relais', 'GPIO'))> 0 and config['cmd'] == "stop"):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.LOW) 
    Settings.POWER_STRIP = False
