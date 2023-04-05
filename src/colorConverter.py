import colorsys


def HEXtoRGB(hexCode):
    rgb = []
    if hexCode.startswith('#'):
        hexCode = hexCode[1:]
    for i in (0, 2, 4):
        decimal = int(hexCode[i:i + 2], 16)
        rgb.append(decimal)
    return tuple(rgb)


def RGBtoHEX(r, g, b):
    return '#{:02x}{:02x}{:02x}'.format(round(r), round(g), round(b))


def HSBtoRGB(h, s, b):
    result = colorsys.hsv_to_rgb(h / 360, s / 100, b / 100)
    return [item * 255 for item in result]


def HSLtoRGB(h, s, l):
    result = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return [item * 255 for item in result]


def RGBtoHSB(r, g, b):
    result = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)
    return round(result[0] * 360), round(result[1] * 100), round(result[2] * 100)


def RGBtoHSL(r, g, b):
    result = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)
    return round(result[0] * 360), round(result[2] * 100), round(result[1] * 100)


def HEXtoHSB(hexCode):
    return RGBtoHSB(*HEXtoRGB(hexCode))


def HSBtoHEX(h, s, b):
    return RGBtoHEX(*HSBtoRGB(h, s, b))


def HEXtoHSL(hexCode):
    return RGBtoHSL(*HEXtoRGB(hexCode))


def HSLtoHEX(h, s, l):
    return RGBtoHEX(*HSLtoRGB(h, s, l))