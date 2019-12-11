# -*- coding: utf-8 -*-
import re
import glob
import os
import argparse
import shutil


def convert_comment(filepath, lang):
    with open(filepath, "rt+") as file:
        text = file.read()
        rex = "/\\*[\\*!]?.*? \\*/"
        rex1 = " \\*  \\\\~" + lang + ".*?" + " \\*  \\\\~"
        rex2 = " \\*  \\\\~" + lang + ".*?" + " \\*/"
        items = re.findall(rex, text, re.RegexFlag.DOTALL)
        # print(items)
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
                # print(content)
                text = text.replace(item, content, 1)
                continue
            else:
                results = re.findall(rex2, item, re.RegexFlag.DOTALL)
                if len(results) > 0:
                    content = results[0]
                    content = content[7 + len(lang):-3]
                    content = prefix + content + " */"
                    # print(content)
                    text = text.replace(item, content, 1)
                    continue
            print("not found language comment...")
            # print(item)
            # text = text.replace(item + "\n", "", 1)
        file.seek(0, 0)
        file.truncate(len(text))
        file.write(text)


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("framework", help="库文件路径")
    return __parse.parse_args()


if __name__ == '__main__':
    parser = parse_argv()
    framework_source_path = parser.framework
    langs = ["chinese", "english"]
    company_name = "hanin"
    company_id = "com.hanin"
    framework = os.path.basename(framework_source_path)
    project_name = ".".split(framework)[0]

    sdkpath = "sdk"
    if os.path.exists(sdkpath):
        shutil.rmtree(sdkpath)
    os.mkdir(sdkpath)

    for lang in langs:
        langDir = "sdk/" + lang
        if os.path.exists(langDir):
            shutil.rmtree(langDir)
        os.mkdir(langDir)
        frameworkpath = langDir + "/" + framework
        shutil.copytree(framework_source_path, frameworkpath)
        paths = glob.iglob(frameworkpath + "/**/*.h", recursive=True)
        # print(paths)
        for path in paths:
            convert_comment(path, lang)
        cmd = "cd " + langDir + ";"
        cmd += "appledoc"
        cmd += " --project-name " + project_name
        cmd += " --project-company " + company_name
        cmd += " --company-id " + company_id
        cmd += " --create-html --no-create-docset --no-install-docset --no-publish-docset"
        cmd += " --output ./ " + framework + ";"
        os.system(cmd)
        os.rename(langDir + "/html", langDir + "/doc")
