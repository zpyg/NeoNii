# -*- encoding: utf-8 -*-
from math import floor
from typing import Tuple

from numpy import uint8, ndarray
from numpy import array, zeros


def rgb2chr(rgb: Tuple[int, int, int]) -> str:
    """将 rgb 转换为 字符"""
    r, g, b = rgb
    code = (r << 16) + (g << 8) + b
    return chr(code)


def img2txt(img: ndarray) -> str:
    """将 图片 转换为 文本"""
    text_arr = [rgb2chr(px)  # 将像素转为字符
            for line in img  # 迭代 y
            for px in line  # 迭代 x
            if any(px)  # 过滤填充的像素
        ]
    return ''.join(text_arr)


def fetch(big_img: ndarray, token: int) -> ndarray:
    """将大图中的小图取出

    Args:
      big_img(ndarray): 大图
      token(int): 即小图的边长
    """
    # 初始化原图
    small_img = zeros((token, token, 3), dtype=uint8)

    src_shape = big_img.shape  # y, x
    sep_x = floor(src_shape[1] / token)
    sep_y = floor(src_shape[0] / token)

    big_y = 0
    for small_y in range(token):
        big_x = 0
        for small_x in range(token):
            small_img[small_y, small_x] = big_img[big_y, big_x]
            big_x += sep_x
        big_y += sep_y
    return small_img


if __name__ == "__main__":
    from PIL import Image
    # Example
    ## 解码默认
    img = array(Image.open("./out/enc_default.png"))
    dec_default = img2txt(img)
    ## 解码嵌入
    token = 0xbc
    big_img = array(Image.open("./out/enc_insert.png"))
    dec_insert = fetch(big_img, token)
