# -*- coding: utf-8 -*-
# @Date:2022/07/03 0:23
# @Author: Lu
# @Description convert utils
from typing import List

_global_encodes = [None, 'utf-8', 'gbk', 'gb18030', 'gb2312']


def read_bin(file_path: str) -> bytes:
    f = open(file_path, 'rb')
    binary = f.read()
    f.close()
    return binary


def read_text(file_path: str) -> str:
    f = open(file_path, 'rb')
    binary = f.read()
    f.close()
    return bin2text(binary)


def bin2text(binary: bytes, encodes: List = None) -> str:
    encodes = _global_encodes if not encodes else encodes
    for en in encodes:
        try:
            text = binary.decode(encoding=en)
            return text
        except Exception as e:
            pass


def text2bin(text: str, encodes: List = None) -> bytes:
    encodes = _global_encodes if not encodes else encodes
    for en in encodes:
        try:
            binary = text.encode(en)
            return binary
        except Exception as e:
            pass
