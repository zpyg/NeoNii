import math

from PIL import Image
import numpy as np


def rgb2hex(rgbcolor):
    r, g, b = rgbcolor
    result = (r << 16) + (g << 8) + b
    return hex(result)


def hex2chr(hex):
    code = int(hex, 16)
    return chr(code)


def decode(source, token):
    encoded_img = np.zeros((token, token, 3), dtype=np.uint8)
    target_img = np.array(Image.open(source), dtype=np.uint8)

    target_size = target_img.shape
    sep_x = math.floor(target_size[0] / token)
    sep_y = math.floor(target_size[1] / token)
    tx, ty = 0, 0
    for x in range(token):
        try:
            tx = 0
            for y in range(token):
                encoded_img[x, y] = target_img[tx, ty]
                tx += sep_x
        except:
            pass
        ty += sep_y

    text = ''
    for line in encoded_img:
        for px in line:
            if not any(px): break
            text += hex2chr(rgb2hex(px))
    return text


if __name__ == "__main__":
    with open("dec.txt", 'w', encoding="utf-8") as f:
        f.write(decode("./enc.png", 81))
