# -*- coding:utf-8 -*-
from script import ShellCommand
import argparse
import os
import shutil
import subprocess


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
    work_dir = subprocess.getoutput("pwd")
    paths = file.split("/")
    file_name = paths[len(paths)-1]
    excutename = file_name.split(".")[0]
    flag, output = ShellCommand.excute_shell("pyinstaller -F " + file, True)
    if flag == 0:
        os.remove(work_dir + "/" + excutename + ".spec")
        shutil.copyfile(work_dir + "/" + "./dist/" + excutename, destination + excutename)
        ShellCommand.excute_shell("chmod 755 " + destination + excutename)
