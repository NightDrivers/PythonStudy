# -*- coding: utf-8 -*-
import openpyxl
import os
import subprocess
import argparse
from openpyxl.styles import Alignment
import re


line_localize_rex = '^".?" = ".?";\\n$'
excel_path = ""
format_string_placeholder_rex = '%@|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*[diouxXcsb]|%[#\\-+ 0]?[0-9*]*\\.?[0-9*]*L?[fFeEgGaA]'


def localize_export(root_path: str, mode_name: str, strings_name: str):
    global excel_path
    dirs = []
    for item in os.listdir(root_path):
        if item.endswith('.lproj'):
            temp = item[:-6]
            if temp != 'Base' and temp != 'zh-Hans':
                dirs.append(temp)
    if len(dirs) == 0:
        print('没有找到翻译相关文件')
        exit(-1)
    print(dirs)
    dic = dict()
    keys = set()
    for lang in dirs:
        path = '{0}/{1}.lproj/{2}.strings'.format(root_path, lang, strings_name)
        file = open(path)
        content_dic = dict()
        for line in file:
            # if re.match(line_localize_rex, line, re.RegexFlag.DOTALL):
            pairs = line.split(' = ')
            key = pairs[0][1:-1]
            content_dic[key] = pairs[1][1:-3]
            if not keys.__contains__(key):
                keys.update({key})
        print(len(content_dic))
        dic[lang] = content_dic
    # for item in keys:
    #     print(item)
    print(len(keys))
    keys_sorted = sorted(keys)

    if os.path.exists(excel_path):
        wb = openpyxl.load_workbook(filename=excel_path)
        if wb.sheetnames.__contains__(mode_name):
            ws = wb[mode_name]
            wb.remove(ws)
        ws = wb.create_sheet(mode_name)
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = mode_name
    ws.sheet_format.defaultColWidth = 50

    langs_sorted = sorted(dirs)
    langs_sorted.insert(0, '中文')
    for i in range(0, len(langs_sorted)):
        for j in range(1, len(keys_sorted) + 2):
            temp_lang = langs_sorted[i]
            cell = ws.cell(row=j, column=i + 1)
            if j == 1:
                cell.value = temp_lang
            else:
                key = keys_sorted[j - 2]
                if i == 0:
                    cell.value = key
                else:
                    temp_dict = dic[temp_lang]
                    cell.value = temp_dict[key]
            cell.alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

    wb.save(excel_path)


def localize_import(root_path: str, mode_name: str, strings_name: str):
    global excel_path, format_string_placeholder_rex
    if not os.path.exists(excel_path):
        print('翻译文件不存在')
        exit(-1)
    wb = openpyxl.load_workbook(filename=excel_path)
    if not wb.sheetnames.__contains__(mode_name):
        print('未找到对应模块')
        exit(-1)
    # ws = wb.create_sheet()
    ws = wb[mode_name]
    print('max row {0}'.format(ws.max_row))
    print('max column {0}'.format(ws.max_column))
    max_row = ws.max_row
    max_column = ws.max_column

    for i in range(2, max_column+1):
        lang = ws.cell(row=1, column=i).value
        if lang is None or len(lang) == 0:
            continue
        string_file_path = '{0}/{1}.lproj/{2}.strings'.format(root_path, lang, strings_name)
        string_file = open(string_file_path, 'wt')
        for j in range(2, max_row+1):
            key = ws.cell(row=j, column=1).value
            value = ws.cell(row=j, column=i).value
            if value is None:
                value = ""
            if value != "":
                key_placeholder_list = re.findall(format_string_placeholder_rex, key, re.RegexFlag.DOTALL)
                if len(key_placeholder_list) != 0:
                    value_placeholder_list = re.findall(format_string_placeholder_rex, value, re.RegexFlag.DOTALL)
                    if key_placeholder_list != value_placeholder_list:
                        print("占位符不匹配 模块: {0} 位置: 第{1}行 语言: {2}".format(mode_name, j, lang))
                        value = ""
            temp = '"{0}" = "{1}";\n'.format(key, value)
            string_file.write(temp)
        string_file.close()


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("modeName", help="翻译模块名称")
    __parse.add_argument("stringsName", help="翻译文件名称")
    __parse.add_argument("path", help="翻译文件路径")
    __parse.add_argument("-forImport", help="将翻译导入项目", action="store_true")
    __parse.add_argument("-excelDir", help="翻译Excel文件目录", default="/Users/ldc/Desktop/翻译")
    return __parse.parse_args()


if __name__ == '__main__':
    argv = parse_argv()
    mode_name = argv.modeName
    home_dir = argv.excelDir
    excel_path = home_dir + "/翻译汇总.xlsx"
    strings_name = argv.stringsName
    root_path = subprocess.getoutput("cd {0};pwd".format(argv.path))
    if argv.forImport:
        localize_import(root_path, mode_name, strings_name)
    else:
        if not os.path.exists(home_dir):
            os.mkdir(home_dir)
        localize_export(root_path, mode_name, strings_name)