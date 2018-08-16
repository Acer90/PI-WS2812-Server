import sys
import time
import RPi.GPIO as GPIO
from neopixel import *

sys.path.insert(0, './..')
import Settings
from Driver import *
from Driver.lcddriver import lcd


def downWipe(config):
    if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH) # an 
    Settings.POWER_STRIP = True

    if('speed' in config): 
        speed = float(config['speed'])
    else: 
        speed = 500

    wait_ms = float(speed / Settings.STRIP.numPixels())
    colordata = ipsymcon.ReadColorData(config['data'])
        
    for i in range(Settings.STRIP.numPixels(), -1, -1):
        if(i in colordata):
            time1 = time.time()
            c = ipsymcon.ColorToRGB(colordata[i])
            Settings.STRIP.setPixelColor(i, Color(c["red"], c["green"], c["blue"]))
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