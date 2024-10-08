# -*- coding:utf-8 -*-
import argparse
# 3.2新出命令行解析模块 https://docs.python.org/3/howto/argparse.html#introducing-positional-arguments
import subprocess
import os
import sys
from datetime import datetime
# 可用于multipart/form-data格式请求
import requests_toolbelt
import requests
import json
from script import ShellCommand


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("scheme")
    __parse.add_argument("-deleteArchive", "-da", help="删除XcArchive文件", action="store_true")
    __parse.add_argument("-localIpa", "-li", help="只存储ipa包到本地，不上传蒲公英", action="store_true")
    __parse.add_argument("-exportPath", "-ep", help="打包文件导出路径", default="~/Documents/")
    __parse.add_argument("-verbose", "-v", help="打印执行信息", action="store_true")
    __parse.add_argument("-workspace", "-w", help="workspace Name")
    __parse.add_argument("-configuration", help="build configuration NAME")
    __parse.add_argument("-buildName", "-bn", help="蒲公英应用名称")
    __parse.add_argument("-exportMethod", "-m", help="导出方式", default="enterprise")
    __parse.add_argument("-pgyerDomain", "-pd", help="蒲公英域名", default="www.xcxwo.com")
    return __parse.parse_args()


def upload_ipa_to_pgyer(domain: str, path: str, appname: str = None):
    """
    将ipa包发送至蒲公英，接口文档
    https://www.pgyer.com/doc/view/api#uploadApp
    https://www.xcxwo.com/doc/view/api#uploadApp
    """
    apikey = "4b704ea49aeb3d2647fc5e32a6b7de63"
    url = "https://{0}/apiv2/app/upload".format(str)
    encoder = requests_toolbelt.multipart.MultipartEncoder(fields={
        'file': (path, open(path, "rb"))
    })
    params = {
        '_api_key': apikey,
        # 'file': (path, open(path, "rb"))
    }
    if appname is not None:
        params["buildName"] = appname
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        'Content-Type': encoder.content_type,
    }
    param = {"headers": header, "params": params}
    response = requests.post(url, data=encoder.to_string(), **param)
    # print(response.text)
    d = json.loads(response.text)
    if d["code"] == 0:
        return 0, "https://${0}/".format(domain) + d["data"]["buildShortcutUrl"]
    else:
        return -1, d["message"]


if __name__ == '__main__':
    # 判断用于安装包导出的配置文件是否存在
    argv = parse_argv()
    home = subprocess.getoutput("cd ~;pwd")
    # ipa导出配置文件，模版见XcarchiveExportOptions.plist
    xcarchiveExportOptionsPath = '{0}/Desktop/XcarchiveExport/{1}.plist'.format(home, argv.exportMethod)
    if not os.path.exists(xcarchiveExportOptionsPath):
        print("xcodebuild -exportArchiv导出配置文件不存在: " + xcarchiveExportOptionsPath)
        sys.exit(-1)
    is_verbose = argv.verbose
    # 编译打包生成xcarchive文件
    now = datetime.today()
    archivePath = "~/Library/Developer/Xcode/Archives"
    archivePath += now.strftime("/%Y-%m-%d/")
    exportPath = argv.exportPath + argv.scheme + now.strftime("\\ %Y-%m-%d\\ %H-%M-%S")
    cmd = "xcodebuild archive -allowProvisioningUpdates "
    if argv.workspace:
        cmd += "-workspace " + argv.workspace + " "
    cmd += "-scheme " + argv.scheme + " "
    if argv.configuration:
        cmd += "-configuration " + argv.configuration + " "
    archivePath += argv.scheme + now.strftime("\\ %Y-%m-%d,\\ %I.%M%p") + ".xcarchive"
    cmd += "-archivePath " + archivePath
    print("archiving...")
    flag, output = ShellCommand.excute_shell(cmd, is_verbose)
    if flag != 0:
        print("Archive Fail")
        sys.exit(1)
    # 判断签名使用的证书是否正确，以下为enterprise对应的开发证书，根据自己证书进行修改
    rex = '"Apple.*?\\([0-9a-zA-Z]{10}\\)"'
    # sign_ids = re.findall(rex, output, re.RegexFlag.DOTALL)
    # if len(sign_ids) < 1 or sign_ids[0] != '"Apple Development: Rongjian Qiu (L5J53ML6QB)"':
    #     if argv.deleteArchive:
    #         cmd = "rm -r " + archivePath
    #         subprocess.getstatusoutput(cmd)
    #     print("error sign identity: " + sign_ids[0])
    #     sys.exit(1)
    # 将xcarchive文件导出为可安装文件包
    cmd = "xcodebuild -exportArchive -allowProvisioningUpdates "
    cmd += "-archivePath " + archivePath + " "
    cmd += "-exportPath " + exportPath + " "
    cmd += "-exportOptionsPlist " + xcarchiveExportOptionsPath
    print(cmd)
    print("exporting...")
    flag, output = ShellCommand.excute_shell(cmd, is_verbose)
    if argv.deleteArchive:
        cmd = "rm -r " + archivePath
        subprocess.getstatusoutput(cmd)
    if flag != 0:
        print("Export Fail")
        sys.exit(1)
    else:
        os.system("open " + exportPath)
    if not argv.localIpa:
        print("uploading ipa...")
        result = upload_ipa_to_pgyer(
            argv.pgyerDomain,
            subprocess.getoutput("cd " + argv.exportPath + ";pwd") + "/" +
            argv.scheme + now.strftime(" %Y-%m-%d %H-%M-%S/") + argv.scheme + ".ipa",
            argv.buildName
        )
        if result[0] == 0:
            os.system("open " + result[1])
        else:
            print(result[1])
