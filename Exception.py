# -*- coding:utf-8 -*-


def hex_value(hex_byte: int) -> int:
    if type(hex_byte) is not int:
        # print("hex_byte must be in")
        raise TypeError("hex_byte must be in")
    else:
        if hex_byte in range(0x30, 0x3a):
            return hex_byte - 0x30
        elif hex_byte in range(0x41, 0x5b):
            return hex_byte - 0x41
        elif hex_byte in range(0x61, 0x7b):
            return hex_byte - 0x61
        else:
            raise ValueError(("hex byte must be in" 
                              " range(0x30, 0x3a)"  # 0-9
                              " or range(0x41, 0x5b)"  # A-Z
                              " or range(0x61, 0x7b)"  # a-z
                              ))


if __name__ == '__main__':
    try:
        flag = hex_value(0x29)
        print(flag)
    except Exception as ex:
        print(ex)
    finally:
        print("---")
