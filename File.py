# coding=UTF-8

if __name__ == "__main__":
    f = open("file", "w")
    f.write("hello world!\n")
    f.write("luna\n")
    # 获取文件指针当前位置
    d = f.tell()
    f.close()
    f = open("file", "r")
    print("文件指针当前位置{}".format(d))
    # 调整文件指针当前位置，offset偏移量, whence偏移量参考位置 0为起始位置 1为当前位置 2为文件结束位置
    f.seek(0, 0)
    print("\nread:")
    c = f.read()
    print(repr(c))
    f.seek(0, 0)
    print("\nfor in:")
    for line in f:
        print(repr(line))
    f.seek(0)
    d = f.readlines()
    print("\nreadlines:\n{}".format(d))
    f.seek(0)
    g = f.readline()
    print("\nreadline:")
    while g:
        print(repr(g))
        g = f.readline()
    f.close()

    print("\nwith as:")
    with open("file", "r") as fi:
        fi.seek(6)
        h = fi.readline()
        print(repr(h))
    print(fi.closed)
