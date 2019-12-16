# -*- coding:utf-8 -*-
import subprocess


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