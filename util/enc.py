# -*- encoding: utf-8 -*-
from math import ceil, floor
from typing import Dict, Tuple

from numpy import uint8, ndarray
from numpy import array


def chr2rgb(char: str) -> Tuple[int, int, int]:
    """将 字符编码 转换为 rgb"""
    code = ord(char)
    return (code >> 16) & 0xff, (code >> 8) & 0xff, code & 0xff


def txt2img(text: str) -> ndarray:
    """将 文本 转换为 由字符编码对应的色彩组成的图像"""
    # 计算dst的边长
    width = ceil(len(text)**0.5)

    # 遍历文本，将单个字符编码转换为rgb色彩存储
    dst = array([chr2rgb(char) for char in text],
                dtype=uint8)
    # 为保存为图像，必须填充不足
    dst.resize((width, width, 3), refcheck=False)
    return dst


def insert(small_img: ndarray, big_img: ndarray) -> Dict[int, ndarray]:
    """将 小图 均匀插入至 大图

    Args:
      small_img(ndarray)： 源图
      big_img(ndarray): 目标图

    Returns:
      token(int): 用于取出图片
      result(ndarray): 处理结果
    """
    small_shape = small_img.shape
    big_shape = big_img.shape  # y, x
    # 根据大小计算插值间距
    sep_x = floor(big_shape[1] / small_shape[1])
    sep_y = floor(big_shape[0] / small_shape[0])
    # 判断目标图可插值
    assert sep_x and sep_y, "目标图过小"

    #TODO: 更高效率迭代
    big_y = 0
    for small_line in small_img:  # 迭代 y
        big_x = 0
        for small_px in small_line:  # 迭代 x
            big_img[big_y, big_x] = small_px
            big_x += sep_x
        big_y += sep_y
    return {
        # TODO: 更高进制支持, 36(S={数字, 小写字母}), 62(S={数字, 小写字母, 大写字母})
        # TODO: 使token可选
        # 以十六进制存储减少长度
        "token": hex(small_shape[0]),
        "result": big_img
    }


if __name__ == "__main__":
    from PIL import Image
    # Example
    with open("./LICENSE") as f:
        text = f.read()
        ## 直接生成
        enc_default = txt2img(text)
        Image.fromarray(enc_default).save("./out/enc_default.png")
        ## 生成嵌入图
        big_img = array(Image.open("./img/test.jpg"))
        enc_insert = insert(enc_default, big_img)
        Image.fromarray(enc_insert["result"]).save("./out/enc_insert.png")
        print(enc_insert["token"]) # 0xbc
