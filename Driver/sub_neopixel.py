def ColortoRGB(color):
    r = (color >> 16)
    g = (color >>  8) & 0xFF
    b = (color >> 0) & 0xFF
    return {"red":r,"green":g,"blue":b}