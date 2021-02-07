# -*- coding: utf-8 -*-
import openpyxl
import os
import subprocess
import argparse
import uuid
import re


if __name__ == '__main__':
    text = '已选%u, 打印%#a份, 预计%-i张, 长度%-.fcm'
    rex = '%[#-+ 0]?[0-9]*\\.?[diouxXfFeEgGaAcsb@]'
    rex = '%@|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*[diouxXfcsb]|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*L?[fFeEgGaA]'
    for item in re.findall(rex, text, re.RegexFlag.DOTALL):
        print(item)
