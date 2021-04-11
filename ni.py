#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
from sys import argv
from argparse import ArgumentParser
from pathlib import Path

from PIL import Image

from util import enc, dec


args = argv[1::]
parser = ArgumentParser()
subparsers = parser.add_subparsers(required=True)

encode = subparsers.add_parser("enc", help="解码")
encode_cencent = encode.add_mutually_exclusive_group(required=True)
encode_cencent.add_argument("--text", help="文本", default=None)
encode_cencent.add_argument("--text-file", help="文本文件", default=None)
encode_out_path = encode.add_argument("--out-path", help="输出路径", default="./out/out.png")
encode_is_insert = encode.add_argument("--insert", help="嵌入到某一大图", default=None)

decode = subparsers.add_parser("dec", help="编码")
decode_img = decode.add_argument("--img", help="需解码图片", required=True)
decode_token = decode.add_argument("--token", help="解码嵌入图的密钥", default=None)
decode_out_path = decode.add_argument("--out-path", help="输出路径", default=None)

args = parser.parse_args(args)

try:
    try:
        if args.text_file != None:
            text = Path(args.text_file).read_text("gbk")
        else:
            text = args.text
        enc_default = enc.txt2img(text)
        if args.insert == None:
            Image.fromarray(enc_default).save(args.out_path)
        else:
            big_img = enc.array(Image.open(args.insert))
            enc_insert = enc.insert(enc_default, big_img)
            Image.fromarray(enc_insert["result"]).save(args.out_path)
            print("token: ", enc_insert["token"])
    except AttributeError:
        pass

    try:
        if args.img != None:
            img = dec.array(Image.open(args.img))
            if args.token != None:
                img = dec.fetch(img, int(args.token, base=16))
                text = dec.img2txt(img)
            else:
                text = dec.img2txt(img)
            if args.out_path == None:
                print(text)
            else:
                Path(args.out_path).write_text(text, "gbk")
    except AttributeError:
        pass

except FileNotFoundError:
    print("错误：文件不存在")
