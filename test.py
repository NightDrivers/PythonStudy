# -*- coding: utf-8 -*-
import re


def re_replace(content_text, occurrence_rex, content_rex):
    source = content_text
    searchpos = 0
    while True:
        occurrence_match = occurrence_rex.search(source, pos=searchpos)
        if occurrence_match is None:
            break
        else:
            occurrence_text = occurrence_match.group(1)
            # print(result)
            content_match = content_rex.search(occurrence_text)
            if content_match is None:
                print("not match content")
                searchpos = occurrence_match.end(0)
                continue
            else:
                print(repr(content_match.group(1)))
                print("--------")
                source = source[:occurrence_match.start(1)] + content_match.group(1) + source[occurrence_match.end(1):]
                searchpos = occurrence_match.end(0) - len(occurrence_text) + len(content_match.group(1))
    return source


if __name__ == '__main__':
    a = "abcdefg"
    rex = "a(?:(ef)|(b(c)))(?:d)"
    m = re.search(rex, a)
    print(m.group(0))
    print(m.group(1))
    print(m.group(2))
    print(m.group(3))
    with open("/Users/ldc/Desktop/外发文件/Hipos/HiPosExample/HiPosSDK.framework/Headers/HiPosPrinter.h", "rt+") as file:
        text = file.read()
        multi_line_comment_re = re.compile("/\\*[\\*!]?\n(.*?) \\*/", re.RegexFlag.DOTALL)
        multi_line_content_rex = "[^\n]*\\\\~" + "english" + "\n(.*?)" + "([^\n]*\\\\~|$)"
        multi_line_content_re = re.compile(multi_line_content_rex, re.RegexFlag.DOTALL)
        re_replace(text, multi_line_comment_re, multi_line_content_re)
