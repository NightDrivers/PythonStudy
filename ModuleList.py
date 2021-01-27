# -*- coding:utf-8 -*-
import parser  # 3.2新出命令行解析模块 https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
import glob
import os


if __name__ == '__main__':
    path = os.system("pwd")
    items = glob.glob("**/*.pkg", recursive=True)
    print(items)
