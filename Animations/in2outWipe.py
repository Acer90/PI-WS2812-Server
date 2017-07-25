import sys
import time

import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver import *
from Driver.lcddriver import lcd

def in2outWipe(config, strip):
    if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
    Settings.POWER_STRIP = True

    if('speed' in config): 
        speed = float(config['speed'])
    else: 
        speed = 500

    wait_ms = float(speed / (strip.numPixels() / 2))
    colordata = ipsymcon.ReadColorData(str(config['data']))

    if strip.numPixels() % 2: #ungrade 
        half = (strip.numPixels() - 1) / 2
        startp = half
        startm = half
    else: #grade 
        half = (strip.numPixels() - 1) / 2
        startp = half + 1
        startm = half
        
    for i in range(half):
        time1 = time.time()
        pixel1 = startp + i
        pixel2 = startm - i
        change = False

        if(pixel1 in colordata):
            c = ipsymcon.ColorToRGB(colordata[pixel1])
            strip.setPixelColor(pixel1, Color(c["red"], c["green"], c["blue"]))
            change = True

        if(pixel2 in colordata and pixel1 != pixel2):
            c = ipsymcon.ColorToRGB(colordata[pixel2])
            strip.setPixelColor(pixel2, Color(c["red"], c["green"], c["blue"]))
            change = True

        if (change == True):
            strip.show()
            time2 = time.time()
            span = time2-time1
            #print("%s seconds"%(span))
            wtime = (wait_ms/1000) - float(span)
            
            if(wtime > 0):
                time.sleep(wtime)
                

    if(int(Settings.CONFIG.get('Relais', 'GPIO'))> 0 and config['cmd'] == "stop"):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.LOW) 
    Settings.POWER_STRIP = False