# -*- coding:utf-8 -*-
import os
import sys
import argparse


def resolve_arg():
    parser = argparse.ArgumentParser()
    parser.add_argument("filePath", help="读取文件路径", type=str)
    group = parser.add_mutually_exclusive_group(**{"required": True})
    group.add_argument("-hex", help="十六进制输出", action="store_true")
    group.add_argument("-utf8", "-u", help="utf8输出", action="store_true")
    group.add_argument("-rawutf8", "-r", help="原生utf8输出", action="store_true")
    return parser.parse_args()


def hexrepr(byte: int) -> str:
    return "{0:02x}".format(byte)


if __name__ == '__main__':
    argv = resolve_arg()
    filePath = argv.filePath
    if not os.path.exists(filePath):
        excutePath = os.system("pwd")
        filePath = excutePath + "/" + filePath
        if not os.path.exists(filePath):
            print("未知文件")
            exit(1)
    with open(filePath, mode="rb") as file:
        content = file.read()
        try:
            if argv.hex:
                print(" ".join(map(hexrepr, content)))
            if argv.utf8:
                print(content.decode("utf8"))
            if argv.rawutf8:
                print(repr(content.decode("utf8")))
        except Exception as e:
            print(e)
