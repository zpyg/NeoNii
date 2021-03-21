# -*- encoding: utf-8 -*-
import math
import numpy as np
from PIL import Image


def hex2rgb(hexcolor):
    hexcolor = int(hexcolor, base=16)
    rgb = ((hexcolor >> 16) & 0xff, (hexcolor >> 8) & 0xff, hexcolor & 0xff)
    return rgb


def chr2hex(char):
    code = ord(char)
    hex_ = hex(code)[2:]
    return hex_.zfill(6)


def encode(source, text):
    str_len = len(text)
    width = math.ceil(str_len**0.5)
    encoded_img = np.array([hex2rgb(chr2hex(char)) for char in text],
                           dtype=np.uint8)
    encoded_img.resize((width, width, 3))
    target_img = np.array(Image.open(source), dtype=np.uint8)

    encoded_size = encoded_img.shape
    target_size = target_img.shape
    sep_x = math.floor(target_size[0] / encoded_size[0])
    sep_y = math.floor(target_size[1] / encoded_size[1])

    print("token: ", width)
    tx, ty = 0, 0
    for line in encoded_img:
        tx = 0
        for px in line:
            if tx >= target_size[0]: continue
            target_img[tx, ty] = px
            tx += sep_x
        ty += sep_y
    return Image.fromarray(target_img)


if __name__ == "__main__":
    with open("./狂人日记.txt", encoding="utf-8") as f:
        encode("./img/source.jpg", f.read()).save("./enc.png")
