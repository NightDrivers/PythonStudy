# -*- coding: utf-8 -*-
import re
import glob
import os
import argparse
import shutil


def convert_comment(filepath, lang):
    with open(filepath, "rt+") as file:
        text = file.read()
        # 多行注释 支持/* */ /*! */ /** */ 注释其他行必须" *  "开头
        muti_line_comment_rex = "/\\*[\\*!]?\n(.*?) \\*/"
        muti_line_content_rex = " \\*  \\\\~" + lang + "\n(.*?)" + "( \\*  \\\\~| \\*/)"
        muti_line_comments = re.findall(muti_line_comment_rex, text, re.RegexFlag.DOTALL)
        for muti_line_comment in muti_line_comments:
            results = re.findall(muti_line_content_rex, muti_line_comment, re.RegexFlag.DOTALL)
            if len(results) > 0:
                result = results[0]
                text = text.replace(muti_line_comment, result[0], 1)
        # 单行注释 ///< //!< 格式
        single_line_comment_rex = "//[/!]< *(.*?)\n"
        single_line_content_rex = "\\\\~" + lang + " *(.*?)( *\\\\~|\n)"
        single_line_comments = re.findall(single_line_comment_rex, text, re.RegexFlag.DOTALL)
        for single_line_comment in single_line_comments:
            results = re.findall(single_line_content_rex, single_line_comment, re.RegexFlag.DOTALL)
            if len(results) > 0:
                result = results[0]
                text = text.replace(single_line_comment, result[0], 1)
        file.seek(0, 0)
        file.truncate(len(text))
        file.write(text)


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("framework", help="库文件路径")
    return __parse.parse_args()


if __name__ == '__main__':
    # parser = parse_argv()
    # framework_source_path = parser.framework
    framework_source_path = "/Users/ldc/Desktop/Demo/Doc/Doc.framework"
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
