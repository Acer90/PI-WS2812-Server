import sys
import time
from math import floor

sys.path.insert(0, './../..')
import Settings

def ColorToRGB(color):
    r = int(floor(color / 65536))
    b = int(floor((color-(r * 65536)) / 256))
    g = int(color-(b * 256)-(r * 65536))
    #print (str(r)+ "|" +str(g) + "|" + str(b))
    w = {"red":r ,"green":g ,"blue":b}
    return w

def RGBToColor(r, g, b):
    color = (r*256*256)+(g*256)+b
    return color

def ReadColordata(data):
    color = {}
    for singledata in data:

        colorcode = 0
        from_led = 0
        to_led = int(Settings.CONFIG.get('Strip', 'LED_COUNT'))

        if ("color" in singledata): colorcode = singledata["color"]
        if ("from" in singledata): from_led = singledata["from"]
        if ("to" in singledata and singledata["to"] < int(Settings.CONFIG.get('Strip', 'LED_COUNT'))): to_led = singledata["to"]

        for i in range(int(from_led), int(to_led)):
            #print("led=" + str(i) + " | color=" + str(colorcode))
            color.update({i: int(colorcode)})
    return color
