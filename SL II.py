#!/usr/local/bin/python3.7
# coding=UTF-8
import re
import subprocess
import sys
import time
import os


def excute_shell(command: str, verbose: bool = False):
    params = {"text": True}
    program = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, **params)
    outputs = []
    while program.poll() is None:
        # 当程序退出时，似乎会读取到一个空字符串
        item = program.stdout.readline()
        if verbose:
            print(item, end="")
        outputs.append(item)
    return program.returncode, "".join(outputs)


if __name__ == '__main__':
    r = excute_shell("python YieldStudy.py", True)
    print(r)
    # params = {"text": True}
    # program = subprocess.Popen("python YieldStudy.py", shell=True, stdout=subprocess.PIPE, **params)
    # output = program.communicate()
    # print("-----------------------")
    # print(output)
    # print(program.returncode)
