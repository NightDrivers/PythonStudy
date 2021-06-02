# coding=UTF-8
import argparse
import os
import re
import uuid
import subprocess


file_count = 0
text_count_need_localize = 0
text_in_code_set = set()
text_need_localize_set = set()
place_holder = str(uuid.uuid1())
white_list_place_holder = str(uuid.uuid1())
white_prefix_rex = 'HLog.share.write\\(|print\\('
verbose = True
codeSuffix = ".swift"


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("project", help="需要导出翻译文本的项目文件路径")
    __parse.add_argument("localizedStrings", help="需要导入翻译的文件路径")
    __parse.add_argument("-verbose", help="打印执行信息", action="store_true")
    __parse.add_argument("-textSuffix", help="项目翻译文本代码后缀", default="\\.localized")
    __parse.add_argument("-codeSuffix", help="代码文件后缀", default=".swift")
    __parse.add_argument("-ignorePrefix", help="忽略跟随该前缀的文本", default=None)
    return __parse.parse_args()


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


def find_file(path: str, rex: str, function):
    global file_count, verbose, codeSuffix
    file_list = os.listdir(path)
    for item in file_list:
        path_new = path + "/" + item
        if os.path.isdir(path_new):
            if item.lower() == "test":
                continue
            else:
                find_file(path_new, rex, function)
        elif os.path.isfile(path_new):
            if item.endswith(codeSuffix):
                file_count = file_count + 1
                if verbose:
                    print("找到新的代码文件: {0}".format(path_new))
                find_text(path_new, rex, function)
        else:
            break


def add_localized_text(text: str):
    global text_count_need_localize, text_need_localize_set
    temp_set = {text}
    text_count_need_localize = text_count_need_localize + 1
    if not text_need_localize_set.issuperset(temp_set):
        if verbose:
            print("找到新的需要翻译文本: {0}".format(text))
        text_need_localize_set.update(temp_set)


def add_code_text(text: str):
    global text_in_code_set
    temp_set = {text}
    if not text_in_code_set.issuperset(temp_set):
        if verbose:
            print("找到新文本: {0}".format(text))
        text_in_code_set.update(temp_set)


if __name__ == "__main__":
    argv = parse_argv()
    verbose = argv.verbose
    codeSuffix = argv.codeSuffix

    localized_strings_path = argv.localizedStrings
    if not os.path.isfile(localized_strings_path):
        localized_strings_path = subprocess.getoutput("pwd") + "/" + localized_strings_path
        if not os.path.isfile(localized_strings_path):
            print("翻译文件不存在")
            exit(1)

    if argv.ignorePrefix is not None:
        white_prefix_rex = '{0}|{1}'.format(white_prefix_rex, argv.ignorePrefix)
    project_path = subprocess.getoutput("cd {0};pwd".format(argv.project))
    localize_rex = '(?<!{0})"[^"]+?"(?={1})'.format(white_list_place_holder, argv.textSuffix)
    find_file(project_path, localize_rex, lambda result: add_localized_text(result))
    find_file(project_path, '(?<!{0})"[^"]+?"'.format(white_list_place_holder), lambda result: add_code_text(result))

    print("---------------")
    print("代码文件数量: {0}".format(file_count))
    print("代码中所有文本数量: {0}".format(len(text_in_code_set)))
    print("代码中需要翻译的文本数量: {0}".format(text_count_need_localize))
    print("翻译文件中key值数量: {0}".format(len(text_need_localize_set)))
    text_without_localize_set = text_in_code_set.difference(text_need_localize_set)
    print("不需要翻译的文本数量: {0}".format(len(text_without_localize_set)))
    for item in text_without_localize_set:
        if not re.match('"[\\x20\\x21\\x23-\\x7e]+"', item, re.RegexFlag.DOTALL):
            print("不需要翻译的文本: {0}".format(item))
    if not text_in_code_set.issuperset(text_need_localize_set):
        _temp = text_need_localize_set.difference(text_in_code_set)
        for item in _temp:
            print(text_in_code_set.__contains__(item))
            print("在文本中未找到的翻译文本: {0}".format(item))
        print("代码中文本不是需要翻译文本的超级，出现未知错误")
        exit(-1)
    # exit(0)

    strings_file = open(localized_strings_path)
    strings_set = set()
    dic = dict()
    keys = []
    for item in strings_file:
        items = item.split(" = ")
        if len(items) != 2:
            continue
        temp = items[0]
        temp_set = {temp}
        dic[temp] = items[1]
        if strings_set.issuperset(temp_set):
            print("翻译文件重复的翻译文本: {0}".format(temp))
        else:
            keys.append(temp)
            strings_set.update(temp_set)

    strings_file.close()
    print("原翻译文件有效文本数量: {0}".format(len(strings_set)))

    text_set_invalid = strings_set.difference(text_need_localize_set)

    print("无用的翻译文本数量: {0}".format(len(text_set_invalid)))
    for item in text_set_invalid:
        print("删除无用文本: {0}".format(item))
        keys.remove(item)

    text_set_more = text_need_localize_set.difference(strings_set)

    print("未翻译文本数量: {0}\n".format(len(text_set_more)))
    for item in text_set_more:
        print("添加缺少的翻译文本: {0}".format(item))
        keys.append(item)
        dic[item] = "\"\";\n"

    strings_file_write = open(localized_strings_path, mode="wt")
    keys.sort()
    for key in keys:
        strings_file_write.write(key + " = " + dic[key])
    strings_file_write.close()


