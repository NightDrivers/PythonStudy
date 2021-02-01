# -*- coding: utf-8 -*-
import openpyxl
import os
import subprocess
import argparse
import uuid
import re

file_count = 0
text_count_need_localize = 0
text_in_code_set = set()
text_need_localize_set = set()
place_holder = str(uuid.uuid1())
white_list_place_holder = str(uuid.uuid1())
white_prefix_rex = 'HLog.share.write\\(|print\\('
verbose = True
codeSuffix = ".swift"


def find_text(path: str, rex: str, function):
    global text_need_localize_set, place_holder, verbose, white_list_place_holder, white_prefix_rex
    file = open(path)
    for line in file:
        temp = line.replace('\\"', place_holder)
        temp = white_list_place_holder.join(re.split(white_prefix_rex, temp, re.RegexFlag.DOTALL))
        results = re.findall(rex, temp, re.RegexFlag.DOTALL)
        for result in results:
            result_txt = result.replace(place_holder, '\\"')
            function(result_txt)


if __name__ == '__main__':
    path = "/Users/ldc/Desktop/svn/HPrintiOS/Trunk/HPrintiOS/HPrint/HPrint/module/printers/FT800/ViewController/FT800ConnectViewController.swift"
    localize_rex = '(?<!{0})"[^"]+?"'.format(white_list_place_holder)
    find_text(path, localize_rex, lambda result: print(result) )
