# -*- coding: utf-8 -*-
import re


if __name__ == '__main__':
    rex = "[^\\d]+"
    a = "ab2bc34werqwe1232"
    b = re.findall(rex, a, re.RegexFlag.DOTALL)
    print(b)
