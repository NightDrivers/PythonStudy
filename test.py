# -*- coding: utf-8 -*-
import openpyxl
import os
import subprocess
import argparse
import uuid
import re
from script import ShellCommand


if __name__ == '__main__':
    print(ShellCommand.excute_shell("cd /usr;pwd;"))
    print(ShellCommand.excute_shell("pwd;"))
