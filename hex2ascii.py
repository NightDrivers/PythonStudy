# coding=utf-8
import sys


if __name__ == '__main__':
    if len(sys.argv) > 1:
        hex_list = sys.argv
        hex_list.pop(0)
        print(bytearray.fromhex(" ".join(hex_list)).decode("utf-8"))
