# -*- coding: utf-8 -*-
import re


def convert_comment(filepath, lang):
    with open(filepath, "rt+") as file:
        text = file.read()
        rex = "/\\*[\\*!]?.*? \\*/"
        rex1 = " \\*  \\\\~" + lang + ".*?" + " \\*  \\\\~"
        rex2 = " \\*  \\\\~" + lang + ".*?" + " \\*/"
        items = re.findall(rex, text, re.RegexFlag.DOTALL)
        print(items)
        for item in items:
            if item[2:3] == "\n":
                prefix = item[:3]
            else:
                prefix = item[:4]
            results = re.findall(rex1, item, re.RegexFlag.DOTALL)
            if len(results) > 0:
                content = results[0]
                content = content[7+len(lang):-6]
                content = prefix + content + " */"
                print(content)
                text = text.replace(item, content, 1)
                continue
            else:
                results = re.findall(rex2, item, re.RegexFlag.DOTALL)
                if len(results) > 0:
                    content = results[0]
                    content = content[7 + len(lang):-3]
                    content = prefix + content + " */"
                    print(content)
                    text = text.replace(item, content, 1)
                    continue
            print("not found language comment...")
            print(item)
            # text = text.replace(item + "\n", "", 1)
        file.seek(0, 0)
        file.truncate(len(text))
        file.write(text)


if __name__ == '__main__':
    convert_comment("/Users/ldc/Desktop/Demo/Doc/Doc/Dispatcher.h", "english")
