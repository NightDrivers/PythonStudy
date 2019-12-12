# -*- coding: utf-8 -*-
import re
import glob
import os
import argparse
import shutil
import cProfile


def re_replace(content_text, occurrence_rex, content_rex):
    source = content_text
    searchpos = 0
    while True:
        occurrence_match = occurrence_rex.search(source, pos=searchpos)
        if occurrence_match is None:
            break
        else:
            occurrence_text = occurrence_match.group(1)
            # 当content_rex中最后一个分组使用"$"时，而且原occurrence_text中最后一个字符是"\n"时，这个"\n"无法匹配到
            # 暂时添加"\n"字符抵消这个情况
            content_match = content_rex.search(occurrence_text + "\n")
            if content_match is None:
                searchpos = occurrence_match.end(0)
                continue
            else:
                source = source[:occurrence_match.start(1)] + content_match.group(1) + source[occurrence_match.end(1):]
                searchpos = occurrence_match.end(0) - len(occurrence_text) + len(content_match.group(1))
    return source


def convert_comment(filepath, lang):
    with open(filepath, "rt+") as file:
        text = file.read()
        # 多行注释 支持/* */ /*! */ /** */
        multi_line_comment_re = re.compile("/\\*[\\*!]?\n(.*?) \\*/", re.RegexFlag.DOTALL)
        multi_line_content_rex = "[^\n]*\\\\~" + lang + "\n(.*?)" + "([^\n]*\\\\~|$)"
        multi_line_content_re = re.compile(multi_line_content_rex, re.RegexFlag.DOTALL)
        text = re_replace(text, multi_line_comment_re, multi_line_content_re)
        # 单行注释 ///< //!< 格式
        single_line_comment_rex = re.compile("//[/!]< *(.*?)\n", re.RegexFlag.DOTALL)
        single_line_content_rex = re.compile("\\\\~" + lang + " *(.*?)( *\\\\~|$)", re.RegexFlag.DOTALL)
        text = re_replace(text, single_line_comment_rex, single_line_content_rex)
        file.seek(0, 0)
        file.truncate(len(text))
        file.write(text)


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("framework", help="库文件路径")
    return __parse.parse_args()


def main():
    # parser = parse_argv()
    # framework_source_path = parser.framework
    framework_source_path = "/Users/ldc/Desktop/外发文件/Hipos/HiPosExample/HiPosSDK.framework"
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
        langdir = "sdk/" + lang
        if os.path.exists(langdir):
            shutil.rmtree(langdir)
        os.mkdir(langdir)
        frameworkpath = langdir + "/" + framework
        shutil.copytree(framework_source_path, frameworkpath)
        paths = glob.iglob(frameworkpath + "/**/*.h", recursive=True)
        # print(paths)
        for path in paths:
            convert_comment(path, lang)
        cmd = "cd " + langdir + ";"
        cmd += "appledoc"
        cmd += " --project-name " + project_name
        cmd += " --project-company " + company_name
        cmd += " --company-id " + company_id
        cmd += " --create-html --no-create-docset --no-install-docset --no-publish-docset"
        cmd += " --output ./ " + framework + ";"
        os.system(cmd)
        os.rename(langdir + "/html", langdir + "/doc")


if __name__ == '__main__':
    # cProfile.run("main()")
    main()
