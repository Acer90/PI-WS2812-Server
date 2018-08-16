import sys
import time

import RPi.GPIO as GPIO
from neopixel import *
from math import floor

sys.path.insert(0, './..')
import Settings
from Driver import *
from Driver.lcddriver import lcd


def fadeStep4Step(config, strip):
    if(not Settings.POWER_STRIP and int(Settings.CONFIG.get('Relais', 'GPIO'))> 0):
        GPIO.output(int(Settings.CONFIG.get('Relais', 'GPIO')), GPIO.HIGH)#an
    Settings.POWER_STRIP = True

    if('speed' in config): 
        speed = float(config['speed'])
    else: 
        speed = 500

    wait_ms = 50
    steps = float(speed / wait_ms)
    colordata = ipsymcon.ReadColorData(config['data'])
    dif = 0
    diflist = {}

    for i in range(strip.numPixels()):
        if(i in colordata):
            c1 = ipsymcon.ColorToRGB(colordata[i])
            c2 = sub_neopixel.ColortoRGB(strip.getPixelColor(i))

            r_dif = c1["red"] - c2["red"]
            g_dif = c1["green"] - c2["green"]
            b_dif = c1["blue"] - c2["blue"]

            diflist[i] = {}
            diflist[i]["red"] = r_dif / steps
            diflist[i]["green"] = g_dif / steps
            diflist[i]["blue"] = b_dif / steps

            diflist[i]["startR"] = c2["red"]
            diflist[i]["startG"] = c2["green"]
            diflist[i]["startB"] = c2["blue"]

            if(r_dif > dif): dif = r_dif
            if(g_dif > dif): dif = g_dif
            if(b_dif > dif): dif = b_dif

            if((r_dif * -1) > dif): dif = (r_dif * -1)
            if((g_dif * -1) > dif): dif = (g_dif * -1)
            if((b_dif * -1) > dif): dif = (b_dif * -1)

    for s in range(1, int(floor(steps + 1))):
        time1 = time.time()
        for i in range(strip.numPixels()):
            if(i in colordata):
                new_r = diflist[i]["startR"] + (s * diflist[i]["red"])
                new_g = diflist[i]["startG"] + (s * diflist[i]["green"])
                new_b = diflist[i]["startB"] + (s * diflist[i]["blue"])

                strip.setPixelColor(i, Color(int(floor(new_r)), int(floor(new_g)), int(floor(new_b))))
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