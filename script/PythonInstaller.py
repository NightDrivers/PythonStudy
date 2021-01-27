# -*- coding:utf-8 -*-
import ShellCommand
import argparse
import os
import shutil


def parse_argv():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="要编译的python文件")
    parser.add_argument("-destination", "-d", help="编译后可执行文件放置目录", default="/usr/local/custom/")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_argv()
    file = args.file
    destination = args.destination
    # file = "Xcarchive.py"
    # destination = "/usr/local/custom/"
    excutename = file.split(".")[0]
    flag, output = ShellCommand.excute_shell("pyinstaller -F " + file, True)
    if flag == 0:
        os.remove(excutename + ".spec")
        shutil.copyfile("./dist/" + excutename, destination + excutename)
        ShellCommand.excute_shell("chmod 755 " + destination + excutename)
