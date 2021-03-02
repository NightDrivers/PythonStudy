# -*- coding: utf-8 -*-


import argparse
import os
import shutil
from script import ShellCommand
import subprocess
import re
import time

identity = "com.idprt.tspl.printer.mac.driver"
version = "1.3.3"
bundle_name = "idprt-tspl-printer-mac-driver"
codesign_identity = "Developer ID Application: Xiamen Hanin Electronic Technology Co., Ltd. (976NLVLZMW)"
install_sign_identity = "Developer ID Installer: Xiamen Hanin Electronic Technology Co., Ltd. (976NLVLZMW)"
developer_name = "ios@prttech.com"
developer_password = "solr-vnoz-tzpu-pdmr"
developer_team = "976NLVLZMW"


def parse_argv():
    __parse = argparse.ArgumentParser()
    __parse.add_argument("--identity", required=True, help="包id")
    __parse.add_argument("--version", required=True, help="版本")
    __parse.add_argument("--bundle_name", required=True, help="包名")
    __parse.add_argument("--codesign_identity", help="代码签名id")
    __parse.add_argument("--install_sign_identity", help="安装包签名id")
    __parse.add_argument("--developer_account", help="开发账号")
    __parse.add_argument("--developer_password", help="开发账号密码")
    __parse.add_argument("--developer_team", help="开发团队id")

    return __parse.parse_args()


def get_notarize_info(request_uuid: str, function):
    global developer_name, developer_password
    notarize_result_cmd = "xcrun altool --notarization-info {0} " \
                          "--username {1} " \
                          "--password {2}"
    notarize_result_cmd = notarize_result_cmd.format(request_uuid, developer_name, developer_password)
    print("查询认证结果")
    flag, result = ShellCommand.excute_shell(notarize_result_cmd, verbose=True)
    if flag != 0:
        print("认证信息查询失败")
        exit(-1)
    pairs = re.findall("\\w[^\\n]*?: [^\\n]+", result, re.RegexFlag.DOTALL)
    dic = dict()
    for pair in pairs:
        items = pair.split(": ")
        dic[items[0]] = items[1]
    status = dic["Status"]
    if status is None:
        print("notarization info Status not found")
        exit(-1)
    else:
        if status == "in progress":
            print("稍后查询...")
            time.sleep(30)
            get_notarize_info(request_uuid, function)
        elif status == "success":
            function(dic)
        else:
            exit(-1)


def staple_ticket(package: str, notarize_info: dict):
    os.system("open {0}".format(notarize_info["LogFileURL"]))
    cmd = "xcrun stapler staple {0}".format(package)
    flag, result = ShellCommand.excute_shell(cmd, verbose=True)
    if flag != 0:
        exit(-1)


if __name__ == '__main__':

    if os.path.exists("build"):
        shutil.rmtree("build")
    os.mkdir("build")

    argv = parse_argv()

    identity = argv.identity
    version = argv.version
    bundle_name = argv.bundle_name

    if argv.codesign_identity is not None:
        codesign_identity = argv.codesign_identity

    if argv.install_sign_identity is not None:
        install_sign_identity = argv.install_sign_identity

    if argv.developer_account is not None:
        developer_account = argv.developer_account

    if argv.developer_password is not None:
        developer_password = argv.developer_password

    if argv.developer_team is not None:
        developer_team = argv.developer_team

    home = subprocess.getoutput("pwd")

    ppd_dir = "{0}/roots/Library/Printers/PPDs/Contents/Resources".format(home)

    for item in os.listdir(ppd_dir):
        if item.endswith(".ppd"):
            os.system("gzip {0}/{1}".format(ppd_dir, item))

    code_dir = "{0}/roots/usr/libexec/cups/filter".format(home)
    for item in os.listdir(code_dir):
        if item.startswith("."):
            continue
        cmd = "codesign --force --verify --verbose " \
              "--sign \"{0}\" " \
              "{1} --deep --options runtime --timestamp"
        cmd = cmd.format(codesign_identity, code_dir + "/" + item)
        flag, result = ShellCommand.excute_shell(cmd, verbose=True)
        if flag != 0:
            print("{0}代码签名失败".format(item))
            exit(-1)

    install_cmd = "pkgbuild " \
                  "--root roots/ " \
                  "--scripts scripts/install " \
                  "--identifier {0}.Install " \
                  "--version {1} " \
                  "--ownership recommended " \
                  "build/{2}.pkg"
    install_cmd = install_cmd.format(identity, version, bundle_name)
    flag, result = ShellCommand.excute_shell(install_cmd, verbose=True)
    if flag != 0:
        print("Install包导出失败")
        exit(-1)

    uninstall_cmd = "pkgbuild " \
                    "--root roots/ " \
                    "--scripts scripts/uninstall " \
                    "--identifier {0}.Uninstall " \
                    "--version {1} " \
                    "--ownership recommended " \
                    "build/uninstall-{2}.pkg"
    uninstall_cmd = uninstall_cmd.format(identity, version, bundle_name)
    flag, result = ShellCommand.excute_shell(uninstall_cmd, verbose=True)
    if flag != 0:
        print("Uninstall包导出失败")
        exit(-1)

    package_cmd = "productbuild " \
                  "--distribution Distribution.xml " \
                  "--package-path build " \
                  "--resources resources " \
                  "--identifier {0} " \
                  "--version {1} " \
                  "--sign \"{2}\" " \
                  "build/{3}-v{1}.pkg"
    package_cmd = package_cmd.format(identity, version, install_sign_identity, bundle_name)
    print(package_cmd)
    flag, result = ShellCommand.excute_shell(package_cmd, verbose=True)
    if flag != 0:
        print("打包失败")
        exit(-1)

    notarize_cmd = "xcrun altool --notarize-app " \
                   "--primary-bundle-id {0} " \
                   "--username {1} " \
                   "--password {2} " \
                   "--file build/{3}-v{4}.pkg " \
                   "-itc_provider {5} &> tmp"
    notarize_cmd = notarize_cmd.format(identity, developer_name, developer_password, bundle_name, version, developer_team)
    print(notarize_cmd)
    flag, result = ShellCommand.excute_shell(notarize_cmd, verbose=True)
    if flag != 0:
        print("包认证失败")
        exit(-1)

    file = open("tmp")
    request_uuid = ""
    for item in file:
        if item.startswith("RequestUUID = "):
            items = item.split(" = ")
            print(items)
            request_uuid = items[1][:-1]
    if len(request_uuid) == 0:
        print("RequestUUID not found in tmp")
        exit(-1)

    get_notarize_info(request_uuid, lambda info: staple_ticket("build/{0}-v{1}.pkg".format(bundle_name, version), info))
