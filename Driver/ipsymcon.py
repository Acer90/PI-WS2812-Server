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

def ReadColorData(data):
    color = {}
    if data.find(";") == -1:
        color = ReadColorSingelData(data)
    else:
        sdata = data.split(';')
        for value in sdata:
            color.update(ReadColorSingelData(value))
    return color

def ReadColorSingelData(data):
    color = {}   
    if data.find(":") != -1:
        sdata = data.split(':')
        if sdata[0].find("-") != -1:
            v2 = sdata[0].split('-')
            for i in range(int(v2[0]), int(v2[1])):
                if(i >= 0 and i < int(Settings.CONFIG.get('Strip', 'LED_COUNT'))):
                    color.update({i:int(sdata[1])})
        else:
            if(int(sdata[0]) >= 0 and int(sdata[0]) < int(Settings.CONFIG.get('Strip', 'LED_COUNT'))):
                color.update({int(sdata[0]):int(sdata[1])})
              
    return color
